# Batch-Protokoll — Pro-Task-Disziplin bei Mehrfach-Operationen

**Zweck:** Erzwingt dass bei Batch-Operationen (≥2 Task-Operationen in derselben Antwort) pro einzelnem Task alle Disziplinen eingehalten werden — Body-Anker im Chat, Custom Fields in ClickUp, Commit-Info.

**Bezug zu Issues:**
- `tracker-001` — Custom Fields werden bei Batch nicht pro Task gesetzt
- `tracker-004` — Body-Anker im Chat-Text wird bei Batch vergessen

Beide haben dieselbe Wurzel: Claude verliert bei Mehrfach-Operationen die pro-Task-Konsequenz. Dieses Protokoll löst beides durch **Format-Zwang statt Erinnerungs-Disziplin**.

---

## 1. Batch-Definition

**Batch** = ≥2 schreibende Task-Operationen in derselben Antwort. Schreibend heißt:

- `clickup_create_task` (tracker neu)
- `clickup_update_task` mit Status-Änderung (tracker start, tracker done)
- `tracker start` mit Parent-Kaskade zählt als **2 Operationen** (Subtask + Parent)

Auch wenn die Tasks inhaltlich unabhängig sind (z.B. 3 Issue-Tasks in verschiedenen Listen) gilt dieses Protokoll — die Disziplin-Lücke entsteht durch die Anzahl der Operationen, nicht durch deren thematische Verwandtschaft.

**KEIN Batch:**
- 1 Task-Create + beliebig viele Custom-Field-Updates am selben Task (zählt als 1 Operation)
- `clickup_search` / `clickup_get_task` ohne schreibenden Folgecall
- Mehrfaches `clickup_update_task` am selben Task (gleiche Task-ID = 1 Operation)
- `tracker start` ohne Parent (1 Operation) → keine Batch-Pflicht, aber Pro-Task-Quittung bleibt

---

## 2. Pro-Task-Quittung (PFLICHT)

Nach **jedem** schreibenden Tool-Call (create oder status-ändernder update) steht **im selben Antwort-Block, bevor der nächste Tool-Call startet**, eine Quittungszeile:

```
✅ <BPM-ID oder Issue-ID> — [BPM-ANCHOR-<task-id>] — <typ>: <kurz>
```

Beispiele:
```
✅ BPM-082 — [BPM-ANCHOR-86c9cg8u5] — erstellt: Regex-Erkennung DocumentTypeRecognizer
✅ tracker-001 — [BPM-ANCHOR-86c9f7awj] — erledigt: Commit a1b2c3d Pro-Task-Quittung
✅ Phase-3-Parent — [BPM-ANCHOR-86c9eqnk6] — erledigt: via Subtask-Kaskade (3.1, 3.2, 3.3, 3.4, 3.5)
```

**Die Quittung ersetzt drei frühere Elemente in einem Format:**
- Bestätigung an User
- Body-Anker (tracker-004)
- Audit-Spur für spätere `conversation_search`

**VERBOTEN:**
- Zusammengefasste Quittungen ("6 Tasks erstellt")
- Tabellen statt einzelner Quittungszeilen
- Quittungen am Ende des Antwortblocks gesammelt nachtragen
- `"analog für die anderen"` / `"wie gehabt"` / `"..."`

---

## 2b. Referenz-Anker in Folge-Antworten (PFLICHT)

Adressiert `tracker-005`. Die Pro-Task-Quittung aus Kapitel 2 greift nur **im
Moment des Tool-Calls**. Wenn ein Task über mehrere Antworten hinweg inhaltlich
besprochen wird (Commit-Vorschlag, Klärungsfrage, Fehler-Fix, Fortschritt),
versinkt er ohne Anker im Chat.

### Format

**Am Anfang jeder Antwort** die einen bereits existierenden Task inhaltlich
betrifft:

```
Betroffene Tasks in dieser Antwort: [BPM-ANCHOR-<task-id>] <name>.
```

- Einzelner Task: `[BPM-ANCHOR-86c9feyj9] tracker-005.`
- Mehrere Tasks: `[BPM-ANCHOR-86c9feyj9] tracker-005, [BPM-ANCHOR-86c9f7awj] tracker-001.`

### Wann Pflicht

- Commit-Vorschlag für einen Task
- Klärungsfrage zu laufendem Task-Fix
- Fehler-Diagnose während Task-Arbeit
- Status-Update / Fortschrittsbericht
- Nachträgliche Analyse oder Konzept-Änderung
- Antwort in einem Thread der einen aktiven Task behandelt

### Wann NICHT Pflicht

- Task-ID nur in Aufzählung erwähnt ("die 4 tracker-Issues")
- Antwort rein über Meta/Tooling (DC, git, Skill-System)
- Rückfrage ohne Task-Bezug
- Reine Begrüßung / Abschluss

### Abgrenzung zu Pro-Task-Quittung

