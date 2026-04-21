---
name: code-erstellen
description: >
  Plant und erzeugt BPM-Codeänderungen auf Basis von INDEX.md, Quickloads und
  fachlichen Invarianten. Use when users want to implement or change application
  code, add a method, service, dialog, data flow, validation, or persistence
  logic. Do not trigger for mockups, git commits, explicit documentation work,
  ClickUp task management, or pure consistency audits.
---

# Code-Erstellen — Orchestrator Skill

## Zweck

Stellt sicher dass vor jeder Code-Erstellung die relevanten Docs
gelesen und geprüft wurden. Nutzt die verbindliche Ladereihenfolge
aus DOC-STANDARD.md Kapitel 8.

---

## 🚨 VERBINDLICHE REGEL: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0`
verwendet werden — KEINE Prosa-Fragen.**

### Diese Fragen IMMER mit ask_user_input_v0:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung | Alle Branch-Namen aus `git branch -a` als Optionen |
| Modus unklar | Lite, Standard, Deep |
| Zielschicht mehrdeutig | Domain, Application, Infrastructure, UI |
| Mehrere Referenz-Implementierungen | Dateinamen als Optionen |
| Fachliche Invariante würde verletzt | "Trotzdem fortsetzen", "Abbrechen", "Andere Lösung" |
| Ausgabeformat mehrdeutig | Komplette Datei, SUCHE/ERSETZE, Download |
| ClickUp-Task-Zuordnung nach Commit | Task-Kandidaten als Optionen + "Kein Task" + "Neuen Task anlegen" |
| Mehrere Blocking Conditions | Welche Datei zuerst laden (Kandidaten) |
| Commit-Version unklar (Major/Minor/Patch) | MAJOR (Breaking), MINOR (Feature), PATCH (Fix) |
| User muss Referenzdatei angeben | Kandidaten aus Projektstruktur |
| Bestehende Daten/Configs betroffen | "Daten löschen, neu anlegen lassen", "Migration bauen", "Abbrechen" |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen  
  (Beispiel: "Welcher Kurztitel für den Commit?")
- User hat gerade eine klare Präferenz signalisiert
- Es ist Erklärung/Kontext, keine echte Entscheidung
- Freitext-Input nötig (z.B. neuer Klassenname, neue Commit-Message)

### Wie ask_user_input_v0 aussieht

Einfache Auswahl:
```
ask_user_input_v0(
  questions: [
    {
      question: "Welcher Modus für diese Aufgabe?",
      options: ["Lite", "Standard", "Deep"]
    }
  ]
)
```

Branch-Auswahl:
```
ask_user_input_v0(
  questions: [
    {
      question: "Welcher Branch ist aktiv?",
      options: ["main", "feature/planmanager-v1", "feature/settings-tabs"]
    }
  ]
)
```

### VERBOTEN

- Branch-Liste im Chat aufzählen und auf getippte Antwort warten
- "Lite oder Standard oder Deep?" als Prosa
- "Welche Datei soll noch geladen werden?" als Prosa wenn Kandidaten bekannt
- "Passt zu BPM-XXX. tracker done ausführen?" als Prosa
- Eine Optionen-Aufzählung im Chat ohne ask_user_input_v0

---

## Branch-Ermittlung (PFLICHT vor GitHub-Zugriff)

1. Prüfe ob Branch bereits in dieser Session bekannt ist → verwenden
2. Wenn nicht bekannt: Alle Branches via GitHub API oder `git branch -a` via DC auflisten
3. **Per `ask_user_input_v0`** den aktiven Branch wählen lassen (Optionen = Branch-Namen)
4. Gewählten Branch für die gesamte Session merken
5. NIE automatisch einen Branch annehmen (weder `main` noch einen anderen)

---

## Arbeitsverzeichnis (PFLICHT bei DC-Zugriff)

Wenn dieser Skill DC-Operationen auslöst (z.B. Code-Dateien lesen,
Entry Points prüfen), das Arbeitsverzeichnis nach **cc-steuerung Kapitel 4** ermitteln.

### Ablauf (erster DC-Aufruf der Session)

1. Pfad-Ermittlung:
```powershell
$pc = hostname; $od = [System.Environment]::GetEnvironmentVariable('OneDrive', 'User'); Write-Host "$pc|$od"
```

