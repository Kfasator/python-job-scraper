# Python Job Scraper

Lokalna aplikacja, która pobiera oferty z API [Arbeitnow](https://www.arbeitnow.com/api), wybiera oferty dla początkujących programistów Python pracujących przy backendzie lub API, zapisuje nowe wyniki w SQLite i udostępnia je w prostym interfejsie WWW.

## Wymagania

- Python 3.12 lub nowszy
- Połączenie z internetem podczas pobierania ofert
- macOS, jeśli chcesz otrzymywać powiadomienia systemowe o nowych ofertach

## Instalacja

W katalogu projektu utwórz środowisko i zainstaluj zależności:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Użycie

Uruchom pobieranie ofert:

```bash
python app/scraper.py
```

Scraper wypisuje dopasowane oferty, zapisuje nowe w `data/jobs.db` i wysyła powiadomienie macOS, jeśli znalazł nowe wyniki.

Aby otworzyć interfejs, uruchom serwer w drugim terminalu:

```bash
source venv/bin/activate
python app/server.py
```

Otwórz <http://127.0.0.1:8000>. Interfejs pokazuje zapisane oferty i pozwala wyszukiwać je po stanowisku, firmie oraz lokalizacji. Odśwież widok po kolejnym uruchomieniu scrapera.

## Kryteria filtrowania

Oferta musi zawierać odniesienie do Pythona (lub Django, FastAPI albo Flask), wskazywać rolę programistyczną, poziom junior/stażowy oraz pracę z backendem lub API. Wybrane niepowiązane role, m.in. sprzedaż, wsparcie techniczne i analiza danych, są pomijane.

## Testy

Testy filtrów wymagają `pytest`. Zainstaluj go w środowisku projektu i uruchom:

```bash
python -m pip install pytest
python -m pytest
```

## Dane lokalne

Baza SQLite (`data/jobs.db`), logi, środowisko wirtualne i pliki tymczasowe nie są przeznaczone do publikacji w repozytorium. Są wykluczone przez `.gitignore`; baza tworzy się automatycznie przy pierwszym uruchomieniu.
