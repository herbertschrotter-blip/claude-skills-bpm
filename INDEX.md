# INDEX — Skill-Übersicht

Routing-Matrix für die 10 Skills im claude-skills-bpm Projekt.

## Skills in alphabetischer Reihenfolge

| Skill | Zweck | Haupt-Trigger |
|-------|-------|---------------|
| **audit** | Konsistenz zwischen Code und Docs prüfen | "audit", "prüfe alles", "konsistenzcheck" |
| **cc-steuerung** | Desktop Commander (DC) MCP-Server steuern | "cc mach", "dc lies", "claude code soll" |
| **chat-wechsel** | Übergabe-Prompt für nächsten Chat erstellen | "neuer chat", "übergabe", "chat wechsel" |
| **chatgpt-review** | Cross-Review-Prompts für ChatGPT bauen | "besprich mit ChatGPT", "frag ChatGPT", "zweite Meinung" |
| **code-erstellen** | Orchestrator für Code-Erstellung (Master-Skill) | Jede Anfrage die Code-Erstellung impliziert |
| **doc-pflege** | Dokumentations-Updates pflegen | "pflege docs", "schreib ADR", "neues Konzept" |
| **git-commit-helper** | Commit-Format generieren | "commit", "git commit", "mach den commit" |
| **mockup-erstellen** | HTML-UI-Mockups für BPM-Screens erstellen | "Mockup für", "Screen-Design", "UI-Mockup" |
| **skill-pflege** | Skills additiv ändern (Meta-Skill) | "Skill updaten", "Skill ändern", "Skill erweitern" |
| **tracker** | ClickUp-Schreibschnittstelle | "tracker neu", "tracker done", "was ist offen" |

## Skill-Hierarchie

### Master-Orchestrator
- **code-erstellen** ← Ruft andere Skills auf bei Code-Tasks

### Meta-Skills (ändern andere Dinge)
- **skill-pflege** ← Ändert bestehende Skills
- **doc-pflege** ← Ändert Docs

### Workflow-Skills
- **chat-wechsel** ← Chat-Ende
- **chatgpt-review** ← Cross-Review
- **audit** ← Konsistenz-Prüfung

### Tool-Wrapper
- **tracker** ← ClickUp
- **git-commit-helper** ← Git
- **cc-steuerung** ← DC/MCP
- **mockup-erstellen** ← UI-Mockups

## Gemeinsame Regeln in allen Skills

Alle Skills folgen diesen Invarianten (konsistent über alle 10 Skills):

1. **`ask_user_input_v0` bei Entscheidungen** — KEINE Prosa-Fragen bei festen Optionen
2. **Branch-Ermittlung** — Nie automatisch annehmen, immer per ask_user_input_v0 wählen lassen
3. **DC-Pfade** — Nie hardcoden, immer per Pfad-Ermittlung aus INDEX.md
4. **Frühphasen-Prinzip** — Keine Migrations-Logik ohne explizite User-Freigabe (siehe BPM INDEX.md Kapitel "Projekt-Phase")
5. **Additive Änderungen** — Bestehende Skill-Inhalte werden nicht gelöscht (siehe skill-pflege)

## Abgrenzung zu öffentlichen Skill-Repos

Diese Skills sind **projektspezifisch** — sie kennen:
- BPM-Docs (INDEX.md, Architektur, DB-SCHEMA, CODING_STANDARDS, etc.)
- ClickUp-IDs (Space/Listen/Custom Fields)
- BPM-Workflow-Regeln (Commit-Format `[vX.Y.Z] Modul, Typ: Kurztitel`)
- Herberts 3-PC-Setup (Desktop-PC / Firmenlaptop / Surface7)

Für **generische** Skills (z.B. TDD, Debugging, Refactoring) empfehlen sich Community-Repos wie:
- [obra/superpowers](https://github.com/obra/superpowers) — Workflow-Skills
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) — 235+ Engineering-/Marketing-Skills
