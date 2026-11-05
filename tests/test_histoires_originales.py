"""Catalogue et contrats du mode historique ; aucun import applicatif ni SQL."""
from contextlib import redirect_stderr
from copy import deepcopy
from io import StringIO
from pathlib import Path
from unittest.mock import patch
import hashlib
import json
import sys
import unittest

from tools import recette_lot6g4 as recipe

BODY_HASHES = (
    'f7b6d26afbc83607969321edc142ca6f33b72bd0200a675d6e8d623656ab8cab',
    '28396b22b85ee03b470cbefeb665fe6623dd0ba8a8a952fdf92fa8bc6a347b3b',
    '3c84da15b940377187ddce16e653f48cd2bdd21801f68def1b66a4d6d6aa1f27',
    '5e2376c28c2c5be4fbe7e916f0a1240ca539c53bcb0ba396e4c4fff40c1e3d79',
    'd819f8662fcb54a2880381edde18bf93cbf9371e4b9c09295a83d391469dbaa5',
    'c8ccc5ad8fb3e0cefff0bc2d1add14c50745fb6d025cc48d18b865f06da627f9',
)


class HistoricalStoriesTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(recipe.HISTORICAL_CATALOG.read_text(encoding='utf-8'))

    def load_changed(self, change):
        data = deepcopy(self.data)
        change(data)
        with patch.object(Path, 'read_text', return_value=json.dumps(data)):
            return recipe.load_historical_stories()

    def test_six_raw_articles_are_the_audited_complete_versions(self):
        rows = recipe.load_historical_stories()
        self.assertEqual(tuple(hashlib.sha256(r['content_html'].encode()).hexdigest() for r in rows), BODY_HASHES)
        self.assertEqual([len([b for b in r['blocks'] if b['tag'] == 'h4']) for r in rows], [5, 5, 4, 5, 5, 5])
        for row in rows:
            self.assertEqual(row['content'], '\n\n'.join(b['text'] for b in row['blocks']))
            self.assertNotIn('Contenu fictif de recette.', row['content'])

    def test_six_categories_ids_slugs_and_sources_are_unambiguous(self):
        rows = recipe.load_historical_stories()
        self.assertEqual([r['id'] for r in rows], [101, 102, 103, 201, 202, 203])
        self.assertEqual([r['category_id'] for r in rows], [1, 1, 1, 2, 2, 2])
        self.assertEqual([r['slug'] for r in rows], ['golden-state-killer','chris-watts','michelle-carter','anthonioz','noirval','manoir-de-l-ombre'])
        for row in rows:
            self.assertIsNone(row['image_url'])
            self.assertEqual(len(row['gallery']), 3)
            self.assertEqual(len(row['testimonies']), 2)
            self.assertIn(len(row['sources']), (2, 3))
            self.assertTrue(row['provenance']['commit'])

    def test_editorial_choice_is_b_without_correction_or_mixing(self):
        rows = recipe.load_historical_stories()
        self.assertEqual(self.data['editorial_choices'], {'cc1':'B','cc2':'B'})
        self.assertIn('Léa', rows[3]['content'])
        self.assertIn('cygantaine', rows[3]['content'])
        self.assertNotIn('Le chiffre 7 sait', rows[3]['content'])
        self.assertIn('corps sans vie', rows[4]['content'])
        self.assertIn('he distingue', rows[4]['content'])
        self.assertNotIn('amnésie', rows[4]['content'])

    def test_the_catalog_is_approved_and_never_a_public_resource(self):
        self.assertIn(recipe.HISTORICAL_CATALOG.resolve(), recipe.validate_sources())
        self.assertNotIn('tools/fixtures/dossiers_historiques.json', recipe.PUBLIC)
        from werkzeug.test import Client
        from werkzeug.wrappers import Response
        client = Client(recipe.public_application(lambda e,s: Response('API')(e,s)), Response)
        self.assertEqual(client.get('/tools/fixtures/dossiers_historiques.json').status_code, 403)

    def test_changed_catalog_is_refused_before_application_import(self):
        original = Path.read_bytes
        def read(path):
            data = original(path)
            return data+b' ' if path == recipe.HISTORICAL_CATALOG.resolve() else data
        with patch.object(Path, 'read_bytes', read):
            with self.assertRaises(SystemExit): recipe.validate_sources()

    def test_wrong_editorial_choice_and_missing_article_are_refused(self):
        for change in [lambda d:d['editorial_choices'].update(cc1='A'), lambda d:d['stories'].pop()]:
            with self.subTest(change=change):
                with self.assertRaises(ValueError): self.load_changed(change)

    def test_duplicate_id_and_slug_are_refused(self):
        for field in ['id','slug']:
            with self.subTest(field=field):
                with self.assertRaises(ValueError): self.load_changed(lambda d:d['stories'][1].update({field:d['stories'][0][field]}))

    def test_string_and_boolean_ids_and_wrong_category_are_refused(self):
        for field, value in [('id','h1'),('id',True),('category_id',2),('category_id',True),('slug','../story')]:
            with self.subTest(field=field,value=value):
                with self.assertRaises(ValueError): self.load_changed(lambda d:d['stories'][0].update({field:value}))

    def test_original_body_or_visible_text_cannot_be_changed_independently(self):
        for field in ['content_html','content']:
            with self.subTest(field=field):
                with self.assertRaises(ValueError): self.load_changed(lambda d:d['stories'][0].update({field:d['stories'][0][field]+'x'}))

    def test_no_image_is_activated_before_the_image_lot(self):
        with self.assertRaises(ValueError): self.load_changed(lambda d:d['stories'][0].update(image_url='images/new.jpg'))

    def test_active_html_attributes_and_truncated_html_are_refused(self):
        for body in ['<script>alert(1)</script>', '<p onclick="x">Texte</p>', '<p>Texte', '<p>Texte</h4>', 'Hors bloc']:
            with self.subTest(body=body):
                with self.assertRaises(ValueError): recipe.historical_blocks(body)

    def test_inline_emphasis_entities_and_punctuation_keep_their_words(self):
        self.assertEqual(recipe.historical_blocks('<h4>Chapitre</h4><p>Un <strong>mot</strong>, &amp; un autre.</p>'),
                         [{'tag':'h4','text':'Chapitre'},{'tag':'p','text':'Un mot, & un autre.'}])

    def test_incompatible_modes_stop_before_preparation(self):
        for argv in [['--check-histoires'], ['--histoires-originales','--check-journey'],
                     ['--histoires-originales','--probe-isolation'],
                     ['--histoires-originales','--check-histoires','--serve','--autorisation-execution-confirmee']]:
            with self.subTest(argv=argv), patch.object(sys,'argv',['recipe']+argv), patch.object(recipe,'validate_sources') as validate:
                with redirect_stderr(StringIO()), self.assertRaises(SystemExit): recipe.main()
                validate.assert_not_called()


if __name__ == '__main__':
    unittest.main()
