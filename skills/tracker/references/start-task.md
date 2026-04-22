# tracker start — Task + Parent auf "in progress" setzen

Setzt einen Subtask auf `in progress` und aktualisiert den Parent-Task
ebenfalls (nur wenn Parent aktuell `open`/`to do`).

Fixt `tracker-002` (Start-Kommando setzte Status nicht).

---

## Kommando

`tracker start: <BPM-ID oder Issue-ID>`

### Implizite Trigger (nur mit Task-ID im Satz!)

Folgende Natural-Language-Phrasen lösen eine **Rückfrage** aus (nicht
automatisch ausführen):

- `"starte BPM-NNN"` / `"starte tracker-002"`
- `"BPM-NNN starten"` / `"Issue-XXX starten"`
- `"fangen wir mit BPM-NNN an"`
- `"los mit BPM-NNN"`
- `"wir machen jetzt BPM-NNN"`

Bei Treffer: `ask_user_input_v0`:
```
Frage: "BPM-NNN + Parent auf 'in progress' setzen?"
Optionen:
- "Ja — beide"
- "Nur Subtask"
- "Nein"
```

**VERBOTEN:** Implizite Erkennung OHNE Task-ID im Satz.
Phrasen wie `"los geht's"`, `"fangen wir an"`, `"starten wir"` OHNE BPM-Nummer
werden ignoriert. Keine rate-basierte Task-Erkennung.

### Fokus-Entscheidung im Dialog (dritte Trigger-Art)

Wenn im Gesprächsverlauf ein Task **zum Arbeitsfokus wird** — auch ohne dass
der User explizit das Wort "starte" verwendet — MUSS Claude `tracker start`
ausführen bevor mit inhaltlicher Arbeit begonnen wird.

**Auslöser:**

- Claude hat einen konkreten Task-Fix vorgeschlagen (`"als nächstes tracker-002"`
  / `"wir machen jetzt BPM-082"`)
- User bestätigt mit `"ja"`, `"ok"`, `"weiter"`, `"mach"`, `"passt"`, `"genau"`,
  `"los"`, `"gemacht"` — oder irgendeiner anderen Zustimmung
- → **In der darauffolgenden Antwort ZUERST `tracker start`**, dann Analyse/Code

**Voraussetzung:** Der zu fokussierende Task muss **eindeutig aus dem vorigen
Turn hervorgehen**. Wenn mehrere Tasks im Raum stehen: `ask_user_input_v0`
welcher gestartet werden soll.

**Beispiel:**

```
Claude: "Vorschlag: Als nächstes tracker-002 Fix — drei Optionen..."
User:   "Vorschlag OK — Option A + restriktives B"

→ In der Antwort die mit "Plan fix:" beginnt:
   1. tracker_update_task(tracker-002, status: "in progress")  ← ZUERST
   2. Pro-Task-Quittung
   3. Erst DANN "Plan fix: ..."
```

Diese Regel korrigiert einen beobachteten Bug: In Session Teil 28 wurde
zwischen User-Freigabe und Beginn der Implementierung der Status nicht
gesetzt — obwohl der Fokus eindeutig war.

---

## Ablauf

1. **Task-ID auflösen:**
   - Explizite ID (`BPM-082`, `tracker-003`) → direkt nutzen
   - Kurzform (`4.1`, `3.5`): via `clickup_search` den passenden Task finden
   - Bei mehreren Treffern: `ask_user_input_v0`

2. **Aktuellen Status prüfen:** `clickup_get_task(task_id)` → wenn schon
   `in progress` oder `done`/`complete`: keine Aktion, Hinweis an User

3. **Subtask-Status setzen:**
   ```
   clickup_update_task(
     task_id: <id>,
     status: "in progress"
   )
   ```

4. **Parent ermitteln:** `clickup_get_task` liefert `parent`-Feld
   - Wenn `parent` null: kein Parent vorhanden → zu Schritt 6
   - Wenn `parent` vorhanden: weiter

