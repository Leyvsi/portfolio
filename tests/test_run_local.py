"""Offline checks for the single-origin launcher: no socket or SQL access."""

import importlib
import socket
import sys
import types
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import Mock, patch
from xml.etree import ElementTree

from sqlalchemy.engine import Engine
from werkzeug.test import Client
from werkzeug.wrappers import Response


class LocalFrontendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guards = ExitStack()
        cls.addClassCleanup(cls.guards.close)
        for owner, name in (
            (socket, "create_connection"),
            (socket.socket, "connect"),
            (socket.socket, "connect_ex"),
            (socket.socket, "bind"),
            (socket.socket, "listen"),
            (Engine, "connect"),
            (Engine, "raw_connection"),
        ):
            cls.guards.enter_context(patch.object(
                owner, name, side_effect=AssertionError("Network/SQL forbidden")
            ))
        cls.launcher = importlib.import_module("run_local")

    def setUp(self):
        self.calls = []

        def api(environ, start_response):
            self.calls.append((environ["REQUEST_METHOD"], environ["PATH_INFO"]))
            return Response("API passthrough", status=404)(environ, start_response)

        self.api = api
        self.client = Client(self.launcher.create_local_app(api), Response)

    def test_root_serves_existing_homepage(self):
        response = self.client.get("/", buffered=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, (self.launcher.FRONTEND_ROOT / "index.html").read_bytes())
        self.assertEqual(self.calls, [])

    def test_html_css_and_js_are_served_on_the_same_origin(self):
        for name in ("index.html", "histoires.html", "coldcases.html", "dossier.html", "styles.css", "api.js", "app.js"):
            with self.subTest(file=name):
                response = self.client.get("/" + name, buffered=True)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, (self.launcher.FRONTEND_ROOT / name).read_bytes())

    def test_default_svg_is_served_and_is_only_a_neutral_placeholder(self):
        response = self.client.get("/images/default-story.svg", buffered=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("image/svg+xml", response.content_type)
        svg = ElementTree.fromstring(response.data)
        self.assertEqual(svg.attrib["viewBox"], "0 0 1200 675")
        self.assertEqual(svg.find("{http://www.w3.org/2000/svg}title").text, "Image à venir")
        self.assertEqual(svg.findall(".//{http://www.w3.org/2000/svg}image"), [])
        self.assertEqual(svg.findall(".//{http://www.w3.org/2000/svg}script"), [])

    def test_missing_image_is_a_404_without_creating_any_file(self):
        path = self.launcher.FRONTEND_ROOT / "images" / "absent-offline-test-file.webp"
        self.assertFalse(path.exists())
        self.assertEqual(self.client.get("/images/absent-offline-test-file.webp", buffered=True).status_code, 404)
        self.assertFalse(path.exists())

    def test_api_paths_and_methods_are_delegated_unchanged(self):
        for method in ("GET", "POST", "PATCH", "DELETE", "OPTIONS"):
            response = self.client.open("/api/v1/stories", method=method, buffered=True)
            self.assertEqual(response.data, b"API passthrough")
            self.assertEqual(self.calls[-1], (method, "/api/v1/stories"))

    def test_static_post_is_not_served_as_a_successful_file_response(self):
        self.assertEqual(self.client.post("/index.html", buffered=True).status_code, 404)
        self.assertEqual(self.calls[-1], ("POST", "/index.html"))

    def test_private_files_and_traversal_are_not_exposed(self):
        for path in ("/.env", "/run_local.py", "/backend/models.py", "/../.env", "/images/../../.env", "/images/../app.js", "/images/README.md", "/tests/images.test.cjs"):
            with self.subTest(path=path):
                response = self.client.get(path, buffered=True)
                self.assertEqual(response.status_code, 404)
                self.assertEqual(response.data, b"API passthrough")

    def test_main_prepares_one_loopback_server_without_starting_it_in_this_test(self):
        fake = types.ModuleType("index")
        fake.app = Mock()
        fake.app.wsgi_app = self.api
        with (
            patch.dict(sys.modules, {"index": fake}),
            patch.object(self.launcher.sys, "path", list(sys.path)),
            patch.object(self.launcher.os, "chdir") as change_directory,
            patch("dotenv.load_dotenv") as load_environment,
        ):
            self.launcher.main()
        change_directory.assert_called_once_with(self.launcher.PROJECT_ROOT)
        load_environment.assert_called_once_with(
            self.launcher.PROJECT_ROOT / ".env",
            encoding="utf-8-sig", override=False,
        )
        fake.app.run.assert_called_once_with(
            host="127.0.0.1", port=5000, debug=False, use_reloader=False
        )
        self.assertIsNot(fake.app.wsgi_app, self.api)


if __name__ == "__main__":
    unittest.main()