Die Quittung aus Kapitel 2 enthält den Anker bereits inline
(`✅ <id> — [BPM-ANCHOR-<task-id>] — <typ>: <kurz>`). Wenn in derselben
Antwort eine Quittung steht, **entfällt der separate Referenz-Anker oben**
für diesen Task.

Für Tasks die *nur erwähnt* werden (ohne Tool-Call) bleibt der Referenz-Anker
oben aber pflicht — auch wenn in derselben Antwort ein anderer Task eine
Quittung bekommt.

### Beispiele

**Quittung in der Antwort → KEIN separater Referenz-Anker für diesen Task:**

```
[clickup_update_task tracker-002 status: "in progress"]

✅ tracker-002 — [BPM-ANCHOR-86c9f7cm4] — start: in progress
```

**Reine inhaltliche Diskussion ohne Tool-Call → Referenz-Anker oben:**

```
Betroffene Tasks in dieser Antwort: [BPM-ANCHOR-86c9feyj9] tracker-005.

Dein Vorschlag A passt besser weil [...]
```

**Mix: Ein Task mit Tool-Call, zweiter nur erwähnt:**

```
Betroffene Tasks in dieser Antwort: [BPM-ANCHOR-86c9feyj9] tracker-005.

[clickup_update_task tracker-002 status: "in progress"]

✅ tracker-002 — [BPM-ANCHOR-86c9f7cm4] — start: in progress

Die Regel für tracker-005 greift danach analog [...]
```

### VERBOTEN

- Referenz-Anker weglassen in Folge-Antworten die den Task inhaltlich betreffen
- Referenz-Anker unten statt oben (erschwert Suche und Überblick)
- Referenz-Anker und Quittung für denselben Task doppelt zeigen
- Referenz-Anker für Tasks setzen die nur am Rande erwähnt werden (z.B. in langen Aufzählungen)

---

## 3. Pro-Task-Custom-Fields (PFLICHT)

Im **selben Tool-Call-Block** wie `clickup_create_task` bzw. der status-ändernde `clickup_update_task` müssen gesetzt werden:

**Bei `create`:**
- `Chat-Anker erstellt` (`512b8920-e958-4e43-826e-110e3bccdfc2`) — Wert: `[BPM-ANCHOR-<task-id>] - erstellt: <kurz>`

**Bei `done`:**
- `Chat-Anker erledigt` (`0c72a2ea-630e-4320-9cdb-80a19bc5ebb6`) — Wert: `[BPM-ANCHOR-<task-id>] - erledigt: <kurz>`
- Commit-Hash + Commit-Text (BPM: `a851a04d-...` + `cae9f6cb-...`; Skill-Issues: `8e8879f7-...`)
- Erledigt-Datum (BPM: `457bde4f-...`)

**Nicht erlaubt:** "Custom Fields setze ich am Ende für alle Tasks gesammelt" — das ist der tracker-001-Bug.

**Task-ID-Problem beim Create:**
Bei `clickup_create_task` kennt Claude die finale Task-ID erst *nach* dem Call. Deshalb zweistufig:

1. `clickup_create_task` mit Platzhalter `[BPM-ANCHOR-PENDING] - erstellt: <kurz>` im Chat-Anker-Feld
2. Sofort danach `clickup_update_task` mit der echten Task-ID: `[BPM-ANCHOR-<echte-id>] - erstellt: <kurz>`
3. Quittungszeile im Chat mit der echten Task-ID

Beide Calls zählen zusammen als **eine** Task-Operation im Sinne der Batch-Definition.

Die exakten Feld-IDs pro Workspace stehen in `clickup-fields.md`. Die dort aufgelisteten IDs sind innerhalb eines Batches **pro Task einzeln** zu senden.

**Unicode-Warnung:** Im Text-Value von Custom Fields das ASCII-Minus `-` verwenden, nicht den em-dash `—`. Letzterer hat in Session Teil 28 einen `clickup_update_task`-Fehler ausgelöst. Im Chat-Body-Anker ist `—` ok — nur in Custom-Field-Values vermeiden.

---

## 4. Ablauf bei Batch

### 4.1 Batch-Ansage (vor dem ersten Tool-Call)

```
📦 Batch: N Tasks (create: X, update: Y, done: Z)
```

Beispiel:
```
📦 Batch: 6 Tasks (create: 6, update: 0, done: 0)
```

Das zwingt Claude, **vor** Beginn die Anzahl zu verbalisieren — das ist der Counter den tracker-004 Option A vorschlägt, jetzt als Pflicht.

### 4.2 Pro Task: Tool-Call → Quittung

Reihenfolge innerhalb eines Task-Zyklus:

1. `clickup_create_task` (oder status-ändernder `clickup_update_task`) **inkl. Anker-Custom-Field im selben Call**
2. Bei `create`: Nachträglicher `clickup_update_task` mit echter Task-ID im Anker-Feld
3. Quittungszeile im Chat-Body schreiben
4. Erst jetzt zum nächsten Task übergehen

Kein Task ohne Quittung. Keine Quittung ohne vorherigen Tool-Call.

