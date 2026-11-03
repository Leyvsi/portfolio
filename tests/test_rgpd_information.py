"""Contrats HTML et non-publication du brouillon, sans serveur ni base réelle."""

from html.parser import HTMLParser
from pathlib import Path
import unittest
from tempfile import TemporaryDirectory

from werkzeug.test import Client
from werkzeug.wrappers import Response

from run_local import create_local_app


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
PRIVATE_POLICY_NAME = "confidentialite-interne.html"
PAGES = {
    "inscription.html": ("signup-form", "signup-data-notice"),
    "theories.html": ("theory-form", "theory-data-notice"),
    "proposer-histoire.html": ("proposal-form", "proposal-data-notice"),
}


class Document(HTMLParser):
    """Lire les éléments utiles sans exécuter de script ou charger une ressource."""

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.stack = []
        self.feed(content)
        self.close()
        if self.stack:
            raise AssertionError("Élément HTML non fermé")

    def handle_starttag(self, tag, attributes):
        node = {"tag": tag, "attrs": dict(attributes), "text": "",
                "position": len(self.nodes), "parents": list(self.stack)}
        self.nodes.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack or self.stack[-1]["tag"] != tag:
            raise AssertionError("Fermeture HTML incohérente : " + tag)
        self.stack.pop()

    def handle_data(self, text):
        for node in self.stack:
            node["text"] += text

    def by_id(self, identifier):
        found = [n for n in self.nodes if n["attrs"].get("id") == identifier]
        if len(found) != 1:
            raise AssertionError("Identifiant absent ou dupliqué : " + identifier)
        return found[0]

    def fields(self, form_id):
        form = self.by_id(form_id)
        return [n for n in self.nodes if n["tag"] in {"input", "select", "textarea"}
                and form in n["parents"]]


def document(name):
    return Document((FRONTEND / name).read_text(encoding="utf-8"))


def offline_api(environ, start_response):
    return Response("API passthrough", status=404)(environ, start_response)


