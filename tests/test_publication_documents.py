"""Contrat de sélection publique ; aucun document interne n'est ouvert."""
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
INTERNAL={
 'docs/soutenance/BILAN_LOT6H17_1.md',
 'docs/soutenance/BILAN_LOT6H17_3.md',
 'docs/soutenance/BILAN_LOT6H18_2.md',
 'docs/soutenance/PROTOCOLE_SOUTENANCE_LOT6H12.md',
}


class PublicDocumentSelectionTests(unittest.TestCase):
    def test_internal_files_are_absent(self):
        for rel in INTERNAL:
            with self.subTest(fichier=rel): self.assertFalse((ROOT/rel).exists())

    def test_internal_paths_are_explicitly_ignored(self):
        patterns=(ROOT/'.gitignore').read_text(encoding='utf-8').splitlines()
        for rel in INTERNAL:
            with self.subTest(fichier=rel): self.assertIn('/'+rel,patterns)

    def test_public_documents_do_not_link_to_internal_files(self):
        for p in ROOT.rglob('*.md'):
            text=re.sub(r'```[\s\S]*?```','',p.read_text(encoding='utf-8-sig'))
            links=re.findall(r'!?\[[^\]]+\]\(([^)]+)\)',text)
            links+=re.findall(r'<(?:a|img)\b[^>]*(?:href|src)=["\x27]([^"\x27]+)["\x27]',text)
            for target in links:
                target=unquote(target)
                if urlsplit(target).scheme: continue
                resolved=(p.parent/target.split('#')[0]).resolve()
                if resolved.is_relative_to(ROOT):
                    with self.subTest(source=str(p.relative_to(ROOT)),cible=target):
                        self.assertNotIn(resolved.relative_to(ROOT).as_posix(),INTERNAL)

    def test_historical_validation_has_current_qualification(self):
        historical=(ROOT/'docs/soutenance/VALIDATION_LOT6H22_4.md').read_text(encoding='utf-8')
        self.assertIn('VALIDATION_LOT6H22_6.md',historical)
        self.assertTrue((ROOT/'docs/soutenance/VALIDATION_LOT6H22_6.md').is_file())


if __name__=='__main__': unittest.main(verbosity=2)
