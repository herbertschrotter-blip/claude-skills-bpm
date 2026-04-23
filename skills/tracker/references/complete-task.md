# tracker done — Task abschließen

Vollständiger Ablauf, Commit-Ermittlung und Beispiel-Workflow für `tracker done`.

---

## Kommando

`tracker done: <Stichwort oder BPM-NNN>`

---

## Ablauf

1. **Task finden** via `clickup_search` (falls BPM-NNN nicht explizit)
2. **Mehrere Treffer** → mit `ask_user_input_v0` User wählen lassen
3. **Review-Workflow-Check** (Pflicht vor jedem Task-Abschluss): Wurden im
   Chat neue Regeln/Entscheidungen besprochen die andere Tasks betreffen?
   4-Punkte-Check (aktueller Task, Parent, Siblings, verweisende offene
   Tasks) gemäß `references/review-workflow.md`. Gefundene Änderungen in
   ClickUp umsetzen BEVOR der Task auf done gesetzt wird.
4. **Commit-Infos ermitteln** (Pflicht):
   - Wenn Task Code-Bezug hat (Modul mit Code-Scope — siehe `projects/<[PROJECT]>/clickup-fields.md` Modul-Kürzel):
     - Claude fragt User: "Welche Datei(en) sind betroffen?" (Prosa, offene Frage!)
     - Per DC: `git log -1 --format="%h|%ad|%s" --date=short -- <Datei>`
     - Oder: `git log --all --diff-filter=A --format="%h %ad %s" --date=short -- <Datei>` (erste Erwähnung)
     - Oder: `git log --grep="vX.Y.Z" --format="%h %ad %s" --date=short` (Version bekannt)
   - Wenn Task reiner Doc-Bezug:
     - Gleicher Weg, aber auf Docs/ Pfade
   - Wenn Task keinen Code-Bezug hat (z.B. Meta-Task):
     - Commit ID + Commit Text leer lassen
     - Erledigt-Datum = heute (YYYY-MM-DD)
5. **Bei mehreren Commits:** `ask_user_input_v0` mit allen Kandidaten (Hash + erste Zeile)
6. **Pro-Task-Quittung im Chat schreiben** (direkt vor `clickup_update_task`):
   ```
   ✅ <BPM-ID oder Issue-ID> — [BPM-ANCHOR-<task-id>] — erledigt: Commit <hash> <kurzbeschreibung>
   ```
   Die Quittung ist Bestätigung + Body-Anker + Audit-Zeile in einem Format.
   **Bei ≥2 Tasks in einer Antwort:** Vollständiges Batch-Protokoll greift — siehe `references/batch-protocol.md` (Batch-Ansage, Pro-Task-Zyklus, Batch-Audit).
7. **Nachpflege-Felder prüfen** (falls bei `tracker neu` nicht gesetzt):
   - Typ, Aufwand, Zielversion, Komponente, Zugehörige Docs
   - Falls alle leer: `ask_user_input_v0` mit fehlenden Feldern
8. **Custom Fields vorbereiten** (konkrete Field-IDs siehe `projects/<[PROJECT]>/clickup-fields.md`):
   ```
   custom_fields = [
     {"id": "<Commit-ID-Field>",         "value": "<7-char-hash>"},
     {"id": "<Commit-Text-Field>",       "value": "<erste Zeile der Commit-Message>"},
     {"id": "<Erledigt-Field>",          "value": "<YYYY-MM-DD>"},
     {"id": "<Chat-Anker-erledigt-Field>", "value": "[BPM-ANCHOR-<task-id>] - erledigt: ..."},
     // + Nachpflege-Felder falls gesetzt
   ]
   ```
9. **Einziger API-Call**:
   ```
   clickup_update_task(
     task_id: "<TaskID>",
     status: "<done-oder-complete-je-nach-Listen-Typ>",   ← KLEINGESCHRIEBEN, Wert aus projects/<[PROJECT]>/clickup-fields.md Status-Matrix
     custom_fields: custom_fields
   )
   ```
