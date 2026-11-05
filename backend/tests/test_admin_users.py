"""Lot 6A: fictitious accounts, guarded temporary SQLite memory, WSGI only."""

import unittest
from unittest.mock import patch

from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Query
import test_reports as report_suite


class AdminUsersTests(unittest.TestCase):
    authenticate = report_suite.ReportTests.authenticate

    @classmethod
    def setUpClass(cls):
        report_suite.ReportTests.setUpClass.__func__(cls)
        with cls.app.app_context():
            cls.db.session.add_all([
                cls.models.User(id=3, username="admin", email="admin@example.invalid", password_hash="unused", is_admin=True),
                cls.models.User(id=4, username="target", email="target@example.invalid", password_hash="unused"),
                cls.models.User(id=5, username="other-admin", email="other-admin@example.invalid", password_hash="unused", is_admin=True),
            ])
            cls.db.session.flush()
            cls.db.session.get(cls.models.User, 4).set_password("Fictitious-User9!")
            cls.db.session.add(cls.models.Story(
                id=2, slug="fictitious-target-story", title="Target story", summary="Fictitious summary",
                content="Fictitious content", category_id=1, author_id=4,
            ))
            cls.db.session.flush()
            cls.db.session.add_all([
                cls.models.Comment(id=2, story_id=2, user_id=4, username="target", text="Fictitious comment"),
                cls.models.Theory(id=1, story_id=2, user_id=4, title="Fictitious theory", content="Evidence"),
                cls.models.Proposal(id=1, user_id=4, title="Fictitious proposal", content="Evidence"),
                cls.models.Vote(id=1, user_id=4, story_id=2),
                cls.models.Report(id=1, type="comment", target_id="2", reason="Fictitious report"),
                cls.models.ColdCaseUpdate(id=1, story_id=2, content="Fictitious update"),
            ])
            cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        report_suite.ReportTests.tearDownClass.__func__(cls)

    def setUp(self):
        report_suite.ReportTests.setUp(self)

    def tearDown(self):
        self.db.session.rollback()
        self.models.User.query.filter(self.models.User.id > 5).delete()
        for user in self.models.User.query.all():
            user.is_banned = user.id == 2
        self.db.session.commit()
        self.db.session.remove()

    # Comparer les neuf tables, pas uniquement le compte ciblé : un bannissement
    # ne doit changer ni contribution, ni auteur, ni compteur, ni autre compte.
    def snapshot(self):
        return {table.name: [dict(row) for row in self.db.session.execute(
            table.select().order_by(table.c.id)
        ).mappings()] for table in self.db.metadata.sorted_tables}

    def client_for(self, user_id=3):
        client = self.app.test_client()
        if user_id is not None:
            with client.session_transaction() as session:
                session["user_id"] = user_id
                session["csrf_token"] = "reports-csrf"
        return client

    def ban(self, target=4, *, legacy=False, actor=3, csrf="reports-csrf", client=None, **kwargs):
        self.client = client or self.client_for(actor)
        if legacy:
            username = {2: "banned", 3: "admin", 4: "target", 5: "other-admin"}.get(target, "missing")
            path, method = "/api/v1/admin/users/" + username + "/ban", "DELETE"
        else:
            path, method = f"/api/v1/admin/users/{target}/ban", "POST"
        return self.client.open(path, method=method, headers={} if csrf is None else {"X-CSRF-Token": csrf}, **kwargs)

    def test_admin_list_includes_boolean_status_without_secrets(self):
        response = self.client_for().get("/api/v1/users")
        self.assertEqual(response.status_code, 200)
        users = response.get_json()
        self.assertEqual([user["id"] for user in users], [1, 2, 3, 4, 5])
        self.assertEqual([user["id"] for user in users if user["is_banned"]], [2])
        for user in users:
            self.assertIs(type(user["is_banned"]), bool)
            self.assertNotIn("password_hash", user)
            self.assertNotIn("csrf_token", user)

    def test_list_rejects_anonymous_reader_and_banned_admin(self):
        for actor, status in ((None, 401), (1, 403), (2, 403)):
            with self.subTest(actor=actor):
                self.assertEqual(self.client_for(actor).get("/api/v1/users").status_code, status)
        self.db.session.get(self.models.User, 3).is_banned = True
        self.db.session.commit()
        self.assertEqual(self.client_for(3).get("/api/v1/users").status_code, 403)

    def test_list_role_is_read_in_database_not_cookie(self):
        client = self.client_for(1)
        with client.session_transaction() as session:
            session["is_admin"] = True
        self.assertEqual(client.get("/api/v1/users").status_code, 403)

    def test_public_signup_and_me_do_not_expose_banned_status(self):
        response = self.client_for(None).post("/api/v1/users", json={
            "username": "fictitious-new", "email": "new@example.invalid", "password": "Fictitious-User9!"
        })
        self.assertEqual(response.status_code, 201)
        self.assertNotIn("is_banned", response.get_json()["user"])
        self.assertNotIn("is_banned", self.client_for(1).get("/api/v1/me").get_json()["user"])

    def test_both_routes_commit_only_target_flag(self):
        for legacy in (False, True):
            with self.subTest(legacy=legacy):
                self.db.session.get(self.models.User, 4).is_banned = False
                self.db.session.commit()
                before = self.snapshot()
                response = self.ban(legacy=legacy)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.get_json()["user"]["is_banned"])
                self.db.session.remove()
                self.assertTrue(self.db.session.get(self.models.User, 4).is_banned)
                expected = before
                next(row for row in expected["users"] if row["id"] == 4)["is_banned"] = True
                self.assertEqual(self.snapshot(), expected)

    def test_both_routes_reject_self_and_other_admin_including_banned_admin(self):
        for legacy in (False, True):
            for target in (3, 5):
                for banned in (False, True):
                    if target == 3 and banned:
                        continue
                    with self.subTest(legacy=legacy, target=target, banned=banned):
                        self.db.session.get(self.models.User, target).is_banned = banned
                        self.db.session.commit()
                        before = self.snapshot()
                        with patch.object(self.db.session, "commit") as commit:
                            response = self.ban(target, legacy=legacy)
                            self.assertEqual(response.status_code, 409)
                            self.assertEqual(response.get_json()["code"], "ADMIN_PROTECTED")
                            commit.assert_not_called()
                        self.assertEqual(self.snapshot(), before)

    def test_both_routes_reject_missing_and_invalid_csrf_before_changes(self):
        before = self.snapshot()
        for legacy in (False, True):
            for csrf in (None, "wrong", "", "é"):
                with self.subTest(legacy=legacy, csrf=csrf):
                    self.assertEqual(self.ban(legacy=legacy, csrf=csrf).status_code, 403)
        self.assertEqual(self.snapshot(), before)

    def test_both_routes_require_current_admin_not_forged_role(self):
        for legacy in (False, True):
            for actor, expected in ((None, 401), (1, 403), (2, 403), (999, 401)):
                with self.subTest(legacy=legacy, actor=actor):
                    self.assertEqual(self.ban(legacy=legacy, actor=actor).status_code, expected)
            client = self.client_for(1)
            with client.session_transaction() as session:
                session["is_admin"] = True
            self.assertEqual(self.ban(legacy=legacy, client=client).status_code, 403)

    def test_both_routes_missing_user_is_404_without_changes(self):
        before = self.snapshot()
        for legacy in (False, True):
            response = self.ban(999, legacy=legacy)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.get_json()["error"], "User not found")
        for target in (0, 2147483648, 10**30):
            self.assertEqual(self.ban(target).status_code, 404)
        self.assertEqual(self.snapshot(), before)

    def test_already_banned_and_repeated_ban_are_idempotent_on_both_routes(self):
        self.assertEqual(self.ban().status_code, 200)
        before = self.snapshot()
        for legacy in (False, True):
            self.assertEqual(self.ban(legacy=legacy).status_code, 200)
            self.assertEqual(self.ban(2, legacy=legacy).status_code, 200)
        self.assertEqual(self.snapshot(), before)

    def test_open_sessions_are_refused_and_new_login_is_blocked(self):
        readers = [self.client_for(None), self.client_for(None)]
        tokens = []
        for client in readers:
            response = client.post("/api/v1/login", json={"username": "target", "password": "Fictitious-User9!"})
            self.assertEqual(response.status_code, 200)
            tokens.append(response.get_json()["csrf_token"])
        self.assertEqual(self.ban().status_code, 200)
        before = self.snapshot()
        self.assertEqual(readers[0].get("/api/v1/me").status_code, 403)
        self.assertEqual(readers[1].post("/api/v1/proposals", json={"title": "No write", "content": "No write"},
                                       headers={"X-CSRF-Token": tokens[1]}).status_code, 403)
        for client in readers:
            with client.session_transaction() as session:
                self.assertNotIn("user_id", session)
        self.assertEqual(readers[0].post("/api/v1/login", json={"username": "target", "password": "Fictitious-User9!"}).status_code, 403)
        self.assertEqual(readers[0].get("/api/v1/stories").status_code, 200)
        self.assertEqual(self.snapshot(), before)

    def test_commit_failure_rolls_back_both_routes_without_details(self):
        before = self.snapshot()
        for legacy in (False, True):
            with patch.object(self.db.session, "commit", side_effect=SQLAlchemyError("private-sql-detail")):
                with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                    response = self.ban(legacy=legacy)
                    self.assertEqual(response.status_code, 500)
                    self.assertNotIn("private-sql-detail", response.get_data(as_text=True))
                    rollback.assert_called_once_with()
            self.db.session.remove()
            self.assertEqual(self.snapshot(), before)

    def test_real_flush_then_error_is_rolled_back(self):
        before = self.snapshot()
        for legacy in (False, True):
            def fail_after_flush(session):
                session.flush()
                raise SQLAlchemyError("private-sql-detail")
            event.listen(self.db.session(), "before_commit", fail_after_flush)
            try:
                self.assertEqual(self.ban(legacy=legacy).status_code, 500)
            finally:
                event.remove(self.db.session(), "before_commit", fail_after_flush)
            self.db.session.remove()
            self.assertEqual(self.snapshot(), before)

    def test_sql_lookup_and_list_failure_return_json_500(self):
        with patch.object(Query, "first", side_effect=SQLAlchemyError("private-sql-detail")):
            self.assertEqual(self.ban().status_code, 500)
        with patch.object(Query, "all", side_effect=SQLAlchemyError("private-sql-detail")):
            response = self.client_for().get("/api/v1/users")
            self.assertEqual(response.status_code, 500)
            self.assertTrue(response.is_json)
            self.assertNotIn("private-sql-detail", response.get_data(as_text=True))

    def test_no_json_body_is_required_or_trusted_for_banning(self):
        for legacy in (False, True):
            with patch.object(self.app.request_class, "get_json", side_effect=AssertionError("No JSON parsing")):
                response = self.ban(legacy=legacy, json={"is_banned": False, "is_admin": False})
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.get_json()["user"]["is_banned"])

    def test_id_route_handles_username_with_slash_without_path_ambiguity(self):
        self.db.session.get(self.models.User, 4).username = "fictitious/reader"
        self.db.session.commit()
        self.assertEqual(self.ban().status_code, 200)
        self.db.session.get(self.models.User, 4).username = "target"
        self.db.session.commit()
