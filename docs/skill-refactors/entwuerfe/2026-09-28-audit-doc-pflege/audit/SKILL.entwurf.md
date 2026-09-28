---
name: audit
description: >
  Prüft read-only, ob Code, Projektdoku und Skills zueinander passen, nach dem
  Skill-Profil des Repos: Doku gegen Code, Doku-Validierung (z. B. Frontmatter,
  Quickload, Router, Statuslisten), Aufgaben im Tracker gegen die
  Aufgabenquelle, im Skill-Repo die Skills gegen INDEX und Qualitätsregeln.
  Meldet Befunde mit Datei und Stelle und gibt sie an den Fix-Skill oder
  tracker weiter; ändert selbst nichts. Use when users want to prüfen, checken,
  auditieren, or validieren without changes — a consistency audit, a
  documentation-vs-code check, a Frontmatter or Quickload validation, a check
  whether INDEX and skill descriptions fit together (zusammenpassen), or a
  systematic read-only review of project rules. Do not trigger for writing
  documentation or fixing findings (doc-pflege), code implementation
  (code-erstellen), build debugging, or general code review of a function or
  diff without doc comparison.
---

# Audit-Skill — Projekt-Konsistenz-Prüfung

## Zweck

Prüft read-only, ob Code, Projektdoku, Aufgaben im Tracker und – im Skill-Repo – die Skills
zueinander passen. **Was** geprüft wird, steht im **Skill-Profil** des Repos (CLAUDE.md,
Abschnitt „Profile laden“): `Doku.Validierungsregeln` und `Doku.Router`,
`Code.Architekturregeln` und `Code.Aufgabenquelle`, dazu die Stack-Referenzen von
code-erstellen (`references/stacks/<key>.md`) für die Code-Seite; in Repos ohne Skill-Profil
das Feld „Validierung“ des **Doku-Profils** und „Schichten / Kopplung“ und „Aufgabenquelle“
des **Code-Profils**. Im Skill-Repo kommen `docs/skill-quality.md` und die Skill-Tabelle der
`INDEX.md` dazu (Modul 7). audit erfindet keine Prüfregeln; es ist der Read-only-Läufer über
diese Regeln. Eigene Prüflisten führt es nur für die Doku-Validierung, solange ein Projekt sie
nicht im Skill-Profil führt (`references/doku-validierung.md`). BPM: INDEX-Routing,
Frontmatter, Quickload, Schema, DI. Heidi: Bauplan, Vertrag, HANDOFF, PD-Register.

---

## Vorrang / Delegation an andere Skills

**audit ist strikt read-only. Wenn die Hauptabsicht ein Fix, eine
Implementierung oder eine Doc-Pflege ist, NICHT hier weiterarbeiten,
sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Code schreiben oder ändern (Fix, Feature, Refactor) | **code-erstellen** |
| Doku schreiben oder Befunde beheben, ADR, Konzept, Frontmatter-Pflege | **doc-pflege** |
| Skill ändern (auch Skill-Befunde beheben) | **skill-pflege** |
| UI-Entwurf als HTML-Mockup | **mockup-erstellen** |
| Commit-Befehl, Commit-Message | **git-commit-helper** |
| ClickUp-Task-Aktion | **tracker** |

Nur wenn die Hauptabsicht **read-only Konsistenzprüfung** ist
(Audit-Report, Frontmatter-Check, Code-vs-Doc-Abgleich, INDEX-Validierung,
Skill-Prüfung im Skill-Repo), bleibt audit zuständig.

**Wichtig:** Nach einem Audit-Report bietet audit KEINE Fixes selbst an.
Die im Report empfohlenen Aktionen werden per Auswahlfrage an
den passenden Skill delegiert (code-erstellen für Code-Fixes, doc-pflege
für Doc-Fixes, skill-pflege für Skill-Befunde) oder als Aufgaben über
**tracker** angelegt (Abschnitt
„Nach dem Report“). audit ist der Analyse-Skill, nicht der Fix-Skill.

---

## Grundsätze

