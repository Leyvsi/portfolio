"""Seule la candidate 6G.2 est autorisée ici, SQLite synthétique en mémoire."""
import importlib.util
from pathlib import Path
import unittest

from alembic.migration import MigrationContext
from alembic.operations import Operations
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError


class CommentLikesMigrationTests(unittest.TestCase):
    def setUp(self):
        path=Path(__file__).resolve().parents[2]/'migrations/versions/c6g200000001_add_comment_likes.py'
        spec=importlib.util.spec_from_file_location('candidate_comment_likes',path)
        self.migration=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.migration)

    def schema(self, value=0, comment_type=None, user_type=None):
        engine=sa.create_engine('sqlite:///:memory:')
        self.addCleanup(engine.dispose)
        conn=engine.connect();self.addCleanup(conn.close)
        metadata=sa.MetaData()
        users=sa.Table('users',metadata,sa.Column('id',user_type or sa.Integer(),primary_key=True))
        comments=sa.Table('comments',metadata,sa.Column('id',comment_type or sa.Integer(),primary_key=True),sa.Column('likes',sa.Integer(),nullable=True))
        votes=sa.Table('votes',metadata,sa.Column('id',sa.Integer(),primary_key=True))
        metadata.create_all(conn)
        conn.execute(users.insert(),{'id':'u' if user_type is not None else 1})
        conn.execute(comments.insert(),{'id':'c' if comment_type is not None else 1,'likes':value})
        conn.execute(votes.insert(),{'id':99});conn.commit()
        self.assertEqual(conn.exec_driver_sql('PRAGMA foreign_keys').scalar(),1)
        return conn

    def upgrade(self, conn):
        with Operations.context(MigrationContext.configure(conn)):self.migration.upgrade()

    def test_valid_zero_preserves_legacy_column_votes_and_enforces_new_constraints(self):
        conn=self.schema();self.upgrade(conn)
        self.assertEqual(conn.exec_driver_sql('SELECT likes FROM comments').scalar(),0)
        self.assertEqual(conn.exec_driver_sql('SELECT id FROM votes').scalar(),99)
        self.assertEqual(len(sa.inspect(conn).get_foreign_keys('comment_likes')),2)
        self.assertEqual(sa.inspect(conn).get_unique_constraints('comment_likes')[0]['column_names'],['user_id','comment_id'])
        conn.exec_driver_sql("INSERT INTO comment_likes(comment_id,user_id,created_at) VALUES (1,1,'2026-01-01')")
        for parent,user in ((1,1),(999,1),(1,999)):
            with self.assertRaises(IntegrityError):
                with conn.begin_nested():conn.exec_driver_sql("INSERT INTO comment_likes(comment_id,user_id,created_at) VALUES (?,?,'2026-01-01')",(parent,user))
        conn.exec_driver_sql('DELETE FROM comments WHERE id=1')
        self.assertEqual(conn.exec_driver_sql('SELECT count(*) FROM comment_likes').scalar(),0)
        self.assertEqual(conn.exec_driver_sql('SELECT id FROM votes').scalar(),99)

    def test_nonzero_null_negative_or_text_history_stops_before_any_ddl(self):
        for value in (8,-1,None,'incompatible'):
            with self.subTest(value=value):
                conn=self.schema(value);before=sa.inspect(conn).get_table_names()
                with self.assertRaisesRegex(RuntimeError,'historiques'):self.upgrade(conn)
                self.assertEqual(sa.inspect(conn).get_table_names(),before)
                self.assertEqual(conn.exec_driver_sql('SELECT likes FROM comments').scalar(),value)

    def test_noninteger_parent_types_are_refused_before_ddl(self):
        for which in ('comment_type','user_type'):
            with self.subTest(which=which):
                conn=self.schema(**{which:sa.String(20)})
                with self.assertRaisesRegex(RuntimeError,'type de clé'):self.upgrade(conn)
                self.assertFalse(sa.inspect(conn).has_table('comment_likes'))

    def test_existing_table_is_never_overwritten(self):
        conn=self.schema();self.upgrade(conn)
        with self.assertRaisesRegex(RuntimeError,'déjà présente'):self.upgrade(conn)
        self.assertEqual(conn.exec_driver_sql('SELECT likes FROM comments').scalar(),0)

    def test_downgrade_with_individual_rows_is_refused_without_loss(self):
        conn=self.schema();self.upgrade(conn)
        conn.exec_driver_sql("INSERT INTO comment_likes(comment_id,user_id,created_at) VALUES (1,1,'2026-01-01')")
        with Operations.context(MigrationContext.configure(conn)):
            with self.assertRaisesRegex(RuntimeError,'perdus'):self.migration.downgrade()
        self.assertEqual(conn.exec_driver_sql('SELECT count(*) FROM comment_likes').scalar(),1)

    def test_empty_downgrade_preserves_old_schema_and_values(self):
        conn=self.schema();self.upgrade(conn)
        with Operations.context(MigrationContext.configure(conn)):self.migration.downgrade()
        self.assertFalse(sa.inspect(conn).has_table('comment_likes'))
        self.assertEqual(conn.exec_driver_sql('SELECT likes FROM comments').scalar(),0)
        self.assertEqual(conn.exec_driver_sql('SELECT id FROM votes').scalar(),99)
