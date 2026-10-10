# Stack Python

Arten, Orte und Grunddateien für neue Python-Projekte. Regeln für Code und Tests im laufenden Projekt stehen bei
code-erstellen (`skills/code-erstellen/references/stacks/python.md`). Läuft das Werkzeug neben Home Assistant, gilt
zusätzlich `references/stacks/home-assistant.md` (Art Python-Werkzeug).

Das **Werkzeug** erzeugt der Generator (`references/generator.md`, Projektart `python-tool`, ohne Speicher oder mit
SQLite); die Vorlagen unter `templates/` setzen alles unten um. Bibliothek und Dienst entstehen nach dieser Reference.

## Arten

| Art | Wofür | Grunddateien |
|---|---|---|
| Werkzeug | ein Aufruf, Ein- und Ausgabe über Dateien oder JSON | `<paket>/__init__.py`, `<paket>/__main__.py`, `tests/`, `pyproject.toml` |
| Bibliothek | von anderen Projekten genutzt | `src/<paket>/`, `tests/`, `pyproject.toml` mit Version |
| Dienst | läuft dauerhaft, oft mit Datenbank | wie Bibliothek, dazu Konfiguration über die Umgebung (`.env.example`; `.env` nie ins Repo) |

## Grunddateien

- `pyproject.toml`: Name, Version, `requires-python`; Prüfwerkzeuge (pytest, pytest-xdist, Ruff) als optionale
  Abhängigkeiten (`[project.optional-dependencies] dev = [...]`) mit fester Version.
- `README.md` mit Aufruf und Testbefehl.
- `.gitignore`: `__pycache__/`, `*.pyc`, `.venv/`, `.pytest_cache/`, `build/`, `dist/`, `*.egg-info/`, `.env`.

## Testgerüst (parallel-fähig)

- `pytest`, `pytest-xdist` und `ruff` mit fester Version (`==`). Die Versionen stehen in `templates/versions.json`
  (vom Generator geprüft); ohne Generator die aktuelle Version beim Anlegen nachsehen
  (`pip index versions pytest-xdist`), nicht raten.
- Befehl: `python -m pytest -n auto`. `-n auto` misst die Kerne zur Laufzeit, auch virtuelle; keine Zahl eintragen,
  auch nicht im Profil. Bei sehr kleinen Läufen kostet das ein, zwei Sekunden Start, dafür muss später nichts
  umgestellt werden. Auf Maschinen mit wenig Speicher eine Obergrenze mit `--maxprocesses`.
- Isolation je Test: Tests schreiben nur in `tmp_path`, nie in feste Ordner oder ins Repo.
- Kein Test beeinflusst einen anderen: SQLite und Dateien in `tmp_path` je Test; eine Server-Datenbank bekommt eine
  Kennung je Lauf und Worker, die Fixture legt sie an und räumt sie ab. Die Worker-ID allein trennt nur Worker, nicht
  Tests desselben Workers.
- Gerüst mit einem grünen Beispieltest:

  ```python
  # tests/conftest.py
  import sqlite3

  import pytest


  @pytest.fixture
  def db(tmp_path):
      """Eigene SQLite-Datenbank je Test – unabhängig von Worker, Reihenfolge und Wiederholung."""
      con = sqlite3.connect(tmp_path / "test.db")
      yield con
      con.close()
  ```

  ```python
  # tests/test_beispiel.py
  def test_schreibt_nur_in_tmp(tmp_path):
      datei = tmp_path / "aus.json"
      datei.write_text("{}", encoding="utf-8")
      assert datei.read_text(encoding="utf-8") == "{}"
  ```

## Skill-Profil

Werte für die `CLAUDE.md` des neuen Projekts (Pfade an die Art anpassen; beim Werkzeug schreibt sie der Generator,
`-n auto` steht dort in `pyproject.toml`):

```
### Checks
- format: python -m ruff format --check . [**/*.py; pyproject.toml]
- lint: python -m ruff check . [**/*.py; pyproject.toml]
- tests: python -m pytest -n auto [<paket>/**; tests/**; pyproject.toml]
- start: python -m <paket> <befehl> [<paket>/**; pyproject.toml]

### Commit
- Pre-Commit-Checks: format; lint; tests; start

### Code
- Stacks: python
- Tests: format; lint; tests; start

### Doku
- Entscheidungs-Ort: docs/entscheidungen.md
```
