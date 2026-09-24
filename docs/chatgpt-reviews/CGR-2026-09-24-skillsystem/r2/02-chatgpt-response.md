# Review Runde 2

## Vorab: Maßstab

Ich übernehme deine fünf Schärfungen S2–S6 vollständig, S1 ist nach Git-Prüfung ebenfalls bestätigt. Die beiden Commits `4c498ce` und `3a34d48` tragen tatsächlich beide `[v0.36.0]`; der Fehler liegt damit in der Git-Historie und nicht im aktuellen CHANGELOG.

Auch Herberts geänderte Distributionsentscheidung ist technisch stimmig: Skills, die über claude.ai aktiviert werden, werden in angemeldeten Claude-Code-Sitzungen synchronisiert. Claude Code lädt sie nach `~/.claude/skills/synced/`; Änderungen müssen auf claude.ai erfolgen und lokale Änderungen dort können beim nächsten Sync überschrieben werden. Damit bleibt Two-Place-Pflege notwendig und der künftige `cc-steuerung`-Adapter muss Claude Code ausdrücklich ausschließen. Deine Vorgabe dazu ist damit verbindliche Grundlage dieser Runde.

---

# 1. Abgleich mit Anthropics Leitfaden

Anthropic bestätigt mehrere unserer Kernbefunde ausdrücklich: Description = Discovery-Layer, SKILL.md möglichst unter 500 Zeilen, References direkt vom SKILL.md aus erreichbar, lange References mit Inhaltsverzeichnis, keine zeitabhängigen Regeln und mindestens drei Evals.

Die Skills im Repo enthalten derzeit **keine gebündelten ausführbaren Scripts**; im `skills/`-Tree liegen SKILL.md, References, zwei `test-prompts.md` und `references.zip`. Deshalb ist der Abschnitt „Code and scripts“ der offiziellen Checklist für die zwölf bestehenden Skills derzeit **nicht anwendbar**. Externe Projekt-Scripts wie `deploy.ps1` sind keine gebündelten Skill-Scripts.

Legende: ✅ erfüllt · ⚠️ teilweise/verbesserungsbedürftig · ❌ nicht erfüllt · — nicht anwendbar.

### Core quality

| Skill | Desc spezifisch + wann | <500 | Details ausgelagert | keine Historie | Begriffe konsistent | konkrete Beispiele | Refs 1 Ebene | Progressive Disclosure | klarer Workflow |
|---|---|---:|---|---|---|---|---|---|---|
| audit | ✅ | ✅ 320 | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ✅ |
| cc-steuerung | ⚠️ | ✅ 429 | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| chat-wechsel | ✅ | ❌ 571 | ❌ | ✅ | ⚠️ | ✅ | ⚠️ | ❌ | ✅ |
| chatgpt-review | ✅ | ❌ 548 | ❌ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ✅ |
| code-erstellen | ✅ | ❌ 524 | ✅ | ⚠️ | ⚠️ | ✅ | ❌ | ✅ | ✅ |
| doc-pflege | ✅ | ✅ 467 | ⚠️ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ✅ |
| git-commit-helper | ✅ | ✅ 274 | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| mockup-erstellen | ✅ | ❌ 596 | ❌ | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ |
| skill-neu | ✅ | ❌ 534 | ❌ | ❌ | ⚠️ | ✅ | ✅ | ❌ | ✅ |
| skill-pflege | ✅ | ❌ 628 | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| ticket | ✅ | ✅ 158 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| tracker | ✅ | ✅ 461 | ✅ | ❌ | ⚠️ | ✅ | ✅ | ✅ | ✅ |

Eine Präzisierung zu `code-erstellen`: `references/stacks/csharp-wpf.md` usw. liegen aus Sicht von SKILL.md unter `references/stacks/…`, also **zwei Verzeichnisebenen tief**. Anthropics Empfehlung lautet ausdrücklich, References direkt eine Ebene tief erreichbar zu halten. Ich würde deshalb später `references/csharp-wpf.md`, `references/python.md` usw. daraus machen.

Beim Tracker ist die Grundstruktur dagegen richtig. Das Problem sind die langen References: elf überschreiten laut deiner Messung 100 Zeilen und brauchen nach offizieller Empfehlung ein Inhaltsverzeichnis.

### Testing

| Skill | ≥3 Eval-Fälle definiert | Haiku/Sonnet/Opus | reale Nutzung gemessen | Feedback |
|---|---|---|---|---|
| audit | ✅ | ❌ | ⚠️ April, inzwischen verändert | — |
| cc-steuerung | ✅ | ❌ | ⚠️ April, inzwischen überholt | — |
| chat-wechsel | ✅ | ❌ | ⚠️ kein belastbarer frischer Lauf | — |
| chatgpt-review | ✅ | ❌ | ⚠️ | — |
| code-erstellen | ✅ | ❌ | ⚠️ alter Lauf zeigte massive Triggerprobleme | — |
| doc-pflege | ✅ | ❌ | ⚠️ | — |
| git-commit-helper | ✅ | ❌ | ⚠️ | — |
| mockup-erstellen | ✅ | ❌ | ⚠️ | — |
| skill-neu | ✅ | ❌ | ⚠️ | — |
| skill-pflege | ✅ | ❌ | ⚠️ | — |
| ticket | ✅ test-prompts | ❌ | ⚠️ keine formale Messung | — |
| tracker | ✅ | ❌ | ✅ reale Nutzung + alter Smoke | — |

„Feedback“ ist für dieses private Ein-Nutzer-System kein sinnvoller Team-Gate und deshalb `—`, nicht ❌.

