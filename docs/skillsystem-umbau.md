# Umbau des Skillsystems – Plan

Arbeitsgrundlage für den Umbau der 12 Skills. Entstanden in der Review-Serie
[CGR-2026-09-24-skillsystem](./chatgpt-reviews/CGR-2026-09-24-skillsystem/README.md) (Runden 1–3); Einzelheiten und
Begründungen stehen dort, vor allem in `r3/02-chatgpt-response.md` (Umbau-Plan) und `r3/03-claude-analysis.md`
(Schärfungen). Erledigte Punkte werden hier abgehakt.

## Entscheidungen

| Thema | Entscheidung |
|---|---|
| Projektwerte | Ein Block `## Skill-Profil` (Version 1) in der CLAUDE.md jedes Repos; Werte genau einmal, lange Regelwerke per `ref:`; `none` = bewusst leer, `fehlt` = blockiert den Skill, der das Feld braucht |
| Große Configs | Tracker, Ticket, Review je als Datei unter `.claude/skill-config/` im Projekt-Repo; `projects/<name>/` verschwindet aus dem Skill-Repo |
| cc-steuerung | bleibt als kleiner Cowork-Adapter (rund 100 Zeilen), löst in Claude Code nie aus |
| Verteilung | Upload über claude.ai; Two-Place-Pflege bleibt (Lieferregeln in `skill-pflege/references/delivery.md`) |
| Umgebung | Claude Code ist die Hauptumgebung; Cowork-Teile wandern in Referenzen |
| Push im Skill-Repo | nach jedem Commit ohne Rückfrage |
| Version im Skill-Repo | neue Nummer und CHANGELOG-Eintrag nur bei Skill-Änderungen; Doku-, Review-, Config-, Eval- und Tool-Commits behalten die Nummer; Versionsquelle ist der oberste CHANGELOG-Eintrag |
| Prüfung der Skills | kein eigener Skill: `tools/validate-skills.ps1` (PowerShell 7) prüft die Mechanik, audit urteilt, skill-pflege nutzt dieselbe Prüfung als Abschluss |
| Messung | `claude plugin eval` für das Auslösen zwischen unseren Skills; echte Sitzungen für Konflikte mit Anthropic-Skills; `skill-creator` für die Qualität einzelner Skills; `test-prompts.md` entfällt |
| Tests | zuerst ein Pilot (5 Fälle × 3 Läufe); danach entscheidet Herbert über die volle Grundmessung (60 Fälle) |
| Namen | kein Umbenennen der Skills |

## Regeln, die der Umbau einführt

- **Qualität** (Quelle künftig `docs/skill-quality.md`): Description „was + wann“, dritte Person, höchstens 1024 Zeichen;
  SKILL.md unter 500 Zeilen; References direkt aus SKILL.md verlinkt, über 100 Zeilen mit Inhaltsverzeichnis; keine
  Historie im Regeltext; einheitliche Begriffe; Freiheitsgrad nach Fragilität (MUSS/NIE nur bei Status, Datenverlust,
  Geheimnissen, Push, Version, Commit-Voraussetzungen); MCP-Werkzeuge voll qualifiziert nur in Integrationsabschnitten
  oder Referenzen.
- **Fragen:** nur, wenn nach Auftrag, Skill-Profil, Regel und Kontext eine echte Entscheidung offen bleibt; dann mit dem
  Auswahlwerkzeug der Umgebung.
- **skill-pflege:** zwei Modi. Safe Patch für kleine Änderungen. Refactor mit Regel-Inventar unter
  `docs/skill-refactors/<Datum>-<skill>.md`:
  - Zustände `KEEP|MOVE|MERGE|REWRITE|DROP|NEW`.
  - Abgleich in beide Richtungen, DROP als Sammelfreigabe.
  - Verweise über Datei und Überschrift statt über Nummern.
- **Eigenständigkeit:** „Self-contained contract, not duplicated implementation“.
- **Descriptions** werden erst nach der Grundmessung geändert, danach jede Änderung mit Eval.

## Tests

