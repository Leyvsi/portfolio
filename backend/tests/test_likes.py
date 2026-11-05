"""Likes réels via WSGI/SQLite mémoire ; jamais de base du site."""
from datetime import datetime
import unittest
from unittest.mock import patch

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.sql.dml import Delete
import test_reports as base
import test_story_deletion as deletion_suite


class LikesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base.ReportTests.setUpClass.__func__(cls)

    @classmethod
    def tearDownClass(cls):
        base.ReportTests.tearDownClass.__func__(cls)

    authenticate = base.ReportTests.authenticate
    archive = deletion_suite.StoryDeletionTests.archive
    preview = deletion_suite.StoryDeletionTests.preview
    confirmation = deletion_suite.StoryDeletionTests.confirmation
    prepare = deletion_suite.StoryDeletionTests.prepare
    delete = deletion_suite.StoryDeletionTests.delete
    snapshot = deletion_suite.StoryDeletionTests.snapshot

    def setUp(self):
        base.ReportTests.setUp(self)
        for table in reversed(self.db.metadata.sorted_tables):
            self.db.session.execute(table.delete())
        m = self.models
        self.db.session.add_all([
            m.User(id=1, username='reader', email='reader@example.invalid', password_hash='unused'),
            m.User(id=2, username='banned', email='banned@example.invalid', password_hash='unused', is_banned=True),
            m.User(id=3, username='admin', email='admin@example.invalid', password_hash='unused', is_admin=True),
            m.User(id=4, username='witness', email='witness@example.invalid', password_hash='unused'),
            m.Category(id=1, name='Resolved'), m.Category(id=2, name='Cold cases')])
        self.db.session.flush()
        self.db.session.add_all([m.Story(id=i, slug='likes-'+str(i), title='Fictitious '+str(i),
            summary='Isolated', content='Isolated', category_id=i, author_id=1) for i in (1,2)])
        self.db.session.flush()
        self.db.session.add_all([m.Comment(id=i, story_id=i, user_id=1, username='reader', text='Comment') for i in (1,2)])
        self.db.session.commit()
        self.headers = {'X-CSRF-Token':'reports-csrf'}
        self.assertEqual(self.db.engine.url.database, ':memory:')
        self.assertEqual(self.db.session.execute(sa.text('PRAGMA foreign_keys')).scalar(), 1)

    def tearDown(self):
        self.db.session.rollback(); self.db.session.remove()

    def call(self, kind, method='GET', *, user=1, target=1, csrf='reports-csrf', **kwargs):
        self.client = self.app.test_client()
        if user is not None: self.authenticate(user)
        path = '/api/v1/votes/'+str(target) if kind=='story' else '/api/v1/comments/'+str(target)+'/like'
        return self.client.open(path, method=method, headers={} if csrf is None else {'X-CSRF-Token':csrf}, **kwargs)

    def add(self, kind, **kwargs):
        response=self.call(kind,'POST',**kwargs)
        self.assertEqual(response.status_code,201 if kind=='story' else 200,response.get_data(as_text=True))
        return response

    def test_story_and_comment_add_duplicate_remove_readd_are_real_rows(self):
        for kind in ('story','comment'):
            with self.subTest(kind=kind):
                self.assertFalse(self.call(kind).get_json()['liked_by_me'])
                self.add(kind,json={'user_id':4,'likes':999})
                self.assertEqual(self.call(kind,'POST').status_code,409)
                state=self.call(kind).get_json()
                self.assertEqual((state['likes'],state['liked_by_me']),(1,True))
                self.assertEqual(self.call(kind,user=4).get_json()['likes'],1)
                self.assertFalse(self.call(kind,user=4).get_json()['liked_by_me'])
                deleted=self.call(kind,'DELETE').get_json()
                self.assertEqual((deleted['likes'],deleted['liked_by_me'],deleted['changed']),(0,False,True))
                self.assertFalse(self.call(kind,'DELETE').get_json()['changed'])
                self.add(kind)
        self.assertEqual(self.models.Vote.query.count(),1)
        self.assertEqual(self.models.CommentLike.query.count(),1)
        self.assertEqual(self.db.session.get(self.models.Comment,1).likes,0)

    def test_two_users_and_two_targets_remain_independent(self):
        for kind in ('story','comment'):
            self.add(kind);self.add(kind,user=4);self.add(kind,target=2,user=4)
            self.call(kind,'DELETE')
            self.assertEqual(self.call(kind).get_json()['likes'],1)
            self.assertTrue(self.call(kind,user=4).get_json()['liked_by_me'])
            self.assertTrue(self.call(kind,target=2,user=4).get_json()['liked_by_me'])

    def test_historical_votes_ids_authors_and_dates_are_not_reinterpreted(self):
        old=self.models.Vote(id=99,user_id=4,story_id=2,created_at=datetime(2020,1,2))
        self.db.session.add(old);self.db.session.commit()
        before=self.snapshot()['votes']
        self.assertTrue(self.call('story',target=2,user=4).get_json()['liked_by_me'])
        self.add('story');self.call('story','DELETE')
        self.assertEqual(self.snapshot()['votes'],before)

    def test_anonymous_banned_missing_and_bad_identifiers_cannot_write(self):
        for kind in ('story','comment'):
            for method in ('GET','POST','DELETE'):
                for user,status in ((None,401),(2,403),(999,401)):
                    with self.subTest(kind=kind,method=method,user=user):
                        self.assertEqual(self.call(kind,method,user=user).status_code,status)
                for target in (0,999,2147483648):
                    self.assertEqual(self.call(kind,method,target=target).status_code,404)
        self.assertEqual(self.models.Vote.query.count()+self.models.CommentLike.query.count(),0)

    def test_csrf_for_post_and_delete_and_personal_cache(self):
        for kind in ('story','comment'):
            for method in ('POST','DELETE'):
                for token in (None,'','false','é'):
                    self.assertEqual(self.call(kind,method,csrf=token).status_code,403)
            self.assertEqual(self.call(kind,csrf=None).headers['Cache-Control'],'private, no-store')

    def test_logout_prevents_later_action(self):
        self.add('story')
        self.assertEqual(self.client.post('/api/v1/logout',headers=self.headers).status_code,200)
        self.assertEqual(self.client.delete('/api/v1/votes/1',headers=self.headers).status_code,401)
        self.assertEqual(self.models.Vote.query.count(),1)

    def test_legacy_positive_or_invalid_counter_is_preserved_and_blocks_actions(self):
        for value in (7,-1):
            comment=self.db.session.get(self.models.Comment,1)
            comment.likes=value;self.db.session.commit()
            before=self.snapshot()
            for method in ('GET','POST','DELETE'):
                response=self.call('comment',method)
                self.assertEqual(response.status_code,409)
                self.assertEqual(response.get_json()['code'],'LEGACY_LIKES_UNRESOLVED')
            public=self.client.get('/api/v1/stories/1/comments').get_json()[0]
            self.assertEqual(public['likes'],value);self.assertFalse(public['likes_compatible'])
            self.assertEqual(self.snapshot(),before)

    def test_public_comment_count_comes_from_individual_rows(self):
        self.add('comment');self.add('comment',user=4)
        self.client=self.app.test_client()
        payload=self.client.get('/api/v1/stories/1/comments').get_json()[0]
        self.assertEqual(payload['likes'],2);self.assertTrue(payload['likes_compatible'])
        self.assertNotIn('liked_by_me',payload)

    def test_real_flush_then_error_rolls_back_add_and_remove_completely(self):
        for kind in ('story','comment'):
            for method in ('POST','DELETE'):
                if method=='DELETE':self.add(kind)
                before=self.snapshot()
                with patch.object(self.db.session,'commit',side_effect=SQLAlchemyError('private-error')):
                    response=self.call(kind,method)
                self.assertEqual(response.status_code,500)
                self.assertNotIn('private-error',response.get_data(as_text=True))
                self.assertEqual(self.snapshot(),before)

    def test_unique_and_both_foreign_keys_are_enforced_by_sql(self):
        self.add('comment')
        for comment_id,user_id in ((1,1),(999,1),(1,999)):
            with self.assertRaises(IntegrityError):
                with self.db.session.begin_nested():
                    self.db.session.add(self.models.CommentLike(comment_id=comment_id,user_id=user_id))
                    self.db.session.flush()
        self.assertEqual(self.models.CommentLike.query.count(),1)
        self.assertEqual(self.db.session.execute(sa.text('PRAGMA foreign_key_check')).all(),[])

    def test_comment_delete_cascades_likes_without_touching_other_dossier(self):
        self.add('comment');self.add('comment',target=2,user=4)
        self.db.session.execute(sa.delete(self.models.Comment).where(self.models.Comment.id==1));self.db.session.commit()
        self.assertEqual(self.models.CommentLike.query.count(),1)
        self.assertEqual(self.call('comment','POST').status_code,404)
        self.assertEqual(self.call('comment','DELETE').status_code,404)
        self.assertEqual(self.models.User.query.count(),4)

    def test_database_author_cascade_removes_only_their_individual_likes(self):
        self.add('comment');self.add('comment',user=4,target=2)
        self.db.session.execute(sa.delete(self.models.User).where(self.models.User.id==4))
        self.db.session.commit()
        self.assertEqual(self.models.CommentLike.query.one().user_id,1)
        self.assertEqual(self.models.Comment.query.count(),2)
        self.assertEqual(self.models.Story.query.count(),2)

    def test_internal_comment_likes_count_towards_purge_volume_limit(self):
        self.add('comment');self.authenticate(3);self.archive()
        import api.v1.views.story_deletion_support as service
        before=self.snapshot()
        with patch.object(service,'MAX_DEPENDENCIES',1):
            self.assertEqual(self.preview().status_code,409)
        self.assertEqual(self.snapshot(),before)

    def test_archive_restore_preserves_story_and_comment_likes(self):
        self.add('story');self.add('comment')
        self.authenticate(3);self.archive()
        for kind in ('story','comment'):
            for method in ('GET','POST','DELETE'):
                self.assertEqual(self.call(kind,method).status_code,404)
        self.authenticate(3)
        self.assertEqual(self.client.post('/api/v1/admin/stories/1/restore',headers=self.headers).status_code,200)
        for kind in ('story','comment'):self.assertTrue(self.call(kind).get_json()['liked_by_me'])

    def test_purge_deletes_internal_likes_and_preserves_five_public_keys(self):
        self.add('comment');self.add('comment',target=2,user=4)
        self.authenticate(3)
        headers=self.prepare()
        preview=self.preview().get_json()
        self.assertEqual(set(preview['impact']),{'comments','theories','votes','updates','reports'})
        response=self.delete(headers=headers)
        self.assertEqual(response.status_code,200,response.get_data(as_text=True))
        self.assertEqual(set(response.get_json()['deleted_counts']),set(preview['impact']))
        self.assertEqual(self.models.CommentLike.query.one().comment_id,2)
        self.assertEqual(self.models.User.query.count(),4)

    def test_like_change_invalidates_old_purge_confirmation(self):
        self.add('comment');self.authenticate(3);self.archive()
        preview=self.preview().get_json()
        self.models.CommentLike.query.update({'user_id':4});self.db.session.commit()
        self.assertEqual(self.confirmation(preview).status_code,412)

    def test_purge_error_after_real_like_delete_rolls_everything_back(self):
        self.add('comment');self.authenticate(3)
        headers=self.prepare();before=self.snapshot();original=self.db.session.execute
        def execute(statement,*args,**kwargs):
            if isinstance(statement,Delete) and statement.table.name=='comments':
                self.assertEqual(self.models.CommentLike.query.count(),0)
                raise SQLAlchemyError('after-real-like-delete')
            return original(statement,*args,**kwargs)
        with patch.object(self.db.session,'execute',side_effect=execute):response=self.delete(headers=headers)
        self.assertEqual(response.status_code,500)
        self.assertEqual(self.snapshot(),before)

    def test_commit_can_succeed_before_response_is_lost(self):
        original=self.db.session.commit
        for kind in ('story','comment'):
            for method in ('POST','DELETE'):
                def commit_then_fail():
                    original();raise SQLAlchemyError('lost-ack')
                with patch.object(self.db.session,'commit',side_effect=commit_then_fail):
                    self.assertEqual(self.call(kind,method).status_code,500)
                self.assertEqual(self.call(kind).get_json()['liked_by_me'],method=='POST')
