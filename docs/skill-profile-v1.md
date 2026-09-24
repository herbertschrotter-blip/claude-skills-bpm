# Skill-Profil v1

Das Skill-Profil ist der Vertrag zwischen den projektneutralen Skills und einem Projekt: Es hält die Werte, die die Skills
brauchen, genau einmal – im Block `## Skill-Profil` der `CLAUDE.md` des Projekt-Repos. Große, veränderliche Strukturen
(Tracker, Tickets, Reviews) liegen als Config-Dateien unter `.claude/skill-config/` im selben Repo. Entstanden in der
Review-Serie [CGR-2026-09-24-skillsystem](./chatgpt-reviews/CGR-2026-09-24-skillsystem/README.md); Qualitätsregeln der Skills:
[skill-quality.md](./skill-quality.md).

## Inhalt

- Grundregeln
- Schema
- Checks
- Pflichtfelder je Skill
- Fehlende Werte
- Configs unter `.claude/skill-config/`
- Prüfung
- Einführung in den Repos

## Grundregeln

1. **Werte genau einmal.** Ein Wert (Versionsquelle, Push-Policy, Testbefehl, Branch …) steht nur im Profil. Prosa in der
   CLAUDE.md verweist darauf oder entfällt.
2. **Regelwerke per Verweis.** Lange Regeln (Architektur, Validierung, Sitzungsabschluss) bleiben in ihrer Doku; das Profil
   verweist mit `ref:<pfad>#<überschrift>`.
3. **Drei besondere Werte:**
   - `none` – bewusst nicht vorhanden. Das ist gültig.
   - `fehlt` – müsste vorhanden sein, ist aber noch nicht definiert. Blockiert jeden Skill, der das Feld braucht.
   - `ref:` – das Regelwerk steht an anderer Stelle.
4. **Version.** `Profil-Version: 1` ist die einzige gültige Version. Ein Skill, der eine andere Version findet, arbeitet
   nicht weiter.
5. **Kein zweites Handbuch.** Das Profil beschreibt die Arbeit im Repo, nicht das Projekt. Fachliche Moduldaten gehören in
   die Doku des Projekts, bei Home-Assistant-Modulen in `module.yaml` (Serie CGR-2026-09-23-ha-grundsatz).
6. **Pfade** mit `/`, relativ zur Repo-Wurzel.

## Schema

```markdown
## Skill-Profil

- Profil-Version: 1
- Projekt-ID: <slug>
- Repo: <owner/repo>
- Branch-Policy: current | fixed:<branch>

### Checks
- <check-name>: <befehl; befehl> [<pfad-glob>; <pfad-glob>]

### Commit
- Format: <format>
- Module: <name=scope; name=scope>
- Versionsquelle: none | <pfad>#<feld> | changelog:<pfad>
- Versionsregel: none | <kurzregel> | ref:<pfad>#<überschrift>
- Push-Policy: user-only | allowed | required-after-commit | required-at-session-end
- Pre-Commit-Checks: none | <check-name>; <check-name>
- Doku-Check: none | <kurzregel> | ref:<pfad>#<überschrift>

### Code
- Stacks: none | <key>; <key>
- Pflichtkontext: none | <pfad/ref>; <pfad/ref>
- Aufgabenquelle: none | <pfad/ref>
- Architekturregeln: none | ref:<pfad>#<überschrift>
- Tests: none | <check-name>; <check-name>
- Auslieferung: none | ref:<pfad>#<überschrift>
- Mockup-Policy: none | required:<bedingung> | ref:<pfad>#<überschrift>
- Befund-Ort: none | <pfad/ref>

### Doku
- Router: none | <pfad>
- Standard: none | ref:<pfad>#<überschrift>
- Pflichtdokumente: none | <pfad/ref>; <pfad/ref>
- Validierungsregeln: none | ref:<pfad>#<überschrift>
- Sitzungsabschluss: none | ref:<pfad>#<überschrift>
- Entscheidungs-Ort: none | <pfad/ref>

### Tracker
- Provider: none | clickup
- Config: none | .claude/skill-config/tracker.md

### Ticket
- Config: none | .claude/skill-config/ticket.md

### Mockup
- Ablage: none | <pfad>
- Designquelle: none | <pfad/ref>
- Ansichten: none | <ansicht>; <ansicht>
- Abnahme-Ort: none | <pfad/ref>

### Review
- Config: none | .claude/skill-config/review.md

### Modul
- Manifest: none | <pfad/muster>
- Grundsatzregeln: none | ref:<pfad>#<überschrift>
```

Bedeutung einzelner Felder:
- **Branch-Policy:**
  - `current` – die aktuelle Arbeitskopie verwenden, ohne zu fragen.
  - `fixed:<branch>` – der aktuelle Branch muss dieser sein, sonst ist das ein echter Konflikt.
- **Push-Policy:**
  - `user-only` – Claude pusht nie.
  - `allowed` – Claude pusht auf Anweisung.
  - `required-after-commit` – Claude pusht nach jedem Commit ohne Rückfrage.
  - `required-at-session-end` – Claude pusht am Ende der Sitzung.
- **Versionsquelle:** eine Datei mit Feld (z. B. `card/package.json#version`) oder `changelog:CHANGELOG.md`. Im
  zweiten Fall ist die Version die Nummer des obersten Eintrags. Die Nummer steht nie zusätzlich im Profil.

## Checks

Ein Check ist ein benannter Befehl mit Geltungsbereich:

```markdown
- card: npm test; npm run lint [card/**]
- backend: python -m pytest [ha/prognose/**]
```