- `skill-validation` läuft vor jedem Commit, der `skills/**` berührt.
- `routing-eval` (`claude plugin eval`) ist **kein** Pre-Commit-Check. Er läuft vor dem Upload bei claude.ai und nach jeder
  Änderung an einer Description oder an auslöserelevanten Abschnitten, dann nur die betroffenen Fälle (`--case`/`--tag`).
  Die ganze Suite läuft in Phase 3 und Phase 7.
- Schwellen: kritische Fälle 3/3, sonst mindestens 2/3. Freigabe eines Umbaus:
  - kein kritischer Fall unter 3/3
  - kein bisher bestandener Negativfall kippt
  - die Gesamtquote liegt nicht unter der Grundmessung
  - neue Konflikte sind erklärt
  - das Prüfskript meldet keine neuen Fehler
- Jeder Lauf ist eine echte Claude-Sitzung und zählt gegen Herberts claude.ai-Kontingent (Abo, keine Rechnung).
- Voraussetzung: `plugin eval` startet für jeden Lauf ein eigenes `claude`-Programm. Das braucht ein angemeldetes CLI
  (`claude auth login`, einmal je PC; prüfen mit `claude auth status`). Die Anmeldung der Desktop-App reicht nicht – der
  erste Pilotversuch am 24.09. brach deshalb nach einem Lauf ab („Not logged in“, ohne Kosten).
- Konflikte mit Anthropic-Skills (`skill-creator` ↔ skill-neu/skill-pflege, `code-review` ↔ audit, cc-steuerung in Claude
  Code) misst `plugin eval` nicht, weil die Sitzung dort abgeschottet ist. Diese Fälle laufen als echte Sitzungen,
  Protokoll unter `quality/real-environment/`.

## Phasen

### Phase 1 – Infrastruktur und Skill-Repo (dieses Repo, keine Skill-Änderung)

- [x] `.claude-plugin/plugin.json` nur für Tests (`experimental.evals: quality/evals`)
- [x] fünf Pilotfälle unter `quality/evals/` (audit-readonly, doc-write, code-implement, skill-update, cc-not-in-claude-code)
- [x] `.gitignore`: `quality/evals/results/`, `quality/results/`
- [x] `tools/validate-skills.ps1` (PowerShell 7, JSON-Bericht, Exit 0/1/2)
- [x] `docs/skill-quality.md`
- [x] `docs/project-architecture.md` → `docs/skill-profile-v1.md` (Spezifikation Skill-Profil v1); `project-architecture.md`
      bleibt als Verweis, solange tracker, README und `projects/bpm` darauf zeigen
- [x] CLAUDE.md: `## Skill-Profil`; `.claude/skill-config/review.md` (aus dem Review-Profil); `.claude/skill-config/tracker.md`
      (Space Claude Skills Entwicklung, Liste ClaudeSkills, Skill-Issue-Listen); altes `## Review-Profil` entfernen –
      abweichend nur auf einen Verweis gekürzt: chatgpt-review liest den Abschnitt noch, er entfällt in Phase 5/6
- [x] CHANGELOG nachziehen:
  - Einträge für v0.35.2–v0.35.4
  - ein gemeinsamer Nachtrag für v0.36.1–v0.36.9 (alte Regel)
  - die doppelte v0.36.0 vermerken
  - zusätzlich gefunden und nachgetragen: v0.23.0, v0.20.0
- [x] README und INDEX: nur Fakten (12 Skills, Inventar, Modus-Zahl); der INDEX-Umbau folgt in Phase 5
- [x] tracker bei claude.ai neu hochladen (Herbert): In der hochgeladenen Fassung enthält `references/create-task.md` den
      Inhalt von `clickup-tools.md`; die Fassung im Repo ist richtig – am 24.09. hochgeladen und geprüft: die von der
      Desktop-App synchronisierte Fassung ist in allen 15 Dateien gleich wie im Repo

**Abnahme:** `claude plugin validate .` ist grün; das Prüfskript läuft; die Pilotfälle werden gefunden; keine SKILL.md
geändert.