class PrivacyInformationTests(unittest.TestCase):
    def test_signup_preserves_collected_fields_and_password_requirements(self):
        page = document("inscription.html")
        fields = page.fields("signup-form")
        self.assertEqual([n["attrs"]["name"] for n in fields],
                         ["username", "email", "password"])
        expected = [("pseudo", "text", "100", "username"),
                    ("email", "email", "150", "email"),
                    ("password", "password", "50", "new-password")]
        for field, (identifier, kind, maximum, autocomplete) in zip(fields, expected):
            attrs = field["attrs"]
            self.assertEqual((attrs["id"], attrs["type"], attrs["maxlength"],
                              attrs["autocomplete"]),
                             (identifier, kind, maximum, autocomplete))
            self.assertIn("required", attrs)
            self.assertNotIn("disabled", attrs)
        self.assertEqual(fields[-1]["attrs"]["minlength"], "8")
        self.assertEqual(fields[-1]["attrs"]["aria-describedby"], "signup-password-help")
        self.assertTrue(page.by_id("signup-password-help")["text"].strip())

    def test_theory_preserves_fields_and_loading_controls(self):
        page = document("theories.html")
        fields = page.fields("theory-form")
        self.assertEqual([n["attrs"]["name"] for n in fields],
                         ["story_id", "title", "content"])
        self.assertEqual([n["tag"] for n in fields], ["select", "input", "textarea"])
        self.assertTrue(all("required" in n["attrs"] for n in fields))
        self.assertIn("disabled", fields[0]["attrs"])
        self.assertEqual(fields[1]["attrs"]["maxlength"], "200")
        self.assertEqual(page.by_id("theory-form")["attrs"]["aria-busy"], "true")
        self.assertIn("disabled", next(n for n in page.nodes if n["tag"] == "button"
                                      and n["attrs"].get("type") == "submit")["attrs"])

    def test_proposal_preserves_fields_and_category_choices(self):
        page = document("proposer-histoire.html")
        fields = page.fields("proposal-form")
        self.assertEqual([n["attrs"]["name"] for n in fields],
                         ["title", "category", "content"])
        self.assertTrue(all("required" in n["attrs"] for n in fields))
        self.assertTrue(all("disabled" not in n["attrs"] for n in fields))
        self.assertEqual(fields[0]["attrs"]["maxlength"], "200")
        self.assertEqual([n["text"].strip() for n in page.nodes if n["tag"] == "option"],
                         ["Histoire", "Cold case"])

    def test_notices_are_visible_before_fields_and_describe_submission(self):
        for name, (form_id, notice_id) in PAGES.items():
            with self.subTest(page=name):
                page = document(name)
                ids = [n["attrs"]["id"] for n in page.nodes if "id" in n["attrs"]]
                self.assertEqual(len(ids), len(set(ids)))
                notice = page.by_id(notice_id)
                self.assertTrue(notice["text"].strip())
                self.assertNotIn("hidden", notice["attrs"])
                self.assertNotIn("style", notice["attrs"])
                self.assertLess(notice["position"], page.fields(form_id)[0]["position"])
                form = page.by_id(form_id)
                self.assertEqual(form["attrs"]["method"], "post")
                self.assertEqual(form["attrs"]["aria-describedby"], notice_id)
                submit = next(n for n in page.nodes if n["tag"] == "button"
                              and n["attrs"].get("type") == "submit")
                self.assertEqual(submit["attrs"]["aria-describedby"], notice_id)
                self.assertNotIn("tabindex", submit["attrs"])
                self.assertNotIn("required", notice["attrs"])

    def test_assets_and_existing_navigation_add_no_tracking_or_consent_control(self):
        for name in PAGES:
            with self.subTest(page=name):
                page = document(name)
                scripts = [n["attrs"].get("src") for n in page.nodes if n["tag"] == "script"]
                expected = ["api.js", "app.js"]
                if name == "theories.html":
                    expected.append("theories-list.js")
                self.assertEqual(scripts, expected)
                self.assertFalse(any(n["tag"] == "input" and
                                     n["attrs"].get("type") in {"checkbox", "hidden"}
                                     for n in page.nodes))
                self.assertFalse(any(n["tag"] in {"iframe", "object", "embed"}
                                     for n in page.nodes))
                for anchor in [n for n in page.nodes if n["tag"] == "a"]:
                    self.assertTrue(anchor["text"].strip())
                    self.assertNotIn("tabindex", anchor["attrs"])

    def test_unfinished_policy_stays_outside_public_files_and_links(self):
        self.assertFalse((FRONTEND / PRIVATE_POLICY_NAME).exists())
        for path in FRONTEND.glob("*.html"):
            page = document(path.name)
            for anchor in [n for n in page.nodes if n["tag"] == "a"]:
                href = anchor["attrs"].get("href", "")
                self.assertNotIn(PRIVATE_POLICY_NAME, href)
                self.assertFalse(href.startswith(("../docs/", "/docs/")))

    def test_internal_document_fixture_cannot_be_downloaded_through_the_launcher(self):
        with TemporaryDirectory(prefix="portfolio-private-fixture-") as directory:
            project = Path(directory)
            frontend = project / "frontend"
            frontend.mkdir()
            private = project / "docs" / "soutenance"
            private.mkdir(parents=True)
            (private / PRIVATE_POLICY_NAME).write_text("<p>Private synthetic fixture</p>", encoding="utf-8")
            client = Client(create_local_app(offline_api, frontend_root=frontend), Response)
            for path in ("/" + PRIVATE_POLICY_NAME, "/docs/soutenance/" + PRIVATE_POLICY_NAME,
                         "/../docs/soutenance/" + PRIVATE_POLICY_NAME,
                         "/images/../../docs/soutenance/" + PRIVATE_POLICY_NAME):
                for method in ("GET", "HEAD"):
                    with self.subTest(path=path, method=method):
                        response = client.open(path, method=method, buffered=True)
                        self.assertEqual(response.status_code, 404)

    def test_public_forms_are_served_with_notices_without_running_a_server(self):
        client = Client(create_local_app(offline_api), Response)
        for name, (form_id, notice_id) in PAGES.items():
            with self.subTest(page=name):
                response = client.get("/" + name, buffered=True)
                self.assertEqual(response.status_code, 200)
                page = Document(response.data.decode("utf-8"))
                self.assertTrue(page.by_id(notice_id)["text"].strip())
                self.assertEqual(page.by_id(form_id)["attrs"]["method"], "post")


if __name__ == "__main__":
    unittest.main()
