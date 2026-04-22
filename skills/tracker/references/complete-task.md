# tracker done — Task abschließen

Vollständiger Ablauf, Commit-Ermittlung und Beispiel-Workflow für `tracker done`.

---

## Kommando

`tracker done: <Stichwort oder BPM-NNN>`

---

## Ablauf

1. **Task finden** via `clickup_search` (falls BPM-NNN nicht explizit)
2. **Mehrere Treffer** → mit `ask_user_input_v0` User wählen lassen
3. **Commit-Infos ermitteln** (Pflicht):
   - Wenn Task Code-Bezug hat (SET/PM/INF/APP/DOM/THM):
     - Claude fragt User: "Welche Datei(en) sind betroffen?" (Prosa, offene Frage!)
     - Per DC: `git log -1 --format="%h|%ad|%s" --date=short -- <Datei>`
     - Oder: `git log --all --diff-filter=A --format="%h %ad %s" --date=short -- <Datei>` (erste Erwähnung)
     - Oder: `git log --grep="vX.Y.Z" --format="%h %ad %s" --date=short` (Version bekannt)
   - Wenn Task reiner Doc-Bezug (DOC/KON):
     - Gleicher Weg, aber auf Docs/ Pfade
   - Wenn Task keinen Code-Bezug hat (z.B. Meta-Task):
     - Commit ID + Commit Text leer lassen
     - Erledigt-Datum = heute (YYYY-MM-DD)
4. **Bei mehreren Commits:** `ask_user_input_v0` mit allen Kandidaten (Hash + erste Zeile)
5. **Anker-Text in Chat schreiben** (direkt vor `clickup_update_task`):
   ```
   [BPM-ANCHOR-<task-id>] — erledigt: Commit <hash> <kurzbeschreibung>
   ```
6. **Nachpflege-Felder prüfen** (falls bei `tracker neu` nicht gesetzt):
   - Typ, Aufwand, Zielversion, Komponente, Zugehörige Docs
   - Falls alle leer: `ask_user_input_v0` mit fehlenden Feldern
7. **Custom Fields vorbereiten**:
   ```
   custom_fields = [
     {"id": "a851a04d-f34a-429f-abce-bec0b0b6859f", "value": "<7-char-hash>"},
     {"id": "cae9f6cb-e0eb-44aa-81f8-df2e1194111e", "value": "<erste Zeile der Commit-Message>"},
     {"id": "457bde4f-c9c1-40ab-b464-897b7f87e6bc", "value": "<YYYY-MM-DD>"},
     {"id": "0c72a2ea-630e-4320-9cdb-80a19bc5ebb6", "value": "<task-id>"},
     // + Nachpflege-Felder falls gesetzt
   ]
   ```
8. **Einziger API-Call**:
   ```
   clickup_update_task(
     task_id: "<TaskID>",
     status: "done",     ← KLEINGESCHRIEBEN (case-sensitive)
     custom_fields: custom_fields
   )
   ```
9. **Memory `[ANKER-LIVE]` aufräumen**:
   - Eintrag mit Task-ID und Typ `erstellt` entfernen
   - Falls temporär ein Typ `erledigt` gesetzt wurde: auch entfernen
   - Nach diesem Schritt existiert im Memory nichts mehr zu diesem Task
10. **Bestätigung** an User:
    ```
    ✅ BPM-XXX auf Done gesetzt
       Commit: <hash> — <Erste Zeile der Message>
       Erledigt: <YYYY-MM-DD>
       Anker: [BPM-ANCHOR-<task-id>] (erstellt + erledigt)
    ```
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

## Beispiel-Workflow: tracker done mit vollständiger Chat-Ermittlung

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
  8. clickup_update_task(
       status: "done",
       custom_fields: [
         {id: "<Typ-ID>", value: "<Feature-Option-ID>"},
         {id: "<Commit ID-ID>", value: "cb46a48"},
         {id: "<Commit Text-ID>", value: "[v0.25.5] PlanManager, Feature: ..."},
         {id: "<Erledigt-ID>", value: "2026-04-15"},
         {id: "<Chat erstellt-ID>", value: "https://claude.ai/chat/d546b50b-..."},
         {id: "<Chat erledigt-ID>", value: "https://claude.ai/chat/015353fe-..."}
       ]
     )
  9. Bestätigung: "✅ BPM-007 Done. Commit cb46a48 (Teil 17), Ausarbeitung Teil 10, Typ Feature."
```