2. INDEX.md laden → Abschnitt "PCs und Arbeitsverzeichnisse" → COMPUTERNAME matchen
   - **GEFUNDEN** → workFolder = OneDrive-Pfad + `\` + Projekt-Suffix aus INDEX.md
   - **NICHT GEFUNDEN** → Self-Registration (cc-steuerung 4.3)

3. Verifikation:
```powershell
Test-Path "<workFolder>"
```

4. workFolder für die gesamte Session merken

**Wichtig:** `$env:OneDrive` funktioniert NICHT über DC `start_process`.
IMMER `[System.Environment]::GetEnvironmentVariable('OneDrive', 'User')` verwenden.
**Keine hardcodierten absoluten Pfade.**

---

## Auto-Anker bei Task-Keywords (Phase 1 des Chat-Anker-Systems)

**Zweck:** Wenn im Chat ein Thema auftaucht das offensichtlich ein späterer Task wird (aber aktuell noch kein Task existiert), setzt dieser Skill automatisch einen temp-Anker. Das stellt sicher, dass die Diskussionsstelle später via `conversation_search` wiederfindbar ist.

Konzept-Doc: `docs/chat-anker-konzept.md` (Phase 1).
Anker-Format + Memory-Registry: siehe tracker-Skill Kapitel "Chat-Anker-System".

### Task-Keywords (Trigger für Auto-Anker)

Claude erkennt folgende Formulierungen als klares Task-Signal:

- "das müssen wir noch bauen"
- "später implementieren"
- "ins backlog"
- "backlog-wert"
- "da brauchen wir einen task"
- "sollten wir im task tracken"
- "muss noch gemacht werden"
- "als task anlegen"

Wenn User diese Keywords nutzt UND das Thema noch keinen offenen Task hat → Auto-Anker setzen.

### Ablauf

1. Keyword erkannt UND Kontext ist klar (Thema identifizierbar)
2. TEMP-ID generieren:
   - Primär via DC PowerShell (siehe tracker-Skill "TEMP-ID Generierung")
   - Fallback: Claude erzeugt `TEMP-<yyMMddHHmm><3 Zufallsbuchstaben>`
3. Anker-Zeile im Chat-Response einfügen (möglichst am Anfang des relevanten Abschnitts):
   ```
   [BPM-ANCHOR-TEMP-<id>] — Idee: <kurzbeschreibung max 60 Zeichen>
   ```
4. Memory aktualisieren:
   ```
   memory_user_edits(command: "add", control: "[ANKER-LIVE] TEMP-<id>|offen|<ISO-timestamp>|<kurzbeschreibung>")
   ```
5. Kurzer Hinweis im Chat: "Anker gesetzt — wird bei `tracker neu` mit Task-ID verknüpft."

### Wann KEIN Auto-Anker

- User spricht nur über bestehende Tasks (nicht Task-würdiger Neu-Content)
- Thema ist zu vage für eine 60-Zeichen-Kurzbeschreibung
- Innerhalb 24h existiert bereits ein Anker mit ähnlichem Thema (Duplikat-Check via `[ANKER-LIVE]`)
- User sagt explizit "kein Task daraus" o.ä.
- Mehr als 10 Anker bereits in `[ANKER-LIVE]` — User sollte erst aufräumen

**Im Zweifel: KEIN Anker.** Lieber ein paar Anker verpassen als den Chat zuspammen.

### Anti-Pattern

- Anker mitten in Code-Blöcken einfügen
- Mehrere Anker direkt hintereinander für dasselbe Thema
- Anker setzen für Dinge die der User nur erwähnt ohne Handlungsabsicht
- Anker mit generischen Beschreibungen wie "Feature X" oder "TODO"

---

## Voraussetzung

INDEX.md im Repo. Optional DOC-STANDARD.md.

---

## Load Order (verbindlich)

### 1. Anfrage klassifizieren → Modus

```
mode = Lite

Eskalation auf Standard:
- neue Methode in öffentlichem Service/ViewModel
- neuer Dialog / View / Commands
- Persistenzlogik ohne neue Tabelle
- mehrere Dateien in einem Projekt
- neue Validierungs-/Statuslogik

