# Eval: git-commit-helper

## Skill-Description (aktuell)

```yaml
description: >
  Erstellt fertige Git-Commit-Befehle und Commit-Messages im BPM-Format
  [vX.Y.Z] Modul, Typ: Kurztitel. Use when users want to commit changes,
  need a git commit command, ask for a commit message, or want the correct
  version bump for an existing change. Do not trigger for code creation,
  code review, git push, or general Zustimmung wie "ok" oder "passt".
```

Stand: `a5b17bb` — 2026-04-21 (Phase 1.1)

---

## Query-Katalog

### should_trigger

| # | Query | Typ | Notiz |
|---|-------|-----|-------|
| 1 | `commit bitte` | [golden] | Teil 5 — funktionierte direkt |
| 2 | `commit befehl` | [golden] | Teil 5 — funktionierte direkt |
| 3 | `mach mir einen commit` | [golden] | Standard-Trigger |
| 4 | `commit` | [golden] | kürzeste Form, Teil 10 |
| 5 | `git commit für die änderung` | [synthetic] | Variante mit Präzisierung |
| 6 | `commit-message für das bitte` | [synthetic] | explizites Artefakt |
| 7 | `wie lautet der commit-text?` | [synthetic] | Frage-Form, immer noch Intent |
| 8 | `version bump für den fix?` | [synthetic] | "version bump for existing change" aus Description |
| 9 | `PATCH oder MINOR für dieses feature?` | [synthetic] | Semver-Entscheidung |
### should_not_trigger

| # | Query | Typ | Notiz |
|---|-------|-----|-------|
| 1 | `ok` | [golden] | Teil 22 — war unerwünschter Trigger, Phase 1.1 Fix |
| 2 | `passt` | [golden] | Teil 22 — war unerwünschter Trigger, Phase 1.1 Fix |
| 3 | `ja passt so` | [synthetic] | Zustimmung, kein Action |
| 4 | `alles klar` | [synthetic] | Zustimmung |
| 5 | `danke` | [synthetic] | Smalltalk |

### other_skill

| # | Query | Typ | Erwarteter Skill | Notiz |
|---|-------|-----|------------------|-------|
| 1 | `push das` | [synthetic] | — (kein Skill) | git push ist explizit Herbert-Aktion, kein Skill |
| 2 | `erstelle die CommitService.cs` | [synthetic] | `code-erstellen` | Code-Erstellung, nicht Commit |
| 3 | `review den letzten commit` | [synthetic] | — (kein Skill) | Code-Review ohne Action, Description schließt es aus |

### ambiguous

| # | Query | Typ | Interpretation A | Interpretation B | Notiz |
|---|-------|-----|------------------|------------------|-------|
| 1 | `git status` | [golden] | triggert (Commit-Absicht vorher besprochen) | triggert nicht (reine Status-Abfrage) | Teil 5 — User sagte vorher "commit", dann git status → damals triggerte Skill |
| 2 | `was muss ich noch committen?` | [synthetic] | triggert (Commit-Intent erkennbar) | triggert nicht (Frage, keine Action) | Grenzfall zwischen Frage und Auftrag |

---

## Run-Log

### baseline

- date: 2026-04-21
- tester: Claude Opus 4.7 (Blind-Modus — nur Name + Description)
- should_trigger: 8/9
- should_not_trigger: 5/5
- other_skill: 3/3
- ambiguous: _dokumentiert_
- notes:
  - Query 9 `PATCH oder MINOR für dieses feature?`: Semver-Entscheidungsfrage triggerte nicht zuverlässig. Description nennt "version bump for existing change", aber "PATCH/MINOR" ohne "version bump" ist für einen blinden Router schwer zuzuordnen. Phase-2-Hinweis: Description um Semver-Keywords erweitern.
  - Ausschluss-Block greift sauber bei `ok` / `passt` / `push das` / `erstelle die CommitService.cs` / `review den letzten commit`.

### after-refactor

- date: _(wird in Phase 5.8 gefüllt)_
- ...
