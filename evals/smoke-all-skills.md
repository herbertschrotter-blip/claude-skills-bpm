# Smoke Eval — All Skills

## Zweck

Eine Smoke-Eval für **alle 11 Skills** als Sicherheitsnetz vor Freigabe der BPM-Feature-Arbeit. Die Eval misst, ob jeder Skill bei den richtigen Queries triggert und bei den falschen nicht — inkl. Konfliktpaare und Multi-Trigger-Fälle für `cc-steuerung`.

Quelle: `Docs/Referenz/chatgpt-reviews/CGR-2026-04-skillsystem/r6/02-chatgpt-response.md` Kapitel 3.

## Scope

- 11 Skills × 6-11 Cases = ~85 Cases
- Blind-Modus (nur Name + Description) — primär
- Vollmodus (Description + Body) — sekundär, optional

## Scoring

| Status | Bedeutung |
|---|---|
| **PASS** | Erwartete Skillmenge exakt oder akzeptierte Teilmenge |
| **WARN** | Fachlich korrekt, aber Modalität (cc-steuerung) unklar sichtbar |
| **FAIL** | Falscher Primärskill oder unerlaubter Skill |

## Run-Snapshots

Einzelne Run-Ergebnisse werden NICHT in dieser Datei gespeichert, sondern als separate Snapshots unter `evals/runs/smoke-YYYY-MM-DD.md`. Diese Datei ist der **stabile Testkatalog**.

Format eines Snapshots:

```markdown
# Smoke Run — YYYY-MM-DD

- model:
- tester:
- mode: real Claude.ai / self-sim / API
- repo ref: main @ <sha>

## Summary
| Skill | PASS | WARN | FAIL |
|---|---:|---:|---:|

## Failures
| Case | Expected | Actual | Diagnosis | Action |
```

## Markierungen

- `[golden]` — echte Formulierung aus dem BPM-Chat-Verlauf
- `[synthetic]` — gezielt konstruierte Variante zur Randtest-Abdeckung

---

## git-commit-helper

Quelle: `evals/git-commit-helper.md` (bereits baseliniert in Phase 1a).

| ID | Query | Erwartung | Kategorie | Notiz |
|---|---|---|---|---|
| GCH-01 | `commit bitte` | git-commit-helper | should_trigger | [golden] Standard-Trigger |
| GCH-02 | `PATCH oder MINOR für dieses feature?` | git-commit-helper | should_trigger | [synthetic] Semver — bekannter Schwachpunkt (`[ARCH-OPEN]`) |
| GCH-03 | `ok` | — (kein Skill) | should_not_trigger | [golden] Phase 1.1 Fix — Zustimmung |
| GCH-04 | `erstelle die CommitService.cs` | code-erstellen | conflict-near-miss | [synthetic] Code-Erstellung trotz "commit"-Wort |
| GCH-05 | `push das` | — (kein Skill) | conflict-near-miss | [synthetic] git push ist ausgeschlossen |
| GCH-06 | `review den letzten commit` | — (kein Skill) | conflict-near-miss | [synthetic] Code-Review ohne Action |

---

## chatgpt-review

Quelle: `evals/chatgpt-review.md` (bereits baseliniert in Phase 1a).

| ID | Query | Erwartung | Kategorie | Notiz |
|---|---|---|---|---|
| CGR-01 | `besprich das mit ChatGPT` | chatgpt-review | should_trigger | [golden] Standard-Trigger |
| CGR-02 | `Runde 3 erstellen` | chatgpt-review | should_trigger | [golden] Folgeprompt — bekannter Schwachpunkt (`[ARCH-OPEN]`) |
| CGR-03 | `antworte darauf` | — (kein Skill) | should_not_trigger | [golden] Phase 1.2 Fix |
| CGR-04 | `neuer chat` | chat-wechsel | conflict-near-miss | [golden] Session-Ende ≠ Review |
| CGR-05 | `schreib mir einen commit-message-prompt` | git-commit-helper | conflict-near-miss | [synthetic] Commit ≠ Review |
| CGR-06 | `mach mir einen prompt für GPT zu einem anderen Thema` | — (kein Skill) | conflict-near-miss | [synthetic] generisches Prompt-Engineering |

