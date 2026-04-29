# INDEX — Skill-Übersicht

Routing-Matrix für die 11 Skills im `claude-skills-bpm` Projekt.

Für tiefe Erklärungen aller Ordner und Dateien siehe [README.md](./README.md).
Für Versionsverlauf siehe [CHANGELOG.md](./CHANGELOG.md).

---

## Skills in alphabetischer Reihenfolge

| Skill | Zweck | Haupt-Trigger |
|-------|-------|---------------|
| **audit** | Konsistenz zwischen Code und Docs prüfen (read-only) | "audit", "prüfe alles", "konsistenzcheck" |
| **cc-steuerung** | Desktop Commander (DC) MCP-Server steuern (Modalität) | "cc mach", "dc lies", "claude code soll" |
| **chat-wechsel** | Handover-Prompt für nächsten Chat erstellen | "neuer chat", "übergabe", "chat wechsel" |
| **chatgpt-review** | Cross-Review-Prompts für ChatGPT + CGR-Archivierung | "besprich mit ChatGPT", "zweite Meinung", "Runde N" |
| **code-erstellen** | Master-Orchestrator für BPM-Code-Erstellung | Jede Anfrage die Code-Erstellung impliziert |
| **doc-pflege** | Dokumentations-Updates nach DOC-STANDARD.md | "pflege docs", "schreib ADR", "neues Konzept" |
| **git-commit-helper** | Commit-Befehle im BPM-Format generieren | "commit", "git commit", "PATCH oder MINOR?" |
| **mockup-erstellen** | HTML-UI-Mockups für BPM-Screens erstellen | "Mockup für", "Screen-Design", "UI-Mockup" |
| **skill-neu** | Neue BPM-Skills von Grund auf erstellen | "neuer Skill für X", "erstelle einen Skill" |
| **skill-pflege** | Bestehende Skills additiv ändern | "Skill updaten", "Skill ändern", "Skill erweitern" |
| **tracker** | ClickUp-Schreibschnittstelle für BPM-Tasks | "tracker neu", "tracker done", "tracker suche" |


---

## Skill-Hierarchie

### Master-Orchestrator

- **code-erstellen** — Ruft andere Skills auf bei Code-Tasks. Lädt INDEX.md, Quickloads, Invarianten. Delegiert an mockup-erstellen, git-commit-helper, doc-pflege, tracker, audit.

### Meta-Skills (ändern andere Dinge)

- **skill-neu** — Erstellt neue Skills von Grund auf
- **skill-pflege** — Ändert bestehende Skills additiv
- **doc-pflege** — Ändert Docs

### Workflow-Skills

- **chat-wechsel** — Session-Ende, Handover
- **chatgpt-review** — Cross-LLM-Review, CGR-Archivierung
- **audit** — Read-only Konsistenzprüfung

### Tool-Wrapper (Integration mit externen Systemen)

- **tracker** — ClickUp-Schreibschnittstelle
- **git-commit-helper** — Git-Commits
- **mockup-erstellen** — HTML-UI-Mockups

### Modalitäts-Skill (WIE statt WAS)

- **cc-steuerung** — Desktop Commander (DC). Läuft **parallel** zu Fachskills, kein Fachvorrang.

---

## Konfliktpaar-Delegation (Phase 5)

Die Paar-Konflikte wurden durch Delegations-Tabellen im Body der jeweiligen Skills entschärft. Im Zweifel siehe die "Vorrang / Delegation"-Abschnitte in den SKILL.md-Bodies.

| Konflikt-Paar | Entscheidungsregel |
|---|---|
| code-erstellen ↔ mockup-erstellen | XAML/Code → code-erstellen; HTML-Mockup → mockup-erstellen |
| code-erstellen ↔ git-commit-helper | Code-Änderung inkl. Inline-Commit-Vorschlag → code-erstellen; expliziter Commit-Request → git-commit-helper |
| code-erstellen ↔ doc-pflege | Advisory-Hinweise aus code-erstellen → KEIN Trigger für doc-pflege; expliziter Doc-Auftrag → doc-pflege |
| code-erstellen ↔ tracker | Code (auch mit Task-Bezug) → code-erstellen; expliziter Tracker-Befehl → tracker |
| audit ↔ code-erstellen | Read-only Prüfung → audit; Fixes → code-erstellen (Delegation per ask_user_input_v0) |
| chat-wechsel ↔ chatgpt-review | Claude-Handover → chat-wechsel; ChatGPT-Review-Prompt → chatgpt-review; generisch → ask_user_input_v0 |
| cc-steuerung ↔ Fachskills | asymmetrisch: cc-steuerung ist Modalität (WIE), Fachskills bleiben für WAS zuständig. Beide können gleichzeitig aktiv sein. |