10. **Memory `[ANKER-LIVE]` aufräumen**:
    - Eintrag mit Task-ID und Typ `erstellt` entfernen
    - Falls temporär ein Typ `erledigt` gesetzt wurde: auch entfernen
    - Nach diesem Schritt existiert im Memory nichts mehr zu diesem Task
11. **Bestätigung** an User:
    ```
    ✅ BPM-XXX auf Done gesetzt
       Commit: <hash> — <Erste Zeile der Message>
       Erledigt: <YYYY-MM-DD>
       Anker: [BPM-ANCHOR-<task-id>] (erstellt + erledigt)
    ```
---

## Automatischer Nachlauf nach tracker done

**Kernregel:** Nach jedem erfolgreichen `clickup_update_task` auf `done`/`complete`
MUSS Claude automatisch den Nachlauf ausführen. **Niemals passiv auf
User-Input warten nach `tracker done`.**

### 4-Schritt-Nachlauf

1. **Commit-Hash selbst via DC holen** (falls nicht schon aus vorhergehendem
   `git commit`-Call bekannt):
   ```
   cd "<Repo-Pfad>"
   git log -1 --format='%h %s'
   ```
   Baut auf cc-steuerung-003 auf (DC ist Default-Ausführungsmodus). Den Hash
   nicht vom User anfordern wenn DC verfügbar ist.

2. **Custom Fields in ClickUp setzen** — passiert typischerweise schon im
   Haupt-Ablauf-Schritt 9 (Commit ID, Commit Text, Erledigt-Datum,
   Chat-Anker erledigt). Falls Hash erst nachträglich via Schritt 1
   ermittelt wurde: zweiter `clickup_update_task` mit den Feld-Updates.

3. **Zwischenstand-Tabelle im Chat** zeigen — Kompakt-Überblick was erledigt
   wurde und was noch offen ist:
   ```
   | Item | Status |
   |------|--------|
   | <Task-ID> done (<hash>, <version>) | ✅ |
   | Push nach origin/main | ⏳ User |
   ```
   Bei mehreren parallelen Items (z.B. Skill-Issues-Session): vollständige
   Session-Tabelle mit allen abgeschlossenen und offenen Punkten.

4. **Folgeoptionen via `ask_user_input_v0`** — 2-4 Optionen mit konkreten
   nächsten Schritten:
   ```
   ask_user_input_v0:
     question: "Was als nächstes?"
     options:
       - "<Nächster geplanter Issue/Task mit Kurzbeschreibung>"
       - "<Alternativer thematisch passender Task>"
       - "Anderen Punkt anpacken (ich sag welchen)"
       - "Pause"
   ```
   Niemals als Prosa-Frage. Niemals still warten.

### Ausnahmen

- **Zero-Change-Tasks:** Schritt 1 entfällt (kein Commit, kein Hash). Schritte
  2-4 bleiben. Im Quittungstext `(Zero-Change)` vermerkt (gemäß `tracker-007`).

- **Batch-Abschluss (mehrere Tasks hintereinander done):** Schritte 1-2 pro
  Task durchlaufen, Schritt 3 einmal am Batch-Ende mit Gesamt-Übersicht,
  Schritt 4 **nur einmal** nach dem letzten Task.

- **DC nicht verfügbar:** Schritt 1 entfällt automatisch. Dann Prosa-Frage
  an den User: "Commit-Hash?" (offene Frage, nicht `ask_user_input_v0`).

### VERBOTEN

- Nach `tracker done` passiv auf User-Input warten ohne `ask_user_input_v0`
- Commit-Hash vom User anfordern wenn DC verfügbar ist
- Zwischenstand-Tabelle nach Task-Abschluss weglassen
- Folgeoptionen als Prosa-Frage statt `ask_user_input_v0`
- Folgeoptionen bereits nach dem ersten Task eines Batches zeigen — erst am Batch-Ende

### Beispiel-Ablauf

