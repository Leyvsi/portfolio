"""Isolated users/votes tests: guarded in-memory SQLite, no network."""

import sqlite3
import unittest
from unittest.mock import Mock, patch

from pymysql.err import IntegrityError as MySQLIntegrityError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import test_reports as report_suite


class UsersVotesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        report_suite.ReportTests.setUpClass.__func__(cls)

    @classmethod
    def tearDownClass(cls):
        report_suite.ReportTests.tearDownClass.__func__(cls)

    authenticate = report_suite.ReportTests.authenticate

    def setUp(self):
        report_suite.ReportTests.setUp(self)
        self.user_payload = {
            "username": "fresh", "email": "fresh@example.invalid",
            "password": "A-goodPass9!",
        }

    def tearDown(self):
        self.db.session.rollback()
        self.models.Vote.query.delete()
        self.models.Report.query.delete()
        self.models.User.query.filter(self.models.User.id > 2).delete()
        self.db.session.commit()
        self.db.session.remove()

    def request(self, route, payload=None, *, raw=None, user_id=1, target_id="1", absent=False):
        self.client = self.app.test_client()
        if user_id is not None:
            self.authenticate(user_id)
        arguments = {"headers": {"X-CSRF-Token": "reports-csrf"}}
        if raw is not None:
            arguments.update(data=raw, content_type="application/json")
        elif not absent:
            arguments["json"] = self.user_payload if route == "users" and payload is None else (payload or {})
        path = "/api/v1/users" if route == "users" else "/api/v1/votes/" + target_id
        return self.client.post(path, **arguments)

    def assert_error(self, response, expected):
        self.assertEqual(response.status_code, expected, response.get_data(as_text=True))
        self.assertTrue(response.is_json)
        body = response.get_json()
        self.assertTrue(body.get("error") or (body.get("status") == "error" and body.get("message")))

    def test_users_rejects_nonobject_and_absent_json(self):
        for raw in ('["x"]', "null", "true", "42", '"text"', "{", ""):
            with self.subTest(raw=raw):
                self.assert_error(self.request("users", raw=raw), 400)
        self.assert_error(self.request("users", absent=True), 400)

    def test_votes_ignores_body_without_parsing_json(self):
        for raw in ('["x"]', "null", "true", "42", '"text"', "{", '{"unused": true}'):
            with self.subTest(raw=raw):
                self.models.Vote.query.delete()
                self.db.session.commit()
                with patch.object(
                    self.app.request_class, "get_json",
                    side_effect=AssertionError("Votes must not parse JSON"),
                ) as get_json:
                    self.assertEqual(self.request("votes", raw=raw).status_code, 201)
                    get_json.assert_not_called()

    def test_votes_accepts_absent_body(self):
        self.assertEqual(self.request("votes", absent=True).status_code, 201)

    def test_users_requires_three_fields(self):
        for field in self.user_payload:
            payload = {**self.user_payload}
            del payload[field]
            with self.subTest(field=field):
                self.assert_error(self.request("users", payload), 400)

    def test_users_rejects_invalid_field_types_and_empty_strings(self):
        for field in self.user_payload:
            for value in (None, True, 42, [], {}, "", "   "):
                with self.subTest(field=field, value=value):
                    self.assert_error(self.request("users", {**self.user_payload, field: value}), 400)

    def test_users_enforces_model_lengths(self):
        for field, value in (
            ("username", "u" * 101), ("email", "e" * 151),
            ("password", "A" * 48 + "a1!"),
        ):
            with self.subTest(field=field):
                self.assert_error(self.request("users", {**self.user_payload, field: value}), 400)

    def test_users_accepts_maximum_valid_lengths(self):
        payload = {
            "username": "u" * 100,
            "email": "a" * 64 + "@" + "b" * 63 + "." + "c" * 21,
            "password": "A" * 47 + "a1!",
        }
        self.assertEqual((len(payload["email"]), len(payload["password"])), (150, 50))
        self.assertEqual(self.request("users", payload).status_code, 201)

    def test_users_checks_email_shape(self):
        for email in (
            "plain", "a@b", "a@@b.com", "a b@example.com",
            ".a@example.com", "a..b@example.com", "a@example..com",
            "a@-bad.example", "a" * 65 + "@example.com",
        ):
            with self.subTest(email=email):
                self.assert_error(self.request("users", {**self.user_payload, "email": email}), 400)

    def test_users_keeps_password_policy(self):
        for password in ("short", "NoDigitPassword!", "NoSymbolPass9", "lowercase9!", "UPPERCASE9!"):
            with self.subTest(password=password):
                self.assert_error(self.request("users", {**self.user_payload, "password": password}), 400)

    def test_users_trims_identifiers_but_preserves_password(self):
        payload = {"username": " spaced ", "email": " spaced@example.invalid ", "password": " A-goodPass9! "}
        response = self.request("users", payload, user_id=None)
        self.assertEqual(response.status_code, 201)
        stored = self.models.User.query.filter_by(username="spaced").one()
        self.assertEqual(stored.email, "spaced@example.invalid")
        self.assertTrue(stored.check_password(payload["password"]))
        self.assertFalse(stored.check_password(payload["password"].strip()))

    def test_users_rejects_invalid_unicode(self):
        for field in self.user_payload:
            with self.subTest(field=field):
                self.assert_error(self.request("users", {**self.user_payload, field: "\ud800"}), 400)

    def test_users_is_public_and_does_not_accept_client_admin_role(self):
        response = self.request("users", {**self.user_payload, "is_admin": True}, user_id=None)
        self.assertEqual(response.status_code, 201)
        stored = self.db.session.get(self.models.User, response.get_json()["user"]["id"])
        self.assertFalse(stored.is_admin)
        self.assertTrue(stored.check_password(self.user_payload["password"]))

    def test_users_blocks_an_existing_banned_session(self):
        self.assert_error(self.request("users", user_id=2), 403)

    def test_users_prechecked_duplicates_are_400(self):
        for field, value in (("username", "reader"), ("email", "reader@example.invalid")):
            with self.subTest(field=field):
                self.assert_error(self.request("users", {**self.user_payload, field: value}), 400)

    def test_votes_requires_authentication_with_unused_body(self):
        self.assert_error(self.request("votes", raw='["x"]', user_id=None), 401)

    def test_votes_blocks_banned_user(self):
        self.assert_error(self.request("votes", user_id=2), 403)
        with self.client.session_transaction() as session:
            self.assertNotIn("user_id", session)

    def test_votes_missing_user_is_401(self):
        self.assert_error(self.request("votes", user_id=999), 401)

    def test_votes_missing_story_is_404(self):
        for target in ("999", "9999999999999999999", "0"):
            with self.subTest(target=target):
                self.assert_error(self.request("votes", target_id=target), 404)

    def test_votes_success_then_duplicate(self):
        first = self.request("votes")
        self.assertEqual(first.status_code, 201)
        self.assertEqual(first.get_json()["votes"], 1)
        self.assert_error(self.request("votes"), 409)
        self.assertEqual(self.models.Vote.query.filter_by(user_id=1, story_id=1).count(), 1)

    def check_commit_error(self, route, error, status):
        with patch.object(self.db.session, "commit", side_effect=error):
            with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                response = self.request(route)
                self.assert_error(response, status)
                rollback.assert_called_once_with()
                self.assertNotIn("private-error-detail", response.get_data(as_text=True))

    def test_users_commit_error_rolls_back_and_session_recovers(self):
        self.check_commit_error("users", SQLAlchemyError("private-error-detail"), 500)
        self.assertEqual(self.models.User.query.count(), 2)
        self.assertEqual(self.request("users").status_code, 201)

    def test_votes_commit_error_rolls_back_and_session_recovers(self):
        self.check_commit_error("votes", SQLAlchemyError("private-error-detail"), 500)
        self.assertEqual(self.models.Vote.query.count(), 0)
        self.assertEqual(self.request("votes").status_code, 201)

    def test_add_errors_roll_back(self):
        for route in ("users", "votes"):
            with self.subTest(route=route):
                with patch.object(self.db.session, "add", side_effect=SQLAlchemyError("private-error-detail")):
                    with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                        response = self.request(route)
                        self.assert_error(response, 500)
                        rollback.assert_called_once_with()
                        self.assertNotIn("private-error-detail", response.get_data(as_text=True))

    def test_users_mysql_sqlite_unique_conflicts_are_400(self):
        originals = [
            sqlite3.IntegrityError("UNIQUE constraint failed: users.username"),
            sqlite3.IntegrityError("UNIQUE constraint failed: users.email"),
            MySQLIntegrityError(1062, "Duplicate entry 'x' for key 'username'"),
            MySQLIntegrityError(1062, "Duplicate entry 'x' for key 'users.email'"),
            MySQLIntegrityError(1062, "Duplicate entry 'x' for key `email`"),
        ]
        for original in originals:
            with self.subTest(original=original.args):
                self.check_commit_error("users", IntegrityError("insert", {}, original), 400)

    def test_votes_mysql_sqlite_unique_conflicts_are_409(self):
        originals = [
            MySQLIntegrityError(1062, "Duplicate entry '1-2' for key 'unique_user_story_vote'"),
            MySQLIntegrityError(1062, "Duplicate entry 'x' for key 'votes.unique_user_story_vote'"),
            MySQLIntegrityError(1062, "Duplicate entry 'x' for key `unique_user_story_vote`"),
            sqlite3.IntegrityError("UNIQUE constraint failed: votes.user_id, votes.story_id"),
        ]
        for original in originals:
            with self.subTest(original=original.args):
                self.check_commit_error("votes", IntegrityError("insert", {}, original), 409)

    def test_other_constraints_are_500_not_business_conflicts(self):
        for route in ("users", "votes"):
            for original in (
                MySQLIntegrityError(1062, "Duplicate entry 'x' for key 'other_constraint'"),
                MySQLIntegrityError(1452, "private-error-detail"),
                sqlite3.IntegrityError("FOREIGN KEY constraint failed"),
                sqlite3.IntegrityError("UNIQUE constraint failed: users.id"),
            ):
                with self.subTest(route=route, original=original.args):
                    self.check_commit_error(route, IntegrityError("insert", {}, original), 500)

    def test_users_real_sqlite_unique_error_after_precheck(self):
        query = Mock()
        query.filter_by.return_value.first.return_value = None
        with patch.object(self.models.User, "query", query):
            with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                self.assert_error(self.request("users", {**self.user_payload, "username": "reader"}), 400)
                rollback.assert_called_once_with()
        self.assertEqual(self.models.User.query.count(), 2)

    def test_votes_real_sqlite_unique_error_after_precheck(self):
        self.assertEqual(self.request("votes").status_code, 201)
        query = Mock()
        query.filter_by.return_value.first.return_value = None
        with patch.object(self.models.Vote, "query", query):
            with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                self.assert_error(self.request("votes"), 409)
                rollback.assert_called_once_with()
        self.assertEqual(self.models.Vote.query.count(), 1)

    def test_mysql_helper_does_not_stringify_exception(self):
        from api.v1.views.write_support import is_unique_conflict
        original = MySQLIntegrityError(1062, "Duplicate entry 'x' for key 'unique_user_story_vote'")
        wrapped = IntegrityError("insert", {}, original)
        with patch.object(MySQLIntegrityError, "__str__", side_effect=AssertionError("No stringify")) as stringify:
            self.assertTrue(is_unique_conflict(
                wrapped, mysql_keys={"unique_user_story_vote"}, sqlite_columns=set()
            ))
            stringify.assert_not_called()

    def test_helper_rejects_wrong_sqlite_constraint(self):
        from api.v1.views.write_support import is_unique_conflict
        error = IntegrityError("insert", {}, sqlite3.IntegrityError(
            "UNIQUE constraint failed: votes.id"
        ))
        self.assertFalse(is_unique_conflict(
            error, mysql_keys={"unique_user_story_vote"},
            sqlite_columns={frozenset({"votes.user_id", "votes.story_id"})},
        ))


if __name__ == "__main__":
    unittest.main()
