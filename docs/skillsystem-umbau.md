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
| Projekt-Repos | Der Umbau ändert keine Projekt-Repos; die Skills werden ohne Bezug zu einer App neutral. Ein Projekt-Profil entsteht erst, wenn ein Skill es braucht und Herbert zustimmt (Phase 2 entfällt, 28.09.2026) |
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

### Phase 2 – Profile der Projekte (entfällt)

**Entfällt seit 28.09.2026 (Entscheidung Herbert):** Der Umbau ändert keine Projekt-Repos. Die Skills werden im Skill-Repo
neutral, ohne Bezug zu einer App. Ein Projekt bekommt sein Skill-Profil erst, wenn ein Skill dort ein Feld braucht und
Herbert dem Vorschlag zustimmt ([skill-profile-v1.md](./skill-profile-v1.md), Abschnitt „Fehlende Werte“). Was mit den
Werten in `projects/` geschieht, klärt Phase 6 beim Skill tracker.

### Phase 3 – Grundmessung

- [x] Pilot: `claude plugin eval . --tag pilot --runs 3 --ablation none --no-publish` – gelaufen am 24.09.2026
      (Ergebnis unten)
- [x] Herbert entscheidet über die volle Grundmessung (60 Fälle nach Risiko, 3 Läufe) – 24.09.: voll, 60 Fälle × 3 Läufe
- [x] 60 Fälle nach Risiko unter `quality/evals/` schreiben: ohne Abhängigkeit von Repo-Dateien (die Sandbox hat keine);
      den audit-Fall teilen in den heutigen Vertrag (Code ↔ Doku) und einen Ziel-Fall Skill-Prüfung, der bis Phase 5
      scheitern darf – 24.09., von Herbert freigegeben; Katalog und Regeln in `quality/README.md`
- [x] Grundmessung laufen lassen (rund 180 Läufe; angemeldetes CLI) – in zwei Teilen: Teil 1 am 24.09. (30 Fälle, auf
      Wunsch abgebrochen, aus den Protokollen nachgerechnet), Teil 2 am 27./28.09. (übrige 30 Fälle und das neu
      formulierte `audit-findings-fix`), Skills unverändert seit 12f90b8. **Ergebnis: 55 von 60 Fällen, 172 von 180
      Läufen, kritische Fälle 20 von 23** – `quality/baseline/grundmessung-2026-09.md`

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
- [x] echte Sitzungen EXT-01 bis EXT-05 – Anleitung `quality/real-environment/README.md`; Protokoll
      `quality/real-environment/2026-09-28.md`: EXT-01 (skill-neu), EXT-02 (skill-pflege), EXT-03 (audit) und EXT-05
      (kein Skill) je 3/3, kein Skill von Anthropic kam; EXT-04 entfällt bis modul-bauplan
- [x] Grundmessung einfrieren – `quality/baseline/grundmessung-2026-09.md` ist die Vergleichsbasis (28.09.2026)
- [x] Abgleich mit den alten Aufgaben der Liste ClaudeSkills (28.09.2026): P4.1 (Skill-Lade-Hinweise) und P2
      (Fresh-Model-API-Eval) als abgelöst geschlossen; P4.2 (Golden Cases) bleibt offen und legt echte Fehlrouting-Fälle
      künftig unter `quality/evals/` bzw. `quality/real-environment/` ab

**Abnahme:** Die unveränderten Skills sind vermessen.

Stand 28.09.2026: Grundmessung 55 von 60 Fällen, 172 von 180 Läufen, kritische Fälle 20 von 23 (eingefroren); echte
Sitzungen 4 von 4 Fällen, 12 von 12 Sitzungen. Unter `skills/` ist seit 12f90b8 nichts geändert. **Phase 3 abgeschlossen
am 28.09.2026.**

### Phase 4 – skill-pflege und skill-neu

- [x] skill-pflege: Safe Patch, Refactor, Regel-Inventar, Lieferregeln in `references/delivery.md`, Prüfskript als Abschluss
      – v0.37.0/v0.37.1, Routing-Eval 33/33, bei claude.ai hochgeladen (28.09.2026)
