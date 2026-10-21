"""OpenAPI/Flask contract tests; guarded SQLite memory, no external access."""

from collections import Counter
import json
from pathlib import Path
import re
import unittest

from werkzeug.routing import IntegerConverter

import test_reports as report_suite


class SwaggerTests(unittest.TestCase):
    METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}
    AUTH_REQUIRED = {
        ("/me", "get"), ("/users", "get"), ("/admin/reports", "get"),
        ("/proposals", "get"), ("/admin/users/{username}/ban", "delete"),
        ("/votes/{story_id}", "post"), ("/reports", "post"),
        ("/stories/{story_id}/comments", "post"),
        ("/comments/{comment_id}/like", "post"),
        ("/comments/{comment_id}/report", "post"),
        ("/stories/{story_id}/theories", "post"),
        ("/theories/{theory_id}/like", "post"), ("/proposals", "post"),
    }
    ADMIN_REQUIRED = {
        ("/users", "get"), ("/proposals", "get"), ("/admin/reports", "get"),
        ("/admin/users/{username}/ban", "delete"),
    }
    OPTIONAL_AUTH = {("/users", "post"), ("/logout", "post")}
    INPUTS = {
        "/login": {"username": "reader", "password": "Swagger-Test9!"},
        "/users": {"username": "swagger-reader", "email": "swagger-reader@example.invalid", "password": "A-goodPass9!"},
        "/stories/{story_id}/comments": {"text": "A comment"},
        "/comments/{comment_id}/report": {"reason": "Spam"},
        "/stories/{story_id}/theories": {"title": "A theory", "content": "Evidence"},
        "/proposals": {"title": "A proposal", "content": "Evidence"},
        "/reports": {"type": "comment", "target_id": "1", "reason": "Spam"},
    }

    @classmethod
    def setUpClass(cls):
        report_suite.ReportTests.setUpClass.__func__(cls)
        cls.document_path = Path(__file__).resolve().parents[1] / "api/v1/swagger.json"
        cls.document = json.loads(cls.document_path.read_text(encoding="utf-8"))
        with cls.app.app_context():
            cls.db.session.get(cls.models.User, 1).set_password("Swagger-Test9!")
            cls.db.session.add_all([
                cls.models.User(
                    id=3, username="admin", email="admin@example.invalid",
                    password_hash="unused", is_admin=True, is_banned=False,
                ),
                cls.models.Theory(id=1, story_id=1, user_id=1, title="Theory", content="Evidence"),
                cls.models.Proposal(id=1, user_id=1, title="Proposal", content="Evidence", status="pending"),
                cls.models.Report(id=1, type="comment", target_id="1", reason="Spam"),
                cls.models.ColdCaseUpdate(id=1, story_id=1, content="Update"),
            ])
            cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        report_suite.ReportTests.tearDownClass.__func__(cls)

    authenticate = report_suite.ReportTests.authenticate

    def setUp(self):
        report_suite.ReportTests.setUp(self)

    def tearDown(self):
        self.db.session.rollback()
        self.models.Vote.query.delete()
        self.models.Report.query.filter(self.models.Report.id > 1).delete()
        self.models.Comment.query.filter(self.models.Comment.id > 1).delete()
        self.models.Theory.query.filter(self.models.Theory.id > 1).delete()
        self.models.Proposal.query.filter(self.models.Proposal.id > 1).delete()
        self.models.User.query.filter(self.models.User.id > 3).delete()
        self.models.Comment.query.update({self.models.Comment.likes: 0})
        self.models.Theory.query.update({self.models.Theory.likes: 0})
        self.db.session.commit()
        self.db.session.remove()

    def documented(self):
        return {
            (path, method): operation
            for path, item in self.document["paths"].items()
            for method, operation in item.items()
            if method in self.METHODS
        }

    def real(self):
        operations = {}
        for rule in self.app.url_map.iter_rules():
            if not rule.rule.startswith("/api/v1/"):
                continue
            path = re.sub(
                r"<(?:[^:<>]+:)?([^<>]+)>",
                lambda match: "{" + match.group(1) + "}",
                rule.rule[len("/api/v1"):],
            )
            for method in rule.methods - {"HEAD", "OPTIONS"}:
                operations[(path, method.lower())] = rule
        return operations

    def resolve(self, node):
        while "$ref" in node:
            target = self.document
            self.assertTrue(node["$ref"].startswith("#/"), "External reference forbidden")
            for part in node["$ref"][2:].split("/"):
                target = target[part.replace("~1", "/").replace("~0", "~")]
            node = target
        return node

    def body_schema(self, path, method="post"):
        return self.resolve(self.document["paths"][path][method]["requestBody"]["content"]["application/json"]["schema"])

    def response_schema(self, path, method, status):
        response = self.resolve(self.document["paths"][path][method]["responses"][str(status)])
        return self.resolve(response["content"]["application/json"]["schema"])

    def call(self, path, method, *, user_id=1, csrf=True):
        self.client = self.app.test_client()
        if user_id is not None:
            self.authenticate(user_id)
        actual = "/api/v1" + path.format(
            story_id=1, theory_id=1, comment_id=1, case_id=1,
            slug="audit-story", username="banned",
        )
        kwargs = {"headers": {"X-CSRF-Token": "reports-csrf"} if csrf else {}}
        if method == "post" and path in self.INPUTS:
            kwargs["json"] = self.INPUTS[path]
        return self.client.open(actual, method=method.upper(), **kwargs)

    def assert_matches_schema(self, value, schema):
        schema = self.resolve(schema)
        if schema.get("nullable") and value is None:
            return
        kind = schema.get("type")
        if kind == "object":
            self.assertIsInstance(value, dict)
            self.assertTrue(set(schema.get("required", [])) <= set(value))
            for name, child in schema.get("properties", {}).items():
                if name in value:
                    self.assert_matches_schema(value[name], child)
        elif kind == "array":
            self.assertIsInstance(value, list)
            for item in value:
                self.assert_matches_schema(item, schema["items"])
        elif kind == "integer":
            self.assertIs(type(value), int)
        elif kind == "boolean":
            self.assertIs(type(value), bool)
        elif kind == "string":
            self.assertIsInstance(value, str)
        if "enum" in schema:
            self.assertIn(value, schema["enum"])
        if "minimum" in schema:
            self.assertGreaterEqual(value, schema["minimum"])

    def test_document_is_valid_json_without_duplicate_keys(self):
        def unique(pairs):
            result = {}
            for key, value in pairs:
                self.assertNotIn(key, result)
                result[key] = value
            return result
        parsed = json.loads(self.document_path.read_text(encoding="utf-8"), object_pairs_hook=unique)
        self.assertEqual(parsed, self.document)

    def test_openapi_version_and_api_prefix(self):
        self.assertEqual(self.document["openapi"], "3.0.3")
        self.assertEqual(self.document["servers"], [{"url": "/api/v1"}])

    def test_every_documented_operation_exists_in_flask(self):
        self.assertEqual(set(self.documented()) - set(self.real()), set())

    def test_every_flask_api_operation_is_documented(self):
        self.assertEqual(set(self.real()) - set(self.documented()), set())

    def test_obsolete_coldcase_theory_route_is_absent(self):
        self.assertNotIn("/coldcases/{case_id}/theories", self.document["paths"])

    def test_http_methods_match_for_every_path(self):
        for path, item in self.document["paths"].items():
            with self.subTest(path=path):
                actual = {method for real_path, method in self.real() if real_path == path}
                self.assertEqual(set(item) & self.METHODS, actual)

    def test_path_parameters_match_flask_names_and_types(self):
        for key, rule in self.real().items():
            with self.subTest(operation=key):
                parameters = self.documented()[key].get("parameters", [])
                documented = {parameter["name"]: parameter for parameter in parameters if parameter["in"] == "path"}
                self.assertEqual(set(documented), set(rule._converters))
                for name, converter in rule._converters.items():
                    self.assertTrue(documented[name]["required"])
                    expected = "integer" if isinstance(converter, IntegerConverter) else "string"
                    self.assertEqual(documented[name]["schema"]["type"], expected)

    def test_vote_documents_201_and_409(self):
        codes = self.document["paths"]["/votes/{story_id}"]["post"]["responses"]
        self.assertIn("201", codes)
        self.assertIn("409", codes)
        self.assertNotIn("200", codes)

    def test_stats_documents_exact_counter_names(self):
        schema = self.response_schema("/stats", "get", 200)
        self.assertEqual(set(schema["properties"]), {"users", "comments", "reports"})
        self.assertEqual(set(schema["required"]), {"users", "comments", "reports"})

    def test_stats_500_documents_error_without_counters(self):
        schema = self.response_schema("/stats", "get", 500)
        self.assertEqual(set(schema["required"]), {"status", "message"})
        self.assertTrue({"users", "comments", "reports"}.isdisjoint(schema["properties"]))

    def test_ban_is_not_described_as_deletion(self):
        operation = self.document["paths"]["/admin/users/{username}/ban"]["delete"]
        text = (operation["summary"] + " " + operation["description"]).lower()
        self.assertNotRegex(text, r"supprim|suppression|effac|delet")
        self.assertIn("is_banned=true", text)
        self.assertIn("idempotente", text)

    def test_generic_report_type_is_comment_only_and_target_is_string(self):
        schema = self.body_schema("/reports")
        self.assertEqual(set(schema["required"]), {"type", "target_id", "reason"})
        self.assertEqual(schema["properties"]["type"]["enum"], ["comment"])
        self.assertEqual(schema["properties"]["target_id"]["type"], "string")

    def test_cookie_and_csrf_security_schemes_match_runtime(self):
        schemes = self.document["components"]["securitySchemes"]
        self.assertEqual((schemes["cookieAuth"]["type"], schemes["cookieAuth"]["in"], schemes["cookieAuth"]["name"]), (
            "apiKey", "cookie", self.app.config["SESSION_COOKIE_NAME"],
        ))
        self.assertEqual((schemes["csrfToken"]["type"], schemes["csrfToken"]["in"], schemes["csrfToken"]["name"]), (
            "apiKey", "header", "X-CSRF-Token",
        ))

    def test_session_requirements_match_actual_permissions(self):
        for key, operation in self.documented().items():
            with self.subTest(operation=key):
                expected = "required" if key in self.AUTH_REQUIRED else ("optional" if key in self.OPTIONAL_AUTH else "public")
                self.assertEqual(operation["x-session-auth"], expected)
                self.assertEqual(operation["x-admin-required"], key in self.ADMIN_REQUIRED)
                if expected == "public":
                    self.assertEqual(operation["security"], [])
                else:
                    requirements = {"cookieAuth": []}
                    if key[1] in {"post", "put", "patch", "delete"}:
                        requirements["csrfToken"] = []
                    self.assertIn(requirements, operation["security"])
                    if expected == "optional":
                        self.assertIn({}, operation["security"])

    def test_login_is_explicitly_exempt_from_csrf(self):
        operation = self.document["paths"]["/login"]["post"]
        self.assertEqual(operation["security"], [])
        self.assertIn("exempte de csrf", operation["description"].lower())

    def test_optional_session_routes_do_not_claim_mandatory_auth(self):
        self.assertNotIn("401", self.document["paths"]["/logout"]["post"]["responses"])
        for path, method in self.OPTIONAL_AUTH:
            self.assertIn({}, self.document["paths"][path][method]["security"])

    def test_request_body_fields_match_real_creation_contracts(self):
        expected = {
            "/login": {"username", "password"},
            "/users": {"username", "email", "password"},
            "/stories/{story_id}/comments": {"text"},
            "/comments/{comment_id}/report": {"reason"},
            "/stories/{story_id}/theories": {"title", "content"},
            "/proposals": {"title", "content"}, "/reports": {"type", "target_id", "reason"},
        }
        for path, fields in expected.items():
            with self.subTest(path=path):
                body = self.document["paths"][path]["post"]["requestBody"]
                self.assertTrue(body["required"])
                schema = self.body_schema(path)
                self.assertEqual(schema["type"], "object")
                self.assertEqual(set(schema["required"]), fields)

    def test_votes_likes_and_logout_do_not_require_json(self):
        for path in ("/votes/{story_id}", "/comments/{comment_id}/like", "/theories/{theory_id}/like", "/logout"):
            with self.subTest(path=path):
                self.assertNotIn("requestBody", self.document["paths"][path]["post"])

    def test_documented_lengths_match_models_and_text_validation(self):
        signup = self.body_schema("/users")["properties"]
        self.assertEqual(signup["username"]["maxLength"], self.models.User.username.type.length)
        self.assertEqual(signup["email"]["maxLength"], self.models.User.email.type.length)
        for path, model in (("/proposals", self.models.Proposal), ("/stories/{story_id}/theories", self.models.Theory)):
            schema = self.body_schema(path)["properties"]
            self.assertEqual(schema["title"]["maxLength"], model.title.type.length)
            self.assertEqual(schema["content"]["x-max-utf8-bytes"], 65535)
        self.assertEqual(self.body_schema("/stories/{story_id}/comments")["properties"]["text"]["x-max-utf8-bytes"], 65535)
        self.assertEqual(self.body_schema("/comments/{comment_id}/report")["properties"]["reason"]["x-max-utf8-bytes"], 65535)
        self.assertNotIn("maxLength", self.body_schema("/reports")["properties"]["reason"])

    def test_framework_errors_document_json_and_allow_header(self):
        for code in ("400", "404", "405", "415", "500"):
            response = self.resolve(self.document["x-framework-errors"][code])
            self.assertIn("application/json", response["content"])
        error = self.document["components"]["schemas"]["ApiError"]
        self.assertEqual(set(error["required"]), {"status", "message"})
        response = self.resolve(self.document["x-framework-errors"]["405"])
        self.assertIn("Allow", response["headers"])

    def test_all_schema_and_response_references_are_local_and_resolvable(self):
        def check(node):
            if isinstance(node, dict):
                if "$ref" in node:
                    self.resolve(node)
                for child in node.values():
                    check(child)
            elif isinstance(node, list):
                for child in node:
                    check(child)
        check(self.document)

    def test_operation_ids_are_unique(self):
        identifiers = [operation["operationId"] for operation in self.documented().values()]
        self.assertTrue(all(isinstance(identifier, str) and identifier for identifier in identifiers))
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_documented_status_codes_match_existing_contracts(self):
        expected = {
            ("/login", "post"): {200,400,401,403,500}, ("/me", "get"): {200,401,403,500},
            ("/logout", "post"): {200,403,500}, ("/users", "get"): {200,401,403,500},
            ("/users", "post"): {201,400,401,403,500},
            ("/admin/users/{username}/ban", "delete"): {200,401,403,404,500},
            ("/stories", "get"): {200,500}, ("/stories/slug/{slug}", "get"): {200,404,500},
            ("/votes/{story_id}", "post"): {201,401,403,404,409,500},
            ("/coldcases/{case_id}/updates", "get"): {200,404,500},
            ("/stories/{story_id}/comments", "get"): {200,404,500},
            ("/stories/{story_id}/comments", "post"): {201,400,401,403,404,500},
            ("/comments/{comment_id}/like", "post"): {200,401,403,404,500},
            ("/comments/{comment_id}/report", "post"): {201,400,401,403,404,500},
            ("/stories/{story_id}/theories", "get"): {200,404,500},
            ("/stories/{story_id}/theories", "post"): {201,400,401,403,404,500},
            ("/theories/{theory_id}/like", "post"): {200,401,403,404,500},
            ("/proposals", "get"): {200,401,403,500}, ("/proposals", "post"): {201,400,401,403,500},
            ("/reports", "post"): {201,400,401,403,404,500},
            ("/admin/reports", "get"): {200,401,403,500}, ("/stats", "get"): {200,500},
            ("/swagger.json", "get"): {200,404,500}, ("/swagger", "get"): {200,500},
        }
        self.assertEqual(set(expected), set(self.documented()))
        for key, codes in expected.items():
            with self.subTest(operation=key):
                self.assertEqual({int(code) for code in self.documented()[key]["responses"]}, codes)

    def test_success_responses_match_documented_shapes_for_all_operations(self):
        for (path, method), operation in self.documented().items():
            with self.subTest(path=path, method=method):
                response = self.call(path, method, user_id=3 if (path, method) in self.ADMIN_REQUIRED else 1)
                status = next(int(code) for code in operation["responses"] if code.startswith("2"))
                self.assertEqual(response.status_code, status, response.get_data(as_text=True))
                if path == "/swagger":
                    self.assertEqual(response.mimetype, "text/html")
                else:
                    self.assertEqual(response.mimetype, "application/json")
                    self.assert_matches_schema(response.get_json(), self.response_schema(path, method, status))

    def test_documented_protected_operations_reject_anonymous_requests(self):
        for path, method in self.AUTH_REQUIRED:
            with self.subTest(path=path, method=method):
                self.assertEqual(self.call(path, method, user_id=None).status_code, 401)

    def test_documented_admin_operations_reject_nonadmin(self):
        for path, method in self.ADMIN_REQUIRED:
            with self.subTest(path=path, method=method):
                self.assertEqual(self.call(path, method).status_code, 403)

    def test_documented_authenticated_writes_require_csrf(self):
        for path, method in self.AUTH_REQUIRED | self.OPTIONAL_AUTH:
            if method in {"post", "put", "patch", "delete"}:
                with self.subTest(path=path, method=method):
                    self.assertEqual(self.call(path, method, csrf=False).status_code, 403)

    def test_optional_auth_routes_accept_anonymous_requests(self):
        self.assertEqual(self.call("/users", "post", user_id=None, csrf=False).status_code, 201)
        self.assertEqual(self.call("/logout", "post", user_id=None, csrf=False).status_code, 200)

    def test_documented_public_operations_work_without_session(self):
        for (path, method), operation in self.documented().items():
            if operation["x-session-auth"] == "public":
                with self.subTest(path=path, method=method):
                    response = self.call(path, method, user_id=None, csrf=False)
                    self.assertEqual(response.status_code, 200)

    def test_swagger_json_endpoint_returns_the_document(self):
        response = self.client.get("/api/v1/swagger.json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(response.get_json(), self.document)

    def test_swagger_ui_serves_html_without_fetching_cdn(self):
        response = self.client.get("/api/v1/swagger")
        self.assertEqual(response.status_code, 200)
        self.assertIn("SwaggerUIBundle", response.get_data(as_text=True))
        self.assertIn("/api/v1/swagger.json", response.get_data(as_text=True))

    def test_route_method_pairs_remain_unique(self):
        pairs = Counter(
            (rule.rule, method)
            for rule in self.app.url_map.iter_rules()
            for method in rule.methods - {"HEAD", "OPTIONS"}
        )
        self.assertTrue(all(count == 1 for count in pairs.values()))


if __name__ == "__main__":
    unittest.main()
