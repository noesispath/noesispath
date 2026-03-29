from datetime import datetime
from typing import Any, Optional
from uuid import UUID as PyUUID

from pydantic import BaseModel, EmailStr, Field

from app.models import (
    AttemptStatus, Confidence, Difficulty,
    PatternType, Priority, ReviewReason, UserType,
)


# ── User ───────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    organization: Optional[str] = None
    type: Optional[UserType] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    organization: Optional[str] = None
    type: Optional[UserType] = None


class UserOut(BaseModel):
    id: PyUUID
    name: str
    email: str
    organization: Optional[str]
    type: Optional[UserType]
    created_at: datetime
    updated_at: datetime
    deleted: bool

    model_config = {"from_attributes": True}


# ── Question ───────────────────────────────────────────────────────────────

class QuestionCreate(BaseModel):
    title: str
    description: str
    difficulty: Difficulty
    topic: str
    expected_time: int  # minutes
    test_cases: dict[str, Any]
    hints: dict[str, Any]
    starter_code: Optional[str] = None
    examples: list[dict[str, Any]] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    follow_up: Optional[str] = None


class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[Difficulty] = None
    topic: Optional[str] = None
    expected_time: Optional[int] = None
    test_cases: Optional[dict[str, Any]] = None
    hints: Optional[dict[str, Any]] = None
    starter_code: Optional[str] = None
    examples: Optional[list[dict[str, Any]]] = None
    constraints: Optional[list[str]] = None
    follow_up: Optional[str] = None


class QuestionOut(BaseModel):
    id: int
    title: str
    description: str
    difficulty: Difficulty
    topic: str
    expected_time: int
    test_cases: dict[str, Any]
    hints: dict[str, Any]
    starter_code: Optional[str] = None
    examples: list[dict[str, Any]] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    follow_up: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Attempt ────────────────────────────────────────────────────────────────

class AttemptCreate(BaseModel):
    user_id: PyUUID
    question_id: int
    attempt_number: Optional[int] = None
    code_submitted: str
    time_taken: int  # seconds
    hints_used: int = 0
    hint_levels_used: list[int] = Field(default_factory=list)
    test_cases_passed: int
    total_test_cases: int
    errors: Optional[str] = None
    status: AttemptStatus
    code_snapshots: list[dict[str, Any]] = Field(default_factory=list)


class AttemptOut(BaseModel):
    id: PyUUID
    user_id: PyUUID
    question_id: int
    attempt_number: int
    code_submitted: str
    time_taken: int
    hints_used: int
    hint_levels_used: list[int]
    test_cases_passed: int
    total_test_cases: int
    errors: Optional[str]
    status: AttemptStatus
    created_at: datetime
    code_snapshots: list[dict[str, Any]] = Field(default_factory=list)

    model_config = {"from_attributes": True}


# ── Pattern ────────────────────────────────────────────────────────────────

class PatternCreate(BaseModel):
    user_id: int
    pattern_type: PatternType
    topic: str
    description: str
    confidence: Confidence
    question_ids: list[int] = []


class PatternUpdate(BaseModel):
    description: Optional[str] = None
    confidence: Optional[Confidence] = None
    question_ids: Optional[list[int]] = None


class PatternOut(BaseModel):
    id: PyUUID
    user_id: PyUUID
    pattern_type: PatternType
    topic: str
    description: str
    confidence: Confidence
    question_ids: list[int]
    detected_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Review Queue ───────────────────────────────────────────────────────────

class ReviewQueueCreate(BaseModel):
    user_id: PyUUID
    question_id: int
    scheduled_for: datetime
    reason: ReviewReason
    priority: Priority


class ReviewQueueUpdate(BaseModel):
    scheduled_for: Optional[datetime] = None
    priority: Optional[Priority] = None
    completed: Optional[bool] = None


class ReviewQueueOut(BaseModel):
    id: PyUUID
    user_id: PyUUID
    question_id: int
    scheduled_for: datetime
    reason: ReviewReason
    priority: Priority
    completed: bool
    created_at: datetime

    model_config = {"from_attributes": True}