Die größte Lücke ist damit eindeutig: **Die Fälle existieren größtenteils, aber die heute aktiven Fassungen wurden nicht systematisch vermessen.** Anthropic empfiehlt zudem Tests mit allen tatsächlich eingesetzten Modellen. Falls Herbert praktisch nur Sonnet und ggf. Opus nutzt, würde ich nicht künstlich Haiku testen; die offizielle Formulierung davor lautet sinngemäß „alle Modelle testen, die man einsetzen will“.

## Zwei wichtigste Folgen je Skill

| Skill | Folge 1 | Folge 2 |
|---|---|---|
| audit | Projekt-Prüfregeln auslagern | Konfliktgrenze zu doc-pflege/modul-bauplan evaluieren |
| cc-steuerung | auf ~100-Zeilen-Cowork-Adapter reduzieren | expliziter Claude-Code-Negativfall |
| chat-wechsel | Cowork-/Task-/Memory-Details auslagern | vollständiger Claude-Code-Handover bleibt gemäß S6 |
| chatgpt-review | CGR-Lifecycle auslagern | Push-Prüfung bleibt, Push-Recht kommt aus Profil |
| code-erstellen | Kern unter 500 | Stack-Refs eine Ebene hochziehen |
| doc-pflege | Modi 3/4/6 öffentlich entfernen | nur Schreiben/Pflegen; Prüfung zu audit |
| git-commit-helper | Push/Version strikt aus Profil | PowerShell-Sequenz korrigieren |
| mockup-erstellen | Sitemap/BPM-Details auslagern | visuelle Qualitätskriterien explizit machen |
| skill-neu | Skill-Grundlagen stark kürzen | Governance + Kollisionsprüfung + Eval beibehalten |
| skill-pflege | Safe Patch/Refactor einführen | Historie und Liefermechanik aus Kern |
| ticket | weitgehend unverändert lassen | nur Begriffe/Profile angleichen |
| tracker | lange References mit TOC | Historienmarken und Drift-Config bereinigen |

---

# 2. Wo Leitfaden und unsere Regeln kollidieren

## MCP-Werkzeugnamen

Anthropic sagt ausdrücklich: Wenn ein Skill MCP verwendet, soll der vollständig qualifizierte Name `ServerName:tool_name` verwendet werden.

Das widerspricht unserer Neutralitätsregel „Handlung statt Werkzeug“ nur scheinbar.

Neue Regel:

> **Kernlogik beschreibt die Handlung. Wenn die Handlung zwingend über ein konkretes MCP erfolgt, steht der vollständig qualifizierte Werkzeugname im Umgebungs-/Integrationsabschnitt oder in einer Reference.**

Also nicht:

> „Benutze immer Tool X, um eine Auswahl zu stellen.“

Aber durchaus:

> „Erstelle die Aufgabe über `ClickUp:create_task`, wenn der ClickUp-Connector verfügbar ist.“

Das erfüllt beide Maßstäbe.

## Harte MUSS/NIE/IMMER-Regeln

Anthropic empfiehlt den Freiheitsgrad nach Fragilität zu wählen: enge Führung bei gefährlichen/deterministischen Abläufen, mehr Urteilsspielraum bei offenen Aufgaben.

Daraus folgt:

**MUSS/NIE** bleiben für:

- Statusübergänge
- Datenverlustschutz
- Secrets
- Push-Policy
- Versionsquelle
- Ticketzustände
- Commit-Voraussetzungen
- Regel-Inventar bei Refactor

Nicht für:

- Doku-Stil im Detail
- jedes Mockup-Layout
- jede Auswahlfrage
- Reihenfolgen, bei denen mehrere Wege gleichwertig sind.

## Historienmarken

Hier folgt die neue Regel direkt Anthropic:

> Aktive Skill-Regeln enthalten keine Incident-Historie, Sitzungsnummern, Daten oder alte Versionsgeschichten. Historie gehört in CHANGELOG, Review-Artefakte oder einen expliziten `Old patterns`-Abschnitt einer Reference.

Damit fliegen insbesondere `skill-pflege-006`, „Teil 31“, alte Datumsbegründungen usw. aus den Kernen.

## Fragepflicht

Die alte Invariante wird vollständig ersetzt:

> **Frage nur, wenn nach Auftrag, Skill-Profil, vorhandener Regel und aktuellem Kontext eine echte Entscheidung offen bleibt. Wenn gefragt wird und feste Optionen existieren, verwende die Auswahlfunktion der Umgebung.**

Das passt außerdem zu Anthropics Hinweis, nicht unnötig viele Optionen anzubieten.

## `skill-neu` erklärt Claude das Schreiben von Skills

Anthropic sagt ausdrücklich, Claude kenne das Format bereits und brauche keinen speziellen „how to write skills“-Prompt.

Das heißt **nicht**, dass `skill-neu` überflüssig ist.

Überflüssig werden dort:

- lange Erklärung von Progressive Disclosure
- Grundkurs SKILL.md
- Grundkurs Description
- allgemeine Schreibstil-Lehre.

Behalten werden:

- Repo-spezifische Governance
- Neutralitätscheck
- Skill-Profil-Vertrag
- Konfliktprüfung mit vorhandenen Skills
- Eval-Erzeugung
- Two-Place-Auslieferung
- CHANGELOG/INDEX-Verfahren.

`skill-neu` wird also vom **Tutorial** zum **Governance-Workflow**.

---

# 3. Skill-Profil v1 – Endfassung

Ich übernehme S2: **ein Wert steht genau einmal**. Prosa darf auf ihn verweisen, ihn aber nicht wiederholen.

Lange Regeln werden nicht in das Profil kopiert, sondern referenziert.

## Verbindliches Format