```
tracker done auf BPM-082 (Code-Task)
  [Haupt-Ablauf Schritte 1-11 durchlaufen]
  ✓ Status auf done gesetzt, Custom Fields gefüllt

Automatischer Nachlauf:
  1. DC: git log -1 --format='%h %s' → hash bereits bekannt aus Commit-Session
  2. Custom Fields schon in Schritt 9 mit drin → übersprungen
  3. Zwischenstand-Tabelle:
     | Item | Status |
     |------|--------|
     | BPM-082 done (ee4476d, v0.26.0) | ✅ |
     | Push nach origin/main | ⏳ User |
  4. ask_user_input_v0:
     "Was als nächstes?"
     - "BPM-083 (Folgefeature laut Prio)"
     - "BPM-084 (Bugfix, geplant)"
     - "Anderer Task"
     - "Pause"
```

---

## Commit-Disziplin: ein Task = ein Commit

**Kernregel:** Jeder abgeschlossene (Sub-)Task bekommt sofort einen eigenen
Commit. Kein Sammeln am Session-Ende.

### Workflow pro Task

1. Task umsetzen (Code/Doc-Änderung)
2. Review-Workflow-Check (siehe `tracker-006` Regel): Parent / Siblings / verweisende offene Tasks betroffen?
3. Commit-Befehl vorbereiten (Versionierung siehe unten)
4. Commit **sofort** nach Abschluss — nicht sammeln
5. Hash aus Commit-Output übernehmen (oder via `git log -1 --format="%h"` ermitteln)
6. `tracker done` mit Commit-Hash im Custom Field `Commit ID` ausführen

### Ausnahmen

- **Nachhol-Commits bei Skill-Regel-Wechsel mitten in einer Session:**
  Wenn die Commit-Disziplin-Regel selbst erst mitten in einer laufenden Phase
  eingeführt/geändert wird, ist ein einmaliger Sammel-Commit für alle
  bereits erledigten Subtasks erlaubt. Diese Ausnahme MUSS im
  Session-Protokoll (Übergabeprompt) dokumentiert sein.

- **Zero-Change-Tasks:** Tasks ohne Git-Änderung (Task-Description-Updates,
  Memory-Edits, reine ClickUp-Pflege) brauchen keinen Commit. Custom Field
  `Commit ID` und `Commit Text` bleiben leer. Im Quittungstext mit
  `(Zero-Change)` markieren, damit das leere Feld nachvollziehbar ist.

### Versionierung

- **PATCH** (`vX.Y.Z+1`): kleine Refactors, Doku-Ergänzungen, Bugfixes innerhalb einer Phase
- **MINOR** (`vX.Y+1.0`): neue Features, abgeschlossene Phasen, neue Reference-Dateien
- **MAJOR** (`vX+1.0.0`): Breaking Changes (Skill-Struktur-Umbau, Routing-Bruch)

### Abgrenzung zu `git-commit-helper`

| Skill | Verantwortung |
|-------|---------------|
| `tracker` | **WANN** committet wird (Task-Lebenszyklus-Kopplung) |
| `git-commit-helper` | **WIE** der Commit formatiert wird (Format, Version, Titel, Body) |

Commit-Disziplin gehört in `tracker`, Commit-Formatierung in `git-commit-helper`.

---

## Status-Werte IMMER kleingeschrieben

- `open` (nicht Open)
- `in progress` (nicht In Progress)
- `done` (nicht Done)

API ist case-sensitive. Grossgeschrieben kann Fehler werfen.

---

## DC nicht verfügbar?

1. User nach Commit-Hash fragen (Prosa, offene Frage)
2. User nach Commit-Message fragen (Prosa)
3. Erledigt-Datum = heute
4. Chat-URLs: aktueller Chat als Fallback für beide Felder

---

## Keine Commit-Info ermittelbar?

Per `ask_user_input_v0`: Manuell eingeben, Feld leer lassen, Abbrechen.

---

## Git-Commit-Ermittlung (Detailhilfe)

### Szenario A: Commit wurde gerade in dieser Session gemacht
Der Hash ist Claude aus dem `git commit` Output bereits bekannt → direkt verwenden.
Chat erledigt = aktueller Chat.

