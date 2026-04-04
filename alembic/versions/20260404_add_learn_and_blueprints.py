"""add learn to questions and blueprints table

Revision ID: 20260404_add_learn_and_blueprints
Revises: 20260403_add_in_progress_status
Create Date: 2026-04-04 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = '20260404_add_learn_blueprints'
down_revision = '20260403_add_in_progress_status'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE questions ADD COLUMN IF NOT EXISTS learn JSONB DEFAULT '{}'::jsonb"
    )
    op.execute(
        "CREATE TABLE IF NOT EXISTS blueprints ("
        "id SERIAL PRIMARY KEY, "
        "user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE, "
        "question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE CASCADE, "
        "approach TEXT NOT NULL, "
        "is_valid BOOLEAN NOT NULL, "
        "feedback TEXT, "
        "edge_cases_considered BOOLEAN NOT NULL, "
        "created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL"
        ")"
    )


def downgrade() -> None:
    op.drop_table('blueprints')
    op.drop_column('questions', 'learn')
