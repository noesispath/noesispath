import asyncio
from app.database import SessionLocal
from app.models import Question, Difficulty
from app.api.seeds.questions import pythonquestions

async def seed_questions():
    from sqlalchemy import select
    async with SessionLocal() as session:
        for q in pythonquestions:
            # Check if a question with the same title exists
            result = await session.execute(select(Question).where(Question.title == q["title"]))
            existing = result.scalar_one_or_none()
            if not existing:
                question = Question(
                    title=q["title"],
                    description=q["description"],
                    difficulty=Difficulty(q["difficulty"]),
                    topic=q["topic"],
                    expected_time=q["expected_time"],
                    test_cases=q["test_cases"],
                    hints=q["hints"]
                )
                session.add(question)
        await session.commit()

import os
def should_seed():
    return os.environ.get("SEED_QUESTIONS_ON_START", "0") == "1"

if __name__ == "__main__":
    if should_seed():
        asyncio.run(seed_questions())
    else:
        print("Set SEED_QUESTIONS_ON_START=1 to seed questions.")