- **Fragen nur bei offener Entscheidung** – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen
  ist –, dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung. Typische Stellen:

  | Situation | Optionen |
  |-----------|----------|
  | Modus-Auswahl (A oder B) | Vollaudit, Teilaudit, Abbrechen |
  | Teilaudit: welches Modul | Modul-Namen aus dem Router des Profils (BPM: INDEX.md; Heidi: Karte/Backend/Doku/Tools) |
  | Vollaudit-Warnung vor Start | Starten, Als Teilaudit starten, Abbrechen |
  | Nach dem Report: was mit den Befunden | Als Tasks anlegen (tracker), An code-erstellen/doc-pflege/skill-pflege, Nur Report |

  Prosa nur bei einer offenen Frage ohne feste Optionen oder wenn der Nutzer eine Präferenz signalisiert hat.
- **Branch** nach der Branch-Policy im Skill-Profil der `CLAUDE.md`: `current` → der aktuelle Branch aus der Shell
  (`git branch --show-current`); `fixed:<branch>` → der aktuelle Branch muss dieser sein, sonst Auswahlfrage
  (auf dem aktuellen Branch prüfen / abbrechen). Ohne Shell gilt bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage. Ohne Skill-Profil: Branch aus Chat-Kontext verwenden; mit Shell (Claude Code:
  Bash/PowerShell, Cowork: DC) `git branch --show-current`; ohne Shell und unbekannt: Auswahlfrage mit den
  Branch-Namen aus `git branch -a`. NIE automatisch einen Branch annehmen.

## Arbeitsverzeichnis (PFLICHT bei Dateizugriff)

Claude Code: Repo-Wurzel der Sitzung (`git rev-parse --show-toplevel`).
Cowork: bei DC-Operationen Arbeitsverzeichnis nach **cc-steuerung**, Abschnitt „Arbeitsverzeichnis“, ermitteln.

---

## Profile laden (Pflicht vor jedem Audit)

1. `CLAUDE.md` des Repos, Abschnitt `## Skill-Profil` (Spezifikation `docs/skill-profile-v1.md` im
   Skill-Repo). Pflichtfelder für audit: die Grundfelder, `Doku.Router`, `Doku.Validierungsregeln`;
   `Code.Architekturregeln`, wenn Code geprüft wird; `Tracker.Config`, wenn der Tracker geprüft wird.
   Dazu, was die Module brauchen: `Code.Stacks`, `Code.Aufgabenquelle`, `Doku.Pflichtdokumente`, im
   Skill-Repo der Check `skill-validation` unter `### Checks`. Fehlt ein Pflichtfeld oder steht es auf
   `fehlt`: genau dieses Feld melden und nach `docs/skill-profile-v1.md`, Abschnitt „Fehlende Werte“,
   fragen; das Profil ergänzt nicht audit, sondern doc-pflege (Projekt-Init) oder der Nutzer.
2. Fehlt der Abschnitt: `## Doku-Profil` (Feld „Validierung“, Pflicht-Docs, Router)
   und `## Code-Profil` (Schichten/Kopplung, Aufgabenquelle, Stacks, Tests)
3. Stack-Referenzen `skills/code-erstellen/references/stacks/<key>.md` für jeden Schlüssel in
   `Code.Stacks` bzw. `Stacks:`
4. Fehlt auch das Doku-Profil: `INDEX.md` + `DOC-STANDARD.md` (BPM-Weg). Fehlt beides: Auswahlfrage
   „Profil anlegen (doc-pflege, Projekt-Init)“ / „Ohne Profil, ich nenne die Docs“ – nie raten.

## Doc-Laderegel

Ladereihenfolge des Doku-Profils. BPM (DOC-STANDARD.md Kapitel 8):
1. INDEX.md → Routing
2. Frontmatter + Quickload → Filter
3. Fachliche Invarianten → Prüfen
4. Langform nur bei Bedarf

Heidi: CLAUDE.md → HANDOFF 3e/4 → Bauplan Statusliste (1), Regeln (2), Vertrag (4) → Karten (8)
nur für die geprüften Schritte → 10/10a für Befunde und Register.

---

## 2 Modi

### Modus A — Vollaudit
Alle Module (Modul 7 nur im Skill-Repo). Token-intensiv — vor Start per Auswahlfrage bestätigen lassen.