---

## tracker

Quelle: `evals/tracker.md` (bereits baseliniert in Phase 1a — saubere 9/9 + 7/7 + 3/3).

| ID | Query | Erwartung | Kategorie | Notiz |
|---|---|---|---|---|
| TRK-01 | `tracker neu: PM — neue Regex-Erkennung` | tracker | should_trigger | [golden] Standard-Workflow |
| TRK-02 | `tracker done BPM-007` | tracker | should_trigger | [golden] done-Kommando |
| TRK-03 | `was ist offen?` | — (kein Skill) | should_not_trigger | [golden] Phase 1.3 Fix — allgemeine Phrase |
| TRK-04 | `implementiere die Regex-Erkennung` | code-erstellen | conflict-near-miss | [synthetic] Code-Aktion trotz Task-Bezug |
| TRK-05 | `merk dir das` | — (kein Skill, → Memory) | conflict-near-miss | [golden] Memory ≠ ClickUp |
| TRK-06 | `nicht vergessen: Feature Y` | tracker (mit ask_user_input_v0) | conflict-near-miss | [synthetic] unklar Task/Notiz — Skill muss nachfragen |

---

## code-erstellen

Quelle: `evals/code-erstellen.md` + Description-Update aus P0.4 (v0.19.1).

| ID | Query | Erwartung | Kategorie | Notiz |
|---|---|---|---|---|
| CE-01 | `implementiere das Feature` | code-erstellen | should_trigger | [golden] Standard-Trigger |
| CE-02 | `neue View für ProfileWizard` | code-erstellen | should_trigger | [golden] WPF/XAML View — durch P0.4 Description-Update gehärtet |
| CE-03 | `bau die Recovery-Logik ein` | code-erstellen | should_trigger | [golden] Standard-Trigger |
| CE-04 | `was hältst du von dem Konzept?` | — (kein Skill) | should_not_trigger | [synthetic] reine Konzept-Diskussion |
| CE-05 | `erstelle ein Mockup für den ProfileWizard` | mockup-erstellen | conflict-near-miss | [golden] Phase 1.4 Konflikt — "erstelle" ≠ Alleinstellungsmerkmal |
| CE-06 | `commit bitte` | git-commit-helper | conflict-near-miss | [golden] Commit ≠ Code |
| CE-07 | `schreib ein ADR für die Entscheidung` | doc-pflege | conflict-near-miss | [golden] Doc-Arbeit |
| CE-08 | `prüfe die Doku auf Widersprüche` | audit | conflict-near-miss | [golden] read-only audit |

---

## chat-wechsel

Konfliktarm. Schwerpunkt: Chat-Ende-Phrasen vs. Smalltalk.

| ID | Query | Erwartung | Kategorie | Notiz |
|---|---|---|---|---|
| CW-01 | `neuer chat` | chat-wechsel | should_trigger | [golden] Standard-Trigger |
| CW-02 | `nächster Chat bitte` | chat-wechsel | should_trigger | [synthetic] Variante |
| CW-03 | `mach einen Übergabe-Prompt` | chat-wechsel | should_trigger | [synthetic] explizit Handover |
| CW-04 | `gute Nacht` | — (kein Skill) | should_not_trigger | [synthetic] Smalltalk-Verabschiedung |
| CW-05 | `tschüss` | — (kein Skill) | should_not_trigger | [synthetic] Smalltalk |
| CW-06 | `besprich das mit ChatGPT` | chatgpt-review | conflict-near-miss | [golden] Cross-LLM ≠ Chat-Wechsel |
| CW-07 | `tracker neu: PM — neue Idee` | tracker | conflict-near-miss | [synthetic] Task-Aktion ≠ Handover |

---

## skill-neu

Konfliktarm. Schwerpunkt: "neuer Skill von Grund auf" vs. Skill-Änderung.

