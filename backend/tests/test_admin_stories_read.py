"""Lot 6B: real public Flask reads compared with the shared frontend fixture."""

from datetime import datetime
import json
from pathlib import Path
import unittest
from urllib.parse import quote

import test_reports as report_suite


class AdminStoriesReadTests(unittest.TestCase):
    authenticate = report_suite.ReportTests.authenticate

    @classmethod
    def setUpClass(cls):
        report_suite.ReportTests.setUpClass.__func__(cls)
        fixture = Path(__file__).resolve().parents[2] / "frontend/tests/fixtures/admin-stories.json"
        cls.fixture = json.loads(fixture.read_text(encoding="utf-8"))
        with cls.app.app_context():
            cls.db.session.get(cls.models.Category, 1).name = "Histoires résolues"
            cls.db.session.add_all([
                cls.models.Category(id=2, name="Cold Cases"),
                cls.models.Category(id=17, name="Catégorie fictive supplémentaire"),
                cls.models.User(id=3, username="fictitious-admin", email="admin@example.invalid",
                                password_hash="unused", is_admin=True),
            ])
            cls.db.session.flush()
            # Même jeu de données complet que les tests frontend, créé seulement
            # dans la SQLite en mémoire protégée par le harnais et ReportTests.
            for row in cls.fixture:
                values = {key:value for key,value in row.items() if key not in ("id", "votes")}
                values["created_at"] = datetime.fromisoformat(values["created_at"])
                story = cls.db.session.get(cls.models.Story, row["id"])
                if story is None:
                    cls.db.session.add(cls.models.Story(id=row["id"], **values))
                else:
                    for key,value in values.items():
                        setattr(story, key, value)
            cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        report_suite.ReportTests.tearDownClass.__func__(cls)

    def setUp(self):
        report_suite.ReportTests.setUp(self)

    def tearDown(self):
        report_suite.ReportTests.tearDown(self)

    def snapshot(self):
        return {table.name:[dict(row) for row in self.db.session.execute(table.select().order_by(table.c.id)).mappings()]
                for table in self.db.metadata.sorted_tables}

    def test_list_matches_shared_frontend_fixture_exactly(self):
        response = self.client.get("/api/v1/stories")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.fixture)
        expected = {"id", "slug", "title", "summary", "content", "image_url",
                    "category_id", "author_id", "votes", "created_at"}
        self.assertTrue(all(set(row) == expected for row in response.get_json()))

    def test_unknown_category_is_preserved_without_invented_name(self):
        rows = self.client.get("/api/v1/stories").get_json()
        self.assertEqual([row["category_id"] for row in rows], [1, 2, 17, 1])
        self.assertTrue(all("category_name" not in row for row in rows))
        self.assertEqual([row["id"] for row in rows], [1, 2, 3, 4])

    def test_existing_detail_route_resolves_each_encoded_slug(self):
        for row in self.fixture:
            with self.subTest(slug=row["slug"]):
                response = self.client.get("/api/v1/stories/slug/" + quote(row["slug"], safe=""))
                self.assertEqual(response.status_code, 200)
                self.assertEqual({key:response.get_json()[key] for key in row}, row)

    def test_missing_detail_is_json_404(self):
        response = self.client.get("/api/v1/stories/slug/fictitious-missing")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.is_json)

    def test_public_reads_remain_public_for_all_session_states(self):
        for user_id in (None, 1, 2, 3):
            with self.subTest(user_id=user_id):
                client = self.app.test_client()
                if user_id is not None:
                    with client.session_transaction() as session:
                        session["user_id"] = user_id
                self.assertEqual(client.get("/api/v1/stories").get_json(), self.fixture)

    def test_all_reads_leave_the_nine_tables_unchanged(self):
        before = self.snapshot()
        self.client.get("/api/v1/stories")
        for row in self.fixture:
            self.client.get("/api/v1/stories/slug/" + quote(row["slug"], safe=""))
        self.client.get("/api/v1/stories/slug/fictitious-missing")
        self.db.session.remove()
        self.assertEqual(self.snapshot(), before)
