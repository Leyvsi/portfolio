"""Préparer une recette fictive ; --serve exige une autorisation humaine préalable.

Par défaut : vérifier l'isolation via WSGI, sans ouvrir de port ni navigateur.
Ne jamais utiliser run_local.main(), qui lirait la configuration privée.
"""
from pathlib import Path
from contextlib import ExitStack
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
import uuid

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).with_name('recette_lot6f2_sources.json')
PUBLIC = {'index.html','histoires.html','coldcases.html','dossier.html','inscription.html',
          'connexion.html','admin-connexion.html','admin-dashboard.html','theories.html',
          'proposer-histoire.html','api.js','app.js','comments.js','admin-dashboard.js',
          'admin-users.js','admin-stories.js','theories-list.js','styles.css','images/default-story.svg'}
AIVEN = ('AIVEN_DB_HOST','AIVEN_DB_PORT','AIVEN_DB_USER','AIVEN_DB_PASSWORD','AIVEN_DB_NAME','AIVEN_CA_CERT')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serve', action='store_true', help='Seulement après autorisation spécifique ; aucun navigateur lancé.')
    parser.add_argument('--autorisation-execution-confirmee', action='store_true')
    args = parser.parse_args()
    if args.serve and not args.autorisation_execution_confirmee:
        parser.error('Obtenir une autorisation humaine distincte avant --serve ; le marqueur ne la remplace pas.')
    config = json.loads(MANIFEST.read_text(encoding='utf-8'))
    for name, digest in config['source_sha256_lf'].items():
        source = (ROOT/name).resolve()
        if not source.is_relative_to(ROOT) or source.name.lower().startswith(('.env','cookies')) or source.suffix.lower() not in {'.py','.js','.cjs','.json','.html','.css','.svg'}:
            raise SystemExit('Chemin interdit dans le manifeste de recette.')
        actual = hashlib.sha256(source.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
        if actual != digest:
            raise SystemExit('Source différente du kit inspecté : '+name)
    if importlib.metadata.version('SQLAlchemy') != '2.0.53':
        raise SystemExit('Revoir le harnais pour cette version SQLAlchemy.')
    # Un dossier neuf uniquement pour les preuves, jamais une base fichier.
    evidence = Path(os.environ.get('TEMP', str(ROOT.parent)))/('portfolio-recette6f2-'+uuid.uuid4().hex)
    if evidence.resolve().is_relative_to(ROOT):
        raise SystemExit('Les preuves de recette doivent rester hors du dépôt.')
    evidence.mkdir(exist_ok=False)
    original_env = {key:os.environ[key] for key in ('SystemRoot','WINDIR','COMSPEC','PATH') if key in os.environ}
    os.environ.clear()
    os.environ.update(original_env | {'TEMP':str(evidence),'TMP':str(evidence),
        'SECRET_KEY':secrets.token_urlsafe(32), 'DATABASE_URL':'sqlite:///:memory:',
        'CORS_ALLOWED_ORIGINS':'http://127.0.0.1:5062','SESSION_COOKIE_SECURE':'false',
        **{key:'' for key in AIVEN}})
    sys.dont_write_bytecode = True
    allowed = {(ROOT/name).resolve() for name in config['source_sha256_lf']}
    allowed.add(Path(__file__).resolve())
    runtime = [Path(sys.prefix).resolve(),Path(sys.base_prefix).resolve()]
    counters = {key:0 for key in ('private_read','repository_write','other_write','outgoing_network','non_memory_database','migration','subprocess')}
    serving = False

    def blocked(key):
        counters[key] += 1
        raise PermissionError('Recette isolée : opération interdite ('+key+').')

    def audit(event, values):
        if event == 'open':
            name,mode,flags = values
            if isinstance(name,int): return
            path = Path(os.fsdecode(name)).resolve()
            writing = isinstance(mode,str) and any(c in mode for c in 'wax+') or bool(flags & (os.O_WRONLY|os.O_RDWR|os.O_APPEND|os.O_CREAT|os.O_TRUNC))
            if writing:
                if path.is_relative_to(ROOT): blocked('repository_write')
                if not path.is_relative_to(evidence): blocked('other_write')
            else:
                sensitive = path.name.lower().startswith(('.env','cookies')) or path.suffix.lower() in {'.db','.sqlite','.sqlite3','.pem','.key','.p12','.pfx'}
                compiled_source = path.parent.parent/(path.name.split('.')[0]+'.py') if path.parent.name=='__pycache__' else None
                if sensitive or not (path in allowed or compiled_source in allowed or path.is_relative_to(evidence) or any(path.is_relative_to(p) for p in runtime)):
                    blocked('private_read')
        elif event == 'sqlite3.connect' and values[0] != ':memory:': blocked('non_memory_database')
        elif event == 'exec' and values:
            if str(getattr(values[0],'co_filename','')).replace('\\','/').startswith(str(ROOT/'migrations').replace('\\','/')): blocked('migration')
        elif event.startswith('socket.'):
            if serving and event in {'socket.__new__','socket.bind'}:
                if event == 'socket.bind' and values[1] != ('127.0.0.1',5062): blocked('outgoing_network')
            elif serving and event == 'socket.getaddrinfo' and values[:2] == ('127.0.0.1',5062): pass
            else: blocked('outgoing_network')
        elif event in {'subprocess.Popen','os.system','os.exec','os.posix_spawn'}: blocked('subprocess')
        elif event in {'os.remove','os.rmdir','os.mkdir','os.chmod','os.chown','os.utime','os.truncate','os.rename','os.link','os.symlink'}:
            for name in values[:2] if event in {'os.rename','os.link','os.symlink'} else values[:1]:
                if not isinstance(name,(str,bytes,os.PathLike)): continue
                path=Path(os.fsdecode(name)).resolve()
                if path.is_relative_to(ROOT): blocked('repository_write')
                if not path.is_relative_to(evidence): blocked('other_write')

    sys.addaudithook(audit)
    import platform
    import sysconfig
    architecture={'win-amd64':'AMD64','win-arm64':'ARM64','win32':'x86','linux-x86_64':'x86_64'}.get(sysconfig.get_platform())
    if architecture is None: raise SystemExit('Plateforme à inspecter avant recette.')
    # Éviter le sondage système/hostname de platform pendant l'import SQLAlchemy.
    with patch.object(platform,'machine',return_value=architecture):
        import dotenv
        import dotenv.main
        import pymysql
        from sqlalchemy.engine import Engine
        from alembic.migration import MigrationContext
        from alembic.operations import Operations
        import alembic.command
    native_connect=sqlite3.dbapi2.connect
    engine_connect,engine_raw=Engine.connect,Engine.raw_connection

    def connect(database,*args,**kwargs):
        if database != ':memory:': blocked('non_memory_database')
        connection=native_connect(database,*args,**kwargs)
        connection.execute('PRAGMA foreign_keys=ON')
        assert connection.execute('PRAGMA foreign_keys').fetchone()[0] == 1
        def authorize(action,*unused):
            if action in {sqlite3.SQLITE_ATTACH,sqlite3.SQLITE_DETACH}: blocked('non_memory_database')
            return sqlite3.SQLITE_OK
        connection.set_authorizer(authorize)
        return connection

    def engine_guard(original,engine,*args,**kwargs):
        if engine.url.drivername != 'sqlite' or engine.url.database != ':memory:': blocked('non_memory_database')
        return original(engine,*args,**kwargs)

    with ExitStack() as stack:
        for owner,name,value in [(dotenv,'load_dotenv',lambda *a,**k:False),(dotenv.main,'load_dotenv',lambda *a,**k:False),
            (pymysql,'connect',lambda *a,**k:blocked('non_memory_database')),
            (sqlite3,'connect',connect),(sqlite3.dbapi2,'connect',connect),
            (Engine,'connect',lambda engine,*a,**k:engine_guard(engine_connect,engine,*a,**k)),
            (Engine,'raw_connection',lambda engine,*a,**k:engine_guard(engine_raw,engine,*a,**k)),
            (MigrationContext,'run_migrations',lambda *a,**k:blocked('migration')),
            (Operations,'invoke',lambda *a,**k:blocked('migration'))]:
            stack.enter_context(patch.object(owner,name,value))
        for name in ('upgrade','downgrade','stamp','revision','ensure_version'):
            stack.enter_context(patch.object(alembic.command,name,lambda *a,**k:blocked('migration')))
        sys.path[:0]=[str(ROOT/'backend'),str(ROOT)]
        from index import app
        from models import db,User,Category,Story
        from run_local import create_local_app
        from werkzeug.test import Client
        from werkzeug.wrappers import Response
        with app.app_context():
            assert db.engine.url.database == ':memory:' and all(not os.environ[key] for key in AIVEN)
            db.create_all()
            # Le mot de passe de recette ne vient ni du dépôt ni d'une base réelle.
            password = secrets.token_urlsafe(20)+'Aa1!'
            admin=User(username='jury6f2_admin',email='jury6f2-admin@example.invalid',is_admin=True,is_banned=False)
            admin.set_password(password)
            db.session.add_all([admin,Category(id=1,name='Histoires résolues'),Category(id=2,name='Cold Cases')]);db.session.flush()
            db.session.add_all([Story(id=17,slug='recette-6f2',title='Dossier isolé 6F.2',summary='Recette uniquement',content='Contenu fictif isolé.',category_id=1,author_id=admin.id),
                                Story(id=42,slug='recette-coldcase-6f2',title='Cold Case isolé',summary='Recette uniquement',content='Autre dossier fictif.',category_id=2,author_id=admin.id)])
            db.session.commit()
            with db.engine.connect() as connection:
                assert connection.exec_driver_sql('PRAGMA foreign_keys').scalar()==1
                assert all(row[2]=='' for row in connection.exec_driver_sql('PRAGMA database_list'))
                assert not connection.exec_driver_sql('PRAGMA foreign_key_check').all()
            real_application=create_local_app(app.wsgi_app)
            def application(environ,start_response):
                path=environ.get('PATH_INFO','')
                if path.startswith('/api/') or path=='/' or path.lstrip('/') in PUBLIC:
                    return real_application(environ,start_response)
                # Les sources historiques exclues ne sont jamais lues ni servies.
                start_response('403 Forbidden',[('Content-Type','text/plain; charset=utf-8')])
                return [b'Ressource hors du perimetre de recette inspecte.']
            client=Client(application,Response)
            for name in ('inscription.html','connexion.html','dossier.html','admin-dashboard.html','comments.js'):
                assert client.get('/'+name).status_code==200
            assert client.get('/donnees.js').status_code==403
            receipt={'result':'READY','stage':'inspection before any listener','sqlite':':memory:','foreign_keys':True,'database_files':[],
                     'server_started':False,'browser_started':False,'guards':counters,
                     'excluded_script':'donnees.js remains blocked; full page script coverage not claimed',
                     'stop':'Ctrl+C destroys this memory database; no persistence after restart'}
            if any(counters.values()):
                receipt['result']='FAIL'
                (evidence/'isolation.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
                raise RuntimeError('Isolation refusée : '+json.dumps(counters))
            (evidence/'isolation.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
            print(json.dumps(receipt),flush=True)
            print('Preuves : '+str(evidence),flush=True)
            if not args.serve: return
            # Cette branche n'est pas exécutée pendant 6F.2. Pas de CDP/reloader.
            serving=True
            from werkzeug.serving import make_server
            stack.enter_context(patch.object(socket,'getfqdn',return_value='localhost'))
            class QuietHandler(__import__('werkzeug.serving',fromlist=['WSGIRequestHandler']).WSGIRequestHandler):
                def log_request(self,*unused): pass
            print('RECETTE FICTIVE : http://127.0.0.1:5062 — Ctrl+C pour arrêter.',flush=True)
            print('Compte de test : jury6f2_admin ; mot de passe éphémère (ne pas capturer) : '+password,flush=True)
            with make_server('127.0.0.1',5062,application,threaded=False,request_handler=QuietHandler) as server:
                receipt['stage']='authorized listener';receipt['server_started']=True
                (evidence/'isolation.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
                try: server.serve_forever()
                except KeyboardInterrupt: pass


if __name__ == '__main__':
    main()
