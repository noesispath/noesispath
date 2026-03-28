from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import attempts, patterns, questions, review_queue, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup (use Alembic for production migrations)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="NoesisPath API",
    description="Adaptive DSA learning system — tracks attempts, detects patterns, schedules reviews.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router)
app.include_router(questions.router)
app.include_router(attempts.router)
app.include_router(patterns.router)
app.include_router(review_queue.router)


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}