# Review Runde 3

## Ausgangspunkt

Die neun Korrekturen K1–K9 sind tragfähig. Ich übernehme K1–K9; bei K9 entscheide ich mich für **PowerShell 7** als Laufzeit des mechanischen Prüfskripts. Damit entsteht keine neue Python-Voraussetzung.

K1 ist durch Anthropics Leitfaden gedeckt: Entscheidend ist nicht die physische Ordnertiefe, sondern dass relevante References **direkt aus SKILL.md referenziert werden** und keine Kette SKILL → A → B nötig ist. Anthropics eigenes Domain-Beispiel verwendet `reference/finance.md`; `references/stacks/<key>.md` kann deshalb bleiben, solange SKILL.md direkt darauf zeigt.

Für `plugin eval` sind ebenfalls alle benötigten Mechanismen belegt: ein alternatives Eval-Verzeichnis kann über `experimental.evals` gesetzt werden; Fälle liegen in eigenen Ordnern mit `prompt.md` und `graders/`; `tool_used` kann Skill-Aufrufe messen; drei Läufe sind Standard; `--ablation none` schaltet die Vergleichs-Arme ab.

---

# 1. Skill-Profil v1 – endgültige Fassung

## 1.1 Grundregeln

Das Profil ist **kein zweites Projekt-Handbuch**.

Es erfüllt fünf Aufgaben:

1. kurze maschinenlesbare Werte genau einmal halten,
2. lange Regeln per `ref:` referenzieren,
3. Checks mit Pfad-Selektoren definieren,
4. komplexe Tracker-/Ticket-/Review-Konfigurationen auslagern,
5. Skills bei fehlenden Werten deterministisch blockieren statt raten zu lassen.

Verbindliche Werte:

```text
none   = bewusst nicht vorhanden
fehlt  = müsste vorhanden sein, ist aber noch nicht definiert
ref:   = Regelwerk liegt an anderer Stelle
```

`fehlt` ist nie ein gültiger produktiver Fallback für einen Skill, der das Feld benötigt.

## 1.2 Schema

```markdown
## Skill-Profil

- Profil-Version: 1
- Projekt-ID: <slug>
- Repo: <owner/repo>
- Branch-Policy: current | fixed:<branch>

### Checks

Syntax:
- <check-name>: <befehl> [<pfad-glob>; <pfad-glob>; ...]

Der Check ist anwendbar, wenn mindestens ein geänderter Pfad
einem der angegebenen Globs entspricht.

### Commit

- Format: <format>
- Module: <name=scope; name=scope; ...>
- Versionsquelle: none | <pfad>#<feld> | profile
- Aktuelle-Version: <semver> | none
- Versionsregel: none | <kurzregel> | ref:<pfad>#<überschrift>
- Push-Policy: user-only | allowed | required-after-commit | required-at-session-end
- Pre-Commit-Checks: none | <check-name>; <check-name>; ...
- Doku-Check: none | <kurzregel> | ref:<pfad>#<überschrift>

### Code

- Stacks: none | <key>; <key>; ...
- Pflichtkontext: none | <pfad/ref>; ...
- Aufgabenquelle: none | ref:<pfad>#<überschrift>
- Architekturregeln: none | ref:<pfad>#<überschrift>
- Tests: none | <check-name>; ...
- Auslieferung: none | ref:<pfad>#<überschrift>
- Mockup-Policy: none | required:<bedingung> | ref:<pfad>#<überschrift>
- Befund-Ort: none | <pfad/ref>

### Doku

- Router: none | <pfad>
- Standard: none | ref:<pfad>#<überschrift>
- Pflichtdokumente: none | <pfad/ref>; ...
- Validierungsregeln: none | ref:<pfad>#<überschrift>
- Sitzungsabschluss: none | ref:<pfad>#<überschrift>
- Entscheidungs-Ort: none | <pfad/ref>

### Tracker

- Provider: none | clickup
- Config: none | <pfad>

### Ticket

- Config: none | <pfad>

### Mockup

- Ablage: none | <pfad>
- Designquelle: none | <pfad/ref>
- Ansichten: none | <wert>; ...
- Abnahme-Ort: none | <pfad/ref>

### Review

- Config: none | <pfad>

### Modul

- Manifest: none | <pfad/pattern>
- Grundsatzregeln: none | ref:<pfad>#<überschrift>
```

### Regeln dazu

`Branch-Policy: current` bedeutet: aktuelle Arbeitskopie verwenden. Keine Auswahlfrage, solange diese eindeutig ist.

`fixed:<branch>` bedeutet: Skill prüft den aktuellen Branch gegen den Pflichtbranch. Abweichung ist ein echter Konflikt.

`Checks` sind benannte Operationen **plus Scope**. K4 ist damit gelöst:

```markdown
- card: npm test; npm run lint [card/**]
- backend: python -m pytest [ha/prognose/**]
```

und:

```markdown
- Pre-Commit-Checks: card; backend
```

Es laufen nur die Checks, deren Scope von den Änderungen betroffen ist.

Komplexe variable Strukturen werden nicht mehr in flache Profilfelder gequetscht:

```markdown
### Tracker
- Provider: clickup
- Config: .claude/skill-config/tracker.md

### Ticket
- Config: .claude/skill-config/ticket.md

### Review
- Config: .claude/skill-config/review.md
```

K3 und K5 sind damit sauber gelöst.

---

# 2. Fertiges Skill-Profil für `claude-skills-bpm`

Das kann nach Anlage der genannten Dateien so in `CLAUDE.md` eingesetzt werden:

