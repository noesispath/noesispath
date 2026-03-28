from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Question, ReviewQueue, User
from app.schemas import ReviewQueueCreate, ReviewQueueOut, ReviewQueueUpdate

router = APIRouter(prefix="/review-queue", tags=["Review Queue"])


@router.post("/", response_model=ReviewQueueOut, status_code=status.HTTP_201_CREATED)
async def enqueue_review(payload: ReviewQueueCreate, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, payload.user_id)
    if not user or user.deleted:
        raise HTTPException(status_code=404, detail="User not found")

    question = await db.get(Question, payload.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    item = ReviewQueue(**payload.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/", response_model=list[ReviewQueueOut])
async def list_review_queue(
    user_id: int | None = None,
    completed: bool | None = None,
    priority: str | None = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    q = select(ReviewQueue)
    if user_id:
        q = q.where(ReviewQueue.user_id == user_id)
    if completed is not None:
        q = q.where(ReviewQueue.completed == completed)
    if priority:
        q = q.where(ReviewQueue.priority == priority)
    result = await db.scalars(q.order_by(ReviewQueue.scheduled_for).offset(skip).limit(limit))
    return result.all()


@router.get("/{item_id}", response_model=ReviewQueueOut)
async def get_review_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(ReviewQueue, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Review queue item not found")
    return item


@router.patch("/{item_id}", response_model=ReviewQueueOut)
async def update_review_item(item_id: int, payload: ReviewQueueUpdate, db: AsyncSession = Depends(get_db)):
    item = await db.get(ReviewQueue, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Review queue item not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(ReviewQueue, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Review queue item not found")
    await db.delete(item)
    await db.commit()
