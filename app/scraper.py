import logging
from logging.handlers import TimedRotatingFileHandler
import subprocess
import time
from pathlib import Path

import requests

from database import save_jobs
from filters import filter_jobs


PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_PATH = PROJECT_DIR / "scraper.log"
SOURCE_URL = "https://www.arbeitnow.com/api/job-board-api"


def configure_logging():
    """Write readable logs to both the terminal and a rotating project log."""
    logger = logging.getLogger()
    if logger.handlers:
        return

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # Detailed INFO logs stay in the file; only warnings and errors reach the terminal.
    console_handler.setLevel(logging.WARNING)
    logger.addHandler(console_handler)

    file_handler = TimedRotatingFileHandler(
        LOG_PATH,
        when="midnight",
        interval=1,
        backupCount=0,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def send_notification(title, message):
    script = """
    on run argv
        display notification (item 2 of argv) with title (item 1 of argv)
    end run
    """

    result = subprocess.run(
        ["osascript", "-e", script, title, message],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        logging.getLogger(__name__).info("macOS notification sent.")
    else:
        logging.getLogger(__name__).warning(
            "Could not send macOS notification (code %s): %s",
            result.returncode,
            result.stderr.strip() or "no details available",
        )


def main():
    configure_logging()
    logger = logging.getLogger(__name__)
    started_at = time.monotonic()
    logger.info("Starting scraper run.")
    logger.info("Listings source: %s", SOURCE_URL)
    logger.info("Log file: %s", LOG_PATH)

    try:
        logger.info("Fetching data from the API (timeout: 15 s).")
        response = requests.get(SOURCE_URL, timeout=15)
        logger.info("API returned HTTP status %s.", response.status_code)
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, dict) or not isinstance(data.get("data"), list):
            raise ValueError("Unexpected API response: missing 'data' list.")
        source_jobs = data["data"]
        logger.info("Fetched %s listings from the source.", len(source_jobs))

        jobs = filter_jobs(source_jobs)
        logger.info("Filters selected %s listings.", len(jobs))
        print(f"Matching listings found: {len(jobs)}")
        for job in jobs:
            logger.info(
                "Matching listing: title=%r | company=%r | location=%r | URL=%s",
                job.get("title", "Untitled listing"),
                job.get("company_name", ""),
                job.get("location", ""),
                job.get("url", "No URL"),
            )
            print("Title:", job.get("title", "Untitled listing"))
            print("Company:", job.get("company_name", ""))
            print("Location:", job.get("location", ""))
            print("Link:", job.get("url", ""))
            print("-" * 50)

        logger.info("Saving selected listings to the local SQLite database.")
        saved_count = save_jobs(jobs)
        print(f"New listings saved to SQLite: {saved_count}")
        logger.info(
            "Save complete: %s new listings; %s matching listings were already in the database.",
            saved_count,
            len(jobs) - saved_count,
        )

        if saved_count > 0:
            send_notification(
                "Python Job Scraper",
                f"Saved {saved_count} new job listings.",
            )
            print("macOS notification sent.")
        else:
            logger.info("No new listings; notification was not sent.")
            print("No new listings. Notification was not sent.")

        logger.info("Run completed successfully in %.2f s.", time.monotonic() - started_at)
    except requests.RequestException:
        logger.exception("Error fetching data from source %s.", SOURCE_URL)
        raise
    except Exception:
        logger.exception("Scraper run failed.")
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # The error has already been logged in main(); make scheduled runs fail visibly.
        raise SystemExit(1)
