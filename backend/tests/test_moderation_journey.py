"""Parcours API/SQL multi-utilisateur, uniquement sous le harnais isolé 6E.3."""

from datetime import datetime
import json
import os
from pathlib import Path
import unittest

from sqlalchemy.exc import IntegrityError

import test_reports as report_suite


class ModerationJourneyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Le marqueur et le dossier viennent du bootstrap inspecté, jamais du site.
        if os.environ.get("PORTFOLIO_ISOLATED_TESTS") != "6e3-memory-only":
            raise RuntimeError("Utiliser le harnais 6E.3 inspecté avant ce test.")
        cls.evidence = Path(os.environ["PORTFOLIO_TEST_EVIDENCE"])
        report_suite.ReportTests.setUpClass.__func__(cls)
        with cls.app.app_context():
            admin = cls.models.User(
                id=3, username="journey-admin", email="admin-journey@example.invalid",
                is_admin=True, is_banned=False,
            )
            admin.set_password("Fictitious-Admin9!")
            cls.db.session.add(admin)
            cls.db.session.add(cls.models.Category(id=2, name="Isolated Cold Cases"))
            cls.db.session.flush()
            cls.db.session.add_all([
                cls.models.Story(
                    id=2, slug="isolated-cold-case", title="Isolated cold case",
                    summary="Test only", content="Test only", category_id=2, author_id=3,
                ),
                cls.models.Story(
                    id=3, slug="isolated-archive", title="Isolated archive",
                    summary="Test only", content="Test only", category_id=1, author_id=3,
                    archived_at=datetime(2026, 10, 31),
                ),
            ])
            cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        report_suite.ReportTests.tearDownClass.__func__(cls)

    def test_real_api_writes_match_test_database_and_admin_data_sources(self):
        self.steps = []
        with self.app.app_context():
            self.assertEqual(self.db.engine.url.drivername, "sqlite")
            self.assertEqual(self.db.engine.url.database, ":memory:")
            with self.db.engine.connect() as connection:
                self.assertEqual(connection.exec_driver_sql("PRAGMA foreign_keys").scalar(), 1)
                databases = connection.exec_driver_sql("PRAGMA database_list").all()
                self.assertTrue(all(row[2] == "" for row in databases))

            def call(client, method, path, status, *, body=None, csrf=None, label):
                kwargs = {}
                if body is not None:
                    kwargs["json"] = body
                if csrf is not None:
                    kwargs["headers"] = {"X-CSRF-Token": csrf}
                response = client.open(path, method=method, **kwargs)
                # La preuve conserve les étapes et codes, pas les mots de passe/jetons.
                self.steps.append({"step": label, "method": method, "path": path,
                                   "status": response.status_code})
                self.assertEqual(response.status_code, status, label)
                self.assertTrue(response.is_json, label)
                return response.get_json()

            def register_and_login(username):
                client = self.app.test_client()
                created = call(client, "POST", "/api/v1/users", 201, body={
                    "username": username, "email": username + "@example.invalid",
                    "password": "Fictitious-Member9!",
                }, label="registration " + username)
                logged = call(client, "POST", "/api/v1/login", 200, body={
                    "username": username, "password": "Fictitious-Member9!",
                }, label="login " + username)
                self.assertEqual(logged["user"]["id"], created["user"]["id"])
                self.assertFalse(logged["user"]["is_admin"])
                return client, logged["csrf_token"], logged["user"]["id"]

            author, author_csrf, author_id = register_and_login("journey-author")
            reporter, reporter_csrf, reporter_id = register_and_login("journey-reporter")
            call(author, "GET", "/api/v1/me", 200, label="author session")
            comment = call(author, "POST", "/api/v1/stories/1/comments", 201,
                           body={"text": "Commentaire du parcours isolé."},
                           csrf=author_csrf, label="comment creation")["comment"]
            comment_id = comment["id"]
            self.db.session.expire_all()
            row = self.db.session.get(self.models.Comment, comment_id)
            self.assertEqual((row.user_id, row.story_id, row.username),
                             (author_id, 1, "journey-author"))
            comments = call(author, "GET", "/api/v1/stories/1/comments", 200,
                            label="public comment read")
            self.assertTrue(any(item["id"] == comment_id for item in comments))

            report_path = f"/api/v1/comments/{comment_id}/report"
            call(reporter, "POST", report_path, 403, body={"reason": "Test only"},
                 label="report missing CSRF rejected")
            self.assertEqual(self.models.Report.query.count(), 0)
            call(reporter, "POST", "/api/v1/reports", 400,
                 body={"type": "story", "target_id": str(comment_id), "reason": "Test only"},
                 csrf=reporter_csrf, label="forbidden report type rejected")
            self.assertEqual(self.models.Report.query.count(), 0)
            report = call(reporter, "POST", report_path, 201,
                          body={"reason": "Motif du parcours isolé."},
                          csrf=reporter_csrf, label="report creation")["report"]
            self.db.session.expire_all()
            report_row = self.db.session.get(self.models.Report, report["id"])
            self.assertEqual(report_row.comment_id, comment_id)
            self.assertEqual(report_row.reason, report["reason"])
            self.assertEqual((report["type"], report["target_id"]), ("comment", str(comment_id)))
            self.assertEqual(report_row.comment.user_id, author_id)
            comments_after_report = call(author, "GET", "/api/v1/stories/1/comments", 200,
                                         label="comment report count read")
            reported_comment = next(item for item in comments_after_report if item["id"] == comment_id)
            self.assertEqual(reported_comment["reports"],
                             self.models.Report.query.filter_by(comment_id=comment_id).count())

            for path in ("/api/v1/admin/reports", "/api/v1/proposals", "/api/v1/users"):
                call(reporter, "GET", path, 403, label="non-admin read rejected " + path)
            proposal = call(author, "POST", "/api/v1/proposals", 201,
                            body={"title": "Proposition isolée", "content": "Données de test seulement."},
                            csrf=author_csrf, label="proposal creation")["proposal"]
            self.assertEqual(proposal["status"], "pending")

            admin = self.app.test_client()
            admin_login = call(admin, "POST", "/api/v1/login", 200,
                               body={"username": "journey-admin", "password": "Fictitious-Admin9!"},
                               label="admin real login")
            admin_csrf = admin_login["csrf_token"]
            self.assertTrue(admin_login["user"]["is_admin"])
            call(admin, "GET", "/api/v1/me", 200, label="admin session")
            reports = call(admin, "GET", "/api/v1/admin/reports", 200,
                           label="admin moderation read")
            displayed = next(item for item in reports if item["id"] == report["id"])
            self.assertEqual({key:displayed[key] for key in report_row.to_dict()}, report_row.to_dict())
            reported_comment = self.db.session.get(self.models.Comment, report_row.comment_id)
            self.assertEqual(displayed['comment']['id'], reported_comment.id)
            self.assertEqual(displayed['comment']['text'], reported_comment.text)
            self.assertEqual(displayed['story']['id'], reported_comment.story_id)

            stats = call(admin, "GET", "/api/v1/stats", 200, label="stats read")
            expected_stats = {"users": self.models.User.query.count(),
                              "comments": self.models.Comment.query.count(),
                              "reports": self.models.Report.query.count()}
            self.assertEqual(stats, expected_stats)
            stories = call(admin, "GET", "/api/v1/stories", 200, label="active stories read")
            active = self.models.Story.query.filter(self.models.Story.archived_at.is_(None))
            self.assertEqual({item["id"] for item in stories}, {item.id for item in active.all()})
            self.assertEqual(sum(item["category_id"] == 1 for item in stories),
                             active.filter_by(category_id=1).count())
            self.assertEqual(sum(item["category_id"] == 2 for item in stories),
                             active.filter_by(category_id=2).count())
            proposals = call(admin, "GET", "/api/v1/proposals", 200, label="admin proposals read")
            pending = sum(item["status"] == "pending" for item in proposals)
            self.assertEqual(pending, self.models.Proposal.query.filter_by(status="pending").count())

            call(admin, "POST", f"/api/v1/admin/users/{reporter_id}/ban", 200,
                 csrf=admin_csrf, label="reporter ban")
            call(reporter, "GET", "/api/v1/me", 403, label="banned session rejected")
            call(reporter, "POST", report_path, 401, body={"reason": "Test only"},
                 csrf=reporter_csrf, label="cleared session cannot report again")
            call(author, "GET", "/api/v1/me", 200, label="other author preserved")
            self.assertEqual(self.models.Report.query.count(), expected_stats["reports"])
            self.assertEqual(self.models.Comment.query.count(), expected_stats["comments"])
            self.assertTrue(self.db.session.get(self.models.User, reporter_id).is_banned)

            # Une FK effective refuse aussi une écriture ORM sans commentaire cible.
            with self.assertRaises(IntegrityError):
                with self.db.session.begin_nested():
                    self.db.session.add(self.models.Report(
                        comment_id=2147483647, reason="Orphelin volontaire de test"
                    ))
                    self.db.session.flush()
            self.assertEqual(self.models.Report.query.count(), expected_stats["reports"])
            with self.db.engine.connect() as connection:
                self.assertEqual(connection.exec_driver_sql("PRAGMA foreign_key_check").all(), [])
                report_fks = connection.exec_driver_sql("PRAGMA foreign_key_list(reports)").all()
                self.assertTrue(any(row[2:5] == ("comments", "comment_id", "id")
                                    and row[6] == "CASCADE" for row in report_fks))

            proof = {"result": "PASS", "scope": "WSGI and SQLite memory only; no browser",
                     "steps": self.steps, "foreign_keys": True, "database_files": [],
                     "comment_id": comment_id, "report_id": report["id"],
                     "report_target_matches_database": True, "reporter_identity_stored": False,
                     "stats_compared_to_database": stats, "active_story_count": len(stories),
                     "category_1_count": sum(item["category_id"] == 1 for item in stories),
                     "category_2_count": sum(item["category_id"] == 2 for item in stories),
                     "pending_proposal_count": pending, "post_ban_data_preserved": True}
            proof.update(orphan_insertion_rejected=True, foreign_key_check_empty=True,
                         report_comment_fk_cascade=True)
            (self.evidence / "moderation-journey.json").write_text(
                json.dumps(proof, ensure_ascii=True, indent=2), encoding="utf-8"
            )