```markdown
## Skill-Profil

- Profil-Version: 1
- Projekt-ID: <slug>
- Repo: <owner/repo>
- Branch-Policy: current | fixed:<branch>

### Checks
- <name>: <Befehl oder Semikolon-Liste>

### Commit
- Format: <Formatstring>
- Module: <Kürzel=Pfad; ...> | fehlt
- Versionsquelle: none | <pfad>#<feld>
- Versionsregel: none | <kompakte Regel> | ref:<pfad>#<abschnitt>
- Push-Policy: user-only | allowed | required-after-commit | required-at-session-end
- Pre-Commit-Checks: none | <Check-Name>
- Doku-Check: none | ref:<pfad>#<abschnitt>

### Code
- Stacks: <skill-reference-keys>
- Pflichtkontext: <Pfad/Abschnitt; ...>
- Aufgabenquelle: none | ref:<pfad>#<abschnitt>
- Architekturregeln: none | ref:<pfad>#<abschnitt>
- Tests: none | <Check-Name>
- Auslieferung: none | ref:<pfad>#<abschnitt>
- Mockup-Policy: none | required:<Bedingung> | ref:<pfad>#<abschnitt>
- Befund-Ort: none | ref:<pfad>#<abschnitt>

### Doku
- Router: none | <pfad>
- Standard: none | ref:<pfad>#<abschnitt>
- Pflichtdokumente: none | <Pfad; ...>
- Validierungsregeln: none | ref:<pfad>#<abschnitt>
- Sitzungsabschluss: none | ref:<pfad>#<abschnitt>
- Entscheidungs-Ort: none | ref:<pfad>#<abschnitt>

### Tracker
- Provider: none | clickup
- Config: none | <Projektpfad>
- Aufgabenquelle: none | ref:<pfad>#<abschnitt>
- Statusmodell: none | ref:<pfad>#<abschnitt>

### Mockup
- Ablage: none | <pfad>
- Designquelle: none | <pfad/ref>
- Ansichten: none | <Liste>
- Abnahme-Ort: none | ref:<pfad>#<abschnitt>

### Review
- Ablage: none | <pfad>
- Kontextquelle: none | <Liste/ref>
- Pflichtblock: none | ref:<pfad>#<abschnitt>
- Ergebnis-Ort: none | ref:<pfad>#<abschnitt>

### Ticket
- Quelle: none | <ref>
- Schreibweg: none | <Befehl/ref>
- Statusmodell: none | ref:<pfad>#<abschnitt>
- Tracker-Kopplung: none | <Regel/ref>
- Beweisquelle: none | <ref>

### Modul
- Manifest: none | <Pfad/Pattern>
- Grundsatzregeln: none | ref:<pfad>#<abschnitt>
```

## Schema-Regeln

`Profil-Version` ist eine Integer-Schemaversion. Version 1 ist jetzt die einzige erlaubte Version.

`fehlt` darf nur während Migration/Audit vorkommen. Ein produktiver Skill darf einen benötigten Wert nicht erraten.

`none` bedeutet bewusst nicht vorhanden und ist gültig. `fehlt` bedeutet unbekannt und blockiert einen Skill, der diesen Wert benötigt.

`ref:` zeigt auf lange Regeln und verhindert Duplizierung.

Pfade werden im Profil mit `/` geschrieben, soweit technisch möglich; Anthropics Leitfaden empfiehlt plattformneutrale Pfade.

## Fehlendes Pflichtfeld

Genau wie vorgeschlagen:

> `<Skill>` benötigt `<Feld>`, das im Skill-Profil fehlt.

Dann nur bei echter Notwendigkeit Auswahl:

- Profil ergänzen
- einmalig Wert nennen
- Aktion abbrechen

Kein „Profil komplett neu erstellen?“.

---

# 4. Pflichtfelder je Skill

`Projekt-ID`, `Repo`, `Branch-Policy` sind Grundfelder und werden nicht in jeder Zeile wiederholt.

| Skill | zusätzliche Pflichtfelder |
|---|---|
| audit | Doku.Validierungsregeln, Doku.Router; Code.Architekturregeln wenn Code geprüft wird; Tracker.Config wenn Tracker-Konsistenz geprüft wird |
| cc-steuerung | keine Projektfelder; nur Umgebung Cowork + ausdrücklicher DC-Auftrag |
| chat-wechsel | Doku.Sitzungsabschluss, Doku.Entscheidungs-Ort; Tracker.* wenn Aufgaben eingebunden sind; Commit.Push-Policy |
| chatgpt-review | Review.Ablage, Review.Kontextquelle, Review.Ergebnis-Ort, Commit.Push-Policy |
| code-erstellen | Code.Stacks, Pflichtkontext, Architekturregeln, Tests, Auslieferung; Aufgabenquelle wenn projektgeführt |
| doc-pflege | Doku.Router, Standard, Validierungsregeln, Entscheidungs-Ort |
| git-commit-helper | Commit.Format, Versionsquelle, Versionsregel, Push-Policy, Pre-Commit-Checks |
| mockup-erstellen | Mockup.Ablage, Designquelle, Ansichten, Abnahme-Ort |
| skill-neu | Skill-Repo-spezifisch: Doku/Commit-Regeln des Skill-Repos |
| skill-pflege | Skill-Repo-spezifisch: Doku/Commit-Regeln des Skill-Repos |
| ticket | Ticket.Quelle, Schreibweg, Statusmodell; Tracker-Kopplung falls nicht `none` |
| tracker | Tracker.Provider, Config, Statusmodell |
| modul-bauplan | Modul.Manifest, Modul.Grundsatzregeln + Code/Doku-Felder für das Projekt |

Wichtig bei `modul-bauplan`: Das Skill-Profil enthält **keine fachlichen Moduldaten**. `module.yaml` beschreibt das Modul; das Skill-Profil beschreibt die Arbeitsweise im Repo. S8 ist damit vollständig bestätigt.

---

# 5. Drei Profile aus dem heutigen belegten Stand

## HA_Dash_DreameX60

