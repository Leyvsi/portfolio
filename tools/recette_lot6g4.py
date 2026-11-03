"""Recette synthétique 6G.4 : inspection WSGI sans écoute par défaut.

--serve exige une autorisation humaine distincte. Aucun lancement de navigateur.
La base est exclusivement SQLite en mémoire et disparaît à l'arrêt.
"""
from contextlib import ExitStack
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch
import argparse
import hashlib
import importlib.metadata
import json
import os
import secrets
import socket
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).with_name('recette_lot6g4_sources.json')
HOST, PORT = '127.0.0.1', 5064
PUBLIC = frozenset({
    'index.html', 'histoires.html', 'coldcases.html', 'dossier.html',
    'inscription.html', 'connexion.html', 'admin-connexion.html',
    'admin-dashboard.html', 'theories.html', 'proposer-histoire.html',
    'api.js', 'app.js', 'comments.js', 'likes.js', 'admin-dashboard.js',
    'admin-users.js', 'admin-stories.js', 'theories-list.js', 'styles.css',
    'images/default-story.svg',
})
AIVEN = ('AIVEN_DB_HOST', 'AIVEN_DB_PORT', 'AIVEN_DB_USER',
         'AIVEN_DB_PASSWORD', 'AIVEN_DB_NAME', 'AIVEN_CA_CERT')


def sensitive(path):
    return (path.name.lower().startswith(('.env', 'cookies')) or
            path.suffix.lower() in {'.db', '.sqlite', '.sqlite3', '.pem', '.key', '.p12', '.pfx'} or
            path.is_relative_to(ROOT / 'certs'))


def validate_sources():
    """Refuser toute source différente ; ne jamais renouveler les empreintes ici."""
    config = json.loads(MANIFEST.read_text(encoding='utf-8'))
    approved = set()
    for name, expected in config['source_sha256_lf'].items():
        source = (ROOT / name).resolve()
        if (not source.is_relative_to(ROOT) or source.is_symlink() or sensitive(source) or
                source.suffix not in {'.py', '.js', '.html', '.css', '.svg', '.json'} or
                source.is_relative_to(ROOT / 'migrations') or
                source.name in {'donnees.js', 'histoires-originales.json', 'ancien_app.py'}):
            raise SystemExit('Source interdite dans le manifeste de recette.')
        if hashlib.sha256(source.read_bytes().replace(b'\r\n', b'\n')).hexdigest() != expected:
            raise SystemExit('Source différente du kit inspecté : ' + name)
        approved.add(source)
    if not {(ROOT / 'frontend' / name).resolve() for name in PUBLIC} <= approved:
        raise SystemExit('Ressource publique absente du manifeste.')
    if Path(__file__).resolve() not in approved:
        raise SystemExit('Le kit doit lui-même être figé dans son manifeste.')
    if importlib.metadata.version('SQLAlchemy') != '2.0.53':
        raise SystemExit('Version SQLAlchemy à réinspecter.')
    return approved