```markdown
## Skill-Profil

- Profil-Version: 1
- Projekt-ID: claude-skills-bpm
- Repo: herbertschrotter-blip/claude-skills-bpm
- Branch-Policy: fixed:main

### Checks

- skill-validation: pwsh -NoProfile -File tools/validate-skills.ps1 [skills/**; .claude-plugin/**; quality/evals/**; docs/skill-profile-v1.md]
- routing-eval: claude plugin eval . --runs 3 --ablation none --no-publish [skills/**]

### Commit

- Format: [vX.Y.Z] <Modul>, <Typ>: <Kurztitel>
- Module: Skill=<Skill-Name>; Doku=<Thema>; Review=<Thema>; Config=<Thema>; Eval=<Thema>; Tools=<Thema>
- Versionsquelle: profile
- Aktuelle-Version: 0.36.9
- Versionsregel: Skill-Änderung unter skills/** → SemVer-Bump und CHANGELOG; reine Doku-, Review-, Config-, Eval- oder Tooling-Änderung → kein Bump, aktuelle Version beibehalten
- Push-Policy: required-after-commit
- Pre-Commit-Checks: skill-validation; routing-eval
- Doku-Check: Skill-Zuständigkeit oder Trigger geändert → INDEX.md; Architektur/Onboarding geändert → README.md; CHANGELOG.md nur bei Skill-Änderung

### Code

- Stacks: none
- Pflichtkontext: INDEX.md; docs/skill-profile-v1.md; docs/skill-quality.md
- Aufgabenquelle: none
- Architekturregeln: ref:docs/skill-quality.md#verbindliche-qualitätsregeln
- Tests: skill-validation; routing-eval
- Auslieferung: none
- Mockup-Policy: none
- Befund-Ort: docs/chatgpt-reviews/

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
```

Eine Präzisierung: `routing-eval` ist zunächst nur der **Pilot-Suite-Check**. Sobald Herbert die volle Grundmessung freigibt und die 60 Fälle vorhanden sind, bleibt derselbe Checkname und derselbe Befehl bestehen; nur der Inhalt von `quality/evals/` wächst.

Das ist besser als später den Profilvertrag nochmals zu ändern.

---

# 3. Review-Config des Skill-Repos

Das bisherige `## Review-Profil` aus `CLAUDE.md` wandert vollständig nach:

```text
.claude/skill-config/review.md
```

Struktur:

```markdown
# Review-Konfiguration

## Allgemein

- Ablage: docs/chatgpt-reviews/
- Serienformat: CGR-YYYY-MM-DD-<thema>
- Übersicht: docs/chatgpt-reviews/INDEX.md

## Thema: skillsystem

- Reviewer-Rolle: erfahrener Architekt für Prompts und Agent Skills
- Repos:
  - herbertschrotter-blip/claude-skills-bpm
- Kontext:
  - INDEX.md
  - docs/skill-profile-v1.md
  - docs/skill-quality.md
  - betroffene skills/*/SKILL.md
- Pflicht-Block:
  - Neutralitäts-Checkliste
  - offizielle Anthropic-Skill-Qualitätsregeln
- Ergebnis-Orte:
  - betroffene Skills
  - INDEX.md
  - CHANGELOG.md

## Thema: ha-grundsatz

- Reviewer-Rolle: erfahrener Home-Assistant-Architekt und Architekt modularer Systeme
- Repos:
  - herbertschrotter-blip/claude-skills-bpm
  - herbertschrotter-blip/HA_Dash_DreameX60
- Kontext:
  - docs/ha-grundsatz/
  - Referenzfall nach Bedarf
- Pflicht-Block: |
    <heutiger Rahmen-Block aus CLAUDE.md>
- Ergebnis-Orte:
  - docs/ha-grundsatz/
  - skills/modul-bauplan/
```

Damit ist die thematische Mehrdimensionalität nicht mehr künstlich in einzelne Profilzeilen gepresst.

---

# 4. Projekt-Configs – endgültige Orte

Verbindlicher Pfad in **jedem Projekt-Repo**:

```text
.claude/
└── skill-config/
    ├── tracker.md
    ├── ticket.md
    └── review.md
```

Nur benötigte Dateien existieren.

## `tracker.md`

Struktur:

```markdown
# Tracker-Konfiguration

## Provider

## Nummernschema

## Nächste freie Nummer

## Listen und Routing

## Statusmodell

## Felder und Option-IDs

## Titel-/Beschreibungsformat

## Quittungsformat

## Sonderfälle
```

`Nächste freie Nummer` liegt **nur hier**. K5 ist damit umgesetzt.

## `ticket.md`

```markdown
# Ticket-Konfiguration

## Quelle

## Lese-/Schreibweg

## Statusmodell

## Pflichtfelder je Status

## Tracker-Kopplung

## Beweisquellen

## Doku-Kopplung

## Schließen / Verifikation
```

## `review.md`

Wie oben:

```markdown
# Review-Konfiguration

## Allgemein

## Thema: <name>
...
```

Mehrere Themen sind ausdrücklich vorgesehen.

---

# 5. Umzug `projects/bpm/`

Die jetzige Datei `projects/bpm/clickup-lists.md` mischt tatsächlich zwei Projekte:

- BauProjektManager
- Claude-Skills-Entwicklung / Skill Issues.

Das wird getrennt.

## Nach `BauProjektManager`

Ziel:

```text
BauProjektManager/
└── .claude/
    └── skill-config/
        └── tracker.md
```

Dorthin wandern aus `projects/bpm/`:

- BPM Space
- die 17 BPM-Listen
- BPM Custom Fields
- Modul-Kürzel
- BPM Statusmodell
- BPM Nummernschema
- BPM Next
- BPM Ankerregeln, soweit weiterhin benutzt.

## Nach `claude-skills-bpm`

Ziel:

```text
claude-skills-bpm/
└── .claude/
    └── skill-config/
        └── tracker.md
```

Dorthin wandern:

- Space `Claude Skills Entwicklung`
- Liste `ClaudeSkills`
- Skill-Issues-Listen
- Skill-Issue Custom Fields
- Skill-Issue Nummernschema
- Statuswerte
- nächste Nummern/Zähler.

## Was nicht mitwandert

