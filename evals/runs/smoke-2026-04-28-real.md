# Smoke Run — 2026-04-28 (real)

- **model:** Claude (claude.ai Web)
- **tester:** Herbert
- **mode:** real Claude.ai (Memory aus, Skills aktiv)
- **repo ref:** main @ <sha-am-Run-Tag-eintragen>
- **Quelle:** `evals/smoke-all-skills.md` Top-30 (P1.2)
- **Methodik:** ein neuer Chat pro Case, Skills + erste Aktion dokumentiert

## Summary

| Skill | PASS | WARN | FAIL | Quote |
|---|---:|---:|---:|---:|
| cc-steuerung (Multi) | 6 | 0 | 0 | 100% |
| audit | 4 | 0 | 0 | 100% |
| tracker | 2 | 0 | 0 | 100% |
| mockup-erstellen | 2 | 0 | 0 | 100% |
| git-commit-helper | 0 | 1 | 0 | (1× WARN) |
| chat-wechsel | 0 | 1 | 0 | (1× WARN — Test-Setup-Bias) |
| doc-pflege | 3 | 0 | 2 | 60% |
| skill-pflege | 1 | 0 | 1 | 50% |
| code-erstellen | 2 | 0 | 5 | 29% |
| **Total (30)** | **20** | **2** | **8** | **PASS 67% / WARN 7% / FAIL 27%** |

## Cases

### Block 1 — cc-steuerung Multi-Trigger (6/6 PASS)

| ID | Query | Skills (ERW) | Skills (TAT) | Aktion (TAT) | Status | Notiz |
|---|---|---|---|---|---|---|
| CC-06 | `cc bau die neue View für ProfileWizard` | cc + code | cc + code | DC-Check via tool_search → DC fehlt → fragt nach Projekt + Variante | PASS | Multi-Trigger korrekt; WAS/WIE-Trennung sauber |
| CC-07 | `dc commit bitte` | cc + git-commit | cc + git-commit | beide Skills gelesen → DC-Check → fragt Repo + Typ + Modul + Version | PASS | Multi-Trigger explizit benannt |
| CC-08 | `cc Mockup für ImportPreviewDialog speichern` | cc + mockup | cc + mockup | beide Skills geladen → conversation_search 2× → fragt: Mockup neu oder existierend? | PASS | Multi-Trigger explizit; intelligente Suche |
| CC-09 | `cc tracker neu: PM — Regex Bug` | cc + tracker | cc + tracker (+ DC + ClickUp) | Multi-Trigger benannt → DC + tracker-Dedup → BPM-007/082-Konflikt → ask_user_input_v0 | PASS | Vorzeige-Antwort: Multi-Trigger, Dedup, Anker, Fragemodus |
| CC-10 | `cc pflege das ADR über Datenschutz` | cc + doc-pflege | cc + doc-pflege (+ DC) | beide Skills gelesen → DC + INDEX → Mehrdeutigkeit erkannt → fragt präzise | PASS | Vorbildliche Ambiguitätserkennung |
| CC-11 | `cc audit über alle Skills` | cc + audit | cc + audit | beide gelesen → Scope-Mismatch erkannt (audit für BPM, nicht Skill-Repo) → fragt | PASS | Skill-Description-Awareness; Scope-Mismatch für P3.2 relevant |

### Block 2 — code-erstellen Konflikte (3/5 PASS, 2 FAIL)

| ID | Query | Skills (ERW) | Skills (TAT) | Aktion (TAT) | Status | Notiz |
|---|---|---|---|---|---|---|
| CE-02 | `neue View für ProfileWizard` | code-erstellen | — (kein Skill) | generische Nachfrage | **FAIL** | P0.4-Härtung greift NICHT bei isolierter View-Query |
| CE-05 | `erstelle ein Mockup für den ProfileWizard` | mockup-erstellen | mockup-erstellen | mockup geladen, kein code-Verwirrung → fragt Schritte/Felder | PASS | "Mockup" als Substantiv-Trigger reicht |
| CE-06 | `commit bitte` | git-commit | git-commit + cc-steuerung | beide gelesen → DC-Check → fragt nach Projekt + Änderungen | **WARN** | cc-steuerung triggert ohne expliziten cc/dc; Cross-Skill-Dependency oder Description zu breit |
| CE-07 | `schreib ein ADR für die Entscheidung` | doc-pflege | — (kein Skill) | generische Nachfrage ohne DOC-STANDARD-Bezug | **FAIL** | doc-pflege Verb-Erkennung schwach bei "schreib" |
| CE-08 | `prüfe die Doku auf Widersprüche` | audit | audit | audit geladen → Sandbox-Awareness → fragt DC/Snippets | PASS | Audit triggert ohne Konfliktablenkung |

### Block 3 — mockup-erstellen Konflikte (2/4 PASS, 2 FAIL)

