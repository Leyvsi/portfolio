"""Reprise contrôlée de données historiques fictives, FK SQLite toujours ON."""
import importlib.util
from pathlib import Path
import unittest

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from alembic.migration import MigrationContext
from alembic.operations import Operations


class ReportMigrationTests(unittest.TestCase):
    def setUp(self):
        self.engine = sa.create_engine('sqlite:///:memory:')
        self.addCleanup(self.engine.dispose)
        self.connection = self.engine.connect()
        self.addCleanup(self.connection.close)
        self.connection.exec_driver_sql('PRAGMA foreign_keys=ON')
        self.assertEqual(self.connection.exec_driver_sql('PRAGMA foreign_keys').scalar(), 1)
        self.connection.exec_driver_sql('CREATE TABLE stories (id INTEGER PRIMARY KEY, title TEXT NOT NULL, archived_at DATETIME)')
        self.connection.exec_driver_sql('CREATE TABLE comments (id INTEGER PRIMARY KEY, story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE)')
        self.connection.exec_driver_sql('CREATE TABLE reports (id INTEGER PRIMARY KEY, type VARCHAR(100) NOT NULL, target_id VARCHAR(100) NOT NULL, reason TEXT NOT NULL, status VARCHAR(20) NOT NULL, created_at DATETIME NOT NULL)')
        self.connection.exec_driver_sql("INSERT INTO stories VALUES (1, 'Fictitious story', NULL), (2, 'Witness', NULL)")
        self.connection.exec_driver_sql('INSERT INTO comments VALUES (1, 1), (2, 2)')
        self.connection.exec_driver_sql("INSERT INTO reports VALUES (1, 'comment', '1', 'Fictitious reason', 'pending', '2026-10-31 10:00:00')")
        self.connection.commit()
        path = Path(__file__).resolve().parents[2] / 'migrations/versions/c6c200000001_comment_reports_and_story_revision.py'
        spec = importlib.util.spec_from_file_location('report_migration_under_test', path)
        self.migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.migration)

    def upgrade(self):
        with Operations.context(MigrationContext.configure(self.connection)):
            self.migration.upgrade()

    def snapshot(self):
        return {'schema': self.connection.exec_driver_sql("SELECT type,name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY type,name").all(),
                **{name: self.connection.exec_driver_sql('SELECT * FROM '+name+' ORDER BY id').all()
                   for name in ('reports', 'comments', 'stories')}}

    def test_valid_migration_preserves_rows_and_uses_actual_integer_type(self):
        self.upgrade()
        self.connection.commit()
        inspector = sa.inspect(self.connection)
        columns = {c['name']: c for c in inspector.get_columns('reports')}
        self.assertNotIn('type', columns)
        self.assertNotIn('target_id', columns)
        self.assertFalse(columns['comment_id']['nullable'])
        self.assertIsInstance(columns['comment_id']['type'], sa.Integer)
        self.assertEqual(self.connection.exec_driver_sql('SELECT id,comment_id,reason,status,created_at FROM reports').all(),
            [(1, 1, 'Fictitious reason', 'pending', '2026-10-31 10:00:00')])
        revisions = self.connection.exec_driver_sql('SELECT management_revision FROM stories').scalars().all()
        self.assertEqual(len(set(revisions)), 2)
        self.assertTrue(all(len(value) == 32 and value != '0'*32 for value in revisions))
        self.assertEqual(self.connection.exec_driver_sql('PRAGMA foreign_keys').scalar(), 1)
        self.assertEqual(self.connection.exec_driver_sql('PRAGMA foreign_key_check').all(), [])

    def test_legacy_other_fixture_is_refused_before_any_schema_or_data_change(self):
        self.connection.exec_driver_sql("INSERT INTO reports VALUES (2, 'other', '1', 'Historical witness', 'pending', '2026-10-31 10:00:00')")
        self.connection.commit()
        before = self.snapshot()
        with self.assertRaisesRegex(RuntimeError, 'référence de signalement incompatible'):
            self.upgrade()
        # Même avant rollback : aucun DDL ni reprise partielle n'a été émis.
        self.assertEqual(self.snapshot(), before)

    def test_missing_invalid_noncanonical_and_unknown_references_are_not_repaired(self):
        for kind, target in [('comment', '999'), ('comment', '0'), ('comment', '0001'),
                             ('comment', ' 1 '), ('comment', '-1'), ('comment', '\u0661'),
                             ('comment', '2147483648'), ('Comment', '1'), ('story', '1')]:
            with self.subTest(kind=kind, target=target):
                self.connection.exec_driver_sql('UPDATE reports SET type=?, target_id=? WHERE id=1', (kind, target))
                self.connection.commit()
                before = self.snapshot()
                with self.assertRaises(RuntimeError):
                    self.upgrade()
                self.assertEqual(self.snapshot(), before)
                self.connection.rollback()

    def test_database_fk_rejects_missing_target_and_cascades_without_orphans(self):
        self.upgrade()
        self.connection.commit()
        with self.assertRaises(IntegrityError):
            self.connection.exec_driver_sql("INSERT INTO reports (id,comment_id,reason,status,created_at) VALUES (2,999,'Invalid','pending','2026-10-31')")
        self.connection.rollback()
        self.connection.exec_driver_sql('DELETE FROM stories WHERE id=1')
        self.connection.commit()
        self.assertEqual(self.connection.exec_driver_sql('SELECT * FROM reports').all(), [])
        self.assertEqual(self.connection.exec_driver_sql('SELECT id FROM comments').all(), [(2,)])
        self.assertEqual(self.connection.exec_driver_sql('PRAGMA foreign_key_check').all(), [])

    def test_duplicate_reports_survive_and_downgrade_is_not_content_recovery(self):
        self.connection.exec_driver_sql("INSERT INTO reports SELECT 2,type,target_id,reason,status,created_at FROM reports WHERE id=1")
        self.connection.commit()
        self.upgrade()
        self.connection.commit()
        self.assertEqual(self.connection.exec_driver_sql('SELECT comment_id FROM reports ORDER BY id').all(), [(1,), (1,)])
        with Operations.context(MigrationContext.configure(self.connection)):
            self.migration.downgrade()
        self.connection.commit()
        self.assertEqual(self.connection.exec_driver_sql('SELECT type,target_id FROM reports ORDER BY id').all(), [('comment', '1'), ('comment', '1')])
        self.assertEqual(self.connection.exec_driver_sql('PRAGMA foreign_keys').scalar(), 1)

    def test_non_integer_real_target_type_is_refused_before_ddl(self):
        self.connection.exec_driver_sql('DROP TABLE comments')
        self.connection.exec_driver_sql('CREATE TABLE comments (id TEXT PRIMARY KEY, story_id INTEGER NOT NULL REFERENCES stories(id))')
        self.connection.exec_driver_sql("INSERT INTO comments VALUES ('1', 1)")
        self.connection.commit()
        before = self.snapshot()
        with self.assertRaisesRegex(RuntimeError, 'type de clé commentaire incompatible'):
            self.upgrade()
        self.assertEqual(self.snapshot(), before)