`projects/bpm/memory-format.md` wird **nicht** als Projektconfig übernommen.

Cowork-spezifisches Memory-Verhalten wandert, soweit noch gebraucht, in den Cowork-Kontext von `chat-wechsel` bzw. `cc-steuerung`. Veraltete `[PROJECT]`-/`[CLICKUP]`-Mechanik entfällt, sobald die Projekt-Config im jeweiligen Repo die Wahrheit ist.

---

# 6. Umzug `projects/heidi/`

Nicht blind kopieren: der Ordner ist bereits gegenüber `HA_Dash_DreameX60` abgedriftet.

Deshalb:

```text
HA_Dash_DreameX60/
└── .claude/
    └── skill-config/
        ├── tracker.md
        ├── ticket.md
        └── review.md     # nur wenn Review für Heidi weiter verwendet wird
```

Quelle für den Neuaufbau:

1. heutige `HA_Dash_DreameX60/CLAUDE.md`
2. heutige Projektdoku
3. tatsächliche ClickUp-Struktur
4. erst danach die alten Dateien `projects/heidi/*` als Migrationshilfe.

`projects/heidi/*` ist **keine** Source of Truth mehr.

Nach erfolgreichem Abgleich und Profil-Umstellung werden:

```text
projects/bpm/
projects/heidi/
```

aus dem Skill-Repo entfernt.

K7 ist damit umgesetzt: **umziehen und aufteilen, nicht Daten vernichten**.

---

# 7. `cc-steuerung` – Cowork-Adapter

## 7.1 Fertige Description

```yaml
description: >
  Steuert Desktop Commander ausschließlich im Claude.ai-Cowork-Chat für
  ausdrücklich gewünschte Datei-, Verzeichnis- und Terminaloperationen auf
  dem lokalen PC. Use when the user explicitly requests "dc", "Desktop
  Commander", "direkt auf dem PC per DC", or uses "cc" in Cowork as the
  established Desktop-Commander shorthand. Do not trigger in Claude Code,
  even when the user says "Claude Code", "commit", "build", "git", "auf
  Platte", or requests normal repository work there. Do not trigger for
  planning, explanations, code shown only in chat, or local execution that
  was not explicitly requested through Desktop Commander.
```

Deutlich unter 1024 Zeichen.

Wichtig: **Diese Description wird erst nach der Baseline geändert.**

## 7.2 Zielkern

Etwa 80–120 Zeilen.

Gliederung:

```markdown
# cc-steuerung — Cowork/Desktop-Commander-Adapter

## Zweck
- Nur Cowork.
- Nur ausdrücklich gewünschter Desktop Commander.
- Kein Fachskill.
- In Claude Code nie anwenden.

## Trigger-Grenze
- positive Beispiele
- negative Beispiele
- "cc" nur im Cowork-Kontext

## Verhältnis zu Fachskills
- Fachskill bestimmt WAS.
- cc-steuerung bestimmt nur lokale DC-Ausführung.
- keine Fachregeln duplizieren.

## Ausführung
1. Prüfen, ob Desktop Commander verfügbar ist.
2. Zielpfad verwenden, wenn eindeutig bekannt.
3. Wenn Zielpfad fehlt: einmal danach fragen.
4. Nur die ausdrücklich angeforderte lokale Operation ausführen.
5. Ergebnis/Folgefehler melden.

## Sicherheit
- keine Secrets
- keine Aktion außerhalb des ausdrücklich gewünschten Scopes
- Löschen nur nach echter Freigabe
- Push nur gemäß Skill-Profil des Projekts

## Integration
- konkrete Desktop-Commander-Werkzeuge:
  siehe references/desktop-commander.md

## VERBOTEN
- in Claude Code triggern
- OneDrive-/PC-Pfade raten
- PCs selbst registrieren
- Fachregeln ersetzen
- eigene Push-Regel
```

## 7.3 References

Nur:

```text
skills/cc-steuerung/
├── SKILL.md
└── references/
    └── desktop-commander.md
```

`desktop-commander.md` enthält:

- vollqualifizierte MCP-Werkzeugnamen,
- Lese-/Schreib-/Terminal-Zuordnung,
- bekannte PowerShell-Eigenheiten,
- Verhalten bei nicht verfügbarem MCP,
- optional kurze Pfad-Hinweise.

Anthropic empfiehlt konkrete MCP-Namen vollständig qualifiziert anzugeben.

## 7.4 Ersatzlos löschen

Aus dem heutigen Skill:

- OneDrive-Autodiscovery
- `hostname` + OneDrive-Kombination
- PC-Registry
- INDEX-Abschnitt `PCs und Arbeitsverzeichnisse`
- Self-Registration unbekannter PCs
- allgemeine Branch-Ermittlung
- allgemeine Git-Regeln
- „User pusht immer selbst“
- „User testet selbst“
- generischer Plan-vs-Direkt-Workflow
- „DC Default nach ok/passt/mach“
- Claude-Code-Trigger
- allgemeine Artifact-Separation
- Fachskill-Ausgabeformate
- historische Incident-IDs und Session-Verweise.

---

# 8. Was in vier Fachskills wegen cc-steuerung entfällt

Ich habe die aktuellen Dateien auf `main` geprüft.

## `audit`

Aktuell:

```text
Cowork: bei DC-Operationen Arbeitsverzeichnis nach cc-steuerung Kapitel 4 ermitteln.
```

→ **ersatzlos entfernen.**

Audit braucht keine eigene lokale Pfadlogik.

## `code-erstellen`

Aktuell betroffen:

- Verweis auf `cc-steuerung Kapitel 4`
- `$pc = hostname`
- OneDrive-Ermittlung
- `workFolder`
- Self-Registration
- `Test-Path`
- `$env:OneDrive`-Sonderregeln.

Der ganze Block wird entfernt.

Künftig:

