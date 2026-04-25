# claude-skills-bpm

Claude-Skills für das BauProjektManager (BPM) Projekt von Herbert Schrotter.

Dieses Repo enthält die Skill-Definitionen für 11 BPM-spezifische Skills samt Eval-Matrix, Projekt-Config, Refactor-Dokumentation und Memory-Konventionen. Die Skills sind gezielt auf den BPM-Workflow optimiert und kennen die BPM-Docs, ClickUp-IDs, Modul-Kürzel und Commit-Konventionen. Sie sind **nicht** als allgemeine Community-Skills gedacht — für generische Skills siehe z.B. [obra/superpowers](https://github.com/obra/superpowers) oder [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills).

> **Verbindliche Regelquelle:** [INDEX.md](./INDEX.md) definiert Routing und globale Invarianten.
> Dieses README ist Onboarding-Kontext und wiederholt keine operativen Regeln.

---

## Source-of-Truth-Hierarchie

| Quelle | Zuständigkeit |
|---|---|
| [`INDEX.md`](./INDEX.md) | Verbindliche Routing- und Invarianten-Regeln |
| `skills/<skill>/SKILL.md` | Operative skill-spezifische Regeln |
| [`MEMORY-RUBRIKEN.md`](./MEMORY-RUBRIKEN.md) | Verbindliche Memory-Rubrik-Konvention |
| [`evals/README.md`](./evals/README.md) | Eval-Methodik und Scoring |
| `README.md` (diese Datei) | Onboarding und Architektur-Überblick |

---

## Zweck dieses Repos

| Zweck | Beschreibung |
|---|---|
| **Versionshistorie** | Jede Skill-Änderung ist ein Git-Commit. Volle Nachvollziehbarkeit von v0.1.0 bis aktuell. Format-Details siehe [`INDEX.md`](./INDEX.md). |
| **Cross-Review** | ChatGPT kann Skills und Review-Runden direkt aus dem Repo lesen. CGR-System archiviert jede Review-Runde in 4 Dateien. |
| **Backup** | Skills gehen nicht verloren wenn der Claude-Projekt-Speicher reset wird. |
| **Portabilität** | Universelle Skills + projektspezifische Config sind getrennt (`skills/` vs `projects/<projekt>/`). Neue Projekte können dasselbe Skill-System nutzen indem sie nur ihren `projects/<n>/`-Ordner anlegen. |
| **Meta-Werkzeug** | Die Skills reflektieren über sich selbst: `skill-neu` erstellt neue Skills, `skill-pflege` ändert bestehende, `evals/` misst das Routing-Verhalten. |

---

## Verzeichnisstruktur (Überblick)

```
claude-skills-bpm/
├── README.md              ← Dieses File (Onboarding)
├── INDEX.md               ← Verbindliches Routing + globale Invarianten
├── CHANGELOG.md           ← Versionsverlauf
├── MEMORY-RUBRIKEN.md     ← Konvention für 4 Memory-Rubriken
├── docs/                  ← Konzepte und Refactor-Notizen
├── evals/                 ← Skill-Routing-Evals
├── projects/              ← Projekt-spezifische Daten (isoliert pro Projekt)
├── reference/             ← Externe Referenz-Artefakte
└── skills/                ← 11 Skills, je ein Ordner mit SKILL.md
```

Die folgenden Kapitel erklären jeden dieser Ordner und die darin liegenden Dateien.

---

## Kapitel 1 — Die 11 Skills im Überblick

Die Skills sind in drei konzeptionelle Gruppen einteilbar: **Fachskills**, **Meta-Skills** und **Modalitäts-Skills**.

> **Verbindliche Trigger:** [`INDEX.md`](./INDEX.md).
> **Operative Regeln je Skill:** `skills/<skill>/SKILL.md`.
> Dieses Kapitel zeigt nur Zweck und grobe Trigger-Beispiele.

### Fachskills (beantworten "WAS wird gemacht")

| Skill | Aufgabe | Trigger-Beispiele |
|---|---|---|
| **code-erstellen** | Master-Orchestrator für BPM-Code-Änderungen. | "implementiere das Feature", "erstelle DocumentTypeRecognizer.cs", "baue Recovery-Logik ein" |
| **mockup-erstellen** | HTML-UI-Mockups für BPM-Screens. | "Mockup für ProfileWizard", "Screen-Design", "UI-Mockup" |
| **doc-pflege** | Erstellt und pflegt BPM-Dokumentation nach DOC-STANDARD.md. | "pflege die docs", "schreib ein ADR", "neues Konzept für X" |
| **chatgpt-review** | Strukturierte Cross-LLM-Review-Prompts zwischen Claude und ChatGPT. | "besprich das mit ChatGPT", "zweite Meinung", "Folgeprompt für Runde 3" |
| **audit** | Strikt read-only Konsistenzprüfung zwischen Code, Docs, Frontmatter und Quickload. | "audit", "prüfe alles", "konsistenzcheck" |
| **tracker** | Standardisierte Schreibschnittstelle zum ClickUp-Task-System. | "tracker neu: PM — Regex-Bug", "tracker done BPM-042", "tracker suche Regex" |
| **git-commit-helper** | Fertige Git-Commit-Befehle im BPM-Format. | "commit bitte", "commit-message", "PATCH oder MINOR?" |
| **chat-wechsel** | Handover-Prompt für die nächste Claude-Session. | "neuer chat", "nächster chat", "übergabe" |

### Meta-Skills (ändern andere Skills)

| Skill | Aufgabe |
|---|---|
| **skill-neu** | Erstellt neue BPM-Skills von Grund auf. |
| **skill-pflege** | Ändert und erweitert bestehende Skills additiv. |

### Modalitäts-Skill (beantwortet "WIE wird ausgeführt")

| Skill | Aufgabe |
|---|---|
| **cc-steuerung** | Steuert den Desktop Commander (DC) MCP-Server für direkte File-/Terminal-Operationen auf Herberts PC. Läuft parallel zu Fachskills. |

---

## Kapitel 2 — `skills/` — Die Skill-Dateien

### Struktur pro Skill

```
skills/<skill-name>/
├── SKILL.md              ← Die Skill-Definition (Frontmatter + Body)
├── references/           ← (optional) Progressive Disclosure Details
│   ├── <aspekt-1>.md
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

Der Body enthält je nach Skill: Zweck, Vorrang/Delegation, Kernregeln, Ablauf, Reference-Tabelle (bei Progressive Disclosure), VERBOTEN-Liste.

> **Operative Regelquelle:** Frontmatter-Schema und Body-Struktur sind in [`INDEX.md`](./INDEX.md) und den jeweiligen Skill-Dateien definiert.

### Progressive Disclosure — am Beispiel `tracker`

Der `tracker`-Skill nutzt Progressive Disclosure: Die `SKILL.md` enthält nur Kernregeln und Routing-Tabelle, Details liegen in 13 `references/`-Dateien (anker-system, anti-patterns, batch-protocol, chat-url-handling, clickup-fields, complete-task, create-task, issue-task, review-workflow, search-and-status, split-and-relations, start-task, update-task).

> **Operative Regelquelle:** [`skills/tracker/SKILL.md`](./skills/tracker/SKILL.md).

### Two-Place-Pflege

Skills werden an zwei Orten gepflegt: `claude-skills-bpm/skills/<n>/SKILL.md` (Repo) und `/mnt/skills/user/<n>/SKILL.md` (Claude.ai).

> **Operative Regelquelle:** [`skills/skill-pflege/SKILL.md`](./skills/skill-pflege/SKILL.md) und [`INDEX.md`](./INDEX.md).

---

## Kapitel 3 — `evals/` — Skill-Routing-Evaluation

Das Eval-System misst, ob ein Skill bei den richtigen Queries triggert und bei den falschen nicht.

### Dateien

| Datei | Inhalt |
|---|---|
| `README.md` | Workflow, Kategorien, Scoring-Schema |
| `_template.md` | Vorlage für neue Skill-Evals |
| `git-commit-helper.md` | Query-Katalog + Run-Log |
| `chatgpt-review.md` | dto. |
| `tracker.md` | dto. |
| `code-erstellen.md` | dto. |
| `phase-5-abschluss-report.md` | Aggregierter Gesamt-Report der Phase-5-Abschluss-Eval |
| `smoke-all-skills.md` | (geplant) Smoke-Test-Katalog für alle 11 Skills |

Aktuell haben 4 Skills detaillierte Evals — die kritischsten aus Phase 1a des Refactors. Die übrigen 7 Skills werden bedarfsbasiert bei Trigger-Problemen nachgezogen.

### Eval-Methodik

Pro Skill ein Query-Katalog mit Einträgen in 4 Kategorien (`should_trigger`, `should_not_trigger`, `other_skill`, `ambiguous`). Queries sind als `[golden]` (echte BPM-Chat-Formulierung) oder `[synthetic]` (konstruierte Variante) markiert.

> **Operative Regelquelle:** [`evals/README.md`](./evals/README.md).
> Dieses Kapitel zeigt nur die Ordnerstruktur.

### Phase-5-Abschluss-Report

Der Report in `phase-5-abschluss-report.md` aggregiert die 4 Eval-Durchläufe. Gesamtergebnis Phase 5: Blind-Modus 73/76, Vollmodus 75/76.

---

## Kapitel 4 — `projects/<projekt>/` — Projekt-spezifische Config

Dieser Ordner isoliert alle Daten, die sich bei einem Projektwechsel ändern würden. Dadurch bleiben die Skills **projekt-agnostisch** — sie lesen ihre projekt-spezifischen Werte zur Laufzeit aus `projects/<[PROJECT]>/`.

### Aktuell: `projects/bpm/`

| Datei | Inhalt |
|---|---|
| `README.md` | Projekt-Identität: Name, Repo-URL, Memory-Eintragsformat |
| `clickup-lists.md` | Listen-IDs für beide Spaces (BPM-Entwicklung + Claude-Skills) |
| `clickup-fields.md` | 10 Custom Fields mit IDs + Dropdown-Option-IDs + Modul-Kürzel + BPM-Nummerierungs-Schema |
| `memory-format.md` | BPM-spezifische Memory-Eintragsformate: `[PROJECT]`, `[CLICKUP]`, `[ANKER-LIVE]` |

### Was gehört in `projects/<projekt>/` vs. `skills/`

| Ort | Beispiele |
|---|---|
| `skills/<skill>/` | Universelle Kernregeln, Ablauf-Schritte, Trigger-Phrasen, VERBOTEN-Listen |
| `projects/<projekt>/` | ClickUp-IDs, Custom-Field-IDs, Modul-Kürzel, Repo-Pfade, projekt-spezifische Konventionen |

> **Operative Regelquelle:** [`docs/project-architecture.md`](./docs/project-architecture.md) für die Entscheidungsregel und das aktive-Projekt-Mechanismus.

---

## Kapitel 5 — `docs/` — Konzepte und Refactor-Notizen

| Datei | Inhalt |
|---|---|
| `chat-anker-konzept.md` | Draft v2 des Chat-Anker-Systems |
| `project-architecture.md` | Trennung universelle Skills / projekt-spezifische Config |
| `skill-refactor-phases.md` | Arbeitsnahe Referenz der 5 Refactor-Phasen |

---

## Kapitel 6 — `reference/` — Externe Referenz-Artefakte

Enthält Artefakte **anderer Projekte oder Quellen**, die als Referenz dienen. Wird **nicht modifiziert**.

| Verzeichnis | Inhalt |
|---|---|
| `reference/anthropic-skill-creator/` | Anthropic's offizieller `skill-creator` als Vergleichsobjekt |

---

## Kapitel 7 — Top-Level-Dokumente

### `INDEX.md` — Routing und globale Invarianten

Die **verbindliche Regelquelle** des Skill-Systems. Enthält Skill-Übersicht, Trigger-Matrix, Skill-Hierarchie und gemeinsame Invarianten über alle Skills.

### `CHANGELOG.md` — Versionsverlauf

Umgekehrt chronologisch, pro Versionstag ein Eintrag mit 2-4 Zeilen Beschreibung.

### `MEMORY-RUBRIKEN.md` — Memory-Konvention

Definiert die 4 Rubriken-Prefixe für Memory-Einträge: `[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]`, `[REVIEW-PENDING]`.

> **Operative Regelquelle:** [`MEMORY-RUBRIKEN.md`](./MEMORY-RUBRIKEN.md).
> README enthält nur eine Kurzbeschreibung.

---

## Kapitel 8 — Refactor-Historie

Das Skill-System wurde zwischen v0.1.0 (2026-04-21) und v0.17.7 (2026-04-24) in 5 Phasen systematisch refactored. Die Phasen-Nummerierung stammt aus dem ChatGPT-Review Runde 4 (`CGR-2026-04-skillsystem-r4`).

| Phase | Inhalt |
|---|---|
| **Phase 1** | Sofort-Fixes — Trigger-Bereinigung an 4 kritischen Skills |
| **Phase 1a** | Eval-Baseline — Verzeichnis, Query-Dateien pro Skill, Baseline-Scores im Blind-Modus |
| **Phase 2** | Description-Schema-Refactor — alle 9 Skills auf einheitliches Schema |
| **Phase 3** | Body-Refactor + Progressive Disclosure — Delegations-Blöcke, `tracker` mit references/, neuer `skill-neu` |
| **Phase 4** | Memory-Integration + CGR-System — 4 Memory-Rubriken, Cross-Review-Archivierung |
| **Phase 5** | Konfliktpaare + Abschluss-Eval — symmetrische Delegations-Tabellen für 7 Konfliktpaare |

> **Detail-Quelle:** [`CHANGELOG.md`](./CHANGELOG.md) für Versionseinträge, [`docs/skill-refactor-phases.md`](./docs/skill-refactor-phases.md) für die arbeitsnahe Phasen-Referenz.

---

## Kapitel 9 — Workflow-Konventionen

Workflow-Konventionen (Branch-Ermittlung, `ask_user_input_v0`-Disziplin, Two-Place-Pflege, Commit-Format, Frühphasen-Prinzip, additive Skill-Änderungen, DC-Pfade, Chat-Anker) sind in den verbindlichen Regelquellen definiert — nicht in dieser README.

> **Verbindliche Regelquelle:** [`INDEX.md`](./INDEX.md) für globale Invarianten.
> **Operative Skill-Regeln:** jeweilige `skills/<skill>/SKILL.md`.
> **Memory-Konvention:** [`MEMORY-RUBRIKEN.md`](./MEMORY-RUBRIKEN.md).

---

## Kapitel 10 — Abgrenzung zu öffentlichen Skill-Repos

Diese Skills sind bewusst **projektspezifisch**. Sie kennen:

- BPM-Docs (INDEX.md, Architektur, DB-SCHEMA, CODING_STANDARDS, DSVGO-Architektur)
- ClickUp-IDs (Space, Listen, 10 Custom Fields)
- BPM-Workflow-Regeln (Commit-Format, Ein-Task-Ein-Commit-Disziplin, Pro-Task-Quittung)
- Herberts 3-PC-Setup (Büro-PC auf D:, Surface auf C:, Standrechner)
- CGR-System-Archivierung im BPM-Repo
- `projects/bpm/`-Struktur für projekt-spezifische Daten

Für **generische** Skills (TDD, Debugging, Refactoring, allgemeine Code-Patterns) empfehlen sich öffentliche Repos:

- [obra/superpowers](https://github.com/obra/superpowers) — Workflow-Skills
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) — 235+ Engineering- und Marketing-Skills
- [anthropic/skill-creator](https://docs.claude.com/) — Anthropic-Referenz (eingebettet in `reference/anthropic-skill-creator/`)

---

## Kapitel 11 — Weiterarbeit und Wartung

### Skills ändern

Über den `skill-pflege`-Skill — Two-Place-Pflege (Repo + Claude.ai-Artifact).

> **Operative Regelquelle:** [`skills/skill-pflege/SKILL.md`](./skills/skill-pflege/SKILL.md).

### Neuen Skill anlegen

Über den `skill-neu`-Skill — Capture-Intent-Interview, Description-Schema, Body-Template, optional `references/`-Aufteilung.

> **Operative Regelquelle:** [`skills/skill-neu/SKILL.md`](./skills/skill-neu/SKILL.md).

### Eval-Runs

Bei substantiellen Skill-Änderungen: Re-Run der Eval-Matrix mit neuem Run-Log-Block.

> **Operative Regelquelle:** [`evals/README.md`](./evals/README.md).

### Memory pflegen

Die 4 Rubriken werden automatisch beim Handover gescannt. Einträge werden nie stillschweigend entfernt.

> **Operative Regelquelle:** [`MEMORY-RUBRIKEN.md`](./MEMORY-RUBRIKEN.md).

### Projekt-Config erweitern

Wenn weitere Skills projekt-spezifische Daten brauchen: neue Datei in `projects/<projekt>/` anlegen, Skill verweist per `projects/<[PROJECT]>/<datei>.md` darauf.

> **Operative Regelquelle:** [`docs/project-architecture.md`](./docs/project-architecture.md).

---

## Kapitel 12 — Schnellreferenz: Datei-Inventar

```
claude-skills-bpm/
├── README.md                              ← dieses File (Onboarding)
├── INDEX.md                               ← Routing + globale Invarianten (verbindlich)
├── CHANGELOG.md                           ← Versionseinträge
├── MEMORY-RUBRIKEN.md                     ← Memory-Konvention (4 Rubriken)
│
├── docs/
│   ├── chat-anker-konzept.md
│   ├── project-architecture.md
│   └── skill-refactor-phases.md
│
├── evals/
│   ├── README.md                          ← Eval-Methodik + Scoring
│   ├── _template.md
│   ├── git-commit-helper.md
│   ├── chatgpt-review.md
│   ├── tracker.md
│   ├── code-erstellen.md
│   └── phase-5-abschluss-report.md
│
├── projects/
│   └── bpm/
│       ├── README.md
│       ├── clickup-lists.md
│       ├── clickup-fields.md
│       └── memory-format.md
│
├── reference/
│   └── anthropic-skill-creator/
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
    ├── skill-pflege/SKILL.md
    └── tracker/
        ├── SKILL.md
        └── references/
```

---

## Lizenz

Privates Repo von Herbert Schrotter. Keine freie Lizenz. Anthropic-Referenzmaterial unter `reference/anthropic-skill-creator/` folgt der dortigen `LICENSE.txt`.
