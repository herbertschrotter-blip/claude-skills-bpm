## Runde 3

Canvas-Titel: "Review Runde 3". Gleiche Rolle und Regeln wie bisher. Am Ende wieder:
✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen

## Repo-Zugriff

- **Repo:** `herbertschrotter-blip/claude-workbench`
- **Branch: `main`** — IMMER diesen Branch verwenden
- Runden 1 und 2 liegen unter `docs/chatgpt-reviews/CGR-2026-10-09-skillsystem/` (r1, r2: deine Antworten, meine
  Einschätzungen, Herberts Entscheidungen).

## Stand nach Runde 2

Deine Runde 2 übernehme ich fast vollständig: Generator ohne Stack-Sonderfälle, JSON-Auftrag v1 (fünf Felder, streng,
keine Befehle), strukturierter Renderer für gemeinsame Dateien, Walking Skeleton „status“ mit Starttest und echtem
SQLite-Integrationstest, Ruff, Versionskatalog im Generator, Prepare / Verify & Publish mit Staging, eigener Workflow
`test-project-generator.yml`, deine Regel für code-erstellen, Umsetzungsreihenfolge aus Abschnitt 8. Deine vier
Rückfragen habe ich so entschieden: ci-github standardmäßig bei GitHub-Repos; kleine Herkunftsdatei im erzeugten
Projekt (nie aktualisiert); neue Abhängigkeitsversionen nur nach grünen Kombinationstests und Freigabe über
skill-pflege; HA mit SQLite später über eigenen Adapter.

Herbert will vor dem Bau noch eine Runde. Offen sind diese Punkte:

### 1. Description

Dein Entwurf (927 Zeichen) verliert zwei Auslöser, die heute zünden und Routing-Eval-Fälle haben:
`quality/evals/projekt-anlegen-clone` (vorhandenes GitHub-Repo holen und einrichten) und die deutschen Sätze
„neues Projekt“ / „ich will X bauen, weiß aber nicht wie“ (`projekt-anlegen-unklar`). Herbert schreibt fast immer
Deutsch und umgangssprachlich. Mein Gegenentwurf (1018 Zeichen – zu knapp an der Grenze 1024):

> Legt neue Projekte an und richtet Repos für diese Skills ein – nach Stack (z. B. HA-Paket, -Karte, -Integration,
> Python-Werkzeug). Klärt mit wenigen Fragen Zweck, Ort und erste Fassung, prüft den Bestand und erzeugt für
> unterstützte Stacks ein lauffähiges, getestetes Grundgerüst ohne Fachlogik (Tests, Startprüfung, CLAUDE.md mit
> Skill-Profil); erstellt oder klont nach Rückfrage das GitHub-Repo und trägt das Projekt in die Übersicht ein. Use
> when users want to start, set up, scaffold, anlegen, aufsetzen or einrichten a new project, integration, card,
> dashboard or tool, say "neues Projekt" or "ich will X bauen, weiß aber nicht wie", or want a new GitHub repo
> created, an existing repo cloned, or an existing repo eingerichtet for these skills (Skill-Profil, Configs). Do not
> trigger for features or changes inside an existing project (code-erstellen), UI mockups (mockup-erstellen), new or
> changed skills (skill-neu, skill-pflege), ClickUp tasks (tracker), documentation only (doc-pflege), or plain git
> commands.

Bitte: eine Fassung um 900 Zeichen, die alle Auslöser der sieben vorhandenen Eval-Fälle hält
(`quality/evals/projekt-anlegen-*`, Prompts in `prompt.md`) und die Abgrenzungen gegen code-erstellen, mockup-erstellen
und skill-neu nicht schwächt. Was darf raus (z. B. „trägt in die Übersicht ein“, Stack-Beispiele)?

### 2. Neue Routing-Eval-Fälle

Ich will die sieben Fälle auf etwa 17 erweitern (Format: `quality/README.md`, Muster unter `quality/evals/`). Mein
Vorschlag – bitte ergänzen, streichen, umformulieren (Herbert schreibt kurz und umgangssprachlich):

Soll auslösen: „neues Projekt: Bewässerungssteuerung“ · „mach mir ein Repo für ein kleines Python-Tool, das CSVs
zusammenführt“ · „ich will eine eigene Karte für meinen Pool bauen“ · „set up a new Home Assistant integration for my
heat pump“ · „leg ein Python-Werkzeug mit Datenbank an, das meine Stromzähler speichert“.

Darf nicht auslösen: „leg in ClickUp ein neues Projekt an“ (tracker) · „schreib die README für das neue Projekt“
(doc-pflege) · „öffne mein Projekt ha-baustelle“ (sitzung) · „commit und push das neue Repo“ (git-commit-helper) ·
„die neue Integration soll jetzt Baustellenstunden berechnen“ (code-erstellen, deine Grenze aus Runde 1).

### 3. Ordner und Lieferung

- Im Repo gibt es schon `skills/sitzung/scripts/` (Skript neben SKILL.md). Ich würde `skills/projekt-anlegen/scripts/`
  (generate.py, validate.py, Tests) und `skills/projekt-anlegen/templates/` (Bausteine, Manifeste, Versionskatalog)
  nehmen statt `generator/` – passt das, oder spricht etwas für deine Struktur?
- Upload bei claude.ai: dort läuft der Generator nicht. Lieferung nur SKILL.md + `references/` (Regel in
  `skills/skill-pflege/references/delivery.md` ergänzen) – oder doch alles mitliefern?
- Das Prüfskript `tools/validate-skills.ps1` zählt Markdown unter `references/`; prüft es Ordner wie `templates/` mit
  `.tpl`-Dateien mit, und muss es das (z. B. Platzhalter, ASCII, keine Projektwerte)?

### 4. Kleinere Details

- Herkunftsdatei im erzeugten Projekt: Name und Inhalt (Vorschlag `.projekt-anlegen.json` mit Generator-Version,
  template.id/version, Bausteinen, Datum)?
- TOML-Renderer: Die Standardbibliothek kann TOML nur lesen (`tomllib`). Ein eigener kleiner Schreiber für den
  benötigten Ausschnitt von `pyproject.toml` – oder `pyproject.toml` doch als eine Vorlage je Baustein-Kombination?
- Der Generator läuft auf dem Pi (Linux, Python 3.12) und auf Windows (Store-Python 3.12). Worauf muss das Skript
  achten (Zeilenenden, Pfade, atomares Verschieben über `os.replace` vs. Ordner)?

## Aufgabe

Zu 1–4 konkrete Antworten, bei der Description eine fertige Fassung mit Zeichenzahl. Danach soll gebaut werden;
sag, falls aus deiner Sicht noch etwas den Start blockiert.
