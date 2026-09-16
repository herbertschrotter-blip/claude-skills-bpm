---
name: doc-pflege
description: >
  Erstellt, aktualisiert und validiert Projektdokumentation nach dem
  Doku-Profil des Repos (BPM: DOC-STANDARD, Frontmatter, Quickload, INDEX.md;
  Heidi: Bauplan, Statusliste, PD-Register, HANDOFF) – projektneutral.
  Use when users want to schreiben, erstellen, pflegen, aktualisieren,
  draften, anlegen, formulieren, dokumentieren, ergänzen, refactoren,
  or validieren documentation — including ADRs, Konzept-Docs, Architektur-
  Docs, Modul-Docs, README, CHANGELOG, BACKLOG, Frontmatter, Quickload,
  Kapitelvorlagen, INDEX.md-Routing, Bauplan-Statuslisten, Handoff-Dokumente,
  or Sitzungsabschluss. Triggers also on bug fixes in documentation (typos,
  broken links, outdated chapters) and structural refactoring of existing docs. Do not trigger for code implementation,
  automatic post-change advisory checks, or generic project discussion
  without explicit doc intent.
---

# Doc-Pflege — Dokumentations-Skill

## Zweck

Stellt Konsistenz der Projektdokumentation sicher. Welche Docs es gibt, wie sie
aufgebaut sind und was geprüft wird, steht im **Doku-Profil** des Projekts
(Abschnitt „Voraussetzung: Doku-Profil“). BPM: Frontmatter, Quickload und
Kapitelstruktur nach DOC-STANDARD.md. Heidi: Bauplan (Statusliste, Aufgabenkarten,
Notizen, PD-Register) und HANDOFF. Initialisiert neue Projekte mit dem Standard-Doc-Set
des Profils. Erzwingt die Vorlagen des Profils bei neuen Docs.

---

## Vorrang / Delegation an andere Skills

**doc-pflege ist für das Schreiben, Validieren und Refactoren von
Projektdokumentation. Wenn die Hauptabsicht Code, Tasks oder andere
Aktionen sind, NICHT hier weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Code schreiben oder ändern (Services, ViewModels, Logik) | **code-erstellen** |
| UI-Entwurf als HTML-Mockup | **mockup-erstellen** |
| Commit-Befehl, Commit-Message, Version-Bump | **git-commit-helper** |
| ClickUp-Task anlegen, updaten, schließen | **tracker** |
| Konsistenzprüfung Code ↔ Docs (read-only) | **audit** |

Nur wenn die Hauptabsicht **echte Doc-Arbeit** ist (neue Doc erstellen,
bestehende Doc refactoren, Frontmatter/Quickload validieren, ADR schreiben,
INDEX.md-Routing pflegen), bleibt doc-pflege zuständig.

**Wichtig:** Code-Änderungen, die "Doc-Folgen" haben (neues Schema,
neue ADR-würdige Entscheidung), werden von code-erstellen oder
git-commit-helper als **Advisory-Hinweise** ausgegeben (siehe Kapitel
"Advisory-Checkliste nach code-relevanten Änderungen"). Diese Hinweise
sind KEIN Trigger für doc-pflege. Der User entscheidet explizit "pflege
jetzt die Doku" bevor doc-pflege selbst übernimmt.

---

