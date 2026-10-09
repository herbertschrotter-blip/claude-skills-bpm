## Runde 2

Canvas-Titel: "Review Runde 2". Gleiche Rolle und Regeln wie in Runde 1. Am Ende wieder:
✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen

## Repo-Zugriff

- **Repo:** `herbertschrotter-blip/claude-workbench`
- **Branch: `main`** — IMMER diesen Branch verwenden
- Runde 1 liegt unter `docs/chatgpt-reviews/CGR-2026-10-09-skillsystem/r1/` (deine Antwort, meine Einschätzung,
  Herberts Entscheidungen).

## Was aus Runde 1 gilt

Übernommen von dir: Bauweise C mit deterministischem Kern aus Bausteinen (Manifeste mit Voraussetzungen und
Konflikten, nicht unterstützte Kombinationen vorher abweisen), eigenes Skript nur mit Standardbibliothek, temporär
erzeugen → prüfen → übernehmen, nie überschreiben, erzeugte Projekte nie wieder anfassen; deine Grenzregel
„technische Funktionsfähigkeit vs. fachliches Verhalten“ samt Routing-Tabelle; kein eigener Generator-Skill; drei
Pflichtklärungen (Zweck, Ort, erste Fassung), Technik leitet Claude ab; Grundsatz-Prüfung in drei Ebenen,
Entscheidungen an `Doku.Entscheidungs-Ort`; nur die benötigte Datenbank, Schema-Version ab Tag 1, kein
Migrationsframework auf Vorrat; Abnahme in fünf Ebenen mit Starttest.

Herberts Entscheidungen:
1. „Lauffähig“ bei einer HA-Integration = automatischer HA-Test (Integration lädt im Test-HA, Config-Flow läuft,
   z. B. mit `pytest-homeassistant-custom-component`). Echtes Laden im laufenden HA macht Herbert selbst (braucht
   seinen Neustart) – nicht Pflicht des Generators.
2. claude.ai: Plan reicht, erzeugt wird nur in Claude Code.
3. Pilot: Python-Werkzeug mit optionalem SQLite, danach direkt HA-Integration (Python-Dienst, PostgreSQL, Karte, C#
   später) – seine echten Projekte sind HA-Integrationen und Karten.

Von mir entschieden: JSON-Erzeugungsauftrag ja (kurzlebig, validiert, Herbert sieht ihn nicht); HA-Paket im
Konfigurationsordner bleibt der einfache Weg außerhalb des Generators.

Mein Widerspruch zu `-n auto`: auf genau diesem Pi gemessen (4 Kerne, 16 GB, ha-baustelle): SQLite-Integrationstests
10:20 → 2:43, PostgreSQL 23:53 → 5:50, alles grün. `-n auto` bleibt; `--maxprocesses` nur als Hinweis für kleinere
Maschinen in der Stack-Reference.

Deinen Befund zur Test-Isolation (Worker-ID isoliert nicht Tests desselben Workers, parallele Läufe kollidieren)
korrigiere ich als eigenen Safe Patch in `skills/projekt-anlegen/references/stacks/python.md` und
`skills/code-erstellen/references/stacks/python.md`: Invariante „kein Test beeinflusst einen anderen“, SQLite
`tmp_path` je Test, PostgreSQL eindeutige Kennung je Lauf und Worker, Fixtures räumen ab.

## Aufgabe Runde 2 – konkret werden

1. **Erzeugungsauftrag (Pilot):** Schlag das JSON-Schema vor (Felder, Pflicht/optional, erlaubte Werte, Version).
   Welche Werte kommen aus den Antworten, welche aus dem Skill-Profil der aufrufenden Umgebung (Ablage,
   GitHub-Owner), welche leitet Claude ab?
2. **Bausteine und Manifest für den Pilot:** Welche Bausteine genau (z. B. `common`, `python-tool`, `storage-sqlite`,
   `ci-github`), was liegt in jedem (Dateiliste), wie sieht ein Manifest aus (Voraussetzungen, Konflikte,
   Platzhalter)? Wo liegt das alles im Repo, damit es im Plugin-Cache und im claude.ai-Zip nicht stört
   (`skills/projekt-anlegen/generator/…` oder außerhalb von `skills/`)?
3. **Walking Skeleton Python-Werkzeug:** Welche Beispiel-Funktion ist „technisch, ohne fachliche Bedeutung“ und läuft
   trotzdem durch CLI → Anwendung → Speicher? Wie sieht der Starttest aus? Welche Werkzeuge für Format/Lint (z. B.
   ruff) – angeheftet wie?
4. **Prüfung des Generators:** Wie testen wir ihn selbst (Unit-Tests des Skripts, Erzeugen jeder unterstützten
   Kombination in CI, darin Tests, Lint und Starttest)? Läuft das in der vorhandenen GitHub Action
   `.github/workflows/validate-skills.yml` mit oder als eigener Workflow?
5. **Änderungen an den Skills** (für das Regel-Inventar des Refactors): Gliederung der neuen SKILL.md von
   projekt-anlegen (welche Abschnitte, was wandert in welche Reference), die neue Description (≤ 1024 Zeichen,
   Entwurf bitte ausformulieren), das neue INDEX-Konfliktpaar projekt-anlegen ↔ code-erstellen, und was code-erstellen
   über die „Grundentscheidungen“ eines erzeugten Projekts wissen muss.
6. **HA-Integration als zweiter Schritt:** Was muss der Pilot schon vorsehen, damit die HA-Integration nur ein weiterer
   Baustein ist und kein Umbau des Generators?
