import tempfile
import unittest
from pathlib import Path

from app import create_app


class AttachmentTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database = Path(self.temp_dir.name) / "test.db"
        self.app = create_app({"TESTING": True, "DATABASE": str(database), "SECRET_KEY": "test"})
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_home_page_shows_empty_state(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No applications yet", response.data)

    def test_can_add_application_and_see_details(self):
        response = self.client.post("/", data={
            "company": "Example Labs", "role": "Python Intern",
            "contact_name": "A. Contact", "contact_email": "contact@example.com",
            "deadline": "2026-11-15", "follow_up_date": "2026-11-20",
            "status": "Applied", "notes": "Send portfolio link",
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        for expected in (b"Example Labs", b"Python Intern", b"Applied", b"Send portfolio link"):
            self.assertIn(expected, response.data)

    def test_requires_company_and_role(self):
        response = self.client.post("/", data={"company": "", "role": "Intern"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Company and role are required", response.data)

    def test_can_delete_application(self):
        self.client.post("/", data={"company": "Example Labs", "role": "Intern"})
        with self.app.app_context():
            from flask import current_app
            import sqlite3
            db = sqlite3.connect(current_app.config["DATABASE"])
            application_id = db.execute("SELECT id FROM applications").fetchone()[0]
            db.close()
        response = self.client.post(f"/applications/{application_id}/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No applications yet", response.data)


if __name__ == "__main__":
    unittest.main()