## 🚨 VERBINDLICHE REGEL: Auswahlfrage bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS eine Auswahlfrage
gestellt werden — KEINE Prosa-Fragen.** Auswahlfrage = Frage-Werkzeug der Umgebung
mit anklickbaren Optionen (Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion`).

### Diese Fragen IMMER als Auswahlfrage:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (nur wenn die Shell ihn nicht liefert) | Branch-Namen aus `git branch -a` |
| Modus-Auswahl bei Unsicherheit | Modus 0-8 als Optionen |
| Validierungsbefund (Modus 6) mit mehreren Lösungen | Befund je Option: Doc anpassen, Quelle anpassen, Ignorieren mit Begründung |
| Sitzungsabschluss (Modus 8): Aufgabe fertig oder offen? | fertig, offen (Rest im HANDOFF), blockiert (Befund) |
| Refactoring 7b: Inhalt passt in kein Kapitel | Eigenes Kapitel am Ende, Vorhandenes Kapitel erweitern, Abbrechen |
| Doc-Pflege Modus bei doc-relevanter Änderung | Jetzt pflegen, Später als Task anlegen, Ignorieren |
| Schema-/DB-Änderung dokumentieren | "Mit Reset-Anweisung", "Mit Migrations-Kapitel (User will explizit)", "Abbrechen" |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen (z.B. Projektname, Modulname, Freitext-Beschreibung)
- User hat Präferenz signalisiert
- Freitext-Input nötig

---

## Branch-Ermittlung

Branch aus Chat-Kontext verwenden. Mit Shell (Claude Code: Bash/PowerShell, Cowork: DC):
`git branch --show-current`; nennt das Profil einen Pflicht-Branch und der aktuelle weicht ab →
Auswahlfrage. Ohne Shell und unbekannt: per Auswahlfrage fragen.
NIE automatisch einen Branch annehmen.

---

## Arbeitsverzeichnis (PFLICHT bei Dateizugriff)

Claude Code: Repo-Wurzel der Sitzung (`git rev-parse --show-toplevel`).
Cowork: bei DC-Operationen Arbeitsverzeichnis nach **cc-steuerung Kapitel 4** ermitteln.

---

## Voraussetzung: Doku-Profil

Abschnitt `## Doku-Profil` in der `CLAUDE.md` des Repos (Claude Code liest sie automatisch;
Cowork per DC). Felder:

| Feld | Bedeutung | BPM | Heidi |
|------|-----------|-----|-------|
| Doc-Standard | Regelwerk für Aufbau und Validierung | `DOC-STANDARD.md` (Frontmatter, Quickload, Kapitelvorlagen, Ladereihenfolge Kap. 8) | Bauplan selbst (Abschnitt 0–2, Formate in 8/10/10a) |
| Router / Index | Wo steht, welche Doc wofür | `INDEX.md` (Task-to-Doc, Primary/Secondary/Reference) | `CLAUDE.md` (Repo-Aufbau) + `docs/HANDOFF.md` Abschnitt 5 |
| Pflicht-Docs | Dateien mit Pfad (ersetzt die alte Pfadtabelle) | Tabelle unten „Beispiel BPM“ | `docs/dreame_x60/BAUPLAN.md`, `docs/HANDOFF.md`, `CLAUDE.md`, `heidi/CLAUDE.md`, `docs/dreame_x60/*.md` (Pläne) |
| Doc-Typen + Vorlagen | Was neu angelegt wird und wie | ADR, Konzept, Modul-Doc, Architektur (Kapitelvorlagen Kap. 7) | Aufgabenkarte (Voraussetzung/Ziel/Nicht ändern/Akzeptanz/Tests/Dateien), Notiz Abschnitt 10 (Datum/Aufgabe/Art/Schwere/Text/Entscheidung), PD-Eintrag 10a (id/bereich/v1/v2/grund/spec_test/Status), Plan-Doc (Stufen, Stand) |
| Validierung (Modus 6) | Was geprüft wird | Frontmatter/Quickload Stufe A/B | Statusliste ↔ ClickUp ↔ Code; PD-Register vollständig; Notizformat; HANDOFF 3e aktuell; Abschnitt 4 ↔ contract.ts |
| Frühphasen-Regel | Reset statt Migration dokumentieren | ja (INDEX.md Kapitel „Projekt-Phase“) | nein – stattdessen Regel: Abweichung von v1 nur mit PD-Eintrag |
| Advisory | Doku-Folgen nach Code-Änderung | Doku-Checkliste des Commit-Profils | Doku-Checkliste des Commit-Profils |
| Sitzungsabschluss (Modus 8) | Was am Ende jeder Sitzung zu tun ist | Handover via chat-wechsel | Statusliste, HANDOFF 3e, offene Punkte Abschnitt 4, Commit + Push |
| Commit-Modul | Modulname für Doku-Commits | `Docs` | `Doku` |

