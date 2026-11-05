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


# Ajouter signalements, mises à jour et état de bannissement. Le défaut SQL
# temporaire renseigne les comptes existants, puis est retiré du schéma.
def upgrade():
    sqlite = op.get_bind().dialect.name == 'sqlite'
    if sqlite and (op.get_bind().exec_driver_sql('PRAGMA foreign_keys').scalar()
                   or not op.get_bind().info.get('sqlite_migration_integrity_scope')):
        # users est une table parent : un DROP sous FK actives pourrait
        # déclencher des cascades. Refuser avant tout DDL hors du cadre dédié.
        raise RuntimeError('SQLite : utiliser sqlite_migration_scope hors transaction.')
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

    if sqlite:
        # SQLite ne sait pas retirer ce défaut avec ALTER COLUMN. Le batch
        # conserve les valeurs False des comptes existants et retire le défaut.
        with op.batch_alter_table('users') as batch:
            batch.alter_column('is_banned', existing_type=sa.Boolean(), server_default=None)
    else:
        # La branche MySQL historique conserve son SQL et sa sémantique.
        op.alter_column('users', 'is_banned', server_default=None)


# Retirer ces éléments du schéma ; les lignes des deux tables supprimées
# ne sont pas sauvegardées par cette opération inverse.
def downgrade():
    op.drop_table('cold_case_updates')
    op.drop_table('reports')

    op.drop_column(
        "users",
        "is_banned"
    )
