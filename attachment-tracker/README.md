# Attachment Tracker

A small Flask web app for managing internship and industrial attachment applications.

## MVP requirements

- Add and view application records with company, role, contact details, deadline, follow-up date, status, and notes.
- Update the status of an application and record when an offer is received.
- Keep application data in a local SQLite database for easy setup.
- Use server-rendered HTML with a small CSS layer; add JavaScript only when the MVP needs it.
- Cover the core page and data operations with automated tests.

## Current scope

This starter implements adding, listing, and deleting applications. Status, deadline, follow-up, contact, and offer fields are stored now; editing and filtering are sensible next learning steps. There is no login yet, so keep this local and do not put sensitive information in it.

## Setup (Python 3.10+)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m flask --app app run --debug
```

Open http://127.0.0.1:5000. The database file `attachment_tracker.db` is created automatically in the project folder.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Database path

The first version uses Python's built-in SQLite support, so no database server is needed. When the app grows, PostgreSQL can replace SQLite by changing the connection layer, adding a PostgreSQL driver, and using migrations to create/upgrade the schema. The application fields and basic SQL concepts transfer directly; database-specific SQL and connection setup may need small changes. Do that as a separate step after learning the current version.

## Learning path

1. Run the app and read `app.py` from top to bottom.
2. Submit one application and inspect how the form names map to database columns.
3. Read `tests/test_app.py` to see how Flask's test client exercises routes without opening a browser.
4. Add an edit flow, then search/filtering, with a test for each behavior.
5. Add PostgreSQL and schema migrations once the SQLite version is understood.