**Fehlt das Profil:** `INDEX.md` + `DOC-STANDARD.md` im Repo als Profil nehmen (BPM-Weg).
Fehlt auch das: Auswahlfrage „Profil anlegen (Vorschlag aus dem Repo)“ / „Ohne Profil, ich nenne die Docs“.

---

## Konkrete Pfade (Beispiel BPM – für andere Projekte gilt das Doku-Profil)

| Datei | Pfad im Repo |
|-------|-------------|
| INDEX.md | `/INDEX.md` (Repo-Root) |
| DOC-STANDARD.md | `/Docs/Referenz/DOC-STANDARD.md` |
| BACKLOG.md | `/Docs/Kern/BACKLOG.md` |
| ADR.md | `/Docs/Referenz/ADR.md` |
| DB-SCHEMA.md | `/Docs/Kern/DB-SCHEMA.md` |
| CHANGELOG.md | `/Docs/Referenz/CHANGELOG.md` |
| DEPENDENCY-MAP.md | `/Docs/Referenz/DEPENDENCY-MAP.md` |
| VISION.md | `/Docs/Referenz/VISION.md` |
| Architektur-Doc | `/Docs/Kern/BauProjektManager_Architektur.md` |
| CODING_STANDARDS.md | `/Docs/Kern/CODING_STANDARDS.md` |
| DSVGO-Architektur.md | `/Docs/Kern/DSVGO-Architektur.md` |

---

## Doc-Laderegel

Dieser Skill liest Docs nach der Ladereihenfolge des Doku-Profils.

BPM (DOC-STANDARD.md Kapitel 8):
1. INDEX.md → Routing
2. Frontmatter + Quickload → Filter
3. Fachliche Invarianten → Prüfen
4. Pflichtlesen → Laden wenn betroffen
5. Langform nur bei Bedarf

Heidi:
1. CLAUDE.md (automatisch) → Repo-Aufbau, Profile
2. HANDOFF.md Abschnitt 3e + 4 → Stand und offene Punkte
3. BAUPLAN.md Statusliste (Abschnitt 1) → welche Aufgabe, welcher Status
4. Nur die betroffene Aufgabenkarte (Abschnitt 8) und Regeln (Abschnitt 2)
5. Abschnitt 10/10a nur, wenn Befund oder Abweichung einzutragen ist

---

## Frühphasen-Regel (PFLICHT bei Schema-/Config-/DB-Doku, wenn das Profil sie führt)

Gilt für Projekte mit „Frühphasen-Regel: ja“ im Doku-Profil (BPM). INDEX.md hat dort das
Kapitel "Projekt-Phase (VERBINDLICH)". Solange dieses Kapitel besteht, gilt für die Doku von
Schema-/Config-/DB-Änderungen:

**Statt Migrations-Kapitel → Reset-Anweisung dokumentieren.**

Wenn z.B. DB-SCHEMA.md, ADR.md oder ein Konzept-Doc eine Schema-Änderung
beschreibt, NICHT formulieren wie "Migration von Schema v2 auf v3":

❌ Falsch:
> Migration von SchemaVersion 2 auf 3:
> 1. ALTER TABLE plans ADD COLUMN ...
> 2. UPDATE plans SET ... WHERE schema_version = 2
> 3. UPDATE plans SET schema_version = 3

✅ Richtig:
> Schema-Änderung von 2 auf 3 (Frühphase, keine Migration):
> Betroffene Datei(en): bpm.db
> Aktion: User löscht bpm.db → BPM erstellt sie beim nächsten Start neu mit Schema v3.

Gleiches gilt für JSON-Configs (`profiles/*.json`, `manifest.json`, `settings.json`):
betroffene Datei nennen, User löscht sie, App erstellt sie neu.

**Ausnahme:** Wenn der User explizit "Migration dokumentieren" sagt
oder das Frühphasen-Kapitel in INDEX.md offiziell entfernt wurde.