| ID | Query | Erwartung | Kategorie | Notiz |
|---|---|---|---|---|
| SN-01 | `erstelle einen neuen Skill für X` | skill-neu | should_trigger | [synthetic] Standard-Trigger |
| SN-02 | `wir brauchen einen Skill für Wetter-Sync` | skill-neu | should_trigger | [synthetic] Skill-Bedarfs-Formulierung |
| SN-03 | `entwirf ein neues Skill-System für Y` | skill-neu | should_trigger | [synthetic] System-Design |
| SN-04 | `commit bitte` | git-commit-helper | should_not_trigger | [synthetic] völlig anderer Skill |
| SN-05 | `was sind unsere Skills?` | — (kein Skill) | should_not_trigger | [synthetic] Übersichtsfrage |
| SN-06 | `pflege den tracker-Skill um eine Regel` | skill-pflege | conflict-near-miss | [synthetic] Änderung an bestehendem Skill |
| SN-07 | `ergänze beim chat-wechsel die Memory-Auflistung` | skill-pflege | conflict-near-miss | [synthetic] additive Änderung |

---

## skill-pflege

Konfliktmittel. Schwerpunkt: Skill-Änderung vs. neuer Skill, sowie Skill ≠ Doku.

| ID | Query | Erwartung | Kategorie | Notiz |
|---|---|---|---|---|
| SP-01 | `pflege den tracker-Skill und ergänze split` | skill-pflege | should_trigger | [synthetic] Standard-Trigger |
| SP-02 | `füg im git-commit-helper die VERBOTEN-Liste um X erweitert` | skill-pflege | should_trigger | [synthetic] additive Änderung |
| SP-03 | `aktualisiere die Description von code-erstellen` | skill-pflege | should_trigger | [synthetic] Description-Refactor |
| SP-04 | `was steht im chat-wechsel-Skill?` | — (kein Skill) | should_not_trigger | [synthetic] reine Lese-Frage |
| SP-05 | `ok` | — (kein Skill) | should_not_trigger | [golden] Zustimmung |
| SP-06 | `erstelle einen komplett neuen Skill für Wetter` | skill-neu | conflict-near-miss | [synthetic] neuer Skill ≠ Pflege |
| SP-07 | `schreib ein ADR über die Skill-Architektur` | doc-pflege | conflict-near-miss | [synthetic] Doku ≠ Skill-Pflege |
| SP-08 | `audit über alle Skills` | audit | conflict-near-miss | [synthetic] read-only ≠ Pflege |

---

## audit

Konfliktträchtig. Schwerpunkt: read-only Konsistenzprüfung vs. Doku-Arbeit, Code-Arbeit, Tracker-Suche.

| ID | Query | Erwartung | Kategorie | Notiz |
|---|---|---|---|---|
| AUD-01 | `audit` | audit | should_trigger | [synthetic] kürzeste Form |
| AUD-02 | `prüfe ob INDEX und Skills konsistent sind` | audit | should_trigger | [synthetic] Standard-Trigger |
| AUD-03 | `konsistenzcheck zwischen Code und DOC-STANDARD` | audit | should_trigger | [synthetic] Code-Doc-Vergleich |
| AUD-04 | `was steht in der INDEX.md?` | — (kein Skill) | should_not_trigger | [synthetic] reine Lese-Frage |
| AUD-05 | `liste alle offenen Tasks` | tracker | should_not_trigger | [synthetic] Tracker-Aktion ≠ Audit |
| AUD-06 | `pflege die Architektur-Doku` | doc-pflege | conflict-near-miss | [synthetic] Doku-Schreiben ≠ Audit |
| AUD-07 | `fix die Inkonsistenz im DB-Schema` | code-erstellen | conflict-near-miss | [synthetic] Fix ≠ read-only |
| AUD-08 | `prüfe alle Frontmatter und repariere fehlende Quickloads` | doc-pflege | conflict-near-miss | [synthetic] Reparatur ≠ Audit |
| AUD-09 | `tracker suche Konsistenz` | tracker | conflict-near-miss | [synthetic] Suche in ClickUp ≠ Audit |

---

## mockup-erstellen