### Modus B — Teilaudit
Nur relevantes Modul.

---

## Ablauf

### Schritt 1: Profile und Router laden (Abschnitt „Profile laden“)
### Schritt 2: Prüfmodule – je Modul die neutrale Frage, darunter die Prüfpunkte je Projekt (BPM als Beispiel, Heidi aus den Profilen)

---

### Modul 1 — Router-Selbst-Check

Neutral: Zeigt der Router des Profils nur auf Dinge, die es gibt, und im richtigen Format?

BPM (INDEX.md):
- Routing-Einträge → Docs existieren?
- Code Entry Points → Dateien existieren?
- Referenzimplementierungen → existieren?
- Routing-Format korrekt (Primary/Secondary/Reference)?
- historical Docs als Primary? → ❌

Heidi (CLAUDE.md „Repo-Aufbau“, HANDOFF Abschnitt 5, Bauplan Abschnitt 5 Zielstruktur):
- Genannte Pfade, Werkzeuge und Docs existieren (`tools/*.ps1`, `docs/dreame_x60/*.md`, `heidi/archiv/`)?
- Profile in der CLAUDE.md vollständig (Commit, Tracker, Code, Doku) und untereinander widerspruchsfrei (Modulnamen, Testbefehl, Pfade)?
- Zielstruktur (Abschnitt 5) ↔ tatsächliche Ordner `src/{domain,ha,components,shared,styles}`?

---

### Modul 2 — Kern-Docs vs. Code (vorwärts)

Neutral: Stimmt das, was die Kern-Docs versprechen, im Code?

BPM:
#### 2a. DB-Schema-Check
#### 2b. DSGVO-Check
#### 2c. Architektur-Check
#### 2d. UI-Konsistenz-Check

Heidi:
#### 2a. Vertrag → Code: jede Entität/jeder Dienst aus Bauplan Abschnitt 4 ist in `contract.ts` erreichbar (`ENTITIES`, `ROBOT_FEATURES`, `roomEntity`, `SERVICES`)
#### 2b. Verbotenes im Repo: `H:\.storage`, `secrets.yaml`, Datenbanken, `prognose/presence_log.csv`, `prognose/runlog.csv`, `access_token`/GPS in Fixtures und Abzügen → jeder Treffer ❌
#### 2c. Regeln Abschnitt 2 im Code: kein `shouldUpdate` in der Shell; Schreiben nach HA nur über `DxApi`; Komponenten lesen nur Views aus Selektoren; keine externen Ressourcen; nichts fest verdrahtet, was Roboter/HA liefern (Räume, Optionen, Namen)
#### 2d. Statusliste → Code: jeder Schritt `fertig`/`eingespielt` hat Dateien, Tests (`tests/unit`, `tests/e2e`) und einen Commit; `offen` hat keinen Code, der schon behauptet fertig zu sein

---

### Modul 3 — Code vs. Docs (rückwärts)

Neutral: Gibt es im Code etwas, das die Docs nicht kennen?

BPM:
#### 3a. Interface-Implementierung
#### 3b. DI-Registrierung
#### 3c. Dependencies
#### 3d. Code Entry Points

Heidi:
#### 3a. Code → Vertrag: Entitäts-IDs oder Dienste im Code (`contract.ts`, `api.ts`, Paket-YAML), die in Abschnitt 4 fehlen
#### 3b. Komponenten ohne Karte: `src/components/dx-*.ts` ohne Aufgabenkarte in Abschnitt 8 bzw. ohne Eintrag in Abschnitt 7
#### 3c. Selektoren: jeder `memoizeSelector` in `ALL_SELECTORS`; `ids` vollständig (Proxy-Test vorhanden)
#### 3d. Abhängigkeiten: `package.json` ↔ Bauplan Abschnitt 3 (Lit, esbuild, Playwright; keine ungenannten Laufzeit-Abhängigkeiten); Version in `package.json`, Lock und Ressourcen-`?v=` gleich

---

### Modul 4 — Referenz-Docs

Neutral: Sind die Begleit-Docs aktuell und vollständig?

