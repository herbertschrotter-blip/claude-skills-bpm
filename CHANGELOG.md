# CHANGELOG

Alle relevanten Änderungen an den Skills werden hier dokumentiert.

Format: Umgekehrte Chronologie (neueste zuerst). Versions-Tags folgen Semantic Versioning (`[vMAJOR.MINOR.PATCH]`). Phasen-Tags beziehen sich auf den Skill-System-Refactor aus dem ChatGPT-Review `CGR-2026-04-skillsystem`.

---

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
