# Stack Python

Arten, Orte und Grunddateien für neue Python-Projekte. Regeln für Code und Tests im laufenden Projekt stehen bei
code-erstellen (`skills/code-erstellen/references/stacks/python.md`). Läuft das Werkzeug neben Home Assistant, gilt
zusätzlich `references/stacks/home-assistant.md` (Art Python-Werkzeug).

## Arten

| Art | Wofür | Grunddateien |
|---|---|---|
| Werkzeug | ein Aufruf, Ein- und Ausgabe über Dateien oder JSON | `<paket>/__init__.py`, `<paket>/__main__.py`, `tests/`, `pyproject.toml` |
| Bibliothek | von anderen Projekten genutzt | `src/<paket>/`, `tests/`, `pyproject.toml` mit Version |
| Dienst | läuft dauerhaft, oft mit Datenbank | wie Bibliothek, dazu Konfiguration über die Umgebung (`.env.example`; `.env` nie ins Repo) |

## Grunddateien

- `pyproject.toml`: Name, Version, `requires-python`; Testwerkzeuge als optionale Abhängigkeiten
  (`[project.optional-dependencies] test = [...]`) mit fester Version.
- `README.md` mit Aufruf und Testbefehl.
- `.gitignore`: `__pycache__/`, `*.pyc`, `.venv/`, `.pytest_cache/`, `build/`, `dist/`, `*.egg-info/`, `.env`.

## Testgerüst (parallel-fähig)

- `pytest` und `pytest-xdist` mit fester Version (`==`). Die aktuelle Version beim Anlegen nachsehen
  (`pip index versions pytest-xdist`), nicht raten.
- Befehl: `python -m pytest -n auto`. `-n auto` misst die Kerne zur Laufzeit, auch virtuelle; keine Zahl eintragen,
  auch nicht im Profil. Bei sehr kleinen Läufen kostet das ein, zwei Sekunden Start, dafür muss später nichts
  umgestellt werden.
- Isolation je Test: Tests schreiben nur in `tmp_path`, nie in feste Ordner oder ins Repo.
- Isolation je Worker: geteilte Ressourcen (Test-Datenbank, Datei, Port) tragen die Worker-ID im Namen.
- Gerüst mit einem grünen Beispieltest:

  ```python
  # tests/conftest.py
  import pytest


  @pytest.fixture(scope="session")
  def db_name(worker_id):
      """Eigene Test-Datenbank je Worker (worker_id von pytest-xdist: gw0, gw1, …; ohne -n: master)."""
      return f"<projekt>_test_{worker_id}"
  ```

  ```python
  # tests/test_beispiel.py
  def test_schreibt_nur_in_tmp(tmp_path):
      datei = tmp_path / "aus.json"
      datei.write_text("{}", encoding="utf-8")
      assert datei.read_text(encoding="utf-8") == "{}"
  ```

## Skill-Profil

Werte für die `CLAUDE.md` des neuen Projekts (Pfade an die Art anpassen):

```
### Checks
- tests: python -m pytest -n auto [<paket>/**; tests/**; pyproject.toml]

### Commit
- Pre-Commit-Checks: tests

### Code
- Stacks: python
- Tests: tests
```