**Heidi hat statt der Frühphasen-Regel die Paritätsregel:** Jede gewollte Abweichung vom
v1-Verhalten braucht einen PD-Eintrag in Abschnitt 10a mit Status `freigegeben` (Herbert);
ohne Eintrag ist eine Abweichung ein Fehler. Neue Entität oder Dienst → Abschnitt 4 des
Bauplans **und** `contract.ts` im selben Commit.

---

## Advisory-Checkliste nach code-relevanten Änderungen

**Dieser Abschnitt ist KEIN Trigger.**
Er wird von anderen Skills nach einer Änderung als **Nachlauf-Checkliste** genutzt.
Der User-Intent für doc-pflege steht ausschließlich in der Frontmatter-Description.
Die hier beschriebene Checkliste wird passiv konsumiert (z.B. durch code-erstellen
oder git-commit-helper), sie aktiviert doc-pflege nicht selbst.

### Quelle der Checkliste: das Commit-Profil

Die Nachlauf-Checkliste ist die **Doku-Checkliste des Commit-Profils** (Abschnitt
`## Commit-Profil` in der CLAUDE.md, gepflegt vom git-commit-helper). Dieser Skill führt keine
eigene Liste; er liest dieselbe. Beispiel BPM: Neue Tabelle → DB-SCHEMA.md; Architektur-
entscheidung → ADR.md; neuer Entry Point → INDEX.md; neues Doc → INDEX.md + BACKLOG.md.
Beispiel Heidi: Bauschritt fertig → Statusliste; Befund/Entscheidung → Abschnitt 10 (Abweichung →
10a); Stand geändert → HANDOFF 3e; neue Entität/Dienst → Abschnitt 4 + contract.ts.

### Typische Fälle (Change-Class-basiert)

Die Nachlauf-Checkliste wird nach doc-relevanten Änderungen durchlaufen:
- Neue Tabelle / Schemaänderung / neue Entität im Vertrag
- Neue Architekturentscheidung / Paritätsabweichung
- Neuer Code-Entry-Point (neues Interface, neuer Service, neuer Dialog, neue Komponente)
- Neues Modul / neuer Workflow mit Benutzerwirkung
- Neue Abhängigkeit (NuGet, npm, Projektreferenz)
- Neues Doc / Doc-Refactor
- Bauschritt abgeschlossen (Statusliste, Aufgabenquelle)

### NICHT triggern bei:

- Lokale UI-Textfixes, Styling-Änderungen
- Kleine Refactors ohne Verhaltensänderung
- Umbenennungen ohne Strukturwirkung
- Reine Formatierungen
- Explorative Zwischenstände
- Bug-Fixes die keine Architektur berühren

### Format: Advisory (nicht interruptiv)

Statt voller Checkpoint-Checkliste → kurze Merkliste am Ende der Antwort:

```
📝 Doc-Hinweis: [DB-SCHEMA.md — neue Spalte angelegt]
📝 Doc-Hinweis: [ADR.md — neue Architekturentscheidung]
```

Nur zutreffende Punkte. Keine Checkliste mit 10 leeren Punkten.
Der User entscheidet ob und wann die Doc-Pflege erfolgt.

---

## 8 Modi

### Modus 0 — Projekt-Init (Standard-Doc-Set)

**Wann:** "neues Projekt", "init projekt", kein Doku-Profil und keine INDEX.md vorhanden.

Für Details siehe `references/projekt-init.md` (falls vorhanden)
oder DOC-STANDARD.md Kapitel 3 (BPM).

