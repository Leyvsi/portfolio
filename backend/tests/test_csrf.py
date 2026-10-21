"""CSRF middleware regressions with guarded in-memory SQLite and no network."""

import unittest
from unittest.mock import patch

from flask import request, session

import test_reports as report_suite


class CsrfTests(unittest.TestCase):
    TOKEN = "reports-csrf"
    CSRF_ERROR = {
        "status": "error", "message": "Token CSRF invalide ou manquant.",
    }

    @classmethod
    def setUpClass(cls):
        report_suite.ReportTests.setUpClass.__func__(cls)
        with cls.app.app_context():
            cls.db.session.get(cls.models.User, 1).set_password("Csrf-Test9!")
            cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        report_suite.ReportTests.tearDownClass.__func__(cls)

    authenticate = report_suite.ReportTests.authenticate

    def setUp(self):
        report_suite.ReportTests.setUp(self)
        self.proposal_payload = {"title": "CSRF test", "content": "Test evidence"}

    def tearDown(self):
        self.db.session.rollback()
        self.models.Proposal.query.delete()
        self.db.session.commit()
        self.db.session.remove()

    def set_session(self, token=TOKEN, *, user_id=1, missing=False):
        self.client = self.app.test_client()
        if user_id is not None:
            with self.client.session_transaction() as current:
                current["user_id"] = user_id
                if not missing:
                    current["csrf_token"] = token

    def post(self, token=TOKEN, *, path="/api/v1/proposals"):
        headers = {} if token is None else {"X-CSRF-Token": token}
        return self.client.post(path, json=self.proposal_payload, headers=headers)

    def assert_csrf_denied(self, response):
        self.assertEqual(response.status_code, 403, response.get_data(as_text=True))
        self.assertEqual(response.get_json(), self.CSRF_ERROR)
        self.assertEqual(self.models.Proposal.query.count(), 0)

    def test_login_without_csrf_is_successful(self):
        self.client = self.app.test_client()
        response = self.client.post("/api/v1/login", json={
            "username": "reader", "password": "Csrf-Test9!",
        })
        self.assertEqual(response.status_code, 200)
        token = response.get_json()["csrf_token"]
        self.assertIsInstance(token, str)
        self.assertTrue(token and token.isascii())
        with self.client.session_transaction() as current:
            self.assertEqual(current["user_id"], 1)
            self.assertEqual(current["csrf_token"], token)

    def test_login_exemption_survives_existing_session_and_invalid_tokens(self):
        self.set_session({"invalid": True})
        with patch.object(self.index.secrets, "compare_digest", side_effect=AssertionError("Login exempt")) as compare:
            response = self.client.post("/api/v1/login", json={
                "username": "reader", "password": "Csrf-Test9!",
            }, headers={"X-CSRF-Token": "\u00e9"})
            self.assertEqual(response.status_code, 200)
            compare.assert_not_called()

    def test_protected_post_with_correct_token_is_allowed(self):
        response = self.post()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.models.Proposal.query.count(), 1)

    def test_missing_header_token_is_403(self):
        self.assert_csrf_denied(self.post(None))

    def test_incorrect_header_token_is_403(self):
        self.assert_csrf_denied(self.post("incorrect-token"))

    def test_empty_header_token_is_403(self):
        self.assert_csrf_denied(self.post(""))

    def test_accented_header_token_is_403_without_exception(self):
        self.assertTrue(self.app.testing)
        self.assert_csrf_denied(self.post("\u00e9"))

    def test_emoji_header_token_is_403_without_exception(self):
        self.assert_csrf_denied(self.post("\U0001f600"))

    def test_other_nonascii_header_tokens_are_403(self):
        for token in ("\u03b1", "\u4e2d", "\u0661", "\u200b", "e\u0301", "\ud800"):
            with self.subTest(token=ascii(token)):
                self.assert_csrf_denied(self.post(token))

    def test_very_long_invalid_header_token_is_403(self):
        self.assert_csrf_denied(self.post("x" * 1_000_000))

    def test_nonstring_session_tokens_are_403(self):
        for token in (None, True, False, 0, 42, 1.5, [], ["token"], {}, {"token": self.TOKEN}, b"token", ("token",)):
            with self.subTest(token=repr(token)):
                self.set_session(token)
                self.assert_csrf_denied(self.post())

    def test_missing_or_empty_session_token_is_403(self):
        self.set_session(missing=True)
        self.assert_csrf_denied(self.post())
        self.set_session("")
        self.assert_csrf_denied(self.post())

    def test_nonascii_session_tokens_are_403_even_if_header_matches(self):
        for token in ("\u00e9", "\U0001f600", "\u4e2d"):
            with self.subTest(token=ascii(token)):
                self.set_session(token)
                self.assert_csrf_denied(self.post(token))

    def test_whitespace_only_tokens_are_403_even_if_they_match(self):
        self.set_session("   ")
        self.assert_csrf_denied(self.post("   "))

    def test_header_tokens_are_not_trimmed_for_comparison(self):
        self.assert_csrf_denied(self.post(" " + self.TOKEN))
        self.assert_csrf_denied(self.post(self.TOKEN + " "))

    def test_authenticated_get_does_not_require_csrf(self):
        self.set_session(missing=True)
        response = self.client.get("/api/v1/me")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["user"]["id"], 1)

    def test_head_and_options_do_not_require_csrf(self):
        for method, path in (("HEAD", "/api/v1/me"), ("OPTIONS", "/api/v1/proposals")):
            with self.subTest(method=method):
                self.set_session(missing=True)
                self.assertEqual(self.client.open(path, method=method).status_code, 200)

    def test_logout_with_correct_token_is_200_and_clears_session(self):
        response = self.post(path="/api/v1/logout")
        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as current:
            self.assertNotIn("user_id", current)
            self.assertNotIn("csrf_token", current)

    def test_logout_without_token_is_403_and_preserves_session(self):
        self.assert_csrf_denied(self.post(None, path="/api/v1/logout"))
        with self.client.session_transaction() as current:
            self.assertEqual(current["user_id"], 1)

    def test_logout_with_incorrect_token_is_403(self):
        self.assert_csrf_denied(self.post("incorrect-token", path="/api/v1/logout"))

    def test_logout_with_unicode_token_is_403(self):
        for token in ("\u00e9", "\U0001f600"):
            with self.subTest(token=ascii(token)):
                self.assert_csrf_denied(self.post(token, path="/api/v1/logout"))

    def test_banned_user_correct_csrf_reaches_permission_check(self):
        self.set_session(user_id=2)
        response = self.post()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json(), {
            "status": "error", "message": "Compte suspendu.",
        })
        with self.client.session_transaction() as current:
            self.assertNotIn("user_id", current)

    def test_banned_user_bad_csrf_is_rejected_before_permissions(self):
        self.set_session(user_id=2)
        with patch("api.v1.views.proposals.get_authenticated_user", side_effect=AssertionError("CSRF first")) as authenticate:
            self.assert_csrf_denied(self.post("incorrect-token"))
            authenticate.assert_not_called()
        with self.client.session_transaction() as current:
            self.assertEqual(current["user_id"], 2)

    def test_all_four_write_methods_require_csrf(self):
        for method in ("POST", "PUT", "PATCH", "DELETE"):
            with self.subTest(method=method):
                self.set_session()
                response = self.client.open(
                    "/api/v1/proposals", method=method,
                    headers={"X-CSRF-Token": "\u00e9"},
                )
                self.assert_csrf_denied(response)

    def test_valid_csrf_does_not_change_existing_method_permissions(self):
        for method in ("PUT", "PATCH", "DELETE"):
            with self.subTest(method=method):
                self.set_session()
                response = self.client.open(
                    "/api/v1/proposals", method=method,
                    headers={"X-CSRF-Token": self.TOKEN},
                )
                self.assertEqual(response.status_code, 405)

    def test_anonymous_requests_still_reach_authentication(self):
        self.set_session(user_id=None)
        response = self.post("\u00e9")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["message"], "Authentification requise.")

    def test_zero_user_id_does_not_bypass_csrf(self):
        self.set_session(user_id=0)
        self.assert_csrf_denied(self.post(None))
        self.assertEqual(self.post().status_code, 401)

    def test_comparison_is_called_only_with_valid_ascii_strings(self):
        compare_digest = self.index.secrets.compare_digest
        with patch.object(self.index.secrets, "compare_digest", wraps=compare_digest) as compare:
            self.assert_csrf_denied(self.post("\u00e9"))
            compare.assert_not_called()
            self.assertEqual(self.post().status_code, 201)
            compare.assert_called_once_with(self.TOKEN, self.TOKEN)

    def test_nonstring_header_values_are_rejected_without_coercion(self):
        class InvalidToken:
            def __str__(self):
                raise AssertionError("Invalid tokens must not be coerced")
        for token in (None, True, 42, b"token", [], {}, InvalidToken()):
            with self.subTest(type=type(token).__name__):
                with self.app.test_request_context("/api/v1/proposals", method="POST"):
                    session["user_id"] = 1
                    session["csrf_token"] = self.TOKEN
                    with patch.object(request._get_current_object(), "headers", {"X-CSRF-Token": token}):
                        response, status = self.index.protect_session_requests_from_csrf()
                        self.assertEqual(status, 403)
                        self.assertEqual(response.get_json(), self.CSRF_ERROR)


if __name__ == "__main__":
    unittest.main()