Eskalation auf Deep:
- neues Interface / Service-Implementierung
- neue Tabelle / Schemaänderung
- externe API / Import / Export
- mehrere Schichten / Projekte
- neuer Benutzerfluss
- DSGVO / DataClassification
- DI betroffen UND nicht rein lokal
```

**Bei Unsicherheit (Anfrage passt zu mehreren Modi):** `ask_user_input_v0` mit Optionen Lite, Standard, Deep.

### 2. INDEX.md laden

Task-to-Doc Routing → Primary/Secondary/Reference ermitteln.

### 3. Quickload-First-Pass (DOC-STANDARD Kapitel 8)

**Verbindliche Ladereihenfolge:**

```
1. INDEX.md → Routing (welche Doc?)
2. Frontmatter + AI-Quickload lesen → Filter (relevant? welches Kapitel?)
3. Fachliche Invarianten prüfen → Sofort sichtbar ohne Langform
4. Pflichtlesen-Kapitel laden → Immer wenn Modul betroffen
5. Weitere Kapitel nur bei Bedarf nachladen
```

**Ablauf:**
1. Relevante Docs aus INDEX-Routing identifizieren (Primary zuerst)
2. Für jede Doc: Nur erste ~30 Zeilen laden (Frontmatter + Quickload)
3. Fachliche Invarianten sofort in den Impact Check übernehmen
4. Pflichtlesen-Kapitel: IMMER laden wenn Modul betroffen → Blocking Condition
5. Aus Quickload-Kapitel-Feld entscheiden welche Kapitel relevant sind
6. Nur relevante Kapitel als Langform nachladen
7. Quickload nicht vorhanden? → Fallback: ganze Doc laden

**Limits:**
- Lite: Quickload max 3 Docs, Langform max 2
- Standard: Quickload max 6 Docs, Langform max 4
- Deep: Quickload max 10 Docs, Langform max 8

### 4. Code Entry Points laden

Kopplungsregeln:
- View → ViewModel prüfen
- Neuer Service → Interface + DI (App.xaml.cs)
- Neuer Dialog → Theme-/Dialog-Referenz
- DB-Änderung → ProjectDatabase.cs + DB-SCHEMA.md

### 5. Impact Check

```
📋 Impact Check:
- UI / XAML / Theme-Tokens: [Ja/Nein]
- ViewModel / Commands / Bindings: [Ja/Nein]
- Domain-Modell / Interface: [Ja/Nein]
- Infrastructure / SQLite / Dateisystem: [Ja/Nein]
- DI-Registrierung: [Ja/Nein]
- Externe Kommunikation: [Ja/Nein]
- DSGVO / DataClassification: [Ja/Nein]
- Settings / Konfiguration: [Ja/Nein]
- App-Lebenszyklus: [Ja/Nein]
- Logging / Fehlerbehandlung: [Ja/Nein]
- Bestehende Daten/Configs betroffen?: [Ja/Nein] (siehe Frühphasen-Prinzip in INDEX.md)
- Referenzimplementierung: [Name oder Nein]
- Fachliche Invarianten verletzt?: [Liste oder Nein]
```

### 6. Blocking Conditions

Blockiere Code-Erstellung wenn:
- Zielschicht unklar → `ask_user_input_v0` (Domain / Application / Infrastructure / UI)
- Referenzdatei nicht gefunden → `ask_user_input_v0` mit Kandidaten oder "Ohne Referenz"
- DI betroffen aber nicht geladen → erst App.xaml.cs laden
- Externe Kommunikation ohne DSGVO-Doc → erst DSVGO-Architektur.md laden
- UI ohne Theme-Doc → erst UI-Doc laden
- DB ohne Schema-Doc → erst DB-SCHEMA.md laden
- **Pflichtlesen-Kapitel nicht geladen obwohl Modul betroffen** → laden
- **Fachliche Invariante würde verletzt werden** → `ask_user_input_v0` (Trotzdem fortsetzen / Abbrechen / Andere Lösung)
- **Migration / Backward-Compatibility wäre nötig** → `ask_user_input_v0` (Daten löschen + neu anlegen / Migration explizit gewünscht / Abbrechen) — siehe Frühphasen-Prinzip in INDEX.md

→ NICHT blind coden, per ask_user_input_v0 nachfragen welche Datei noch geladen werden muss.

### 7. Code erzeugen

Standards aus Project Files, Referenzimplementierungen als Muster.

### 8. Ausgabeformat (→ suche-ersetze)

- Neue Datei → komplett
- < 600 Zeilen UND > 30% geändert → komplett
- ≥ 600 Zeilen → SUCHE/ERSETZE
- XAML → Download

**Bei Mehrdeutigkeit:** `ask_user_input_v0` mit den möglichen Formaten.

### 9. Commit + DocMaintenanceHints (→ git-commit-helper + doc-pflege)

```
[vX.Y.Z] Modul, Typ: Kurztitel