```markdown
## Skill-Profil

- Profil-Version: 1
- Projekt-ID: heidi
- Repo: herbertschrotter-blip/HA_Dash_DreameX60
- Branch-Policy: fixed:main

### Checks
- card: npm test; npm run lint
- backend: python -m pytest

### Commit
- Format: [vX.Y.Z] Modul, Typ: Kurztitel
- Module: Karte=card/; Backend=ha/; Doku=docs/; Werkzeuge=tools/
- Versionsquelle: card/package.json#version
- Versionsregel: Feature=MINOR nur neue Funktion; Verbesserung/Fix/Umbau=PATCH; Doku/Werkzeuge ohne Laufzeitänderung=kein Bump
- Push-Policy: required-at-session-end
- Pre-Commit-Checks: card bzw. backend nach Änderung
- Doku-Check: ref:CLAUDE.md#arbeitsweise

### Code
- Stacks: typescript-lit; home-assistant-yaml; python
- Pflichtkontext: docs/STATUS.md; passende Modul-Doku; docs/ENTSCHEIDUNGEN.md
- Aufgabenquelle: fehlt
- Architekturregeln: ref:CLAUDE.md#regeln
- Tests: card/backend
- Auslieferung: ref:CLAUDE.md#arbeitsweise
- Mockup-Policy: required:große Umbauten der Oberfläche
- Befund-Ort: docs/ENTSCHEIDUNGEN.md bzw. docs/AUDIT.md

### Doku
- Router: docs/README.md
- Standard: ref:docs/README.md#regeln-für-diese-doku
- Pflichtdokumente: fehlt
- Validierungsregeln: fehlt
- Sitzungsabschluss: ref:CLAUDE.md#arbeitsweise
- Entscheidungs-Ort: docs/ENTSCHEIDUNGEN.md

### Tracker
- Provider: clickup
- Config: fehlt
- Aufgabenquelle: fehlt
- Statusmodell: fehlt

### Mockup
- Ablage: mockups/
- Designquelle: fehlt
- Ansichten: fehlt
- Abnahme-Ort: fehlt

### Review
- Ablage: fehlt
- Kontextquelle: fehlt
- Pflichtblock: fehlt
- Ergebnis-Ort: fehlt

### Ticket
- Quelle: /config/prognose/diag/tickets.json
- Schreibweg: tools/ticket.ps1
- Statusmodell: ref:docs/DIAGNOSE.md
- Tracker-Kopplung: fehlt
- Beweisquelle: ref:docs/DIAGNOSE.md

### Modul
- Manifest: fehlt
- Grundsatzregeln: fehlt
```

Das ist bewusst **nicht** das alte Heidi-Profil kopiert. Lücken bleiben Lücken.

Danach kann `## Commits` weitgehend entfallen und auf `## Skill-Profil → Commit` verweisen. `## Aufgaben und Tickets` behält die menschliche Erklärung, IDs/Nummernschemata gehören aber in die Tracker-Config. `## Arbeitsweise` bleibt als Regelwerk bestehen; das Profil verweist darauf, statt Tests/Deploy erneut in Prosa zu duplizieren.

---

## BPM

```markdown
## Skill-Profil

- Profil-Version: 1
- Projekt-ID: bpm
- Repo: herbertschrotter-blip/BauProjektManager
- Branch-Policy: fixed:main

### Checks
- pre-commit: fehlt

### Commit
- Format: [vX.Y.Z] Modul, Typ: Kurztitel
- Module: fehlt
- Versionsquelle: Directory.Build.props
- Versionsregel: fehlt
- Push-Policy: user-only
- Pre-Commit-Checks: fehlt
- Doku-Check: ref:INDEX.md#8-doc-pflege-policy

### Code
- Stacks: csharp-wpf
- Pflichtkontext: INDEX.md + dort geroutete Docs
- Aufgabenquelle: fehlt
- Architekturregeln: ref:Docs/Kern/BauProjektManager_Architektur.md
- Tests: fehlt
- Auslieferung: fehlt
- Mockup-Policy: fehlt
- Befund-Ort: fehlt

### Doku
- Router: INDEX.md
- Standard: fehlt
- Pflichtdokumente: über INDEX.md geroutet
- Validierungsregeln: fehlt
- Sitzungsabschluss: fehlt
- Entscheidungs-Ort: Docs/Referenz/ADR.md

### Tracker
- Provider: fehlt
- Config: fehlt
- Aufgabenquelle: fehlt
- Statusmodell: fehlt

### Mockup
- Ablage: fehlt
- Designquelle: Docs/Referenz/UI_UX_Guidelines.md
- Ansichten: fehlt
- Abnahme-Ort: fehlt

### Review
- Ablage: fehlt
- Kontextquelle: fehlt
- Pflichtblock: fehlt
- Ergebnis-Ort: fehlt

### Ticket
- Quelle: none
- Schreibweg: none
- Statusmodell: none
- Tracker-Kopplung: none
- Beweisquelle: none

### Modul
- Manifest: none
- Grundsatzregeln: none
```

Danach wird `CLAUDE.md ## Git` auf eine knappe Verweisregel reduziert. `INDEX.md Projekt-Metadaten` sollte Repo, Branch und Versionsquelle nicht weiter duplizieren, sondern auf das Skill-Profil verweisen.

---

## Skill-Repo