> Claude Code arbeitet in der aktuellen Repo-Wurzel. Cowork schreibt lokal nur, wenn der User ausdrücklich Desktop Commander verlangt; die Ausführung übernimmt cc-steuerung.

Mehr braucht `code-erstellen` nicht.

## `doc-pflege`

Aktuell:

> Cowork: bei DC-Operationen Arbeitsverzeichnis nach cc-steuerung Kapitel 4 ermitteln.

→ entfernen.

Ein kurzer Satz zur Liefermodalität reicht.

## `mockup-erstellen`

Entfernen:

- Verweis `cc-steuerung Kapitel 4`
- lokale `workFolder`-Mechanik
- Toolnamen im Kern, soweit nur Cowork-Ausführung beschrieben wird.

Schritt „auf Platte speichern“ wird neutral:

> In Claude Code in die Ablage des Mockup-Profils schreiben. Im Cowork-Chat lokale Speicherung nur nach ausdrücklichem Desktop-Commander-Auftrag.

Keine nummerierte Cross-Skill-Abhängigkeit mehr.

---

# 9. INDEX.md – neue Aufgabe

INDEX ist künftig **Routing-Registry**, nicht zweites Regelbuch.

## Zielgliederung

```markdown
# INDEX — Skill-Routing

## 1. Aktive Skills
Tabelle der 12 Skills

## 2. Geplante Skills
- modul-bauplan

## 3. Routing-Grundsätze
- Description entscheidet Discovery
- Fachskill = WAS
- Adapter = Integrations-/Umgebungsausführung
- Projektwerte aus Skill-Profil/Config

## 4. Konfliktpaare
interne Skills

## 5. Externe Konfliktpaare
skill-creator ↔ skill-neu
skill-creator ↔ skill-pflege
code-review ↔ audit

## 6. Geplantes Konfliktpaar
modul-bauplan ↔ audit

## 7. Regelquellen
Skill-Profil
Skill-Qualität
SKILL.md
References
Projekt-Configs
Eval-Suite

## 8. Test-/Validierungsquellen
tools/validate-skills.ps1
quality/evals/
Real-Environment-Golden-Tests
```

## Inventartabelle

Beispiel:

| Skill | Zuständigkeit | Nicht zuständig | Konfig |
|---|---|---|---|
| audit | read-only systemweite Konsistenz | Änderungen | Skill-Profil |
| cc-steuerung | Cowork-DC-Adapter | Claude Code, Fachlogik | — |
| code-erstellen | Anwendungscode ändern | Mockups, reine Doku, read-only Audit | Code-Profil |
| doc-pflege | Doku schreiben/ändern | read-only Prüfung | Doku-Profil |
| ticket | Ticket-Lifecycle | freie Bugfixes ohne Ticket | Ticket.Config |
| tracker | Aufgabenmutationen | freie Planung | Tracker.Config |

## Konfliktpaare

Neu zwingend:

```text
audit ↔ doc-pflege
audit ↔ modul-bauplan
skill-neu ↔ skill-pflege
skill-neu ↔ skill-creator
skill-pflege ↔ skill-creator
audit ↔ code-review
cc-steuerung ↔ alle Fachskills
```

Bei externen Skills steht ausdrücklich:

> Automatischer `plugin eval` deckt diese Konkurrenz nicht vollständig ab; Prüfung im Real-Environment-Golden-Set.

Denn `plugin eval` startet isolierte Sessions ohne persönliche Skills, andere Plugins, Projekt-CLAUDE oder Memory.

---

# 10. Die alten INDEX-Invarianten 1–10

| Alt | Inhalt | Neuer Ort |
|---|---|---|
| 1 | `ask_user_input_v0` bei Entscheidungen | **alte Regel löschen**; kleine globale Regel: nur fragen, wenn Entscheidung offen; bei festen Optionen Auswahlfunktion der Umgebung |
| 2 | Branch immer auswählen | **Skill-Profil → Branch-Policy** |
| 3 | DC-Pfade/PowerShell | alte globale Regel löschen; nur relevante DC-Technik nach `cc-steuerung/references/desktop-commander.md` |
| 4 | Frühphasen-Prinzip | als globale Regel löschen; projektspezifisch über `Code.Architekturregeln` bzw. `Modul.Grundsatzregeln` |
| 5 | additive Skill-Änderungen | `skill-pflege`: Safe Patch / Refactor + Inventar |
| 6 | Pro-Task-Quittung | `tracker` bzw. `references/batch-protocol.md` |
| 7 | Memory-Rubriken | Cowork-spezifische Reference bei chat-wechsel; nicht globale Skill-Invariante |
| 8 | Two-Place | `skill-pflege/references/delivery.md`; skill-neu nutzt denselben Governance-Grundsatz |
| 9 | cc parallel zu Fachskills | alte Regel löschen; INDEX-Konfliktpaar + neue cc-Description |
| 10 | Fragilitäten/Frühwarnung | aus INDEX entfernen; relevante Fälle in Evals/Skill-Qualität überführen, historische Doku archivisch behalten |

Damit enthält INDEX keine operative Regelkopie mehr.

---

# 11. README.md

README wird nur Onboarding.

Neue Kernbotschaft:

```text
Dieses Repo enthält 12 aktive projektneutrale Skills,
ihre Qualitäts-/Eval-Infrastruktur und Referenzdokumentation.
Projektwerte liegen in der CLAUDE.md und unter
.claude/skill-config/ des jeweiligen Projekt-Repos.
```

README enthält:

- Zweck
- Verzeichnisstruktur
- 12 Skills als grobe Übersicht
- Source-of-Truth-Tabelle
- Entwicklungs-/Testworkflow
- Distribution via claude.ai
- Verweis auf INDEX
- Verweis auf Skill-Profil v1
- Verweis auf Qualität/Evals.

Entfallen:

- „11 Skills“
- „BPM-spezifische Skills“
- `projects/<name>/` als Architektur
- ausführliche operative Invarianten
- `test-prompts.md` als Testsystem.

