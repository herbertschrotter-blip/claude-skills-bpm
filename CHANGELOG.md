# CHANGELOG

Alle relevanten Änderungen an den Skills werden hier dokumentiert.

Format: Umgekehrte Chronologie (neueste zuerst). Versions-Tags folgen Semantic Versioning (`[vMAJOR.MINOR.PATCH]`). Phasen-Tags beziehen sich auf den Skill-System-Refactor aus dem ChatGPT-Review `CGR-2026-04-skillsystem`.

---

## [v0.29.0] — 2026-09-16

- **skills/skill-pflege/SKILL.md, Feature:** umgebungsneutral – Cowork (view/DC/Artifact-Paar) und Claude Code (Read/Edit, Lieferung per SendUserFile, Zip bei references) im selben Ablauf; Skill-Liste aus `skills/` des Repos; Memory-Cleanup mit Claude-Code-Weg; Auswahlfrage statt `ask_user_input_v0`
- Neu: Regel 6 description ≤ 1024 Zeichen (Upload-Limit claude.ai) mit Messung vor jeder Lieferung; Regel 12a CHANGELOG/INDEX/Commit/Push als Teil jeder Skill-Änderung (Schritt 5a); Regel 13 Zip-Lieferung bei references; 14b: references-Änderungen brauchen wieder eine Lieferung (alte Ausnahme gestrichen); Diff-Report um description-Länge, Dateiliste, Version/Hash erweitert
- Neu: **Regel 21 Split-Prüfung** (Herberts Vorschlag) – Kriterien, wann Teile eines Skills nach `references/` gehören (Größe, nur ein Kommando/eine Umgebung/ein Stack, Projektwerte, Wiederholungen), Muster SKILL.md = Routing + Kernregeln, Ablauf nur mit Freigabe und durch Verschieben statt Neuschreiben; Auto-Issue-Erkennung um Werkzeug-/Projektbindung und Split-Kandidat ergänzt
- Regel 4: zweite Ausnahme „Neutralisieren“ (wesentliche Teile umbauen, Rest Original)
- Quelle: Heidi-Sitzung Claude Code 16.09.2026

## [v0.28.1] — 2026-09-16

- **skills/code-erstellen/SKILL.md, Fix:** Frontmatter-description auf unter 1024 Zeichen gekürzt (claude.ai lehnte den Upload ab: „field description must be at most 1024 characters“)

## [v0.28.0] — 2026-09-16

- **skills/code-erstellen, Feature:** Stack-Referenzen `references/stacks/<key>.md` (Herberts Vorschlag): sprachspezifische Schichten/Kopplung, Modus-Beispiele, Impact-Check-Lesart, Blocking-Dateien, Tests, Ausgabe, typische Fehler – je Sprache eine Datei, erweiterbar ohne Skill-Änderung. Start: `csharp-wpf` (BPM), `typescript-lit`, `home-assistant-yaml`, `python` (Heidi)
- Code-Profil bekommt das Feld **Stacks** (Schlüsselliste, mehrere erlaubt) + Build/Lint; der Skill lädt die Referenzen vor Modus/Impact/Blocking; fehlende Referenz → Auswahlfrage statt raten
- SKILL.md: BPM-/Heidi-Klammern aus Modus, Entry Points, Impact Check, Blocking, Tests, Auslieferung entfernt → jetzt wirklich neutral; VERBOTEN „Sprachspezifisches in die SKILL.md“
- Heidi CLAUDE.md: Zeile `Stacks: typescript-lit, home-assistant-yaml, python`
- Quelle: Heidi-Sitzung Claude Code 16.09.2026

## [v0.27.1] — 2026-09-16

- **skills/code-erstellen/SKILL.md, Fix:** letzte wörtliche `ask_user_input_v0`-Stelle im Tracker-Abgleich → Auswahlfrage

## [v0.27.0] — 2026-09-16

- **skills/code-erstellen/SKILL.md, Feature:** projektneutral über ein **Code-Profil** (Abschnitt `## Code-Profil` in der CLAUDE.md des Repos: Stack, Pflicht-Docs, Aufgabenquelle, Schichten/Kopplung, Tests, Auslieferung, Mockup-Pflicht, Notiz-Ort, Pflicht-Branch); ohne Profil weiter INDEX.md (BPM-Weg). Modus-Kriterien, Impact Check, Blocking Conditions und Entry Points stack-neutral mit BPM- und Heidi-Lesart
- Neu: Schritt 2 „Aufgabenquelle laden“ (Akzeptanz → Testfälle), Schritt 7b **Tests** (Befehl aus dem Profil, rot = Blocking, Claude Code führt aus), Schritt 9b **Auslieferung**, **Mockup-Hook** bei Deep + UI; Tests-Spalte in der Modus-Übersicht; Doku-Zeilen = Doku-Checkliste des Commit-Profils
- Werkzeugneutral: Auswahlfrage statt `ask_user_input_v0`, Branch aus der Shell (`git branch --show-current`, Pflicht-Branch aus dem Profil), Arbeitsverzeichnis in Claude Code = Repo-Wurzel, Ausgabeformat nur Cowork, Auto-Anker nur Cowork (Claude Code: Auswahlfrage tracker neu / Notiz-Ort), Anker-Präfix aus der Tracker-Config
- Heidi-Repo: Abschnitt `## Code-Profil` in CLAUDE.md angelegt; INDEX.md und docs/project-architecture.md nachgezogen
- Quelle: Heidi-Sitzung Claude Code 16.09.2026

## [v0.26.0] — 2026-09-16

- **skills/tracker, Feature:** Präfix wird pro Projekt festgelegt – Titel `<PRÄFIX>-NNN | KÜRZEL | Kurztitel` und Anker `[<PRÄFIX>-ANCHOR-…]` als Platzhalter in SKILL.md und allen Abläufen (create/start/complete/issue/update/split/anti-patterns), Präfix aus `projects/<[PROJECT]>/clickup-lists.md` (BPM `BPM`, Heidi `DX`); Zähler `Next` je Umgebung (Cowork Memory `[CLICKUP]`, Claude Code Tracker-Profil in CLAUDE.md)
- Falsche Heidi-Beispiele („Bauplan-Nummer, keine Anker, keine Felder“) korrigiert; die Sonderabläufe ohne Zähler/Felder/Anker sind jetzt als Ausnahme gekennzeichnet, Standard ist das volle Schema
- Werkzeugneutral: `ask_user_input_v0` → „Auswahlfrage“ in allen references (Kernregel nennt beide Werkzeuge), Memory-Entfernen und Skill-Artefakt mit Claude-Code-Weg (Memory-Ordner, SendUserFile), „Per DC“ → Shell der Umgebung, `ToolSearch`-Variante in clickup-tools.md
- clickup-tools.md: Abschnitt mit festen Workspace-/Space-/Listen-IDs entfernt → Verweis auf `projects/<[PROJECT]>/clickup-lists.md`; anker-system.md: Präfix-Hinweis
- projects/bpm/clickup-lists.md: Abschnitt „Präfix (Nummern und Anker)“ ergänzt
- Quelle: Heidi-Sitzung Claude Code 16.09.2026 (Herbert: „das Präfix sollte pro Projekt festgelegt werden“)