```markdown
## Skill-Profil

- Profil-Version: 1
- Projekt-ID: claude-skills-bpm
- Repo: herbertschrotter-blip/claude-skills-bpm
- Branch-Policy: fehlt

### Checks
- skill-validation: fehlt
- routing-eval: fehlt

### Commit
- Format: fehlt
- Module: fehlt
- Versionsquelle: fehlt
- Versionsregel: fehlt
- Push-Policy: fehlt
- Pre-Commit-Checks: skill-validation; routing-eval
- Doku-Check: fehlt

### Code
- Stacks: none
- Pflichtkontext: INDEX.md; offizielle Skill-Leitlinien; Neutralitäts-Checkliste
- Aufgabenquelle: none
- Architekturregeln: ref:docs/project-architecture.md
- Tests: routing-eval
- Auslieferung: claude.ai Skill-Upload
- Mockup-Policy: none
- Befund-Ort: docs/chatgpt-reviews/

### Doku
- Router: INDEX.md
- Standard: fehlt
- Pflichtdokumente: INDEX.md; README.md; CHANGELOG.md
- Validierungsregeln: fehlt
- Sitzungsabschluss: fehlt
- Entscheidungs-Ort: docs/chatgpt-reviews/

### Tracker
- Provider: fehlt
- Config: fehlt
- Aufgabenquelle: none
- Statusmodell: fehlt

### Mockup
- Ablage: none
- Designquelle: none
- Ansichten: none
- Abnahme-Ort: none

### Review
- Ablage: docs/chatgpt-reviews/
- Kontextquelle: INDEX.md; docs/project-architecture.md; betroffene SKILL.md
- Pflichtblock: Neutralitäts-Checkliste
- Ergebnis-Ort: betroffene Skills; CHANGELOG.md

### Ticket
- Quelle: none
- Schreibweg: none
- Statusmodell: none
- Tracker-Kopplung: none
- Beweisquelle: none
```

Der heutige separate `## Review-Profil`-Abschnitt geht danach vollständig im `Skill-Profil → Review` auf.

---

# 6. S7 – Tracker-Config ins Projekt-Repo?

### Entscheidung: Ja

`projects/<name>/` im Skill-Repo sollte für aktive Projektwerte aufgegeben werden.

Grund:

> Skill = Verfahren. Projekt-Repo = Projektwahrheit.

Der heutige Heidi-Fall zeigt, wie schnell die zweite Kopie driftet.

Ich würde große Configs im Projekt z. B. so ablegen:

```text
.claude/
└── skill-config/
    ├── tracker.md
    └── ticket.md
```

oder unter einem bestehenden Projektdoku-Bereich.

Das Skill-Profil verweist darauf:

```text
Tracker.Config: .claude/skill-config/tracker.md
```

Cowork kippt diese Entscheidung nicht. Wenn der Projekt-Repo-Kontext dort verfügbar ist, wird er gelesen; wenn nicht, greift der definierte feldweise Fallback. Eine dauerhaft veraltende zweite Kopie im Skill-Repo ist schlechter als ein sauber erkennbarer fehlender Kontext.

---

# 7. `skill-pflege` – baubare Spezifikation

## Modus Safe Patch

Verwenden bei:

- einzelne Regel ergänzen/korrigieren
- Description gezielt ändern
- kleiner Fehler
- kein Strukturumbau.

Ablauf:

1. aktuellen Repo-Stand vollständig lesen
2. Scope exakt benennen
3. nur betroffene Regelstellen ändern
4. keine unbeteiligte Struktur verändern
5. Querverweise prüfen
6. mechanischen Skill-Check ausführen
7. relevante Evals ausführen
8. Diff-Report
9. CHANGELOG/INDEX nach Bedarf
10. Two-Place-Lieferung.

## Modus Refactor

Verwenden bei:

- Kürzen
- Zusammenführen
- Verschieben nach References
- Strukturänderung
- mehrere alte Regeln ersetzen
- tote Regeln entfernen.

Ablauf:

1. Skill + References vollständig lesen.
2. mechanisches Regel-Kandidaten-Inventar erzeugen.
3. semantisch vervollständigen.
4. Zielstruktur entwerfen.
5. Inventarzustände zuweisen.
6. alle `DROP` gesammelt freigeben lassen.
7. Refactor durchführen.
8. Alt→Neu-Abgleich.
9. Neu→Alt-Abgleich.
10. Querverweise prüfen.
11. Leitfaden-/Neutralitätsprüfung.
12. Evals ausführen.
13. Inventar + Diff + Ergebnis committen.
14. Two-Place-Lieferung.

## Regel-Inventar-Datei

Ort:

```text
docs/skill-refactors/<YYYY-MM-DD>-<skill>.md
```

Das Datum steht damit im Review-Artefakt, **nicht im Skill-Regeltext**.

Format:

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md §… | … | KEEP | SKILL.md `## Kernregeln` | — | — | ✅ |
| R002 | … | … | MOVE | references/cowork.md | — | — | ✅ |
| R003 | … | … | MERGE | … | R007 | — | ✅ |
| R004 | … | … | REWRITE | … | — | — | ✅ semantisch |
| R005 | … | … | DROP | — | — | Batch A | ✅ |

Zustände exakt:

`KEEP | MOVE | MERGE | REWRITE | DROP | NEW`

`NEW` ist für Regeln nötig, die erst im neuen Text entstehen.

## Mechanisches Vorsammeln

Das Prüfskript markiert Kandidaten aus:

- `MUSS`
- `NIE`
- `IMMER`
- `PFLICHT`
- `VERBOTEN`
- Tabellen mit verpflichtenden Zuständen/Aktionen
- Description und Negativtrigger
- Statusübergänge.

Aber: Das Script erzeugt **Kandidaten**, kein vollständiges Regelverständnis. Implizite normative Sätze brauchen Urteil.

## Bidirektionaler Abgleich

Alt → Neu:

> Jede alte Regel-ID muss einen Zustand besitzen.

Neu → Alt:

> Jede normative Regel im neuen Text muss einer alten ID oder `NEW` zugeordnet sein.

Damit kann weder still etwas verschwinden noch unbemerkt eine neue Vorschrift entstehen.

## DROP-Freigabe

Keine Frage je Regel.

Vor dem Schreiben:

