"""Purge fictive par WSGI, SQLite mémoire et FK ON ; aucun serveur réel."""
import importlib
import json
import unittest
from unittest.mock import patch

import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy.sql.dml import Delete

import test_reports as report_suite


class StoryDeletionTests(unittest.TestCase):
    authenticate = report_suite.ReportTests.authenticate

    @classmethod
    def setUpClass(cls):
        report_suite.ReportTests.setUpClass.__func__(cls)
        cls.service = importlib.import_module('api.v1.views.story_deletion_support')

    @classmethod
    def tearDownClass(cls):
        report_suite.ReportTests.tearDownClass.__func__(cls)

    def setUp(self):
        report_suite.ReportTests.setUp(self)
        self.db.session.rollback()
        for table in reversed(self.db.metadata.sorted_tables):
            self.db.session.execute(table.delete())
        m = self.models
        self.db.session.add_all([
            m.User(id=1, username='reader', email='reader@example.invalid', password_hash='unused'),
            m.User(id=2, username='banned', email='banned@example.invalid', password_hash='unused', is_banned=True),
            m.User(id=3, username='admin', email='admin@example.invalid', password_hash='unused', is_admin=True),
            m.Category(id=1, name='Resolved'), m.Category(id=2, name='Cold cases'),
        ])
        self.db.session.flush()
        self.db.session.add_all([m.Story(id=i, slug='fiction-'+str(i), title='Fictitious '+str(i),
            summary='Summary', content='Content', category_id=i, author_id=1) for i in (1, 2)])
        self.db.session.flush()
        for i in (1, 2):
            self.db.session.add_all([
                m.Comment(id=i, story_id=i, user_id=1, username='reader', text='Comment '+str(i)),
                m.Theory(id=i, story_id=i, user_id=None, title='Theory', content='Evidence', likes=2),
                m.Vote(id=i, story_id=i, user_id=1),
                m.ColdCaseUpdate(id=i, story_id=i, content='Update'),
            ])
        self.db.session.flush()
        self.db.session.add_all([m.Report(id=1, comment_id=1, reason='Report 1'),
            m.Report(id=2, comment_id=1, reason='Report 2', status='resolved'),
            m.Report(id=3, comment_id=2, reason='Witness'),
            m.Proposal(id=1, user_id=1, title='Independent', content='Independent')])
        self.db.session.commit()
        self.authenticate(3)
        self.headers = {'X-CSRF-Token': 'reports-csrf'}
        self.assertEqual(self.db.session.execute(sa.text('PRAGMA foreign_keys')).scalar(), 1)
        self.before = self.snapshot()

    def tearDown(self):
        self.db.session.rollback()
        self.db.session.remove()

    def snapshot(self):
        self.db.session.remove()
        return {table.name: [dict(row) for row in self.db.session.execute(table.select().order_by(table.c.id)).mappings()]
                for table in self.db.metadata.sorted_tables}

    def archive(self):
        response = self.client.post('/api/v1/admin/stories/1/archive', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def preview(self):
        return self.client.get('/api/v1/admin/stories/1/deletion-preview')

    def confirmation(self, preview=None, **changes):
        data = preview or self.preview().get_json()
        return self.client.post('/api/v1/admin/stories/1/deletion-confirmations', headers=self.headers,
            json={'preview_token': data['preview_token'], 'typed_title': data['story']['title'],
                  'confirm_contributions': True, **changes})

    def prepare(self):
        self.archive()
        preview = self.preview().get_json()
        final = self.confirmation(preview).get_json()
        return {**self.headers, 'If-Match': preview['resource_etag'],
                'X-Deletion-Confirmation': final['confirmation_token']}

    def delete(self, headers=None, identifier=1, **kwargs):
        return self.client.delete('/api/v1/admin/stories/'+str(identifier),
            headers=headers or self.headers, **kwargs)

    def test_complete_graph_deleted_other_dossier_and_accounts_unchanged(self):
        headers = self.prepare()
        response = self.delete(headers)
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body['code'], 'STORY_DELETED')
        self.assertEqual(body['deleted_counts'], {'comments':1, 'theories':1, 'votes':1, 'updates':1, 'reports':2})
        self.assertEqual(response.headers['Cache-Control'], 'no-store')
        after = self.snapshot()
        for name in ('users', 'categories', 'proposals'):
            self.assertEqual(after[name], self.before[name])
        for name in ('stories', 'comments', 'theories', 'votes', 'cold_case_updates'):
            self.assertEqual(after[name], [self.before[name][1]])
        self.assertEqual(after['reports'], [self.before['reports'][2]])
        self.assertEqual(self.db.session.execute(sa.text('PRAGMA foreign_key_check')).all(), [])
        self.assertEqual(len(after), 10)  # La dixième table contient les likes, aucun reçu.
        self.assertIn('comment_likes', after)

    def test_permission_matrix_all_three_operations(self):
        headers = self.prepare()
        for user_id, status in ((None,401), (1,403), (2,403), (999,401)):
            for suffix, method in (('/deletion-preview','GET'),('/deletion-confirmations','POST'),('','DELETE')):
                self.client = self.app.test_client()
                if user_id is not None:
                    self.authenticate(user_id)
                    with self.client.session_transaction() as session:
                        session['is_admin'] = True
                response = self.client.open('/api/v1/admin/stories/1'+suffix, method=method, headers=headers)
                self.assertEqual(response.status_code, status)
        self.assertIsNotNone(self.db.session.get(self.models.Story, 1))

    def test_csrf_missing_invalid_empty_and_unicode_for_confirmation_and_delete(self):
        headers = self.prepare()
        for token in (None, '', 'wrong', 'é'):
            changed = {key:value for key,value in headers.items() if key != 'X-CSRF-Token'}
            if token is not None:
                changed['X-CSRF-Token'] = token
            for suffix, method in (('/deletion-confirmations','POST'),('','DELETE')):
                self.assertEqual(self.client.open('/api/v1/admin/stories/1'+suffix,
                    method=method, headers=changed).status_code, 403)

    def test_active_dossier_cannot_be_prepared_or_deleted(self):
        self.assertEqual(self.preview().status_code, 409)
        headers = self.prepare()
        self.client.post('/api/v1/admin/stories/1/restore', headers=self.headers)
        self.assertEqual(self.delete(headers).status_code, 409)

    def test_missing_invalid_and_huge_ids_are_404_with_valid_preconditions(self):
        headers = self.prepare()
        for identifier in (0, -1, 999, 2147483648, '9'*80, 'abc'):
            self.assertEqual(self.delete(headers, identifier).status_code, 404)

    def test_exact_title_true_boolean_and_strict_json_required(self):
        self.archive()
        preview = self.preview().get_json()
        for changes in ({'typed_title':'wrong'}, {'typed_title':' Fictitious 1 '},
                        {'typed_title':1}, {'confirm_contributions':1}, {'confirm_contributions':False},
                        {'unexpected':True}):
            self.assertEqual(self.confirmation(preview, **changes).status_code, 400)
        raw = json.dumps({'preview_token':preview['preview_token'],'typed_title':'Fictitious 1',
                          'confirm_contributions':True})[:-1]+',"typed_title":"Fictitious 1"}'
        response = self.client.post('/api/v1/admin/stories/1/deletion-confirmations',
            data=raw, content_type='application/json', headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_preview_and_confirmation_have_no_database_effect(self):
        self.archive()
        before = self.snapshot()
        preview = self.preview()
        self.assertEqual(preview.status_code, 200)
        self.assertEqual(preview.get_json()['impact']['reports'], 2)
        self.assertEqual(self.confirmation(preview.get_json()).status_code, 200)
        self.assertEqual(self.snapshot(), before)

    def test_missing_preconditions_weak_wildcard_and_multiple_etags_refused(self):
        headers = self.prepare()
        self.assertEqual(self.delete().status_code, 428)
        without_token = {key:value for key,value in headers.items() if key != 'X-Deletion-Confirmation'}
        self.assertEqual(self.delete(without_token).status_code, 428)
        for etag in ('*', 'W/'+headers['If-Match'], headers['If-Match']+','+headers['If-Match'], 'wrong'):
            self.assertEqual(self.delete({**headers,'If-Match':etag}).status_code, 400)
        self.assertEqual(self.delete({**headers, 'If-Match':'"'+'0'*64+'"'}).status_code, 412)

    def test_wrong_signature_session_and_actor_cannot_reuse_confirmation(self):
        headers = self.prepare()
        self.assertEqual(self.delete({**headers,'X-Deletion-Confirmation':'fake'}).status_code, 403)
        with self.client.session_transaction() as session:
            session['csrf_token'] = 'other-csrf'
        self.assertEqual(self.delete({**headers,'X-CSRF-Token':'other-csrf'}).status_code, 403)

    def test_expiry_of_preview_and_final_token_does_not_extend_on_confirmation(self):
        self.archive()
        preview = self.preview().get_json()
        final = self.confirmation(preview).get_json()
        self.assertEqual(final['expires_at'], preview['expires_at'])
        for token, purpose in ((preview['preview_token'],'preview'), (final['confirmation_token'],'delete')):
            data = self.service.signer().loads(token)
            data['expires'] = 1
            expired = self.service.signer().dumps(data)
            response = self.confirmation(preview, preview_token=expired) if purpose == 'preview' else self.delete({
                **self.headers, 'If-Match':preview['resource_etag'],'X-Deletion-Confirmation':expired})
            self.assertEqual(response.status_code, 412)

    def test_restore_rearchive_invalidates_even_if_time_is_equal(self):
        headers = self.prepare()
        initial = self.db.session.get(self.models.Story, 1)
        before, archived_at, updated_at = initial.management_revision, initial.archived_at, initial.updated_at
        self.client.post('/api/v1/admin/stories/1/restore', headers=self.headers)
        self.archive()
        current = self.db.session.get(self.models.Story, 1)
        current.archived_at, current.updated_at = archived_at, updated_at
        self.db.session.commit()
        self.assertNotEqual(current.management_revision, before)
        self.assertEqual(self.delete(headers).status_code, 412)

    def test_changed_dependency_with_same_count_invalidates_confirmation(self):
        headers = self.prepare()
        self.db.session.get(self.models.Report, 1).reason = 'Changed while preparing'
        self.db.session.commit()
        self.assertEqual(self.delete(headers).status_code, 412)

    def test_repeated_delete_has_one_effect_and_returns_404_without_receipt(self):
        headers = self.prepare()
        self.assertEqual(self.delete(headers).status_code, 200)
        self.assertEqual(self.delete(headers).status_code, 404)
        self.assertEqual(self.client.get('/api/v1/admin/stories/1').status_code, 404)

    def test_reused_numeric_id_does_not_accept_old_confirmation(self):
        headers = self.prepare()
        self.delete(headers)
        self.db.session.add(self.models.Story(id=1, slug='replacement', title='Replacement', summary='New',
            content='New', category_id=1, author_id=1))
        self.db.session.commit()
        self.archive()
        self.assertEqual(self.delete(headers).status_code, 412)
        self.assertEqual(self.db.session.get(self.models.Story, 1).title, 'Replacement')

    def test_failure_after_real_delete_of_reports_or_comments_rolls_back_nine_tables(self):
        for failing_table in ('reports', 'comments'):
            headers = self.prepare()
            before = self.snapshot()
            original = self.db.session.execute
            def execute(statement, *args, **kwargs):
                result = original(statement, *args, **kwargs)
                if isinstance(statement, Delete) and statement.table.name == failing_table:
                    raise SQLAlchemyError('fictitious-private-sql')
                return result
            with patch.object(self.db.session, 'execute', side_effect=execute):
                response = self.delete(headers)
            self.assertEqual(response.status_code, 500)
            self.assertNotIn('fictitious-private', response.get_data(as_text=True))
            self.assertEqual(self.snapshot(), before)

    def test_commit_failure_before_commit_restores_all_rows(self):
        headers = self.prepare()
        before = self.snapshot()
        with patch.object(self.db.session, 'commit', side_effect=SQLAlchemyError('lost-commit')):
            response = self.delete(headers)
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json()['code'], 'DELETE_STATUS_UNKNOWN')
        self.assertEqual(self.snapshot(), before)

    def test_commit_success_with_lost_ack_is_not_falsely_announced_as_rollback(self):
        headers = self.prepare()
        original = self.db.session.commit
        def lost_ack():
            original()
            raise SQLAlchemyError('lost acknowledgement')
        with patch.object(self.db.session, 'commit', side_effect=lost_ack):
            response = self.delete(headers)
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.get_json()['code'], 'DELETE_STATUS_UNKNOWN')
        self.assertEqual(self.client.get('/api/v1/admin/stories/1').status_code, 404)

    def test_volume_guard_refuses_before_deletion(self):
        self.archive()
        before = self.snapshot()
        with patch.object(self.service, 'MAX_DEPENDENCIES', 1):
            response = self.preview()
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.get_json()['code'], 'CASE_TOO_LARGE')
        self.assertEqual(self.snapshot(), before)

    def test_no_receipt_table_or_routes_and_global_stats_correct(self):
        stats = self.client.get('/api/v1/stats').get_json()
        headers = self.prepare()
        self.delete(headers)
        after = self.client.get('/api/v1/stats').get_json()
        self.assertEqual(after, {**stats, 'comments':stats['comments']-1, 'reports':stats['reports']-2})
        self.assertEqual(self.models.Proposal.query.filter_by(status='pending').count(), 1)
        self.assertFalse(any('receipt' in name for name in self.db.metadata.tables))
        self.assertEqual(self.client.get('/api/v1/admin/story-deletions/anything').status_code, 404)

    def test_model_only_comment_reports_and_database_target_required(self):
        with self.assertRaises(ValueError):
            self.models.Report(type='other', target_id='1', reason='Forbidden')
        self.db.session.add(self.models.Report(comment_id=999, reason='Missing'))
        with self.assertRaises(IntegrityError):
            self.db.session.commit()
        self.db.session.rollback()
        self.assertEqual(self.snapshot(), self.before)

    def test_forged_database_sentinel_revision_is_not_purgeable(self):
        self.archive()
        self.db.session.get(self.models.Story, 1).management_revision = '0'*32
        self.db.session.commit()
        self.assertEqual(self.preview().status_code, 409)

    def test_body_on_delete_is_rejected_without_mutation(self):
        headers = self.prepare()
        before = self.snapshot()
        self.assertEqual(self.delete(headers, json={'id':2}).status_code, 400)
        self.assertEqual(self.snapshot(), before)

    def test_empty_graph_can_be_deleted_with_zero_real_counts(self):
        for model in (self.models.Report, self.models.Theory, self.models.Vote, self.models.ColdCaseUpdate, self.models.Comment):
            if model is self.models.Report:
                model.query.filter(model.comment_id == 1).delete()
            else:
                model.query.filter(model.story_id == 1).delete()
        self.db.session.commit()
        response = self.delete(self.prepare())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.get_json()['deleted_counts'].values()), {0})

    def test_two_admin_clients_with_distinct_confirmations_have_one_effect(self):
        headers = self.prepare()
        self.db.session.add(self.models.User(id=4, username='second-admin', email='second@example.invalid',
            password_hash='unused', is_admin=True))
        self.db.session.commit()
        second = self.app.test_client()
        with second.session_transaction() as session:
            session.update(user_id=4, csrf_token='second-csrf')
        preview = second.get('/api/v1/admin/stories/1/deletion-preview').get_json()
        final = second.post('/api/v1/admin/stories/1/deletion-confirmations',
            json={'preview_token':preview['preview_token'], 'typed_title':'Fictitious 1', 'confirm_contributions':True},
            headers={'X-CSRF-Token':'second-csrf'}).get_json()
        self.assertEqual(self.delete(headers).status_code, 200)
        response = second.delete('/api/v1/admin/stories/1', headers={'X-CSRF-Token':'second-csrf',
            'If-Match':preview['resource_etag'], 'X-Deletion-Confirmation':final['confirmation_token']})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.models.Report.query.count(), 1)

    def test_simulated_deadlock_is_503_without_sql_detail_or_mutation(self):
        headers = self.prepare()
        before = self.snapshot()
        # Objet d'erreur simulé seulement : aucune connexion à MySQL.
        with patch.object(self.service, 'snapshot', side_effect=OperationalError(
                'statement', {}, Exception(1213, 'fictitious-private-deadlock'))):
            response = self.delete(headers)
        self.assertEqual(response.status_code, 503)
        self.assertNotIn('fictitious-private', response.get_data(as_text=True))
        self.assertEqual(self.snapshot(), before)
