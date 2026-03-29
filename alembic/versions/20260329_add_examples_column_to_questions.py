"""
Add examples column to questions table
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '20260329_add_examples'
down_revision: Union[str, Sequence[str], None] = '83aba3f6a555'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('questions', sa.Column('examples', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'))


def downgrade() -> None:
    op.drop_column('questions', 'examples')
