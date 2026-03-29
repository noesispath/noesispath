import json
import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from groq import Groq
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Attempt, Question, User
from app.schemas import AttemptCreate, AttemptOut

router = APIRouter(prefix="/attempts", tags=["Attempts"])
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


@router.post("", response_model=AttemptOut, status_code=status.HTTP_201_CREATED)
async def create_attempt(payload: AttemptCreate, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, payload.user_id)
    if not user or user.deleted:
        raise HTTPException(status_code=404, detail="User not found")

    question = await db.get(Question, payload.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if payload.attempt_number is None:
        count_q = select(func.count(Attempt.id)).where(
            Attempt.user_id == payload.user_id,
            Attempt.question_id == payload.question_id,
        )
        previous_attempts = (await db.scalar(count_q)) or 0
        attempt_number = previous_attempts + 1
    else:
        attempt_number = payload.attempt_number

    attempt_data = payload.model_dump(exclude={"attempt_number"})
    attempt = Attempt(**attempt_data, attempt_number=attempt_number)
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)
    return attempt


@router.get("", response_model=list[AttemptOut])
async def list_attempts(
    user_id: str | None = None,
    question_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    q = select(Attempt)
    if user_id:
        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user_id format; must be UUID")

        q = q.where(Attempt.user_id == user_uuid)
    if question_id:
        q = q.where(Attempt.question_id == question_id)
    result = await db.scalars(q.order_by(Attempt.created_at.desc()).offset(skip).limit(limit))
    return result.all()


@router.get("/{attempt_id}", response_model=AttemptOut)
async def get_attempt(attempt_id: str, db: AsyncSession = Depends(get_db)):
    qid = uuid.UUID(attempt_id)
    attempt = await db.get(Attempt, qid)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return attempt


async def resolve_user_uuid(user_id: str, db: AsyncSession) -> uuid.UUID:
    """Resolve user ID from UUID only.

    - Accepts actual UUID string (preferred).
    """
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id format; must be UUID")

    user = await db.get(User, user_uuid)
    if not user or user.deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return user_uuid


@router.get("/user/{user_id}/question/{question_id}", response_model=list[AttemptOut])
async def get_attempts_for_user_question(
    user_id: str, question_id: int, db: AsyncSession = Depends(get_db)
):
    """All attempts by a user on a specific question, ordered by attempt_number."""
    user_uuid = await resolve_user_uuid(user_id, db)

    q = select(Attempt).where(Attempt.user_id == user_uuid, Attempt.question_id == question_id)
    result = await db.scalars(q.order_by(Attempt.attempt_number))
    return result.all()


@router.get("/history/{user_id}/{question_id}", response_model=list[AttemptOut])
async def get_attempt_history(
    user_id: str, question_id: int, db: AsyncSession = Depends(get_db)
):
    """Submission history for a user on a specific question, ordered by attempt number."""
    user_uuid = await resolve_user_uuid(user_id, db)

    q = select(Attempt).where(Attempt.user_id == user_uuid, Attempt.question_id == question_id)
    result = await db.scalars(q.order_by(Attempt.attempt_number))
    return result.all()


@router.post("/{attempt_id}/feedback")
async def get_submission_feedback(
    attempt_id: str,
    db: AsyncSession = Depends(get_db)
):
    attempt_uuid = uuid.UUID(attempt_id)
    attempt = await db.get(Attempt, attempt_uuid)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    question = await db.get(Question, attempt.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    prompt = f"""
                Submitted solution for {question.title}:

                {attempt.code_submitted}

                Results: {attempt.test_cases_passed}/{attempt.total_test_cases} test cases passed.

                Analyze their code and provide:
                1. what_went_wrong: What specifically failed in their code (2-3 sentences, reference their actual code)
                2. missing_concept: The core concept or pattern they're missing
                3. key_insight: The key insight to solve this optimally (no full solution)

                Be specific to their actual code. Not generic advice.

                Respond in JSON only:
                {{
                    "what_went_wrong": "...",
                    "missing_concept": "...",
                    "key_insight": "..."
                }}
            """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.3,
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)