class Isolation:
    """Gardes locaux aux processus du kit, sans changement Windows ou pare-feu."""
    def __init__(self, evidence, approved):
        self.evidence, self.approved = evidence.resolve(), approved
        self.runtime = [Path(sys.prefix).resolve(), Path(sys.base_prefix).resolve()]
        self.serving = False
        self.counts = dict.fromkeys(('private_read', 'repository_write', 'other_write',
                                    'network', 'non_memory_database', 'migration', 'subprocess'), 0)

    def blocked(self, kind):
        self.counts[kind] += 1
        raise PermissionError('Recette isolée : opération interdite (' + kind + ').')

    def read(self, path):
        path = Path(os.fsdecode(path)).resolve()
        compiled = path.parent.parent / (path.name.split('.')[0] + '.py') if path.parent.name == '__pycache__' else None
        if sensitive(path) or not (path in self.approved or compiled in self.approved or
                                   path.is_relative_to(self.evidence) or
                                   any(path.is_relative_to(base) for base in self.runtime)):
            self.blocked('private_read')

    def write(self, path):
        path = Path(os.fsdecode(path)).resolve()
        if path.is_relative_to(ROOT):
            self.blocked('repository_write')
        if not path.is_relative_to(self.evidence):
            self.blocked('other_write')

    def database(self, engine):
        if engine.url.drivername != 'sqlite' or engine.url.database != ':memory:':
            self.blocked('non_memory_database')

    def audit(self, event, values):
        if event == 'open':
            name, mode, flags = values
            if isinstance(name, int):
                return
            writing = (isinstance(mode, str) and any(c in mode for c in 'wax+') or
                       bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC)))
            (self.write if writing else self.read)(name)
        elif event == 'sqlite3.connect' and values[0] != ':memory:':
            self.blocked('non_memory_database')
        elif event == 'exec' and values:
            filename = getattr(values[0], 'co_filename', '')
            if filename and Path(filename).resolve().is_relative_to(ROOT / 'migrations'):
                self.blocked('migration')
        elif event.startswith('socket.'):
            # Seule l'écoute future autorisée peut créer/accepter un socket.
            if self.serving and event == 'socket.__new__':
                return
            if self.serving and event == 'socket.bind' and values[1] == (HOST, PORT):
                return
            if self.serving and event == 'socket.getaddrinfo' and values[:2] == (HOST, PORT):
                return
            self.blocked('network')
        elif event in {'subprocess.Popen', 'os.system', 'os.exec', 'os.posix_spawn'}:
            self.blocked('subprocess')
        elif event in {'os.remove', 'os.rmdir', 'os.mkdir', 'os.chmod', 'os.chown',
                       'os.utime', 'os.truncate', 'os.rename', 'os.link', 'os.symlink'}:
            for name in values[:2] if event in {'os.rename', 'os.link', 'os.symlink'} else values[:1]:
                if isinstance(name, (str, bytes, os.PathLike)):
                    self.write(name)


def public_application(api_app):
    from run_local import create_local_app
    real = create_local_app(api_app)

    def application(environ, start_response):
        path = environ.get('PATH_INFO', '')
        if path == '/' or path.startswith('/api/v1/') or path.lstrip('/') in PUBLIC:
            return real(environ, start_response)
        start_response('403 Forbidden', [('Content-Type', 'text/plain; charset=utf-8')])
        return [b'Ressource hors du perimetre de recette.']
    return application


def seed(db, models):
    credentials = {}
    for number, name in enumerate(('admin', 'alice', 'bob'), 1):
        password = secrets.token_urlsafe(20) + 'Aa1!'
        username = 'jury6g4_' + name
        user = models.User(id=number, username=username, email=name + '6g4@example.invalid',
                           is_admin=name == 'admin', is_banned=False)
        user.set_password(password)
        db.session.add(user)
        credentials[name] = {'username': username, 'password': password}
    db.session.add_all([models.Category(id=1, name='Histoires résolues'),
                        models.Category(id=2, name='Cold Cases')])
    db.session.flush()
    for identifier, slug, category in ((17, 'recette-6g4', 1), (42, 'recette-coldcase-6g4', 2)):
        db.session.add(models.Story(id=identifier, slug=slug, title='Dossier fictif ' + str(identifier),
                                    summary='Démonstration isolée uniquement.', content='Contenu fictif de recette.',
                                    image_url='/images/default-story.svg', category_id=category, author_id=1))
    db.session.commit()
    return credentials


def seven_counts(db, models):
    return {'stories': models.Story.query.filter_by(archived_at=None).count(),
            'resolved': models.Story.query.filter_by(archived_at=None, category_id=1).count(),
            'coldcases': models.Story.query.filter_by(archived_at=None, category_id=2).count(),
            'users': models.User.query.count(), 'comments': models.Comment.query.count(),
            'reports': models.Report.query.count(),
            'pending-proposals': models.Proposal.query.filter_by(status='pending').count()}


def inspect_assets(client):
    class Assets(HTMLParser):
        def __init__(self):
            super().__init__(); self.paths = []
        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == 'script':
                self.paths.append(attrs.get('src'))
            if tag == 'link' and attrs.get('rel') == 'stylesheet':
                self.paths.append(attrs.get('href'))
    for name in sorted(PUBLIC):
        response = client.get('/' + name)
        assert response.status_code == 200, name
        if name.endswith('.html'):
            parsed = Assets(); parsed.feed(response.get_data(as_text=True))
            assert all(path in PUBLIC for path in parsed.paths), name
    for name in ('donnees.js', 'histoires-originales.json', '.env', 'cookies.txt',
                 'README.md', '../docs/soutenance/BILAN_LOT6G3.md'):
        assert client.get('/' + name).status_code == 403


