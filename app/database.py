import logging
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "jobs.db"
logger = logging.getLogger(__name__)


def create_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                url TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    logger.info("SQLite database ready: %s", DB_PATH)


def save_jobs(jobs):
    create_database()
    saved_count = 0
    logger.info("Saving %s matching listings to %s.", len(jobs), DB_PATH)

    with sqlite3.connect(DB_PATH) as connection:
        for job in jobs:
            cursor = connection.execute("""
                INSERT OR IGNORE INTO jobs (title, company, location, url)
                VALUES (?, ?, ?, ?)
            """, (
                job.get("title", "Untitled listing"),
                job.get("company_name", ""),
                job.get("location", ""),
                job.get("url", "")
            ))

            saved_count += cursor.rowcount

    logger.info(
        "Database: added %s new records; skipped %s existing listings.",
        saved_count,
        len(jobs) - saved_count,
    )
    return saved_count

def get_all_jobs():
    create_database()

    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute("""
            SELECT title, company, location, url, created_at
            FROM jobs
            ORDER BY created_at DESC
        """).fetchall()

    return [dict(row) for row in rows]

if __name__ == "__main__":
    create_database()
    print("Database created!")