---

# 12. `docs/project-architecture.md`

Nicht weiterpflegen.

Vorgehen:

```text
git mv docs/project-architecture.md docs/skill-profile-v1.md
```

und den Inhalt komplett als **Skill-Profil-v1-Spezifikation** neu aufbauen.

Das ist ein Refactor, kein Safe Patch.

Git bewahrt die Historie; ein zusätzlicher Redirect ist nicht nötig.

---

# 13. `docs/skill-quality.md`

Neue zentrale Qualitätsquelle.

Gliederung:

```markdown
# Skill-Qualität

## Verbindliche Qualitätsregeln

### Neutralität
- Handlung statt Integrationsdetail
- Projektwerte außerhalb generischer Skills
- Fallback nie raten
...

### Anthropic Skill Authoring
- Description was + wann
- <=1024 Zeichen
- SKILL.md Ziel <500 Zeilen
- direkt referenzierte References
- Reference >100 Zeilen mit Inhaltsverzeichnis
- keine aktive Historie
- Terminologie konsistent
- Freiheitsgrad passend zur Fragilität
...

## Skill-Prüfung

### Mechanisch
tools/validate-skills.ps1

### Semantisch
audit

### Verhaltensmessung
plugin eval / skill-creator / Golden Sessions

## Dokumentationsregeln

...
```

Damit muss `skill-neu` die Theorie nicht mehr hundert Zeilen lang lehren.

---

# 14. Prüfskript

## Sprache

**PowerShell 7.**

Grund:

- auf dem aktuellen Büro-PC verfügbar,
- keine neue Python-Installation,
- ausreichend für Text-/JSON-/Dateisystemchecks,
- passend zu Herberts Windows-/Claude-Code-Umgebung.

`quick_validate.py` bleibt Referenz für Regeln, aber keine Runtime-Abhängigkeit.

## Ort

```text
tools/validate-skills.ps1
```

## Aufruf

```powershell
pwsh -NoProfile -File tools/validate-skills.ps1
```

optional:

```powershell
pwsh -NoProfile -File tools/validate-skills.ps1 `
  -JsonPath quality/results/skill-validation.json
```

## JSON

```json
{
  "schemaVersion": 1,
  "status": "pass",
  "summary": {
    "skills": 12,
    "errors": 0,
    "warnings": 4
  },
  "skills": [
    {
      "name": "audit",
      "lines": 320,
      "descriptionLength": 526,
      "errors": [],
      "warnings": []
    }
  ]
}
```

## Exit-Codes

```text
0 = keine Errors; Warnungen erlaubt
1 = mindestens ein Qualitätsfehler
2 = Validator selbst konnte nicht korrekt laufen
```

## Fehler

Mechanisch eindeutig und künftig merge-blockierend:

- SKILL.md ohne Frontmatter
- `name` fehlt/ungültig
- `description` fehlt
- Description >1024
- XML-/spitze-Klammer-Verstoß in Frontmatter gemäß Skill-Schema
- lokaler Markdown-Reference-Link zeigt auf nicht vorhandene Datei
- Skillname doppelt
- unbekannte Profil-Version
- benötigte zentrale Datei des Skill-Repos fehlt
- `projects/<name>/` nach abgeschlossener Migration wieder in einem Skill als Configquelle verwendet
- `test-prompts.md` nach abgeschlossener Eval-Migration neu eingeführt.

## Warnungen

- SKILL.md ≥500 Zeilen
- Reference >100 Zeilen ohne Inhaltsverzeichnis
- Windows-Pfad im generischen Skill
- Historienmarker im aktiven Regeltext
- Datums-/Versions-/Session-Marker
- `ask_user_input_v0`, `present_files`, `SendUserFile`, `Desktop Commander` usw. außerhalb erlaubter Cowork-/Delivery-References
- nummerierte Cross-Skill-Verweise wie `Regel 21`, `Kapitel 4`
- Cross-Skill-Verweis auf eine Überschrift, die nicht gefunden wird
- Begriffe `BPM`, `Heidi`, konkrete Projektpfade in generischen Regelabschnitten
- Description enthält projektspezifische Zuständigkeit
- kein Evalfall für einen Skill
- kein `Do not trigger`-Teil, solange diese Repo-Konvention beibehalten wird.

Einige dieser Warnungen können nach Abschluss des Refactors zu Errors hochgestuft werden.

---

# 15. Plugin-Manifest für die Evals

Anthropic erlaubt `.claude-plugin/plugin.json` am Plugin-Root; `version` ist optional. Für den reinen lokalen Test-Harness würde ich **keine zweite Versionsquelle einführen**.

Datei:

```text
.claude-plugin/plugin.json
```

Inhalt:

```json
{
  "name": "herbert-skills-eval",
  "description": "Local evaluation harness for Herbert's Claude skill collection",
  "author": {
    "name": "Herbert Schrotter"
  },
  "experimental": {
    "evals": "quality/evals"
  }
}
```

`experimental.evals` ist offiziell für den Fall vorgesehen, dass `evals/` bereits anderweitig belegt ist.

Damit bleibt der alte Ordner zunächst unberührt:

```text
evals/
```

und die neue native Suite lebt in:

```text
quality/evals/
```

Nach erfolgreicher Migration kann das alte Eval-System archiviert/entfernt werden.

---

# 16. Eval-Pilot – fünf Fälle

## Struktur

```text
quality/evals/
├── audit-readonly/
├── doc-write/
├── code-implement/
├── skill-update/
├── cc-not-in-claude-code/
└── results/                 # gitignore
```

Alle fünf bekommen:

```yaml
---
tags: [pilot]
runs: 3
max_turns: 4
allowed_tools: [Skill, Read, Glob, Grep]
---
```

Anthropic dokumentiert diese Felder für `prompt.md`; der Default für Runs wäre ohnehin 3.

---

## Fall 1 — `audit-readonly/prompt.md`

```markdown
---
tags: [pilot, critical, routing]
runs: 3
max_turns: 4
allowed_tools: [Skill, Read, Glob, Grep]
---

