from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Pattern, User
from app.schemas import PatternCreate, PatternOut, PatternUpdate

router = APIRouter(prefix="/patterns", tags=["Patterns"])


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
