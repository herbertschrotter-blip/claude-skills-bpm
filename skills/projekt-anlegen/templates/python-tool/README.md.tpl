# {{name}}

Python-Werkzeug mit Befehlszeile. Angelegt als lauffähiges Grundgerüst; die Fachlogik kommt danach.

## Starten

```sh
python -m {{package}} status
```

Ausgabe: `{"status": "ready"}`. Einstellungen kommen aus der Umgebung (Namen in `.env.example`).

## Entwickeln

```sh
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python -m ruff format --check .
.venv/bin/python -m ruff check .
.venv/bin/python -m pytest
```

Unter Windows heißt der Interpreter `.venv\Scripts\python.exe`. Die Tests laufen parallel auf allen Kernen
(`-n auto`). Grundentscheidungen: [docs/entscheidungen.md](docs/entscheidungen.md).