```text
DROP-Gruppe A:
R005 – Grund …
R012 – Grund …
R019 – Grund …
```

Eine Sammelfreigabe.

## Querverweise

Keine nummerierten Verweise mehr wie:

> Regel 21  
> Kapitel 4  
> Modus 6

Sondern:

```text
skills/tracker/references/anker-system.md#temp-id
skills/doc-pflege/SKILL.md#sitzungsabschluss
```

Semantische Überschrift + Datei.

## Alte Regeln

**1 Original lesen:** bleibt.

**2 nie löschen:** nur noch Safe Patch. Im Refactor ersetzt durch Inventar.

**3 nie kürzen:** entfällt.

**4 nie umformulieren:** entfällt; semantischer Abgleich ersetzt es.

**5 Struktur nie ändern:** Safe Patch ja, Refactor nein.

**6 Frontmatter nicht ändern:** neu: nur ändern, wenn Trigger/Zuständigkeit betroffen; dann Trigger-Eval Pflicht.

**19 Eigenständig bleiben:** wird:

> Self-contained contract, not duplicated implementation.

**21 Split-Regel:** bleibt, aber nach offiziellem Maßstab verschärft:

- Ziel <500 Zeilen
- Detailabläufe in References
- References direkt eine Ebene
- >100 Zeilen mit Inhaltsverzeichnis
- umgebungs- oder integrationsspezifische Abläufe aus Kern heraus.

## Lieferung

Two-Place bleibt wegen Herberts Distributionsentscheidung, aber vollständig in:

```text
references/delivery.md
```

Dort:

- Repo zuerst
- claude.ai Datei/Zip
- exakter `SKILL.md`-Name
- ein Artifact pro Antwort
- Cowork-Sonderfälle.

Der Kern enthält nur:

> Nach erfolgreicher Prüfung gemäß `references/delivery.md` ausliefern.

---

# 8. Eval – `claude plugin eval`

### Urteil: Ja, als Hauptwerkzeug für Routing-Regressionsmessung

`claude plugin eval` ist genau für reproduzierbare Plugin-/Skill-Evals gedacht. Ein Fall ist ein realistischer Prompt plus Grader; `tool_used` kann konkret prüfen, ob ein bestimmter Skill aufgerufen wurde. Standardmäßig läuft jeder Fall dreimal in frischen isolierten Sitzungen.

Das Skill-Repo bekommt dafür:

```text
.claude-plugin/
└── plugin.json
```

nur als Test-Harness. Die Produktivverteilung bleibt claude.ai.

## Zwei Eval-Systeme nicht vermischen

Die Formate sind offiziell verschieden:

- `claude plugin eval` → Fallordner mit `prompt.md`, `graders/`, optional `case.yaml`
- `skill-creator` → `evals/evals.json`

Anthropic sagt ausdrücklich, dass die Formate nicht austauschbar sind.

Daher:

### Routing und Konflikte im eigenen Skillset
→ **plugin eval**

### Ergebnisqualität und Verbesserung eines einzelnen Skills
→ **skill-creator**

`skill-creator` kann zusätzlich:

- mit/ohne Skill vergleichen
- Passrate, Zeit und Tokens messen
- Version A/B
- Description should-trigger/should-not-trigger optimieren.

Damit ist `test-prompts.md` als drittes System überflüssig.

---

# 9. Fallformat

Für unsere 60 Routingfälle würde ich **die nativen plugin-eval-Fallordner** verwenden, keine eigene `cases.json`.

Beispiel:

```text
evals/
└── audit-frontmatter-readonly/
    ├── prompt.md
    └── graders/
        ├── audit-fired.md
        └── doc-pflege-not-fired.md
```

`audit-fired.md`:

```yaml
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?audit"'
---
```

Das ist genau das dokumentierte Muster.

Für Negativfälle kann derselbe Grader mit `min: 0`, `max: 0` verwendet werden; die Dokumentation beschreibt dies ausdrücklich für „must not invoke“.

Die `skills/query/files/expected_behavior`-Struktur des allgemeinen Leitfadens bleibt das **inhaltliche Modell für Output-Evals**, aber nicht unsere zweite physische Routing-Testquelle.

---

# 10. 60 Fälle nach Risiko

| Skill | Fälle |
|---|---:|
| code-erstellen | 8 |
| doc-pflege | 7 |
| audit | 7 |
| mockup-erstellen | 6 |
| skill-pflege | 6 |
| skill-neu | 5 |
| chat-wechsel | 4 |
| chatgpt-review | 4 |
| tracker | 4 |
| git-commit-helper | 3 |
| ticket | 3 |
| cc-steuerung | 3 |
| **Gesamt** | **60** |

Konfliktfälle werden **innerhalb** dieser 60 gezählt, nicht zusätzlich.

Pflicht enthalten:

- audit ↔ doc-pflege
- audit ↔ modul-bauplan
- skill-neu ↔ skill-pflege
- code-erstellen ↔ mockup
- ticket ↔ tracker
- ticket ↔ code-erstellen
- chat-wechsel ↔ chatgpt-review
- code-erstellen ↔ tracker
- generisches „prüfe…“
- generisches „ändere…“
- `cc-steuerung` bei Claude-Code-Kontext darf nicht auslösen.

Descriptions ändern wir gemäß S5 **erst nach der Baseline**.

---

# 11. Schwellen und Gate

Deinen Vorschlag 3/3 bzw. 2/3 übernehme ich.

## Kritisch

3/3:

- falscher Skill könnte schreiben/löschen
- Push-/Commit-Verwechslung
- ticket/tracker-Status
- audit vs Schreibskill
- cc-steuerung in Claude Code
- skill-neu vs skill-pflege
- modul-bauplan vs audit.

## Normal

mindestens 2/3.

## Freigabe

