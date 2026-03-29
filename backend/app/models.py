from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import (
    Boolean, DateTime, Enum, ForeignKey, Integer,
    String, Text, func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

import enum


# ── Enums ──────────────────────────────────────────────────────────────────

class UserType(str, enum.Enum):
    student = "student"
    professional = "professional"


class Difficulty(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class AttemptStatus(str, enum.Enum):
    passed = "passed"
    failed = "failed"
    partial = "partial"


class PatternType(str, enum.Enum):
    edge_cases = "edge_cases"
    gives_up_early = "gives_up_early"
    time_complexity = "time_complexity"
    concept_gap = "concept_gap"
    inconsistent_recall = "inconsistent_recall"


class Confidence(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ReviewReason(str, enum.Enum):
    failed = "failed"
    multiple_attempts = "multiple_attempts"
    scheduled_review = "scheduled_review"


class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


# ── Models ─────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    organization: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    type: Mapped[Optional[UserType]] = mapped_column(Enum(UserType), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    attempts: Mapped[list["Attempt"]] = relationship("Attempt", back_populates="user")
    patterns: Mapped[list["Pattern"]] = relationship("Pattern", back_populates="user")
    review_queue: Mapped[list["ReviewQueue"]] = relationship("ReviewQueue", back_populates="user")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[Difficulty] = mapped_column(Enum(Difficulty), nullable=False)
    topic: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. "array", "hashmap"
    expected_time: Mapped[int] = mapped_column(Integer, nullable=False)  # minutes
    test_cases: Mapped[dict] = mapped_column(JSONB, nullable=False)
    hints: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    starter_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    examples: Mapped[list] = mapped_column(JSONB, server_default='[]')
    constraints: Mapped[list] = mapped_column(JSONB, server_default='[]')
    follow_up: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    attempts: Mapped[list["Attempt"]] = relationship("Attempt", back_populates="question")
    review_queue: Mapped[list["ReviewQueue"]] = relationship("ReviewQueue", back_populates="question")


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    code_submitted: Mapped[str] = mapped_column(Text, nullable=False)
    time_taken: Mapped[int] = mapped_column(Integer, nullable=False)  # seconds
    hints_used: Mapped[int] = mapped_column(Integer, default=0)  # max hint level 0–3
    hint_levels_used: Mapped[dict] = mapped_column(JSONB, default=list)
    test_cases_passed: Mapped[int] = mapped_column(Integer, nullable=False)
    total_test_cases: Mapped[int] = mapped_column(Integer, nullable=False)
    errors: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[AttemptStatus] = mapped_column(Enum(AttemptStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    code_snapshots: Mapped[list] = mapped_column(JSONB, server_default='[]')

    user: Mapped["User"] = relationship("User", back_populates="attempts")
    question: Mapped["Question"] = relationship("Question", back_populates="attempts")


class Pattern(Base):
    __tablename__ = "patterns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    pattern_type: Mapped[PatternType] = mapped_column(Enum(PatternType), nullable=False)
    topic: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[Confidence] = mapped_column(Enum(Confidence), nullable=False)
    question_ids: Mapped[list] = mapped_column(JSONB, default=list)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="patterns")


class ReviewQueue(Base):
    __tablename__ = "review_queue"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    scheduled_for: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reason: Mapped[ReviewReason] = mapped_column(Enum(ReviewReason), nullable=False)
    priority: Mapped[Priority] = mapped_column(Enum(Priority), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="review_queue")
    question: Mapped["Question"] = relationship("Question", back_populates="review_queue")