| ID | Query | Skills (ERW) | Skills (TAT) | Aktion (TAT) | Status | Notiz |
|---|---|---|---|---|---|---|
| MU-06 | `neue XAML View für ProfileWizard` | code-erstellen | code-erstellen | code-erstellen geladen → fragt Mockup-vs-Implementierung → Plan-Phase | PASS | "XAML" rettet Trigger gegenüber CE-02 |
| MU-07 | `kleiner UI-Fix im bestehenden Dialog` | code-erstellen | — (kein Skill) | generische Nachfrage | **FAIL** | "UI-Fix" / "Dialog" ohne starkes Verb fällt durch |
| MU-08 | `HTML-Mockup danach bitte implementieren` | mockup + code (ask) | — (kein Skill) | generische Nachfrage, weder mockup-Konvention noch code-Plan-Phase | **FAIL** | Multi-Intent ohne Subjekt zieht keinen Skill |
| MU-09 | `Architektur für ImportPreviewDialog` | doc-pflege | — (kein Skill) | generische Nachfrage, "klingt nach Implementierung" | **FAIL** | "Architektur" mehrdeutig; weder doc-pflege noch code triggert |

### Block 4 — doc-pflege Konflikte (3/4 PASS, 1 FAIL)

| ID | Query | Skills (ERW) | Skills (TAT) | Aktion (TAT) | Status | Notiz |
|---|---|---|---|---|---|---|
| DOC-06 | `implementiere die neue Recovery-Logik` | code-erstellen | — (kein Skill) | generische Nachfrage, sucht Kontext in alten Chats | **FAIL** | code-erstellen triggert NICHT bei "implementiere" + generischem Substantiv |
| DOC-07 | `prüfe alle Frontmatter und Quickloads` | audit | audit | audit geladen → Modul 6 erkannt → Teilaudit identifiziert → fragt DC/ZIP | PASS | Saubere Skill-Anwendung |
| DOC-08 | `repariere fehlende Quickloads in Konzept-Docs` | doc-pflege | doc-pflege | doc-pflege geladen, kein audit-Falsch-Trigger → "Modus 6" erkannt | PASS | doc-pflege triggert bei BPM-Domain-Begriffen |
| DOC-09 | `Mockup für die neue ADR-Übersicht` | mockup-erstellen | mockup-erstellen | mockup geladen, kein doc-pflege-Falsch-Trigger → Visualizer-Preview-Workflow | PASS | "Mockup" als Subjekt schlägt "ADR" zuverlässig |

### Block 5 — audit Konflikte (3/4 PASS, 1 FAIL)

| ID | Query | Skills (ERW) | Skills (TAT) | Aktion (TAT) | Status | Notiz |
|---|---|---|---|---|---|---|
| AUD-06 | `pflege die Architektur-Doku` | doc-pflege | doc-pflege | doc-pflege geladen, kein audit-Falsch-Trigger → Modus 5 erkannt → 3 Wege | PASS | "pflege" Verb-Anker zuverlässig |
| AUD-07 | `fix die Inkonsistenz im DB-Schema` | code-erstellen | — (kein Skill) | minimale generische Nachfrage | **FAIL** | weder code noch audit triggert; "fix" + "Inkonsistenz" ohne BPM-Domain |
| AUD-08 | `prüfe alle Frontmatter und repariere fehlende Quickloads` | doc-pflege | audit + doc-pflege | beide geladen, bewusste Aufteilung "audit für Prüfung, doc-pflege für Reparaturen" | PASS | Multi-Intent korrekt aufgeteilt; Katalog-Erwartung war zu eng |
| AUD-09 | `tracker suche Konsistenz` | tracker | tracker | tracker geladen → clickup_search → 7 Treffer formatiert | PASS | Beste tracker-Demonstration: Trigger + Ausführung |

### Block 6 — git-commit-helper SNT (2/3 PASS, 1 FAIL)

| ID | Query | Skills (ERW) | Skills (TAT) | Aktion (TAT) | Status | Notiz |
|---|---|---|---|---|---|---|
| GCH-03 | `ok` | — | — (kein Skill) | freundliche Begrüßung, fragt nach Auftrag | PASS | Phase-1.1-Fix bestätigt |
| GCH-04 | `erstelle die CommitService.cs` | code-erstellen | — (kein Skill) | nur ask_user_input_v0 ohne Skill-Workflow | **FAIL** | KRITISCH: stärkstes Code-Wording (Imperativ + .cs) triggert nicht |
| GCH-06 | `review den letzten commit` | — | — (kein Skill) | bietet Review an → DC-Check → fragt nach Repo/Pfad/Branch | PASS | weder git-commit noch chatgpt-review feht falsch |

### Block 7 — chatgpt-review Konflikte (1 PASS, 1 WARN)

| ID | Query | Skills (ERW) | Skills (TAT) | Aktion (TAT) | Status | Notiz |
|---|---|---|---|---|---|---|
| CGR-04 | `neuer chat` | chat-wechsel | — (kein Skill) | freundliche Begrüßung in leerer Session | **WARN** | Test-Setup-Bias: leere Session kann chat-wechsel nicht testen — Skill funktioniert real (golden case) |
| CGR-06 | `mach mir einen prompt für GPT zu einem anderen Thema` | — | — (kein Skill) | fragt nach Thema (Tennis) → liefert generischen Tennis-Prompt | PASS | chatgpt-review sauber abgegrenzt |

