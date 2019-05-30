"""empty message

Revision ID: 0da415735f3b
Revises: 8f51fb7f4e40
Create Date: 2019-05-30 10:05:19.421289

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0da415735f3b'
down_revision = '8f51fb7f4e40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project_favorites',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('application_keys', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_index('idx_task_validation_mapper_status_composite', table_name='task_invalidation_history')
    op.create_index('idx_task_validation_mapper_status_composite', 'task_invalidation_history', ['mapper_id', 'is_closed'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_task_validation_mapper_status_composite', table_name='task_invalidation_history')
    op.create_index('idx_task_validation_mapper_status_composite', 'task_invalidation_history', ['invalidator_id', 'is_closed'], unique=False)
    op.alter_column('application_keys', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.drop_table('project_favorites')
    # ### end Alembic commands ###
