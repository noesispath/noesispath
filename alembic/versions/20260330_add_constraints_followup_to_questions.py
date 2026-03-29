"""
Add constraints and follow_up fields to questions.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '20260330_constraints_followup'
down_revision = '20260329_convert_all_ids_to_uuid'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('questions', sa.Column('constraints', JSONB, nullable=False, server_default='[]'))
    op.add_column('questions', sa.Column('follow_up', sa.Text, nullable=True))


def downgrade():
    op.drop_column('questions', 'follow_up')
    op.drop_column('questions', 'constraints')
