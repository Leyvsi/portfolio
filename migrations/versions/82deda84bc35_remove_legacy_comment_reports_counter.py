"""Remove legacy comment reports counter

Revision ID: 82deda84bc35
Revises: a590c8aac613
Create Date: 2026-10-20 21:12:52.688507

"""

from alembic import op
import sqlalchemy as sa


revision = "82deda84bc35"
down_revision = "a590c8aac613"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.drop_column("reports")


def downgrade():
    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "reports",
                sa.Integer(),
                nullable=False,
                server_default="0",
            )
        )

    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.alter_column(
            "reports",
            server_default=None,
        )
