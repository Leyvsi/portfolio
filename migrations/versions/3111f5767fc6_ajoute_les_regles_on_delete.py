"""Ajoute les regles ON DELETE

Revision ID: 3111f5767fc6
Revises: 921687c1bd7c
Create Date: 2026-10-01 20:09:01.766166

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "3111f5767fc6"
down_revision = "921687c1bd7c"
branch_labels = None
depends_on = None


def upgrade():
    # Comments:
    # - deleting a story deletes its comments
    # - deleting a user keeps the comment but sets user_id to NULL
    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.drop_constraint(
            "comments_ibfk_1",
            type_="foreignkey"
        )

        batch_op.drop_constraint(
            "comments_ibfk_2",
            type_="foreignkey"
        )

        batch_op.create_foreign_key(
            "fk_comments_story",
            "stories",
            ["story_id"],
            ["id"],
            ondelete="CASCADE"
        )

        batch_op.create_foreign_key(
            "fk_comments_user",
            "users",
            ["user_id"],
            ["id"],
            ondelete="SET NULL"
        )

    # Proposals:
    # deleting a user deletes their proposals
    with op.batch_alter_table("proposals", schema=None) as batch_op:
        batch_op.drop_constraint(
            "proposals_ibfk_1",
            type_="foreignkey"
        )

        batch_op.create_foreign_key(
            "fk_proposals_user",
            "users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE"
        )

    # Theories:
    # - deleting a story deletes its theories
    # - deleting a user keeps the theory but sets user_id to NULL
    with op.batch_alter_table("theories", schema=None) as batch_op:
        batch_op.drop_constraint(
            "theories_ibfk_1",
            type_="foreignkey"
        )

        batch_op.drop_constraint(
            "theories_ibfk_2",
            type_="foreignkey"
        )

        batch_op.create_foreign_key(
            "fk_theories_story",
            "stories",
            ["story_id"],
            ["id"],
            ondelete="CASCADE"
        )

        batch_op.create_foreign_key(
            "fk_theories_user",
            "users",
            ["user_id"],
            ["id"],
            ondelete="SET NULL"
        )

    # Votes:
    # deleting a story or user deletes the associated vote
    with op.batch_alter_table("votes", schema=None) as batch_op:
        batch_op.drop_constraint(
            "votes_ibfk_1",
            type_="foreignkey"
        )

        batch_op.drop_constraint(
            "votes_ibfk_2",
            type_="foreignkey"
        )

        batch_op.create_foreign_key(
            "fk_votes_story",
            "stories",
            ["story_id"],
            ["id"],
            ondelete="CASCADE"
        )

        batch_op.create_foreign_key(
            "fk_votes_user",
            "users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE"
        )


def downgrade():
    # Restore votes constraints without ON DELETE rules
    with op.batch_alter_table("votes", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_votes_story",
            type_="foreignkey"
        )

        batch_op.drop_constraint(
            "fk_votes_user",
            type_="foreignkey"
        )

        batch_op.create_foreign_key(
            "votes_ibfk_1",
            "stories",
            ["story_id"],
            ["id"]
        )

        batch_op.create_foreign_key(
            "votes_ibfk_2",
            "users",
            ["user_id"],
            ["id"]
        )

    # Restore theories constraints without ON DELETE rules
    with op.batch_alter_table("theories", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_theories_story",
            type_="foreignkey"
        )

        batch_op.drop_constraint(
            "fk_theories_user",
            type_="foreignkey"
        )

        batch_op.create_foreign_key(
            "theories_ibfk_1",
            "stories",
            ["story_id"],
            ["id"]
        )

        batch_op.create_foreign_key(
            "theories_ibfk_2",
            "users",
            ["user_id"],
            ["id"]
        )

    # Restore proposals constraint without ON DELETE rule
    with op.batch_alter_table("proposals", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_proposals_user",
            type_="foreignkey"
        )

        batch_op.create_foreign_key(
            "proposals_ibfk_1",
            "users",
            ["user_id"],
            ["id"]
        )

    # Restore comments constraints without ON DELETE rules
    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_comments_story",
            type_="foreignkey"
        )

        batch_op.drop_constraint(
            "fk_comments_user",
            type_="foreignkey"
        )

        batch_op.create_foreign_key(
            "comments_ibfk_1",
            "stories",
            ["story_id"],
            ["id"]
        )

        batch_op.create_foreign_key(
            "comments_ibfk_2",
            "users",
            ["user_id"],
            ["id"]
        )