- [x] skill-neu: Lehrbuchteile raus, Governance-Ablauf, Qualitätsquelle, zentrale Eval-Fälle, Kollisionsprüfung inkl.
      Anthropic-Skills – v0.38.0, Routing-Eval 24/24, bei claude.ai hochgeladen (28.09.2026)
- [x] Prüfskript: `-RuleInventory` sammelt Regel-Kandidaten für die Inventare (94f06d0)

**Abnahme:** Refactors können Text entfernen und zusammenführen, ohne dass Regeln unbemerkt verloren gehen.

Stand 28.09.2026: Beide Skills sind nach dem neuen Refactor-Ablauf umgebaut, jeweils mit Regel-Inventar unter
`docs/skill-refactors/`. Jede alte Regel hat dort einen Zustand, die DROP-Gruppen hat Herbert freigegeben, beide
Richtungen sind geprüft. skill-pflege 628 → 195 Zeilen, skill-neu 534 → 172 Zeilen, Descriptions unverändert;
Routing-Eval gleich wie die Grundmessung (33/33 bzw. 24/24). Offene Verweise auf alte skill-pflege-Nummern stehen in den
Aufgaben zu Phase 5 (cc-steuerung) und Phase 6 (doc-pflege, tracker). **Phase 4 abgeschlossen am 28.09.2026.**

### Phase 5 – Querschnitt

- [x] cc-steuerung als Cowork-Adapter (neue Description, schließt Claude Code aus) – v0.38.1, 428 → 113 Zeilen plus
      `references/desktop-commander.md`; Routing-Eval `cc-not-in-claude-code` 3/3 (Grundmessung 2/3); EXT-05 nach dem Upload
- [x] Cowork-Pfadermittlung aus audit, code-erstellen, doc-pflege und mockup-erstellen entfernen – v0.38.2: Verweis auf
      cc-steuerung, Abschnitt „Arbeitsverzeichnis“; in code-erstellen der kopierte Ablauf entfernt; nebenbei der tote
      Verweis in doc-pflege behoben (Prüfskript 0 Fehler)
- [x] Regel „Fragen nur bei offener Entscheidung“ in alle Skills übernehmen – v0.39.1, Abschnitt „Grundsätze“ in acht
      Skills (ticket bewusst unverändert, cc-steuerung, skill-neu und skill-pflege hatten sie schon)
- [x] Branch und Push aus dem Profil lesen – v0.39.1; ohne Skill-Profil bleibt der bisherige Rückfall je Skill
      (Entscheidung Herbert); git-commit-helper liest dafür zuerst das Skill-Profil v1
- [x] INDEX neu als Verzeichnis für das Auslösen; Invarianten 1–10 an ihren neuen Ort – 28.09.2026: Tabelle
      „Zuständig für / Löst aus bei“, Konfliktpaare samt Anthropic-Skills, Tabelle „Wo die gemeinsamen Regeln stehen“
      statt der Invarianten; entfallen: Smoke-Test-Pflicht (Datei gibt es nicht mehr), Frühphasen-Prinzip (Projektregel),
      Fallback über `projects/`/Memory und die Aussage „projektspezifisch“ (212 → 109 Zeilen)
- [x] Lieferung v0.38.2/v0.39.1 an Herbert: audit, chat-wechsel, chatgpt-review, code-erstellen, doc-pflege,
      git-commit-helper, mockup-erstellen, tracker (je ein Upload, 28.09.2026)
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
- [ ] README und INDEX aktuell; kein Skill mit Werten oder Beispielen einer bestimmten App

### Plan (07.10.2026, von Herbert freigegeben; Schritte 1–6 erledigt) – Plugin-Marketplace

