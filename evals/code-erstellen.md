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

- date: 2026-04-24
- tester: Claude Opus 4.7 (Selbst-Simulation, kein echter API-Blind-Run)
- methode: Zwei Durchläufe — Blind-Modus (nur Name + Description) und Vollmodus (inkl. Body-Delegations-Tabelle aus Phase 5.1/5.2/5.3/5.4/5.5)
- commit-range: baseline `4028411` → after `4f750a3` (Phase 5.1-5.5 betreffen code-erstellen)
- confidence: mittel — Selbst-Simulation, methodische Grenze offen dokumentiert (siehe notes)

#### Blind-Modus (Description-only)

- should_trigger: 9/10
- should_not_trigger: 3/3
- other_skill: 6/6
- ambiguous: _dokumentiert_
- delta vs baseline: ±0 — Description in Phase 5 NICHT geändert

#### Vollmodus (Description + Body-Delegation)

- should_trigger: 10/10 (+1 ggü. Blind/Baseline — Query 5 `neue View für ProfileWizard` triggert jetzt klarer als Code. Die Delegations-Tabelle zu mockup-erstellen präzisiert: "UI-Entwurf als **HTML-Mockup**" → mockup-erstellen. Damit ist implizit klar dass XAML-Views in code-erstellen gehören.)
- should_not_trigger: 3/3
- other_skill: 6/6 (Konfidenz deutlich erhöht — die Delegations-Tabelle im Body benennt alle 5 Paar-Konflikte explizit)
- ambiguous: _dokumentiert_ — Query 3 `schreib den Code dafür` nach Mockup-Abnahme wird im Vollmodus klarer zu code-erstellen geroutet durch Delegations-Tabelle
- delta vs baseline: +1 bei should_trigger (9/10 → 10/10) im Vollmodus, Konfidenz bei other_skill deutlich höher

#### notes

- Größter qualitativer Gewinn von Phase 5: code-erstellen ist der Catch-all und hat 5 Paar-Delegations (5.1/5.2/5.3/5.4/5.5). Die Tabelle im Body listet alle Nachbarn mit klarer Grenze.
- Query 5 `neue View für ProfileWizard` war Baseline-Grenzfall ("View" mehrdeutig). Durch die Schärfung des Begriffs "HTML-Mockup" in mockup-erstellen Kapitel 5.1 ist XAML-View jetzt klar code-erstellen. Das ist ein messbarer Vollmodus-Gewinn.
- Ambiguous-Queries 1+2 (`mach es fertig`, `kannst du das noch einbauen?`) bleiben kontext-abhängig. Das ist korrekt und gewollt — solche Formulierungen sollen per ask_user_input_v0 geklärt werden.
- Methodische Einschränkung wie bei git-commit-helper (siehe dort).
- verbleibende ❌: keine
- verbleibende ⚠️: ambiguous 1+2 bleiben Grenzfälle (kontextabhängig, per Design)