📝 Doc-Pflege nötig:
- INDEX.md: [Ja/Nein]
- DB-SCHEMA.md: [Ja/Nein]
- CHANGELOG.md: [Ja/Nein]
- ADR.md: [Ja/Nein]
- Frontmatter: [welche Docs]
- Quickload: [welche Docs]

📂 Gelesene Dateien: [Liste]
📋 Quickload-Only: [Liste]
⚠️ Annahmen: [falls vorhanden]
🚫 Nicht geladen: [Begründung]
```

**Version-Bump unklar?** `ask_user_input_v0`:
- MAJOR (Breaking Change)
- MINOR (neues Feature)
- PATCH (Bugfix)

### 10. ClickUp Tracker-Abgleich (optional)

Nach erfolgreichem Commit prüfen:
1. Gibt es einen offenen ClickUp-Task der zu dieser Änderung passt?
   - `clickup_search` mit Schlüsselwörtern aus dem Commit-Titel
2. **Wenn Kandidaten gefunden → `ask_user_input_v0`:**
   ```
   Frage: "Commit passt zu folgenden Tasks. Welcher soll auf Done?"
   Optionen:
   - "BPM-004 | 5998er Statikplaene Erkennung"
   - "BPM-007 | andere passende Task"
   - "Kein Task passt"
   - "Neuen Task anlegen"
   ```
3. Bei "Neuen Task anlegen" → `tracker neu` aufrufen
4. Bei Task-Auswahl → `tracker done` aufrufen
5. NICHT automatisch schließen — nur vorschlagen
6. Alle ClickUp-Operationen über den **tracker-Skill**, NICHT direkt

Beispiel-Ausgabe nach Commit:

```
[v0.25.30] PlanManager, Fix: 5998er Statikplaene Erkennung

📝 Doc-Pflege nötig: Nein
🎯 ClickUp: 1 passender Task gefunden
```
→ dann `ask_user_input_v0` mit dem Task als Option

---

## Modus-Übersicht

| Modus | Quickload | Langform | Code | Impact |
|-------|-----------|----------|------|--------|
| Lite | max 3 | max 2 | 1-3 | Kurz |
| Standard | max 6 | max 4 | 3-8 | Voll |
| Deep | max 10 | max 8 | 5-12+ | Voll + Blocking |

---

## VERBOTEN

- Code ohne INDEX.md
- Quickload-First-Pass überspringen
- Pflichtlesen-Kapitel ignorieren
- Fachliche Invarianten ignorieren
- Annahmen ohne geladene Dateien
- Impact Check weglassen
- DocMaintenanceHints weglassen
- Branch automatisch annehmen ohne User-Auswahl
- **Branch-Auswahl als Prosa** — IMMER ask_user_input_v0
- Hardcodierte absolute Pfade bei DC-Zugriff
- ClickUp-Tasks direkt erstellen/schließen (→ immer über tracker-Skill)
- Tasks automatisch als Done markieren ohne User-Bestätigung
- **Task-Zuordnung nach Commit als Prosa** — IMMER ask_user_input_v0
- **Modus-Auswahl als Prosa bei Unsicherheit** — IMMER ask_user_input_v0
- **Blocking-Condition-Auflösung als Prosa** wenn Kandidaten bekannt — IMMER ask_user_input_v0
- Optionen im Chat aufzählen und auf getippte Antwort warten
- Migration / Backward-Compatibility automatisch bauen ohne User-Freigabe (siehe Frühphasen-Prinzip in INDEX.md)
- **Auto-Anker bei vagen Themen setzen** — lieber keinen Anker als einen unscharfen
- **Anker mit generischen Beschreibungen** ("Feature X", "TODO") — immer konkret benennen
- **Anker setzen ohne Memory-Update** — Chat-Zeile UND `[ANKER-LIVE]`-Eintrag gehören zusammen