Konfliktträchtig. Schwerpunkt: HTML-Mockup vs. WPF/XAML-View — direkter Konflikt mit code-erstellen.

| ID | Query | Erwartung | Kategorie | Notiz |
|---|---|---|---|---|
| MU-01 | `Mockup für ImportPreviewDialog` | mockup-erstellen | should_trigger | [synthetic] Standard-Trigger |
| MU-02 | `HTML-Entwurf für ProfileWizard` | mockup-erstellen | should_trigger | [synthetic] explizit HTML |
| MU-03 | `Screen-Design für Segment-Erkennung` | mockup-erstellen | should_trigger | [synthetic] Design-Wort |
| MU-04 | `was hältst du vom Layout?` | — (kein Skill) | should_not_trigger | [synthetic] Review-Frage ohne Action |
| MU-05 | `commit bitte` | git-commit-helper | should_not_trigger | [synthetic] Commit ≠ Mockup |
| MU-06 | `neue XAML View für ProfileWizard` | code-erstellen | conflict-near-miss | [synthetic] WPF-View ≠ HTML-Mockup (P0.4-Härtung) |
| MU-07 | `kleiner UI-Fix im bestehenden Dialog` | code-erstellen | conflict-near-miss | [synthetic] Fix ≠ neuer Entwurf |
| MU-08 | `HTML-Mockup danach bitte implementieren` | mockup-erstellen + code-erstellen (ask) | conflict-near-miss | [synthetic] Multi-Intent — Skill muss klarstellen |
| MU-09 | `Architektur für ImportPreviewDialog` | doc-pflege | conflict-near-miss | [synthetic] Architektur-Doc ≠ Mockup |

---

## doc-pflege

Konfliktträchtig. Schwerpunkt: Doku-Arbeit vs. Code, ADR vs. Konzept-Diskussion, Frontmatter-Reparatur vs. Audit.

| ID | Query | Erwartung | Kategorie | Notiz |
|---|---|---|---|---|
| DOC-01 | `pflege die Architektur-Doku` | doc-pflege | should_trigger | [synthetic] Standard-Trigger |
| DOC-02 | `schreib ein ADR über die Profilarchitektur` | doc-pflege | should_trigger | [golden] ADR-Schreiben |
| DOC-03 | `neues Konzept für das Wetter-Modul` | doc-pflege | should_trigger | [synthetic] Konzept-Doc |
| DOC-04 | `was hältst du von dem Konzept?` | — (kein Skill) | should_not_trigger | [synthetic] Diskussion ≠ Doku-Schreiben |
| DOC-05 | `erklär mir wie ADRs funktionieren` | — (kein Skill) | should_not_trigger | [synthetic] Erklärungsfrage |
| DOC-06 | `implementiere die neue Recovery-Logik` | code-erstellen | conflict-near-miss | [golden] Code ≠ Doku |
| DOC-07 | `prüfe alle Frontmatter und Quickloads` | audit | conflict-near-miss | [synthetic] read-only ≠ pflegen |
| DOC-08 | `repariere fehlende Quickloads in Konzept-Docs` | doc-pflege | conflict-near-miss | [synthetic] Reparatur = pflegen (NICHT audit) |
| DOC-09 | `Mockup für die neue ADR-Übersicht` | mockup-erstellen | conflict-near-miss | [synthetic] HTML-Mockup ≠ Doc-Schreiben |

---

## cc-steuerung (Modalitäts-Skill)

Konfliktträchtig — Multi-Trigger ist Normalfall. Schwerpunkt: Modalitätsregel aus INDEX.md §9 (Invariante 9 aus P0.2). 6 Multi-Trigger-Cases entsprechen P1.4 (Q5-Q10 aus CGR r6 Kapitel 1).

