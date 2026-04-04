"""
Add in_progress value to attemptstatus enum
"""
from alembic import op

revision = '20260403_add_in_progress_status'
down_revision = '20260330_constraints_followup'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE attemptstatus ADD VALUE IF NOT EXISTS 'in_progress'")


def downgrade():
    # Postgres doesn't support removing enum values; handled manually if needed
    pass