## [v0.25.4] — 2026-09-16

- **projects/heidi, Chore:** Feld-IDs und Option-IDs der 11 Custom Fields (von Herbert angelegt) in `clickup-fields.md` eingetragen, Feld-Regeln (Zielversion, Komponente, Docs, Commit-Felder, Anker); alle 55 DX-Aufgaben in ClickUp befüllt

## [v0.25.3] — 2026-09-16

- **projects/heidi, Fix:** Herbert: Skill-Schema gilt vollständig – Nummernschema `DX-NNN | KÜRZEL | Kurztitel` (Kürzel KARTE/BACKEND/DOKU/TOOLS, Phasen als Parents ohne Nummer), alle 10 Custom Fields wie BPM (IDs folgen, sobald Herbert sie in ClickUp angelegt hat), Chat-Anker `[DX-ANCHOR-…]`; 55 Aufgaben umbenannt (DX-001…DX-055), Next DX-056. Ersetzt die Fassung „keine Felder, keine Nummern“ aus v0.25.0

## [v0.25.2] — 2026-09-16

- **projects/heidi, Chore:** Beschreibungs-Muster = Skill-Template mit Heidi-DoD (Herberts Entscheidung), Checkbox-Regeln je Status, Meta-Kurzform für Phasen; Nummernschema um `Backend:`, `[PC]` und Befund-Nummern ergänzt. Alle 62 Aufgaben der Liste „dreame_x60 – Bauplan“ am 16.09. auf dieses Muster umgeschrieben (Titel vereinheitlicht, Struktur und Status unverändert)

## [v0.25.1] — 2026-09-16

- **skills/tracker/references, Change:** Abläufe für Projekte ohne Zähler, Custom Fields und Chat-Anker ergänzt (additiv, Original bleibt) – create-task: Nummer aus Kontext (Bauplan-Nummer), eine Liste, Beschreibung nach Projektmuster, Quittung ohne Anker; start-task: Status-Wert aus `clickup-lists.md` Übergänge (Heidi `in development`); complete-task: Status `testing` statt `shipped`, Kommentar mit Version und Hash statt Felder, Hash in der Shell der Umgebung (DC oder Bash), Folgeoptionen als Auswahlfrage; chat-url-handling: entfällt ohne Chat-Felder oder ohne Chat-Suche (Claude Code); search-and-status: Anzeige und `tracker next` ohne Felder (Bauplan-Reihenfolge, `testing` zuerst)
- SKILL.md: Memory-Abschnitt `[CLICKUP]` und Chat-URL-Frage nur für Projekte mit Zähler bzw. Chat-Feldern
- Quelle: Heidi-Sitzung Claude Code 16.09.2026

## [v0.25.0] — 2026-09-16