Kurzablauf:
1. Grundinfos sammeln (Projektname, Tech-Stack, Repo, DB?, Aufgabenquelle, Auslieferung)
2. Repo scannen
3. **Doku-Profil in der CLAUDE.md anlegen** (Felder oben) – zusammen mit Commit-, Tracker- und Code-Profil, wenn die fehlen
4. Standard-Doc-Set laut Profil generieren (BPM: INDEX.md, Architektur.md, BACKLOG.md, CHANGELOG.md, ADR.md, DEPENDENCY-MAP.md, ggf. DB-SCHEMA.md; Heidi-artig: CLAUDE.md, HANDOFF.md, BAUPLAN.md mit Statusliste/Regeln/Vertrag/Aufgabenkarten/Notizen/Register)
5. Korrekte Vorlagen des Profils (BPM: Frontmatter + Quickload + Kapitelstruktur)
6. Invarianten-Check
7. Paket dem User vorlegen

---

### Modus 1 — Index Sync

**Wann:** Neues Doc, Doc umbenannt, neuer Code-Entry-Point.

Router des Profils laden und Eintrag nachziehen. BPM: INDEX.md, Routing-Eintrag im
Primary/Secondary/Reference-Format. Heidi: CLAUDE.md „Repo-Aufbau“ und HANDOFF Abschnitt 5
(Referenzen); neue Plan-Docs unter `docs/dreame_x60/` dort verlinken.

---

### Modus 2 — Companion Docs Check

**Wann:** Neue Tabelle, Feature, Architekturentscheidung, Abhängigkeit, neue Entität.

Doku-Checkliste des Commit-Profils → betroffene Pflicht-Docs ändern (BPM: INDEX.md → Doc-Pflege
Policy; Heidi: Abschnitt 4 + Abschnitt 10/10a + HANDOFF).

---

### Modus 3 — Passive Advisory

**Wann:** code-erstellen hat DocMaintenanceHints ausgegeben.

Hints konsumieren, Hinweise ausgeben.

---

### Modus 4 — Automatischer Checkpoint (Advisory)

**Wann:** Nach doc-relevanten Änderungen (siehe Abschnitt "Advisory-Checkliste nach code-relevanten Änderungen" oben — Nachlauf-Checkliste, kein Trigger).

Kurze Advisory-Merkliste ausgeben.
NICHT bei trivialen Änderungen.
NICHT den Arbeitsfluss unterbrechen.

---

### Modus 5 — Explicit Doc Maintenance

**Wann:** "pflege die Doku", "aktualisiere alles".

Volle Prüfung aller Pflicht-Docs des Profils + Validierung nach Modus 6.

---

### Modus 6 — Validierung nach Profil

**Wann:** "prüfe frontmatter", "quickload check", "prüfe die doku", "stimmt der bauplan", oder explizit angefordert.

Die Prüfliste kommt aus dem Feld „Validierung“ des Doku-Profils. Befunde als Tabelle
(Doc, Stelle, Befund, Vorschlag); bei mehreren Lösungen Auswahlfrage. Nichts stillschweigend
korrigieren, was eine Entscheidung des Users ist (Status, Freigaben).

#### Heidi-Prüfliste (aus dem Doku-Profil)

Stufe A — Blocker:
- Statusliste (Bauplan Abschnitt 1) ↔ ClickUp-Status (DX-Aufgaben) ↔ Code: fertig nur, wenn Code, Tests und Commit da sind
- Jede Abweichung von v1 hat einen PD-Eintrag in 10a mit Status `freigegeben`
- Abschnitt 4 (Entitäts-Vertrag) ↔ `contract.ts`: gleiche Entitäten, gleiche Dienste
- HANDOFF Abschnitt 3e nennt den letzten abgeschlossenen Bauschritt und die aktuelle Version
- Nichts Verbotenes im Repo (Token, GPS, `.storage`, Datenbanken, Laufprotokolle)

Stufe B — Warnung:
- ⚠️ Notiz in Abschnitt 10 ohne Datum, Aufgabe, Art oder Schwere; Entscheidung Herbert fehlt bei Widerspruch/Wunsch
- ⚠️ Aufgabenkarte ohne Akzeptanz oder ohne Tests
- ⚠️ Offene Punkte (HANDOFF Abschnitt 4) ohne Gegenstück in ClickUp
- ⚠️ Plan-Doc (GERAETEPROFIL, PLANER-NACHHOLEN, UX-TRANSITIONS) ohne Stand-Datum
- ⚠️ Version in package.json, Lock und Ressourcen-`?v=` uneinheitlich

