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
			"starter_code": q.starter_code,
			"examples": q.examples,
			"constraints": q.constraints,
			"follow_up": q.follow_up,
			"created_at": q.created_at,
		}
		for q in questions
	]


from fastapi import HTTPException

@router.get("/{id}", summary="Get a question by ID")
async def get_question(id: int, db: AsyncSession = Depends(get_db)):
	question = await db.get(Question, id)
	if not question:
		raise HTTPException(status_code=404, detail="Question not found")
	return {
		"id": question.id,
		"title": question.title,
		"description": question.description,
		"difficulty": question.difficulty,
		"topic": question.topic,
		"expected_time": question.expected_time,
		"test_cases": question.test_cases,
		"hints": question.hints,
		"starter_code": question.starter_code,
		"examples": question.examples,
		"constraints": question.constraints,
		"follow_up": question.follow_up,
		"created_at": question.created_at,
	}
