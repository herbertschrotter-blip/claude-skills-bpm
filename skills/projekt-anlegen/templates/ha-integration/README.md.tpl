# {{name}}

Eigene Home-Assistant-Integration. Angelegt als lauffähiges Grundgerüst: Einrichtung über die Oberfläche, ein
technischer Status-Sensor, Diagnose-Download, Übersetzungen (de, en). Die Fachlogik kommt danach.

## Entwickeln

Die Tests gegen Home Assistant brauchen Python 3.14 und laufen unter Linux (unter Windows in WSL).

```sh
uv venv --python 3.14 .venv
uv pip install --python .venv/bin/python -r requirements-logik.txt
uv pip install --python .venv/bin/python -r requirements-ha.txt
.venv/bin/python -m ruff format --check .
.venv/bin/python -m ruff check .
.venv/bin/python -m pytest -q tests/logik
.venv/bin/python -m pytest -q -n auto tests/integration
```

Läuft das auf Home Assistant OS, gehört zu beiden `uv pip install` noch `--index-strategy unsafe-best-match` (dort
ist ein zusätzlicher Paketindex eingetragen). Die Fachlogik-Tests unter `tests/logik` brauchen kein Home Assistant.

## In Home Assistant laden

Den Ordner `custom_components/{{package}}` in den Ordner `custom_components` der Home-Assistant-Konfiguration
kopieren, Konfiguration prüfen und Home Assistant neu starten. Danach unter Einstellungen → Geräte & Dienste →
Integration hinzufügen → „{{name}}“.

Grundentscheidungen: [docs/entscheidungen.md](docs/entscheidungen.md).