### 4.3 Subtask-Regel

Werden in einem Batch **sowohl Parent als auch Subtasks** angelegt oder erledigt:

- **Jeder Subtask** bekommt eine eigene Quittung mit eigenem Anker (Subtasks haben ihre eigene Task-ID, auch wenn sie keine BPM-Nummer führen)
- **Der Parent** bekommt eine eigene Quittung — niemals "Parent-Anker deckt Subtasks mit ab"

### 4.4 Parent-Container-Regel

Wird ein Parent-Task ausschließlich dadurch erledigt, dass alle Subtasks done sind (Kaskaden-Abschluss, keine direkte Arbeit am Parent), bekommt er trotzdem eine eigene Quittung:

```
✅ <Parent-ID> — [BPM-ANCHOR-<parent-task-id>] — erledigt: via Subtask-Kaskade (<liste der subtask-bezüge>)
```

Das adressiert Fall 3 aus tracker-001 (Parent bekommt keinen Anker weil keine direkte Arbeit). Ohne diese Regel bleibt der Parent-Abschluss im Chat unauffindbar.

### 4.5 Batch-Audit (am Ende)

Nach der letzten Quittung **muss** eine Audit-Zeile folgen:

```
Batch-Audit: N/N Body-Anker ✅ | N/N Custom Fields ✅
```

Falls nicht N/N:
- Fehlende Quittungen **sofort nachholen**, nicht einfach weiterschreiben
- Fehlende Custom Fields per zusätzlichem `clickup_update_task` pro Task nachtragen
- Erneuter Audit bis N/N

**N** ist die Zahl aus der Batch-Ansage (4.1). Diese muss wieder auftauchen — das verhindert dass Claude "vergisst" wie viele Tasks der Batch eigentlich hatte.

---

## 5. Memory `[ANKER-LIVE]` bei Batch

Die Lifecycle-Regeln aus `anker-system.md` gelten **pro Task einzeln**:

| Pro Task im Batch | Memory-Aktion |
|---|---|
| `create` mit TEMP | TEMP-Eintrag ersetzen durch Task-ID-Eintrag (Typ `erstellt`) |
| `create` ohne TEMP | Neuer Eintrag (Typ `erstellt`) |
| `done` | Beide Einträge (erstellt + ggf. erledigt) entfernen |

**Keine Sammelaktualisierung am Batch-Ende.** Jeder `memory_user_edits`-Call ist Teil des Pro-Task-Zyklus aus 4.2.

---

## 6. Integration mit anderen Skills

### 6.1 `chat-wechsel`

Am Chat-Ende werden oft mehrere Tasks gleichzeitig erledigt (Batch-Abschluss). Das gesamte Batch-Protokoll gilt dort uneingeschränkt — kein "vereinfachtes Abschluss-Protokoll" nur weil es um Übergabe geht.

### 6.2 `code-erstellen`

Nach Commit wird typischerweise **ein** Task erledigt → kein Batch. Erst wenn ein Commit mehrere Tasks abschließt, greift dieses Protokoll.

### 6.3 `skill-pflege` / `skill-neu`

Wenn in einem Skill-Update mehrere Skill-Issues gemeinsam gelöst werden, ist der Abschluss dieser Issues ein Batch. Das Protokoll gilt.

---

## 7. VERBOTEN (Batch-spezifisch)

- Tabelle statt einzelner Quittungszeilen
- Gesammelte Anker-Liste am Ende ("hab ich jetzt alle auf einmal nachgetragen")
- Parent-Anker nutzen um Subtask-Anker zu sparen
- Custom Fields nur am ersten oder letzten Task des Batches setzen
- Batch-Audit weglassen
- em-dash `—` in Custom-Field-Values (nur ASCII `-` verwenden)
- Quittung schreiben ohne dass der Tool-Call vorher stattgefunden hat (Reihenfolge-Bruch)
- Mehrere Tool-Calls hintereinander ohne zwischendurch Quittungen (Batch-Aufschub)

---

## 8. Live-Test-Beispiel (Session Teil 28)

**Kontext:** 2 Issues gleichzeitig in cc-steuerung-Liste anlegen.

```
📦 Batch: 2 Tasks (create: 2, update: 0, done: 0)

[clickup_create_task cc-steuerung-001 mit Anker-Platzhalter]
[clickup_update_task 86c9fczy4 mit echter Anker-ID]
✅ cc-steuerung-001 — [BPM-ANCHOR-86c9fczy4] — erstellt: DC-Erkennung am Chat-Start

[clickup_create_task cc-steuerung-002 mit Anker-Platzhalter]
[clickup_update_task 86c9fd0g0 mit echter Anker-ID]
✅ cc-steuerung-002 — [BPM-ANCHOR-86c9fd0g0] — erstellt: DC PowerShell verschluckt Dollar-Variablen

Batch-Audit: 2/2 Body-Anker ✅ | 2/2 Custom Fields ✅
```

Das ist das Referenz-Format. Abweichungen sind Regel-Verstöße.
