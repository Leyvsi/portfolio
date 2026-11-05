"""Lot 6D : contrat administratif réel, données fictives en SQLite mémoire."""

from datetime import datetime
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Query

import test_reports as report_suite


class AdminPendingStatsTests(unittest.TestCase):
    authenticate = report_suite.ReportTests.authenticate

    @classmethod
    def setUpClass(cls):
        report_suite.ReportTests.setUpClass.__func__(cls)
        fixture = Path(__file__).resolve().parents[2] / "frontend/tests/fixtures/admin-proposals.json"
        cls.fixture = json.loads(fixture.read_text(encoding="utf-8"))
        with cls.app.app_context():
            cls.db.session.add(cls.models.User(
                id=3, username="fictitious-admin", email="admin@example.invalid",
                password_hash="unused", is_admin=True, is_banned=False,
            ))
            cls.db.session.commit()

    @classmethod
    def tearDownClass(cls):
        report_suite.ReportTests.tearDownClass.__func__(cls)

    def setUp(self):
        report_suite.ReportTests.setUp(self)
        self.authenticate(3)
        for row in self.fixture:
            values = dict(row)
            for key in ("created_at", "updated_at"):
                values[key] = datetime.fromisoformat(values[key])
            self.db.session.add(self.models.Proposal(**values))
        self.db.session.commit()

    def tearDown(self):
        self.db.session.rollback()
        self.models.Proposal.query.delete()
        self.db.session.commit()
        report_suite.ReportTests.tearDown(self)

    def snapshot(self):
        return {table.name: [dict(row) for row in self.db.session.execute(
            table.select().order_by(table.c.id)).mappings()]
            for table in self.db.metadata.sorted_tables}

    def test_private_list_matches_complete_shared_frontend_fixture(self):
        response = self.client.get("/api/v1/proposals")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.fixture)
        expected = {"id", "user_id", "title", "content", "status", "created_at", "updated_at"}
        self.assertTrue(all(set(row) == expected for row in response.get_json()))
        self.assertEqual(sum(row["status"] == "pending" for row in response.get_json()), 2)

    def test_other_text_statuses_are_preserved_without_enum_or_normalization(self):
        # Valeurs synthétiques permises par String(20), sans nouveau workflow.
        for value in ("approved", "rejected", "Pending", " pending", "unknown"):
            with self.subTest(status=value):
                self.db.session.get(self.models.Proposal, 1).status = value
                self.db.session.commit()
                rows = self.client.get("/api/v1/proposals").get_json()
                self.assertEqual(rows[0]["status"], value)
                self.assertEqual(sum(row["status"] == "pending" for row in rows), 1)

    def test_empty_list_is_successful_and_distinct_from_failure(self):
        self.models.Proposal.query.delete()
        self.db.session.commit()
        response = self.client.get("/api/v1/proposals")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_anonymous_reader_banned_and_forged_role_cannot_read_proposals(self):
        for user_id, status in ((None, 401), (1, 403), (2, 403)):
            with self.subTest(user_id=user_id):
                self.client = self.app.test_client()
                if user_id is not None:
                    self.authenticate(user_id)
                    with self.client.session_transaction() as session:
                        session["is_admin"] = True
                response = self.client.get("/api/v1/proposals")
                self.assertEqual(response.status_code, status)
                self.assertNotIn(self.fixture[0]["title"], response.get_data(as_text=True))

    def test_public_stats_contract_stays_three_aggregate_counts(self):
        self.client = self.app.test_client()
        response = self.client.get("/api/v1/stats")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"users": 3, "comments": 1, "reports": 0})
        self.assertNotIn("proposals", response.get_data(as_text=True))

    def test_reads_preserve_all_nine_tables(self):
        before = self.snapshot()
        self.assertEqual(len(before), 10)
        self.assertIn('comment_likes', before)
        for route in ("/api/v1/proposals", "/api/v1/stats", "/api/v1/stories"):
            self.assertEqual(self.client.get(route).status_code, 200)
        self.db.session.remove()
        self.assertEqual(self.snapshot(), before)

    def test_creation_still_forces_pending_even_if_client_requests_approved(self):
        self.authenticate(1)
        response = self.client.post("/api/v1/proposals", json={
            "title": "Fictitious creation", "content": "Test only", "status": "approved",
        }, headers={"X-CSRF-Token": "reports-csrf"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["proposal"]["status"], "pending")

    def test_database_failure_does_not_turn_into_successful_empty_list(self):
        # Le gestionnaire HTTP 500 existant est exercé sans changer l'application.
        # Intercepter le journal évite la lecture implicite des sources par le
        # formateur de traceback ; le vrai traitement HTTP 500 reste exécuté.
        with patch.object(self.app.logger, "error") as logged, patch.dict(
            self.app.config, {"PROPAGATE_EXCEPTIONS": False}
        ), patch.object(
            Query, "all", side_effect=SQLAlchemyError("fictitious-private-sql-detail")
        ):
            response = self.client.get("/api/v1/proposals")
        self.assertEqual(response.status_code, 500)
        self.assertNotEqual(response.get_json(silent=True), [])
        self.assertNotIn("fictitious-private-sql-detail", response.get_data(as_text=True))
        logged.assert_called_once()
