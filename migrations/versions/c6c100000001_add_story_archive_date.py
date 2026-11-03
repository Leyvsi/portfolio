"""Date d'archivage réversible des dossiers — migration préparée, non déployée.

Revision ID: c6c100000001
Revises: 82deda84bc35
"""

from alembic import op
import sqlalchemy as sa

revision = 'c6c100000001'
down_revision = '82deda84bc35'
branch_labels = None
depends_on = None


def upgrade():
    # Une colonne nullable sans défaut rend tous les dossiers existants actifs.
    # Aucune réécriture d'enfant, relation, FK ou règle CASCADE.
    op.add_column('stories', sa.Column('archived_at', sa.DateTime(), nullable=True))


def downgrade():
    # Retirer cette colonne perd l'état d'archive et rend les dossiers visibles
    # à l'ancien code : contrôler ce risque avant toute rétrogradation réelle.
    op.drop_column('stories', 'archived_at')