Ziel: Skills, Skill-Log und Skill-Wächter mit einem Befehl auf jedem Rechner installieren (Firmen-Laptop) und für
andere nutzbar machen. Herbert hat entschieden: erst Fragen klären und Plan, umgebaut wird nach seiner Freigabe auf dem
Zweig `umbau-plugins`, Merge ebenfalls nach Freigabe. ClickUp:
[📦 Umbau 2026-09 · Plugin-Marketplace](https://app.clickup.com/t/123ztrd09u7).

**Namen (Herbert, 07.10.2026)**

| Was | Name | Installation |
|---|---|---|
| Repo | `claude-workbench` (bis 07.10.2026 `claude-skills-bpm`) | `/plugin marketplace add herbertschrotter-blip/claude-workbench` |
| Marketplace | `workbench` (steht in `marketplace.json`, unabhängig vom Repo-Namen) | |
| Plugin für die Arbeit | `work` | `work@workbench` |
| Plugin für Skill-Arbeit | `skill-workshop` | `skill-workshop@workbench` |

**Inhalt der Plugins**

- **`work`:** code-erstellen, mockup-erstellen, doc-pflege, ticket, projekt-anlegen, tracker, git-commit-helper, audit,
  chat-wechsel, sitzung, chatgpt-review; Hooks Skill-Log und Wächter (mit `regeln.json`); ein Befehl, der Skill-Profil und
  Configs im Projekt anlegt.
- **`skill-workshop`:** skill-neu, skill-pflege, skill-auswertung, Prüfskript, Eval-Gerüst, Report; für jedes Skill-Repo
  mit Profil.
- **Außerhalb:** cc-steuerung (nur Cowork, Upload).
- Jeder Skill liegt in genau einem Plugin (keine Kopien, die auseinanderlaufen können).

**Geklärte Fragen (Claude-Code-Doku, auf dem Pi noch zu testen)**

| Frage | Antwort laut Doku |
|---|---|
| Synchronisierte claude.ai-Skills in Claude Code abschalten? | Ja: `syncClaudeAiSkills: false` in `settings.json` (ganz) oder `skillOverrides` je Skill (`"anthropic-skills:<name>": "off"`). Damit kann der Pi die Skills aus dem Plugin laden, ohne sie doppelt zu haben |
| Installation aus privatem GitHub-Repo? | Ja, über die Git-Zugangsdaten des Rechners (SSH-Schlüssel oder `gh auth login` + `gh auth setup-git`); Plugins in Unterordnern per `"source": "./plugins/<name>"` |
| Automatische Updates? | Ab Werk aus; je Marketplace in `/plugin` einschaltbar oder `"autoUpdate": true` im Eintrag unter `extraKnownMarketplaces`. Version aus `plugin.json`, sonst der Git-Commit; von Hand `claude plugin update work@workbench` |
| Plugin nur mit Hooks? | Ja: `.claude-plugin/plugin.json` und `hooks/hooks.json` genügen; Skripte über `"${CLAUDE_PLUGIN_ROOT}/…"`; für Variante B stehen die Hooks direkt im Marketplace-Eintrag |

**Übernommen aus [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)** (Marketplace mit 99
Plugins im selben Repo)

- `plugin.json` streng halten: Claude Code lehnt das ganze Plugin bei einem unbekannten Eintrag ab; Pfade beginnen mit
  `./`. Das Prüfskript prüft künftig `plugin.json` und `marketplace.json`.
- Hooks scheitern stumm (Ende mit 0, nichts blockiert bei eigenem Fehler) und lassen sich je Hook über eine
  Umgebungsvariable abschalten (z. B. `SKILL_GUARD=0`, `SKILL_LOG=0`); jeder Hook mit `timeout`.
- Zahlen in README und Beschreibungen (Skills, Eval-Fälle) nicht von Hand pflegen, sondern prüfen oder erzeugen.

**Was der Umbau berührt**

- Root-`.claude-plugin/plugin.json` (`herbert-skills-eval`, Eval-Rahmen) neben der neuen `marketplace.json`: prüfen, ob
  beides im selben Ordner geht, sonst den Eval-Rahmen verlegen; `routing-eval`-Befehl im Profil anpassen.
- Prüfskript, GitHub Action `validate-skills.yml`, Evals (`quality/evals`), Report-Skript: neue Pfade `plugins/<name>/skills/`.
- skill-pflege: Lieferung (`references/delivery.md`) um den Plugin-Weg ergänzen; Description nennt den Repo-Namen.
- Umbenennung des Repos: Remotes der Klone (Pi, PC), Skill-Profil in `CLAUDE.md` (Projekt-ID, Repo), Wächter-Regel mit
  `"projekt": "claude-skills-bpm"` in `regeln.json` (der Wächter vergleicht den Projektnamen), Tracker-Config, Verweise
  in `docs/` und im HA-Profil (`/config/CLAUDE.md`, Link auf die HA-Grundsatzregeln; GitHub leitet alte Adressen weiter).
- Hooks in `~/.claude/settings.json` auf dem Pi: Herbert ersetzt sie durch das Plugin (Claude ändert keine
  Hook-Einstellungen).

**Schritte**

1. ✅ **Test auf dem Pi (07.10.2026, Claude Code 2.1.292),** im Scratch-Ordner, danach wieder entfernt:
   - `skillOverrides` in der Projekt-`settings.json`: `"anthropic-skills:audit": "off"` blendet den Skill aus;
     `"name-only"` lässt ihn in der Liste.
   - Marketplace `workbench` mit Plugin `work` nur mit Hooks: `claude plugin validate` grün, auch neben der
     Root-`plugin.json` des Eval-Rahmens; Installation mit `--scope local`; Skill-Log schreibt Sitzung, Prompt und
     Rundenende. Die Skripte müssen im Plugin-Ordner liegen (installiert wird nur der Plugin-Ordner).
   - Befunde: Das Repo ist **öffentlich** (kein Test mit privatem Repo nötig; Schritt 8 heißt damit „private Daten
     raus“, bevor der Marketplace beworben wird). Der Hostname im Add-on ist eine Container-ID; `SKILL_LOG_HOST` muss je
     Rechner gesetzt werden (Plugin-Option oder `env` in `settings.json`). Der Wächter hat den Schalter `SKILL_GUARD=0`
     schon; Skill-Log bekommt `SKILL_LOG=0`. `claude plugin marketplace list` zeigt außerdem
     `claudeai-my-uploads` – die claude.ai-Uploads als eigener Marketplace; vor Schritt 5 prüfen, ob das ein Weg ist.
2. ✅ **Zweig `umbau-plugins`, Marketplace-Gerüst:** `marketplace.json` (`workbench`), Plugin `work` nur mit den Hooks;
   `skill_log.py`, `skill_guard.py`, `regeln.json` und der Wächter-Test liegen jetzt in `plugins/work/hooks/`
   (`tools/skill-log/` behält nur die Auswertung); Schalter `SKILL_LOG=0` neu; Prüfskript prüft `marketplace.json` und
   die Plugin-Ordner (unbekannte Einträge, Pfade mit `./`, Namen, fehlende Hook-Skripte). Gegenprobe auf dem Pi mit
   dem Plugin aus dem Worktree: Wächter blockt, Skill-Log schreibt – zusammen mit den Hooks aus `settings.json` jedes
   Ereignis doppelt, also nie beides zugleich einrichten.
3. ✅ **Pi umstellen – vor dem Merge** (07.10.2026 erledigt: Hooks aus `settings.json` entfernt, `env` gesetzt, Plugin installiert, Fenster neu gestartet; Gegenprobe: jedes Ereignis einmal mit Host `ha-pi`, Wächter blockt aus dem Plugin; danach Merge): Der Pi-Klon auf `main` ist zugleich die Quelle der heutigen Hooks. Nach dem Merge
   fehlen `tools/skill-guard/` und `tools/skill-log/skill_log.py`; ein fehlendes Skript im `PreToolUse`-Hook endet mit
   Exit 2 und blockiert jede Aktion. Deshalb zuerst: Herbert trägt `"env": { "SKILL_LOG_HOST": "ha-pi" }` ein, entfernt
   die Hooks aus `~/.claude/settings.json`, installiert `work@workbench` (vor dem Merge aus dem Worktree, danach aus
   GitHub) und startet die Fenster neu; erst dann Merge und `git pull`. Gegenprobe: jedes Ereignis einmal im Log.
4. ✅ **Skills ins Plugin – ohne Umzug (Variante B, Herbert 07.10.2026):** Die Skills bleiben unter `skills/`. Die
   Einträge in `marketplace.json` haben `"source": "./"` und `"strict": false` und nennen die Skill-Ordner
   (`work`: 11 Skills, `skill-workshop`: 3; cc-steuerung in keinem Plugin); die Hooks stehen direkt im Eintrag von
   `work` (ein Dateipfad für Hooks geht dort nicht), die Skripte bleiben unter `plugins/work/hooks/`. Folgen, auf dem Pi
   getestet:
   - Im Hauptordner darf keine `.claude-plugin/plugin.json` liegen (sonst „widersprüchliche Manifeste“). Der
     Eval-Rahmen zieht nach `quality/`: Manifest `quality/.claude-plugin/plugin.json`, `quality/skills` als Symlink auf
     `../skills`, Aufruf `claude plugin eval quality …` (ein Symlink für die Fälle wird abgelehnt, einer für die Skills
     nicht).
   - Bei der Installation landet das ganze Repo (rund 4 MB) im Plugin-Cache.
   - Claude Code registriert Hooks eines Plugin-Namens nur einmal, auch aus zwei Marketplaces.
   - Skill-Log und Wächter schneiden das Präfix ab (`work:code-erstellen` = `code-erstellen`).
   - Kein Skill geändert, kein Upload. Variante A (Umzug nach `plugins/<name>/skills/`) hätte rund 8 Skills mit Upload
     geändert.
5. ✅ **Doppeltes Laden abschalten – vor dem Plugin-Update** (07.10.2026 erledigt: `skillOverrides` für 14 Skills, `work` 0.2.0, `skill-workshop` 0.1.0; Gegenprobe: jeder Skill einmal geladen, cc-steuerung weiter aus claude.ai, Skill-Log einmal mit `ha-pi`, Wächter blockt): Sobald der Pi `work@workbench` auf die Version mit Skills
   aktualisiert, wären die 14 Skills doppelt da (`anthropic-skills:…` aus claude.ai und `work:…`/`skill-workshop:…`).
   Deshalb zuerst Herbert: in `~/.claude/settings.json` `skillOverrides` mit `"anthropic-skills:<name>": "off"` für die
   14 Skills, dann `claude plugin update work@workbench`, `claude plugin install skill-workshop@workbench`, Fenster neu
   starten; prüfen, dass jeder Skill einmal geladen wird. claude.ai und Cowork behalten den Upload; cc-steuerung bleibt
   aus claude.ai.
6. ✅ **Repo umbenennen** in `claude-workbench` (07.10.2026, `gh repo rename`): Verweise, Projekt-ID, Wächter-Regel `skills`, Remote; Ordner auf dem Pi `/config/projekte/claude-workbench` samt Gesprächsverlauf. Der Klon am PC und Verweise in anderen Projekten (`/config/CLAUDE.md`, ha-baustelle, HA_Dash_DreameX60, `/config/projekte/README.md`) ziehen nach; GitHub leitet die alten Adressen weiter.
7. **Weitere Rechner.** Desktop-PC (07.10.2026): Im Terminal greifen `skillOverrides`, in der Claude-Desktop-App nicht
   (Skills doppelt, gleiche Version 2.1.293). Deshalb gibt es das Plugin `work-hooks` (nur Skill-Log und Wächter, eigener
   Ordner `plugins/work-hooks/`, dort liegen jetzt die Hook-Skripte; `work` ruft sie unter diesem Pfad auf). Ein Eintrag
   mit `strict: false` und `source: "./"` lädt `skills/` immer mit, auch ohne oder mit leerer `skills`-Liste – darum der
   eigene Ordner. Rechner mit Desktop-App: `work-hooks` statt `work` und `skill-workshop`, ohne `skillOverrides`.
   Plugin-Versionen: keine feste `version` in `marketplace.json` und `plugin.json`, damit der Git-Commit als Version
   gilt. Mit fester Nummer erkennt `claude plugin update` Skill-Änderungen nicht (skill-workshop blieb auf 0.1.0 mit
   alter Description von skill-pflege).
   ✅ Desktop-PC eingerichtet (07.10.2026): `work-hooks`, `SKILL_LOG_HOST=desktop-pc`, keine `skillOverrides`; in der App
   alle 15 Skills einmal aus claude.ai; Log-Zeilen mit `desktop-pc` vor dem Wechsel auf `work-hooks` geprüft.
   **Firmen-Laptop:** Marketplace hinzufügen, `work` installieren, Auto-Update einschalten.
8. **Für andere:** private Daten (Projektnamen, ClickUp-IDs, `projects/`) aus dem geteilten Teil, Einrichtungsbefehl,
   README für fremde Nutzer. Bestandsaufnahme 07.10.2026: keine Zugangsdaten im Repo (Tokens, Schlüssel, Mails, IPs).
   Herbert hat entschieden (07.10.2026): **nur der aktuelle Stand** wird bereinigt, die Git-Historie bleibt (Repo ist
   seit 04/2026 öffentlich, ClickUp-IDs ohne Zugang wertlos); Lizenz **MIT**. Bleiben drin: Protokolle
   (`docs/chatgpt-reviews/`, `docs/skill-refactors/`, `quality/real-environment/`, `evals/runs/`), BPM/Heidi als
   Beispiele in den Skills, `.claude/skill-config/tracker.md` (Arbeits-Config dieses Repos).
   - **8a** `LICENSE` (MIT), Lizenz-Abschnitt der README, `skills/sitzung/scripts/__pycache__/*.pyc` aus dem Repo
     (steht trotz `.gitignore` drin). Keine neue Nummer.
   - **8b** tracker neutral: feste IDs aus `skills/tracker/SKILL.md` (BPM-Listen) und `references/issue-task.md`
     (Skill-Issue-Liste) in Profil bzw. Tracker-Config; danach `projects/` entfernen (nur noch tracker liest dort).
     Über skill-pflege, PATCH, Upload tracker.
   - **8c** Wächter für Fremde: `regeln.json` im Plugin wird neutrale Vorlage, eigene Regeln außerhalb (z. B.
     `~/.claude/skill-guard/regeln.json`, wird zuerst gelesen); Hinweistext „sag es Herbert“ neutral. Eigener Entwurf
     vorab; Herbert legt danach seine Regeldatei an.
   - **8d** README-Teil für Fremde: was das Repo ist, Installation (`marketplace add`, welches Plugin wofür,
     `SKILL_LOG_HOST`), Skill-Profil in der `CLAUDE.md` als Voraussetzung. Über doc-pflege.
   - **8e** Einrichtungsbefehl, der Skill-Profil und Configs im Projekt anlegt – eher eigener Skill, MINOR, später.
9. **Merge** nach Herberts Freigabe.

## Was Herbert selbst tut

- nach jeder Skill-Änderung die SKILL.md bzw. Zip bei claude.ai hochladen
- nach dem Pilot über die volle Grundmessung entscheiden
- die echten Sitzungen für die Konflikte mit Anthropic-Skills starten

## ClickUp

Je Phase eine Aufgabe in der Liste ClaudeSkills (Space Claude Skills Entwicklung):

| Phase | Aufgabe |
|---|---|
| 1 | [Infrastruktur und Skill-Repo](https://app.clickup.com/t/123ztrcxedg) |
| 2 | [Profile der Projekte](https://app.clickup.com/t/123ztrcxedj) (entfällt) |
| 3 | [Grundmessung](https://app.clickup.com/t/123ztrcxedk) |
| 4 | [skill-pflege und skill-neu](https://app.clickup.com/t/123ztrcxedm) |
| 5 | [Querschnitt](https://app.clickup.com/t/123ztrcxedp) |
| 6 | [Skill für Skill verkleinern](https://app.clickup.com/t/123ztrcxedq) |
| 7 | [Gesamtabnahme](https://app.clickup.com/t/123ztrcxedr) |