- Ein Check gilt, wenn mindestens eine geänderte Datei zu einem seiner Pfad-Muster passt.
- `Pre-Commit-Checks` nennt die Checks, die vor einem Commit laufen; es laufen nur die, die gelten.
- Checks mit echten Modellaufrufen wie `claude plugin eval` sind keine Pre-Commit-Checks, weil jeder Lauf das Kontingent
  belastet. Sie laufen als Tor vor der Auslieferung (siehe [skill-quality.md](./skill-quality.md), Abschnitt „Verhalten“).

## Pflichtfelder je Skill

Grundfelder für alle: `Profil-Version`, `Projekt-ID`, `Repo`, `Branch-Policy`.

| Skill | Pflichtfelder |
|---|---|
| audit | Doku.Router, Doku.Validierungsregeln; Code.Architekturregeln, wenn Code geprüft wird; Tracker.Config, wenn der Tracker geprüft wird |
| cc-steuerung | keine (nur Cowork-Chat mit ausdrücklichem Desktop-Commander-Auftrag) |
| chat-wechsel | Doku.Sitzungsabschluss, Doku.Entscheidungs-Ort, Commit.Push-Policy; Tracker.Config, wenn Aufgaben eingebunden sind |
| chatgpt-review | Review.Config, Commit.Push-Policy |
| code-erstellen | Code.Stacks, Code.Pflichtkontext, Code.Architekturregeln, Code.Tests, Code.Auslieferung; Code.Aufgabenquelle, wenn das Projekt Aufgaben führt |
| doc-pflege | Doku.Router, Doku.Standard, Doku.Entscheidungs-Ort |
| git-commit-helper | Commit.Format, Commit.Module, Commit.Versionsquelle, Commit.Versionsregel, Commit.Push-Policy, Commit.Pre-Commit-Checks |
| mockup-erstellen | Mockup.Ablage, Mockup.Designquelle, Mockup.Ansichten, Mockup.Abnahme-Ort |
| skill-neu, skill-pflege | das Profil des Skill-Repos (Commit, Doku, Checks) |
| ticket | Ticket.Config |
| tracker | Tracker.Provider, Tracker.Config |
| modul-bauplan (geplant) | Modul.Manifest, Modul.Grundsatzregeln, dazu die Code- und Doku-Felder |

## Fehlende Werte

Braucht ein Skill ein Feld, das fehlt oder `fehlt` ist, meldet er genau dieses Feld:

> `<Skill>` braucht `<Bereich>.<Feld>`; der Wert fehlt im Skill-Profil.

Dann eine Auswahlfrage mit drei Optionen: *Profil ergänzen* / *Wert einmalig nennen* / *Abbrechen*. Kein „ganzes Profil
anlegen?“. Fehlt das Profil ganz, wird es mit dem Vorschlag aus dem Repo angelegt, bevor der Skill weiterarbeitet.

## Configs unter `.claude/skill-config/`

Es gibt nur die Dateien, die ein Projekt braucht.

| Datei | Gliederung |
|---|---|
| `tracker.md` | Provider · Nummernschema · Nächste freie Nummer · Listen und Routing · Statusmodell · Felder und Option-IDs · Titel- und Beschreibungsformat · Quittungsformat · Sonderfälle |
| `ticket.md` | Quelle · Lese- und Schreibweg · Statusmodell · Pflichtangaben je Status · Tracker-Kopplung · Beweisquellen · Doku-Kopplung · Schließen und Prüfen |
| `review.md` | Allgemein (Ablage, Serienformat, Übersicht) · je Thema: Reviewer-Rolle, Repos, Kontextquelle, Pflicht-Block, Ergebnis-Ort |

Die nächste freie Aufgabennummer steht nur in `tracker.md`.

## Prüfung

- **Laufzeit:** Jeder Skill prüft nur seine Pflichtfelder (Tabelle oben).
- **Prüfskript:** `tools/validate-skills.ps1` prüft im Skill-Repo die Profil-Version.
- **audit:** prüft in jedem Repo das ganze Profil:
  - Ist die Version gültig?
  - Sind die Bereiche vollständig, die die genutzten Skills brauchen?
  - Gibt es die Dateien und Überschriften, auf die `ref:` zeigt?
  - Widersprechen sich Profil und Prosa der CLAUDE.md?
  - Gibt es unbekannte Felder oder veraltete Pfade?

## Einführung in den Repos

| Repo | Stand |
|---|---|
| claude-skills-bpm | Profil in der `CLAUDE.md`, Configs `review.md` und `tracker.md` (Umbau Phase 1) |
| BauProjektManager | Phase 2: Profil und `tracker.md`; Push-Policy `user-only` |
| HA_Dash_DreameX60 | Phase 2: Profil, `tracker.md`, `ticket.md` (`review.md` nur bei Bedarf), aus dem heutigen Stand neu aufgebaut |

Bis die Skills in den Umbau-Phasen 5 und 6 das Profil lesen, bleiben ihre bisherigen Quellen als Verweise erhalten:
`docs/project-architecture.md` und der Abschnitt `## Review-Profil` in der CLAUDE.md des Skill-Repos. `projects/` wird
erst entfernt, wenn kein Skill mehr dorthin zeigt. Entwürfe für die Profile von BPM und Heidi stehen in
`docs/chatgpt-reviews/CGR-2026-09-24-skillsystem/r2/02-chatgpt-response.md` (Abschnitt 5) – nur als Ausgangspunkt, die
Werte müssen im jeweiligen Repo geprüft werden.