#### BPM-Prüfliste: Frontmatter + Quickload

##### Stufe A — Formal (Blocker)

- Frontmatter vorhanden bei Kern/, Module/, Referenz/?
- Alle Pflichtfelder?
- doc_id eindeutig?
- Enums korrekt?
- Quickload bei source_of_truth/secondary?
- Quickload Kapitel-Feld stimmt mit H2s?
- Kapitelreihenfolge nach Vorlage?
- Pflichtlesen verweist auf existierende Kapitel?
- Fachliche Invarianten max 5?

##### Stufe B — Semantisch (Warnung)

- ⚠️ Quickload Kapitel stimmt nicht mit H2s
- ⚠️ historical als Primary im Router
- ⚠️ related_docs nicht existent
- ⚠️ Kapitelvorlage nicht eingehalten
- ⚠️ Fachliche Invarianten leer bei großem Modul
- ⚠️ Pflichtlesen leer bei source_of_truth Modul

---

### Modus 7 — Neue Doc erstellen oder Refactoring

**Wann:** "neues Konzept für X", "erstelle Modul-Doc für Y",
"refactore PlanManager.md nach Standard", "docs umbauen",
oder wenn in Modus 0/2 ein neues Doc entsteht.

#### 7a. Neue Doc erstellen

1. Vorlage für den Doc-Typ aus dem Profil laden (BPM: DOC-STANDARD.md Kapitel 7; Heidi: Muster im Bauplan – Aufgabenkarte, Notiz, PD-Eintrag, Plan-Doc)
2. Router laden → verwandte Docs identifizieren (BPM: INDEX.md; Heidi: CLAUDE.md, HANDOFF 5)
3. Quickloads verwandter Docs lesen → Fachliche Invarianten sammeln
4. Doc mit korrektem Frontmatter + Quickload + Kapitelstruktur erstellen
5. Invarianten-Check durchführen:

```
📋 Invarianten-Check:
- Gibt es fachliche Regeln die bei JEDER Änderung gelten?
  → Fachliche Invarianten im Quickload
- Welche Kapitel müssen IMMER gelesen werden?
  → Pflichtlesen im Quickload
- Gibt es Abhängigkeiten zu anderen Modulen?
  → related_docs im Frontmatter
```

6. INDEX.md Routing-Eintrag vorschlagen

#### 7b. Bestehendes Doc refactoren

1. Vorlage für den Doc-Typ aus dem Profil laden (BPM: DOC-STANDARD.md)
2. Bestehende Doc komplett laden
3. Inhalt auf die Standard-Kapitel mappen
4. Frontmatter + Quickload ergänzen oder aktualisieren
5. Invarianten-Check (siehe oben)
6. Vollständigkeits-Check gegen das Original

**REFACTORING-INVARIANTE (HARTE REGEL):**
- KEIN Inhalt darf gelöscht oder gekürzt werden — nur umordnen
- Inhalt der in kein Standard-Kapitel passt → eigenes Kapitel am Ende
- Nach dem Refactoring: Abschnitt-für-Abschnitt prüfen ob alles
  aus dem Original in der neuen Struktur vorhanden ist
- Im Zweifel lieber ein Kapitel zu viel als Inhalt verlieren

**VERBOTEN:** Doc ohne die Vorlage des Profils erstellen (BPM: Frontmatter, Quickload, Kapitelvorlage; Heidi: Karten-/Notiz-/PD-Format).
**VERBOTEN:** Beim Refactoring Inhalte weglassen, kürzen oder zusammenfassen.

---

### Modus 8 — Sitzungsabschluss

**Wann:** "sitzung abschließen", "wir hören auf", "stand festhalten", nach dem letzten `tracker done`
einer Sitzung, oder wenn der Bauplan/das Profil es am Ende jeder Sitzung verlangt (Heidi: Startprompt
Abschnitt 0). Ersetzt nicht chat-wechsel (Übergabeprompt für den nächsten Chat), sondern liefert ihm zu.

