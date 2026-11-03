"""Contexte de modération : vraies vues, SQLite mémoire et données fictives."""
from datetime import datetime
import unittest
from unittest.mock import patch

import sqlalchemy as sa
from flask_sqlalchemy.query import Query
from sqlalchemy.exc import SQLAlchemyError
import test_reports as base


class AdminReportContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base.ReportTests.setUpClass.__func__(cls)

    @classmethod
    def tearDownClass(cls):
        base.ReportTests.tearDownClass.__func__(cls)

    authenticate = base.ReportTests.authenticate

    def setUp(self):
        base.ReportTests.setUp(self)
        for table in reversed(self.db.metadata.sorted_tables):
            self.db.session.execute(table.delete())
        m = self.models
        self.db.session.add_all([
            m.User(id=1, username='reader', email='reader@example.invalid', password_hash='unused'),
            m.User(id=2, username='banned', email='banned@example.invalid', password_hash='unused', is_banned=True),
            m.User(id=3, username='admin', email='admin@example.invalid', password_hash='unused', is_admin=True),
            m.Category(id=1, name='Catégorie SQL résolue'), m.Category(id=2, name='Catégorie SQL froide')])
        self.db.session.flush()
        self.db.session.add_all([m.Story(id=i, slug='report-'+str(i), title='Dossier SQL '+str(i),
            summary='Fictif', content='Fictif', category_id=1 if i==17 else 2, author_id=1) for i in (17,42)])
        self.db.session.flush()
        self.db.session.add_all([m.Comment(id=7, story_id=17, user_id=1, username='reader', text='Commentaire témoin'),
                                 m.Comment(id=8, story_id=42, user_id=3, username='admin', text='<img src=x onerror=alert(1)>')])
        self.db.session.flush()
        self.db.session.add_all([m.Report(id=1, comment_id=7, reason='Motif A'), m.Report(id=2, comment_id=8, reason='Motif B')])
        self.db.session.commit()
        self.authenticate(3)
        self.assertEqual(self.db.engine.url.database, ':memory:')
        self.assertEqual(self.db.session.execute(sa.text('PRAGMA foreign_keys')).scalar(), 1)

    def tearDown(self):
        self.db.session.rollback()
        self.db.session.remove()

    def get(self):
        return self.client.get('/api/v1/admin/reports')

    def snapshot(self):
        return {table.name:self.db.session.execute(sa.select(table).order_by(table.c.id)).all()
                for table in self.db.metadata.sorted_tables}

    def test_both_contexts_match_real_comment_story_category_without_account_fields(self):
        response=self.get(); self.assertEqual(response.status_code,200)
        self.assertEqual(response.headers['Cache-Control'],'private, no-store')
        rows={row['id']:row for row in response.get_json()}
        for identifier,comment_id,story_id,category_id in ((1,7,17,1),(2,8,42,2)):
            row=rows[identifier]
            self.assertEqual(row['target_id'],str(comment_id))
            self.assertEqual(row['comment'],{'id':comment_id,'story_id':story_id,
                'text':self.db.session.get(self.models.Comment,comment_id).text})
            self.assertEqual(row['story'],{'id':story_id,'slug':'report-'+str(story_id),
                'title':'Dossier SQL '+str(story_id),'category_id':category_id,
                'category_name':self.db.session.get(self.models.Category,category_id).name,'is_archived':False})
            self.assertNotIn('email',row);self.assertNotIn('username',row['comment'])

    def test_archived_story_and_updated_comment_remain_readable_to_admin(self):
        self.db.session.get(self.models.Story,42).archived_at=datetime(2026,11,1)
        self.db.session.get(self.models.Comment,8).text='Texte modifié <script>test</script>'
        self.db.session.commit()
        row=next(row for row in self.get().get_json() if row['id']==2)
        self.assertTrue(row['story']['is_archived'])
        self.assertEqual(row['comment']['text'],'Texte modifié <script>test</script>')
        self.assertEqual(self.client.get('/api/v1/stories/42/comments').status_code,404)

    def test_anonymous_member_and_banned_accounts_cannot_read_context(self):
        for user,status in ((None,401),(1,403),(2,403),(3,200)):
            self.client=self.app.test_client()
            if user is not None:self.authenticate(user)
            response=self.get();self.assertEqual(response.status_code,status)
            if status!=200:
                self.assertNotIn('Commentaire témoin',response.get_data(as_text=True))
                self.assertNotIn('category_name',response.get_data(as_text=True))

    def test_admin_reads_preserve_all_ten_tables_and_public_stats(self):
        before=self.snapshot()
        stats=self.client.get('/api/v1/stats').get_json()
        self.assertEqual(len(self.get().get_json()),2)
        self.assertEqual(self.snapshot(),before)
        self.assertEqual(self.client.get('/api/v1/stats').get_json(),stats)

    def test_comment_deletion_removes_only_its_report_and_preserves_other_context(self):
        self.db.session.execute(sa.delete(self.models.Comment).where(self.models.Comment.id==7))
        self.db.session.commit()
        rows=self.get().get_json()
        self.assertEqual(len(rows),1)
        self.assertEqual((rows[0]['id'],rows[0]['comment']['id'],rows[0]['story']['id']),(2,8,42))
        self.assertEqual(self.db.session.execute(sa.text('PRAGMA foreign_key_check')).all(),[])

    def test_inconsistent_synthetic_reference_is_visible_as_unavailable_never_reassigned(self):
        # Ancienne référence impossible avec FK actives : cas synthétique de
        # diagnostic uniquement, sans exécuter une migration ni réparer la ligne.
        self.db.session.remove()
        with self.db.engine.connect() as connection:
            connection.exec_driver_sql('PRAGMA foreign_keys=OFF')
            connection.exec_driver_sql('UPDATE reports SET comment_id=999 WHERE id=1')
            connection.commit()
            connection.exec_driver_sql('PRAGMA foreign_keys=ON')
            self.assertEqual(connection.exec_driver_sql('PRAGMA foreign_keys').scalar(),1)
        row=next(row for row in self.get().get_json() if row['id']==1)
        self.assertEqual(row['target_id'],'999')
        self.assertIsNone(row['comment']);self.assertIsNone(row['story'])
        self.assertEqual(self.models.Report.query.count(),2)

    def test_sql_failure_returns_generic_500_without_partial_context_or_changes(self):
        before=self.snapshot()
        with patch.object(Query,'all',side_effect=SQLAlchemyError('private-database-detail')):
            response=self.get()
        self.assertEqual(response.status_code,500)
        self.assertNotIn('private-database-detail',response.get_data(as_text=True))
        self.assertEqual(self.snapshot(),before)

    def test_context_loading_does_not_issue_queries_for_each_report(self):
        statements=[]
        def record(connection,cursor,statement,parameters,context,many):
            if statement.lstrip().upper().startswith('SELECT'):statements.append(statement)
        sa.event.listen(self.db.engine,'before_cursor_execute',record)
        try:
            self.assertEqual(self.get().status_code,200)
        finally:
            sa.event.remove(self.db.engine,'before_cursor_execute',record)
        self.assertLessEqual(len(statements),2)  # Compte courant + contexte joint.
