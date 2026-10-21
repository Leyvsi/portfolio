"""Isolated tests for POST /api/v1/reports; only in-memory SQLite is allowed."""

from contextlib import ExitStack
import importlib
import os
from pathlib import Path
import socket
import sys
import unittest
from unittest.mock import patch

from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
import dotenv


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guards = ExitStack()
        cls.addClassCleanup(cls.guards.close)
        cls.guards.enter_context(patch.dict(os.environ, {
            "SECRET_KEY": "reports-test-only",
            "CORS_ALLOWED_ORIGINS": "http://localhost:3000",
            "DATABASE_URL": "sqlite:///:memory:",
            "SESSION_COOKIE_SECURE": "false",
            **{name: "" for name in (
                "AIVEN_DB_HOST", "AIVEN_DB_PORT", "AIVEN_DB_USER",
                "AIVEN_DB_PASSWORD", "AIVEN_DB_NAME", "AIVEN_CA_CERT",
            )},
        }, clear=True))
        cls.dotenv_mock = cls.guards.enter_context(
            patch.object(dotenv, "load_dotenv", return_value=False)
        )
        cls.network_guards = [
            cls.guards.enter_context(patch.object(
                owner, name, side_effect=AssertionError("Network forbidden")
            ))
            for owner, name in (
                (socket, "create_connection"),
                (socket.socket, "connect"),
                (socket.socket, "connect_ex"),
            )
        ]
        cls.memory_connections = 0
        original_connect = Engine.connect
        original_raw_connection = Engine.raw_connection

        def guard_database(engine):
            if engine.url.drivername != "sqlite" or engine.url.database != ":memory:":
                raise AssertionError("Only SQLite in memory is allowed")

        def connect(engine, *args, **kwargs):
            guard_database(engine)
            cls.memory_connections += 1
            return original_connect(engine, *args, **kwargs)

        def raw_connection(engine, *args, **kwargs):
            guard_database(engine)
            return original_raw_connection(engine, *args, **kwargs)

        cls.guards.enter_context(patch.object(Engine, "connect", connect))
        cls.guards.enter_context(patch.object(Engine, "raw_connection", raw_connection))
        backend = str(Path(__file__).resolve().parents[1])
        cls.guards.enter_context(patch.object(sys, "path", [backend, *sys.path]))
        cls.index = importlib.import_module("index")
        cls.models = importlib.import_module("models")
        cls.app = cls.index.app
        cls.app.config["TESTING"] = True
        cls.db = cls.models.db
        with cls.app.app_context():
            guard_database(cls.db.engine)
            cls.db.create_all()
            cls.db.session.add_all([
                cls.models.User(
                    id=1, username="reader", email="reader@example.invalid",
                    password_hash="unused", is_admin=False, is_banned=False,
                ),
                cls.models.User(
                    id=2, username="banned", email="banned@example.invalid",
                    password_hash="unused", is_admin=False, is_banned=True,
                ),
                cls.models.Category(id=1, name="audit"),
            ])
            cls.db.session.flush()
            cls.db.session.add(cls.models.Story(
                id=1, slug="audit-story", title="Audit", summary="Summary",
                content="Content", category_id=1, author_id=1,
            ))
            cls.db.session.flush()
            cls.db.session.add(cls.models.Comment(
                id=1, story_id=1, user_id=1, username="reader", text="Comment",
            ))
            cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            cls.db.session.remove()
            cls.db.engine.dispose()
        for guard in cls.network_guards:
            guard.assert_not_called()
        print(
            "Isolation verified: SQLite memory only; network calls=0; "
            "dotenv reads=0; Aiven connections=0"
        )

    def setUp(self):
        self.context = self.app.app_context()
        self.context.push()
        self.addCleanup(self.context.pop)
        self.client = self.app.test_client()
        self.authenticate()
        self.payload = {"type": "comment", "target_id": "1", "reason": "Spam"}

    def tearDown(self):
        self.db.session.rollback()
        self.db.session.query(self.models.Report).delete()
        self.db.session.commit()
        self.db.session.remove()

    def authenticate(self, user_id=1):
        with self.client.session_transaction() as session:
            session.clear()
            session["user_id"] = user_id
            session["csrf_token"] = "reports-csrf"

    def post(self, payload=None, **kwargs):
        if "data" not in kwargs:
            kwargs["json"] = self.payload if payload is None else payload
        return self.client.post(
            "/api/v1/reports", headers={"X-CSRF-Token": "reports-csrf"}, **kwargs
        )

    def assert_error(self, response, status):
        self.assertEqual(response.status_code, status)
        self.assertTrue(response.is_json)
        body = response.get_json()
        self.assertEqual(body["status"], "error")
        self.assertIsInstance(body["message"], str)

    def test_anonymous_is_401_even_with_invalid_body(self):
        self.client = self.app.test_client()
        self.assert_error(self.post(["invalid"]), 401)

    def test_banned_is_403_and_session_is_cleared(self):
        self.authenticate(2)
        self.assert_error(self.post(), 403)
        with self.client.session_transaction() as session:
            self.assertNotIn("user_id", session)

    def test_missing_user_is_401(self):
        self.authenticate(999)
        self.assert_error(self.post(), 401)

    def test_missing_csrf_is_403(self):
        response = self.client.post("/api/v1/reports", json=self.payload)
        self.assert_error(response, 403)

    def test_array_body_is_400(self):
        self.assert_error(self.post(["invalid"]), 400)

    def test_absent_body_is_400(self):
        self.assert_error(self.post(data=b""), 400)

    def test_malformed_json_is_400(self):
        self.assert_error(self.post(data="{", content_type="application/json"), 400)

    def test_scalar_bodies_are_400(self):
        for body in (None, True, False, 1, "text"):
            with self.subTest(body=body):
                response = self.client.post(
                    "/api/v1/reports", json=body,
                    headers={"X-CSRF-Token": "reports-csrf"},
                )
                self.assert_error(response, 400)

    def test_missing_type_is_400(self):
        del self.payload["type"]
        self.assert_error(self.post(), 400)

    def test_missing_target_id_is_400(self):
        del self.payload["target_id"]
        self.assert_error(self.post(), 400)

    def test_missing_reason_is_400(self):
        del self.payload["reason"]
        self.assert_error(self.post(), 400)

    def test_all_fields_must_be_strings(self):
        for field in self.payload:
            for value in (None, True, 1, [], {}):
                with self.subTest(field=field, value=value):
                    self.assert_error(self.post({**self.payload, field: value}), 400)

    def test_all_fields_must_be_nonempty(self):
        for field in self.payload:
            for value in ("", "   "):
                with self.subTest(field=field, value=value):
                    self.assert_error(self.post({**self.payload, field: value}), 400)

    def test_unsupported_types_are_400(self):
        for report_type in ("commentaire", "Comment", "story", "theory", "user", "photo"):
            with self.subTest(report_type=report_type):
                self.assert_error(self.post({**self.payload, "type": report_type}), 400)

    def test_invalid_target_ids_are_400(self):
        for target_id in ("0", "000", "-1", "+1", "1.0", "abc", "2147483648", "9" * 5000, "\u0661"):
            with self.subTest(target_id=target_id[:30]):
                self.assert_error(self.post({**self.payload, "target_id": target_id}), 400)

    def test_missing_comment_is_404(self):
        self.assert_error(self.post({**self.payload, "target_id": "999"}), 404)

    def test_valid_comment_is_201_and_persisted(self):
        response = self.post()
        self.assertEqual(response.status_code, 201)
        body = response.get_json()
        self.assertEqual(body["status"], "success")
        stored = self.db.session.get(self.models.Report, body["report"]["id"])
        self.assertEqual((stored.type, stored.target_id, stored.reason), ("comment", "1", "Spam"))

    def test_values_are_trimmed_and_id_is_canonical(self):
        response = self.post({"type": " comment ", "target_id": " 00001 ", "reason": " Spam "})
        self.assertEqual(response.status_code, 201)
        report = response.get_json()["report"]
        self.assertEqual((report["type"], report["target_id"], report["reason"]), ("comment", "1", "Spam"))

    def test_duplicate_reports_remain_allowed(self):
        first = self.post()
        second = self.post()
        self.assertEqual((first.status_code, second.status_code), (201, 201))
        self.assertNotEqual(first.get_json()["report"]["id"], second.get_json()["report"]["id"])
        self.assertEqual(self.models.Report.query.count(), 2)

    def test_commit_failure_rolls_back_without_sql_leak(self):
        with patch.object(self.db.session, "commit", side_effect=SQLAlchemyError("internal-commit-detail")):
            with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                response = self.post()
                self.assert_error(response, 500)
                rollback.assert_called_once_with()
                self.assertNotIn("internal-commit-detail", response.get_data(as_text=True))
        self.assertEqual(self.models.Report.query.count(), 0)
        self.assertEqual(self.post().status_code, 201)

    def test_add_failure_rolls_back(self):
        with patch.object(self.db.session, "add", side_effect=SQLAlchemyError("internal-add-detail")):
            with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                response = self.post()
                self.assert_error(response, 500)
                rollback.assert_called_once_with()
                self.assertNotIn("internal-add-detail", response.get_data(as_text=True))

    def test_no_legacy_reports_column_and_counter_stays_compatible(self):
        self.assertNotIn("reports", self.models.Comment.__table__.columns)
        self.assertFalse(hasattr(self.models.Comment, "reports"))
        self.assertEqual(self.post().status_code, 201)
        comments = importlib.import_module("api.v1.views.comments")
        comment = self.db.session.get(self.models.Comment, 1)
        self.assertEqual(comments.comment_to_dict(comment)["reports"], 1)


if __name__ == "__main__":
    unittest.main()
