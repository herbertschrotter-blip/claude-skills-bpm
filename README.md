# claude-skills-bpm

Claude-Skills von Herbert Schrotter, entstanden im Projekt BauProjektManager (BPM).

Dieses Repo enthält die Skill-Definitionen für 12 Skills samt Evals, Prüfskript, Projekt-Config, Refactor-Dokumentation und Memory-Konventionen. Seit v0.24 (16.09.2026) sind die Skills projektneutral: Projektwerte (Pfade, Präfixe, IDs) kommen aus Profilen in der `CLAUDE.md` des jeweiligen Repos bzw. noch aus `projects/<projekt>/` (BPM, Heidi). Sie sind **nicht** als allgemeine Community-Skills gedacht — für generische Skills siehe z.B. [obra/superpowers](https://github.com/obra/superpowers) oder [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills).

> **Umbau läuft (seit 24.09.2026):** [`docs/skillsystem-umbau.md`](./docs/skillsystem-umbau.md) – Skill-Profil v1,
> Qualitätsregeln, Prüfskript und Routing-Tests; Ergebnis der Review-Serie `CGR-2026-09-24-skillsystem`.

> **Verbindliche Regelquelle:** [INDEX.md](./INDEX.md) definiert Routing und globale Invarianten.
> Dieses README ist Onboarding-Kontext und wiederholt keine operativen Regeln.

---

## Source-of-Truth-Hierarchie

| Quelle | Zuständigkeit |
|---|---|
| [`INDEX.md`](./INDEX.md) | Verbindliche Routing- und Invarianten-Regeln |
| `skills/<skill>/SKILL.md` | Operative skill-spezifische Regeln |
| [`docs/skill-quality.md`](./docs/skill-quality.md) | Verbindliche Qualitätsregeln für Skills (Aufbau, Inhalt, Neutralität, Prüfung) |
| [`docs/skill-profile-v1.md`](./docs/skill-profile-v1.md) | Spezifikation des Skill-Profils in der `CLAUDE.md` eines Repos |
| [`MEMORY-RUBRIKEN.md`](./MEMORY-RUBRIKEN.md) | Verbindliche Memory-Rubrik-Konvention |
| [`evals/README.md`](./evals/README.md) | Eval-Methodik und Scoring (manuelle Evals) |
| `README.md` (diese Datei) | Onboarding und Architektur-Überblick |

---

## Zweck dieses Repos

| Zweck | Beschreibung |
|---|---|
| **Versionshistorie** | Jede Skill-Änderung ist ein Git-Commit. Volle Nachvollziehbarkeit von v0.1.0 bis aktuell. Format-Details siehe [`INDEX.md`](./INDEX.md). |
| **Cross-Review** | ChatGPT kann Skills und Review-Runden direkt aus dem Repo lesen. CGR-System archiviert jede Review-Runde in 4 Dateien. |
| **Backup** | Skills gehen nicht verloren wenn der Claude-Projekt-Speicher reset wird. |
| **Portabilität** | Universelle Skills + projektspezifische Werte sind getrennt (`skills/` vs Profile in der CLAUDE.md des Projekts bzw. noch `projects/<projekt>/`). Neue Projekte nutzen dasselbe Skill-System, indem sie ihr Profil anlegen ([`docs/skill-profile-v1.md`](./docs/skill-profile-v1.md)). |
| **Meta-Werkzeug** | Die Skills reflektieren über sich selbst: `skill-neu` erstellt neue Skills, `skill-pflege` ändert bestehende, `evals/` misst das Routing-Verhalten. |

---

## Verzeichnisstruktur (Überblick)

```
claude-skills-bpm/
├── README.md              ← Dieses File (Onboarding)
├── INDEX.md               ← Verbindliches Routing + globale Invarianten
├── CHANGELOG.md           ← Versionsverlauf
├── CLAUDE.md              ← Skill-Profil dieses Repos (Commit, Checks, Push)
├── MEMORY-RUBRIKEN.md     ← Konvention für 4 Memory-Rubriken
├── .claude/skill-config/  ← Configs der Skills für dieses Repo (tracker, review)
├── .claude-plugin/        ← plugin.json – nur für Tests mit claude plugin eval
├── docs/                  ← Konzepte, Regeln, Reviews, Umbau-Plan
├── evals/                 ← Manuelle Skill-Routing-Evals (bis v0.20)
├── projects/              ← Projekt-spezifische Daten (isoliert pro Projekt)
├── quality/evals/         ← Testfälle für claude plugin eval
├── reference/             ← Externe Referenz-Artefakte
├── skills/                ← 12 Skills, je ein Ordner mit SKILL.md
└── tools/                 ← Prüfskript validate-skills.ps1
```

Die folgenden Kapitel erklären jeden dieser Ordner und die darin liegenden Dateien.

---

## Kapitel 1 — Die 12 Skills im Überblick

Die Skills sind in drei konzeptionelle Gruppen einteilbar: **Fachskills**, **Meta-Skills** und **Modalitäts-Skills**.

> **Verbindliche Trigger:** [`INDEX.md`](./INDEX.md).
> **Operative Regeln je Skill:** `skills/<skill>/SKILL.md`.
> Dieses Kapitel zeigt nur Zweck und grobe Trigger-Beispiele.

### Fachskills (beantworten "WAS wird gemacht")

| Skill | Aufgabe | Trigger-Beispiele |
|---|---|---|
| **code-erstellen** | Master-Orchestrator für Code-Änderungen (Code-Profil in der CLAUDE.md des Projekts). | "implementiere das Feature", "erstelle DocumentTypeRecognizer.cs", "baue Recovery-Logik ein" |
| **mockup-erstellen** | HTML-UI-Mockups nach Mockup-Profil. | "Mockup für ProfileWizard", "Screen-Design", "UI-Mockup" |
| **doc-pflege** | Erstellt und pflegt Projektdokumentation nach Doku-Profil (BPM: DOC-STANDARD.md). | "pflege die docs", "schreib ein ADR", "neues Konzept für X" |
| **ticket** | Fehler-Tickets eines Projekts einzeln und immer im selben Ablauf bearbeiten (acht Schritte). | "ticket liste", "ticket HT-0007", "nimm das nächste ticket" |
| **chatgpt-review** | Strukturierte Cross-LLM-Review-Prompts zwischen Claude und ChatGPT. | "besprich das mit ChatGPT", "zweite Meinung", "Folgeprompt für Runde 3" |
| **audit** | Strikt read-only Konsistenzprüfung zwischen Code, Docs, Frontmatter und Quickload. | "audit", "prüfe alles", "konsistenzcheck" |
| **tracker** | Standardisierte Schreibschnittstelle zum ClickUp-Task-System. | "tracker neu: PM — Regex-Bug", "tracker done BPM-042", "tracker suche Regex" |
| **git-commit-helper** | Fertige Git-Commit-Befehle im Format `[vX.Y.Z] Modul, Typ: Kurztitel` (Commit-Profil). | "commit bitte", "commit-message", "PATCH oder MINOR?" |
| **chat-wechsel** | Handover-Prompt für die nächste Claude-Session. | "neuer chat", "nächster chat", "übergabe" |

### Meta-Skills (ändern andere Skills)

| Skill | Aufgabe |
|---|---|
| **skill-neu** | Erstellt neue Skills von Grund auf (projektneutral). |
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

Der `tracker`-Skill nutzt Progressive Disclosure: Die `SKILL.md` enthält nur Kernregeln und Routing-Tabelle, Details liegen in 14 `references/`-Dateien (anker-system, anti-patterns, batch-protocol, chat-url-handling, clickup-fields, clickup-tools, complete-task, create-task, issue-task, review-workflow, search-and-status, split-and-relations, start-task, update-task). Auch `code-erstellen` hat `references/` (`stacks/`: csharp-wpf, home-assistant-yaml, python, typescript-lit).

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
| `smoke-all-skills.md` | Smoke-Test-Katalog für die 11 Skills bis v0.20 (88 Fälle; ticket fehlt) |
| `methodik-anleitung.md` | Test-Setup-Regeln für Smoke-Läufe (aus dem Lauf vom 28.04.2026) |
| `runs/smoke-2026-04-28-real.md` | Snapshot des manuellen Smoke-Laufs (30 Fälle) |

4 Skills haben detaillierte Evals — die kritischsten aus Phase 1a des Refactors. Die übrigen 8 Skills sind nur im Smoke-Katalog (ticket gar nicht) und werden bedarfsbasiert nachgezogen.

### Neu: automatische Routing-Tests (`quality/evals/`)

Seit Umbau Phase 1 (24.09.2026) gibt es Testfälle für `claude plugin eval` (Manifest `.claude-plugin/plugin.json`, nur
für Tests). Fünf Pilotfälle: audit-readonly, doc-write, code-implement, skill-update, cc-not-in-claude-code. Aufruf und
Schwellen: Skill-Profil in [`CLAUDE.md`](./CLAUDE.md) und [`docs/skillsystem-umbau.md`](./docs/skillsystem-umbau.md).
Die mechanische Prüfung aller Skills macht [`tools/validate-skills.ps1`](./tools/validate-skills.ps1).

### Eval-Methodik

Pro Skill ein Query-Katalog mit Einträgen in 4 Kategorien (`should_trigger`, `should_not_trigger`, `other_skill`, `ambiguous`). Queries sind als `[golden]` (echte BPM-Chat-Formulierung) oder `[synthetic]` (konstruierte Variante) markiert.

> **Operative Regelquelle:** [`evals/README.md`](./evals/README.md).
> Dieses Kapitel zeigt nur die Ordnerstruktur.

### Phase-5-Abschluss-Report

Der Report in `phase-5-abschluss-report.md` aggregiert die 4 Eval-Durchläufe. Gesamtergebnis Phase 5: Blind-Modus 73/76, Vollmodus 75/76.

---

## Kapitel 4 — `projects/<projekt>/` — Projekt-spezifische Config

Dieser Ordner isoliert alle Daten, die sich bei einem Projektwechsel ändern würden. Dadurch bleiben die Skills **projekt-agnostisch** — sie lesen ihre projekt-spezifischen Werte zur Laufzeit aus `projects/<[PROJECT]>/`.

### Aktuell: `projects/bpm/` und `projects/heidi/`

| Datei | Inhalt |
|---|---|
| `README.md` | Projekt-Identität: Name, Repo-URL, Memory-Eintragsformat |
| `clickup-lists.md` | Listen-IDs, Status, Nummernschema (BPM: nur noch der BPM-Space) |
| `clickup-fields.md` | Custom Fields mit IDs + Dropdown-Option-IDs + Modul-Kürzel + Nummerierungs-Schema |
| `memory-format.md` | Memory-Eintragsformate (BPM: `[PROJECT]`, `[CLICKUP]`, `[ANKER-LIVE]`; Heidi: CLAUDE.md-Abschnitt statt Memory) |

`projects/heidi/` ist die Config der Heidi-Karte (Home Assistant, Dreame X60, Repo `HA_Dash_DreameX60`). Die Werte des
Space „Claude Skills Entwicklung“ (Liste ClaudeSkills, Skill-Issue-Listen) stehen seit 24.09.2026 in
`.claude/skill-config/tracker.md`. Laut Umbau-Plan ziehen die Projektwerte in Profile der CLAUDE.md des jeweiligen
Repos (Phase 2); `projects/` wird in Phase 7 entfernt.

### Was gehört in `projects/<projekt>/` vs. `skills/`

| Ort | Beispiele |
|---|---|
| `skills/<skill>/` | Universelle Kernregeln, Ablauf-Schritte, Trigger-Phrasen, VERBOTEN-Listen |
| `projects/<projekt>/` | ClickUp-IDs, Custom-Field-IDs, Modul-Kürzel, Repo-Pfade, projekt-spezifische Konventionen |

> **Operative Regelquelle:** [`docs/skill-profile-v1.md`](./docs/skill-profile-v1.md) (Skill-Profil v1: welche Werte wohin gehören und wie ein Skill sie findet).

---

## Kapitel 5 — `docs/` — Konzepte, Regeln, Reviews

| Datei | Inhalt |
|---|---|
| `chat-anker-konzept.md` | Draft v2 des Chat-Anker-Systems |
| `chatgpt-reviews/` | CGR-Archiv dieses Repos (Serien `CGR-2026-09-23-ha-grundsatz`, `CGR-2026-09-24-skillsystem`) mit `INDEX.md` |
| `fragilitaeten-und-fruehwarn.md` | 4 Fragilitäten mit Frühwarn-Indikatoren (INDEX-Invariante 10) |
| `ha-grundsatz/` | HA-Grundsatzregeln für Home-Assistant-Projekte (im Aufbau, Grundlage für den Skill `modul-bauplan`) |
| `project-architecture.md` | Verweis auf `skill-profile-v1.md` (bleibt, bis tracker umgestellt ist) |
| `skill-profile-v1.md` | Spezifikation Skill-Profil v1 (Abschnitt `## Skill-Profil` in der CLAUDE.md, Configs unter `.claude/skill-config/`) |
| `skill-quality.md` | Verbindliche Qualitätsregeln für Skills |
| `skill-refactor-phases.md` | Arbeitsnahe Referenz der 5 Refactor-Phasen (April 2026) |
| `skillsystem-umbau.md` | Umbau-Plan Phasen 1–7 (seit 24.09.2026) |

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

Umgekehrt chronologisch, pro Versionstag ein Eintrag mit 2-4 Zeilen Beschreibung. Seit 24.09.2026 gibt es eine neue
Nummer nur bei Skill-Änderungen (Versionsregel oben in der Datei).

### `CLAUDE.md` — Skill-Profil dieses Repos

Regeln für die Arbeit in diesem Repo mit Claude Code: Commit-Format und Module, Prüfungen vor dem Commit
(`skill-validation`, `routing-eval`), Versionsquelle, Push nach jedem Commit, Verweise auf die Configs unter
`.claude/skill-config/`.

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

Bis v0.23 waren diese Skills **BPM-spezifisch** (BPM-Docs, ClickUp-IDs, Commit-Format, Herberts 3-PC-Setup,
CGR-Archiv im BPM-Repo). Seit v0.24 (16.09.2026) sind sie projektneutral; sie bleiben aber auf Herberts Arbeitsweise
zugeschnitten:

- Workflow-Regeln (Commit-Format `[vX.Y.Z] Modul, Typ: Kurztitel`, Ein-Task-Ein-Commit, Pro-Task-Quittung)
- ClickUp als Aufgaben-System (Werte je Projekt aus Profil bzw. `projects/<projekt>/`)
- Herberts PCs (Büro-PC auf D:, Surface auf C:, Standrechner)
- CGR-Archivierung der ChatGPT-Reviews im jeweiligen Repo

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

### Prüfen und Eval-Runs

Vor jedem Commit an Skills: `pwsh -NoProfile -File tools/validate-skills.ps1` (mechanische Prüfung). Nach Änderungen an
einer description und vor dem Hochladen: die betroffenen Fälle mit `claude plugin eval` (Befehl im Skill-Profil der
[`CLAUDE.md`](./CLAUDE.md)). Die manuellen Evals unter `evals/` bleiben als Archiv.

> **Operative Regelquelle:** [`docs/skill-quality.md`](./docs/skill-quality.md) und [`docs/skillsystem-umbau.md`](./docs/skillsystem-umbau.md); für die manuellen Evals [`evals/README.md`](./evals/README.md).

### Memory pflegen

Die 4 Rubriken werden automatisch beim Handover gescannt. Einträge werden nie stillschweigend entfernt.

> **Operative Regelquelle:** [`MEMORY-RUBRIKEN.md`](./MEMORY-RUBRIKEN.md).

### Projekt-Config erweitern

Wenn weitere Skills projekt-spezifische Daten brauchen: nach Skill-Profil v1 als Feld im `## Skill-Profil` der
CLAUDE.md des Projekts oder als Config unter `.claude/skill-config/`. Bis zur Umstellung der Skills (Umbau Phase 3–6)
lesen tracker und git-commit-helper noch `projects/<[PROJECT]>/<datei>.md`.

> **Operative Regelquelle:** [`docs/skill-profile-v1.md`](./docs/skill-profile-v1.md).

---

## Kapitel 12 — Schnellreferenz: Datei-Inventar

```
claude-skills-bpm/
├── README.md                              ← dieses File (Onboarding)
├── INDEX.md                               ← Routing + globale Invarianten (verbindlich)
├── CHANGELOG.md                           ← Versionseinträge
├── CLAUDE.md                              ← Skill-Profil dieses Repos
├── MEMORY-RUBRIKEN.md                     ← Memory-Konvention (4 Rubriken)
├── .gitignore
│
├── .claude/skill-config/
│   ├── review.md                          ← Config für chatgpt-review
│   └── tracker.md                         ← Config für tracker (Space Claude Skills Entwicklung)
│
├── .claude-plugin/
│   └── plugin.json                        ← nur für claude plugin eval
│
├── docs/
│   ├── chat-anker-konzept.md
│   ├── chatgpt-reviews/                   ← CGR-Archiv + INDEX.md
│   ├── fragilitaeten-und-fruehwarn.md
│   ├── ha-grundsatz/
│   ├── project-architecture.md            ← Verweis auf skill-profile-v1.md
│   ├── skill-profile-v1.md
│   ├── skill-quality.md
│   ├── skill-refactor-phases.md
│   └── skillsystem-umbau.md
│
├── evals/
│   ├── README.md                          ← Eval-Methodik + Scoring
│   ├── _template.md
│   ├── git-commit-helper.md
│   ├── chatgpt-review.md
│   ├── tracker.md
│   ├── code-erstellen.md
│   ├── methodik-anleitung.md
│   ├── phase-5-abschluss-report.md
│   ├── smoke-all-skills.md
│   └── runs/
│
├── projects/
│   ├── bpm/
│   │   ├── README.md
│   │   ├── clickup-lists.md
│   │   ├── clickup-fields.md
│   │   └── memory-format.md
│   └── heidi/                             ← dieselben 4 Dateien
│
├── quality/evals/                         ← 5 Pilotfälle (prompt.md + graders/)
│
├── reference/
│   └── anthropic-skill-creator/
│
├── skills/
│   ├── audit/SKILL.md
│   ├── cc-steuerung/SKILL.md
│   ├── chat-wechsel/SKILL.md
│   ├── chatgpt-review/SKILL.md
│   ├── code-erstellen/
│   │   ├── SKILL.md
│   │   └── references/stacks/
│   ├── doc-pflege/SKILL.md
│   ├── git-commit-helper/SKILL.md
│   ├── mockup-erstellen/SKILL.md
│   ├── skill-neu/                         ← SKILL.md + test-prompts.md
│   ├── skill-pflege/SKILL.md
│   ├── ticket/                            ← SKILL.md + test-prompts.md
│   └── tracker/
│       ├── SKILL.md
│       ├── references/
│       └── references.zip                 ← entfällt in Umbau Phase 7
│
└── tools/
    └── validate-skills.ps1                ← Prüfskript (PowerShell 7)
```

---

## Lizenz

Privates Repo von Herbert Schrotter. Keine freie Lizenz. Anthropic-Referenzmaterial unter `reference/anthropic-skill-creator/` folgt der dortigen `LICENSE.txt`.
