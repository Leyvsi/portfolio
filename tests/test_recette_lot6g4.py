"""Contrats du kit et des pages corrigées ; aucun serveur, navigateur ou SQL."""
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import json
import sys
import unittest

from werkzeug.test import Client
from werkzeug.wrappers import Response
from tools import recette_lot6g4 as recipe
from test_rgpd_information import Document


class RecipeTests(unittest.TestCase):
    def test_all_ten_pages_have_shared_account_controls_and_one_feedback(self):
        pages=[name for name in recipe.PUBLIC if name.endswith('.html')]
        self.assertEqual(len(pages),10)
        for name in pages:
            with self.subTest(page=name):
                page=Document((recipe.ROOT/'frontend'/name).read_text(encoding='utf-8'))
                controls=page.by_id('session-controls')
                self.assertEqual(controls['attrs']['role'],'group')
                self.assertTrue(page.by_id('session-feedback'))
                self.assertTrue(any(node['tag']=='script' and node['attrs'].get('src')=='app.js' for node in page.nodes))

    def test_three_account_pages_keep_forms_and_api_scripts_without_legacy(self):
        for name, form_id, fields in (
            ('connexion.html', 'login-form', ['username', 'password']),
            ('admin-connexion.html', 'login-form', ['username', 'password']),
            ('inscription.html', 'signup-form', ['username', 'email', 'password']),
        ):
            with self.subTest(page=name):
                document = Document((recipe.ROOT / 'frontend' / name).read_text(encoding='utf-8'))
                self.assertEqual([node['attrs'].get('src') for node in document.nodes if node['tag'] == 'script'],
                                 ['api.js', 'app.js'])
                self.assertEqual([node['attrs']['name'] for node in document.fields(form_id)], fields)

    def test_proposal_and_theory_also_keep_api_order_without_legacy(self):
        for name, scripts in (('proposer-histoire.html', ['api.js', 'app.js']),
                              ('theories.html', ['api.js', 'app.js', 'theories-list.js'])):
            document = Document((recipe.ROOT / 'frontend' / name).read_text(encoding='utf-8'))
            self.assertEqual([node['attrs'].get('src') for node in document.nodes if node['tag'] == 'script'], scripts)

    def test_every_public_asset_and_page_script_is_served_by_new_kit_without_sql(self):
        def api(environ, start_response):
            return Response('API passthrough', status=404)(environ, start_response)
        recipe.inspect_assets(Client(recipe.public_application(api), Response))

    def test_source_manifest_covers_likes_and_kit_and_excludes_private_legacy_migrations(self):
        approved = recipe.validate_sources()
        self.assertIn(recipe.ROOT / 'frontend/likes.js', approved)
        self.assertIn(Path(recipe.__file__).resolve(), approved)
        self.assertNotIn(recipe.ROOT / 'frontend/donnees.js', approved)
        self.assertFalse(any(recipe.sensitive(path) or path.is_relative_to(recipe.ROOT / 'migrations') for path in approved))

    def test_changed_like_source_is_refused_before_any_application_import(self):
        original = Path.read_bytes
        def read(path):
            data = original(path)
            return data + b' ' if path == recipe.ROOT / 'frontend/likes.js' else data
        with patch.object(Path, 'read_bytes', read):
            with self.assertRaisesRegex(SystemExit, 'Source différente'):
                recipe.validate_sources()

    def test_private_manifest_entry_is_refused_before_read(self):
        config = json.dumps({'source_sha256_lf': {'.env': 'not-read'}})
        with patch.object(Path, 'read_text', return_value=config), patch.object(Path, 'read_bytes') as read:
            with self.assertRaisesRegex(SystemExit, 'Source interdite'):
                recipe.validate_sources()
        read.assert_not_called()

    def isolation(self):
        return recipe.Isolation(recipe.ROOT.parent / 'synthetic-evidence-only', set())

    def test_only_exact_memory_sqlite_database_is_accepted(self):
        guard = self.isolation()
        guard.database(SimpleNamespace(url=SimpleNamespace(drivername='sqlite', database=':memory:')))
        for driver, database in (('mysql+pymysql', ':memory:'), ('sqlite', 'site.db'), ('sqlite', None)):
            with self.assertRaises(PermissionError):
                guard.database(SimpleNamespace(url=SimpleNamespace(drivername=driver, database=database)))
        self.assertEqual(guard.counts['non_memory_database'], 3)

    def test_private_reads_and_repository_writes_are_denied_before_io(self):
        guard = self.isolation()
        for path in (recipe.ROOT / '.env', recipe.ROOT / 'cookies.txt', recipe.ROOT / 'frontend/donnees.js'):
            with self.assertRaises(PermissionError):
                guard.read(path)
        with self.assertRaises(PermissionError):
            guard.write(recipe.ROOT / 'README.md')

    def test_listener_policy_is_closed_by_default_and_outgoing_connections_stay_denied(self):
        guard = self.isolation()
        with self.assertRaises(PermissionError):
            guard.audit('socket.bind', (None, (recipe.HOST, recipe.PORT)))
        guard.serving = True
        guard.audit('socket.bind', (None, (recipe.HOST, recipe.PORT)))
        for event, args in (('socket.bind', (None, ('0.0.0.0', recipe.PORT))),
                            ('socket.connect', (None, (recipe.HOST, recipe.PORT))),
                            ('socket.getaddrinfo', ('example.invalid', 443))):
            with self.assertRaises(PermissionError):
                guard.audit(event, args)

    def test_migration_and_subprocess_execution_stay_denied(self):
        guard = self.isolation()
        code = compile('pass', str(recipe.ROOT / 'migrations/env.py'), 'exec')
        with self.assertRaises(PermissionError):
            guard.audit('exec', (code,))
        with self.assertRaises(PermissionError):
            guard.audit('subprocess.Popen', ())

    def test_serve_without_authorization_marker_stops_before_preparation(self):
        with patch.object(sys, 'argv', ['recipe', '--serve']), patch.object(recipe, 'validate_sources') as validate:
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit) as error:
                recipe.main()
        self.assertEqual(error.exception.code, 2)
        validate.assert_not_called()

    def test_journey_cannot_be_combined_with_manual_listener(self):
        with patch.object(sys, 'argv', ['recipe', '--serve', '--autorisation-execution-confirmee', '--check-journey']):
            with patch.object(recipe, 'validate_sources') as validate:
                with redirect_stderr(StringIO()), self.assertRaises(SystemExit) as error:
                    recipe.main()
        self.assertEqual(error.exception.code, 2)
        validate.assert_not_called()


if __name__ == '__main__':
    unittest.main()
