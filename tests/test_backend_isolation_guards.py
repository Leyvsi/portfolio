"""Sondes du vrai harnais dans des fixtures Temp, sans application ni base réelle."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IsolationGuardTests(unittest.TestCase):
    def test_real_audit_hook_paths_and_mutations(self):
        temporary = Path(tempfile.mkdtemp(prefix='lpe-guard-fixtures-')).resolve()
        project = temporary / 'candidate-synthetique'
        suites = project / 'backend/tests'
        suites.mkdir(parents=True)
        outside = temporary / 'hors-preuves'
        outside.mkdir()
        (outside / 'source.txt').write_text('témoin', encoding='utf-8')
        (outside / '.env').write_text('FIXTURE_SANS_SECRET', encoding='utf-8')
        (outside / 'repertoire-vide').mkdir()
        (suites / 'test_reports.py').write_text('# Fixture de présence uniquement.\n', encoding='utf-8')
        code = '''from pathlib import Path
import os
import socket
import sqlite3
import _sqlite3
import tempfile
import unittest

OUTSIDE = Path(OUTSIDE_LITERAL)
EVIDENCE = Path(os.environ['PORTFOLIO_TEST_EVIDENCE'])

class SyntheticGuardProbes(unittest.TestCase):
    def denied(self, operation):
        with self.assertRaises(PermissionError):
            operation()

    def test_positive_mutations_inside_evidence(self):
        folder = EVIDENCE / 'autorise'
        folder.mkdir()
        source = folder / 'source.txt'
        source.write_text('fictif', encoding='utf-8')
        self.assertEqual(source.read_text(encoding='utf-8'), 'fictif')
        destination = folder / 'destination.txt'
        source.rename(destination)
        os.truncate(destination, 2)
        os.chmod(destination, 0o600)
        os.utime(destination, None)
        replacement = folder / 'remplacement.txt'
        destination.replace(replacement)
        replacement.unlink()
        folder.rmdir()
        self.assertTrue(Path(tempfile.mkdtemp()).is_relative_to(EVIDENCE))

    def test_mkdir_absolute(self): self.denied(lambda: (OUTSIDE / 'mkdir-absolu').mkdir())
    def test_mkdir_relative(self): self.denied(lambda: Path(os.path.relpath(OUTSIDE / 'mkdir-relatif')).mkdir())
    def test_mkdir_traversal(self): self.denied(lambda: (EVIDENCE / '..' / 'sortie-par-parent').mkdir())
    def test_mkdir_prefix_collision(self): self.denied(lambda: Path(str(EVIDENCE) + '-autre').mkdir())
    def test_open_write(self): self.denied(lambda: (OUTSIDE / 'nouveau.txt').write_text('fictif'))
    def test_open_bytes_path(self): self.denied(lambda: open(os.fsencode(OUTSIDE / 'octets.txt'), 'w'))
    def test_open_append(self): self.denied(lambda: open(OUTSIDE / 'source.txt', 'a'))
    def test_open_readwrite(self): self.denied(lambda: open(OUTSIDE / 'source.txt', 'r+'))
    def test_open_exclusive(self): self.denied(lambda: open(OUTSIDE / 'exclusif.txt', 'x'))
    def test_os_open(self): self.denied(lambda: os.open(OUTSIDE / 'os-open.txt', os.O_CREAT | os.O_WRONLY))
    def test_remove(self): self.denied(lambda: (OUTSIDE / 'source.txt').unlink())
    def test_rmdir(self): self.denied(lambda: (OUTSIDE / 'repertoire-vide').rmdir())
    def test_rename_source_outside(self): self.denied(lambda: (OUTSIDE / 'source.txt').rename(EVIDENCE / 'destination.txt'))
    def test_replace_source_outside(self): self.denied(lambda: (OUTSIDE / 'source.txt').replace(EVIDENCE / 'destination.txt'))
    def test_rename_destination_outside(self):
        source = EVIDENCE / 'renommer.txt'
        source.write_text('fictif')
        self.denied(lambda: source.rename(OUTSIDE / 'renomme.txt'))
        self.assertTrue(source.exists())
    def test_replace_destination_outside(self):
        source = EVIDENCE / 'remplacer.txt'
        source.write_text('fictif')
        self.denied(lambda: source.replace(OUTSIDE / 'remplace.txt'))
        self.assertTrue(source.exists())
    def test_truncate(self): self.denied(lambda: os.truncate(OUTSIDE / 'source.txt', 0))
    def test_chmod(self): self.denied(lambda: os.chmod(OUTSIDE / 'source.txt', 0o600))
    def test_utime(self): self.denied(lambda: os.utime(OUTSIDE / 'source.txt', None))
    def test_hard_link(self): self.denied(lambda: os.link(OUTSIDE / 'source.txt', EVIDENCE / 'lien.txt'))
    def test_symbolic_link(self): self.denied(lambda: os.symlink(OUTSIDE / 'source.txt', EVIDENCE / 'symbolique.txt'))
    def test_private_read(self): self.denied(lambda: (OUTSIDE / '.env').read_text())
    def test_sqlite_file(self): self.denied(lambda: sqlite3.connect(str(OUTSIDE / 'jetable.sqlite3')))
    def test_sqlite_memory(self):
        with sqlite3.connect(':memory:') as connection:
            self.assertEqual(connection.execute('SELECT 1').fetchone()[0], 1)
    def test_sqlite_attach(self):
        with sqlite3.connect(':memory:') as connection:
            with self.assertRaises(sqlite3.DatabaseError):
                connection.execute('ATTACH DATABASE ? AS autre', (str(OUTSIDE / 'attache.sqlite3'),))
    def test_sqlite_detach(self):
        with sqlite3.connect(':memory:') as connection:
            with self.assertRaises(sqlite3.DatabaseError):
                connection.execute('DETACH DATABASE autre')
    def test_sqlite_vacuum_into(self):
        with sqlite3.connect(':memory:') as connection:
            with self.assertRaises(sqlite3.DatabaseError):
                connection.execute('VACUUM INTO ?', (str(OUTSIDE / 'vacuum.sqlite3'),))
    def test_sqlite_extension(self):
        with sqlite3.connect(':memory:') as connection:
            self.denied(lambda: connection.enable_load_extension(True))
    def test_original_counterexample_is_refused_before_attach(self):
        path = OUTSIDE / 'constructeur-direct.sqlite3'
        def original_counterexample():
            connection = sqlite3.Connection(':memory:')
            try:
                connection.execute('ATTACH DATABASE ? AS fixture', (str(path),))
                connection.execute('CREATE TABLE fixture.temoin (id INTEGER PRIMARY KEY)')
                connection.commit()
            finally:
                connection.close()
        self.denied(original_counterexample)
        self.assertFalse(path.exists())
    def test_dbapi_connection_constructor(self): self.denied(lambda: sqlite3.dbapi2.Connection(':memory:'))
    def test_native_connection_constructor(self): self.denied(lambda: _sqlite3.Connection(':memory:'))
    def test_native_connect_alias(self): self.denied(lambda: _sqlite3.connect(':memory:'))
    def test_direct_file_constructor(self): self.denied(lambda: sqlite3.Connection(str(OUTSIDE / 'direct.sqlite3')))
    def test_connection_subclass_constructor(self):
        class OtherConnection(sqlite3.Connection): pass
        self.denied(lambda: OtherConnection(':memory:'))
    def test_custom_factory_not_called(self):
        calls = []
        def other_factory(*args, **kwargs):
            calls.append(True)
            return sqlite3.Connection(*args, **kwargs)
        self.denied(lambda: sqlite3.connect(':memory:', factory=other_factory))
        self.assertEqual(calls, [])
    def test_factory_subclass_refused(self):
        class OtherConnection(sqlite3.Connection): pass
        self.denied(lambda: sqlite3.connect(':memory:', factory=OtherConnection))
    def test_known_factory_is_secured(self):
        with sqlite3.connect(':memory:', factory=sqlite3.Connection) as connection:
            self.denied(lambda: connection.set_authorizer(None))
            with self.assertRaises(sqlite3.DatabaseError):
                connection.execute('ATTACH DATABASE ? AS other', (str(OUTSIDE / 'factory.sqlite3'),))
    def test_authorizer_cannot_be_removed(self):
        with sqlite3.connect(':memory:') as connection:
            self.denied(lambda: connection.set_authorizer(None))
    def test_authorizer_cannot_be_replaced(self):
        with sqlite3.connect(':memory:') as connection:
            self.denied(lambda: connection.set_authorizer(lambda *args: sqlite3.SQLITE_OK))
    def test_temp_store_cannot_be_changed(self):
        with sqlite3.connect(':memory:') as connection:
            with self.assertRaises(sqlite3.DatabaseError): connection.execute('PRAGMA temp_store=FILE')
            self.assertEqual(connection.execute('PRAGMA temp_store').fetchone()[0], 2)
    def test_temp_directory_cannot_be_changed(self):
        with sqlite3.connect(':memory:') as connection:
            with self.assertRaises(sqlite3.DatabaseError): connection.execute("PRAGMA temp_store_directory='.'")
    def test_data_directory_cannot_be_changed(self):
        with sqlite3.connect(':memory:') as connection:
            with self.assertRaises(sqlite3.DatabaseError): connection.execute("PRAGMA data_store_directory='.'")
    def test_memory_uri_refused(self): self.denied(lambda: sqlite3.connect('file:fixture?mode=memory&cache=shared', uri=True))
    def test_file_uri_refused(self): self.denied(lambda: sqlite3.connect('file:' + str(OUTSIDE / 'uri.sqlite3'), uri=True))
    def test_empty_database_refused(self): self.denied(lambda: sqlite3.connect(''))
    def test_attach_memory_also_refused(self):
        with sqlite3.connect(':memory:') as connection:
            with self.assertRaises(sqlite3.DatabaseError): connection.execute("ATTACH DATABASE ':memory:' AS other")
    def test_sql_extension_refused(self):
        with sqlite3.connect(':memory:') as connection:
            with self.assertRaises(sqlite3.DatabaseError): connection.execute("SELECT load_extension('fixture-inexistante')")
    def test_memory_backup_is_allowed(self):
        source, destination = sqlite3.connect(':memory:'), sqlite3.connect(':memory:')
        try:
            source.execute('CREATE TABLE temoin(id INTEGER PRIMARY KEY)')
            source.execute('INSERT INTO temoin VALUES (1)')
            source.commit()
            source.backup(destination)
            self.assertEqual(destination.execute('SELECT id FROM temoin').fetchone()[0], 1)
        finally:
            source.close(); destination.close()
    def test_dbapi_connect_memory_is_allowed(self):
        with sqlite3.dbapi2.connect(':memory:') as connection:
            self.assertEqual(connection.execute('SELECT 1').fetchone()[0], 1)
    def test_creation_permission_reset_after_error(self):
        with self.assertRaises(TypeError): sqlite3.connect(':memory:', timeout=object())
        self.denied(lambda: sqlite3.Connection(':memory:'))
    def test_network(self): self.denied(lambda: socket.socket())
'''.replace('OUTSIDE_LITERAL', repr(str(outside)))
        (suites / 'test_sondes.py').write_text(code, encoding='utf-8')
        command = [sys.executable, '-I', '-B', str(ROOT / 'tools/valider_backend_isole.py'),
                   '--candidate-root', str(project), '--suite', 'test_sondes.py']
        process = subprocess.run(command, cwd=project, capture_output=True)
        output = process.stdout.decode('utf-8', 'replace')
        if process.returncode:
            self.fail(process.stderr.decode('utf-8', 'replace'))
        reports = [json.loads(line) for line in output.splitlines() if line.startswith('{')]
        report = reports[-1]
        self.assertEqual(report['tests'], 52)
        self.assertEqual(report['failures'] + report['errors'] + report['skipped'], 0)
        self.assertGreaterEqual(report['guard_counts']['write_denied'], 21)
        self.assertGreaterEqual(report['guard_counts']['sqlite_bypass_denied'], 8)
        self.assertGreaterEqual(report['guard_counts']['sqlite_policy_denied'], 7)
        self.assertEqual((outside / 'source.txt').read_text(encoding='utf-8'), 'témoin')
        self.assertEqual(sorted(p.name for p in outside.iterdir()), ['.env', 'repertoire-vide', 'source.txt'])
        print(json.dumps({'sondes_gardes': report, 'fixtures_seulement': True}, ensure_ascii=True))


if __name__ == '__main__':
    unittest.main(verbosity=2)
