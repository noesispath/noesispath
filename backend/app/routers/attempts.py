from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Attempt, Question, User
from app.schemas import AttemptCreate, AttemptOut

router = APIRouter(prefix="/attempts", tags=["Attempts"])


@router.post("/", response_model=AttemptOut, status_code=status.HTTP_201_CREATED)
async def create_attempt(payload: AttemptCreate, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, payload.user_id)
    if not user or user.deleted:
        raise HTTPException(status_code=404, detail="User not found")

    question = await db.get(Question, payload.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    attempt = Attempt(**payload.model_dump())
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)
    return attempt


@router.get("/", response_model=list[AttemptOut])
async def list_attempts(
    user_id: int | None = None,
    question_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    q = select(Attempt)
    if user_id:
        q = q.where(Attempt.user_id == user_id)
    if question_id:
        q = q.where(Attempt.question_id == question_id)
    result = await db.scalars(q.order_by(Attempt.created_at.desc()).offset(skip).limit(limit))
    return result.all()


@router.get("/{attempt_id}", response_model=AttemptOut)
async def get_attempt(attempt_id: int, db: AsyncSession = Depends(get_db)):
    attempt = await db.get(Attempt, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return attempt


@router.get("/user/{user_id}/question/{question_id}", response_model=list[AttemptOut])
async def get_attempts_for_user_question(
    user_id: int, question_id: int, db: AsyncSession = Depends(get_db)
):
    """All attempts by a user on a specific question, ordered by attempt_number."""
    result = await db.scalars(
        select(Attempt)
        .where(Attempt.user_id == user_id, Attempt.question_id == question_id)
        .order_by(Attempt.attempt_number)
    )
    return result.all()
