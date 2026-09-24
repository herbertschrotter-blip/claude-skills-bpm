# claude-skills-bpm

Skills für Claude (Hauptumgebung Claude Code, dazu der Cowork-Chat) mit ihrer Prüf- und Test-Infrastruktur. Aufbau und
Regeln: `README.md`, `INDEX.md`, `docs/skill-quality.md`, `docs/skill-profile-v1.md`; laufender Umbau:
`docs/skillsystem-umbau.md`. Antworten auf Deutsch.

## Skill-Profil

- Profil-Version: 1
- Projekt-ID: claude-skills-bpm
- Repo: herbertschrotter-blip/claude-skills-bpm
- Branch-Policy: fixed:main

### Checks
- skill-validation: pwsh -NoProfile -File tools/validate-skills.ps1 [skills/**; quality/evals/**; .claude-plugin/**; docs/skill-quality.md; docs/skill-profile-v1.md]
- routing-eval: claude plugin eval . --runs 3 --ablation none --no-publish --trust-plugin [skills/**]

### Commit
- Format: [vX.Y.Z] <Modul>, <Typ>: <Kurztitel>
- Module: <skill>=skills/<skill>/**; skillsystem=docs/**, INDEX.md, README.md, CLAUDE.md, .claude/**; ha-grundsatz=docs/ha-grundsatz/**; Tools=tools/**; Eval=quality/**, .claude-plugin/**
- Versionsquelle: changelog:CHANGELOG.md
- Versionsregel: Skill-Änderung unter skills/** → neue Nummer (Feature → MINOR, sonst PATCH) und CHANGELOG-Eintrag; Commits an Doku, Reviews, Config, Evals und Tools behalten die aktuelle Nummer
- Push-Policy: required-after-commit
- Pre-Commit-Checks: skill-validation
- Doku-Check: Zuständigkeit oder Auslöser eines Skills geändert → INDEX.md; Aufbau des Repos geändert → README.md; Skill geändert → CHANGELOG.md und Lieferung an Herbert für den Upload bei claude.ai

### Code
- Stacks: none
- Pflichtkontext: INDEX.md; docs/skill-quality.md; docs/skill-profile-v1.md; die betroffenen skills/<skill>/SKILL.md
- Aufgabenquelle: Tracker.Config (Liste ClaudeSkills, Skill-Issue-Listen); docs/skillsystem-umbau.md
- Architekturregeln: ref:docs/skill-quality.md#verbindliche-qualitätsregeln
- Tests: skill-validation; routing-eval
- Auslieferung: Upload bei claude.ai durch Herbert (SKILL.md oder Zip mit references/); vorher routing-eval für die betroffenen Fälle
- Mockup-Policy: none
- Befund-Ort: docs/chatgpt-reviews/; Skill-Issues im Tracker

### Doku
- Router: INDEX.md
- Standard: ref:docs/skill-quality.md#dokumentationsregeln
- Pflichtdokumente: INDEX.md; README.md; CHANGELOG.md
- Validierungsregeln: ref:docs/skill-quality.md#skill-prüfung
- Sitzungsabschluss: none
- Entscheidungs-Ort: docs/chatgpt-reviews/

### Tracker
- Provider: clickup
- Config: .claude/skill-config/tracker.md

### Ticket
- Config: none

### Mockup
- Ablage: none
- Designquelle: none
- Ansichten: none
- Abnahme-Ort: none

### Review
- Config: .claude/skill-config/review.md

### Modul
- Manifest: none
- Grundsatzregeln: none

## Review-Profil

Steht in `.claude/skill-config/review.md` (Skill-Profil → Review): Ablage, Themen, Repos, Kontextquelle, Pflicht-Blöcke,
Reviewer-Rollen und Ergebnis-Orte je Thema. Dieser Abschnitt bleibt als Verweis, bis chatgpt-review die Config direkt liest
(Umbau Phase 5/6).
