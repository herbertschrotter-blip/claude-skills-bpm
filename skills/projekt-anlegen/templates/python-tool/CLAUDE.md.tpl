# {{name}}

Python-Werkzeug mit Befehlszeile; Fachlogik getrennt von Befehlszeile (`{{package}}/cli.py`) und Speicher
(`{{package}}/speicher.py`). Grundentscheidungen: `docs/entscheidungen.md`.

## Skill-Profil

- Profil-Version: 1
- Projekt-ID: {{slug}}
- Repo: none
- Branch-Policy: current

### Checks
- format: python -m ruff format --check . [**/*.py; pyproject.toml]
- lint: python -m ruff check . [**/*.py; pyproject.toml]
- tests: python -m pytest [**/*.py; pyproject.toml]
- start: python -m {{package}} status [{{package}}/**; pyproject.toml]

### Commit
- Format: [vX.Y.Z] <Modul>, <Typ>: <Kurztitel>
- Module: {{package}}={{package}}/**; Tests=tests/**; Doku=docs/**, README.md, CHANGELOG.md, CLAUDE.md
- Versionsquelle: pyproject.toml#project.version
- Versionsregel: none
- Push-Policy: allowed
- Pre-Commit-Checks: format; lint; tests; start
- Doku-Check: Funktion geändert → CHANGELOG.md; Entscheidung geändert → docs/entscheidungen.md

### Code
- Stacks: python
- Pflichtkontext: CLAUDE.md; docs/entscheidungen.md
- Aufgabenquelle: none
- Architekturregeln: none
- Tests: format; lint; tests; start
- Auslieferung: none
- Mockup-Policy: none
- Befund-Ort: none

### Doku
- Router: none
- Standard: none
- Pflichtdokumente: README.md; CHANGELOG.md; docs/entscheidungen.md
- Validierungsregeln: none
- Sitzungsabschluss: none
- Entscheidungs-Ort: docs/entscheidungen.md
