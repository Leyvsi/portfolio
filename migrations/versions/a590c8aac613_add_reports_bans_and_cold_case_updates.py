"""add reports bans and cold case updates

Revision ID: a590c8aac613
Revises: 3111f5767fc6
Create Date: 2026-10-12 13:50:45.629332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a590c8aac613'
down_revision = '3111f5767fc6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=100), nullable=False),
        sa.Column('target_id', sa.String(length=100), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'cold_case_updates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('story_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ['story_id'],
            ['stories.id'],
            name='fk_cold_case_updates_story',
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id')
    )

    op.add_column(
        "users",
        sa.Column(
            "is_banned",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )

    op.alter_column(
        "users",
        "is_banned",
        server_default=None
    )


def downgrade():
    op.drop_table('cold_case_updates')
    op.drop_table('reports')

    op.drop_column(
        "users",
        "is_banned"
    )