---

## Gemeinsame Regeln in allen Skills (Invarianten)

Alle Skills folgen diesen Konventionen. Sie sind die DNA des Skill-Systems und wurden in den Phasen 1–5 des Refactors systematisch durchgezogen.

### 1. `ask_user_input_v0` bei Entscheidungen (Phase 1)

KEINE Prosa-Fragen bei festen Entscheidungsoptionen. Jede "A oder B?"-Frage geht durch `ask_user_input_v0`. Gilt für: Branch-Wahl, Modus-Auswahl, Liefermodus (Chat/SUCHE-ERSETZE/DC), Commit-Typ, Version-Bump, Task-Zuordnung, Löschungen.

### 2. Branch-Ermittlung (Phase 1)

Nie automatisch annehmen — bei jedem GitHub-Zugriff den Branch aus `git branch -a` per `ask_user_input_v0` wählen lassen. Einmal gewählt gilt er für die ganze Session.

### 3. DC-Pfade dynamisch ermitteln (cc-steuerung-001 + 002)

Keine hartkodierten Pfade. Auto-Discovery via `hostname` + `[System.Environment]::GetEnvironmentVariable('OneDrive','User')` + PC-Lookup in INDEX.md. KEINE `$`-Variablen-Assignments in PowerShell-Command-Strings (äußere Shell-Schicht interpoliert sie zu leerem String).

### 4. Frühphasen-Prinzip (Phase 3.1)

Keine Migrations-Logik ohne explizite User-Freigabe. Schema-/DB-/Config-Änderungen werden als "Datei löschen, neu anlegen lassen" dokumentiert, nicht als Migration. Gilt in `doc-pflege`, `code-erstellen`, `chatgpt-review` (PFLICHT-Block im Initialprompt).

### 5. Additive Skill-Änderungen (skill-pflege-001)

Bestehende Skill-Inhalte werden **nie gelöscht oder gekürzt** — nur ergänzt. Ein Skill pro Bearbeitungszyklus, `ask_user_input_v0` vor Wechsel zum nächsten.

### 6. Pro-Task-Quittung (tracker-001)

Nach jedem ClickUp-`create`/`status-change`-Update MUSS eine Quittungszeile im selben Antwort-Block stehen: `✅ <ID> — [BPM-ANCHOR-<task-id>] — <typ>: <kurz>`. Bei ≥2 Task-Operationen greift das Batch-Protokoll (Ansage → Pro-Task-Zyklus → Audit).

### 7. Memory-Rubriken (Phase 4.5)

Offene Punkte im Memory werden nach 4 Rubriken strukturiert: `[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]`, `[REVIEW-PENDING]`. Details in [MEMORY-RUBRIKEN.md](./MEMORY-RUBRIKEN.md). Der `chat-wechsel`-Skill scannt diese Rubriken bei jedem Handover und übernimmt sie in den Prompt. Einträge werden NIE stillschweigend entfernt.

### 8. Two-Place-Skill-Pflege (skill-pflege-001)

Skills werden an zwei Orten gepflegt: `claude-skills-bpm/skills/<n>/SKILL.md` (Repo via DC) und `/mnt/skills/user/<n>/SKILL.md` (Claude.ai via Artifact). Artifact-Dateiname MUSS exakt `SKILL.md` heißen, sonst fehlt der "Skill speichern"-Button. Nach jedem Skill-Commit ist der Artifact-Block Pflicht.

### 9. Modalitäts-Skill `cc-steuerung` läuft parallel zu Fachskills (Phase 5.7)

`cc-steuerung` ist kein konkurrierender Fachskill, sondern eine Ausführungs-Modalität für Desktop Commander / Claude Code / direkte PC-Operationen.

**Trigger für die Modalität:**
- `cc`
- `dc`
- `Claude Code`
- `direkt auf den PC`
- explizite Datei-/Terminal-/Build-/Git-Ausführung auf dem User-PC

