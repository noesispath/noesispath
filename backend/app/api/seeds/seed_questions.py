import asyncio
from sqlalchemy import select, text
from app.database import SessionLocal
from app.models import Question, Difficulty
from app.api.seeds.questions import pythonquestions

async def seed_questions():
    async with SessionLocal() as session:
        for q in pythonquestions:
            # Check by fixed ID so re-runs are idempotent
            existing = await session.get(Question, q["id"])
            if not existing:
                question = Question(
                    id=q["id"],
                    title=q["title"],
                    description=q["description"],
                    difficulty=Difficulty(q["difficulty"]),
                    topic=q["topic"],
                    expected_time=q["expected_time"],
                    test_cases=q["test_cases"],
                    hints=q["hints"],
                    starter_code=q.get("starter_code"),
                    examples=q.get("examples", []),
                    constraints=q.get("constraints", []),
                    learn=q.get("learn", {}),
                    follow_up=q.get("follow_up"),
                )
                session.add(question)
            else:
                existing.title = q["title"]
                existing.description = q["description"]
                existing.difficulty = Difficulty(q["difficulty"])
                existing.topic = q["topic"]
                existing.expected_time = q["expected_time"]
                existing.test_cases = q["test_cases"]
                existing.hints = q["hints"]
                existing.starter_code = q.get("starter_code")
                existing.examples = q.get("examples", [])
                existing.constraints = q.get("constraints", [])
                existing.learn = q.get("learn", {})
                existing.follow_up = q.get("follow_up")
        await session.commit()
        # Reset the sequence so future inserts don't collide with seeded IDs
        await session.execute(
            text("SELECT setval('questions_id_seq', (SELECT MAX(id) FROM questions))")
        )
        await session.commit()

import os
def should_seed():
    return os.environ.get("SEED_QUESTIONS_ON_START", "0") == "1"

if __name__ == "__main__":
    if should_seed():
        asyncio.run(seed_questions())
    else:
        print("Set SEED_QUESTIONS_ON_START=1 to seed questions.")
