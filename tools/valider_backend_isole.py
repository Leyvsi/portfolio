"""Tests de confiance sur SQLite mémoire ; gardes Python sans frontière système."""
from pathlib import Path
import argparse
import ast
from contextlib import ExitStack
from contextvars import ContextVar
import json
import os
import socket
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

def create_audit_guard(evidence, counters, sqlite_authorized=lambda: False):
    """Garde des API Python auditées ; ne remplace pas une sandbox système."""
    evidence = evidence.resolve()
    def writable(name, dir_fd=None):
        # Aucun descripteur de répertoire opaque ne permet de contourner
        # la résolution par rapport au dossier courant.
        if dir_fd not in (None, -1) or isinstance(name, int):
            counters['write_denied'] += 1
            raise PermissionError('Descripteur non résolu interdit.')
        path = Path(os.fsdecode(name)).resolve()
        if not path.is_relative_to(evidence):
            counters['write_denied'] += 1
            raise PermissionError('Mutation hors ressources temporaires interdite.')
    def audit(event, values):
        if event.startswith('socket.'):
            counters['network_denied'] += 1
            raise PermissionError('Réseau interdit dans ce harnais.')
        if event in {'subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn'}:
            raise PermissionError('Sous-processus interdit.')
        if event == 'sqlite3.connect':
            if values[0] != ':memory:':
                counters['file_database_denied'] += 1
                raise PermissionError('Seule SQLite mémoire est autorisée.')
            if not sqlite_authorized():
                counters['sqlite_bypass_denied'] += 1
                raise PermissionError('Création SQLite hors de la fabrique contrôlée interdite.')
            counters['sqlite_memory_connections'] += 1
        if event in {'sqlite3.enable_load_extension', 'sqlite3.load_extension'}:
            raise PermissionError('Extension SQLite interdite.')
        if event == 'open':
            name, mode, flags = values
            writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or bool(
                (flags or 0) & (os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC))
            if writing:
                writable(name)
            elif not isinstance(name, int):
                path = Path(os.fsdecode(name)).resolve()
                if (path.name.startswith('.env') or path.suffix.lower() in
                        {'.db', '.sqlite', '.sqlite3', '.pem', '.key', '.pfx', '.p12'} or
                        path.name.lower().startswith('cookies')):
                    counters['private_read_denied'] += 1
                    raise PermissionError('Lecture privée interdite.')
        elif event in {'os.mkdir', 'os.chmod', 'os.chown', 'os.utime'}:
            writable(values[0], values[-1])
        elif event in {'os.remove', 'os.rmdir'}:
            writable(values[0], values[1])
        elif event == 'os.rename':
            writable(values[0], values[2])
            writable(values[1], values[3])
        elif event == 'os.truncate':
            writable(values[0])
        elif event in {'os.link', 'os.symlink'}:
            # Les liens ne sont pas nécessaires aux suites ; refus explicite.
            counters['write_denied'] += 1
            raise PermissionError('Création de lien interdite.')
    return audit

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate-root',type=Path,required=True)
    parser.add_argument('--suite',action='append',default=[])
    parser.add_argument('--liste',action='store_true')
    args=parser.parse_args();root=args.candidate_root.resolve()
    if not (root/'backend/tests/test_reports.py').is_file():raise SystemExit('Racine candidate invalide.')
    files=sorted((root/'backend/tests').glob('test_*.py'))
    if args.suite:
        if any(Path(x).name!=x or not x.startswith('test_') or not x.endswith('.py') for x in args.suite):raise SystemExit('Nom de suite invalide.')
        files=[root/'backend/tests'/x for x in args.suite]
    if args.liste:
        rows=[{'fichier':p.name,'methodes_test':sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith('test_') for n in ast.walk(ast.parse(p.read_text(encoding='utf-8'))))} for p in files]
        print(json.dumps({'mode':'LISTE_STATIQUE_SANS_EXECUTION','suites':rows},ensure_ascii=True));return 0
    # Les bibliothèques sont chargées avant les gardes, sans application Flask.
    import dotenv
    import sqlalchemy as sa
    from sqlalchemy.engine import Engine
    evidence=Path(tempfile.mkdtemp(prefix='lpe-backend-isole-')).resolve()
    counters={'network_denied':0,'file_database_denied':0,'write_denied':0,'private_read_denied':0,'sqlite_memory_connections':0,
              'sqlite_bypass_denied':0,'sqlite_policy_denied':0}
    creation_authorized = ContextVar('lpe_sqlite_creation_authorized', default=False)
    audit = create_audit_guard(evidence, counters, creation_authorized.get)
    original_connect = sqlite3.connect
    original_connection_type = sqlite3.Connection
    class GuardedConnection(original_connection_type):
        def set_authorizer(self, callback):
            counters['sqlite_policy_denied'] += 1
            raise PermissionError('Remplacement de l’autoriseur du harnais interdit.')
    def memory_connect(*positional, **keywords):
        # Une fabrique arbitraire pourrait exécuter du SQL dans son __init__,
        # avant l'installation de l'autoriseur : seules les fabriques connues
        # sont acceptées, puis remplacées par notre sous-classe contrôlée.
        supplied_factory = positional[5] if len(positional) > 5 else keywords.get('factory', original_connection_type)
        if supplied_factory is not original_connection_type:
            counters['sqlite_bypass_denied'] += 1
            raise PermissionError('Fabrique SQLite personnalisée interdite.')
        if len(positional) > 5:
            positional = (*positional[:5], GuardedConnection, *positional[6:])
        else:
            keywords['factory'] = GuardedConnection
        token = creation_authorized.set(True)
        try:
            connection = original_connect(*positional, **keywords)
        finally:
            creation_authorized.reset(token)
        def authorize(action, first, second, database, trigger):
            if action in (sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH):
                counters['file_database_denied'] += 1
                return sqlite3.SQLITE_DENY
            if action == sqlite3.SQLITE_FUNCTION and second == 'load_extension':
                counters['sqlite_policy_denied'] += 1
                return sqlite3.SQLITE_DENY
            if action == sqlite3.SQLITE_PRAGMA and second is not None and first.lower() in {
                    'temp_store', 'temp_store_directory', 'data_store_directory'}:
                counters['sqlite_policy_denied'] += 1
                return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK
        try:
            # Le handle de l'événement d'audit n'est pas encore initialisé.
            # Configurer la mémoire puis l'autoriseur avant de rendre la base.
            connection.execute('PRAGMA temp_store=MEMORY')
            original_connection_type.set_authorizer(connection, authorize)
        except BaseException:
            connection.close()
            raise
        return connection
    def foreign_keys(connection,_):
        cursor=connection.cursor();cursor.execute('PRAGMA foreign_keys=ON');cursor.close()
    sa.event.listen(Engine,'connect',foreign_keys)
    sys.dont_write_bytecode=True
    sys.path[:0]=[str(root),str(root/'backend'),str(root/'backend/tests')]
    sys.addaudithook(audit)
    tempfile.tempdir = str(evidence)
    settings={'SECRET_KEY':'validation-synthetic-only','CORS_ALLOWED_ORIGINS':'http://localhost:3000',
              'DATABASE_URL':'sqlite:///:memory:','SESSION_COOKIE_SECURE':'false',
              'PORTFOLIO_ISOLATED_TESTS':'6e3-memory-only','PORTFOLIO_TEST_EVIDENCE':str(evidence),
              **{name:'' for name in ('AIVEN_DB_HOST','AIVEN_DB_PORT','AIVEN_DB_USER','AIVEN_DB_PASSWORD','AIVEN_DB_NAME','AIVEN_CA_CERT')}}
    with ExitStack() as stack:
        stack.enter_context(patch.object(sqlite3, 'connect', memory_connect))
        stack.enter_context(patch.object(sqlite3.dbapi2, 'connect', memory_connect))
        stack.enter_context(patch.dict(os.environ,settings,clear=True))
        stack.enter_context(patch.object(dotenv,'load_dotenv',return_value=False))
        suite=unittest.TestSuite()
        for path in files:suite.addTests(unittest.defaultTestLoader.discover(str(path.parent),pattern=path.name))
        result=unittest.TextTestRunner(verbosity=2).run(suite)
        report={'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
                'resultat':'PASS' if result.wasSuccessful() else 'FAIL','guard_counts':counters,
                'mysql_tested':False,'persistent_database_opened':False,'suites':[p.name for p in files],
                'security_scope':'Gardes Python pour tests de confiance ; aucun confinement système propre au harnais attesté.'}
        (evidence/'resultat.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'rapport':str(evidence/'resultat.json'),**report},ensure_ascii=True))
        return 0 if result.wasSuccessful() else 1

if __name__=='__main__':raise SystemExit(main())
