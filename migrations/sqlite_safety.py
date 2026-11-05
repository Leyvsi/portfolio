"""Encadrer les reconstructions Alembic SQLite en maintenance exclusive.

Ce module ne choisit ni n'ouvre de base. L'appelant fournit sa connexion.
Les migrations applicatives ordinaires gardent les clés étrangères actives.
"""
from contextlib import contextmanager


@contextmanager
def sqlite_migration_scope(connection):
    """Transaction explicite, contrôle FK avant/après, réactivation même sur échec."""
    if connection.dialect.name != 'sqlite':
        raise ValueError('Connexion SQLite requise.')
    if connection.in_transaction():
        raise RuntimeError('Une connexion sans transaction est requise.')
    raw = connection.connection.dbapi_connection
    raw.execute('PRAGMA foreign_keys=ON')
    if raw.execute('PRAGMA foreign_key_check').fetchone() is not None:
        raise RuntimeError('Intégrité initiale invalide ; migration refusée.')
    raw.execute('PRAGMA foreign_keys=OFF')
    if raw.execute('PRAGMA foreign_keys').fetchone()[0] != 0:
        raise RuntimeError('Impossible de suspendre les FK hors transaction.')
    try:
        with connection.begin():
            # sqlite3 en mode historique ne démarre pas de transaction sur DDL.
            connection.exec_driver_sql('BEGIN')
            connection.info['sqlite_migration_integrity_scope'] = True
            yield
            if connection.exec_driver_sql('PRAGMA foreign_key_check').first() is not None:
                raise RuntimeError('Intégrité finale invalide ; rollback requis.')
    finally:
        connection.info.pop('sqlite_migration_integrity_scope', None)
        raw.execute('PRAGMA foreign_keys=ON')
        if raw.execute('PRAGMA foreign_keys').fetchone()[0] != 1:
            raise RuntimeError('Réactivation des FK impossible.')
