import json
import os
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from groq import Groq
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Blueprint, Question, User
from app.schemas import BlueprintValidateRequest, BlueprintValidationOut

router = APIRouter(prefix="/blueprint", tags=["Blueprints"])
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def resolve_user_uuid(user_id: str) -> uuid.UUID:
    try:
        return uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user_id format; must be UUID")


@router.post("/validate", response_model=BlueprintValidationOut, status_code=status.HTTP_200_OK)
async def validate_blueprint(payload: BlueprintValidateRequest, db: AsyncSession = Depends(get_db)):
    user_uuid = resolve_user_uuid(payload.user_id)
    user = await db.get(User, user_uuid)
    if not user or user.deleted:
        raise HTTPException(status_code=404, detail="User not found")

    question = await db.get(Question, payload.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    prompt = f"""
You are a DSA coach reviewing a student's planned approach before they code.

Problem: {question.title}
{question.description}

Student's planned approach:
{payload.approach}

Evaluate their thinking and respond in JSON only:
{{
  "is_valid": true/false,
  "feedback": "specific feedback on their approach in 2-3 sentences",
  "missing": "what they haven't considered, or null if solid",
  "edge_cases_considered": true/false,
  "nudge": "one encouraging sentence to move them to coding"
}}

Be honest. If their approach is wrong say so clearly but kindly. Do not give the solution.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.3,
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(clean)
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="Failed to parse AI response")

    if not isinstance(parsed, dict) or "is_valid" not in parsed or "feedback" not in parsed:
        raise HTTPException(status_code=502, detail="AI response did not include required fields")

    blueprint = Blueprint(
        user_id=user.id,
        question_id=question.id,
        approach=payload.approach,
        is_valid=bool(parsed.get("is_valid", False)),
        feedback=str(parsed.get("feedback", "")),
        edge_cases_considered=bool(parsed.get("edge_cases_considered", False)),
    )
    db.add(blueprint)
    await db.commit()
    await db.refresh(blueprint)

    return {
        "is_valid": bool(parsed.get("is_valid", False)),
        "feedback": str(parsed.get("feedback", "")),
        "missing": parsed.get("missing"),
        "edge_cases_considered": bool(parsed.get("edge_cases_considered", False)),
        "nudge": str(parsed.get("nudge", "")),
    }