Ein Refactor ist freigegeben, wenn:

1. kein kritischer Fall schlechter als 3/3,
2. kein bisher bestandener Negativfall zur Fehlaktivierung wird,
3. Gesamtquote nicht unter Baseline fällt,
4. neue Konflikte begründet oder korrigiert sind,
5. Skill-Qualitätscheck keine neuen ❌ erzeugt.

---

# 12. Kosten

Ein voller Lauf mit 60 Fällen und Standardkonfiguration bedeutet:

- 60 × 3 = **180 Runs mit Plugin**
- mit Standard-Ablation zusätzlich 180 ohne Plugin
- also **360 Agent-Runs**.

Zusätzliche `llm`-Grader verursachen weitere Modellaufrufe; `tool_used`, `regex`, `tool_order` und `file_exists` sind dagegen kostenfrei als Grader.

Für reines Routing ist deshalb:

```text
--runs 3
--ablation none
```

richtig.

Dann bleiben 180 Agent-Runs.

Eine belastbare Dollarzahl kann ich vor dem ersten Lauf **nicht** angeben, weil Modell, Promptlänge, Skilllänge und Turns den Verbrauch bestimmen. Die offizielle Dokumentation zeigt nur ein Beispiel, bei dem ein einzelner Fall mit sechs Runs `$0.41` kostete; linear wären 60 solcher Fälle etwa `$24.60`, aber das ist ausdrücklich **keine belastbare Prognose** für dieses Repo.

Sauberer Ablauf:

1. 5 repräsentative Fälle
2. 3 Runs
3. `--ablation none`
4. keine LLM-Grader
5. beobachtete Kosten pro Fall erfassen
6. daraus Full-Run-Budget ableiten.

Mit:

```text
--max-cost-usd 5
```

für den Pilot.

Danach den Full-Run-Cap aus den echten Pilotkosten setzen. `--max-cost-usd` wird offiziell unterstützt und stoppt das Starten weiterer Runs nach Erreichen des Budgets.

Für reine Routingfälle würde ich außerdem `max_turns` auf etwa 3–5 begrenzen, statt den Default 10 zu verwenden.

---

# 13. Konflikte mit Anthropic-Skills

Hier ist deine offene Frage jetzt beantwortet.

`plugin eval` startet eine Wegwerf-Sitzung **mit nur dem Ziel-Plugin**. Persönliche Einstellungen, CLAUDE.md, andere installierte Plugins, Memory und andere Skills werden nicht geladen.

Damit misst ein normaler Lauf **nicht zuverlässig**:

- `skill-creator ↔ skill-neu`
- `skill-creator ↔ skill-pflege`
- `code-review ↔ audit`

gegen Herberts reale Umgebung.

Ich würde deshalb zwei Ebenen führen:

### Automatisch
`plugin eval` für alle Konflikte **innerhalb unseres Plugins**.

### Real-Environment-Golden-Set
Für Anthropic-/Account-Kollisionen je 3–5 fest definierte Prompts in frischen normalen Claude-Code-Sitzungen mit dem tatsächlich geladenen Skillset.

Ergebnis protokollieren:

```text
Prompt
geladene Skills
tatsächlich gewählter Skill
PASS/FAIL
Claude-Code-Version
Modell
```

Ob sich mehrere externe Plugin-Verzeichnisse gezielt in denselben Eval-Run einschleusen lassen, ist aus den von mir geprüften offiziellen Stellen nicht ausreichend belegt, um darauf unsere Architektur zu bauen. Bis das verifiziert ist, bleibt dieser Teil ein echter Real-Session-Test.

---

# 14. Skill-Analyse – eigener Skill?

### Entscheidung: Nein, kein 13. Skill

Dein Vorschlag ist architektonisch sauberer.

Das System wird:

```text
Prüfskript
    ↓ mechanische Fakten
audit
    ↓ interpretiert Gesamtzustand
skill-pflege
    ↓ nutzt dieselbe Prüfung als Postcondition
plugin eval / skill-creator
    ↓ messen Verhalten
```

Damit entsteht keine weitere Description-Konkurrenz.

## Mechanisch prüfbar

Ein kleines Script kann deterministisch prüfen:

- YAML-Frontmatter gültig
- Name-Regeln
- Description vorhanden
- Description ≤1024
- Zeilenzahl SKILL.md
- Reference-Pfade existieren
- Reference-Tiefe
- References >100 Zeilen ohne Inhaltsverzeichnis
- Windows-Pfade
- Historien-/Datumsmarker
- bekannte obsolete Werkzeugnamen
- MCP-Werkzeugnamen ohne Server-Präfix
- tote Markdown-Links
- Cross-Skill-Verweise auf fehlende Dateien/Überschriften
- nummerierte Verweise (`Regel 21`, `Kapitel 4` usw.)
- `test-prompts.md`-Altlasten
- Eval-Fälle vorhanden
- Skill-Profil-Schema vollständig
- ZIP-Duplikate bzw. getrackte generierte Artefakte
- Description-/Skillnamen-Kollisionen exakt/näherungsweise
- normative Marker für das Regel-Inventar.

Das Script sollte einen strukturierten Bericht erzeugen, z. B.:

```json
{
  "skill": "skill-pflege",
  "errors": [],
  "warnings": [],
  "metrics": {}
}
```

## Urteil erforderlich

`audit` bzw. Claude muss beurteilen:

- Ist die Description semantisch zu breit/zu eng?
- Kollidiert sie mit einem anderen Skill trotz unterschiedlicher Wörter?
- Ist eine Regel überhaupt nötig?
- Ist der Freiheitsgrad angemessen?
- Ist eine Regel projektneutral?
- Sind zwei Regeln semantisch doppelt?
- Ist ein Beispiel hilfreich oder veraltet?
- Ist Progressive Disclosure sinnvoll geschnitten?
- Muss ein Ablauf hart oder flexibel sein?
- Ist der Skill überhaupt noch eine eigene Fähigkeit wert?
- Sind Eval-Prompts realistisch?
- Ist das Ergebnis qualitativ besser als ohne Skill?