Stand 24.09.2026: `claude plugin validate .` bestanden mit einer erwarteten Warnung (CLAUDE.md im Plugin-Wurzelordner wird
nicht als Kontext geladen). Das Prüfskript läuft: 12 Skills, 1 Fehler, 120 Warnungen – der Fehler ist ein toter Verweis
in doc-pflege (`references/projekt-init.md`) und wird mit der ersten Änderung an doc-pflege behoben. `plugin eval` liest
`quality/evals/` aus dem Manifest; der Pilot am 24.09. hat alle fünf Fälle gefunden und bewertet. Seit dem Plan-Commit ist
unter `skills/` nichts geändert. **Phase 1 abgeschlossen am 24.09.2026.**

### Phase 2 – Profile der Projekte (je eine Sitzung im Projekt-Repo)

- [ ] BPM: `## Skill-Profil` in `CLAUDE.md`, `.claude/skill-config/tracker.md` (BPM-Space, 17 Listen, Felder, Kürzel,
      Status, Nummern). Push-Policy `user-only`: Herbert pusht.
- [ ] Heidi (`HA_Dash_DreameX60`, anderer PC): Profil und `tracker.md`/`ticket.md` (`review.md` nur, wenn gebraucht) aus der
      heutigen CLAUDE.md, der Projektdoku und ClickUp neu aufbauen; `projects/heidi/` nur zum Gegenprüfen
- [ ] `projects/` aus dem Skill-Repo entfernen, wenn alles gegengeprüft ist

**Abnahme:** Alle drei Repos haben ein vollständiges Profil; nichts zeigt mehr auf `projects/<name>/`.

### Phase 3 – Grundmessung

- [x] Pilot: `claude plugin eval . --tag pilot --runs 3 --ablation none --no-publish` – gelaufen am 24.09.2026
      (Ergebnis unten)
- [x] Herbert entscheidet über die volle Grundmessung (60 Fälle nach Risiko, 3 Läufe) – 24.09.: voll, 60 Fälle × 3 Läufe
- [x] 60 Fälle nach Risiko unter `quality/evals/` schreiben: ohne Abhängigkeit von Repo-Dateien (die Sandbox hat keine);
      den audit-Fall teilen in den heutigen Vertrag (Code ↔ Doku) und einen Ziel-Fall Skill-Prüfung, der bis Phase 5
      scheitern darf – 24.09., von Herbert freigegeben; Katalog und Regeln in `quality/README.md`
- [ ] Grundmessung laufen lassen (rund 180 Läufe; angemeldetes CLI) – Teil 1 am 24.09. (20:59–21:58, auf Wunsch
      abgebrochen): 30 Fälle vollständig, 25 bestanden, 81/91 Läufe; Ergebnis in `quality/baseline/teil-1-2026-09-24.md`.
      Offen: Teil 2 mit den übrigen 30 Fällen (ab `doc-changelog`) bei unveränderten Skills; `audit-findings-fix` vorher
      ohne Verweis auf fehlenden Kontext neu formulieren

Ergebnis des Pilots (unveränderte Skills, 5 Fälle × 3 Läufe):

| Fall | Ergebnis | Bewertung |
|---|---|---|
| audit-readonly (kritisch) | 0/3 | audit löst nie aus; der Auftrag (INDEX gegen Skill-Beschreibungen prüfen) liegt außerhalb der heutigen audit-Description (Code ↔ Doku). Dazu fehlen die genannten Dateien in der Sandbox, zwei Läufe liefen bis zur Grenze von 8 Schritten. Der Fall misst den Zielzustand nach Phase 5, nicht den heutigen Vertrag. |
| cc-not-in-claude-code (kritisch) | 2/3 | echter Fehler: cc-steuerung löst einmal aus; die Description nennt „Claude Code“ als Auslöser (Behebung Phase 5) |
| code-implement | 3/3 | – |
| doc-write (kritisch) | 3/3 | audit löst nicht aus |
| skill-update (kritisch) | 3/3 | skill-neu löst nicht aus |