BPM:
#### 4a. ADR-Status
#### 4b. CHANGELOG-Vollständigkeit
#### 4c. BACKLOG-Aktualität

Heidi:
#### 4a. PD-Register (10a): jede Abweichung von v1, die im Code oder in Abschnitt 10 genannt ist, hat einen Eintrag mit Status `freigegeben`; kein Eintrag `offen` älter als der zugehörige Bauschritt
#### 4b. HANDOFF 3e/4: nennt letzten abgeschlossenen Bauschritt und aktuelle Version; offene Punkte haben ClickUp-Bezug oder Begründung
#### 4c. Plan-Docs (GERAETEPROFIL, PLANER-NACHHOLEN, UX-TRANSITIONS, ENTITAETEN): Stand-Datum vorhanden, „So funktioniert es heute“ stimmt mit dem Code

---

### Modul 5 — Aufgabenquelle ↔ Tracker

Neutral: Sagen Aufgabenquelle und Tracker dasselbe?

BPM:
- Module/ vs. Konzepte/ Zuordnung
- INDEX Routing vollständig?
- ClickUp-Tasks (BPM-NNN) ↔ BACKLOG

Heidi:
- Bauplan Statusliste (Abschnitt 1) ↔ ClickUp `DX-NNN`-Status (Mapping aus `projects/heidi/clickup-lists.md`: fertig→shipped/testing, in Arbeit→in development, offen→backlog); Abweichung ⚠️, fehlende Aufgabe ❌
- Jede Aufgabenkarte hat eine DX-Aufgabe und umgekehrt (Phasen ausgenommen)
- Notizen in Abschnitt 10 mit Format `- [Datum] [Aufgabe] Art · Schwere: … Entscheidung Herbert: …`; Wünsche mit Post-2.0-Task
(ClickUp lesen über den tracker-Skill, read-only: `clickup_filter_tasks`, `clickup_get_task`)

---

### Modul 6 — Formale Doc-Prüfung nach Profil

Neutral: Halten die Docs die Validierungsregeln des Projekts ein?

Die Prüfregeln stehen in `Doku.Validierungsregeln` des Skill-Profils (ohne Skill-Profil: Feld
„Validierung“ des Doku-Profils). Führt das Projekt dort keine, gelten die Prüflisten in
[references/doku-validierung.md](references/doku-validierung.md): je Projekt Stufe A (Blocker) und
Stufe B (Warnung) sowie die Kurzprüfung.

---

### Modul 7 — Skills (im Skill-Repo)

Neutral: Passen die Skills zu INDEX und Qualitätsregeln?

Nur im Skill-Repo (Repo mit `skills/<name>/SKILL.md` und `docs/skill-quality.md`); sonst entfällt
das Modul.

- **Mechanik:** Check `skill-validation` des Skill-Profils, mit JSON-Bericht in eine Datei außerhalb
  des Repos (audit schreibt nichts ins Repo). Fehler → ❌, Warnungen → ⚠️.
- **Urteil** nach `docs/skill-quality.md`, Abschnitt „Urteil – audit“: Description zu breit oder zu
  eng, Kollisionen mit anderen Skills, Neutralität, inhaltliche Doppelungen, Schnitt Kern/References,
  Eval-Fälle realistisch.
- **INDEX ↔ Descriptions:** Skill-Tabelle der `INDEX.md` gegen die Descriptions – jeder Ordner unter
  `skills/` hat eine Zeile und umgekehrt; Zuständigkeit und Auslöser der Zeile decken sich mit der
  Description.
- **Befunde** → skill-pflege bzw. `tracker issue <skill>` (Abschnitt „Nach dem Report“).

---

## Report-Format

Befunde immer mit Datei und Stelle (Zeile oder Abschnitt), damit der Fix-Skill direkt hinspringen kann.

```
🔍 Audit-Report [Projekt] ([Datum]) — Modus A/B, Profile: Doku ✓ Code ✓ Stacks: <keys>
═══════════════════════════════════

📊 Zusammenfassung: X ✅ | Y ⚠️ | Z ❌

─── Modul 1–5 ───

──────────────────────────────────
Modul 6 — Frontmatter + Quickload
──────────────────────────────────
❌ [Doc]: [Problem]
⚠️ [Doc]: [Warnung]
✅ [Doc]: OK

═══════════════════════════════════
📝 Empfohlene Aktionen:
═══════════════════════════════════
1. ❌ [Aktion]
2. ⚠️ [Aktion]
```

