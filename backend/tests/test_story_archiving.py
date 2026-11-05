"""Phase 1 du lot 6C : WSGI et SQLite mémoire, données entièrement fictives."""

from datetime import datetime
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
from alembic.migration import MigrationContext
from alembic.operations import Operations

import test_reports as report_suite


class StoryArchivingTests(unittest.TestCase):
    authenticate = report_suite.ReportTests.authenticate

    @classmethod
    def setUpClass(cls):
        report_suite.ReportTests.setUpClass.__func__(cls)
        with cls.app.app_context():
            # Activer les FK hors transaction, sur l'unique connexion mémoire.
            cls.db.session.remove()
            with cls.db.engine.connect() as connection:
                connection.exec_driver_sql('PRAGMA foreign_keys=ON')
                assert connection.exec_driver_sql('PRAGMA foreign_keys').scalar() == 1
            cls.db.session.add(cls.models.User(id=3, username='archive-admin',
                email='archive@example.invalid', password_hash='unused', is_admin=True))
            cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        report_suite.ReportTests.tearDownClass.__func__(cls)

    def setUp(self):
        report_suite.ReportTests.setUp(self)
        self.authenticate(3)
        m = self.models
        self.db.session.add_all([
            m.Category(id=2, name='Fictitious Cold Cases'),
            m.Theory(id=1, story_id=1, user_id=None, title='Fictitious theory', content='Evidence', likes=4),
            m.Vote(id=1, story_id=1, user_id=1),
            m.ColdCaseUpdate(id=1, story_id=1, content='Fictitious update'),
            m.Report(id=1, type='comment', target_id='1', reason='Fictitious reason'),
            m.Report(id=2, type='comment', target_id='1', reason='Second reason'),
            m.Proposal(id=1, user_id=1, title='Independent', content='Independent', status='pending'),
        ])
        self.db.session.flush()
        self.db.session.add(m.Story(id=2, slug='cold-case-witness', title='Witness',
            summary='Other', content='Other', category_id=2, author_id=1))
        self.db.session.flush()
        self.db.session.add(m.Comment(id=2, story_id=2, user_id=1, username='reader', text='Witness comment'))
        self.db.session.flush()
        # L'ancien type other est maintenant couvert comme reprise refusée
        # dans test_report_migration. Le témoin reste un vrai autre dossier.
        self.db.session.add(m.Report(id=3, comment_id=2, reason='Unrelated'))
        self.db.session.commit()
        self.before = self.snapshot()

    def tearDown(self):
        self.db.session.rollback()
        for model in (self.models.Report, self.models.Vote, self.models.Theory,
                      self.models.ColdCaseUpdate, self.models.Proposal):
            model.query.delete()
        self.models.Comment.query.filter_by(id=2).delete()
        self.models.Story.query.filter_by(id=2).delete()
        self.models.Category.query.filter_by(id=2).delete()
        self.models.Story.query.update({self.models.Story.archived_at: None})
        self.db.session.commit()
        self.db.session.remove()

    def snapshot(self):
        self.db.session.remove()
        self.assertEqual(self.db.session.execute(sa.text('PRAGMA foreign_keys')).scalar(), 1)
        self.assertEqual(self.db.session.execute(sa.text('PRAGMA foreign_key_check')).all(), [])
        return {table.name: [dict(row) for row in self.db.session.execute(
            table.select().order_by(table.c.id)).mappings()] for table in self.db.metadata.sorted_tables}

    def post(self, action='archive', identifier=1, **kwargs):
        kwargs.setdefault('headers', {'X-CSRF-Token': 'reports-csrf'})
        return self.client.post(f'/api/v1/admin/stories/{identifier}/{action}', **kwargs)

    def test_admin_archive_and_idempotence(self):
        with patch.object(self.db.session, 'commit', wraps=self.db.session.commit) as commit:
            response = self.post()
            self.assertEqual(response.status_code, 200)
            commit.assert_called_once_with()
        data = response.get_json()
        self.assertTrue(data['changed'])
        self.assertTrue(data['story']['is_archived'])
        self.assertIsNotNone(data['story']['archived_at'])
        self.assertEqual(response.headers['Cache-Control'], 'no-store')
        repeated = self.post().get_json()
        self.assertFalse(repeated['changed'])
        self.assertEqual(repeated['story']['archived_at'], data['story']['archived_at'])

    def test_reader_banned_and_forged_session_role_denied(self):
        for user in (1, 2):
            for action in ('archive', 'restore'):
                self.authenticate(user)
                with self.client.session_transaction() as session:
                    session['is_admin'] = True
                self.assertEqual(self.post(action).status_code, 403)
        self.assertEqual(self.snapshot(), self.before)

    def test_anonymous_and_missing_user_denied(self):
        for user in (None, 999):
            self.client = self.app.test_client()
            if user:
                self.authenticate(user)
            for action in ('archive', 'restore'):
                self.assertEqual(self.post(action).status_code, 401)
        self.assertEqual(self.snapshot(), self.before)

    def test_missing_invalid_empty_and_unicode_csrf(self):
        for action in ('archive', 'restore'):
            for token in (None, '', 'incorrect', 'é'):
                headers = {} if token is None else {'X-CSRF-Token': token}
                self.assertEqual(self.post(action, headers=headers).status_code, 403)
        self.assertEqual(self.snapshot(), self.before)

    def test_invalid_and_missing_identifiers_are_json_404(self):
        for action in ('archive', 'restore'):
            for identifier in (0, -1, 999, 2147483648, '9' * 80, 'abc', '1.0'):
                response = self.post(action, identifier)
                self.assertEqual(response.status_code, 404)
                self.assertTrue(response.is_json)
        self.assertEqual(self.snapshot(), self.before)

    def test_archive_preserves_every_child_and_unrelated_table(self):
        self.post()
        after = self.snapshot()
        for name in self.before:
            if name != 'stories':
                self.assertEqual(after[name], self.before[name], name)
        self.assertEqual(after['stories'][1], self.before['stories'][1])
        for key in self.before['stories'][0]:
            if key not in ('archived_at', 'updated_at', 'management_revision'):
                self.assertEqual(after['stories'][0][key], self.before['stories'][0][key])

    def test_public_list_and_slug_hide_archive_even_for_admin(self):
        self.post()
        for user in (None, 1, 3):
            self.client = self.app.test_client()
            if user:
                self.authenticate(user)
            self.assertEqual([row['id'] for row in self.client.get('/api/v1/stories').get_json()], [2])
            self.assertEqual(self.client.get('/api/v1/stories/slug/audit-story').status_code, 404)

    def test_every_public_child_read_is_404(self):
        self.post()
        for route in ('stories/1/theories', 'stories/1/comments', 'coldcases/1/updates'):
            response = self.client.get('/api/v1/' + route)
            self.assertEqual(response.status_code, 404, route)
            self.assertNotIn('Evidence', response.get_data(as_text=True))

    def test_all_seven_contribution_entry_points_are_blocked(self):
        self.post()
        before = self.snapshot()
        self.authenticate(1)
        routes = {
            'stories/1/theories': {'title': 'Forbidden', 'content': 'Forbidden'},
            'stories/1/comments': {'text': 'Forbidden'}, 'votes/1': {},
            'theories/1/like': {}, 'comments/1/like': {},
            'comments/1/report': {'reason': 'Forbidden'},
            'reports': {'type': 'comment', 'target_id': '0001', 'reason': 'Forbidden'},
        }
        for route, payload in routes.items():
            response = self.client.post('/api/v1/' + route, json=payload,
                headers={'X-CSRF-Token': 'reports-csrf'})
            self.assertEqual(response.status_code, 404, route)
        self.assertEqual(self.snapshot(), before)

    def test_admin_archive_list_filters_and_detail_keep_content(self):
        self.post()
        self.assertEqual([row['id'] for row in self.client.get('/api/v1/admin/stories').get_json()], [2])
        rows = self.client.get('/api/v1/admin/stories?state=archived').get_json()
        self.assertEqual([row['id'] for row in rows], [1])
        self.assertEqual(len(self.client.get('/api/v1/admin/stories?state=all').get_json()), 2)
        self.assertEqual(self.client.get('/api/v1/admin/stories?state=unknown').status_code, 400)
        data = self.client.get('/api/v1/admin/stories/1').get_json()
        self.assertEqual(data['comments'][0]['text'], 'Comment')
        self.assertEqual(data['comments'][0]['reports'], 2)
        self.assertEqual(data['theories'][0]['content'], 'Evidence')
        self.assertEqual(data['updates'][0]['content'], 'Fictitious update')
        self.assertEqual(data['votes'], 1)
        self.assertEqual(len(self.client.get('/api/v1/admin/reports').get_json()), 3)

    def test_archive_reads_are_private_and_missing_detail_is_404(self):
        for user, expected in ((None, 401), (1, 403), (2, 403)):
            self.client = self.app.test_client()
            for route in ('admin/stories?state=archived', 'admin/stories/1'):
                # Un refus de compte banni vide la session : recréer la session
                # fictive pour vérifier séparément les deux points d'entrée.
                if user:
                    self.authenticate(user)
                self.assertEqual(self.client.get('/api/v1/' + route).status_code, expected)
        self.authenticate(3)
        for identifier in (0, 999, 2147483648):
            self.assertEqual(self.client.get(f'/api/v1/admin/stories/{identifier}').status_code, 404)

    def test_restore_republishes_same_slug_children_and_vote_uniqueness(self):
        self.post()
        self.assertTrue(self.post('restore').get_json()['changed'])
        self.assertFalse(self.post('restore').get_json()['changed'])
        self.assertIsNone(self.db.session.get(self.models.Story, 1).archived_at)
        self.assertEqual(len(self.client.get('/api/v1/stories').get_json()), 2)
        self.assertEqual(self.client.get('/api/v1/stories/slug/audit-story').status_code, 200)
        for route in ('stories/1/comments', 'stories/1/theories', 'coldcases/1/updates'):
            self.assertEqual(len(self.client.get('/api/v1/' + route).get_json()), 1)
        self.authenticate(1)
        self.assertEqual(self.client.post('/api/v1/votes/1', headers={'X-CSRF-Token': 'reports-csrf'}).status_code, 409)
        self.assertEqual(self.client.post('/api/v1/stories/1/comments', json={'text': 'Allowed'},
            headers={'X-CSRF-Token': 'reports-csrf'}).status_code, 201)
        # Nettoyer seulement le contenu fictif créé dans ce scénario.
        self.models.Comment.query.filter(self.models.Comment.id > 2).delete()
        self.db.session.commit()

    def test_active_counts_exclude_each_category_and_global_counts_do_not_change(self):
        stats = self.client.get('/api/v1/stats').get_json()
        for identifier in (1, 2):
            self.post(identifier=identifier)
            rows = self.client.get('/api/v1/stories').get_json()
            self.assertEqual(len(rows), 1)
            self.assertNotIn(identifier, [row['category_id'] for row in rows])
            self.assertEqual(self.client.get('/api/v1/stats').get_json(), stats)
            self.assertEqual(self.models.Proposal.query.filter_by(status='pending').count(), 1)
            self.post('restore', identifier)

    def test_sql_failure_after_real_flush_rolls_back_archive_and_restore(self):
        for action in ('archive', 'restore'):
            if action == 'restore':
                self.post()
            before = self.snapshot()
            def fail_after_flush():
                self.db.session.flush()
                # Le changement est réellement visible dans la transaction.
                current = self.db.session.execute(sa.select(self.models.Story.archived_at).where(
                    self.models.Story.id == 1)).scalar()
                self.assertEqual(current is not None, action == 'archive')
                raise SQLAlchemyError('fictitious-secret-sql-detail')
            with patch.object(self.db.session, 'commit', side_effect=fail_after_flush):
                response = self.post(action)
            self.assertEqual(response.status_code, 500)
            self.assertTrue(response.is_json)
            self.assertNotIn('fictitious-secret', response.get_data(as_text=True))
            self.assertEqual(self.snapshot(), before)
            self.assertEqual(self.post(action).status_code, 200)

    def test_select_failure_is_explicit_json_error(self):
        from sqlalchemy.orm import Query
        for route, method in (('/admin/stories', 'GET'), ('/admin/stories/1/archive', 'POST')):
            with patch.object(Query, 'all' if method == 'GET' else 'first',
                              side_effect=SQLAlchemyError('private-detail')):
                response = self.client.open('/api/v1' + route, method=method,
                    headers={'X-CSRF-Token': 'reports-csrf'})
            self.assertEqual(response.status_code, 500)
            self.assertNotIn('private-detail', response.get_data(as_text=True))
        self.assertEqual(self.snapshot(), self.before)

    def test_separate_admin_clients_repeat_and_reverse_without_content_loss(self):
        second = self.app.test_client()
        with second.session_transaction() as session:
            session.update(user_id=3, csrf_token='reports-csrf')
        self.assertTrue(self.post().get_json()['changed'])
        self.assertFalse(second.post('/api/v1/admin/stories/1/archive',
            headers={'X-CSRF-Token': 'reports-csrf'}).get_json()['changed'])
        self.assertTrue(second.post('/api/v1/admin/stories/1/restore',
            headers={'X-CSRF-Token': 'reports-csrf'}).get_json()['changed'])
        self.assertFalse(self.post('restore').get_json()['changed'])
        after = self.snapshot()
        for name in self.before:
            if name != 'stories':
                self.assertEqual(after[name], self.before[name])

    def test_no_unconfirmed_story_delete(self):
        self.assertEqual(self.client.delete('/api/v1/admin/stories/1',
            headers={'X-CSRF-Token': 'reports-csrf'}).status_code, 428)
        for suffix in ('/admin/stories/1/archive', '/admin/stories/1/restore'):
            self.assertEqual(self.client.delete('/api/v1' + suffix,
                headers={'X-CSRF-Token': 'reports-csrf'}).status_code, 405)

    def test_role_read_sql_failure_rolls_back_and_returns_private_json(self):
        with patch.object(self.db.session, 'get', side_effect=SQLAlchemyError('private-role-sql')):
            for route, method in (('/admin/stories', 'GET'), ('/admin/stories/1', 'GET'),
                                  ('/admin/stories/1/archive', 'POST'), ('/admin/stories/1/restore', 'POST')):
                response = self.client.open('/api/v1' + route, method=method,
                    headers={'X-CSRF-Token': 'reports-csrf'})
                self.assertEqual(response.status_code, 500)
                self.assertTrue(response.is_json)
                self.assertNotIn('private-role-sql', response.get_data(as_text=True))
        self.assertEqual(self.snapshot(), self.before)

    def test_prepared_migration_on_fictitious_memory_schema_only(self):
        # Importer cette seule migration n'importe ni env.py ni la configuration
        # applicative. Cette preuve ne prétend pas rejouer la chaîne historique.
        path = Path(__file__).resolve().parents[2] / 'migrations/versions/c6c100000001_add_story_archive_date.py'
        spec = importlib.util.spec_from_file_location('archive_migration_test', path)
        migration = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration)
        engine = sa.create_engine('sqlite:///:memory:')
        with engine.begin() as connection:
            connection.exec_driver_sql('PRAGMA foreign_keys=ON')
            connection.exec_driver_sql('CREATE TABLE stories (id INTEGER PRIMARY KEY, title TEXT NOT NULL)')
            connection.exec_driver_sql("INSERT INTO stories VALUES (1, 'Fictitious legacy story')")
            connection.exec_driver_sql('CREATE TABLE children (id INTEGER PRIMARY KEY, story_id INTEGER REFERENCES stories(id))')
            connection.exec_driver_sql('INSERT INTO children VALUES (1, 1)')
            with Operations.context(MigrationContext.configure(connection)):
                migration.upgrade()
            self.assertEqual(connection.exec_driver_sql('SELECT id, title, archived_at FROM stories').one(),
                (1, 'Fictitious legacy story', None))
            self.assertEqual(connection.exec_driver_sql('SELECT * FROM children').all(), [(1, 1)])
            self.assertEqual(connection.exec_driver_sql('PRAGMA foreign_key_check').all(), [])
        engine.dispose()
