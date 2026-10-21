"""Isolated proposals/admin-ban tests: guarded SQLite memory, no network."""

import unittest
from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

import test_reports as report_suite


class ProposalsBanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        report_suite.ReportTests.setUpClass.__func__(cls)
        with cls.app.app_context():
            cls.db.session.add_all([
                cls.models.User(
                    id=3, username="admin", email="admin@example.invalid",
                    password_hash="unused", is_admin=True, is_banned=False,
                ),
                cls.models.User(
                    id=4, username="target", email="target@example.invalid",
                    password_hash="unused", is_admin=False, is_banned=False,
                ),
            ])
            cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        report_suite.ReportTests.tearDownClass.__func__(cls)

    authenticate = report_suite.ReportTests.authenticate

    def setUp(self):
        report_suite.ReportTests.setUp(self)
        self.proposal_payload = {"title": " A proposal ", "content": " Some evidence "}

    def tearDown(self):
        self.db.session.rollback()
        self.models.Proposal.query.delete()
        self.models.User.query.filter(self.models.User.id.in_((1, 3, 4))).update(
            {self.models.User.is_banned: False}, synchronize_session=False,
        )
        self.db.session.commit()
        self.db.session.remove()

    def request(self, route, payload=None, *, raw=None, absent=False,
                user_id=1, username="target", session_admin=None):
        self.client = self.app.test_client()
        if user_id is not None:
            self.authenticate(user_id)
            if session_admin is not None:
                with self.client.session_transaction() as session:
                    session["is_admin"] = session_admin
        kwargs = {"headers": {"X-CSRF-Token": "reports-csrf"}}
        if raw is not None:
            kwargs.update(data=raw, content_type="application/json")
        elif route == "post" and not absent:
            kwargs["json"] = self.proposal_payload if payload is None else payload
        if route == "ban":
            return self.client.delete("/api/v1/admin/users/" + username + "/ban", **kwargs)
        if route == "get":
            return self.client.get("/api/v1/proposals", **kwargs)
        return self.client.post("/api/v1/proposals", **kwargs)

    def assert_error(self, response, status):
        self.assertEqual(response.status_code, status, response.get_data(as_text=True))
        self.assertTrue(response.is_json)
        body = response.get_json()
        self.assertTrue(body.get("error") or (
            body.get("status") == "error" and body.get("message")
        ))
        self.assertNotIn("private-sql-detail", response.get_data(as_text=True))

    def test_post_anonymous_is_401_without_parsing_json(self):
        with patch.object(self.app.request_class, "get_json", side_effect=AssertionError("Auth first")) as get_json:
            self.assert_error(self.request("post", raw='["invalid"]', user_id=None), 401)
            get_json.assert_not_called()

    def test_post_banned_is_403_without_parsing_json(self):
        with patch.object(self.app.request_class, "get_json", side_effect=AssertionError("Auth first")) as get_json:
            self.assert_error(self.request("post", raw='["invalid"]', user_id=2), 403)
            get_json.assert_not_called()
        with self.client.session_transaction() as session:
            self.assertNotIn("user_id", session)

    def test_post_missing_user_is_401_without_parsing_json(self):
        with patch.object(self.app.request_class, "get_json", side_effect=AssertionError("Auth first")) as get_json:
            self.assert_error(self.request("post", raw='["invalid"]', user_id=999), 401)
            get_json.assert_not_called()
        with self.client.session_transaction() as session:
            self.assertNotIn("user_id", session)

    def test_post_array_json_is_400(self):
        self.assert_error(self.request("post", raw='["invalid"]'), 400)

    def test_post_absent_body_is_400(self):
        self.assert_error(self.request("post", absent=True), 400)

    def test_post_null_scalar_or_malformed_json_is_400(self):
        for raw in ("null", "true", "42", '"text"', "{", ""):
            with self.subTest(raw=raw):
                self.assert_error(self.request("post", raw=raw), 400)

    def test_post_title_is_required(self):
        self.assert_error(self.request("post", {"content": "Evidence"}), 400)

    def test_post_content_is_required(self):
        self.assert_error(self.request("post", {"title": "Evidence"}), 400)

    def test_post_both_fields_must_be_strings(self):
        for field in self.proposal_payload:
            for value in (None, True, 42, [], {}):
                with self.subTest(field=field, value=value):
                    self.assert_error(self.request("post", {
                        **self.proposal_payload, field: value,
                    }), 400)

    def test_post_both_fields_must_be_nonempty(self):
        for field in self.proposal_payload:
            for value in ("", "   ", "\t\r\n"):
                with self.subTest(field=field, value=value):
                    self.assert_error(self.request("post", {
                        **self.proposal_payload, field: value,
                    }), 400)

    def test_post_rejects_title_over_model_limit(self):
        limit = self.models.Proposal.title.type.length
        self.assertEqual(limit, 200)
        self.assert_error(self.request("post", {
            **self.proposal_payload, "title": "t" * (limit + 1),
        }), 400)

    def test_post_accepts_title_at_model_limit_after_trim(self):
        title = "t" * self.models.Proposal.title.type.length
        response = self.request("post", {**self.proposal_payload, "title": " " + title + " "})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["proposal"]["title"], title)

    def test_post_rejects_content_over_text_byte_limit(self):
        for content in ("x" * 65536, "\u00e9" * 32768):
            with self.subTest(bytes=len(content.encode("utf-8"))):
                self.assert_error(self.request("post", {
                    **self.proposal_payload, "content": content,
                }), 400)

    def test_post_accepts_content_at_text_byte_limit(self):
        for content in ("x" * 65535, "\u00e9" * 32767):
            with self.subTest(bytes=len(content.encode("utf-8"))):
                response = self.request("post", {**self.proposal_payload, "content": content})
                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.get_json()["proposal"]["content"], content)

    def test_post_rejects_invalid_unicode(self):
        for field in self.proposal_payload:
            with self.subTest(field=field):
                self.assert_error(self.request("post", {
                    **self.proposal_payload, field: "\ud800",
                }), 400)

    def test_post_success_is_201_and_values_are_trimmed(self):
        response = self.request("post")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["status"], "success")
        body = response.get_json()["proposal"]
        self.assertEqual((body["title"], body["content"]), ("A proposal", "Some evidence"))
        stored = self.db.session.get(self.models.Proposal, body["id"])
        self.assertEqual((stored.title, stored.content, stored.user_id), ("A proposal", "Some evidence", 1))

    def test_post_ignores_client_user_id(self):
        for user_id in (2, 999, None, {"forged": True}):
            with self.subTest(user_id=user_id):
                response = self.request("post", {**self.proposal_payload, "user_id": user_id})
                self.assertEqual(response.status_code, 201)
                body = response.get_json()["proposal"]
                self.assertEqual(body["user_id"], 1)
                self.assertEqual(self.db.session.get(self.models.Proposal, body["id"]).user_id, 1)

    def test_post_ignores_client_status(self):
        for status in ("approved", "rejected", None, {"forged": True}):
            with self.subTest(status=status):
                response = self.request("post", {**self.proposal_payload, "status": status})
                self.assertEqual(response.status_code, 201)
                body = response.get_json()["proposal"]
                self.assertEqual(body["status"], "pending")
                self.assertEqual(self.db.session.get(self.models.Proposal, body["id"]).status, "pending")

    def test_post_default_status_is_pending(self):
        response = self.request("post")
        self.assertEqual(response.status_code, 201)
        proposal = response.get_json()["proposal"]
        self.assertEqual((proposal["user_id"], proposal["status"]), (1, "pending"))

    def test_post_add_failure_rolls_back_and_session_recovers(self):
        with patch.object(self.db.session, "add", side_effect=SQLAlchemyError("private-sql-detail")):
            with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                self.assert_error(self.request("post"), 500)
                rollback.assert_called_once_with()
        self.assertEqual(self.models.Proposal.query.count(), 0)
        self.assertEqual(self.request("post").status_code, 201)

    def test_post_commit_failure_rolls_back_and_session_recovers(self):
        with patch.object(self.db.session, "commit", side_effect=SQLAlchemyError("private-sql-detail")):
            with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                self.assert_error(self.request("post"), 500)
                rollback.assert_called_once_with()
        self.assertEqual(self.models.Proposal.query.count(), 0)
        self.assertEqual(self.request("post").status_code, 201)

    def test_post_failure_after_real_flush_undoes_insert(self):
        def fail_after_flush():
            self.db.session.flush()
            raise SQLAlchemyError("private-sql-detail")
        with patch.object(self.db.session, "commit", side_effect=fail_after_flush):
            with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                self.assert_error(self.request("post"), 500)
                rollback.assert_called_once_with()
        self.assertEqual(self.models.Proposal.query.count(), 0)
        self.assertEqual(self.request("post").status_code, 201)

    def test_get_anonymous_is_401(self):
        self.assert_error(self.request("get", user_id=None), 401)

    def test_get_nonadmin_is_403(self):
        self.assert_error(self.request("get"), 403)

    def test_get_admin_is_200_and_returns_proposals(self):
        created = self.request("post").get_json()["proposal"]
        response = self.request("get", user_id=3)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)
        self.assertEqual(response.get_json(), [created])

    def test_get_ignores_forged_admin_session_claim(self):
        self.assert_error(self.request("get", session_admin=True), 403)
        self.assertEqual(self.request("get", user_id=3, session_admin=False).status_code, 200)

    def test_get_missing_user_is_401(self):
        self.assert_error(self.request("get", user_id=999), 401)

    def test_get_banned_admin_is_403(self):
        self.db.session.get(self.models.User, 3).is_banned = True
        self.db.session.commit()
        self.assert_error(self.request("get", user_id=3), 403)

    def test_ban_anonymous_is_401(self):
        self.assert_error(self.request("ban", user_id=None), 401)

    def test_ban_nonadmin_is_403(self):
        self.assert_error(self.request("ban"), 403)
        self.assertFalse(self.db.session.get(self.models.User, 4).is_banned)

    def test_ban_banned_actor_is_403(self):
        self.assert_error(self.request("ban", user_id=2), 403)

    def test_ban_missing_actor_is_401(self):
        self.assert_error(self.request("ban", user_id=999), 401)

    def test_ban_ignores_forged_admin_session_claim(self):
        self.assert_error(self.request("ban", session_admin=True), 403)
        self.assertFalse(self.db.session.get(self.models.User, 4).is_banned)

    def test_ban_missing_target_is_404_without_commit(self):
        with patch.object(self.db.session, "commit") as commit:
            self.assert_error(self.request("ban", user_id=3, username="missing"), 404)
            commit.assert_not_called()
        self.assertEqual(self.models.User.query.count(), 4)

    def test_ban_success_changes_only_is_banned(self):
        target = self.db.session.get(self.models.User, 4)
        before = {column.name: getattr(target, column.name) for column in self.models.User.__table__.columns}
        response = self.request("ban", user_id=3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "success")
        after = {column.name: getattr(target, column.name) for column in self.models.User.__table__.columns}
        self.assertEqual(after, {**before, "is_banned": True})

    def test_ban_second_request_is_200_and_stays_banned(self):
        first = self.request("ban", user_id=3)
        second = self.request("ban", user_id=3)
        self.assertEqual((first.status_code, second.status_code), (200, 200))
        self.assertTrue(self.db.session.get(self.models.User, 4).is_banned)
        self.assertEqual(self.models.User.query.count(), 4)

    def test_ban_already_banned_target_is_200(self):
        self.assertEqual(self.request("ban", user_id=3, username="banned").status_code, 200)
        self.assertTrue(self.db.session.get(self.models.User, 2).is_banned)

    def test_ban_never_deletes_user(self):
        with patch.object(self.db.session, "delete", wraps=self.db.session.delete) as delete:
            self.assertEqual(self.request("ban", user_id=3).status_code, 200)
            delete.assert_not_called()
        self.assertIsNotNone(self.db.session.get(self.models.User, 4))
        self.assertEqual(self.models.User.query.count(), 4)

    def test_ban_commit_failure_rolls_back_and_session_recovers(self):
        with patch.object(self.db.session, "commit", side_effect=SQLAlchemyError("private-sql-detail")):
            with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                self.assert_error(self.request("ban", user_id=3), 500)
                rollback.assert_called_once_with()
        self.assertFalse(self.db.session.get(self.models.User, 4).is_banned)
        self.assertEqual(self.models.User.query.count(), 4)
        self.assertEqual(self.request("ban", user_id=3).status_code, 200)
        self.assertTrue(self.db.session.get(self.models.User, 4).is_banned)

    def test_ban_failure_after_real_flush_undoes_update(self):
        def fail_after_flush():
            self.db.session.flush()
            raise SQLAlchemyError("private-sql-detail")
        with patch.object(self.db.session, "commit", side_effect=fail_after_flush):
            with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                self.assert_error(self.request("ban", user_id=3), 500)
                rollback.assert_called_once_with()
        self.assertFalse(self.db.session.get(self.models.User, 4).is_banned)
        self.assertEqual(self.models.User.query.count(), 4)
        self.assertEqual(self.request("ban", user_id=3).status_code, 200)

    def test_ban_requires_no_json_body(self):
        with patch.object(self.app.request_class, "get_json", side_effect=AssertionError("JSON forbidden")) as get_json:
            self.assertEqual(self.request("ban", user_id=3, raw='["invalid"]').status_code, 200)
            get_json.assert_not_called()

    def test_admin_self_ban_remains_allowed_and_next_request_is_blocked(self):
        self.assertEqual(self.request("ban", user_id=3, username="admin").status_code, 200)
        admin = self.db.session.get(self.models.User, 3)
        self.assertTrue(admin.is_banned)
        self.assertTrue(admin.is_admin)
        self.assert_error(self.request("get", user_id=3), 403)
        with self.client.session_transaction() as session:
            self.assertNotIn("user_id", session)
        self.assertEqual(self.models.User.query.count(), 4)


if __name__ == "__main__":
    unittest.main()
