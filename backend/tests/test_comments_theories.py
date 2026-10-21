"""Isolated comments/theories writes; SQLite memory only, network forbidden."""

import unittest
from unittest.mock import Mock, patch

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.attributes import set_committed_value

import test_reports as report_suite


class CommentsTheoriesTests(unittest.TestCase):
    PATHS = {
        "comment": "/api/v1/stories/{id}/comments",
        "report": "/api/v1/comments/{id}/report",
        "comment_like": "/api/v1/comments/{id}/like",
        "theory": "/api/v1/stories/{id}/theories",
        "theory_like": "/api/v1/theories/{id}/like",
    }
    PAYLOADS = {
        "comment": {"text": " A useful comment "},
        "report": {"reason": " Spam "},
        "theory": {"title": " A theory ", "content": " Some evidence "},
    }
    LIKES = ("comment_like", "theory_like")
    CREATES = ("comment", "report", "theory")

    @classmethod
    def setUpClass(cls):
        report_suite.ReportTests.setUpClass.__func__(cls)
        with cls.app.app_context():
            cls.db.session.add(cls.models.Theory(
                id=1, story_id=1, user_id=1, title="Existing theory",
                content="Existing evidence",
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
        self.models.Report.query.delete()
        self.models.Comment.query.filter(self.models.Comment.id > 1).delete()
        self.models.Theory.query.filter(self.models.Theory.id > 1).delete()
        for model in (self.models.Comment, self.models.Theory):
            self.db.session.execute(update(model).values(likes=0))
        self.db.session.commit()
        self.db.session.remove()

    def post(self, route, payload=None, *, raw=None, absent=False, user_id=1, identifier=1):
        self.client = self.app.test_client()
        if user_id is not None:
            self.authenticate(user_id)
        kwargs = {"headers": {"X-CSRF-Token": "reports-csrf"}}
        if raw is not None:
            kwargs.update(data=raw, content_type="application/json")
        elif not absent and route in self.PAYLOADS:
            kwargs["json"] = self.PAYLOADS[route] if payload is None else payload
        return self.client.post(self.PATHS[route].format(id=identifier), **kwargs)

    def assert_error(self, response, status):
        self.assertEqual(response.status_code, status, response.get_data(as_text=True))
        self.assertTrue(response.is_json)
        body = response.get_json()
        self.assertTrue(body.get("error") or (
            body.get("status") == "error" and body.get("message")
        ))
        self.assertNotIn("private-sql-detail", response.get_data(as_text=True))

    def model_for(self, route):
        return {
            "comment": self.models.Comment, "report": self.models.Report,
            "theory": self.models.Theory,
            "comment_like": self.models.Comment, "theory_like": self.models.Theory,
        }[route]

    def like_body(self, route, response):
        key = "comment" if route == "comment_like" else "theory"
        return response.get_json()[key]

    def test_all_five_routes_require_authentication(self):
        for route in self.PATHS:
            with self.subTest(route=route):
                self.assert_error(self.post(route, raw='["invalid"]', user_id=None), 401)

    def test_all_five_routes_block_banned_user(self):
        for route in self.PATHS:
            with self.subTest(route=route):
                self.assert_error(self.post(route, user_id=2), 403)
                with self.client.session_transaction() as session:
                    self.assertNotIn("user_id", session)

    def test_all_five_routes_reject_missing_session_user(self):
        for route in self.PATHS:
            with self.subTest(route=route):
                self.assert_error(self.post(route, user_id=999), 401)

    def test_missing_resources_are_404_before_body_validation(self):
        for route in self.PATHS:
            for identifier in (0, 999, 9999999999999999999):
                with self.subTest(route=route, identifier=identifier):
                    self.assert_error(self.post(route, raw='["invalid"]', identifier=identifier), 404)

    def test_all_three_create_routes_reject_nonobject_json(self):
        for route in self.CREATES:
            for raw in ('["invalid"]', "null", "true", "42", '"text"', "{"):
                with self.subTest(route=route, raw=raw):
                    self.assert_error(self.post(route, raw=raw), 400)

    def test_all_three_create_routes_require_a_body(self):
        for route in self.CREATES:
            with self.subTest(route=route):
                self.assert_error(self.post(route, absent=True), 400)
                self.assert_error(self.post(route, raw=""), 400)

    def test_comment_requires_text(self):
        self.assert_error(self.post("comment", {}), 400)

    def test_comment_rejects_wrong_text_types(self):
        for value in (None, True, 1, [], {}):
            with self.subTest(value=value):
                self.assert_error(self.post("comment", {"text": value}), 400)

    def test_comment_rejects_empty_text(self):
        for value in ("", "   ", "\t\r\n"):
            with self.subTest(value=value):
                self.assert_error(self.post("comment", {"text": value}), 400)

    def test_comment_rejects_text_over_mysql_text_byte_limit(self):
        for value in ("x" * 65536, "\u00e9" * 32768):
            with self.subTest(bytes=len(value.encode("utf-8"))):
                self.assert_error(self.post("comment", {"text": value}), 400)

    def test_comment_accepts_mysql_text_boundary(self):
        for value in ("x" * 65535, "\u00e9" * 32767):
            with self.subTest(bytes=len(value.encode("utf-8"))):
                response = self.post("comment", {"text": value})
                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.get_json()["comment"]["text"], value)

    def test_comment_success_trims_text_and_uses_server_identity(self):
        response = self.post("comment", {
            "text": "  New evidence  ", "user_id": 2, "username": "forged",
        })
        self.assertEqual(response.status_code, 201)
        body = response.get_json()["comment"]
        self.assertEqual((body["text"], body["user_id"], body["username"]), (
            "New evidence", 1, "reader",
        ))
        self.assertEqual(body["reports"], 0)
        self.assertEqual(self.db.session.get(self.models.Comment, body["id"]).text, "New evidence")

    def test_report_requires_reason(self):
        self.assert_error(self.post("report", {}), 400)

    def test_report_rejects_wrong_reason_types(self):
        for value in (None, True, 1, [], {}):
            with self.subTest(value=value):
                self.assert_error(self.post("report", {"reason": value}), 400)

    def test_report_rejects_empty_reason(self):
        for value in ("", "   ", "\t\r\n"):
            with self.subTest(value=value):
                self.assert_error(self.post("report", {"reason": value}), 400)

    def test_report_accepts_over_2000_characters_up_to_text_limit(self):
        for value in ("r" * 2001, "r" * 65535):
            with self.subTest(length=len(value)):
                response = self.post("report", {"reason": value})
                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.get_json()["report"]["reason"], value)

    def test_report_rejects_reason_over_mysql_text_byte_limit(self):
        for value in ("x" * 65536, "\u00e9" * 32768):
            with self.subTest(bytes=len(value.encode("utf-8"))):
                self.assert_error(self.post("report", {"reason": value}), 400)

    def test_report_stores_comment_type_and_canonical_target(self):
        response = self.post("report", {"reason": "  Spam  "}, identifier="0001")
        self.assertEqual(response.status_code, 201)
        body = response.get_json()["report"]
        self.assertEqual((body["type"], body["target_id"], body["reason"]), ("comment", "1", "Spam"))
        stored = self.db.session.get(self.models.Report, body["id"])
        self.assertEqual((stored.type, stored.target_id), ("comment", "1"))

    def test_report_does_not_reintroduce_legacy_column(self):
        self.assertNotIn("reports", self.models.Comment.__table__.columns)
        self.assertFalse(hasattr(self.models.Comment, "reports"))
        self.assertEqual(self.post("report").status_code, 201)
        comment = self.db.session.get(self.models.Comment, 1)
        from api.v1.views.comments import comment_to_dict
        self.assertEqual(comment_to_dict(comment)["reports"], 1)

    def test_theory_requires_title_and_content(self):
        for missing in ("title", "content"):
            payload = dict(self.PAYLOADS["theory"])
            del payload[missing]
            with self.subTest(missing=missing):
                self.assert_error(self.post("theory", payload), 400)

    def test_theory_rejects_wrong_field_types(self):
        for field in ("title", "content"):
            for value in (None, True, 1, [], {}):
                with self.subTest(field=field, value=value):
                    self.assert_error(self.post("theory", {
                        **self.PAYLOADS["theory"], field: value,
                    }), 400)

    def test_theory_rejects_empty_fields(self):
        for field in ("title", "content"):
            for value in ("", "   ", "\t\r\n"):
                with self.subTest(field=field, value=value):
                    self.assert_error(self.post("theory", {
                        **self.PAYLOADS["theory"], field: value,
                    }), 400)

    def test_theory_enforces_title_length_from_model(self):
        self.assertEqual(self.models.Theory.title.type.length, 200)
        self.assert_error(self.post("theory", {
            **self.PAYLOADS["theory"], "title": "t" * 201,
        }), 400)
        response = self.post("theory", {
            **self.PAYLOADS["theory"], "title": "  " + "t" * 200 + "  ",
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["theory"]["title"], "t" * 200)

    def test_theory_rejects_content_over_mysql_text_byte_limit(self):
        for value in ("x" * 65536, "\u00e9" * 32768):
            with self.subTest(bytes=len(value.encode("utf-8"))):
                self.assert_error(self.post("theory", {
                    **self.PAYLOADS["theory"], "content": value,
                }), 400)

    def test_theory_accepts_mysql_text_content_boundary(self):
        response = self.post("theory", {
            "title": "Evidence", "content": "x" * 65535,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.get_json()["theory"]["content"]), 65535)

    def test_theory_success_trims_fields_and_uses_server_identity(self):
        response = self.post("theory", {
            "title": "  Evidence  ", "content": "  Some evidence  ", "user_id": 2,
        })
        self.assertEqual(response.status_code, 201)
        body = response.get_json()["theory"]
        self.assertEqual((body["title"], body["content"], body["user_id"]), (
            "Evidence", "Some evidence", 1,
        ))
        self.assertEqual(self.db.session.get(self.models.Theory, body["id"]).content, "Some evidence")

    def test_all_text_fields_reject_invalid_unicode(self):
        fields = (("comment", "text"), ("report", "reason"), ("theory", "title"), ("theory", "content"))
        for route, field in fields:
            with self.subTest(route=route, field=field):
                self.assert_error(self.post(route, {
                    **self.PAYLOADS[route], field: "\ud800",
                }), 400)

    def test_all_three_create_routes_roll_back_add_failures(self):
        for route in self.CREATES:
            with self.subTest(route=route):
                count = self.model_for(route).query.count()
                with patch.object(self.db.session, "add", side_effect=SQLAlchemyError("private-sql-detail")):
                    with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                        self.assert_error(self.post(route), 500)
                        rollback.assert_called_once_with()
                self.assertEqual(self.model_for(route).query.count(), count)

    def test_all_three_create_routes_roll_back_commit_failures_and_recover(self):
        for route in self.CREATES:
            with self.subTest(route=route):
                count = self.model_for(route).query.count()
                with patch.object(self.db.session, "commit", side_effect=SQLAlchemyError("private-sql-detail")):
                    with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                        self.assert_error(self.post(route), 500)
                        rollback.assert_called_once_with()
                self.assertEqual(self.model_for(route).query.count(), count)
                self.assertEqual(self.post(route).status_code, 201)

    def test_likes_return_incremented_persisted_counter(self):
        for route in self.LIKES:
            with self.subTest(route=route):
                response = self.post(route)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(self.like_body(route, response)["likes"], 1)
                self.assertEqual(self.db.session.get(self.model_for(route), 1).likes, 1)

    def test_likes_allow_repeated_likes_from_same_user(self):
        for route in self.LIKES:
            with self.subTest(route=route):
                first = self.post(route)
                second = self.post(route)
                self.assertEqual((first.status_code, second.status_code), (200, 200))
                self.assertEqual((self.like_body(route, first)["likes"], self.like_body(route, second)["likes"]), (1, 2))

    def test_likes_never_parse_json(self):
        for route in self.LIKES:
            for raw in (None, '["invalid"]', "null", "{"):
                with self.subTest(route=route, raw=raw):
                    with patch.object(self.app.request_class, "get_json", side_effect=AssertionError("JSON forbidden")) as get_json:
                        self.assertEqual(self.post(route, raw=raw).status_code, 200)
                        get_json.assert_not_called()

    def test_likes_increment_database_value_despite_stale_orm_counter(self):
        for route in self.LIKES:
            with self.subTest(route=route):
                item = self.db.session.get(self.model_for(route), 1)
                set_committed_value(item, "likes", 999)
                response = self.post(route)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(self.like_body(route, response)["likes"], 1)
                self.assertEqual(self.db.session.get(self.model_for(route), 1).likes, 1)

    def test_likes_roll_back_update_failures(self):
        for route in self.LIKES:
            with self.subTest(route=route):
                with patch.object(self.db.session, "execute", side_effect=SQLAlchemyError("private-sql-detail")):
                    with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                        self.assert_error(self.post(route), 500)
                        rollback.assert_called_once_with()
                self.assertEqual(self.db.session.get(self.model_for(route), 1).likes, 0)

    def test_likes_roll_back_refresh_failures(self):
        for route in self.LIKES:
            with self.subTest(route=route):
                with patch.object(self.db.session, "refresh", side_effect=SQLAlchemyError("private-sql-detail")):
                    with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                        self.assert_error(self.post(route), 500)
                        rollback.assert_called_once_with()
                self.assertEqual(self.db.session.get(self.model_for(route), 1).likes, 0)

    def test_likes_roll_back_commit_failures_and_recover(self):
        for route in self.LIKES:
            with self.subTest(route=route):
                with patch.object(self.db.session, "commit", side_effect=SQLAlchemyError("private-sql-detail")):
                    with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                        self.assert_error(self.post(route), 500)
                        rollback.assert_called_once_with()
                self.assertEqual(self.db.session.get(self.model_for(route), 1).likes, 0)
                self.assertEqual(self.post(route).status_code, 200)

    def test_likes_resource_disappearing_before_update_is_404(self):
        for route in self.LIKES:
            with self.subTest(route=route):
                with patch.object(self.db.session, "execute", return_value=Mock(rowcount=0)):
                    with patch.object(self.db.session, "rollback", wraps=self.db.session.rollback) as rollback:
                        with patch.object(self.db.session, "commit") as commit:
                            self.assert_error(self.post(route), 404)
                            rollback.assert_called_once_with()
                            commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()