### Block 8 — skill-neu vs skill-pflege (1 PASS, 1 FAIL)

| ID | Query | Skills (ERW) | Skills (TAT) | Aktion (TAT) | Status | Notiz |
|---|---|---|---|---|---|---|
| SN-06 | `pflege den tracker-Skill um eine Regel` | skill-pflege | skill-pflege | skill-pflege geladen, tracker vor-gelesen → fragt Wortlaut + Stelle → Diff + Artifact | PASS | "pflege" Verb-Anker; saubere Trennung zu skill-neu |
| SN-07 | `ergänze beim chat-wechsel die Memory-Auflistung` | skill-pflege | — (nur chat-wechsel Ziel-Skill, kein skill-pflege Workflow) | chat-wechsel direkt gelesen, fragt 3 Varianten — kein Diff, kein Artifact | **FAIL** | "ergänze" triggert skill-pflege NICHT; Workflow fehlt |

## Failures

| Case | Expected | Actual | Diagnosis | Action |
|---|---|---|---|---|
| CE-02 | code-erstellen | — | "neue View für X" — Substantiv allein ohne Verb | Description: Substantiv-Trigger ergänzen ODER Verb nachschärfen |
| CE-07 | doc-pflege | — | "schreib ein ADR" — generisches Verb + Substantiv | Description: Trigger-Verben erweitern (schreib, draften, anlegen) |
| MU-07 | code-erstellen | — | "UI-Fix Dialog" — beschreibend ohne Verb / XAML | Description: Bug-Fix-Vokabular und Dialog-Substantive |
| MU-08 | mockup + code (ask) | — | Multi-Intent ohne Subjekt | Description: Mockup-Trigger ohne Subjekt prüfen ODER ask-Pattern erzwingen |
| MU-09 | doc-pflege | — | "Architektur für X" — mehrdeutig | "Architektur" als Trigger pflegen ODER bewusst raus |
| DOC-06 | code-erstellen | — | "implementiere Recovery-Logik" — generisches Substantiv | code-erstellen kritisch: selbst klassischer Imperativ greift nicht |
| AUD-07 | code-erstellen | — | "fix Inkonsistenz im DB-Schema" — generisch, fällt durch | code-erstellen kritisch (gleiches Muster wie DOC-06) |
| **GCH-04** | **code-erstellen** | **—** | **🔴 KRITISCH: stärkstes Code-Wording (Imperativ + .cs-Datei) triggert nicht** | **code-erstellen Description-Refactor priorisieren** |
| SN-07 | skill-pflege | — | "ergänze" als alternatives Pflege-Verb | skill-pflege Description: Verben erweitern (ergänze, füg-hinzu, einbauen) |

## Methodik-Befunde

1. **Test-Setup-Bias bei chat-wechsel:** Smoke-Test in leerer Session kann den Skill nicht realistisch testen. Künftige Runs brauchen 3-5 Vor-Nachrichten.
2. **Selbst-Sim-Bias bestätigt:** Vorhersage aus Teil 33 hatte 27% Bias (4 falsch-positive PASS-Vorhersagen für CE-02, CE-07, DOC-06, SN-07).
3. **Skill-Loading-Indikator nicht 100% verlässlich:** Bei SN-07 wurde nur Ziel-Skill, nicht Workflow-Skill als geladen angezeigt.

## Hauptbefunde

1. **🔴 `code-erstellen` strukturell schwach** (29% PASS): triggert nur bei "XAML"-Substantiv oder cc/dc-Modalität. Generische Code-Verben + generische Software-Substantive triggern nicht.
2. **🟡 Pflege-Skills triggern nur auf "pflege"** als Verb. Alternative Verben ("schreib", "ergänze") fallen durch. Betrifft `doc-pflege` und `skill-pflege`.
3. **✅ Multi-Trigger funktioniert hervorragend** (cc + Fachskill 6/6 PASS). Invariante 9 in der Praxis bestätigt.
4. **✅ Negative Diskriminierung funktioniert** (should-not-trigger-Cases korrekt abgewiesen). Skills sind nicht "übergriffig".
5. **⚠️ Description-Schärfe** ist der Haupthebel — nicht Skill-Architektur. Die "starken" Skills (audit, tracker, mockup, cc-steuerung) haben präzise Trigger; die "schwachen" haben zu enge Verb/Substantiv-Inventare.

## Empfehlungen für P1.3

1. **Priorität 1 (kritisch):** `code-erstellen` Description-Refactor mit Trigger-Inventar (Verben + Substantive + Endungen)
2. **Priorität 2:** `doc-pflege` und `skill-pflege` Verb-Inventar erweitern
3. **Priorität 3:** Mehrdeutigkeits-Disambiguation für "Architektur" (MU-09) und Multi-Intent (MU-08)
4. **Methodik:** chat-wechsel-Tests künftig mit Vor-Konversation; Selbst-Sim-Vorhersagen mit Vorsicht behandeln