Das lässt sich nicht sinnvoll durch Regex automatisieren.

## `skill-pflege` bekommt keinen eigenen „Prüfen“-Modus

Sonst entsteht wieder Zuständigkeitsüberlappung.

`skill-pflege` hat:

- Safe Patch
- Refactor

und **beide enden verpflichtend mit derselben Skill-Validierung**, die `audit` auch eigenständig aufrufen kann.

---

# 15. Feste neue Regeln für `skill-neu` und `skill-pflege`

Aus Anthropics Leitfaden übernehmen wir verbindlich:

1. Description: was + wann, spezifische natürliche Schlüsselbegriffe, dritte Person, ≤1024.
2. SKILL.md Ziel <500 Zeilen.
3. References direkt eine Ebene tief.
4. Reference >100 Zeilen → Inhaltsverzeichnis.
5. Keine aktive Historie/zeitabhängige Regeln.
6. Einheitliche Terminologie.
7. Freiheitsgrad nach Fragilität.
8. Mindestens drei Evals vor Freigabe.
9. Evals vor großem Ausbau der Anweisungen.
10. Bei MCP konkrete Werkzeuge vollständig qualifizieren.
11. Reale Nutzung nach dem synthetischen Eval beobachten.
12. Änderungen an Description benötigen Trigger-Eval.

Überflüssig in `skill-neu` werden dagegen Erklärungen, die Claude bereits kennt:

- Was ist ein Skill?
- Warum Progressive Disclosure?
- Wie Markdown/YAML grundsätzlich funktioniert?
- allgemeiner Prompt-Schreibkurs
- ausführliche Anthropic-Theorie.

Die **Regeln** bleiben; die **Lehrbucherklärung** verschwindet.

---

# 16. Namensmuster

Anthropic empfiehlt konsistente Namen, aber das ist hier kein P0-Thema.

Ich würde **keinen Rename-Refactor** starten.

Die bestehenden Namen sind verständlich genug und Umbenennen würde:

- Uploads
- Querverweise
- Evals
- Dokumentation
- Gewohnheit

unnötig destabilisieren.

Das wird als bewusst akzeptierte Abweichung dokumentiert.

---

# 17. Ergebnis zu S1–S8

| Punkt | Urteil |
|---|---|
| S1 doppelte v0.36.0 in Git | ✅ bestätigt |
| S2 Werte genau einmal | ✅ übernehmen |
| S3 mechanisches Regel-Inventar + bidirektional | ✅ übernehmen |
| S4 automatische Evals, 3/3 bzw. 2/3 | ✅ übernehmen |
| S5 Description erst nach Baseline | ✅ zwingend |
| S6 vollständiger chat-wechsel auch Claude Code | ✅ nicht erneut öffnen |
| S7 Tracker-Config ins Projekt-Repo | ✅ übernehmen |
| S8 Skill-Profil ≠ module.yaml | ✅ übernehmen |

---

# ✅ Einigkeit

- Kein neuer Skill-Analyse-Skill.
- `audit` ist der unabhängige Prüfer.
- `skill-pflege` verwendet dieselbe Prüfung als Abschluss.
- `skill-creator` misst Einzel-Skill-Qualität und Description.
- `plugin eval` wird das automatische Routing-/Regressionstool.
- Two-Place bleibt.
- claude.ai bleibt Distributionsquelle.
- `cc-steuerung` bleibt als kleiner Cowork-Adapter und muss in Claude Code negativ getestet werden.
- Skill-Profil v1 ist strikt, ein Block, Werte genau einmal.
- Tracker-/Projektconfig gehört ins Projekt-Repo.
- Refactor wird über Regel-Inventar statt Wortlautkonservierung abgesichert.
- Description-Änderungen kommen erst nach der Baseline.

# ⚠️ Widerspruch / Präzisierung

- Die offizielle Empfehlung „alle Haiku/Sonnet/Opus testen“ würde ich auf **alle Modelle, die Herbert tatsächlich verwendet**, operationalisieren. Sonst bezahlen wir Tests für eine Kombination, die im realen Workflow keine Rolle spielt.
- `plugin eval` ersetzt `skill-creator` nicht. Routing und Ergebnisqualität sind zwei verschiedene Messprobleme.
- Ein automatischer `plugin eval` kann die realen Konflikte mit Herberts extern geladenen Anthropic-Skills nicht allein abbilden, weil die dokumentierte Isolation andere Skills ausblendet. Dafür bleibt ein kleines Real-Environment-Golden-Set.
- Projektwerte aus `projects/<name>/` sollten vollständig aus dem Skill-Repo verschwinden, nicht nur „sekundär“ werden.

# ❓ Für Runde 3 offen

1. konkrete neue `cc-steuerung`-Description und ~100-Zeilen-Kern,
2. welche vier Fachskills danach welche cc-Verweise verlieren,
3. exakte Phase-1-Dateiliste mit Änderung je Datei,
4. neuer schlanker INDEX,
5. Zuordnung der heutigen INDEX-Invarianten 1–10 zu:
   - löschen,
   - globale Regel,
   - Skill-Profil,
   - Fachskill,
   - Reference,
6. endgültiger Pfad/Name für Projekt-Tracker-Config,
7. erstes Schema des mechanischen Skill-Prüfskripts,
8. konkretes Plugin-Manifest + erste fünf Pilot-Evalfälle.

Damit ist Runde 2 aus meiner Sicht konkret genug, dass Runde 3 unmittelbar in einen umsetzbaren Refactor-Plan übergehen kann.
