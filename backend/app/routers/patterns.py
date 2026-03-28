import json
import os

from fastapi import APIRouter, Depends, HTTPException, status
from groq import Groq
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Attempt, Confidence, Pattern, PatternType, Question, User
from app.schemas import PatternCreate, PatternOut, PatternUpdate

router = APIRouter(prefix="/patterns", tags=["Patterns"])


class PatternRequest(BaseModel):
    user_id: int


class PatternResponse(BaseModel):
    patterns: list[dict]
    summary: str


PATTERN_TYPE_MAP = {
    "edge_case_blindness": PatternType.edge_cases,
    "edge_cases": PatternType.edge_cases,
    "gives_up_early": PatternType.gives_up_early,
    "time_complexity_blindness": PatternType.time_complexity,
    "time_complexity": PatternType.time_complexity,
    "topic_weakness": PatternType.concept_gap,
    "concept_gap": PatternType.concept_gap,
    "inconsistent_recall": PatternType.inconsistent_recall,
}


@router.post("/", response_model=PatternOut, status_code=status.HTTP_201_CREATED)
async def create_pattern(payload: PatternCreate, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, payload.user_id)
    if not user or user.deleted:
        raise HTTPException(status_code=404, detail="User not found")

    pattern = Pattern(**payload.model_dump())
    db.add(pattern)
    await db.commit()
    await db.refresh(pattern)
    return pattern


@router.get("/", response_model=list[PatternOut])
async def list_patterns(
    user_id: int | None = None,
    pattern_type: str | None = None,
    topic: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(Pattern)
    if user_id:
        q = q.where(Pattern.user_id == user_id)
    if pattern_type:
        q = q.where(Pattern.pattern_type == pattern_type)
    if topic:
        q = q.where(Pattern.topic == topic)
    result = await db.scalars(q.order_by(Pattern.detected_at.desc()))
    return result.all()


@router.get("/{pattern_id}", response_model=PatternOut)
async def get_pattern(pattern_id: int, db: AsyncSession = Depends(get_db)):
    pattern = await db.get(Pattern, pattern_id)
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")
    return pattern


@router.patch("/{pattern_id}", response_model=PatternOut)
async def update_pattern(pattern_id: int, payload: PatternUpdate, db: AsyncSession = Depends(get_db)):
    pattern = await db.get(Pattern, pattern_id)
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(pattern, field, value)

    await db.commit()
    await db.refresh(pattern)
    return pattern


@router.delete("/{pattern_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pattern(pattern_id: int, db: AsyncSession = Depends(get_db)):
    pattern = await db.get(Pattern, pattern_id)
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")
    await db.delete(pattern)
    await db.commit()


@router.post("/analyze", response_model=PatternResponse)
async def analyze_patterns(request: PatternRequest, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, request.user_id)
    if not user or user.deleted:
        raise HTTPException(status_code=404, detail="User not found")

    attempts_result = await db.scalars(
        select(Attempt)
        .where(Attempt.user_id == request.user_id)
        .order_by(Attempt.created_at.desc())
        .limit(20)
    )
    attempts = attempts_result.all()

    if len(attempts) < 3:
        return PatternResponse(
            patterns=[],
            summary="Not enough attempts yet. Solve at least 3 questions before pattern analysis.",
        )

    question_ids = list({attempt.question_id for attempt in attempts})
    questions_result = await db.scalars(select(Question).where(Question.id.in_(question_ids)))
    question_map = {question.id: question for question in questions_result.all()}

    attempt_data = []
    for attempt in attempts:
        question = question_map.get(attempt.question_id)
        if not question:
            continue
        attempt_data.append(
            {
                "question": question.title,
                "topic": question.topic,
                "difficulty": question.difficulty.value,
                "expected_time": question.expected_time,
                "time_taken": attempt.time_taken,
                "hints_used": attempt.hints_used,
                "hint_levels_used": attempt.hint_levels_used,
                "test_cases_passed": attempt.test_cases_passed,
                "total_test_cases": attempt.total_test_cases,
                "status": attempt.status.value,
                "attempt_number": attempt.attempt_number,
            }
        )

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is not configured")

    prompt = f"""
                You are an expert DSA coach analyzing a student's learning patterns.

                Here are their recent attempts:
                {json.dumps(attempt_data, indent=2)}

                Analyze these attempts and identify specific weakness patterns.
                Focus on these pattern types:
                1. edge_case_blindness — passes main cases but fails edge cases
                2. gives_up_early — uses level 3 hints too quickly or multiple attempts before trying
                3. time_complexity_blindness — solves correctly but takes much longer than expected
                4. topic_weakness — consistently struggles with a specific topic
                5. inconsistent_recall — solved before but struggling again

                Respond in this exact JSON format only, no other text:
                {{
                "patterns": [
                    {{
                    "type": "pattern_type",
                    "confidence": "low/medium/high",
                    "description": "specific observation about this user",
                    "affected_topics": ["topic1", "topic2"],
                    "recommendation": "specific actionable advice"
                    }}
                ],
                "summary": "2-3 sentence overall assessment of this learner"
                }}
            """

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.3,
    )

    raw = response.choices[0].message.content or "{}"
    clean = raw.replace("```json", "").replace("```", "").strip()
    try:
        result = json.loads(clean)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail=f"Failed to parse LLM response: {exc}") from exc

    parsed_patterns = result.get("patterns", [])
    summary = result.get("summary", "No summary provided.")

    for pattern in parsed_patterns:
        pattern_key = str(pattern.get("type", "")).strip()
        pattern_type = PATTERN_TYPE_MAP.get(pattern_key)
        if not pattern_type:
            continue

        confidence_raw = str(pattern.get("confidence", "medium")).lower().strip()
        if confidence_raw not in {"low", "medium", "high"}:
            confidence_raw = "medium"

        affected_topics = pattern.get("affected_topics") or []
        topic = affected_topics[0] if affected_topics else "general"
        if topic not in {"array", "hashmap", "stack", "linked list", "binary search", "sliding window", "recursion/dp", "two pointers", "general"}:
            topic = str(topic)[:100] or "general"

        question_ids_for_topic = [
            attempt.question_id for attempt in attempts if question_map.get(attempt.question_id) and question_map[attempt.question_id].topic == topic
        ]
        if not question_ids_for_topic:
            question_ids_for_topic = [attempt.question_id for attempt in attempts][:5]

        existing = await db.scalar(
            select(Pattern).where(
                Pattern.user_id == request.user_id,
                Pattern.pattern_type == pattern_type,
                Pattern.topic == topic,
            )
        )

        if existing:
            existing.description = str(pattern.get("description", existing.description))
            existing.confidence = Confidence(confidence_raw)
            existing.question_ids = question_ids_for_topic
        else:
            db.add(
                Pattern(
                    user_id=request.user_id,
                    pattern_type=pattern_type,
                    topic=topic,
                    description=str(pattern.get("description", "No description provided.")),
                    confidence=Confidence(confidence_raw),
                    question_ids=question_ids_for_topic,
                )
            )

    await db.commit()

    return PatternResponse(patterns=parsed_patterns, summary=summary)