Prüfe bitte, ob INDEX.md und die Skill-Beschreibungen konsistent sind.
Nur prüfen und Befunde nennen, nichts reparieren.
```

`graders/audit-fired.md`:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?audit"'
---
```

`graders/doc-not-fired.md`:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?doc-pflege"'
min: 0
max: 0
---
```

---

## Fall 2 — `doc-write/prompt.md`

```markdown
---
tags: [pilot, critical, routing]
runs: 3
max_turns: 4
allowed_tools: [Skill, Read, Glob, Grep]
---

Pflege die Projektdokumentation: Aktualisiere den Architekturabschnitt
nach einer bereits umgesetzten Änderung und schreibe den neuen Stand
in die passende Doku.
```

`doc-fired.md`:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?doc-pflege"'
---
```

`audit-not-fired.md`:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?audit"'
min: 0
max: 0
---
```

---

## Fall 3 — `code-implement/prompt.md`

```markdown
---
tags: [pilot, routing]
runs: 3
max_turns: 4
allowed_tools: [Skill, Read, Glob, Grep]
---

Implementiere eine Recovery-Logik für einen fehlgeschlagenen Dateiimport
und ergänze die passenden Tests.
```

`code-fired.md`:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?code-erstellen"'
---
```

Dieser Fall ist absichtlich nahe einem alten Fehlfall.

---

## Fall 4 — `skill-update/prompt.md`

```markdown
---
tags: [pilot, critical, routing]
runs: 3
max_turns: 4
allowed_tools: [Skill, Read, Glob, Grep]
---

Ergänze im bestehenden chat-wechsel-Skill eine Regel, dass tote
Dateiverweise vor der Übergabe gemeldet werden.
```

`pflege-fired.md`:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?skill-pflege"'
---
```

`neu-not-fired.md`:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?skill-neu"'
min: 0
max: 0
---
```

---

## Fall 5 — `cc-not-in-claude-code/prompt.md`

```markdown
---
tags: [pilot, critical, routing]
runs: 3
max_turns: 4
allowed_tools: [Skill, Read, Glob, Grep]
---

Ich bin in Claude Code. Zeig mir bitte den Git-Status des aktuellen Repos.
```

`cc-not-fired.md`:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?cc-steuerung"'
min: 0
max: 0
---
```

Der `tool_used`-Grader unterstützt `min: 0` und `max: 0` ausdrücklich als „Tool darf nie aufgerufen werden“.

Dieser Fall **darf vor dem Refactor scheitern**. Das wäre ein bestätigter Baseline-Befund, kein Fehler des Piloten.

---

# 17. Pilotlauf

## Preflight

```powershell
claude --version
claude plugin validate .
pwsh -NoProfile -File tools/validate-skills.ps1
```

`plugin eval` benötigt laut aktueller Dokumentation Claude Code 2.1.269 oder neuer.

## Pilot

```powershell
claude plugin eval . `
  --tag pilot `
  --runs 3 `
  --ablation none `
  --no-publish
```

Kein `--max-cost-usd` nötig.

K8 ist bestätigt: der Wert begrenzt nur die geschätzten Listenpreiskosten; reale Runs zählen trotzdem gegen das jeweilige Plan-Kontingent.

Falls Herbert trotzdem eine zusätzliche Notbremse möchte, kann sie genutzt werden; sie schützt aber **nicht direkt** sein Abo-Kontingent.

---

# 18. Protokoll für echte Sitzungen mit Anthropic-Skills

`plugin eval` lädt nur das getestete Plugin; persönliche Skills, andere Plugins, CLAUDE.md und Memory fehlen.

Darum getrennt:

```text
quality/real-environment/
└── YYYY-MM-DD.md
```

Format:

```markdown
# Real Environment Routing – YYYY-MM-DD

- Claude-Code-Version:
- Modell:
- aktive externe Skills:
- Skill-Repo-Stand:

| ID | Prompt | Erwartet | Tatsächlich geladen | Ergebnis | Notiz |
|---|---|---|---|---|---|
| EXT-01 | ... | skill-neu | ... | PASS/FAIL | ... |
```

Pflichtfälle:

```text
EXT-01 skill-creator ↔ skill-neu
EXT-02 skill-creator ↔ skill-pflege
EXT-03 code-review ↔ audit
EXT-04 modul-bauplan ↔ audit   # sobald modul-bauplan aktiv ist
EXT-05 cc-steuerung in Claude Code darf nicht triggern
```

Je Prompt drei frische Sitzungen, wenn er als kritischer Konflikt in die endgültige Freigabe eingeht.

---

# 19. Phase 1 – konkrete Dateiliste

Wichtig: **Keine Skill-Description wird vor dem Pilot geändert.**

## Schritt 1A – Test-/Qualitätsinfrastruktur

| Reihenfolge | Datei | Aktion | Art |
|---:|---|---|---|
| 1 | `.claude-plugin/plugin.json` | Test-Harness anlegen | Neu |
| 2 | `quality/evals/...` | 5 Pilotfälle anlegen | Neu |
| 3 | `.gitignore` | `quality/evals/results/`, `quality/results/` | Safe Patch |
| 4 | `tools/validate-skills.ps1` | mechanischen Validator anlegen | Neu |
| 5 | `docs/skill-quality.md` | zentrale Qualitätsquelle | Neu |
| 6 | `docs/project-architecture.md` → `docs/skill-profile-v1.md` | umbenennen + vollständig neu strukturieren | Refactor |

### Abnahme

- Plugin validiert.
- Validator läuft ohne Laufzeitfehler.
- Pilotfälle werden gefunden.
- keine SKILL.md verändert.

---

## Schritt 1B – Skill-Repo-Profil und Config

| Datei | Änderung | Art |
|---|---|---|
| `CLAUDE.md` | `## Skill-Profil` einfügen | Safe Patch |
| `.claude/skill-config/review.md` | heutiges Review-Profil auslagern | Neu |
| `.claude/skill-config/tracker.md` | Claude-Skills-/Skill-Issue-Config übernehmen | Neu |
| `CLAUDE.md` | altes `## Review-Profil` nach erfolgreichem Umzug entfernen | Refactor |

