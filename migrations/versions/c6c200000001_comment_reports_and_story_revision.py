"""Signalements de commentaires et révision de gestion — non déployée.

Revision ID: c6c200000001
Revises: c6c100000001
"""
import re
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

revision = 'c6c200000001'
down_revision = 'c6c100000001'
branch_labels = None
depends_on = None
SENTINEL = '0' * 32


def inspect_legacy(bind):
    # Toute anomalie de données est refusée AVANT le premier DDL : même un
    # moteur dont les ALTER commettent implicitement reste inchangé dans ce cas.
    inspector = sa.inspect(bind)
    column = next(c for c in inspector.get_columns('comments') if c['name'] == 'id')
    if not isinstance(column['type'], sa.Integer):
        raise RuntimeError('Migration refusée : type de clé commentaire incompatible.')
    metadata = sa.MetaData()
    reports = sa.Table('reports', metadata, autoload_with=bind)
    comments = sa.Table('comments', metadata, autoload_with=bind)
    rows = bind.execute(sa.select(reports.c.id, reports.c.type, reports.c.target_id)).all()
    existing = set(bind.execute(sa.select(comments.c.id)).scalars())
    mapped = []
    for identifier, kind, target in rows:
        if (kind != 'comment' or not isinstance(target, str) or
                not re.fullmatch(r'[1-9][0-9]{0,9}', target) or
                int(target) > 2147483647 or int(target) not in existing):
            # Le message ne copie ni cible, ni motif, ni autre donnée historique.
            raise RuntimeError('Migration refusée : référence de signalement incompatible ; aucune reprise automatique.')
        mapped.append({'report_id': identifier, 'comment_id': int(target)})
    return column['type'].copy(), mapped


def upgrade():
    bind = op.get_bind()
    comment_type, mapped = inspect_legacy(bind)
    # Exécution réelle uniquement en maintenance, anciens écrivains drainés.
    op.add_column('reports', sa.Column('comment_id', comment_type, nullable=True))
    table = sa.table('reports', sa.column('id'), sa.column('comment_id'))
    for row in mapped:
        bind.execute(table.update().where(table.c.id == row['report_id']).values(comment_id=row['comment_id']))
    # reports n'a aucune FK entrante : reconstruire cette table enfant ne
    # nécessite pas de désactiver les FK SQLite des autres tables.
    with op.batch_alter_table('reports') as batch:
        batch.alter_column('comment_id', existing_type=comment_type, nullable=False)
        batch.create_foreign_key('fk_reports_comment', 'comments', ['comment_id'], ['id'], ondelete='CASCADE')
        batch.drop_column('type')
        batch.drop_column('target_id')
        batch.create_index('ix_reports_comment_id', ['comment_id'], unique=False)
    op.add_column('stories', sa.Column('management_revision', sa.String(32), nullable=False, server_default=SENTINEL))
    stories = sa.table('stories', sa.column('id'), sa.column('management_revision'))
    for identifier in bind.execute(sa.select(stories.c.id)).scalars().all():
        bind.execute(stories.update().where(stories.c.id == identifier).values(management_revision=uuid4().hex))
    op.create_index('uq_stories_management_revision', 'stories', ['management_revision'], unique=True)


def downgrade():
    # Revenir au format antérieur ne recrée aucune donnée définitivement purgée.
    bind = op.get_bind()
    op.add_column('reports', sa.Column('type', sa.String(100), nullable=True))
    op.add_column('reports', sa.Column('target_id', sa.String(100), nullable=True))
    reports = sa.table('reports', sa.column('id'), sa.column('comment_id'), sa.column('type'), sa.column('target_id'))
    for identifier, target in bind.execute(sa.select(reports.c.id, reports.c.comment_id)).all():
        bind.execute(reports.update().where(reports.c.id == identifier).values(type='comment', target_id=str(target)))
    with op.batch_alter_table('reports') as batch:
        batch.drop_constraint('fk_reports_comment', type_='foreignkey')
        batch.drop_index('ix_reports_comment_id')
        batch.alter_column('type', existing_type=sa.String(100), nullable=False)
        batch.alter_column('target_id', existing_type=sa.String(100), nullable=False)
        batch.drop_column('comment_id')
    op.drop_index('uq_stories_management_revision', table_name='stories')
    op.drop_column('stories', 'management_revision')
