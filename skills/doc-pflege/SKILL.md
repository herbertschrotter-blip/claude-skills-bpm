---
name: doc-pflege
description: >
  Erstellt, aktualisiert und validiert BPM-Dokumentation nach DOC-STANDARD,
  inklusive Frontmatter, Quickload, Kapitelvorlagen und Routing in INDEX.md.
  Use when users want to write or update docs, create an ADR or concept doc,
  validate Frontmatter or Quickload, or refactor documentation to the project
  standard. Do not trigger for code implementation, automatic post-change
  advisory checks, or generic project discussion without explicit doc intent.
---

# Doc-Pflege — Dokumentations-Skill

## Zweck

Stellt Konsistenz der Projektdokumentation sicher. Validiert Frontmatter,
Quickload und Kapitelstruktur nach DOC-STANDARD.md. Initialisiert neue
Projekte mit Standard-Doc-Set. Erzwingt Kapitelvorlagen bei neuen Docs.

---

## 🚨 VERBINDLICHE REGEL: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0`
verwendet werden — KEINE Prosa-Fragen.**

### Diese Fragen IMMER mit ask_user_input_v0:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (unbekannt) | Branch-Namen aus `git branch -a` |
| Modus-Auswahl bei Unsicherheit | Modus 0-7 als Optionen |
| Refactoring 7b: Inhalt passt in kein Kapitel | Eigenes Kapitel am Ende, Vorhandenes Kapitel erweitern, Abbrechen |
| Doc-Pflege Modus bei doc-relevanter Änderung | Jetzt pflegen, Später als Task anlegen, Ignorieren |
| Schema-/DB-Änderung dokumentieren | "Mit Reset-Anweisung", "Mit Migrations-Kapitel (User will explizit)", "Abbrechen" |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen (z.B. Projektname, Modulname, Freitext-Beschreibung)
- User hat Präferenz signalisiert
- Freitext-Input nötig

---

## Branch-Ermittlung

Branch aus Chat-Kontext verwenden.
Wenn Branch in dieser Session noch nicht bekannt: Per ask_user_input_v0 fragen.
NIE automatisch einen Branch annehmen.

---

## Arbeitsverzeichnis (PFLICHT bei DC-Zugriff)

Bei DC-Operationen: Arbeitsverzeichnis nach **cc-steuerung Kapitel 4** ermitteln.

---

## Konkrete Pfade im BPM-Repo

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

Dieser Skill liest Docs nach der verbindlichen Ladereihenfolge
(DOC-STANDARD.md Kapitel 8):
1. INDEX.md → Routing
2. Frontmatter + Quickload → Filter
3. Fachliche Invarianten → Prüfen
4. Pflichtlesen → Laden wenn betroffen
5. Langform nur bei Bedarf

---

## Frühphasen-Regel (PFLICHT bei Schema-/Config-/DB-Doku)

INDEX.md hat das Kapitel "Projekt-Phase (VERBINDLICH)". Solange dieses Kapitel
besteht, gilt für die Doku von Schema-/Config-/DB-Änderungen:

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

---

## Advisory-Checkliste nach code-relevanten Änderungen

**Dieser Abschnitt ist KEIN Trigger.**
Er wird von anderen Skills nach einer Änderung als **Nachlauf-Checkliste** genutzt.
Der User-Intent für doc-pflege steht ausschließlich in der Frontmatter-Description.
Die hier beschriebene Checkliste wird passiv konsumiert (z.B. durch code-erstellen
oder git-commit-helper), sie aktiviert doc-pflege nicht selbst.

### Typische Fälle (Change-Class-basiert)

Die Nachlauf-Checkliste wird nach doc-relevanten Änderungen durchlaufen:
- Neue Tabelle / Schemaänderung
- Neue Architekturentscheidung
- Neuer Code-Entry-Point (neues Interface, neuer Service, neuer Dialog)
- Neues Modul / neuer Workflow mit Benutzerwirkung
- Neue Abhängigkeit (NuGet, Projektreferenz)
- Neues Doc / Doc-Refactor

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