### Szenario B: Task ist früher erledigt worden (Nachtrag)

Per DC:
```powershell
cd "<Repo-Pfad>"
# Suche nach erster Datei-Erstellung
git log --all --diff-filter=A --format="%h|%ad|%s" --date=short -- "<Pfad/zur/Datei.cs>"

# Oder: Suche nach bestimmter Version
git log --all --format="%h|%ad|%s" --date=short --grep="vX.Y.Z"

# Oder: Suche nach Stichwort
git log --all --format="%h|%ad|%s" --date=short --grep="<Stichwort>"

# Oder: Genauer Zeitpunkt (für Chat-Matching)
git log --all --format="%h|%aI|%s" -- "<Datei>"
```
Der Pipe-Separator `|` erleichtert das Parsen: `<hash>|<datum>|<message>`.

### Szenario C: Mehrere relevante Commits

`ask_user_input_v0` mit allen Kandidaten als Optionen (Hash + erste Zeile Message).
In der Regel: Erster Commit der die Funktionalität eingeführt hat (diff-filter=A).

### Datumsformat

- DC liefert: `YYYY-MM-DD` (mit `--date=short`) oder ISO (`%aI`)
- ClickUp erwartet: `YYYY-MM-DD` (direkt)
- Für Chat-Suche: ISO-Zeitstempel mit Stunde/Minute (für recent_chats Zeitfilter)
---

## Beispiel-Workflow (BPM-Projekt, `tracker done` mit Commit-Ermittlung)

Dieser Beispiel-Ablauf zeigt einen konkreten `tracker done`-Durchlauf für BPM.
Feld-IDs und Status-Werte stehen in `projects/bpm/clickup-fields.md`.

```
User: tracker done BPM-007

Claude intern:
  1. clickup_get_task("86c9cg8u5") → BPM-007 PlanTyp-Erkennung
  2. Prosa-Frage: "Welche Datei(en) sind betroffen?"
     User: "DocumentTypeRecognizer.cs"
  3. DC: git log --all --diff-filter=A --format="%h|%aI|%s" -- "src/.../DocumentTypeRecognizer.cs"
     → "cb46a48|2026-04-15T11:34:52+02:00|[v0.25.5] PlanManager, Feature: PatternTemplates..."
  4. Nur 1 Kandidat → direkt verwenden
  5. Chat erledigt:
     → recent_chats(after: "2026-04-15T07:34", before: "2026-04-15T15:34", n: 5, sort_order: "asc")
     → Treffer: Teil 17 (015353fe-...)
  6. Chat erstellt (nicht gesetzt):
     → conversation_search("Plantyp-Erkennung DocumentTypeRecognizer prefix contains")
     → Teil 10 (d546b50b-...) als ältester konkreter Treffer
  7. Nachpflege: Typ fehlt noch
     → ask_user_input_v0: Typ → Feature
  8. Pro-Task-Quittung im Chat:
     ✅ BPM-007 — [BPM-ANCHOR-<task-id>] — erledigt: Commit cb46a48 PlanTyp-Erkennung
  9. clickup_update_task(
       status: "done",
       custom_fields: [
         {id: "<Typ-ID>", value: "<Feature-Option-ID>"},
         {id: "<Commit ID-ID>", value: "cb46a48"},
         {id: "<Commit Text-ID>", value: "[v0.25.5] PlanManager, Feature: ..."},
         {id: "<Erledigt-ID>", value: "2026-04-15"},
         {id: "<Chat erstellt-ID>", value: "https://claude.ai/chat/d546b50b-..."},
         {id: "<Chat erledigt-ID>", value: "https://claude.ai/chat/015353fe-..."},
         {id: "<Chat-Anker-erledigt-ID>", value: "[BPM-ANCHOR-<task-id>] - erledigt: Commit cb46a48"}
       ]
     )
  10. Memory `[ANKER-LIVE]`: Einträge zu BPM-007 entfernen
```