def check_journey(app, application, db, models, credentials):
    """Vraies routes/transactions, transport WSGI ; aucun navigateur simulé ici."""
    from sqlalchemy.exc import SQLAlchemyError
    from werkzeug.test import Client
    from werkzeug.wrappers import Response
    client = Client(application, Response, use_cookies=True)
    exchanges, checks = [], []
    csrf = None

    def request(method, path, status=200, body=None, token=True):
        response = client.open('/api/v1' + path, method=method, json=body,
                               headers={'X-CSRF-Token': csrf} if token and csrf else {})
        assert response.status_code == status, (method, path, response.status_code, status)
        exchanges.append({'method': method, 'path': path, 'status': response.status_code})
        return response.get_json()

    def login(name):
        nonlocal csrf
        csrf = request('POST', '/login', body=credentials[name])['csrf_token']

    request('POST', '/users', 201, {'username': 'jury6g4_inscrit', 'email': 'inscrit6g4@example.invalid',
                                 'password': secrets.token_urlsafe(20) + 'Aa1!'})
    login('alice'); checks.append('inscription et connexion réelles')
    assert request('GET', '/stories/slug/recette-6g4')['id'] == 17
    assert request('GET', '/stories/slug/recette-coldcase-6g4')['id'] == 42
    comment = request('POST', '/stories/17/comments', 201, {'text': 'Commentaire fictif 6G.4'})['comment']
    identifier = comment['id']; checks.append('deux catégories et commentaire réel')
    paths = ('/votes/17', '/comments/' + str(identifier) + '/like')
    for path in paths:
        request('POST', path, 403, token=False)
        request('POST', path, 201 if path.startswith('/votes') else 200)
        request('POST', path, 409)
        state = request('GET', path)
        assert state['likes'] == 1 and state['liked_by_me'] is True
        state = request('DELETE', path)
        assert state['likes'] == 0 and state['changed'] is True
        assert request('DELETE', path)['changed'] is False
        request('POST', path, 201 if path.startswith('/votes') else 200)
    checks.append('likes ajout retrait réajout unicité et refus CSRF')
    request('POST', '/comments/' + str(identifier) + '/report', 403, {'reason': 'Refus fictif'}, token=False)
    request('POST', '/comments/' + str(identifier) + '/report', 201, {'reason': 'Signalement fictif 6G.4'})
    # Le compteur historique reste protégé même dans cette mémoire synthétique.
    with app.app_context():
        legacy = models.Comment(story_id=42, user_id=2, username='jury6g4_alice',
                                text='Témoin historique strictement synthétique.', likes=7)
        db.session.add(legacy); db.session.commit()
        legacy_id = legacy.id
    for method in ('GET', 'POST', 'DELETE'):
        assert request(method, '/comments/' + str(legacy_id) + '/like', 409)['code'] == 'LEGACY_LIKES_UNRESOLVED'
    with app.app_context():
        assert db.session.get(models.Comment, legacy_id).likes == 7
    checks.append('signalement réel et historique incompatible préservé/refusé')
    with app.app_context():
        before = {table.name: db.session.execute(db.select(db.func.count()).select_from(table)).scalar_one()
                  for table in db.metadata.sorted_tables}
    with patch.object(db.session, 'commit', side_effect=SQLAlchemyError('synthetic-commit-failure')):
        result = request('POST', '/votes/42', 500)
        assert 'synthetic-commit-failure' not in json.dumps(result)
    with app.app_context():
        assert before == {table.name: db.session.execute(db.select(db.func.count()).select_from(table)).scalar_one()
                          for table in db.metadata.sorted_tables}
    checks.append('erreur serveur après flush et rollback sans fuite')
    request('POST', '/logout'); csrf = None
    request('DELETE', paths[0], 401)
    login('admin')
    assert any(row['target_id'] == str(identifier) for row in request('GET', '/admin/reports'))
    detail = request('GET', '/admin/stories/17')
    assert detail['votes'] == 1 and detail['comments'][0]['likes'] == 1
    stats, stories, proposals = request('GET', '/stats'), request('GET', '/stories'), request('GET', '/proposals')
    observed = {'stories': len(stories), 'resolved': sum(row['category_id'] == 1 for row in stories),
                'coldcases': sum(row['category_id'] == 2 for row in stories),
                **stats, 'pending-proposals': sum(row['status'] == 'pending' for row in proposals)}
    with app.app_context():
        assert observed == seven_counts(db, models)
    checks.append('administration et sept valeurs API égales aux SELECT')
    request('POST', '/admin/stories/17/archive')
    request('GET', '/stories/17/comments', 404)
    request('GET', paths[0], 404)
    request('POST', '/admin/stories/17/restore')
    assert request('GET', paths[0])['likes'] == 1
    request('POST', '/admin/users/3/ban')
    request('POST', '/logout'); csrf = None
    request('POST', '/login', 403, credentials['bob'])
    login('alice')
    assert request('GET', paths[1])['liked_by_me'] is True
    checks.append('archive restauration bannissement et conservation des likes')
    return {'result': 'PASS', 'checks': checks, 'requests': exchanges,
            'seven_counts': observed, 'browser': 'NOT_EXECUTED', 'transport': 'WSGI'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--autorisation-execution-confirmee', action='store_true')
    parser.add_argument('--check-journey', action='store_true', help='Parcours API isolé, sans écoute ; mémoire jetée ensuite.')
    parser.add_argument('--probe-isolation', action='store_true', help='Sondes de refus séparées, sans import applicatif.')
    args = parser.parse_args()
    if args.serve and not args.autorisation_execution_confirmee:
        parser.error('Obtenir une autorisation humaine distincte avant --serve ; le marqueur ne la remplace pas.')
    if args.serve and (args.check_journey or args.probe_isolation):
        parser.error('Les essais et le lancement manuel doivent utiliser des processus distincts.')
    approved = validate_sources()
    temp_root = Path(os.environ.get('TEMP') or os.environ.get('TMP') or '').resolve()
    if temp_root.is_relative_to(ROOT) or not temp_root.is_dir():
        raise SystemExit('Le dossier temporaire doit rester hors du dépôt.')
    evidence = Path(tempfile.mkdtemp(prefix='portfolio-recette6g4-', dir=temp_root)).resolve()
    env = {key: os.environ[key] for key in ('SystemRoot', 'WINDIR', 'COMSPEC', 'PATH') if key in os.environ}
    os.environ.clear()
    os.environ.update(env | {'TEMP': str(evidence), 'TMP': str(evidence),
                            'SECRET_KEY': secrets.token_urlsafe(32), 'DATABASE_URL': 'sqlite:///:memory:',
                            'CORS_ALLOWED_ORIGINS': 'http://' + HOST + ':' + str(PORT),
                            'SESSION_COOKIE_SECURE': 'false', **{key: '' for key in AIVEN}})
    sys.dont_write_bytecode = True
    isolation = Isolation(evidence, approved)
    sys.addaudithook(isolation.audit)
    if args.probe_isolation:
        checks = []
        for name, action in (
            ('private_read', lambda: isolation.read(ROOT / '.env')),
            ('repository_write', lambda: isolation.write(ROOT / 'README.md')),
            ('outside_write', lambda: isolation.write(ROOT.parent / 'forbidden.txt')),
            ('file_database', lambda: sqlite3.connect(str(evidence / 'forbidden.sqlite3'))),
            ('network', lambda: isolation.audit('socket.connect', (None, (HOST, PORT)))),
            ('migration', lambda: isolation.blocked('migration')),
            ('subprocess', lambda: isolation.audit('subprocess.Popen', ())),
        ):
            try:
                action()
            except PermissionError:
                checks.append(name)
            else:
                raise RuntimeError('Sonde non bloquée : ' + name)
        receipt = {'result': 'PASS', 'stage': 'probes only', 'blocked_before_io': checks,
                   'probe_counts': isolation.counts, 'server_started': False, 'browser_started': False}
        (evidence / 'probes.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
        print(json.dumps(receipt)); print('Preuves : ' + str(evidence)); return

    import platform
    import sysconfig
    architecture = {'win-amd64': 'AMD64', 'win-arm64': 'ARM64', 'win32': 'x86',
                    'linux-x86_64': 'x86_64'}.get(sysconfig.get_platform())
    if architecture is None:
        raise SystemExit('Plateforme à réinspecter.')
    with patch.object(platform, 'machine', return_value=architecture):
        import dotenv
        import dotenv.main
        import pymysql
        from sqlalchemy.engine import Engine
        from alembic.migration import MigrationContext
        from alembic.operations import Operations
        import alembic.command
    original_sqlite = sqlite3.dbapi2.connect
    engine_connect, engine_raw = Engine.connect, Engine.raw_connection

    def connect(database, *positional, **options):
        if database != ':memory:':
            isolation.blocked('non_memory_database')
        connection = original_sqlite(database, *positional, **options)
        connection.execute('PRAGMA foreign_keys=ON')
        assert connection.execute('PRAGMA foreign_keys').fetchone()[0] == 1
        def authorize(action, *unused):
            if action in {sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH}:
                isolation.blocked('non_memory_database')
            return sqlite3.SQLITE_OK
        connection.set_authorizer(authorize)
        return connection

    def engine_guard(original, engine, *positional, **options):
        isolation.database(engine)
        return original(engine, *positional, **options)

    with ExitStack() as stack:
        for owner, name, value in (
            (dotenv, 'load_dotenv', lambda *a, **k: False),
            (dotenv.main, 'load_dotenv', lambda *a, **k: False),
            (pymysql, 'connect', lambda *a, **k: isolation.blocked('non_memory_database')),
            (sqlite3, 'connect', connect), (sqlite3.dbapi2, 'connect', connect),
            (Engine, 'connect', lambda engine, *a, **k: engine_guard(engine_connect, engine, *a, **k)),
            (Engine, 'raw_connection', lambda engine, *a, **k: engine_guard(engine_raw, engine, *a, **k)),
            (MigrationContext, 'run_migrations', lambda *a, **k: isolation.blocked('migration')),
            (Operations, 'invoke', lambda *a, **k: isolation.blocked('migration')),
        ):
            stack.enter_context(patch.object(owner, name, value))
        for name in ('upgrade', 'downgrade', 'stamp', 'revision', 'ensure_version'):
            stack.enter_context(patch.object(alembic.command, name, lambda *a, **k: isolation.blocked('migration')))
        sys.path[:0] = [str(ROOT / 'backend'), str(ROOT)]
        from index import app
        import models
        from werkzeug.test import Client
        from werkzeug.wrappers import Response
        db = models.db
        with app.app_context():
            isolation.database(db.engine)
            assert all(not os.environ[key] for key in AIVEN)
            db.create_all()  # Schéma neuf synthétique ; aucune migration d'une base existante.
            credentials = seed(db, models)
            assert len(db.metadata.tables) == 10
        application = public_application(app.wsgi_app)
        inspect_assets(Client(application, Response, use_cookies=True))
        if args.check_journey:
            journey = check_journey(app, application, db, models, credentials)
            (evidence / 'journey.json').write_text(json.dumps(journey, indent=2), encoding='utf-8')
        with app.app_context():
            assert db.session.execute(db.text('PRAGMA foreign_keys')).scalar_one() == 1
            assert not db.session.execute(db.text('PRAGMA foreign_key_check')).all()
            assert all(row[2] == '' for row in db.session.execute(db.text('PRAGMA database_list')))
            counts = seven_counts(db, models)
        receipt = {'result': 'READY', 'stage': 'WSGI inspection without listener',
                   'sqlite': ':memory:', 'database_files': [], 'foreign_keys': True,
                   'aiven_parameters_empty': True, 'dotenv_disabled_before_application_import': True,
                   'server_started': False, 'browser_started': False, 'guards': isolation.counts,
                   'seven_counts_sql': counts, 'journey': 'PASS' if args.check_journey else 'NOT_REQUESTED',
                   'all_page_script_references_served': True, 'schema': 'new synthetic schema; not a migration'}
        if any(isolation.counts.values()):
            receipt['result'] = 'FAIL'
        (evidence / 'isolation.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
        if receipt['result'] != 'READY':
            raise RuntimeError('Inspection refusée : opération interdite détectée.')
        print(json.dumps(receipt), flush=True); print('Preuves : ' + str(evidence), flush=True)
        if not args.serve:
            return
        # Branche préparée seulement : ne pas la lancer pendant 6G.4.
        from werkzeug.serving import make_server, WSGIRequestHandler
        class QuietHandler(WSGIRequestHandler):
            def log_request(self, *unused):
                pass
        stack.enter_context(patch.object(socket, 'getfqdn', return_value='localhost'))
        isolation.serving = True
        with make_server(HOST, PORT, application, threaded=False, request_handler=QuietHandler) as server:
            receipt.update(stage='authorized local listener', server_started=True)
            (evidence / 'isolation.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
            print('RECETTE FICTIVE : http://' + HOST + ':' + str(PORT), flush=True)
            print('Comptes et mots de passe éphémères (ne pas capturer) : ' + json.dumps(credentials), flush=True)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass


if __name__ == '__main__':
    main()