**Entscheidungsregel:**
- Das **WAS** bleibt beim Fachskill (`code-erstellen`, `tracker`, `git-commit-helper`, `doc-pflege`, `audit`, `mockup-erstellen`, etc.)
- Das **WIE** kommt zusätzlich von `cc-steuerung`
- Bei `cc`/`dc` ohne fachliches WAS: Claude fragt per `ask_user_input_v0` nach der Zielaktion
- Datei-/Repo-Nennung allein triggert `cc-steuerung` nicht — explizite PC-/DC-/Ausführungsabsicht ist nötig

**Smoke-Test-Pflicht:**
- Multi-Intent-Fälle (`cc + code`, `cc + commit`, `cc + tracker`, `cc + audit`, `cc + mockup`) werden in `evals/smoke-all-skills.md` geprüft
- **Exit-Kriterium:** Wenn 2+ Multi-Trigger-Cases in realer Claude.ai-Nutzung nur einen Skill faktisch berücksichtigen, wird Variante A umgesetzt — kurzer Modalitätsblock zusätzlich in den betroffenen Fachskills

**Quellen:** CGR-2026-04-skillsystem-r5/r6, ClickUp-Task `86c9gmjan`

### 10. Fragilitäten und Frühwarn-Indikatoren (P3.2)

Vier dokumentierte Fragilitäten mit konkreten Beobachtungssignalen und
Sofortmaßnahmen — Pflichtlektüre vor jedem Smoke-Run und beim Handover-Check.

| # | Fragilität | Hauptsignal |
|---|---|---|
| 1 | cc-steuerung-Pfad-/Modalitätsfragilität | Codeblöcke statt Dateioperation, hartkodierte Pfade, `$`-Variablen |
| 2 | Tracker-Anker / Task-Scope-Disziplin | Fehlender Anker, `tracker done` ohne Hash, Multi-Task-Commit |
| 3 | Memory-Schatten-Backlog | 5+ offene Punkte, 3-Handovers-Wiederkehr, unklare Formulierung |
| 4 | Frühphasen-Verstoss | Migration/Legacy-Vorschläge, Backward-Compat ohne Auftrag |

Volldoku mit Indikatoren, Sofortmaßnahmen, Beispielen und Gegenbeispielen:
[docs/fragilitaeten-und-fruehwarn.md](./docs/fragilitaeten-und-fruehwarn.md).

`chat-wechsel` (Memory-Scan Schritt 4) prüft diese Indikatoren beim Handover
und nimmt Treffer als Eskalationshinweis in den Übergabeprompt auf.

**Quelle:** CGR-2026-04-skillsystem-r6 Kapitel 4, ClickUp-Task `86c9gmkd5`

---

## Projekt-Kontext und Fallback

Das Skill-System ist projekt-agnostisch gebaut — projekt-spezifische Daten liegen in `projects/<projekt>/`. Claude ermittelt das aktive Projekt aus dem Memory-Eintrag `[PROJECT] <n> | ...`.

| Situation | Verhalten |
|---|---|
| `[PROJECT]`-Memory vorhanden | Claude liest aus `projects/<n>/`, arbeitet projekt-kontextualisiert |
| `[PROJECT]`-Memory fehlt | Claude listet `projects/`-Ordner und fragt per `ask_user_input_v0`, schlägt Memory-Eintrag vor |
| `projects/<n>/<datei>.md` fehlt | Universell-Modus: Claude fragt benötigte Daten ad-hoc vom User ab |
| `projects/`-Ordner leer | Vollständiger Universell-Modus mit Hinweis aufs Anlegen |

Für BPM: siehe `projects/bpm/` mit ClickUp-Listen-IDs, Custom-Field-IDs, Modul-Kürzeln und Memory-Eintragsformaten.

---

## Abgrenzung zu öffentlichen Skill-Repos

Diese Skills sind **projektspezifisch** — sie kennen:

- BPM-Docs (INDEX.md, Architektur, DB-SCHEMA, CODING_STANDARDS, DSVGO-Architektur, etc.)
- ClickUp-IDs (Space/Listen/10 Custom Fields)
- BPM-Workflow-Regeln (Commit-Format `[vX.Y.Z] Modul, Typ: Kurztitel`, Ein-Task-Ein-Commit)
- Herberts 3-PC-Setup
- CGR-System-Archivierung im BPM-Repo

Für **generische** Skills siehe öffentliche Repos:

- [obra/superpowers](https://github.com/obra/superpowers) — Workflow-Skills
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) — 235+ Engineering-/Marketing-Skills
- [anthropic/skill-creator](https://docs.claude.com/) — Anthropic-Referenz (eingebettet in `reference/anthropic-skill-creator/`)