---

## Ampel

| ✅ | Konsistent | — |
| ⚠️ | Inkonsistenz | Sollte korrigiert werden |
| ❌ | Fehler | Muss korrigiert werden |

---

## Nach dem Report: Befunde weitergeben

audit ändert nichts – aber es lässt die Befunde nicht im Chat liegen. Direkt nach dem Report
eine Auswahlfrage:

- **„Als Tasks anlegen“** → `tracker neu` (Schema und Präfix des Projekts, z.B. `DX-NNN | DOKU | Audit: …`).
  Ein Sammel-Task pro Modul mit den Befunden als Checkliste in der Beschreibung; ❌-Befunde mit
  Priorität `high`, ⚠️ `normal`. Bei ≤ 3 Befunden auch je Befund ein Task (Auswahlfrage).
  Alle ClickUp-Operationen über den tracker-Skill, nie direkt.
  Skill-Befunde (Modul 7) stattdessen als `tracker issue <skill>: Audit: …`, je Skill ein Issue mit
  den Befunden als Checkliste.
- **„An code-erstellen / doc-pflege / skill-pflege“** → Befunde als Aufgabenliste an den Fix-Skill
  übergeben (Code-Befunde → code-erstellen, Doc-Befunde → doc-pflege, Abschnitt „Doku pflegen“,
  Skill-Befunde → skill-pflege); der Fix-Skill startet erst nach eigener Bestätigung.
- **„Nur Report“** → Report bleibt; Hinweis, dass Befunde ohne Task beim nächsten Audit wieder auftauchen.

Bei Heidi zusätzlich: Befunde, die eine Entscheidung von Herbert brauchen (Regel-Widerspruch,
Abweichung von v1), als Notiz-Vorschlag für Bauplan Abschnitt 10 formulieren (Art `Widerspruch`,
Entscheidung offen) – eintragen tut doc-pflege, nicht audit.

---

## Tool-Strategie

- Frontmatter/Quickload (BPM): Nur erste 30 Zeilen jeder Doc; Heidi: Statusliste, Abschnitt 4 und 10a gezielt lesen, Karten nur für geprüfte Schritte
- Existenz: Cowork `list_directory`, Claude Code `Glob`
- Content: Cowork `start_search`, Claude Code `Grep` (Muster: Entitäts-IDs, `shouldUpdate`, `callService`, `access_token`, `latitude`)
- ClickUp (Modul 5): read-only über tracker (`clickup_filter_tasks` mit `include_closed: true`)
- Teilaudit: max 10 Tool-Calls (Claude Code: Grep-Läufe zählen je einer)
- Vollaudit: max 35 Tool-Calls; bei Heidi vorher `npm test`-Ergebnis vom User erfragen statt selbst zu bauen (read-only)

---

## VERBOTEN

- Dateien ändern (read-only)
- Annahmen ohne Dateien
- False Positives als Fehler
- Vollaudit ohne Auswahlfrage-Vorwarnung
- Ladereihenfolge des Profils ignorieren (BPM: Quickload-Laderegel)
- Prosa-Fragen bei festen Entscheidungsoptionen (Modus-Auswahl, Modul-Auswahl für Teilaudit)
- Branch automatisch annehmen (Branch-Policy lesen, Shell fragen oder Auswahlfrage)
- Eigene Prüfregeln erfinden statt Skill-Profil (bzw. Doku-/Code-Profil), Stack-Referenzen und
  `references/doku-validierung.md` zu lesen
- BPM-Prüfpunkte (DB-Schema, DI, Frontmatter) auf ein Projekt anwenden, das sie laut Profil nicht hat
- Befunde ohne Datei und Stelle melden
- Report beenden ohne Auswahlfrage „Tasks / Fix-Skill / Nur Report“
- ClickUp direkt schreiben (Tasks nur über tracker, und nur nach Auswahlfrage)
