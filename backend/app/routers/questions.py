from fastapi import APIRouter

router = APIRouter(prefix="/questions", tags=["Questions"])


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Question

@router.get("/", summary="List all questions")
async def list_questions(db: AsyncSession = Depends(get_db)):
	result = await db.execute(select(Question))
	questions = result.scalars().all()
	# Convert SQLAlchemy objects to dicts for JSON response
	return [
		{
			"id": q.id,
			"title": q.title,
			"description": q.description,
			"difficulty": q.difficulty,
			"topic": q.topic,
			"expected_time": q.expected_time,
			"test_cases": q.test_cases,
			"hints": q.hints,
			"created_at": q.created_at,
		}
		for q in questions
	]
