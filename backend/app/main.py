from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import attempts, execute, hints, patterns, questions, review_queue, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup (use Alembic for production migrations)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Optionally seed questions if flag is set
    import os
    if os.environ.get("SEED_QUESTIONS_ON_START", "0") == "1":
        from app.api.seeds.seed_questions import seed_questions
        import asyncio
        await seed_questions()
    yield


app = FastAPI(
    title="NoesisPath API",
    description="Adaptive DSA learning system — tracks attempts, detects patterns, schedules reviews.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router, prefix="/api")
app.include_router(questions.router, prefix="/api")
app.include_router(attempts.router, prefix="/api")
app.include_router(execute.router, prefix="/api")
app.include_router(patterns.router, prefix="/api")
app.include_router(review_queue.router, prefix="/api")
app.include_router(hints.router, prefix="/api", tags=["hints"])


@app.get("/api/health", tags=["Health"])
async def health():
    return {"status": "ok"}