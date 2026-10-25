# Python Job Scraper

A local application that fetches job listings from the [Arbeitnow API](https://www.arbeitnow.com/api), filters for junior Python backend and API roles, stores new matches in SQLite, and displays them in a simple web interface.

## Requirements

- Python 3.12 or newer
- An internet connection to fetch listings
- macOS for desktop notifications about new listings

## Installation

From the project directory, create a virtual environment and install the runtime dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Usage

Run the scraper to fetch and save matching listings:

```bash
python app/scraper.py
```

The scraper prints matching listings, saves new ones to `data/jobs.db`, and sends a macOS notification when it finds new results.

To view saved listings, start the web server in a second terminal:

```bash
source venv/bin/activate
python app/server.py
```

Open <http://127.0.0.1:8000>. The interface lets you search saved listings by title, company, and location. Refresh the page after another scraper run to see new results.

## Filtering criteria

A listing must mention Python, Django, FastAPI, or Flask; indicate a software development role; be junior or entry-level; and involve backend or API work. Unrelated roles, including sales, support, and data analysis, are excluded. The filter also recognizes Polish job-title terms to match local listings.

## Tests

Install the development dependencies, including the pinned `pytest` version:

```bash
python -m pip install -r requirements-dev.txt
```

Run the tests from the project directory:

```bash
python -m pytest
```

## Local data

The SQLite database (`data/jobs.db`), logs, virtual environment, and temporary files are not included in the repository. They are excluded by `.gitignore`. The database is created automatically on the first run.