Kein Versionsbump.

Commit bleibt auf aktueller Skill-Version `v0.36.9`.

Push unmittelbar nach Commit gemäß `required-after-commit`.

---

## Schritt 1C – Projektconfigs

### BPM

Neu:

```text
BauProjektManager/.claude/skill-config/tracker.md
```

`CLAUDE.md` bekommt den Skill-Profil-v1-Block.

### Heidi

Neu:

```text
HA_Dash_DreameX60/.claude/skill-config/tracker.md
HA_Dash_DreameX60/.claude/skill-config/ticket.md
HA_Dash_DreameX60/.claude/skill-config/review.md   # wenn genutzt
```

`CLAUDE.md` bekommt Skill-Profil v1.

Bei Heidi müssen K6-Werte beim tatsächlichen Einbau noch mit Herbert bzw. der heutigen Projektstruktur validiert werden; insbesondere Tracker-Next, Pflichtdocs und Review-Themen dürfen nicht aus der alten `projects/heidi/`-Config ungeprüft übernommen werden.

---

## Schritt 1D – Repository-Doku

Vor Baseline erlaubt:

| Datei | Änderung |
|---|---|
| `README.md` | 11→12, neue Profil-/Config-Architektur, altes `projects/`-Modell entfernen |
| `INDEX.md` | nur faktische Drift beheben, **noch keine Description-basierte neue Routingsemantik** |
| `docs/skill-profile-v1.md` | neue Regelquelle |
| `docs/skill-quality.md` | neue Qualitätsspezifikation |

Der komplette INDEX-Refactor kann auch unmittelbar **nach** dem Pilot erfolgen, wenn maximale Baseline-Reinheit gewünscht ist.

Ich bevorzuge das.

---

# 20. Was ausdrücklich erst nach der Baseline kommt

Keine Änderungen vorher an:

```text
skills/*/SKILL.md descriptions
```

Insbesondere nicht:

- `cc-steuerung` Description
- `audit` Description
- `doc-pflege` Description
- `code-erstellen` Description
- `skill-pflege` Description
- `skill-neu` Description.

Ebenfalls erst danach:

- `cc-steuerung` Refactor
- `skill-pflege` Safe-Patch/Refactor-Neubau
- `skill-neu` Kürzung
- doc-pflege Modi 3/4/6 entfernen
- Projektbegriffe aus Descriptions entfernen
- große Progressive-Disclosure-Schnitte.

Damit ist S5 strikt eingehalten.

---

# 21. Was Herbert selbst tun muss

Nur drei Dinge.

## Nach Pilot

Herbert entscheidet:

> Volle 60-Fall-Grundmessung: ja/nein.

## Nach jeder Skill-Änderung

Claude Code kann Repo, Commit und Push selbst erledigen.

Herbert muss anschließend die neue SKILL.md bzw. Zip **bei claude.ai hochladen/ersetzen**.

Two-Place bleibt deshalb zwingend.

## Real-Environment-Tests

Herbert muss die frischen Claude-Code-Sitzungen starten bzw. die Prompts ausführen, soweit dies nicht zuverlässig automatisiert werden kann.

---

# 22. Gesamtplan Phasen 1–7

## Phase 1 — Wahrheitsquellen und Infrastruktur

- [ ] `Skill-Profil v1` spezifizieren
- [ ] `docs/skill-quality.md`
- [ ] Validator PowerShell 7
- [ ] Plugin-Manifest
- [ ] 5 Pilotfälle
- [ ] Config-Zielstruktur anlegen
- [ ] offensichtliche README/INDEX-Drift dokumentieren
- [ ] keine Skill-Descriptions ändern

**Abnahme:** Validator und `plugin validate` funktionieren; Pilot ist startbar.

---

## Phase 2 — Profile und Projektconfig

- [ ] Skill-Repo `Skill-Profil v1`
- [ ] Skill-Repo Tracker-/Review-Config
- [ ] BPM Skill-Profil + Tracker-Config
- [ ] Heidi Skill-Profil + Tracker-/Ticket-/Review-Config
- [ ] Werte aus `projects/bpm` sauber aufteilen
- [ ] `projects/heidi` gegen heutigen Stand neu aufbauen
- [ ] `projects/` erst nach erfolgreichem Gegencheck entfernen
- [ ] keine doppelten Projektwerte mehr

**Abnahme:** alle drei Repos bestehen Profil-/Config-Validierung; keine benötigte Config zeigt mehr auf `projects/<name>/`.

---

## Phase 3 — Baseline

- [ ] 5×3 Pilot durchführen
- [ ] Befunde dokumentieren
- [ ] Herbert entscheidet Full Baseline
- [ ] bei Freigabe: 60 Fälle aufbauen
- [ ] 3 Läufe pro Fall
- [ ] kritische Konflikte 3/3
- [ ] normale Fälle 2/3
- [ ] Real-Environment-Golden-Set für Anthropic-Skills

**Abnahme:** unveränderte alte Skills sind vermessen; Baseline eingefroren.

---

## Phase 4 — Governance-Skills

### `skill-pflege`

- [ ] Safe Patch
- [ ] Refactor
- [ ] Regel-Inventar
- [ ] KEEP/MOVE/MERGE/REWRITE/DROP/NEW
- [ ] bidirektionaler Abgleich
- [ ] Sammelfreigabe DROP
- [ ] stabile Datei+Überschrift-Verweise
- [ ] `references/delivery.md`
- [ ] Validator als Pflichtabschluss
- [ ] Eval-Gate.