## 7 Modi

### Modus 0 — Projekt-Init (Standard-Doc-Set)

**Wann:** "neues Projekt", "init projekt", keine INDEX.md vorhanden.

Für Details siehe `references/projekt-init.md` (falls vorhanden)
oder DOC-STANDARD.md Kapitel 3.

Kurzablauf:
1. Grundinfos sammeln (Projektname, Tech-Stack, Repo, DB?)
2. Repo scannen
3. Standard-Doc-Set generieren (INDEX.md, Architektur.md, BACKLOG.md, CHANGELOG.md, ADR.md, DEPENDENCY-MAP.md, ggf. DB-SCHEMA.md)
4. Korrektes Frontmatter + Quickload + Kapitelstruktur
5. Invarianten-Check
6. Paket dem User vorlegen

---

### Modus 1 — Index Sync

**Wann:** Neues Doc, Doc umbenannt, neuer Code-Entry-Point.

INDEX.md laden, Routing-Eintrag im Primary/Secondary/Reference-Format.

---

### Modus 2 — Companion Docs Check

**Wann:** Neue Tabelle, Feature, Architekturentscheidung, Abhängigkeit.

INDEX.md → Doc-Pflege Policy → Pflicht-Docs ändern.

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

Volle Prüfung aller Pflicht-Docs + Frontmatter/Quickload Validierung.

---

### Modus 6 — Frontmatter + Quickload Validierung

**Wann:** "prüfe frontmatter", "quickload check", oder explizit angefordert.

#### Stufe A — Formal (Blocker)

- Frontmatter vorhanden bei Kern/, Module/, Referenz/?
- Alle Pflichtfelder?
- doc_id eindeutig?
- Enums korrekt?
- Quickload bei source_of_truth/secondary?
- Quickload Kapitel-Feld stimmt mit H2s?
- Kapitelreihenfolge nach Vorlage?
- Pflichtlesen verweist auf existierende Kapitel?
- Fachliche Invarianten max 5?

#### Stufe B — Semantisch (Warnung)

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

1. DOC-STANDARD.md laden (Kapitel 7: Kapitelvorlage für den doc_type)
2. INDEX.md laden → verwandte Docs identifizieren
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

1. DOC-STANDARD.md laden (Kapitelvorlage für den doc_type)
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

**VERBOTEN:** Doc ohne Frontmatter, ohne Quickload, ohne Kapitelvorlage erstellen.
**VERBOTEN:** Beim Refactoring Inhalte weglassen, kürzen oder zusammenfassen.

---

## Ausgabeformat

- SUCHE/ERSETZE oder DC
- Neue Docs komplett mit Frontmatter + Quickload + Kapitelstruktur
- Commit: `[vX.Y.Z] Docs, Docs: [Kurztitel]`

---

## Skill-Governance

Bei jeder Änderung an diesem Skill prüfen:
1. Trigger zu breit geworden?
2. Redundanz zu anderer Skill-Regel entstanden?
3. Negativgrenzen noch korrekt?
4. DOC-STANDARD / INDEX betroffen?

---

## VERBOTEN

- Frei inferieren welche Docs betroffen sind
- Docs ohne Frontmatter in Kern/Module/Referenz akzeptieren
- Neue Docs ohne Kapitelvorlage erstellen
- Modus 4 bei trivialen Änderungen triggern
- Modus 4 als interruptive Checkliste statt Advisory ausgeben
- Quickload-Laderegel ignorieren (DOC-STANDARD Kapitel 8)
- Invarianten-Check bei neuen Docs überspringen
- Branch automatisch annehmen ohne ask_user_input_v0
- Modus-Auswahl als Prosa bei Unsicherheit — IMMER ask_user_input_v0
- Prosa-Fragen bei festen Entscheidungsoptionen
- Migrations-Kapitel in Doc dokumentieren ohne User-Freigabe (siehe Frühphasen-Prinzip in INDEX.md)
