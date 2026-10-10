# {{name}}

Eigene Home-Assistant-Integration `{{package}}` (Ordner `custom_components/{{package}}/`). Fachlogik ohne Home
Assistant liegt in `custom_components/{{package}}/logik/` und hat eigene Tests. Grundentscheidungen:
`docs/entscheidungen.md`.

## Skill-Profil

- Profil-Version: 1
- Projekt-ID: {{slug}}
- Repo: none
- Branch-Policy: current

### Checks
- format: .venv/bin/python -m ruff format --check . [**/*.py; pyproject.toml]
- lint: .venv/bin/python -m ruff check . [**/*.py; pyproject.toml]
- logik: .venv/bin/python -m pytest -q -p no:cacheprovider tests/logik [custom_components/**; tests/logik/**]
- integration: .venv/bin/python -m pytest -q -p no:cacheprovider -n auto tests/integration [custom_components/**; tests/integration/**; requirements-ha.txt]

### Commit
- Format: [vX.Y.Z] <Modul>, <Typ>: <Kurztitel>
- Module: Integration=custom_components/**; Tests=tests/**; Doku=docs/**, README.md, CHANGELOG.md, CLAUDE.md
- Versionsquelle: custom_components/{{package}}/manifest.json#version
- Versionsregel: none
- Push-Policy: allowed
- Pre-Commit-Checks: format; lint; logik; integration
- Doku-Check: Funktion geändert → CHANGELOG.md; Entscheidung geändert → docs/entscheidungen.md

### Code
- Stacks: python
- Pflichtkontext: CLAUDE.md; docs/entscheidungen.md
- Aufgabenquelle: none
- Architekturregeln: none
- Tests: format; lint; logik; integration
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
