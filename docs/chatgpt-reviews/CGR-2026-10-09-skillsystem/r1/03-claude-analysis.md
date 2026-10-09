# Runde 1 – Einschätzung Claude

## Übernehmen (überzeugt)

- **C mit deterministischem Kern, Bausteine statt Vorlagen je Kombination:** Das ist besser als mein A. Manifeste mit
  Voraussetzungen und Konflikten halten die Zahl der Kombinationen klein; nicht unterstützte werden vor der Erzeugung
  abgewiesen.
- **Eigenes kleines Skript (Standardbibliothek)**, temporär erzeugen, prüfen, erst dann übernehmen; nie überschreiben;
  Generator fasst erzeugte Projekte nie wieder an.
- **Grenze als prüfbare Regel** („technische Funktionsfähigkeit“ vs. „fachliches Verhalten“) samt Routing-Tabelle –
  direkt als Eval-Fälle und INDEX-Konfliktpaar verwendbar. Kein eigener Generator-Skill.
- **Weniger Fragen:** drei Pflichtklärungen (Zweck, Ort, erste Fassung), Technik leitet Claude ab und erklärt sie im
  Plan. Die Frage „Soll es Daten dauerhaft speichern?“ statt „SQLite oder PostgreSQL?“ passt genau zu Herbert.
- **Grundsatz-Prüfung in drei Ebenen** (Generator / Auswahlfragen / Projektdoku); Entscheidungen an
  `Doku.Entscheidungs-Ort` statt in README und CLAUDE.md doppelt.
- **Nur die benötigte Datenbank**, Schema-Version ab Tag 1, kein Migrationsframework auf Vorrat.
- **Abnahme in fünf Ebenen**, mit Starttest statt nur pytest.
- **claude.ai:** dort nur Plan, Generierung in Claude Code – Herbert arbeitet ohnehin fast nur in Claude Code.

## Berechtigter Befund an den heutigen Skills

- Die Test-Datenbank je Worker (`<projekt>_test_<worker_id>`) in `projekt-anlegen/references/stacks/python.md` und die
  Regel „Isolation je Worker“ in `code-erstellen/references/stacks/python.md` isolieren nur Worker, nicht Tests
  desselben Workers; zwei parallele Läufe (CI und lokal gegen dieselbe PostgreSQL) können kollidieren. Richtig ist die
  Invariante „kein Test beeinflusst einen anderen“: SQLite `tmp_path` je Test; PostgreSQL eindeutige Kennung je Lauf
  und Worker, Fixtures räumen ab. → Safe Patch an beiden python.md, unabhängig vom Generator.

## Teilweise Widerspruch

- **`-n auto` auf dem Pi:** In ha-baustelle gemessen (4 Kerne, 16 GB): SQLite 10:20 → 2:43, PostgreSQL 23:53 → 5:50,
  alles grün. Für den Pi ist `-n auto` also belegt. Eine Obergrenze (`--maxprocesses`) gehört trotzdem als Hinweis in
  die Stack-Reference für kleinere Maschinen; kein fester Wert.
- **Pilot „Python CLI ohne Datenbank“ zuerst:** technisch sauber, aber Herberts echte Projekte sind HA-Integrationen
  und -Karten. Vorschlag: Pilot Python-Werkzeug mit optionalem SQLite (beweist Generator, Persistenz, Isolation), danach
  direkt HA-Integration statt Python-Dienst und PostgreSQL.

## Zu den Rückfragen

1. **HA-Integration lauffähig:** automatisierter Test mit `pytest-homeassistant-custom-component` (Integration lädt,
   Config-Flow läuft) als Abnahme; echtes Laden im laufenden HA braucht einen Neustart, den nur Herbert auslöst – als
   Praxistest, nicht als Pflicht des Generators.
2. **Projekte ohne eigenes Repo** (HA-Paket im Konfigurationsordner): ja, als eigener, einfacher Pfad, der heute schon
   existiert („Ordner im aktuellen Repo“); der Generator ist für eigenständige Anwendungen.
3. **claude.ai:** Plan genügt (Entscheidung Herbert offen).
4. **JSON-Vertrag:** ja, als kurzlebiger Erzeugungsauftrag; technisch, Herbert muss ihn nicht sehen.

## Entscheidungen für Herbert

- Was heißt „lauffähig“ bei einer HA-Integration?
- Muss der Generator auch bei claude.ai im Browser/Handy laufen, oder reicht Claude Code?
- Pilot: Python-Werkzeug mit SQLite, dann HA-Integration – oder gleich mit der HA-Integration beginnen?
