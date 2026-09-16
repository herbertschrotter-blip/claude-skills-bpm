---
name: audit
description: >
  Prüft read-only die Konsistenz zwischen Code und Projektdokumentation nach
  Doku- und Code-Profil des Repos (BPM: INDEX-Routing, Frontmatter, Quickloads;
  Heidi: Bauplan-Statusliste, Entitäts-Vertrag ↔ contract.ts, HANDOFF,
  PD-Register). Use when users want a consistency audit, a documentation-vs-code
  check, a Frontmatter or Quickload validation, a Bauplan check, or a systematic
  read-only review of project rules. Do not trigger for code
  implementation, build debugging, or general code review without doc/context
  comparison.
---

# Audit-Skill — Projekt-Konsistenz-Prüfung

## Zweck

Prüft ob Code und Docs konsistent sind. **Was** geprüft wird, steht in den Profilen des
Repos (CLAUDE.md): Feld „Validierung“ des **Doku-Profils**, „Schichten / Kopplung“ und
„Aufgabenquelle“ des **Code-Profils**, dazu die Stack-Referenzen von code-erstellen
(`references/stacks/<key>.md`) für die Code-Seite. audit führt keine eigenen Prüfregeln;
es ist der Read-only-Läufer über diese Regeln. BPM: INDEX-Routing, Frontmatter, Quickload,
Schema, DI. Heidi: Bauplan, Vertrag, HANDOFF, PD-Register.

---

## Vorrang / Delegation an andere Skills

**audit ist strikt read-only. Wenn die Hauptabsicht ein Fix, eine
Implementierung oder eine Doc-Pflege ist, NICHT hier weiterarbeiten,
sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Code schreiben oder ändern (Fix, Feature, Refactor) | **code-erstellen** |
| Doku schreiben, ADR, Konzept, Frontmatter-Pflege | **doc-pflege** |
| UI-Entwurf als HTML-Mockup | **mockup-erstellen** |
| Commit-Befehl, Commit-Message | **git-commit-helper** |
| ClickUp-Task-Aktion | **tracker** |

Nur wenn die Hauptabsicht **read-only Konsistenzprüfung** ist
(Audit-Report, Frontmatter-Check, Code-vs-Doc-Abgleich, INDEX-Validierung),
bleibt audit zuständig.

**Wichtig:** Nach einem Audit-Report bietet audit KEINE Fixes selbst an.
Die im Report empfohlenen Aktionen werden per Auswahlfrage an
den passenden Skill delegiert (code-erstellen für Code-Fixes, doc-pflege
für Doc-Fixes) oder als Aufgaben über **tracker** angelegt (Abschnitt
„Nach dem Report“). audit ist der Analyse-Skill, nicht der Fix-Skill.

---

## 🚨 VERBINDLICHE REGEL: Auswahlfrage bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS eine Auswahlfrage
gestellt werden — KEINE Prosa-Fragen.** Auswahlfrage = Frage-Werkzeug der Umgebung
mit anklickbaren Optionen (Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion`).

### Diese Fragen IMMER als Auswahlfrage:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (nur wenn die Shell ihn nicht liefert) | Branch-Namen aus `git branch -a` |
| Modus-Auswahl (A oder B) | Vollaudit, Teilaudit, Abbrechen |
| Teilaudit: welches Modul | Modul-Namen aus dem Router des Profils (BPM: INDEX.md; Heidi: Karte/Backend/Doku/Tools) |
| Vollaudit-Warnung vor Start | Starten, Als Teilaudit starten, Abbrechen |
| Nach dem Report: was mit den Befunden | Als Tasks anlegen (tracker), An code-erstellen/doc-pflege, Nur Report |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen
- User hat Präferenz signalisiert

## Branch-Ermittlung

Branch aus Chat-Kontext verwenden. Mit Shell (Claude Code: Bash/PowerShell, Cowork: DC):
`git branch --show-current`. Ohne Shell und unbekannt: Auswahlfrage.
NIE automatisch einen Branch annehmen.

## Arbeitsverzeichnis (PFLICHT bei Dateizugriff)

Claude Code: Repo-Wurzel der Sitzung (`git rev-parse --show-toplevel`).
Cowork: bei DC-Operationen Arbeitsverzeichnis nach **cc-steuerung Kapitel 4** ermitteln.

---

## Profile laden (Pflicht vor jedem Audit)

1. `CLAUDE.md` des Repos: Abschnitte `## Doku-Profil` (Feld „Validierung“, Pflicht-Docs, Router)
   und `## Code-Profil` (Schichten/Kopplung, Aufgabenquelle, Stacks, Tests)
2. Stack-Referenzen `skills/code-erstellen/references/stacks/<key>.md` für jeden Schlüssel in `Stacks:`
3. Fehlt das Doku-Profil: `INDEX.md` + `DOC-STANDARD.md` (BPM-Weg). Fehlt beides: Auswahlfrage
   „Profil anlegen (doc-pflege Modus 0)“ / „Ohne Profil, ich nenne die Docs“ – nie raten.

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
Alle 6 Module. Token-intensiv — vor Start per Auswahlfrage bestätigen lassen.

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

Für die detaillierten Prüfregeln siehe **doc-pflege Modus 6** (Validierung nach Profil;
BPM Stufe A Formal/Blocker, Stufe B Semantisch/Warnung; Heidi-Prüfliste ebendort).

Heidi-Kurzprüfung: Karten mit allen Feldern (Voraussetzung, Ziel, Nicht ändern, Akzeptanz);
Statusliste ohne Lücken; keine Notiz ohne Datum/Art/Schwere; PD-Tabelle vollständig gefüllt.

BPM-Kurzprüfung hier:

#### 6a. Frontmatter-Vollständigkeit
- Frontmatter vorhanden? Pflichtfelder? doc_id eindeutig?

#### 6b. Quickload-Vollständigkeit
- Quickload vorhanden bei source_of_truth/secondary?
- Kapitel-Feld stimmt mit H2s?

#### 6c. Cross-Checks
- INDEX referenziert nur Docs mit gültigem Frontmatter?
- source_of_truth hat Quickload?
- historical NICHT als Primary im Router?
- Keine doppelten doc_ids?
- Fachliche Invarianten nicht widersprüchlich zwischen Docs?

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
- **„An code-erstellen / doc-pflege“** → Befunde als Aufgabenliste an den Fix-Skill übergeben
  (Code-Befunde → code-erstellen, Doc-Befunde → doc-pflege Modus 5/6); der Fix-Skill startet erst
  nach eigener Bestätigung.
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
- Modus-Auswahl als Prosa — IMMER Auswahlfrage
- Modul-Auswahl für Teilaudit als Prosa — IMMER Auswahlfrage
- Branch automatisch annehmen (Shell fragen oder Auswahlfrage)
- Eigene Prüfregeln erfinden statt Doku-/Code-Profil und Stack-Referenzen zu lesen
- BPM-Prüfpunkte (DB-Schema, DI, Frontmatter) auf ein Projekt anwenden, das sie laut Profil nicht hat
- Befunde ohne Datei und Stelle melden
- Report beenden ohne Auswahlfrage „Tasks / Fix-Skill / Nur Report“
- ClickUp direkt schreiben (Tasks nur über tracker, und nur nach Auswahlfrage)
