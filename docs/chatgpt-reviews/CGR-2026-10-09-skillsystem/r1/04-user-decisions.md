# Runde 1 – Entscheidungen Herbert (09.10.2026)

1. **„Lauffähig“ bei einer HA-Integration:** automatischer HA-Test (Integration lädt in einem Test-HA, Config-Flow
   läuft). Das echte Laden im laufenden HA macht Herbert danach selbst; nicht Pflicht des Generators.
2. **claude.ai:** Plan reicht; erzeugt wird nur in Claude Code (Pi oder PC).
3. **Pilot:** Python-Werkzeug mit optionalem SQLite, danach direkt HA-Integration (Python-Dienst, PostgreSQL, Karte,
   C# später).

Von Claude ohne Rückfrage entschieden (technisch): JSON-Erzeugungsauftrag als interne Schnittstelle; HA-Paket im
Konfigurationsordner bleibt eigener einfacher Weg außerhalb des Generators; `-n auto` bleibt (auf dem Pi gemessen),
Obergrenze nur als Hinweis in der Stack-Reference; Test-Isolation in beiden python.md als eigener Safe Patch korrigieren.