Gesamt 11/15 Läufe (3 von 5 Fällen). Dauer 14 Minuten (rund 55 Sekunden je Lauf), Gegenwert zum Listenpreis 5,66 USD
(rund 0,38 USD je Lauf; keine Rechnung, zählt gegen das Max-Kontingent). Hochgerechnet: 60 Fälle × 3 Läufe sind rund
180 Läufe, knapp 3 Stunden nacheinander, Gegenwert rund 70 USD. `plugin eval` löscht die Protokolle der Läufe; zur
Fehlersuche einen Fall einzeln mit `--keep-temp` laufen lassen (behält laut Hilfe die Temp-Ordner).
- [ ] echte Sitzungen EXT-01 bis EXT-05
- [ ] Grundmessung einfrieren

**Abnahme:** Die unveränderten Skills sind vermessen.

### Phase 4 – skill-pflege und skill-neu

- [ ] skill-pflege: Safe Patch, Refactor, Regel-Inventar, Lieferregeln in `references/delivery.md`, Prüfskript als Abschluss
- [ ] skill-neu: Lehrbuchteile raus, Governance-Ablauf, Qualitätsquelle, zentrale Eval-Fälle, Kollisionsprüfung inkl.
      Anthropic-Skills

**Abnahme:** Refactors können Text entfernen und zusammenführen, ohne dass Regeln unbemerkt verloren gehen.

### Phase 5 – Querschnitt

- [ ] cc-steuerung als Cowork-Adapter (neue Description, schließt Claude Code aus)
- [ ] Cowork-Pfadermittlung aus audit, code-erstellen, doc-pflege und mockup-erstellen entfernen
- [ ] Regel „Fragen nur bei offener Entscheidung“ in alle Skills übernehmen
- [ ] Branch und Push aus dem Profil lesen
- [ ] INDEX neu als Verzeichnis für das Auslösen; Invarianten 1–10 an ihren neuen Ort
- [ ] Grenzen audit ↔ doc-pflege ↔ modul-bauplan festziehen (doc-pflege Modus 3, 4 und 6 als öffentliche Modi entfernen)
- [ ] Descriptions anpassen, jeweils mit Eval

**Abnahme:** keine kopierten Querschnittsregeln mehr; cc-steuerung löst in Claude Code nicht aus.

### Phase 6 – Skill für Skill verkleinern

Reihenfolge: mockup-erstellen, chat-wechsel, chatgpt-review, code-erstellen, doc-pflege, tracker, audit,
git-commit-helper, ticket.

Je Skill:
- Regel-Inventar
- Refactor
- unter 500 Zeilen
- Historie und Projektwerte raus
- Inhaltsverzeichnisse in langen References
- Verweise über Datei und Überschrift
- Prüfskript und Evals
- Commit
- Upload bei claude.ai durch Herbert

**Abnahme:** Kein Skill ist schlechter als seine Grundmessung.

### Phase 7 – Gesamtabnahme

- [ ] alle Fälle und die echten Sitzungen
- [ ] `skill-creator` auf die kritischen Skills
- [ ] Prüfskript ohne Fehler
- [ ] `test-prompts.md`, `references.zip`, `projects/` entfernt
- [ ] README und INDEX aktuell; alle Projekt-Repos mit Profil v1

## Was Herbert selbst tut

- nach jeder Skill-Änderung die SKILL.md bzw. Zip bei claude.ai hochladen
- nach dem Pilot über die volle Grundmessung entscheiden
- die echten Sitzungen für die Konflikte mit Anthropic-Skills starten
- in BPM selbst pushen

## ClickUp

Je Phase eine Aufgabe in der Liste ClaudeSkills (Space Claude Skills Entwicklung):

| Phase | Aufgabe |
|---|---|
| 1 | [Infrastruktur und Skill-Repo](https://app.clickup.com/t/123ztrcxedg) |
| 2 | [Profile der Projekte](https://app.clickup.com/t/123ztrcxedj) |
| 3 | [Grundmessung](https://app.clickup.com/t/123ztrcxedk) |
| 4 | [skill-pflege und skill-neu](https://app.clickup.com/t/123ztrcxedm) |
| 5 | [Querschnitt](https://app.clickup.com/t/123ztrcxedp) |
| 6 | [Skill für Skill verkleinern](https://app.clickup.com/t/123ztrcxedq) |
| 7 | [Gesamtabnahme](https://app.clickup.com/t/123ztrcxedr) |
