"""Likes individuels ; candidat non appliqué à une base réelle.

Revision ID: c6g200000001
Revises: c6c200000001
"""
from alembic import op
import sqlalchemy as sa

revision = 'c6g200000001'
down_revision = 'c6c200000001'
branch_labels = None
depends_on = None


def inspect_legacy(bind):
    # Aucun DDL ou UPDATE avant ces contrôles. Les anciens écrivains doivent
    # être arrêtés pendant une éventuelle opération réelle séparément autorisée.
    if bind.dialect.name == 'sqlite' and bind.exec_driver_sql('PRAGMA foreign_keys').scalar() != 1:
        # Seule l'enveloppe transactionnelle SQLite dédiée peut suspendre les
        # FK pour reconstruire les tables parent des révisions précédentes.
        # Elle contrôle les relations avant commit et réactive toujours les FK.
        if not bind.info.get('sqlite_migration_integrity_scope'):
            raise RuntimeError('Migration refusée : clés étrangères SQLite inactives.')
        if bind.exec_driver_sql('PRAGMA foreign_key_check').first() is not None:
            raise RuntimeError('Migration refusée : intégrité SQLite invalide.')
    inspector = sa.inspect(bind)
    if bind.dialect.name == 'mysql':
        if bind.exec_driver_sql('SELECT @@foreign_key_checks').scalar() != 1 or any(
                str(inspector.get_table_options(name).get('mysql_engine', '')).lower() != 'innodb'
                for name in ('comments', 'users')):
            raise RuntimeError('Migration refusée : intégrité MySQL non garantie.')
    if inspector.has_table('comment_likes'):
        raise RuntimeError('Migration refusée : table de likes déjà présente.')
    parent_types = []
    for table in ('comments', 'users'):
        column = next(c for c in inspector.get_columns(table) if c['name'] == 'id')
        if not isinstance(column['type'], sa.Integer):
            raise RuntimeError('Migration refusée : type de clé parent incompatible.')
        parent_types.append(column['type'].copy())
    comments = sa.Table('comments', sa.MetaData(), autoload_with=bind)
    # Lire sans cast : SQLite peut contenir un texte malgré l'affinité Integer.
    for value in bind.execute(sa.select(comments.c.likes)).scalars():
        if type(value) is not int or value != 0:
            raise RuntimeError('Migration refusée : likes historiques non attribuables ; décision humaine nécessaire.')
    return parent_types


def upgrade():
    comment_type, user_type = inspect_legacy(op.get_bind())
    op.create_table(
        'comment_likes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('comment_id', comment_type, nullable=False),
        sa.Column('user_id', user_type, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], name='fk_comment_likes_comment', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_comment_likes_user', ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'comment_id', name='unique_user_comment_like'),
        mysql_engine='InnoDB',
    )
    op.create_index('ix_comment_likes_comment_id', 'comment_likes', ['comment_id'], unique=False)
    # Comment.likes et tous les Vote restent intacts : aucune attribution fictive.


def downgrade():
    table = sa.Table('comment_likes', sa.MetaData(), autoload_with=op.get_bind())
    if op.get_bind().execute(sa.select(table.c.id).limit(1)).first():
        raise RuntimeError('Retour refusé : des likes individuels seraient perdus.')
    op.drop_index('ix_comment_likes_comment_id', table_name='comment_likes')
    op.drop_table('comment_likes')