5. **Parent-Status prüfen und ggf. setzen:**
   - `clickup_get_task(parent_id)` → aktuellen Status lesen
   - Nur wenn Parent auf `open` / `to do`: auch auf `in progress` setzen
   - Wenn Parent schon `in progress` / `done` / `complete`: keine Änderung

6. **Pro-Task-Quittung im Chat** (pro geändertem Task):
   ```
   ✅ <BPM-ID oder Issue-ID> — [BPM-ANCHOR-<task-id>] — start: in progress
   ✅ <Parent-ID> — [BPM-ANCHOR-<parent-task-id>] — start: in progress (als Parent)
   ```

7. **Batch-Audit** (wenn Parent mit geändert wurde):
   ```
   Batch-Audit: 2/2 Body-Anker ✅ | 2/2 Custom Fields (Status) ✅
   ```

8. **Erst DANN inhaltliche Arbeit beginnen.**

---

## Status-Werte pro Listen-Typ

Nicht alle ClickUp-Listen nutzen die gleichen Status-Werte. Aktueller Stand:

| Listen-Typ | open | in progress | done |
|---|---|---|---|
| BPM-Listen | `open` | `in progress` | `done` |
| Skill-Issue-Listen | `to do` | `in progress` | `complete` |

Bei `tracker start` ist nur `in progress` relevant — der Wert ist
listen-übergreifend gleich.

Bei `tracker done`: Fallback-Reihenfolge `done` → `complete`. Bei Fehler
`ask_user_input_v0` mit Alternativen.

---

## VERBOTEN

- Impliziter Start-Trigger OHNE Task-ID im Satz (Prosa-Phrasen wie
  "los geht's" triggern NICHT)
- Status-Änderung ohne Pro-Task-Quittung
- Parent ohne Check auf aktuellen Status automatisch überschreiben
  (wenn Parent schon `in progress` oder `done`: nichts tun)
- Inhaltliche Arbeit beginnen BEVOR `tracker start` ausgeführt wurde
- Raten welche Task-ID gemeint ist wenn unklar — `ask_user_input_v0`

---

## Beispiel-Workflow

### Explizites Kommando

```
User: tracker start: tracker-002

Claude intern:
  1. Task-ID: tracker-002 → 86c9f7cm4 (aus Issue-ID-Lookup)
  2. clickup_get_task(86c9f7cm4) → status = "to do", parent = null
  3. clickup_update_task(86c9f7cm4, status: "in progress")
  4. Kein Parent → Schritt 6
  6. Pro-Task-Quittung im Chat:
     ✅ tracker-002 — [BPM-ANCHOR-86c9f7cm4] — start: in progress
  8. Inhaltliche Arbeit beginnt.
```

### Impliziter Trigger mit Task-ID

```
User: fangen wir mit tracker-002 an

Claude:
  [ask_user_input_v0]
  Frage: "tracker-002 auf 'in progress' setzen? (Kein Parent vorhanden.)"
  Optionen: Ja / Nein

  User: Ja
  → Ablauf wie oben
```

### Impliziter Trigger mit Parent

```
User: starte 4.1

Claude intern:
  1. clickup_search "4.1" → Task 86c9xyz (Parent: 86c9parent)
  2. ask_user_input_v0:
     "4.1 + Parent (Phase 4) auf 'in progress' setzen?"
     Optionen: Ja - beide / Nur Subtask / Nein
  3. User: Ja - beide
  4. clickup_update_task(86c9xyz, "in progress")
  5. clickup_get_task(86c9parent) → status = "to do"
  6. clickup_update_task(86c9parent, "in progress")
  7. Quittungen:
     ✅ 4.1 — [BPM-ANCHOR-86c9xyz] — start: in progress
     ✅ Phase-4 — [BPM-ANCHOR-86c9parent] — start: in progress (als Parent)
     Batch-Audit: 2/2 Body-Anker ✅ | 2/2 Custom Fields ✅
```
