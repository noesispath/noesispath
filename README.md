# NoesisPath API — V1

Adaptive DSA learning backend: tracks attempts, detects learning patterns, schedules spaced repetition.

## Stack
- **FastAPI** — async REST API
- **PostgreSQL** — primary database
- **SQLAlchemy 2.0** — async ORM with mapped columns
- **Alembic** — schema migrations
- **Pydantic v2** — request/response validation

---

## Project Structure

```
noesispath/
├── app/
│   ├── main.py          # FastAPI app + lifespan
│   ├── config.py        # Settings (DATABASE_URL)
│   ├── database.py      # Async engine + session + Base
│   ├── models.py        # SQLAlchemy ORM models + enums
│   ├── schemas.py       # Pydantic schemas (Create / Update / Out)
│   └── routers/
│       ├── users.py
│       ├── questions.py
│       ├── attempts.py
│       ├── patterns.py
│       └── review_queue.py
├── alembic/
│   └── env.py
├── alembic.ini
├── requirements.txt
└── .env.example
```

---

## Setup

### 1. Create virtualenv & install deps
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your actual DATABASE_URL
```

### 3. Create the database
```bash
psql -U postgres -c "CREATE DATABASE noesispath;"
```

### 4. Run migrations (or let the app auto-create on startup for dev)
```bash
# Generate first migration
alembic revision --autogenerate -m "initial schema"

# Apply
alembic upgrade head
```

### 5. Start the server
```bash
uvicorn app.main:app --reload
```

API docs → http://localhost:8000/docs

---

## API Overview

| Resource       | Base Path        | Description                          |
|----------------|------------------|--------------------------------------|
| Users          | `/users`         | CRUD + soft delete                   |
| Questions      | `/questions`     | DSA problem bank                     |
| Attempts       | `/attempts`      | Per-user attempt tracking            |
| Patterns       | `/patterns`      | Detected learning weaknesses         |
| Review Queue   | `/review-queue`  | Spaced repetition scheduling         |

### Key endpoints

```
POST   /users/                              Create user
GET    /users/{id}                          Get user
PATCH  /users/{id}                          Update user
DELETE /users/{id}                          Soft delete user

POST   /questions/                          Add DSA question
GET    /questions/?topic=tree&difficulty=hard  Filter questions

POST   /attempts/                           Log attempt
GET    /attempts/user/{uid}/question/{qid}  All attempts by user on question

POST   /patterns/                           Store detected pattern
GET    /patterns/?user_id=1&topic=dp        Query patterns

POST   /review-queue/                       Schedule review
GET    /review-queue/?user_id=1&completed=false  Pending reviews
PATCH  /review-queue/{id}                   Mark completed
```

---

## Data Flow

```
User attempts question
        ↓
    Attempt stored
        ↓
System analyzes attempts → Pattern detected → Pattern stored
        ↓
Weak questions scheduled → Review Queue entry created
        ↓
Next recommendation influenced by patterns + review queue
```

---

## Hints JSON structure (in Questions)
```json
{
  "1": "Think about edge cases with empty arrays",
  "2": "Consider using a two-pointer approach",
  "3": "Here's the key insight: traverse from both ends simultaneously"
}
```

## Test Cases JSON structure (in Questions)
```json
{
  "cases": [
    {"input": [1, 2, 3], "expected_output": 6},
    {"input": [], "expected_output": 0}
  ]
}
```