### `skill-neu`

- [ ] Lehrbuchteile entfernen
- [ ] Governance-Workflow behalten
- [ ] neue Qualitätsquelle verwenden
- [ ] zentrale Eval-Suite statt `test-prompts.md`
- [ ] Konfliktprüfung inkl. externen Skills.

**Abnahme:** künftige Refactors können Text entfernen/zusammenführen, ohne unkontrollierten Regelverlust.

---

## Phase 5 — Querschnitt bereinigen

- [ ] `cc-steuerung` → Cowork-Adapter
- [ ] OneDrive/PC-Registry entfernen
- [ ] cc-Verweise aus audit/code/doc/mockup entfernen
- [ ] Fragepflicht ersetzen
- [ ] Branch-Policy ins Profil
- [ ] Push-Policy aus Fachskills
- [ ] alte INDEX-Invarianten auflösen
- [ ] INDEX als Routing-Registry neu
- [ ] `audit ↔ doc-pflege ↔ modul-bauplan` festziehen
- [ ] betroffene Descriptions erst jetzt ändern
- [ ] nach jeder Description-Änderung dieselben Baselinefälle erneut laufen lassen.

**Abnahme:** keine globale Regelkopie mehr; kein cc-Trigger in Claude Code.

---

## Phase 6 — Skill für Skill verkleinern

Priorität:

1. skill-pflege – schon Phase 4
2. mockup-erstellen
3. chat-wechsel
4. chatgpt-review
5. skill-neu – schon Phase 4
6. code-erstellen
7. doc-pflege
8. tracker
9. audit
10. git-commit-helper
11. ticket
12. cc-steuerung – schon Phase 5.

Pro Skill:

- [ ] Regel-Inventar
- [ ] Refactor
- [ ] <500 Ziel
- [ ] History raus
- [ ] References mit TOC >100 Zeilen
- [ ] Projektwerte raus
- [ ] Cross-Refs semantisch
- [ ] Validator
- [ ] relevante Evals
- [ ] Commit + Push
- [ ] Herbert Upload claude.ai.

**Abnahme:** kein Skill schlechter als seine relevante Baseline.

---

## Phase 7 — Gesamtabnahme

- [ ] alle 60 Routingfälle
- [ ] kritische Fälle 3/3
- [ ] normale Fälle ≥2/3
- [ ] Real-Environment-Golden-Set
- [ ] skill-creator auf die kritischen Einzel-Skills
- [ ] Validator ohne Error
- [ ] alte `test-prompts.md` entfernt
- [ ] `references.zip` entfernt
- [ ] `projects/` entfernt
- [ ] README/INDEX aktuell
- [ ] keine toten Querverweise
- [ ] alle aktiven Projekt-Repos Profil v1
- [ ] finale Version/CHANGELOG nur für tatsächliche Skill-Änderungen.

**Abnahme:** neues Skillsystem ist Source-of-Truth-konsistent, messbar und ohne bekannte P0/P1-Architekturbrüche.

---

# 23. Ein Punkt, den ich gegenüber Runde 2 korrigiere

Meine Aussage, `references/stacks/<key>.md` müsse wegen der Ordnertiefe verschoben werden, war falsch.

K1 ist richtig.

Anthropic warnt vor **verschachtelten Verweisketten**, nicht vor einem Unterordner an sich. SKILL.md darf direkt auf `reference/finance.md` oder analog `references/stacks/python.md` zeigen.

Die Stack-Struktur bleibt daher unverändert.

---

# ✅ Einigkeit

- K1–K9 werden übernommen.
- PowerShell 7 statt Python für den Validator.
- Projektwerte liegen im Projekt-Repo.
- Tracker-/Ticket-/Review-Config unter `.claude/skill-config/`.
- Review erhält eine eigene mehrthemenfähige Config.
- Zähler liegen in Tracker-Config.
- Skill-Profil enthält Werte einmal; lange Regelwerke per `ref:`.
- Skill-Repo pusht nach jedem Commit automatisch.
- Nur Skill-Änderungen erhöhen die Version und schreiben CHANGELOG.
- Two-Place bleibt wegen claude.ai-Verteilung.
- `cc-steuerung` wird reiner Cowork-Adapter.
- Baseline vor Description-Änderungen.
- fünf Pilotfälle zuerst.
- kein 13. Analyse-Skill.
- `plugin eval` = Routing; `skill-creator` = Einzel-Skill-Qualität; audit = semantisches Urteil; PowerShell-Validator = Mechanik.

# ⚠️ Widerspruch / Präzisierung

- Der heutige große INDEX darf **nicht komplett vor der Baseline semantisch umgeschrieben werden**, wenn wir eine möglichst saubere Vorhermessung wollen. Faktische Korrekturen sind unkritisch; der neue Routing-INDEX sollte unmittelbar nach dem Pilot bzw. nach eingefrorener Baseline kommen.
- `projects/heidi` darf nicht einfach verschoben werden. Es muss aus dem heutigen `HA_Dash_DreameX60` neu rekonstruiert und nur gegen die alte Config gegengeprüft werden.
- `--max-cost-usd` ist für Herberts Abo kein Budgetschutz; höchstens eine zusätzliche Abbruchschwelle nach Listenpreisschätzung.
- `references/stacks/` bleibt; meine Runde-2-Kritik dazu ist zurückgenommen.

# ❓ Rückfragen

Keine grundsätzliche Architekturfrage ist mehr offen.

Beim tatsächlichen Einbau müssen nur noch konkrete Projektwerte verifiziert werden – vor allem aktuelle ClickUp-Zähler, Heidi-Trackerfelder und ggf. Heidi-Review-Themen. Das sind Implementierungsdaten, keine offenen Architekturentscheidungen.

**Serie abschließbar.**