Ablauf (Orte aus dem Profil, Feld „Sitzungsabschluss“):
1. **Aufgabenquelle/Statusliste** nachziehen: jede in der Sitzung angefasste Aufgabe hat den richtigen
   Status (Heidi: Bauplan Abschnitt 1 ↔ ClickUp DX-Status; fertig / offen / blockiert per Auswahlfrage,
   wenn unklar)
2. **Befunde und Entscheidungen** eintragen (Heidi: Abschnitt 10, Abweichungen 10a; BPM: ADR/BACKLOG)
3. **Stand-Abschnitt** schreiben (Heidi: HANDOFF 3e – Version, was gebaut, Stolpersteine; Datum)
4. **Offene Punkte** als Checkliste (Heidi: HANDOFF Abschnitt 4), erledigte abhaken, neue ergänzen,
   jede mit ClickUp-Bezug oder Begründung, warum ohne
5. Doku-Checkliste des Commit-Profils durchgehen (nichts vergessen: Abschnitt 4, INDEX, CHANGELOG)
6. Commit `[vX.Y.Z] <Doku-Modul>, Docs: Sitzungsabschluss <Datum> – <Kurztitel>` + Push (git-commit-helper)
7. Kurzer Abschlussbericht im Chat: erledigt / offen / nächster Schritt – derselbe Text taugt als
   Einstieg für chat-wechsel

**VERBOTEN:** Sitzung beenden mit uncommitteten Doku-Änderungen; Statusliste „fertig“ ohne Tests und Commit;
offene Punkte nur im Chat statt im Doc.

---

## Ausgabeformat

- Claude Code: Dateien direkt ändern (Edit/Write); Cowork: SUCHE/ERSETZE oder DC
- Neue Docs komplett mit der Vorlage des Profils (BPM: Frontmatter + Quickload + Kapitelstruktur)
- Commit: `[vX.Y.Z] <Doku-Modul des Commit-Profils>, Docs: [Kurztitel]` (BPM: `Docs`, Heidi: `Doku`)

---

## Skill-Governance

Bei jeder Änderung an diesem Skill prüfen:
1. Trigger zu breit geworden?
2. Redundanz zu anderer Skill-Regel entstanden?
3. Negativgrenzen noch korrekt?
4. DOC-STANDARD / INDEX / Doku-Profil betroffen?
5. Split-Prüfung (skill-pflege Regel 21): Modi noch in einer Datei sinnvoll?

---

## VERBOTEN

- Frei inferieren welche Docs betroffen sind — Doku-Profil und Doku-Checkliste des Commit-Profils lesen
- Docs ohne Frontmatter in Kern/Module/Referenz akzeptieren (BPM)
- Neue Docs ohne die Vorlage des Profils erstellen
- Modus 4 bei trivialen Änderungen triggern
- Modus 4 als interruptive Checkliste statt Advisory ausgeben
- Ladereihenfolge des Profils ignorieren (BPM: DOC-STANDARD Kapitel 8)
- Invarianten-Check bei neuen Docs überspringen
- Branch automatisch annehmen (Shell fragen oder Auswahlfrage)
- Modus-Auswahl als Prosa bei Unsicherheit — IMMER Auswahlfrage
- Prosa-Fragen bei festen Entscheidungsoptionen
- Migrations-Kapitel in Doc dokumentieren ohne User-Freigabe (Projekte mit Frühphasen-Regel, BPM: INDEX.md)
- Abweichung von v1 dokumentieren ohne PD-Eintrag mit Freigabe (Heidi-Paritätsregel)
- Statusliste auf `fertig` setzen, solange Tests oder Commit fehlen
- BPM-Pfade oder -Dateinamen für ein anderes Projekt annehmen — alles aus dem Doku-Profil
- Sitzung ohne Modus 8 beenden, wenn Docs geändert wurden
