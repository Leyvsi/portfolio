"""Contrats HTML et non-publication du brouillon, sans serveur ni base réelle."""

from html.parser import HTMLParser
from pathlib import Path
import unittest
from contextlib import ExitStack
from unittest.mock import patch
import socket
import tempfile

from sqlalchemy.engine import Engine

from werkzeug.test import Client
from werkzeug.wrappers import Response

from run_local import create_local_app


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
# Noms de sondes : aucun texte juridique interne n'est nécessaire au clone.
PRIVATE_PROBES = ("information-interne-test.html", "politique-interne-test.html")
PAGES = {
    "connexion.html": ("login-form", "login-data-notice"),
    "admin-connexion.html": ("login-form", "admin-login-data-notice"),
    "inscription.html": ("signup-form", "signup-data-notice"),
    "theories.html": ("theory-form", "theory-data-notice"),
    "proposer-histoire.html": ("proposal-form", "proposal-data-notice"),
}
FORMS = [(name, form, notice) for name, (form, notice) in PAGES.items()] + [
    ("dossier.html", "comment-form", "comment-data-notice"),
    ("dossier.html", "report-form", "report-data-notice"),
]
ALL_PAGES = (*PAGES, "dossier.html")


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
    @classmethod
    def setUpClass(cls):
        cls.guards = ExitStack()
        cls.addClassCleanup(cls.guards.close)
        for owner, name in ((socket, "create_connection"), (socket.socket, "connect"),
                            (socket.socket, "connect_ex"), (socket.socket, "bind"),
                            (socket.socket, "listen"), (Engine, "connect"),
                            (Engine, "raw_connection")):
            cls.guards.enter_context(patch.object(owner, name,
                side_effect=AssertionError("Network/SQL forbidden")))

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
        for name, form_id, notice_id in FORMS:
            with self.subTest(page=name, form=form_id):
                page = document(name)
                ids = [n["attrs"]["id"] for n in page.nodes if "id" in n["attrs"]]
                self.assertEqual(len(ids), len(set(ids)))
                notice = page.by_id(notice_id)
                self.assertTrue(notice["text"].strip())
                self.assertNotIn("hidden", notice["attrs"])
                self.assertNotIn("style", notice["attrs"])
                form = page.by_id(form_id)
                self.assertIn(form, notice["parents"])
                self.assertLess(notice["position"], page.fields(form_id)[0]["position"])
                self.assertIn(notice_id, form["attrs"].get("aria-describedby", "").split())
                # Les formulaires dynamiques de dossier gardent leur contrat existant.
                self.assertEqual(form["attrs"].get("method"), None if name == "dossier.html" else "post")
                submit = next(n for n in page.nodes if n["tag"] == "button"
                              and n["attrs"].get("type") == "submit" and form in n["parents"])
                self.assertIn(notice_id, submit["attrs"].get("aria-describedby", "").split())
                self.assertNotIn("tabindex", submit["attrs"])
                self.assertNotIn("required", notice["attrs"])

    def test_login_fields_roles_and_autocomplete_are_preserved(self):
        for name in ("connexion.html", "admin-connexion.html"):
            with self.subTest(page=name):
                page = document(name)
                fields = page.fields("login-form")
                self.assertEqual([n["attrs"]["name"] for n in fields], ["username", "password"])
                self.assertEqual([n["attrs"]["autocomplete"] for n in fields], ["username", "current-password"])
                self.assertEqual([n["attrs"]["type"] for n in fields], ["text", "password"])
                self.assertTrue(all("required" in n["attrs"] for n in fields))
                self.assertEqual(page.by_id("login-form")["attrs"].get("data-admin"),
                                 "true" if name.startswith("admin-") else None)

    def test_comment_report_and_loading_controls_are_preserved(self):
        page = document("dossier.html")
        for form_id, field_id, button_id, name in (
            ("comment-form", "comment-text", "comment-send", "text"),
            ("report-form", "report-reason", "report-send", "reason"),
        ):
            fields = page.fields(form_id)
            self.assertEqual(len(fields), 1)
            self.assertEqual(fields[0]["attrs"]["id"], field_id)
            self.assertEqual(fields[0]["attrs"]["name"], name)
            self.assertIn("required", fields[0]["attrs"])
            self.assertIn("disabled", fields[0]["attrs"])
            self.assertIn("disabled", page.by_id(button_id)["attrs"])
            self.assertIn("contribution-limit", fields[0]["attrs"]["aria-describedby"].split())
        self.assertIn("hidden", page.by_id("report-form")["attrs"])
        self.assertIn("hidden", page.by_id("story-comments")["attrs"])

    def test_notices_explain_distinct_audiences_and_session_without_promises(self):
        for name, (_, notice_id) in PAGES.items():
            notice = document(name).by_id(notice_id)["text"]
            self.assertIn("préparation", notice)
        self.assertIn("hachage", document("inscription.html").by_id("signup-data-notice")["text"])
        for name, notice_id in (("connexion.html", "login-data-notice"),
                                ("admin-connexion.html", "admin-login-data-notice")):
            self.assertIn("cookie de session", document(name).by_id(notice_id)["text"])
        self.assertIn("sans connexion", document("theories.html").by_id("theory-data-notice")["text"])
        self.assertIn("ne publie pas automatiquement", document("proposer-histoire.html").by_id("proposal-data-notice")["text"])
        page = document("dossier.html")
        self.assertIn("sans connexion", page.by_id("comment-data-notice")["text"])
        self.assertIn("administration", page.by_id("report-data-notice")["text"])
        self.assertIn("ne masque pas automatiquement", page.by_id("report-data-notice")["text"])

    def test_like_information_precedes_controls_and_names_account_link(self):
        page = document("dossier.html")
        for target_id, notice_id in (("story-like", "story-like-data-notice"),
                                     ("comments-list", "comment-like-data-notice")):
            target, notice = page.by_id(target_id), page.by_id(notice_id)
            self.assertLess(notice["position"], target["position"])
            self.assertIn(notice_id, target["attrs"]["aria-describedby"].split())
            self.assertIn("compte", notice["text"])
            self.assertIn("retrait", notice["text"])
            self.assertNotIn("hidden", notice["attrs"])

    def test_assets_and_navigation_add_no_tracking_or_consent_control(self):
        for name in ALL_PAGES:
            with self.subTest(page=name):
                page = document(name)
                scripts = [n["attrs"].get("src") for n in page.nodes if n["tag"] == "script"]
                expected = (["api.js", "likes.js", "comments.js", "app.js"]
                            if name == "dossier.html" else ["api.js", "app.js"])
                if name == "theories.html":
                    expected.append("theories-list.js")
                self.assertEqual(scripts, expected)
                self.assertFalse(any(n["tag"] == "input" and n["attrs"].get("type")
                                     in {"checkbox", "hidden"} for n in page.nodes))
                self.assertFalse(any(n["tag"] in {"iframe", "object", "embed"} for n in page.nodes))
                for anchor in (n for n in page.nodes if n["tag"] == "a"):
                    self.assertTrue(anchor["text"].strip())
                    self.assertNotIn("tabindex", anchor["attrs"])

    def test_unfinished_policies_stay_outside_public_files_and_links(self):
        self.assertFalse((FRONTEND / "confidentialite.html").exists())
        for name in PRIVATE_PROBES:
            self.assertFalse((FRONTEND / name).exists())
        for path in FRONTEND.glob("*.html"):
            for anchor in (n for n in document(path.name).nodes if n["tag"] == "a"):
                href = anchor["attrs"].get("href", "")
                self.assertNotIn("confidentialite", href.lower())
                self.assertFalse(href.startswith(("../docs/", "/docs/")))

    def test_synthetic_private_documents_are_real_files_outside_the_public_root(self):
        # Fixtures synthétiques jetables, sans copier un document ou une donnée privée.
        with tempfile.TemporaryDirectory(prefix="lpe-rgpd-fixture-") as temporary:
            root = Path(temporary)
            public = root / "frontend"
            internal = root / "docs" / "soutenance"
            public.mkdir()
            internal.mkdir(parents=True)
            for name in PRIVATE_PROBES:
                fixture = internal / name
                fixture.write_text("<p>MARQUEUR_INTERNE_SYNTHETIQUE</p>", encoding="utf-8")
                self.assertTrue(fixture.is_file())
                self.assertFalse((public / name).exists())

    def test_internal_drafts_cannot_be_downloaded_through_either_launcher(self):
        import tools.recette_lot6g4 as recipe
        with tempfile.TemporaryDirectory(prefix="lpe-rgpd-http-") as temporary:
            root = Path(temporary)
            public = root / "frontend"
            internal = root / "docs" / "soutenance"
            public.mkdir()
            internal.mkdir(parents=True)
            for name in PRIVATE_PROBES:
                (internal / name).write_text("<p>MARQUEUR_INTERNE_SYNTHETIQUE</p>", encoding="utf-8")
            # Le kit compose le lanceur sans argument : détourner ce point de
            # composition vers le même frontend temporaire, pas vers le dépôt.
            factory = lambda api: create_local_app(api, frontend_root=public)
            with patch("run_local.create_local_app", side_effect=factory):
                kit = recipe.public_application(offline_api)
            for application, status in ((factory(offline_api), 404), (kit, 403)):
                client = Client(application, Response)
                for name in PRIVATE_PROBES:
                    for path in ("/" + name, "/docs/soutenance/" + name,
                                 "/../docs/soutenance/" + name,
                                 "/images/../../docs/soutenance/" + name):
                        for method in ("GET", "HEAD"):
                            with self.subTest(path=path, method=method, status=status):
                                response = client.open(path, method=method, buffered=True)
                                self.assertEqual(response.status_code, status)
                                self.assertNotIn(b"MARQUEUR_INTERNE_SYNTHETIQUE", response.data)

    def test_public_forms_are_served_with_notices_without_a_server(self):
        from tools.recette_lot6g4 import public_application
        for application in (create_local_app(offline_api), public_application(offline_api)):
            client = Client(application, Response)
            for name, form_id, notice_id in FORMS:
                with self.subTest(page=name, form=form_id):
                    response = client.get("/" + name, buffered=True)
                    self.assertEqual(response.status_code, 200)
                    page = Document(response.data.decode("utf-8"))
                    self.assertTrue(page.by_id(notice_id)["text"].strip())
                    page.by_id(form_id)


if __name__ == "__main__":
    unittest.main()