| ID | Query | Erwartung | Kategorie | Notiz |
|---|---|---|---|---|
| CC-01 | `cc lies INDEX.md` | cc-steuerung | should_trigger (solo) | [synthetic] Q1 — reine cc-Operation |
| CC-02 | `dc list directory von BauProjektManager` | cc-steuerung | should_trigger (solo) | [synthetic] Q2 — DC-Operation explizit |
| CC-03 | `claude code starten und git status zeigen` | cc-steuerung | should_trigger (solo) | [synthetic] Q3 — explizite Modalität |
| CC-04 | `wie geht das mit cc?` | — (kein Skill) | should_not_trigger | [synthetic] Q4 — Erklärungsfrage |
| CC-05 | `cc oder dc?` | — (kein Skill, → ask_user_input_v0) | should_not_trigger | [synthetic] Modus-Frage ohne fachliches WAS |
| CC-06 | `cc bau die neue View für ProfileWizard` | cc-steuerung + code-erstellen | multi-trigger | [synthetic] Q5 — Modalität + Code (WPF/XAML) |
| CC-07 | `dc commit bitte` | cc-steuerung + git-commit-helper | multi-trigger | [synthetic] Q6 — Modalität + Commit |
| CC-08 | `cc Mockup für ImportPreviewDialog speichern` | cc-steuerung + mockup-erstellen | multi-trigger | [synthetic] Q7 — Modalität + Mockup |
| CC-09 | `cc tracker neu: PM — Regex Bug` | cc-steuerung + tracker | multi-trigger | [synthetic] Q8 — Modalität + Tracker |
| CC-10 | `cc pflege das ADR über Datenschutz` | cc-steuerung + doc-pflege | multi-trigger | [synthetic] Q9 — Modalität + Doku |
| CC-11 | `cc audit über alle Skills` | cc-steuerung + audit | multi-trigger | [synthetic] Q10 — Modalität + Audit |

**Multi-Trigger-Erwartung:** WAS bleibt beim Fachskill, WIE liefert cc-steuerung. Nach INDEX §9 Invariante 9 sind beide Skills aktiv. CC ohne fachliches WAS (CC-05) löst `ask_user_input_v0`.

---

## Zusammenfassung

| Skill | Cases | Quelle |
|---|---:|---|
| git-commit-helper | 6 | bestehende Eval (Phase 1a) |
| chatgpt-review | 6 | bestehende Eval (Phase 1a) |
| tracker | 6 | bestehende Eval (Phase 1a) |
| code-erstellen | 8 | bestehende Eval + P0.4 |
| chat-wechsel | 7 | neu für Smoke |
| skill-neu | 7 | neu für Smoke |
| skill-pflege | 8 | neu für Smoke |
| audit | 9 | neu für Smoke |
| mockup-erstellen | 9 | neu für Smoke |
| doc-pflege | 9 | neu für Smoke |
| cc-steuerung | 11 | neu für Smoke (P1.4 inline) |
| **Total** | **86** | |

## Top-30 für manuellen Run (P1.2)

Priorität für die manuelle 30-Cases-Runde (höchste Risiko-Konfliktpaare zuerst):

1. **cc-steuerung Multi-Trigger (CC-06 bis CC-11)** — 6 Cases, deckt INDEX §9 Invariante 9
2. **code-erstellen Konflikte (CE-02, CE-05, CE-06, CE-07, CE-08)** — 5 Cases, P0.4-Härtung + 4 Konfliktpaare
3. **mockup-erstellen Konflikte (MU-06, MU-07, MU-08, MU-09)** — 4 Cases, direkter Konflikt mit code-erstellen
4. **doc-pflege Konflikte (DOC-06, DOC-07, DOC-08, DOC-09)** — 4 Cases, audit/code/mockup-Abgrenzung
5. **audit Konflikte (AUD-06, AUD-07, AUD-08, AUD-09)** — 4 Cases, doc-pflege/code-Abgrenzung
6. **git-commit-helper SNT (GCH-03, GCH-04, GCH-06)** — 3 Cases, Zustimmung/Code/Review-Abgrenzung
7. **chatgpt-review Konflikte (CGR-04, CGR-06)** — 2 Cases, chat-wechsel-Abgrenzung
8. **skill-neu vs skill-pflege (SN-06, SN-07)** — 2 Cases, Konfliktpaar Meta-Skills

Total: 30 Cases.
