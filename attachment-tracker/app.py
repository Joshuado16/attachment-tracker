"""Attachment Tracker: a small Flask app for internship applications."""

import os
import sqlite3
from contextlib import closing
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for


BASE_DIR = Path(__file__).resolve().parent
STATUSES = ("Interested", "Applied", "Interview", "Offer", "Rejected", "Withdrawn")


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "local-development-key"),
        DATABASE=str(BASE_DIR / "attachment_tracker.db"),
    )
    if test_config:
        app.config.update(test_config)

    def get_db():
        connection = sqlite3.connect(app.config["DATABASE"])
        connection.row_factory = sqlite3.Row
        return connection

    def initialize_database():
        with closing(get_db()) as db:
            db.execute("PRAGMA foreign_keys = ON")
            db.execute(
                """CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    role TEXT NOT NULL,
                    contact_name TEXT NOT NULL DEFAULT '',
                    contact_email TEXT NOT NULL DEFAULT '',
                    deadline TEXT NOT NULL DEFAULT '',
                    follow_up_date TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'Interested',
                    notes TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )"""
            )
            db.commit()

    @app.route("/", methods=("GET", "POST"))
    def index():
        if request.method == "POST":
            company = request.form.get("company", "").strip()
            role = request.form.get("role", "").strip()
            status = request.form.get("status", "Interested")
            if not company or not role:
                flash("Company and role are required.", "error")
            elif status not in STATUSES:
                flash("Choose a valid application status.", "error")
            else:
                with closing(get_db()) as db:
                    db.execute(
                        """INSERT INTO applications
                           (company, role, contact_name, contact_email, deadline,
                            follow_up_date, status, notes)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (company, role,
                         request.form.get("contact_name", "").strip(),
                         request.form.get("contact_email", "").strip(),
                         request.form.get("deadline", ""),
                         request.form.get("follow_up_date", ""), status,
                         request.form.get("notes", "").strip()),
                    )
                    db.commit()
                flash("Application added.", "success")
                return redirect(url_for("index"))

        with closing(get_db()) as db:
            applications = db.execute(
                "SELECT * FROM applications ORDER BY created_at DESC, id DESC"
            ).fetchall()
        return render_template("index.html", applications=applications, statuses=STATUSES)

    @app.post("/applications/<int:application_id>/delete")
    def delete_application(application_id):
        with closing(get_db()) as db:
            result = db.execute("DELETE FROM applications WHERE id = ?", (application_id,))
            db.commit()
        if result.rowcount:
            flash("Application deleted.", "success")
        else:
            flash("That application was not found.", "error")
        return redirect(url_for("index"))

    with app.app_context():
        initialize_database()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
