"""Persistent framework-error, stats and login checks; isolated SQLite memory."""

import unittest
from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

import test_reports as report_suite


class ApiErrorsStatsLoginTests(unittest.TestCase):
    PASSWORD = " Index-Test9! "

    @classmethod
    def setUpClass(cls):
        report_suite.ReportTests.setUpClass.__func__(cls)
        with cls.app.app_context():
            for user_id in (1, 2):
                cls.db.session.get(cls.models.User, user_id).set_password(cls.PASSWORD)
            cls.db.session.add(cls.models.Report(
                type="comment", target_id="1", reason="Test only",
            ))
            cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        report_suite.ReportTests.tearDownClass.__func__(cls)

    authenticate = report_suite.ReportTests.authenticate

    def setUp(self):
        report_suite.ReportTests.setUp(self)

    def tearDown(self):
        self.db.session.rollback()
        self.db.session.remove()

    def test_framework_400_is_json_without_private_detail(self):
        with patch.object(self.app, "preprocess_request", side_effect=BadRequest("private-detail")):
            response = self.client.get("/api/v1/stats")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"status": "error", "message": "Bad Request"})

    def test_framework_415_is_json_without_private_detail(self):
        with patch.object(self.app.request_class, "get_json", side_effect=UnsupportedMediaType("private-detail")):
            response = self.client.post("/api/v1/login", data="not-json")
        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.get_json(), {"status": "error", "message": "Unsupported Media Type"})

    def test_404_contract_is_preserved(self):
        for path in ("/route-inexistante", "/api/v1/route-inexistante"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.get_json(), {"status": "error", "message": "Not found"})

    def test_405_preserves_allow_header(self):
        response = self.client.get("/api/v1/login")
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.get_json(), {"status": "error", "message": "Method Not Allowed"})
        self.assertIn("POST", response.headers["Allow"])

    def test_non_api_framework_error_remains_html(self):
        with patch.object(self.app, "preprocess_request", side_effect=BadRequest("private-detail")):
            response = self.client.get("/outside-api")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.mimetype, "text/html")

    def test_business_error_contract_is_preserved(self):
        response = self.client.get("/api/v1/stories/slug/missing")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Story not found"})

    def test_stats_returns_real_nonzero_counts(self):
        response = self.client.get("/api/v1/stats")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"users": 2, "comments": 1, "reports": 1})

    def test_stats_database_failures_rollback_and_return_no_false_counts(self):
        for model in (self.models.User, self.models.Comment, self.models.Report):
            with self.subTest(model=model.__name__):
                with patch.object(model, "query") as query:
                    query.count.side_effect = SQLAlchemyError("private-sql-detail")
                    with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                        response = self.client.get("/api/v1/stats")
                        self.assertEqual(response.status_code, 500)
                        self.assertEqual(response.get_json(), {
                            "status": "error", "message": "Statistics unavailable",
                        })
                        rollback.assert_called_once_with()
                self.assertEqual(self.client.get("/api/v1/stats").status_code, 200)

    def test_login_invalid_json_shapes_are_400(self):
        for payload in ([], ["x"], True, 42, "text", None):
            with self.subTest(payload=payload):
                response = self.client.post("/api/v1/login", json=payload)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.get_json(), {
                    "status": "error", "message": "Identifiant et mot de passe obligatoires.",
                })

    def test_login_invalid_field_types_or_unicode_are_400(self):
        for field in ("username", "password"):
            for value in (None, True, 42, [], {}, "\ud800"):
                with self.subTest(field=field, value=repr(value)):
                    payload = {"username": "reader", "password": self.PASSWORD}
                    payload[field] = value
                    self.assertEqual(self.client.post("/api/v1/login", json=payload).status_code, 400)

    def test_login_preserves_valid_password_and_existing_authentication(self):
        response = self.client.post("/api/v1/login", json={
            "username": " reader ", "password": self.PASSWORD,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["user"]["id"], 1)
        self.assertTrue(response.get_json()["csrf_token"].isascii())

    def test_login_keeps_401_and_banned_403(self):
        for username, password, status in (
            ("reader", "incorrect", 401), ("banned", self.PASSWORD, 403),
        ):
            with self.subTest(username=username):
                response = self.client.post("/api/v1/login", json={
                    "username": username, "password": password,
                })
                self.assertEqual(response.status_code, status)

    def test_unexpected_production_500_is_generic_json(self):
        with patch.dict(self.app.config, {"PROPAGATE_EXCEPTIONS": False}):
            with patch.object(self.app, "log_exception"):
                with patch.object(self.app, "preprocess_request", side_effect=RuntimeError("private-detail")):
                    response = self.client.get("/api/v1/stats")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {"status": "error", "message": "Internal Server Error"})

    def test_single_application_and_route_count_are_preserved(self):
        import api.v1.app as relay
        self.assertIs(self.app, relay.app)
        self.assertEqual(len(list(self.app.url_map.iter_rules())), 25)



if __name__ == "__main__":
    unittest.main()
