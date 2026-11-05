"""Chaîne Alembic réelle et conservation relationnelle, uniquement SQLite mémoire."""
from pathlib import Path
from types import SimpleNamespace
import importlib.util
import io
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from flask import Flask
from migrations.sqlite_safety import sqlite_migration_scope


def guard(event, args):
    if event == 'sqlite3.connect' and args[0] != ':memory:':
        raise PermissionError('Seule SQLite mémoire est autorisée.')
    if event.startswith('socket.') or event in {'subprocess.Popen', 'os.system'}:
        raise PermissionError('Réseau et sous-processus interdits.')


REVISIONS = ['921687c1bd7c', '3111f5767fc6', 'a590c8aac613', '82deda84bc35',
             'c6c100000001', 'c6c200000001', 'c6g200000001']


class MigrationChainTests(unittest.TestCase):
    def setUp(self):
        self.engine = sa.create_engine('sqlite:///:memory:')
        self.addCleanup(self.engine.dispose)
        self.app = Flask('migration_fixture')
        self.app.extensions['migrate'] = SimpleNamespace(
            db=SimpleNamespace(engine=self.engine, metadata=sa.MetaData()), configure_args={})
        self.config = Config(str(ROOT / 'migrations/alembic.ini'), stdout=io.StringIO())
        self.config.set_main_option('script_location', str(ROOT / 'migrations'))

    def upgrade(self, revision):
        # Utilise env.py et alembic_version : aucun remplacement d'opérations.
        with self.app.app_context():
            command.upgrade(self.config, revision)
        with self.engine.connect() as c:
            self.assertEqual(c.exec_driver_sql('PRAGMA foreign_keys').scalar(), 1)
            self.assertEqual(c.exec_driver_sql('PRAGMA foreign_key_check').all(), [])
            self.assertEqual(c.exec_driver_sql('SELECT version_num FROM alembic_version').scalar(), revision)

    def seed_baseline(self):
        with self.engine.begin() as c:
            c.exec_driver_sql("INSERT INTO users VALUES (1,'auteur-fictif','auteur@example.test','synthetique',0,'2026-01-01'),(2,'membre-fictif','membre@example.test','synthetique',0,'2026-01-01')")
            c.exec_driver_sql("INSERT INTO categories VALUES (1,'fictive','fixture')")
            c.exec_driver_sql("INSERT INTO stories VALUES (1,'fixture','Titre','Résumé','Texte',NULL,1,1,'2026-01-01','2026-01-01')")
            c.exec_driver_sql("INSERT INTO comments VALUES (1,1,2,'membre-fictif','Commentaire témoin',0,0,'2026-01-01')")
            c.exec_driver_sql("INSERT INTO theories VALUES (1,1,2,'Théorie','Texte témoin',0,'2026-01-01')")
            c.exec_driver_sql("INSERT INTO votes VALUES (1,1,2,'2026-01-01')")
            c.exec_driver_sql("INSERT INTO proposals VALUES (1,2,'Proposition','Contenu','pending','2026-01-01','2026-01-01')")

    def test_seven_revisions_empty_database(self):
        for revision in REVISIONS:
            self.upgrade(revision)

    def test_seven_revisions_populated_database_and_relations(self):
        self.upgrade(REVISIONS[0])
        self.seed_baseline()
        for revision in REVISIONS[1:]:
            self.upgrade(revision)
            if revision == 'a590c8aac613':
                with self.engine.begin() as c:
                    self.assertEqual(c.exec_driver_sql('SELECT is_banned FROM users ORDER BY id').scalars().all(), [0, 0])
                    column = next(x for x in sa.inspect(c).get_columns('users') if x['name'] == 'is_banned')
                    self.assertIsNone(column['default'])
                    c.exec_driver_sql("INSERT INTO reports VALUES (1,'comment','1','Motif fictif','pending','2026-01-01')")
                    c.exec_driver_sql("INSERT INTO cold_case_updates VALUES (1,1,'Mise à jour fictive','2026-01-01')")
            with self.engine.connect() as c:
                for table, count in [('users', 2), ('categories', 1), ('stories', 1), ('comments', 1), ('theories', 1), ('votes', 1), ('proposals', 1)]:
                    self.assertEqual(c.exec_driver_sql('SELECT COUNT(*) FROM ' + table).scalar(), count, (revision, table))
                self.assertEqual(c.exec_driver_sql('SELECT text FROM comments WHERE id=1').scalar(), 'Commentaire témoin')
        with self.engine.begin() as c:
            self.assertEqual(c.exec_driver_sql('SELECT comment_id FROM reports').scalar(), 1)
            self.assertRegex(c.exec_driver_sql('SELECT management_revision FROM stories').scalar(), r'^[a-f0-9]{32}$')
            fks = [fk for table in sa.inspect(c).get_table_names() for fk in sa.inspect(c).get_foreign_keys(table)]
            self.assertEqual(len(fks), 13)
            c.exec_driver_sql("INSERT INTO comment_likes (id,comment_id,user_id,created_at) VALUES (1,1,2,'2026-01-01')")
            c.exec_driver_sql('DELETE FROM users WHERE id=2')
            self.assertIsNone(c.exec_driver_sql('SELECT user_id FROM comments').scalar())
            self.assertIsNone(c.exec_driver_sql('SELECT user_id FROM theories').scalar())
            for table in ('votes', 'proposals', 'comment_likes'):
                self.assertEqual(c.exec_driver_sql('SELECT COUNT(*) FROM ' + table).scalar(), 0)
            c.exec_driver_sql('DELETE FROM stories WHERE id=1')
            for table in ('comments', 'theories', 'reports', 'cold_case_updates'):
                self.assertEqual(c.exec_driver_sql('SELECT COUNT(*) FROM ' + table).scalar(), 0)
            self.assertEqual(c.exec_driver_sql('PRAGMA foreign_key_check').all(), [])

    def test_failure_rolls_back_ddl_and_restores_foreign_keys(self):
        with self.engine.connect() as c:
            with self.assertRaisesRegex(RuntimeError, 'échec fictif'):
                with sqlite_migration_scope(c):
                    c.exec_driver_sql('CREATE TABLE jetable(id INTEGER PRIMARY KEY)')
                    raise RuntimeError('échec fictif')
            self.assertEqual(c.exec_driver_sql('PRAGMA foreign_keys').scalar(), 1)
            self.assertNotIn('jetable', sa.inspect(c).get_table_names())

    def test_invalid_final_relations_roll_back(self):
        with self.engine.connect() as c:
            with self.assertRaisesRegex(RuntimeError, 'Intégrité finale'):
                with sqlite_migration_scope(c):
                    c.exec_driver_sql('CREATE TABLE parent(id INTEGER PRIMARY KEY)')
                    c.exec_driver_sql('CREATE TABLE child(id INTEGER REFERENCES parent(id))')
                    c.exec_driver_sql('INSERT INTO child VALUES (999)')
            self.assertNotIn('child', sa.inspect(c).get_table_names())
            self.assertEqual(c.exec_driver_sql('PRAGMA foreign_keys').scalar(), 1)

    def test_active_transaction_is_refused(self):
        with self.engine.begin() as c:
            with self.assertRaisesRegex(RuntimeError, 'sans transaction'):
                with sqlite_migration_scope(c):
                    self.fail('Ne doit pas entrer dans la migration.')

    def test_unsafe_a590_refuses_before_ddl(self):
        path = next((ROOT / 'migrations/versions').glob('a590*.py'))
        spec = importlib.util.spec_from_file_location('migration_refus_fixture', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with self.engine.connect() as c:
            c.exec_driver_sql('PRAGMA foreign_keys=ON')
            with Operations.context(MigrationContext.configure(c)):
                with self.assertRaisesRegex(RuntimeError, 'sqlite_migration_scope'):
                    module.upgrade()
            self.assertEqual(sa.inspect(c).get_table_names(), [])


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    sys.addaudithook(guard)
    unittest.main(verbosity=2)
