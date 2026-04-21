# Eval: code-erstellen

## Skill-Description (aktuell)

```yaml
description: >
  Plant und erzeugt BPM-Codeänderungen auf Basis von INDEX.md, Quickloads und
  fachlichen Invarianten. Use when users want to implement or change application
  code, add a method, service, dialog, data flow, validation, or persistence
  logic. Do not trigger for mockups, git commits, explicit documentation work,
  ClickUp task management, or pure consistency audits.
```

Stand: `4028411` — 2026-04-21 (Phase 1.4)

---

## Query-Katalog

### should_trigger

| # | Query | Typ | Notiz |
|---|-------|-----|-------|
| 1 | `implementiere das Feature` | [golden] | Teil 9 — Standard-Trigger |
| 2 | `erstelle die DocumentTypeRecognizer.cs` | [golden] | explizit Code-Datei |
| 3 | `bau die Recovery-Logik ein` | [golden] | Standard-Trigger |
| 4 | `neuer Service für PatternTemplates` | [golden] | Teil 11 — Service-Anlage |
| 5 | `neue View für ProfileWizard` | [golden] | Teil 11 — View-Anlage |
| 6 | `füg eine Methode GetPendingImports() hinzu` | [golden] | Teil 22 BPM-016 — Methode hinzufügen |
| 7 | `fix den Parser bei 5998er Statikplänen` | [synthetic] | Fix-Trigger |
| 8 | `refactore den Dialog in 2-Spalten-Layout` | [synthetic] | Refactor-Trigger |
| 9 | `baue die Validierung für Pflichtfelder` | [synthetic] | Validierung aus Description |
| 10 | `persistenz-logik für profiles.json` | [synthetic] | persistence aus Description |

### should_not_trigger

| # | Query | Typ | Notiz |
|---|-------|-----|-------|
| 1 | `was hältst du von dem Konzept?` | [synthetic] | reine Konzept-Diskussion ohne Code-Intent |
| 2 | `erklär mir wie Commands in MVVM funktionieren` | [synthetic] | Erklärungsfrage, kein Code-Auftrag |
| 3 | `ist das Design gut?` | [synthetic] | Review-Frage ohne Action |

### other_skill

| # | Query | Typ | Erwarteter Skill | Notiz |
|---|-------|-----|------------------|-------|
| 1 | `erstelle ein Mockup für den ProfileWizard` | [golden] | `mockup-erstellen` | Phase 1.4 Konflikt — „erstelle" ist nicht mehr Alleinstellungsmerkmal |
| 2 | `commit bitte` | [golden] | `git-commit-helper` | Phase 1.4 Konflikt — Description-Ausschluss aktiv |
| 3 | `schreib ein ADR für die Entscheidung` | [golden] | `doc-pflege` | Phase 1.4 Konflikt — documentation work |
| 4 | `tracker neu: PM — 5998er Bug` | [golden] | `tracker` | Phase 1.4 Konflikt — ClickUp task management |
| 5 | `prüfe die Doku auf Widersprüche` | [golden] | `audit` | Phase 1.4 Konflikt — pure consistency audits |
| 6 | `neuer chat` | [golden] | `chat-wechsel` | Session-Ende ≠ Code |

### ambiguous

| # | Query | Typ | Interpretation A | Interpretation B | Notiz |
|---|-------|-----|------------------|------------------|-------|
| 1 | `mach es fertig` nach Konzeptdiskussion | [synthetic] | triggert (Code-Umsetzung nach Plan) | triggert nicht (zu vage, kein Code-Keyword) | hängt stark vom Chat-Kontext ab |
| 2 | `kannst du das noch einbauen?` | [synthetic] | triggert (Änderungswunsch → Code) | triggert nicht (zu unspezifisch) | typische Grenzformulierung aus echten Chats |
| 3 | `schreib den Code dafür` nach Mockup-Abnahme | [synthetic] | triggert (Code nach Design-Konsens) | triggert nicht (Interaktion mit `mockup-erstellen`) | Paar-Konflikt mit mockup-erstellen (Phase 5.1) |

---

## Run-Log

### baseline

- date: 2026-04-21
- tester: Claude Opus 4.7 (Blind-Modus — nur Name + Description)
- should_trigger: 9/10
- should_not_trigger: 3/3
- other_skill: 6/6
- ambiguous: _dokumentiert_
- notes:
  - Query 5 `neue View für ProfileWizard`: Konflikt zwischen "dialog" (triggert) und "mockups" (ausgeschlossen). "View" ist in WPF eine UI-Datei; für einen blinden Router mehrdeutig (Code-View vs Mockup-View). Description sollte Phase-2 klarstellen: "Code-Views (.xaml + .xaml.cs) triggern, reine HTML/SVG-Mockups triggern nicht".
  - Ausschluss-Block ist sehr stark — 6/6 other_skill-Queries werden korrekt abgewiesen. Phase 1.4 Description-Fix hat den erwarteten Effekt.
  - should_not_trigger (Konzept-/Erklärungsfragen) sauber abgewiesen.

### after-refactor

- date: _(wird in Phase 5.8 gefüllt)_
- ...