- **skills/tracker/SKILL.md, Feature:** projektneutral – Nummernschema, Anker-Präfix und Custom-Field-IDs sind Profilwerte aus `projects/<[PROJECT]>/` (BPM: BPM-NNN + `[BPM-ANCHOR-…]` + 10 Felder; Heidi: Bauplan-Nummer im Titel, keine Anker, keine Felder → Quittung ohne Anker, Commit-Hash als Kommentar); Referenz-Anker-Regel gilt nur für Projekte mit Ankern
- Werkzeugnamen raus: `ask_user_input_v0` → „Auswahlfrage“ (Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion`), DC → Shell der Umgebung, `tool_search` → Werkzeugsuche der Umgebung (Claude Code `ToolSearch select:`)
- Projektkennung je Umgebung: Claude Code liest Abschnitt `## Tracker-Profil` in der CLAUDE.md des Repos, Cowork weiter den `[PROJECT]`-Memory-Eintrag; Fallback-Ablauf entsprechend
- Kommando-Tabelle mit `<Task-ID>` statt `<BPM-NNN>`; zwei neue VERBOTEN-Punkte (Werkzeuge/Umgebung fest annehmen, BPM-Schema für andere Projekte annehmen)
- **projects/heidi/** neu: README, clickup-lists (Space Smart Home, Liste dreame_x60 – Bauplan, 9 Status, Übergänge start→in development, done→testing), clickup-fields (keine Felder, Beschreibungs- und Kommentarmuster), memory-format (CLAUDE.md-Abschnitt statt Memory)
- references/batch-protocol.md: feste Feld-IDs als BPM-Beispiel gekennzeichnet; alle übrigen references unverändert (BPM-Beispiele bleiben Muster)
- Quelle: Heidi-Sitzung Claude Code 16.09.2026

## [v0.24.1] — 2026-09-16

- **skills/git-commit-helper/SKILL.md, Fix:** vier Lücken aus der Bewertung nach dem Neutral-Umbau – (1) Schritt 1a: Versionsdatei (Versionsquelle des Profils) wird hochgezählt und gehört in denselben Commit; (2) Schritt 1b + Regel 9: Doku-Checkliste vor der Commit-Sequenz statt nach dem Push; (3) Abschnitt „Wenn ein Glied der Sequenz fehlschlägt“: Abbruch am roten Glied, Ursache nennen, kein Teil-Commit; (4) Modul-Regel (Hauptmodul bei mehreren, sonst zwei Commits) und zweite Message-Zeile beschrieben
- Klein: Typen Test und Chore ergänzt; Regel 11 (Versionsdatei im selben Commit) und 12 (ein Block je Commit bei mehreren Commits)
- Alles Übrige unverändert (Herbert: „nur die wesentlichen Teile umbauen, Rest bleibt Original“)
- Quelle: Heidi-Sitzung Claude Code 16.09.2026

## [v0.24.0] — 2026-09-16

- **skills/git-commit-helper/SKILL.md, Feature:** projektneutral – Format `[vX.Y.Z] Modul, Typ: Kurztitel` bleibt fest, alles Projektspezifische kommt aus einem **Projektprofil** (Abschnitt `## Commit-Profil` in der CLAUDE.md des Repos: Modul-Namen, Versionsquelle, Bump-Regel, Doku-Checkliste); fehlt es, sucht der Skill docs/, *.md und Versionsdateien im Repo und bietet per Auswahlfrage an, das Profil anzulegen
- Bump-Regel des Profils darf die Typenliste überschreiben (z. B. Vorabversion: jede Änderung zählt hoch); Aufgabennummern gehören in den Kurztitel oder die zweite Zeile, nie vor die Version
- Werkzeugnamen raus: `ask_user_input_v0` → „Auswahlfrage“ (Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion`), Desktop Commander/cc-steuerung → Shell der Umgebung, Arbeitsverzeichnis per `git rev-parse --show-toplevel`
- Doku-Checkliste: BPM-Liste bleibt als Beispiel, zweites Beispiel Bauplan/HANDOFF (Heidi); Testbefehl als erstes Glied der Sequenz, wenn das Projekt Tests vor dem Commit verlangt
- Zwei neue Verbote: Versionsquelle/Doku raten, Werkzeugnamen fest verdrahten; Regel 10 Projektprofil lesen
- Erster Einsatz außerhalb BPM: herbert-smarthome-v2 (Heidi) mit Commit-Profil in CLAUDE.md
- Quelle: Heidi-Sitzung Claude Code 16.09.2026 (Herbert: „kann ich diese Skills nicht neutral machen?“)

## [v0.22.3] — 2026-04-29

- **skills/tracker/SKILL.md, Fix:** Description triggert jetzt auch auf "issue erstellen" / "task anlegen" / "ClickUp-Eintrag"
- Hintergrund: User-Beobachtung in Claude Code — "neues issue clickup erstellen" hat tracker-Skill nicht ausgelöst
- Diagnose: Wort "issue" fehlte komplett in Description, obwohl Skill den Befehl `tracker issue <skill>: <Titel>` mit eigener Reference unterstützt
- Hybrid-Description-Pattern angewandt (deutsche Trigger-Verben + englische Satzstruktur), wie bei code-erstellen-001, doc-pflege-001, mockup-erstellen-001 in v0.20.x
- 1 Stelle geändert: nur Frontmatter-Description, Body unverändert
- Two-Place-Pflege: Repo + Artifact für `/mnt/skills/user/`
- Schließt: ClickUp `86c9jtmk0` (tracker-011)
- Quelle: BauProjektManager Teil 34

## [v0.22.2] — 2026-04-29

- **skills/chatgpt-review/SKILL.md, Refactor:** CGR-ID-Schema von `YYYY-MM` auf `YYYY-MM-DD` umgestellt
- Begründung: Mehrere Serien können im selben Monat starten — Tag macht ID eindeutig und chronologisch sortierbar
- 6 Stellen im Skill-Body angepasst: ID-Schema-Block, Ablagestruktur, Serie-starten Schritt 2/4/5, Runde-starten Pfad, Formatierungs-Block, VERBOTEN-Liste
- Themen-Enum unverändert
- Two-Place-Pflege: Repo + Artifact für `/mnt/skills/user/`
- BPM-Repo-Anpassungen parallel: 4 alte CGR-Ordner umbenannt auf `CGR-2026-04-22-*`, neuer Ordner `CGR-2026-04-29-cc-vs-dc/`, INDEX.md angepasst
- Quelle: BauProjektManager Teil 34

## [v0.22.1] — 2026-04-29

- **skills/git-commit-helper/SKILL.md, Fix:** One-Block-Regel für Commit-Sequenzen
- **Schritt 2 umstrukturiert:** Komplette Commit-Sequenz in EINEM Code-Block, nicht in mehreren
- **PowerShell-Variante** (Default, `;`-Trenner) und **Bash-Variante** (`&&`-Trenner) explizit dokumentiert
- `git log -1 --format="%h %s"` als letztes Glied der Sequenz, damit Commit-Hash sofort sichtbar
- **Regel 5** geändert von „cd nur beim ersten Block" zu „Komplette Commit-Sequenz in EINEM Code-Block"
- **VERBOTEN-Liste erweitert:** Mehrere Code-Blöcke für eine Commit-Sequenz / Erklärungen zwischen Befehlen
- Two-Place-Pflege: Repo + Artifact für /mnt/skills/user/
- Schließt: ClickUp `86c9grk8h` (git-commit-helper-001)
- Beobachteter Fall: P0.3 README-Refactor 2026-04-25, Commit-Sequenz in 5 separaten Blöcken
- Quelle: BauProjektManager Teil 34

## [v0.22.0] — 2026-04-29

- **docs/fragilitaeten-und-fruehwarn.md (neu), Docs:** P3.2 Fragilitäten-und-Frühwarn-Doku angelegt
- 4 Sektionen mit Indikatoren, Sofortmaßnahmen, Beispielen und Gegenbeispielen:
  1. cc-steuerung-Pfad-/Modalitätsfragilität (Top 1)
  2. Tracker-Anker / Task-Scope-Disziplin (Top 2)
  3. Memory-Schatten-Backlog (verweist auf MEMORY-RUBRIKEN.md Anhang)
  4. Frühphasen-Verstoss
- **INDEX.md:** Neue Sektion 10 "Fragilitäten und Frühwarn-Indikatoren" mit
  Übersichts-Tabelle und Verweis auf Volldoku
- **chat-wechsel/SKILL.md:** Memory-Scan Schritt 4 erweitert um
  Fragilitäten-Check beim Handover (Two-Place-Pflege: Repo + Artifact für
  /mnt/skills/user/)
- Schließt: ClickUp `86c9gmkd5` (P3.2 Frühwarn-Indikatoren dokumentieren)
- Roadmap: P3 Doku-Hygiene → P3.1 + P3.2 done → P3 Eltern-Task kann auf
  done gesetzt werden
- Quelle: CGR-2026-04-skillsystem-r6 Kapitel 4
- Version-Bump MINOR: neue Doku-Datei + Skill-Erweiterung
- Quelle: BauProjektManager Teil 34

## [v0.21.0] — 2026-04-29

- **MEMORY-RUBRIKEN.md, Docs:** P3.1 Memory-Eskalation geschärft + Frühwarn-Indikatoren
- Lifecycle-Abschnitt: Eskalations-Aktion in 3 Schritten konkretisiert
  (1. tracker neu, 2. Memory-Eintrag entfernen, 3. Memory-Ursprung im Task-Body
  vermerken)
- Neuer Abschnitt „Hygiene-Prüfung beim Handover“ mit Verweis auf
  `chat-wechsel` Phase 4.1
- Neuer Anhang „Frühwarn-Indikatoren“ (4 Indikatoren aus ChatGPT-Review
  CGR-2026-04-skillsystem-r6 Kapitel 4) mit konkreter Reaktion pro Indikator
- Schließt: ClickUp `86c9gmkcp` (P3.1 Memory-Rubriken-Eskalation)
- Roadmap: P3 Doku-Hygiene → P3.1 done (P3.2 Frühwarn-Indikatoren bleibt offen
  als separater Punkt für Skill-Code-Implementierung in `chat-wechsel`/`tracker`)
- Version-Bump MINOR: neuer Anhang strukturell hinzugefügt
- Quelle: BauProjektManager Teil 34

## [v0.20.7] — 2026-04-29

- **evals, Docs:** Methodik-Anleitung für Smoke-Runs (chat-wechsel-001)
- Neue Datei `evals/methodik-anleitung.md` (171 Zeilen):
  - Standard-Setup (frischer Chat, Memory aus, eine Query pro Chat)
  - Demonstrativ-Bezug-Regel mit Beispielen aus Smoke-Run 2026-04-28
  - chat-wechsel-Spezialfall (braucht Vor-Konversation)
  - Diagnose-Checkliste "Test-Setup-Bias vs. echter Skill-Bug"
  - Snapshot-Format
  - Re-Test-Workflow nach Skill-Refactor
  - Bias-Hinweis: Selbst-Sim ≠ echter Re-Test
- Header-Notiz in `evals/smoke-all-skills.md` mit Verweis auf methodik-anleitung
- Hintergrund: Im Smoke-Run 2026-04-28 wurden 4 von 8 FAILs durch Test-Setup-Bias verursacht (MU-07, DOC-06, AUD-07, CE-07-Re-Test). Diese Cases sind in leeren Sessions nicht testbar, weil sie Demonstrativ-Bezug haben. Mit Vor-Kontext alle PASS.
- Schließt: ClickUp `86c9hyt0c` (chat-wechsel-001)
- KEIN Skill-Refactor — reine Doku-Anleitung, kein Re-Test nötig
- Quelle: BauProjektManager Teil 33

## [v0.20.6] — 2026-04-29

- **mockup-erstellen, Fix:** Description-Refactor — Verb-Inventar + Multi-Intent (mockup-erstellen-001)
- Neue Verben (deutsch): mocken, entwerfen, skizzieren, zeigen, visualisieren, layouten
- Neue Substantive: mockups, screen designs, UI proposals, layout drafts, dialog sketches, tab/panel arrangements
- Neuer Multi-Intent-Hinweis: "For sequential intents like 'mock and then implement': triggers as the first step (mockup), then defers to code-erstellen" — adressiert FAIL MU-08
- Negativliste geschärft: "architecture" entfernt (MU-09 ist doc-pflege/code-erstellen-Domäne, nicht hier negieren), "database design" bleibt
- Sprachstil: Hybrid (deutsche Trigger-Verben, englische Satzstruktur) — analog zu code-erstellen v0.20.3, doc-pflege v0.20.4, skill-pflege v0.20.5
- Schließt teilweise: ClickUp `86c9hyrm8` (mockup-erstellen-001)
- Hinweis: MU-09 (`Architektur für X`) wird NICHT in mockup-erstellen gefixt — gehört zu doc-pflege (bereits in v0.20.4 abgedeckt durch "Architektur-Docs"). Methodik-Befund "Demonstrativ-Bezug ohne Vor-Kontext" wandert in `chat-wechsel-001`.
- Quelle: BauProjektManager Teil 33

## [v0.20.5] — 2026-04-29

- **skill-pflege, Fix:** Description-Refactor — Verb-Inventar erweitert (skill-pflege-008)
- Neue Verben (deutsch): ändern, erweitern, ergänzen, einbauen, einfügen, schärfen, refactoren, aktualisieren, anpassen, präzisieren, korrigieren
- Neue Spezialfälle: adding new rules, adjusting trigger wording, refining descriptions, fixing typos, updating references, restructuring existing SKILL.md content
- Negativliste geschärft: "changing skills in unrelated repos" als zusätzlicher Schutz
- Ziel: FAIL-Case SN-07 (`ergänze beim chat-wechsel die Memory-Auflistung`) soll zu PASS werden
- Sprachstil: Hybrid (deutsche Trigger-Verben, englische Satzstruktur) — analog zu code-erstellen v0.20.3 und doc-pflege v0.20.4
- Schließt: ClickUp `86c9hyr87` (skill-pflege-008) — re-test nach Push erforderlich
- Quelle: BauProjektManager Teil 33

## [v0.20.4] — 2026-04-28

- **doc-pflege, Fix:** Description-Refactor — Verb-Inventar erweitert (doc-pflege-001)
- Neue Verben (deutsch): schreiben, erstellen, pflegen, aktualisieren, draften, anlegen, formulieren, dokumentieren, ergänzen, refactoren, validieren
- Neue Substantive: ADRs, Konzept-Docs, Architektur-Docs, Modul-Docs, README, CHANGELOG, BACKLOG, Frontmatter, Quickload, Kapitelvorlagen, INDEX.md-Routing
- Neue Spezialfälle: bug fixes in documentation (typos, broken links, outdated chapters), structural refactoring of existing docs
- Ziel: FAIL-Case CE-07 (`schreib ein ADR für die Entscheidung`) soll zu PASS werden
- Sprachstil: Hybrid (deutsche Trigger-Verben, englische Satzstruktur) — analog zu code-erstellen v0.20.3
- Schließt: ClickUp `86c9hyqv9` (doc-pflege-001) — re-test nach Push erforderlich
- Quelle: BauProjektManager Teil 33

## [v0.20.3] — 2026-04-28

- **code-erstellen, Fix:** Description-Refactor — Trigger-Vokabular erweitert (code-erstellen-001)
- Neue Verben: schreiben, erstellen, bauen, implementieren, fixen, refaktorieren, ändern, ergänzen, korrigieren, erweitern
- Neue Substantive: view models, repositories, handlers, validators, models, controllers, schemas, migrations
- Neue Endungen explizit: .cs, .xaml, .json
- Neue Spezialfälle: bug fixes, UI fixes in existing dialogs/screens/views, logic regardless of domain
- Negativliste geschärft: HTML-Entwürfe (statt nur "UI mockups"), ADR / Konzept-Doc / Frontmatter / Quickload (statt nur "documentation authoring")
- Ziel: 5 FAIL-Cases aus Smoke-Run 2026-04-28 (CE-02, MU-07, DOC-06, AUD-07, GCH-04) sollen zu PASS werden
- Sprachstil: Hybrid (deutsche Trigger-Verben, englische Satzstruktur)
- Schließt: ClickUp `86c9hyq7c` (code-erstellen-001) — re-test nach Push erforderlich
- Quelle: BauProjektManager Teil 33

## [v0.20.2] — 2026-04-28

- **evals, Docs:** P1.2 Smoke-Run-Snapshot als `evals/runs/smoke-2026-04-28-real.md`
- 30 Cases manuell durchlaufen, ein Chat pro Case (Memory aus, Skills aktiv)
- Ergebnis: PASS 67% (20/30), WARN 7% (2/30), FAIL 27% (8/30)
- Hauptbefund: `code-erstellen` strukturell schwach (29% PASS) — 5 von 7 Cases gefailt
- `cc-steuerung` Multi-Trigger 100% PASS — Invariante 9 in Praxis bestätigt
- P1.3: 5 Skill-Issues angelegt (code-erstellen-001, doc-pflege-001, skill-pflege-008, mockup-erstellen-001, chat-wechsel-001)
- Schließt: ClickUp `86c9gmk15` (P1.2), `86c9gmk1m` (P1.3)
- Quelle: BauProjektManager Teil 33

## [v0.20.1] — 2026-04-25

- **tracker, Feature:** ClickUp-Tool-Inventar als `references/clickup-tools.md` (tracker-010)
- Lade-Pattern dokumentiert: `tool_search` mit EXAKTEM Tool-Namen, nicht Umschreibung
- Tool-Inventar (Schreiben/Lesen/Suche/Comments/Custom-Fields/Time-Tracking/Members/Reminders/Documents)
- Befehl→Tool-Mapping für alle 9 tracker-Befehle
- Workspace-IDs (BPM-Spaces, Skill-Issue-Listen)
- SKILL.md erweitert um neuen Block "ClickUp-Tools (Lade-Pattern)" + VERBOTEN-Eintrag
- Schließt: ClickUp `86c9ht3xn` (tracker-010)
- Quelle: BauProjektManager Teil 32 (CGR-Kontext, Roadmap-Status-Abgleich)

## [v0.19.1] — 2026-04-25

- **code-erstellen, Refactor:** Description um WPF/XAML/code-behind ergänzt (P0.4 aus CGR-r5/r6)
- Blind-Miss 3 aus CGR r5 adressiert: "neue View für ProfileWizard" wurde im Blind-Modus unzuverlässig zu code-erstellen geroutet, weil "View" generisch auch ein Design-/Mockup-Wort ist
- Description-Trigger erweitert: "including WPF/XAML views, dialogs, code-behind, services, validation, persistence logic, or data flows"
- Vorbereitung für BPM-Feature-Arbeit (PlanManager, ProfileWizard, ImportPreviewDialog) wo UI-Sprache häufig kommt
- Two-Place-Sync: Repo + Claude.ai-Artifact

---

## [v0.19.0] — 2026-04-25

- **README, Refactor:** README entnormativiert (P0.3 aus CGR-r6 Kapitel 2)
- README ist jetzt reines Onboarding, INDEX.md ist verbindliche Regelquelle
- Top-Intro: "Single Source of Truth" → "Verbindliche Regelquelle: INDEX.md"
- Source-of-Truth-Hierarchie als neue Sektion (5 Quellen klar abgegrenzt)
- Kapitel 1 Skill-Liste: operative Details entfernt (Tracker-Kommandos, DC-Default, CGR-Dateien)
- Kapitel 2 Two-Place-Pflege: auf Verweis reduziert
- Kapitel 3 Evals: Methodik auf Verweis reduziert
- Kapitel 8 Refactor-Historie: Tabelle 6 Zeilen statt 6 Absätze
- Kapitel 9 Workflow-Konventionen: komplett entfernt, Verweis-Block stattdessen
- 4 Verweis-Block-Patterns konsistent eingeführt (INDEX, Skill, Memory, Eval)
- Reduktion: 549 → 362 Zeilen (-34%)

- **INDEX, Feature:** Invariante 9 cc-steuerung-Modalitätsregel ergänzt (P0.2 aus CGR-r5/r6)
- Modalitäts-Definition (cc/dc/Claude Code/direkt-auf-PC), WAS bleibt Fachskill, WIE kommt von cc-steuerung
- Bei `cc`/`dc` ohne fachliches WAS → `ask_user_input_v0`
- Datei-/Repo-Nennung allein triggert cc-steuerung nicht — explizite Ausführungsabsicht nötig
- Smoke-Test-Pflicht für Multi-Intent-Fälle in `evals/smoke-all-skills.md`
- Exit-Kriterium dokumentiert: bei 2+ FAILs in realer Nutzung → Variante A (Modalitätsblock in Fachskills)
- Quelle: CGR-2026-04-skillsystem-r5/r6, ClickUp-Task `86c9gmjan`

## [v0.18.1] — 2026-04-25

- **CHANGELOG, Docs:** Drift schließen v0.17.8 bis v0.18.0 (P0.1 aus CGR-r5)
- 5 fehlende Versionseinträge nachgetragen (v0.17.8/9/10/11 + v0.18.0)
- Henne-Ei-Eintrag v0.17.8 dokumentiert die CHANGELOG-Pflege selbst
- Befund verifiziert in CGR-2026-04-skillsystem-r5 (ChatGPT-Audit)
- Quelle: ClickUp-Task `86c9gmj81`

## [v0.18.0] — 2026-04-24

- **skill-pflege, Feature:** Max 1 Skill-Artifact pro Antwort (skill-pflege-007)
- Zwei Artifacts mit Dateiname `SKILL.md` überschreiben sich gegenseitig im Container-Pfad `/home/claude/SKILL.md`
- Bei Multi-Skill-Updates sequentiell über mehrere Antworten — Repo-Edits dürfen gebündelt werden
- Regel 13b in skill-pflege-Body + VERBOTEN-Eintrag

## [v0.17.11] — 2026-04-24

- **skills, Fix:** Description-Schärfung git-commit-helper + chatgpt-review (ARCH-OPEN aus Phase 5.8)
- git-commit-helper Description ergänzt um `(including PATCH/MINOR/MAJOR decisions or semver questions)`
- chatgpt-review Description ergänzt um `(inkl. Runden-Folgeprompts wie "Runde 3 erstellen")`
- ARCH-OPEN-Memory-Eintrag aus Phase 5.8 entfernt

## [v0.17.10] — 2026-04-24

- **docs, Docs:** INDEX.md neu strukturiert
- 11 Skills in Routing-Matrix (alphabetisch + nach Hierarchie)
- 8 Invarianten als DNA des Systems dokumentiert (Phase 1–5 durchgezogen)
- Phase-5-Delegations-Matrix für 7 Konfliktpaare als Tabelle

## [v0.17.9] — 2026-04-24

- **docs, Docs:** README.md neu strukturiert
- 12 Kapitel, 549 Zeilen, tiefe Erklärung aller Ordner und Dateien
- Onboarding-orientiert mit Architektur-Erklärungen, Skill-Gruppen und Refactor-Historie
- Verweise auf INDEX.md, CHANGELOG.md, MEMORY-RUBRIKEN.md, evals/

## [v0.17.8] — 2026-04-24

- **docs, Docs:** CHANGELOG.md neu strukturiert
- 60+ Versionseinträge in umgekehrter Chronologie
- Phasen-Tags auf CGR-2026-04-skillsystem-Runden verweisen
- Format vereinheitlicht: `[vX.Y.Z] — <Datum>` + Bullet-Liste der Änderungen

## [v0.17.7] — 2026-04-24

- **evals, Docs:** Phase 5.8 Abschluss-Eval nach Refactor
- 4 Eval-Dateien (git-commit-helper, chatgpt-review, tracker, code-erstellen) mit `after-refactor`-Block gefüllt — Blind-Modus + Vollmodus-Simulation
- `evals/phase-5-abschluss-report.md` als Gesamtreport angelegt
- Ergebnis: Blind 73/76 (unverändert), Vollmodus 75/76 (+2 ggü. Baseline), Ambiguitätsquote stabil
- `[ARCH-OPEN]` für 2 Description-Schärfungen dokumentiert (git-commit-helper Q9, chatgpt-review Q6)

## [v0.17.6] — 2026-04-24

- **cc-steuerung, Feature:** Paar 7 — Modalitäts-Abgrenzung zu Fachskills (asymmetrisch)
- cc-steuerung bekommt Abschnitt "Vorrang / Verhältnis zu Fachskills (Modalität, KEIN Fachvorrang)" mit WAS/WIE-Rollentrennung
- Bewusst asymmetrisch — keine Delegations-Zeile in den 8 Fachskills, weil cc-steuerung kein alternativer Fachskill ist sondern eine Modalität

## [v0.17.5] — 2026-04-24

- **skills, Feature:** Paar 6 — chat-wechsel ↔ chatgpt-review symmetrisch abgegrenzt
- Beide Skills bekommen Delegations-Tabellen mit klarer Rollentrennung (Handover vs. Review-Prompt)
- Generische "mach mir den Prompt"-Aufforderungen triggern nicht automatisch — Klärung per `ask_user_input_v0`

## [v0.17.4] — 2026-04-24

- **audit, Feature:** Paar 5 — Delegations-Tabelle zu code-erstellen
- audit bleibt strikt read-only — bietet keine Fixes selbst an, delegiert per `ask_user_input_v0`
- Expliziter Verweis: Code-Fixes → code-erstellen, Doc-Fixes → doc-pflege

## [v0.17.3] — 2026-04-24

- **tracker, Feature:** Paar 4 — Delegations-Tabelle zu code-erstellen
- tracker wird nicht automatisch durch Code-Commits ausgelöst — nur explizite `tracker <kommando>` oder expliziter Aufruf aus anderen Skills via `ask_user_input_v0`

## [v0.17.2] — 2026-04-24

- **doc-pflege, Feature:** Paar 3 — Delegations-Tabelle zu code-erstellen
- Advisory-Hinweise aus code-erstellen/git-commit-helper sind KEIN Trigger für doc-pflege
- Doc-Pflege startet nur auf expliziten User-Auftrag

## [v0.17.1] — 2026-04-24

- **git-commit-helper, Feature:** Paar 2 — Delegations-Tabelle zu code-erstellen
- Inline-Commit-Vorschlag aus code-erstellen ist kein Trigger für git-commit-helper
- Nur explizite Commit-Requests oder aktive Delegation aus code-erstellen triggern

## [v0.17.0] — 2026-04-24

- **skills, Feature:** Paar 1 — code-erstellen ↔ mockup-erstellen symmetrisch abgegrenzt
- Beide Skills bekommen Delegations-Tabellen
- mockup-erstellen → HTML-Mockups; XAML/Code → code-erstellen (auch bei kleinen UI-Fixes)


## [v0.16.0] — 2026-04-23

- **chatgpt-review, Feature:** CGR-System Integration (Phase 4.6)
- ChatGPT-Reviews werden inkrementell in `BauProjektManager/Docs/Referenz/chatgpt-reviews/` archiviert
- ID-Schema `CGR-<YYYY-MM>-<thema>-r<runde>`, 4 Dateien pro Runde (01-claude-prompt, 02-chatgpt-response, 03-claude-analysis, 04-user-decisions)
- Themen-Enum: skillsystem, docs-refactor, bpm-architektur, datenschutz-dbschema

## [v0.15.12] — 2026-04-23

- **tracker, Feature:** Memory-Eskalation Brücke (Phase 4.4)
- Memory-Einträge (Rubriken VERIFY/ARCH-OPEN/INFRA-TODO/REVIEW-PENDING) werden nie automatisch zu ClickUp-Tasks
- Eskalation nur auf expliziten User-Auftrag, Memory-Entfernung erst nach Bestätigung

## [v0.15.11] — 2026-04-23

- **skill-pflege, Feature:** Memory-Cleanup 3-Schritt-Sequenz (Phase 4.3)
- Memory-Hygiene-Protokoll bei Skill-Änderungen: Check vor Update → Update → Cleanup-Vorschlag
- Stale-Einträge werden via `ask_user_input_v0` zur Entfernung vorgeschlagen

## [v0.15.10] — 2026-04-23

- **skill-neu, Feature:** Memory-Disziplin (Phase 4.2)
- Capture-Intent-Interview bezieht Memory-Rubriken ein
- Neue Skills berücksichtigen bestehende Memory-Einträge bei Description-Entwurf

## [v0.15.9] — 2026-04-23

- **docs, Feature:** MEMORY-RUBRIKEN.md Konvention festgezogen (Phase 4.5)
- Master-Doku der 4 Memory-Rubriken: VERIFY, ARCH-OPEN, INFRA-TODO, REVIEW-PENDING
- Verbindliche Regel: nur für offene Punkte, nicht für ClickUp-würdige Aufgaben


## [v0.15.8] — 2026-04-22

- **tracker, Feature:** Referenz-Anker auch bei übernommenen Tasks (tracker-009)
- Folge-Antworten zu Tasks die nur gelesen/bearbeitet werden (nicht via `tracker neu`/`tracker done`) benötigen trotzdem Referenz-Anker im Chat

## [v0.15.7] — 2026-04-22

- **tracker, Feature:** Skill-Artifact-Nachlauf bei Skill-Issue-done (skill-pflege-005)
- Nach erfolgreichem `tracker done` eines Skill-Issues wird automatisch der Skill-Artifact-Block im Chat erzeugt

## [v0.15.6] — 2026-04-22

- **skill-pflege, Fix:** Artifact-Mechanik Tool-Call-Paar (skill-pflege-006)
- `create_file` + `present_files` müssen zusammen in einem Tool-Call-Paar stehen
- Separate Antwort-Blöcke brechen die Skill-speichern-Button-Erkennung

## [v0.15.5] — 2026-04-22

- **skill-pflege, Feature:** Artifact-Pflicht nach Skill-Commit (skill-pflege-005)
- Nach jedem Skill-Commit MUSS ein Artifact-Block im selben oder direkt folgenden Antwort-Block erzeugt werden

## [v0.15.4] — 2026-04-22

- **skill-pflege + skill-neu, Feature:** Auto-Issue-Erkennung (skill-pflege-002)
- Skill-Updates erkennen automatisch ob ein Skill-Issue dazu existiert und setzen den Tracker-Bezug

## [v0.15.3] — 2026-04-22

- **skill-pflege + skill-neu + cc-steuerung, Feature:** Artifact-Dateiname-Regel (skill-pflege-004)
- Artifacts müssen exakt `SKILL.md` heißen (kein Prefix/Suffix), sonst erscheint kein "Skill speichern"-Button

## [v0.15.2] — 2026-04-22

- **skill-pflege + skill-neu + cc-steuerung, Feature:** Artifact-Separation (skill-pflege-003)
- DC-Schreib-Operation + Artifact-Erstellung in einer Antwort: KEIN `ask_user_input_v0` im selben Block


## [v0.15.1] — 2026-04-22

- **skill-pflege + skill-neu, Change:** Two-Place-Workflow Repo + Artifact (skill-pflege-001)
- Skill-Änderungen landen via DC direkt im Repo UND als Artifact für den Claude.ai-Skill-Store-Button
- Kein Download-File in `/mnt/user-data/outputs/` mehr, kein `present_files` für Skill-Updates

## [v0.15.0] — 2026-04-22

- **cc-steuerung, Change:** DC als Default-Ausführungsmodus nach Konzept-Freigabe (cc-steuerung-003)
- Nach User-Freigabe ("code bitte", "mach", "ok") ist DC der Default-Modus
- SUCHE/ERSETZE im Chat nur auf explizite Anfrage oder wenn DC nicht verfügbar

## [v0.14.8] — 2026-04-22

- **cc-steuerung, Feature:** PowerShell Dollar-Escaping-Regel (cc-steuerung-002)
- KEINE `$`-Variablen in DC-PowerShell-Command-Strings — äußere Shell-Schicht interpoliert sie zu leerem String
- Lösung: Sequentielle Ausgabe per Semikolon oder `.ps1`-Datei

## [v0.14.7] — 2026-04-22

- **cc-steuerung, Feature:** Tool-basierte DC-Umgebungs-Erkennung (cc-steuerung-001)
- DC-Verfügbarkeit NUR über Tool-Liste prüfen, NIEMALS via `bash_tool hostname`
- `bash_tool` läuft in Claude-internem Container, nicht auf User-PC

## [v0.14.6] — 2026-04-22

- **tracker, Feature:** Auto-Nummerierung für Skill-Issues (tracker-003)
- `tracker issue <skill>` vergibt automatisch die nächste freie Issue-ID (`<skill>-NNN`)
- Unique-Check über `clickup_filter_tasks` mit `include_closed: true`

## [v0.14.5] — 2026-04-22

- **tracker, Feature:** Automatischer Nachlauf nach tracker done (tracker-008)
- 4-Schritt-Nachlauf: Hash via DC holen, Custom Fields setzen, Zwischenstand-Tabelle, Folgeoptionen via `ask_user_input_v0`


## [v0.14.4] — 2026-04-22

- **tracker, Feature:** Review-Workflow vor Task-Übergang (tracker-006)
- 4-Punkte-Scope-Check vor `tracker done` / `tracker start` / Fokus-Wechsel
- Prüfung: aktueller Task + Parent + Siblings + verweisende offene Tasks

## [v0.14.3] — 2026-04-22

- **tracker, Feature:** Commit-Disziplin ein Task ein Commit (tracker-007)
- Jeder abgeschlossene (Sub-)Task bekommt sofort einen eigenen Commit — kein Sammeln

## [v0.14.2] — 2026-04-22

- **tracker, Refactor:** create-task.md Abgrenzung zu issue-task.md (86c9f78mj.03)
- Klare Trennung: BPM-Tasks via `tracker neu` → `create-task.md`; Skill-Issues via `tracker issue` → `issue-task.md`

## [v0.14.1] — 2026-04-22

- **tracker, Refactor:** SKILL.md Routing-Tabelle + Querverweis für tracker issue (86c9f78mj.02)
- Routing-Tabelle um `tracker issue <skill>: <Titel>` erweitert

## [v0.14.0] — 2026-04-22

- **tracker, Feature:** issue-task.md Spec für tracker issue Kommando (86c9f78mj.01)
- Neue Reference-Datei mit Ablauf für Skill-Issue-Anlage (Ordner-Lookup, Custom-Fields, Numerierung)

## [v0.13.2] — 2026-04-22

- **tracker, Refactor:** anti-patterns.md VERBOTEN Projekt-Config (7.6.05)
- Projekt-Daten nicht hartkodieren — alles aus `projects/<[PROJECT]>/` lesen

## [v0.13.1] — 2026-04-22

- **tracker, Refactor:** search/update/chat-url/split Verweise (7.6.04)
- Finale Querverweise in SKILL.md angepasst an die Progressive-Disclosure-Struktur


## [v0.13.0] — 2026-04-22

- **skill-repo, Refactor:** Projekt-Architektur `projects/bpm/` eingeführt
- Projekt-spezifische Daten (Listen-IDs, Custom-Field-IDs, Modul-Kürzel) aus Skills in `projects/<name>/` extrahiert
- Skills werden damit projekt-agnostisch, verweisen nur noch auf `projects/<[PROJECT]>/`

## [v0.12.0] — 2026-04-22

- **tracker, Feature:** Referenz-Anker in Folge-Antworten (tracker-005)
- Jede Folge-Antwort die einen Task inhaltlich betrifft MUSS einen Referenz-Anker oben tragen
- Format: `Betroffene Tasks in dieser Antwort: [BPM-ANCHOR-<id>] <n>.`

## [v0.11.0] — 2026-04-22

- **tracker, Feature:** tracker start Kommando + Status-Werte pro Listen-Typ (tracker-002)
- Neues Kommando `tracker start: <BPM-NNN>` setzt Task auf `in progress` + Parent-Kaskade
- Status-Werte pro Listen-Typ dokumentiert (BPM-Listen vs. Skill-Issues)

## [v0.10.0] — 2026-04-21

- **tracker, Feature:** Pro-Task-Quittung + Batch-Protokoll (tracker-001, tracker-004)
- Nach jedem Task-Create/Update MUSS eine Quittungszeile im selben Antwort-Block stehen
- Batch-Protokoll bei ≥2 Task-Operationen: Ansage → Pro-Task-Zyklus → Audit am Ende

## [v0.9.0] — 2026-04-21

- **chat-wechsel, Feature:** Memory-Scan bei Handover (Phase 4.1)
- Memory wird bei Handover nach 4 Rubriken gefiltert: VERIFY, ARCH-OPEN, INFRA-TODO, REVIEW-PENDING
- Gemeinsamer Block "Offene Punkte aus Memory" im Handover-Prompt

## [v0.8.0] — 2026-04-21

- **docs, Feature:** Skill-Refactor-Phasen als arbeitsnahe Referenz
- Extrakt aus ChatGPT-Review Runde 4 (`CGR-2026-04-skillsystem-r4`)
- Dient als Arbeits-Roadmap für die folgenden Phasen 2–5


## [v0.7.1] — 2026-04-21

- **skill-pflege, Feature:** Bidirektionaler Verweis auf skill-neu (Phase 3.5)
- skill-pflege und skill-neu kennen sich gegenseitig explizit, Abgrenzung in beiden Descriptions geschärft

## [v0.7.0] — 2026-04-21

- **skill-neu, Feature:** Initial skill — neue BPM-Skills von Grund auf erstellen
- Capture-Intent-Interview, Description-Schema, Body-Template, references/-Aufteilung, Test-Prompt-Setup
- Ergänzt skill-pflege (der nur bestehende Skills ändert)

## [v0.6.0] — 2026-04-21

- **tracker, Refactor:** Progressive Disclosure (Phase 3.3)
- SKILL.md auf 147 Zeilen reduziert, Details in 9 Reference-Dateien ausgelagert
- `references/`: clickup-fields, anker-system, batch-protocol, chat-url-handling, create-task, issue-task, start-task, complete-task, review-workflow, update-task, search-and-status, split-and-relations, anti-patterns

## [v0.5.2] — 2026-04-21

- **code-erstellen, Refactor:** Delegationsblock für 5 Nachbarskills (Phase 3.2)
- code-erstellen ist der größte Catch-all, bekommt explizite Delegations-Tabelle
- UI-Entwurf → mockup-erstellen, Commit → git-commit-helper, ADR/Doc → doc-pflege, Task → tracker, Audit → audit

## [v0.5.1] — 2026-04-21

- **doc-pflege, Refactor:** Advisory-Block aus Trigger-Identität entfernt (Phase 3.1)
- Advisory-Checkliste wird als Nachlauf von code-erstellen/git-commit-helper konsumiert
- Advisory-Abschnitt explizit markiert: "KEIN Trigger für doc-pflege selbst"

## [v0.5.0] — 2026-04-21

- **skills, Refactor:** Phase 2 Description-Schema-Refactor (9 Skills)
- Einheitliches Description-Schema für 9 Skills
- Pattern: Zweck-Satz + `Use when...` + `Do not trigger for...`


## [v0.4.5] — 2026-04-21

- **evals, Docs:** Baseline-Scores für 4 Skills erfasst (Blind-Modus Opus 4.7)
- Phase 1a.3 — Routing-Scores als Referenz für spätere Re-Runs
- Ergebnisse: git-commit-helper 8/9/5/5/3/3, chatgpt-review 8/9/4/4/2/3, tracker 9/9/7/7/3/3, code-erstellen 9/10/3/3/6/6

## [v0.4.4] — 2026-04-21

- **tracker, Feature:** Stale-Check für [ANKER-LIVE] beim Chat-Start
- Anker-Einträge älter als 24h werden beim Chat-Start geprüft und ggf. gemeldet

## [v0.4.3] — 2026-04-21

- **tracker, Feature:** Kommando `anker setzen` für manuelle Phase-1-Anker
- User kann selbst einen Temp-Anker für noch nicht konkretisierte Themen anlegen

## [v0.4.2] — 2026-04-21

- **code-erstellen, Feature:** Auto-Anker bei Task-Keywords (Phase 1 des Chat-Anker-Systems)
- Task-Signal-Wörter ("das müssen wir noch bauen", "ins backlog") setzen automatisch einen Temp-Anker
- TEMP-ID-Format: `TEMP-<yyMMddHHmm><3 Zufallsbuchstaben>`

## [v0.4.1] — 2026-04-21

- **chat-wechsel, Feature:** Chat-Anker-Übergabe zwischen Sessions
- `[ANKER-LIVE]` wird im Handover-Prompt als Tabelle mitgegeben und im alten Chat aus Memory entfernt
- Anker reisen per Prompt, nicht per Memory (weil Memory pro Session)

## [v0.4.0] — 2026-04-21

- **tracker, Feature:** Chat-Anker-System Phase 2+3 + neue Custom-Field-IDs
- Custom Fields `Chat-Anker erstellt` / `Chat-Anker erledigt` / `Chat-Anker temp` in ClickUp
- Anker-Format `[BPM-ANCHOR-<task-id>] — <typ>: <kurz>` im Chat + Custom Field synchron


## [v0.3.1] — 2026-04-21

- **docs, Feature:** Chat-Anker-System Konzept v2 (Task-ID + temp-ID kombiniert)
- Konzept-Doc für das 3-Phasen-Anker-System (Phase 1: TEMP-ID, Phase 2: Task-ID, Phase 3: erledigt)

## [v0.3.0] — 2026-04-21

- **evals, Feature:** Phase 1a.1 + 1a.2 Eval-Verzeichnis mit 4 Skill-Katalogen
- `evals/`-Ordner angelegt mit README, Template und 4 Skill-Eval-Dateien
- 12–16 Queries pro Skill in 4 Kategorien: should_trigger, should_not_trigger, other_skill, ambiguous

## [v0.2.0] — 2026-04-21

- **skills, Refactor:** Trigger-Bereinigung für 4 kritische Skills (Phase 1.1–1.4)
- git-commit-helper: "ok"/"passt"-Zustimmung und git push aus Triggern entfernt
- chatgpt-review: "antworte darauf" ohne expliziten Review-Kontext entfernt
- tracker: "was ist offen?"-Backlog-Talk ohne tracker-Kommando entfernt
- code-erstellen: Ausschlüsse für mockups/commits/docs/tasks/audits ergänzt
- Zusätzlich: Anthropic skill-creator als Referenz hinzugefügt

## [v0.1.0] — 2026-04-21

- **claude-skills-bpm, Feature:** Initial-Inhalt mit 10 Skills
- Erste Version des Repos — 10 bestehende Skills aus dem Claude-Projekt übernommen:
  - audit (193 Zeilen)
  - cc-steuerung (271 Zeilen)
  - chat-wechsel (307 Zeilen)
  - chatgpt-review (238 Zeilen) — Frühphasen-Hinweis-Block integriert
  - code-erstellen (326 Zeilen) — Frühphasen-Prinzip + Migrations-Blocking
  - doc-pflege (321 Zeilen) — Frühphasen-Regel für Schema-/DB-Doku
  - git-commit-helper (105 Zeilen)
  - mockup-erstellen (235 Zeilen)
  - skill-pflege (299 Zeilen)
  - tracker (911 Zeilen)

### Entscheidungen v0.1.0

- Separate Repo statt Unterordner im BPM-Repo (bessere Trennung, eigene Historie)
- Struktur folgt Anthropic-Standard (`skills/<n>/SKILL.md`)
- Sync: Skills werden in zwei Orten gepflegt (`/mnt/skills/user/` + `claude-skills-bpm/skills/`)
