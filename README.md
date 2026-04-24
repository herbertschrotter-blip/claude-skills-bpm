# claude-skills-bpm

Claude-Skills für das BauProjektManager (BPM) Projekt von Herbert Schrotter.

Dieses Repo ist die **Single Source of Truth** für 11 BPM-spezifische Skills samt Eval-Matrix, Projekt-Config, Refactor-Dokumentation und Memory-Konventionen. Die Skills sind gezielt auf den BPM-Workflow optimiert und kennen die BPM-Docs, ClickUp-IDs, Modul-Kürzel und Commit-Konventionen. Sie sind **nicht** als allgemeine Community-Skills gedacht — für generische Skills siehe z.B. [obra/superpowers](https://github.com/obra/superpowers) oder [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills).

---

## Zweck dieses Repos

| Zweck | Beschreibung |
|---|---|
| **Versionshistorie** | Jede Skill-Änderung ist ein Git-Commit im Format `[vX.Y.Z] Skill, Typ: Kurztitel`. Volle Nachvollziehbarkeit von v0.1.0 (Initial) bis aktuell. |
| **Cross-Review** | ChatGPT kann Skills und Review-Runden direkt aus dem Repo lesen. CGR-System archiviert jede Review-Runde in 4 Dateien. |
| **Backup** | Skills gehen nicht verloren wenn der Claude-Projekt-Speicher reset wird. |
| **Portabilität** | Universelle Skills + projektspezifische Config sind getrennt (`skills/` vs `projects/<projekt>/`). Neue Projekte können dasselbe Skill-System nutzen indem sie nur ihren `projects/<n>/`-Ordner anlegen. |
| **Meta-Werkzeug** | Die Skills reflektieren über sich selbst: `skill-neu` erstellt neue Skills, `skill-pflege` ändert bestehende, `evals/` misst das Routing-Verhalten. |

---

## Verzeichnisstruktur (Überblick)

```
claude-skills-bpm/
├── README.md              ← Dieses File
├── INDEX.md               ← Skill-Übersicht + Trigger-Matrix
├── CHANGELOG.md           ← Versionsverlauf (60+ Einträge)
├── MEMORY-RUBRIKEN.md     ← Konvention für 4 Memory-Rubriken
├── docs/                  ← Konzepte und Refactor-Notizen
├── evals/                 ← Skill-Routing-Evals (Baseline + after-refactor)
├── projects/              ← Projekt-spezifische Daten (isoliert pro Projekt)
├── reference/             ← Externe Referenz-Artefakte
└── skills/                ← 11 Skills, je ein Ordner mit SKILL.md
```

Die folgenden Kapitel erklären jeden dieser Ordner und die darin liegenden Dateien detailliert.

---

## Kapitel 1 — Die 11 Skills im Überblick

Die Skills sind in drei konzeptionelle Gruppen einteilbar: **Fachskills**, **Meta-Skills** und **Modalitäts-Skills**. Ihre Interaktion wurde in Phase 5 des Refactors (ChatGPT-Review Runde 4) durch symmetrische Delegations-Tabellen und Konfliktpaar-Cross-References sauber abgegrenzt.

### Fachskills (beantworten "WAS wird gemacht")

| Skill | Aufgabe | Trigger-Beispiele |
|---|---|---|
| **code-erstellen** | Master-Orchestrator für BPM-Code-Änderungen. Lädt INDEX.md, Quickloads und fachliche Invarianten. Führt Impact-Check und Blocking-Conditions durch. Delegiert UI-Mockups, Commits, Docs, Tasks und Audits an die passenden Nachbar-Skills. | "implementiere das Feature", "erstelle die DocumentTypeRecognizer.cs", "baue die Recovery-Logik ein" |
| **mockup-erstellen** | HTML-UI-Mockups für BPM-Screens. Lädt UI_UX_Guidelines.md, Colors.xaml und WPF_UI_Architecture.md. Namenskonvention `NN_Blatt[_Untermenue].html` in `Docs/Mockups/<Modul>/`. Workflow: Preview im Chat → User-Bestätigung → DC-Speichern. | "Mockup für den ProfileWizard", "Screen-Design", "UI-Mockup" |
| **doc-pflege** | Erstellt und pflegt BPM-Dokumentation nach DOC-STANDARD.md. 7 Modi von Projekt-Init über Index-Sync bis Frontmatter-Validierung. Konsumiert Advisory-Hinweise von code-erstellen und git-commit-helper **passiv** (kein Trigger). | "pflege die docs", "schreib ein ADR", "neues Konzept für X" |
| **chatgpt-review** | Strukturierte Cross-LLM-Review-Prompts zwischen Claude und ChatGPT. CGR-System: archiviert jede Runde inkrementell in 4 Dateien (`01-claude-prompt.md`, `02-chatgpt-response.md`, `03-claude-analysis.md`, `04-user-decisions.md`) im BPM-Repo unter `Docs/Referenz/chatgpt-reviews/`. ID-Schema `CGR-<YYYY-MM>-<thema>-r<runde>`. | "besprich das mit ChatGPT", "zweite Meinung", "Folgeprompt für Runde 3" |
| **audit** | Strikt read-only Konsistenzprüfung zwischen Code, Docs, Frontmatter und Quickload. 2 Modi (Vollaudit, Teilaudit) × 6 Prüfmodule (INDEX-Selbstcheck, Kern-Docs vs Code, Code vs Docs, Referenz-Docs, Modul-Docs, Frontmatter+Quickload). Bietet keine Fixes selbst — delegiert Empfehlungen per `ask_user_input_v0`. | "audit", "prüfe alles", "konsistenzcheck" |
| **tracker** | Einzige standardisierte Schreibschnittstelle zum ClickUp-Task-System. Kommandos: `tracker neu/done/update/status/suche/next/split/relate/field/start/issue`. Pro-Task-Quittung ist Pflicht, Batch-Protokoll bei ≥2 Operationen, 4-Punkte-Scope-Check vor Task-Übergang, automatischer Nachlauf nach `tracker done` (Hash holen, Zwischenstand, Folgeoptionen). Projekt-Daten aus `projects/<[PROJECT]>/` — nichts hartkodiert. | "tracker neu: PM — Regex-Bug", "tracker done BPM-042", "tracker suche Regex" |
| **git-commit-helper** | Fertige Git-Commit-Befehle im BPM-Format `[vX.Y.Z] Modul, Typ: Kurztitel`. Semantic-Versioning-Ableitung (PATCH/MINOR/MAJOR) inkl. `ask_user_input_v0` bei Unsicherheit. Doc-Pflege-Trigger-Checkliste als Nachlauf. | "commit bitte", "commit-message", "PATCH oder MINOR?" |
| **chat-wechsel** | Handover-Prompt für die nächste Claude-Session. Bei jedem Handover Pflicht: ClickUp-Batch-Abschluss (Done-Markierung + neue Tasks per `ask_user_input_v0`), Memory-Scan nach 4 Rubriken, `[ANKER-LIVE]`-Transfer in den neuen Chat, Chat-URL einfügen. | "neuer chat", "nächster chat", "übergabe" |


### Meta-Skills (ändern andere Skills)

| Skill | Aufgabe |
|---|---|
| **skill-neu** | Erstellt neue BPM-Skills von Grund auf. Capture-Intent-Interview, Description-Schema nach BPM-Standard (`Zweck + Use when + Do not trigger for`), Body-Template, `references/`-Aufteilung bei Progressive Disclosure, Test-Prompt-Setup. Berücksichtigt Memory-Rubriken (Phase 4.2). |
| **skill-pflege** | Ändert und erweitert bestehende Skills **additiv** — Originalinhalt wird nie gekürzt. Two-Place-Workflow (Repo via DC + Artifact im Chat). Artifact-Dateiname zwingend `SKILL.md` damit der Claude.ai "Skill speichern"-Button erscheint. Memory-Cleanup-Sequenz bei Stale-Einträgen (Phase 4.3). |

### Modalitäts-Skill (beantwortet "WIE wird ausgeführt")

| Skill | Aufgabe |
|---|---|
| **cc-steuerung** | Steuert den Desktop Commander (DC) MCP-Server für direkte File-/Terminal-Operationen auf Herberts PC. **Kein Fachvorrang** — läuft parallel zu Fachskills. DC ist Default-Ausführungsmodus nach Konzept-Freigabe. Pfad-Auto-Discovery per `hostname` + `[System.Environment]::GetEnvironmentVariable('OneDrive','User')`, Self-Registration unbekannter PCs in INDEX.md, PowerShell-`$`-Variablen-Regel (sequentielle Ausgabe statt Assignment). |

### Trigger-Disziplin — das Kernprinzip

Jede Skill-Description folgt dem Schema:

```yaml
description: >
  <Zweck-Satz> Use when <positive Trigger>. Do not trigger for <Negativgrenzen>.
```

Dieses Schema wurde in **Phase 2** des Refactors einheitlich durchgezogen und in **Phase 5** durch Delegations-Tabellen im Body ergänzt. Details siehe Kapitel "Refactor-Historie" und die CHANGELOG.

---

## Kapitel 2 — `skills/` — Die Skill-Dateien

### Struktur pro Skill

```
skills/<skill-name>/
├── SKILL.md              ← Die Skill-Definition (Frontmatter + Body)
├── references/           ← (optional) Progressive Disclosure Details
│   ├── <aspekt-1>.md
│   ├── <aspekt-2>.md
│   └── ...
└── test-prompts.md       ← (optional) Beispielqueries zum Trigger-Test
```

### Aufbau einer `SKILL.md`

Jede Skill-Datei beginnt mit einem YAML-Frontmatter:

```yaml
---
name: <skill-name>
description: >
  <Zweck-Satz>. Use when <positive Trigger>. Do not trigger for <Ausschlüsse>.
---
```

Der Body enthält typischerweise diese Abschnitte (je nach Skill unterschiedlich):

1. **Zweck** — Ein-Absatz-Erklärung
2. **Vorrang / Delegation** (Phase 5) — Tabelle mit "WENN Hauptabsicht X → Skill Y" zur Entflechtung von Paar-Konflikten
3. **🚨 Kernregeln** — unumstößliche Regeln z.B. `ask_user_input_v0` bei Entscheidungen, Branch-Ermittlung vor GitHub-Zugriff, Artifact-Dateiname
4. **Ablauf** — konkrete Schrittfolge mit Code/Kommandos
5. **Reference-Tabelle** (bei Progressive Disclosure) — Kommando → Reference-Datei
6. **VERBOTEN** — Anti-Patterns-Liste

### Progressive Disclosure — am Beispiel `tracker`

Der `tracker`-Skill ist der längste und nutzt Progressive Disclosure. Die `SKILL.md` enthält nur Kernregeln + Routing-Tabelle; Details sind in 13 `references/`-Dateien ausgelagert:

| Reference | Inhalt |
|---|---|
| `anker-system.md` | Chat-Anker-Master-Spec: `[BPM-ANCHOR-...]`-Format, `[ANKER-LIVE]`-Registry, TEMP-ID-Generierung, Lifecycle |
| `anti-patterns.md` | Vollständige VERBOTEN-Liste, Automationspolitik, Integration mit anderen Skills |
| `batch-protocol.md` | Pro-Task-Quittung, Batch-Ansage, Batch-Audit, Regeln für ≥2 Task-Operationen |
| `chat-url-handling.md` | Chat-URL-Ermittlung per `recent_chats`/`conversation_search` |
| `clickup-fields.md` | 10 Custom Fields mit IDs + Option-IDs (BPM-spezifisch — wird durch `projects/<[PROJECT]>/clickup-fields.md` ersetzt) |
| `complete-task.md` | `tracker done` Ablauf, Commit-Disziplin, automatischer Nachlauf |
| `create-task.md` | `tracker neu` Ablauf, Description-Template, Workflow |
| `issue-task.md` | `tracker issue <skill>` Ablauf, Issue-ID-Nummerierung |
| `review-workflow.md` | 4-Punkte-Scope-Check vor Task-Übergang |
| `search-and-status.md` | `tracker status`, `next`, `suche`, `listen` |
| `split-and-relations.md` | `tracker split`, `tracker relate`, Dependency-Typen |
| `start-task.md` | `tracker start` Ablauf, Parent-Kaskade |
| `update-task.md` | `tracker update`, `tracker field` |


### Sync-Mechanismus: Two-Place-Pflege

Skills werden an **zwei Orten** gepflegt:

| Ort | Zweck |
|---|---|
| `claude-skills-bpm/skills/<n>/SKILL.md` | Git-versioniert, CGR-lesbar, Backup |
| `/mnt/skills/user/<n>/SKILL.md` | Claude.ai-aktive Instanz (Skill-Store im User-Account) |

Der `skill-pflege`-Skill erzwingt die Aktualisierung **beider** Orte via DC (Repo-Seite) **und** Artifact im Chat (Claude.ai-Seite). Der Artifact-Dateiname MUSS exakt `SKILL.md` heißen — nur dann erscheint im Chat der "Skill speichern"-Button der die Claude.ai-Seite aktualisiert. Nach jedem Skill-Commit MUSS ein Artifact-Block folgen (Regel `skill-pflege-005`).

---

## Kapitel 3 — `evals/` — Skill-Routing-Evaluation

Das Eval-System misst, ob ein Skill bei den richtigen Queries triggert und bei den falschen nicht. Es ist das objektive Qualitätsmaß für das Skill-System.

### Dateien

| Datei | Inhalt |
|---|---|
| `README.md` | Erklärt Workflow, Kategorien, Scoring-Schema |
| `_template.md` | Vorlage für neue Skill-Evals |
| `git-commit-helper.md` | Query-Katalog + Baseline + after-refactor Scores |
| `chatgpt-review.md` | dto. |
| `tracker.md` | dto. |
| `code-erstellen.md` | dto. |
| `phase-5-abschluss-report.md` | Aggregierter Gesamt-Report der Phase-5-Abschluss-Eval |

Nur 4 Skills haben aktuell Evals — das waren die kritischsten aus Phase 1a des Refactors. Die übrigen 7 Skills werden bedarfsbasiert bei Trigger-Problemen nachgezogen.

### Eval-Methodik

Pro Skill ein Query-Katalog mit 12–16 Einträgen in 4 Kategorien:

| Kategorie | Bedeutung | Bewertung |
|---|---|---|
| `should_trigger` | Dieser Skill MUSS triggern | Zählt in Score |
| `should_not_trigger` | KEIN Skill darf triggern (reines Gespräch, Zustimmung, Rückfrage) | Zählt in Score |
| `other_skill` | Ein ANDERER, benannter Skill soll triggern | Zählt in Score |
| `ambiguous` | Grenzfall, beide Interpretationen vertretbar | Wird dokumentiert, nicht bewertet |

Jede Query ist markiert als:

- `[golden]` — echte Formulierung aus dem BPM-Chat-Verlauf
- `[synthetic]` — gezielt konstruierte Variante zur Randtest-Abdeckung

### Scoring-Runs pro Eval-Datei

```yaml
## Run-Log

### baseline
- date: 2026-04-21
- tester: Claude Opus 4.7 (Blind-Modus — nur Name + Description)
- should_trigger: X/Y
- should_not_trigger: X/Y
- other_skill: X/Y
- ambiguous: dokumentiert
- notes: ...

### after-refactor
- date: 2026-04-24
- tester: Claude Opus 4.7 (Selbst-Simulation, Blind + Vollmodus)
- ...
```

### Zwei Modi in der after-refactor-Eval

| Modus | Sichtbar für Router | Zweck |
|---|---|---|
| **Blind-Modus** | Nur Name + Description | Misst reines Description-Matching |
| **Vollmodus** | Name + Description + Body | Misst Mehrwert der Body-Delegations-Tabellen aus Phase 5 |

### Phase-5-Abschluss-Report

Der Report in `phase-5-abschluss-report.md` aggregiert die 4 Eval-Durchläufe und dokumentiert:

- Verbleibende ❌ (Score-Regressionen oder persistente Fehltrigger)
- Verbleibende ⚠️ (kontextabhängige Grenzfälle, gewollt)
- `[ARCH-OPEN]`-Einträge für spätere Description-Schärfungen
- Methodische Grenzen (Selbst-Simulation vs. echter API-Blind-Run)

**Gesamtergebnis Phase 5:** Blind-Modus 73/76 (unverändert, erwartbar da Descriptions stabil), Vollmodus 75/76 (+2 gegenüber Baseline — Delegations-Tabellen greifen).


---

## Kapitel 4 — `projects/<projekt>/` — Projekt-spezifische Config

Dieser Ordner isoliert alle Daten, die sich bei einem Projektwechsel ändern würden. Dadurch bleiben die Skills **projekt-agnostisch** — sie lesen ihre projekt-spezifischen Werte zur Laufzeit aus `projects/<[PROJECT]>/`.

### Das aktive Projekt ermitteln

Claude ermittelt das aktive Projekt aus dem Memory-Eintrag `[PROJECT] <n> | ...`. Ist dieser Eintrag nicht vorhanden, listet Claude die Ordner in `projects/` und fragt per `ask_user_input_v0` welches Projekt aktiv ist. Nach User-Auswahl wird der Memory-Eintrag vorgeschlagen und auf Bestätigung geschrieben.

### Aktuell: `projects/bpm/`

| Datei | Inhalt |
|---|---|
| `README.md` | Projekt-Identität: Name, Repo-URL, Memory-Eintragsformat |
| `clickup-lists.md` | Listen-IDs für beide Spaces (BPM-Entwicklung + Claude-Skills), Scope-Erkennungsregeln welche Liste bei welchem Befehl |
| `clickup-fields.md` | Alle 10 Custom Fields mit IDs + Dropdown-Option-IDs + Modul-Kürzel-Tabelle + Status-Werte pro Listen-Typ + BPM-Nummerierungs-Schema |
| `memory-format.md` | Alle BPM-spezifischen Memory-Eintragsformate: `[PROJECT]`, `[CLICKUP]`, `[ANKER-LIVE]` |

### Was gehört in `projects/<projekt>/` vs. `skills/`

Entscheidungsregel aus `docs/project-architecture.md`:

> Wenn eine Information **beim Wechsel zu einem neuen Projekt neu definiert werden müsste** → projekt-spezifisch → `projects/<projekt>/`.  
> Wenn sie **für jedes Projekt gleich sinnvoll** ist → universell → `skills/`.

| Ort | Beispiele |
|---|---|
| `skills/<skill>/` | Kernregeln (Pro-Task-Quittung, em-dash-Verbot), Ablauf-Schritte, universelle Trigger-Phrasen, universelle VERBOTEN-Listen |
| `projects/<projekt>/` | ClickUp-Listen-IDs, Custom-Field-IDs, Dropdown-Option-IDs, Modul-Kürzel, Repo-Pfade, projekt-spezifische Konventionen |

### Fallback-Verhalten

Fehlt der `[PROJECT]`-Memory-Eintrag: Claude bietet Auswahl aus vorhandenen `projects/`-Ordnern an. Fehlt eine benötigte Datei in `projects/<[PROJECT]>/`: Claude läuft im **Universell-Modus** und fragt die benötigten Daten ad-hoc vom User ab, mit dem Hinweis dass eine projekt-spezifische Datei nützlich wäre.

---

## Kapitel 5 — `docs/` — Konzepte und Refactor-Notizen

Enthält tiefgehende Konzept- und Architekturdokumente die nicht in einzelne Skills gehören, aber als Referenz für mehrere Skills dienen.

| Datei | Inhalt |
|---|---|
| `chat-anker-konzept.md` | Draft v2 des Chat-Anker-Systems: Problem (Chat-URLs schwer rückverfolgbar), Ziel (deterministische Rückverfolgung), Kernidee (`[BPM-ANCHOR-<task-id>]`-Format), 3 Phasen (TEMP-ID → Task-ID → erledigt), `[ANKER-LIVE]`-Registry in Memory |
| `project-architecture.md` | Erklärt die Trennung universelle Skills / projekt-spezifische Config, Entscheidungsregel für die Zuordnung, Memory-Mechanismus für das aktive Projekt, Fallback-Verhalten |
| `skill-refactor-phases.md` | Arbeitsnahe Referenz der 5 Refactor-Phasen aus ChatGPT-Review Runde 4 (`CGR-2026-04-skillsystem-r4`). Compact-Format ohne Diskussionskontext — für laufende Sessions als Arbeitsroadmap. |

---

## Kapitel 6 — `reference/` — Externe Referenz-Artefakte

Enthält Artefakte **anderer Projekte oder Quellen**, die als Referenz für den Skill-Aufbau dienen. Wird **nicht modifiziert** — dient nur zum Nachschlagen.

| Verzeichnis | Inhalt |
|---|---|
| `reference/anthropic-skill-creator/` | Anthropic's offizieller `skill-creator` mit `SKILL.md`, `references/`, `scripts/`, `eval-viewer/` und `agents/` — Vergleichsobjekt für die Skill-Architektur. Sofern Anthropic Updates veröffentlicht, werden diese bei Bedarf synchronisiert. |

---

## Kapitel 7 — Top-Level-Dokumente

### `INDEX.md` — Skill-Übersicht und Trigger-Matrix

Der schnelle Einstieg in das Skill-System. Enthält:

- Alphabetische Skill-Liste mit Zweck + Haupt-Trigger
- Skill-Hierarchie (Master-Orchestrator, Meta-Skills, Workflow-Skills, Tool-Wrapper, Modalitäts-Skill)
- Gemeinsame Regeln über alle Skills (Invarianten): `ask_user_input_v0`, Branch-Ermittlung, DC-Pfade, Frühphasen-Prinzip, additive Änderungen
- Abgrenzung zu öffentlichen Skill-Repos

### `CHANGELOG.md` — Versionsverlauf

Umgekehrt chronologisch, pro Versionstag ein Eintrag mit 2-4 Zeilen Beschreibung. Aktuell 60+ Einträge von v0.17.7 (Phase 5.8) bis v0.1.0 (Initial-Commit).

### `MEMORY-RUBRIKEN.md` — Memory-Konvention

Definiert die 4 Rubriken-Prefixe für Memory-Einträge:

| Prefix | Zweck |
|---|---|
| `[VERIFY]` | Ausstehende Prüfung oder Verifikation |
| `[ARCH-OPEN]` | Offene Architektur-/Systementscheidung |
| `[INFRA-TODO]` | Kleine Infra-/Prozessaufgabe, nicht ClickUp-würdig |
| `[REVIEW-PENDING]` | Externe Rückmeldung/Review-Antwort steht aus |

Definiert Format (`[<RUBRIK>] <Kurztext>`), Lifecycle (erstellen, erledigen mit Bestätigung, eskalieren zu ClickUp nach 3 Handovers), Abgrenzung zu ClickUp-Tasks (Faustregel: wenn unsicher → ClickUp), Abgrenzung zu anderen Memory-Konventionen (`[CLICKUP]`, `[SKILL-ISSUES]`, `[ANKER-LIVE]`, `[PROJECT]` haben eigenen Lifecycle).

Die Skill-Integration läuft über vier Skills:

| Skill | Rolle |
|---|---|
| `chat-wechsel` | Memory-Scan bei Handover, Sektion "Offene Punkte aus Memory" im Prompt |
| `skill-neu` | Memory-Disziplin beim Anlegen neuer Skills |
| `skill-pflege` | Memory-Cleanup mit User-Bestätigung, kein stilles Remove |
| `tracker` | Memory-Eskalation: wiederholte Einträge → Vorschlag `tracker neu` |


---

## Kapitel 8 — Refactor-Historie (5 Phasen)

Das Skill-System wurde zwischen v0.1.0 (Initial-Commit am 2026-04-21) und v0.17.7 (Phase-5-Abschluss am 2026-04-24) in 5 Phasen systematisch refactored. Die Phasen-Nummerierung stammt aus dem **ChatGPT-Review Runde 4** (`CGR-2026-04-skillsystem-r4`) und ist in `docs/skill-refactor-phases.md` detailliert dokumentiert.

### Phase 1 — Sofort-Fixes (v0.2.0) ✅

Trigger-Bereinigung an 4 kritischen Skills: Zustimmungsphrasen (`ok`, `passt`) aus `git-commit-helper` entfernt, `antworte darauf` aus `chatgpt-review` ohne expliziten Review-Kontext entfernt, allgemeiner Backlog-Talk aus `tracker` entfernt, Catch-all-Satz aus `code-erstellen` entfernt.

### Phase 1a — Eval-Baseline (v0.3.0 bis v0.4.5) ✅

Eval-Verzeichnis angelegt, Query-Dateien pro Skill (12–16 Queries in 4 Kategorien), problematische Skills priorisiert getestet, Baseline-Scores im Blind-Modus (Name + Description) erfasst. Parallel dazu: Chat-Anker-System Phase 1+2+3 eingeführt (v0.3.1–v0.4.4).

### Phase 2 — Description-Schema-Refactor (v0.5.0) ✅

Alle 9 damaligen Skills auf einheitliches Description-Schema umgestellt: `Zweck-Satz` + `Use when <positive Trigger>` + `Do not trigger for <Negativgrenzen>`.

### Phase 3 — Body-Refactor + Progressive Disclosure (v0.5.1 bis v0.8.0) ✅

Advisory-Block aus `doc-pflege` als Trigger entfernt (3.1), Delegations-Block für 5 Nachbar-Skills in `code-erstellen` (3.2), Progressive Disclosure in `tracker` (147 Zeilen SKILL.md + 13 references/-Dateien, 3.3), neuer `skill-neu`-Skill (3.4+3.5), Skill-Refactor-Phasen-Referenz als arbeitsnahes Dokument (3.6).

### Phase 4 — Memory-Integration + CGR-System (v0.9.0, v0.15.9–v0.16.0) ✅

4.1 chat-wechsel Memory-Scan bei Handover (4 Rubriken), 4.2 skill-neu Memory-Disziplin, 4.3 skill-pflege Memory-Cleanup 3-Schritt-Sequenz, 4.4 tracker Memory-Eskalations-Brücke, 4.5 `MEMORY-RUBRIKEN.md` als Master-Doku, 4.6 chatgpt-review CGR-System (inkrementelle Archivierung von Review-Runden im BPM-Repo).

### Parallelgleise während Phase 3–4 (v0.10.0 bis v0.15.8)

Parallel zum Refactor wurden laufend Skill-Issues abgearbeitet (jeweils als eigener Commit): `tracker-001`..`tracker-009` (Pro-Task-Quittung, Batch-Protokoll, Chat-Anker-System, Referenz-Anker, Scope-Check, Commit-Disziplin, Automatischer Nachlauf, Auto-Nummerierung für Skill-Issues), `cc-steuerung-001`..`cc-steuerung-003` (Tool-basierte DC-Erkennung, PowerShell-`$`-Escaping, DC als Default nach Konzept-Freigabe), `skill-pflege-001`..`skill-pflege-006` (Two-Place-Workflow, Auto-Issue-Erkennung, Artifact-Separation, Artifact-Dateiname, Artifact-Pflicht, Artifact-Tool-Call-Paar).

### Phase 5 — Konfliktpaare + Abschluss-Eval (v0.17.0 bis v0.17.7) ✅

Auflösung der 7 Konfliktpaare aus ChatGPT-Review Runde 3 durch symmetrische Delegations-Tabellen im Body der jeweiligen Skills:

| Paar | Skills | Art | Commit | Version |
|---|---|---|---|---|
| 5.1 | code-erstellen ↔ mockup-erstellen | symmetrisch | `b93388a` | v0.17.0 |
| 5.2 | code-erstellen ↔ git-commit-helper | symmetrisch | `075d248` | v0.17.1 |
| 5.3 | code-erstellen ↔ doc-pflege | symmetrisch | `1e725f9` | v0.17.2 |
| 5.4 | code-erstellen ↔ tracker | symmetrisch | `90c56d3` | v0.17.3 |
| 5.5 | audit ↔ code-erstellen | symmetrisch | `4f750a3` | v0.17.4 |
| 5.6 | chat-wechsel ↔ chatgpt-review | symmetrisch | `5c88d8d` | v0.17.5 |
| 5.7 | cc-steuerung ↔ Fachskills | asymmetrisch (Modalität) | `06b52c4` | v0.17.6 |
| 5.8 | Abschluss-Eval (4 Skills + Report) | — | `83c4114` | v0.17.7 |

Abschluss-Eval (5.8) zeigt im Vollmodus 75/76 (+2 gegenüber Baseline 73/76), Blind-Modus unverändert bei 73/76 — erwartbar, da Phase 5 auf Body-Klarheit zielte, nicht auf Description-Schärfung.

**Offen (als `[ARCH-OPEN]` dokumentiert):** `git-commit-helper` Description um "version-bump"-Keyword erweitern (Query 9), `chatgpt-review` optional "Runde N" als Keyword (Query 6).

---

## Kapitel 9 — Wichtige Workflow-Konventionen

Diese Konventionen werden **in allen Skills** angewendet und sind das Rückgrat des Systems.

### `ask_user_input_v0` statt Prosa-Fragen

Bei **jeder** Entscheidungsfrage mit festen Optionen wird der `ask_user_input_v0`-Mechanismus verwendet — nie eine Prosa-Frage mit Optionen im Chattext. Gilt für: Branch-Wahl, Modus-Auswahl, Datei-Liefermodus (Chat/SUCHE-ERSETZE/DC), Typ/Version bei Commits, Task-Zuordnung, Löschungs-Bestätigungen.

### Branch-Ermittlung vor GitHub-Zugriff

Kein Skill nimmt automatisch an, auf welchem Branch gearbeitet wird. Beim ersten GitHub-Zugriff einer Session wird — falls nicht schon bekannt — per `git branch -a` die Liste geladen und der User wählt per `ask_user_input_v0`. Der gewählte Branch gilt für die gesamte Session.

### Two-Place-Skill-Pflege

Skills werden an zwei Orten gepflegt (`claude-skills-bpm/skills/<n>/SKILL.md` im Repo und `/mnt/skills/user/<n>/SKILL.md` in Claude.ai). Der `skill-pflege`-Skill erzwingt diese Zwei-Orte-Pflege. Der Artifact-Dateiname MUSS exakt `SKILL.md` heißen, sonst fehlt in Claude.ai der "Skill speichern"-Button.

### Commit-Format

```
[vX.Y.Z] Modul, Typ: Kurztitel
```

Typen: `Feature` (→ MINOR), `Fix` (→ PATCH), `Change` (→ PATCH/MINOR), `Refactor` (→ PATCH), `Perf` (→ PATCH), `Docs` (→ PATCH). Semantic-Versioning strikt. Commit-Disziplin: **ein Task = ein Commit** — keine Sammel-Commits.

### Frühphasen-Prinzip

BPM ist in früher Entwicklung ohne Produktivdaten. Schema-/DB-/Config-Änderungen werden **nicht** als Migration dokumentiert, sondern als "Datei löschen, neu anlegen lassen". Gilt in `doc-pflege`, `code-erstellen`, `chatgpt-review` (PFLICHT-Block in jedem Initialprompt). Ausnahme nur auf expliziten User-Wunsch "Migration bauen".

### Additive Skill-Änderungen

Der `skill-pflege`-Skill erzwingt: Bestehender Skill-Inhalt wird **nie gelöscht oder gekürzt** — nur ergänzt. Diff-Report pro Änderung, ein Skill pro Bearbeitungszyklus, `ask_user_input_v0` bevor zum nächsten Skill gewechselt wird.

### DC-Pfade nie hartkodieren

Arbeitsverzeichnisse werden über das Auto-Discovery-Protokoll in `cc-steuerung` Kapitel 4 ermittelt: `hostname` + `[System.Environment]::GetEnvironmentVariable('OneDrive','User')` + PC-Lookup in INDEX.md. Unbekannte PCs werden per Self-Registration in die INDEX.md-PC-Tabelle eingetragen. **Keine** absoluten Pfade wie `C:\Users\herbe\...` im Skill-Body.

### Chat-Anker

Projekt-übergreifendes Tracking zwischen Chat und ClickUp-Tasks via `[BPM-ANCHOR-<task-id>]`-Marker. Im Chat-Body (pro Task-Quittung) + ClickUp-Custom-Fields (`Chat-Anker erstellt` / `Chat-Anker erledigt`). Live-Registry `[ANKER-LIVE]` im Memory. Bei Chat-Wechsel per `chat-wechsel` in den neuen Chat transportiert und im alten Chat geleert. Details in `skills/tracker/references/anker-system.md` und `docs/chat-anker-konzept.md`.


---

## Kapitel 10 — Abgrenzung zu öffentlichen Skill-Repos

Diese Skills sind bewusst **projektspezifisch**. Sie kennen:

- BPM-Docs (INDEX.md, Architektur, DB-SCHEMA, CODING_STANDARDS, DSVGO-Architektur, etc.)
- ClickUp-IDs (Space, Listen, 10 Custom Fields samt Dropdown-Option-IDs)
- BPM-Workflow-Regeln (Commit-Format `[vX.Y.Z] Modul, Typ: Kurztitel`, Ein-Task-Ein-Commit-Disziplin, Pro-Task-Quittung)
- Herberts 3-PC-Setup (Büro-PC "Firmenlaptop" auf D:, Surface7 auf C:, Standrechner)
- CGR-System-Archivierung im BPM-Repo
- `projects/bpm/`-Struktur für projekt-spezifische Daten

Für **generische** Skills (TDD, Debugging, Refactoring, allgemeine Code-Patterns) empfehlen sich öffentliche Repos:

- [obra/superpowers](https://github.com/obra/superpowers) — Workflow-Skills
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) — 235+ Engineering- und Marketing-Skills
- [anthropic/skill-creator](https://docs.claude.com/) — Anthropic-Referenz (eingebettet in `reference/anthropic-skill-creator/`)

---

## Kapitel 11 — Weiterarbeit und Wartung

### Skills ändern

Immer über den `skill-pflege`-Skill:

1. Änderungswunsch formulieren
2. `skill-pflege` lädt aktuellen Skill-Zustand
3. Konzept zeigen, User bestätigen
4. Additive Änderung per DC im Repo + Artifact im Chat
5. Commit-Vorschlag im BPM-Format
6. Task-Zuordnung in ClickUp per `ask_user_input_v0`

### Neuen Skill anlegen

Über den `skill-neu`-Skill:

1. Capture-Intent-Interview (Rolle, Zweck, Trigger, Negativgrenzen, Nachbarn)
2. Description-Schema generieren
3. Body-Template mit Ablauf + Kernregeln + VERBOTEN-Liste
4. Bei Progressive Disclosure: `references/`-Ordner anlegen
5. Test-Prompts in `test-prompts.md` dokumentieren
6. Eval-Matrix anlegen (in `evals/<n>.md`) wenn der Skill potenziell konfliktträchtig ist

### Eval-Runs

Bei substantiellen Skill-Änderungen: Re-Run der Eval-Matrix und neuen Block unter `## Run-Log` anlegen. Blind-Modus und Vollmodus getrennt dokumentieren. Bei Score-Regressionen: gezielt nachbessern (siehe Phase-5-Methodik).

### Memory pflegen

Die 4 Rubriken (`[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]`, `[REVIEW-PENDING]`) werden von den Skills automatisch gescannt (z.B. bei `chat-wechsel`). Einträge werden **nie stillschweigend** entfernt — immer per User-Bestätigung über `ask_user_input_v0`. Eskalation zu ClickUp-Tasks: wenn derselbe Eintrag in 3 Handovers in Folge auftaucht.

### Projekt-Config erweitern

Wenn weitere Skills projekt-spezifische Daten brauchen: neue Datei in `projects/<projekt>/` anlegen, Skill verweist per `projects/<[PROJECT]>/<datei>.md` darauf. Nicht hartkodieren.

---

## Kapitel 12 — Schnellreferenz: Datei-Inventar

Eine vollständige Karte aller versionierten Dateien zum Zeitpunkt dieser README:

```
claude-skills-bpm/
├── README.md                              ← dieses File
├── INDEX.md                               ← Skill-Übersicht und Trigger-Matrix
├── CHANGELOG.md                           ← 60+ Versionseinträge
├── MEMORY-RUBRIKEN.md                     ← Memory-Konvention (4 Rubriken)
│
├── docs/
│   ├── chat-anker-konzept.md              ← Draft v2 Chat-Anker-System
│   ├── project-architecture.md            ← universal vs. projekt-spezifisch
│   └── skill-refactor-phases.md           ← arbeitsnahe Referenz der 5 Phasen
│
├── evals/
│   ├── README.md                          ← Workflow, Kategorien, Scoring
│   ├── _template.md                       ← Vorlage für neue Skill-Evals
│   ├── git-commit-helper.md               ← Query-Katalog + Baseline + after-refactor
│   ├── chatgpt-review.md                  ← dto.
│   ├── tracker.md                         ← dto.
│   ├── code-erstellen.md                  ← dto.
│   └── phase-5-abschluss-report.md        ← Aggregierter Gesamt-Report
│
├── projects/
│   └── bpm/
│       ├── README.md                      ← Projekt-Identität
│       ├── clickup-lists.md               ← Listen-IDs beider Spaces
│       ├── clickup-fields.md              ← 10 Custom Fields + Option-IDs
│       └── memory-format.md               ← BPM-Memory-Eintragsformate
│
├── reference/
│   └── anthropic-skill-creator/           ← Anthropic-Referenz-Skill
│       ├── SKILL.md
│       ├── references/
│       ├── scripts/
│       ├── eval-viewer/
│       ├── agents/
│       └── assets/
│
└── skills/
    ├── audit/SKILL.md
    ├── cc-steuerung/SKILL.md
    ├── chat-wechsel/SKILL.md
    ├── chatgpt-review/SKILL.md
    ├── code-erstellen/SKILL.md
    ├── doc-pflege/SKILL.md
    ├── git-commit-helper/SKILL.md
    ├── mockup-erstellen/SKILL.md
    ├── skill-neu/
    │   ├── SKILL.md
    │   └── test-prompts.md
    ├── skill-pflege/SKILL.md
    └── tracker/
        ├── SKILL.md                       ← Routing-Entry (147 Zeilen)
        └── references/
            ├── anker-system.md
            ├── anti-patterns.md
            ├── batch-protocol.md
            ├── chat-url-handling.md
            ├── clickup-fields.md
            ├── complete-task.md
            ├── create-task.md
            ├── issue-task.md
            ├── review-workflow.md
            ├── search-and-status.md
            ├── split-and-relations.md
            ├── start-task.md
            └── update-task.md
```

---

## Lizenz

Privates Repo von Herbert Schrotter. Keine freie Lizenz. Anthropic-Referenzmaterial unter `reference/anthropic-skill-creator/` folgt der dortigen `LICENSE.txt`.
