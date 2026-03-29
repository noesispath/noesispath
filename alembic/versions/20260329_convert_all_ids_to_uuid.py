"""
Convert user/attempt/pattern/review IDs to UUID.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '20260329_convert_all_ids_to_uuid'
down_revision = '20260329_add_code_snapshots'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    # Step 1: add new UUID columns
    op.add_column('users', sa.Column('id_new', UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')))
    op.add_column('attempts', sa.Column('id_new', UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')))
    op.add_column('patterns', sa.Column('id_new', UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')))
    op.add_column('review_queue', sa.Column('id_new', UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')))

    # Step 2: add new FK columns before converting IDs
    op.add_column('attempts', sa.Column('user_id_new', UUID(as_uuid=True), nullable=True))
    op.add_column('patterns', sa.Column('user_id_new', UUID(as_uuid=True), nullable=True))
    op.add_column('review_queue', sa.Column('user_id_new', UUID(as_uuid=True), nullable=True))

    # Step 3: populate new user UUID IDs
    op.execute("UPDATE users SET id_new = gen_random_uuid()")
    op.execute("UPDATE attempts SET user_id_new = u.id_new FROM users u WHERE attempts.user_id = u.id")
    op.execute("UPDATE patterns SET user_id_new = u.id_new FROM users u WHERE patterns.user_id = u.id")
    op.execute("UPDATE review_queue SET user_id_new = u.id_new FROM users u WHERE review_queue.user_id = u.id")

    # Step 4: convert user_id columns to uuid via swapping columns for FK relationships
    op.drop_constraint('attempts_user_id_fkey', 'attempts', type_='foreignkey')
    op.drop_constraint('patterns_user_id_fkey', 'patterns', type_='foreignkey')
    op.drop_constraint('review_queue_user_id_fkey', 'review_queue', type_='foreignkey')

    op.drop_column('attempts', 'user_id')
    op.alter_column('attempts', 'user_id_new', new_column_name='user_id', nullable=False)

    op.drop_column('patterns', 'user_id')
    op.alter_column('patterns', 'user_id_new', new_column_name='user_id', nullable=False)

    op.drop_column('review_queue', 'user_id')
    op.alter_column('review_queue', 'user_id_new', new_column_name='user_id', nullable=False)

    # Step 5: swap primary key IDs to UUID
    op.drop_constraint('users_pkey', 'users', type_='primary')
    op.alter_column('users', 'id', new_column_name='id_old')
    op.alter_column('users', 'id_new', new_column_name='id')
    op.create_primary_key('users_pkey', 'users', ['id'])
    op.drop_column('users', 'id_old')

    op.drop_constraint('attempts_pkey', 'attempts', type_='primary')
    op.alter_column('attempts', 'id', new_column_name='id_old')
    op.alter_column('attempts', 'id_new', new_column_name='id')
    op.create_primary_key('attempts_pkey', 'attempts', ['id'])
    op.drop_column('attempts', 'id_old')

    op.drop_constraint('patterns_pkey', 'patterns', type_='primary')
    op.alter_column('patterns', 'id', new_column_name='id_old')
    op.alter_column('patterns', 'id_new', new_column_name='id')
    op.create_primary_key('patterns_pkey', 'patterns', ['id'])
    op.drop_column('patterns', 'id_old')

    op.drop_constraint('review_queue_pkey', 'review_queue', type_='primary')
    op.alter_column('review_queue', 'id', new_column_name='id_old')
    op.alter_column('review_queue', 'id_new', new_column_name='id')
    op.create_primary_key('review_queue_pkey', 'review_queue', ['id'])
    op.drop_column('review_queue', 'id_old')

    # Step 6: recreate foreign keys
    op.create_foreign_key('attempts_user_id_fkey', 'attempts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('patterns_user_id_fkey', 'patterns', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('review_queue_user_id_fkey', 'review_queue', 'users', ['user_id'], ['id'], ondelete='CASCADE')



def downgrade():
    raise NotImplementedError('Downgrade not supported for UUID key migration')
