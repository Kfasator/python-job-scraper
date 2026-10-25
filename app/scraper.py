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
        logging.getLogger(__name__).info("Powiadomienie macOS wysłane.")
    else:
        logging.getLogger(__name__).warning(
            "Nie udało się wysłać powiadomienia macOS (kod %s): %s",
            result.returncode,
            result.stderr.strip() or "brak szczegółów",
        )


def main():
    configure_logging()
    logger = logging.getLogger(__name__)
    started_at = time.monotonic()
    logger.info("Rozpoczynam przebieg scrapera.")
    logger.info("Źródło ofert: %s", SOURCE_URL)
    logger.info("Plik logu: %s", LOG_PATH)

    try:
        logger.info("Pobieram dane z API (limit czasu: 15 s).")
        response = requests.get(SOURCE_URL, timeout=15)
        logger.info("API odpowiedziało kodem HTTP %s.", response.status_code)
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, dict) or not isinstance(data.get("data"), list):
            raise ValueError("Odpowiedź API ma nieoczekiwany format: brak listy 'data'.")
        source_jobs = data["data"]
        logger.info("Pobrano %s ofert ze źródła.", len(source_jobs))

        jobs = filter_jobs(source_jobs)
        logger.info("Filtry wybrały %s ofert.", len(jobs))
        print(f"Znaleziono ofert: {len(jobs)}")
        for job in jobs:
            logger.info(
                "Dopasowana oferta: stanowisko=%r | firma=%r | lokalizacja=%r | URL=%s",
                job.get("title", "Brak tytułu"),
                job.get("company_name", ""),
                job.get("location", ""),
                job.get("url", "Brak URL"),
            )
            print("Stanowisko:", job.get("title", "Brak tytułu"))
            print("Firma:", job.get("company_name", ""))
            print("Lokalizacja:", job.get("location", ""))
            print("Link:", job.get("url", ""))
            print("-" * 50)

        logger.info("Zapisuję wybrane oferty do lokalnej bazy SQLite.")
        saved_count = save_jobs(jobs)
        print(f"Zapisano nowych ofert do SQLite: {saved_count}")
        logger.info(
            "Zapis zakończony: %s nowych ofert; %s dopasowanych już było w bazie.",
            saved_count,
            len(jobs) - saved_count,
        )

        if saved_count > 0:
            send_notification(
                "Python Job Scraper",
                f"Zapisano {saved_count} nowych ofert pracy.",
            )
            print("Wysłano powiadomienie macOS.")
        else:
            logger.info("Brak nowych ofert; powiadomienie nie zostało wysłane.")
            print("Brak nowych ofert. Powiadomienie nie zostało wysłane.")

        logger.info("Przebieg zakończony poprawnie w %.2f s.", time.monotonic() - started_at)
    except requests.RequestException:
        logger.exception("Błąd podczas pobierania danych ze źródła %s.", SOURCE_URL)
        raise
    except Exception:
        logger.exception("Przebieg scrapera zakończył się błędem.")
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # The error has already been logged in main(); make scheduled runs fail visibly.
        raise SystemExit(1)
