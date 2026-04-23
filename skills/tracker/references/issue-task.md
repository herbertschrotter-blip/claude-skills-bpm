# tracker issue — Skill-Issue-Task anlegen

Vollständiger Ablauf für das `tracker issue` Kommando.
Issue-Tasks leben in Skill-Issues-Listen (projekt-spezifisch, siehe
`projects/<[PROJECT]>/clickup-lists.md` Abschnitt 2b).

Abgrenzung zu `create-task.md`: Dort geht es um Haupttasks im Projekt-Scope
(BPM-Listen, ClaudeSkills-Liste). Hier geht es um Skill-Issues-Scope
(6 Custom Fields, eigenes Typ-Dropdown, `<skill>-NNN` Nummerierung).

---

## Kommando

`tracker issue <skill-name>: <kurztitel>`

### Beispiele

- `tracker issue tracker: Em-Dash in API-Calls`
- `tracker issue chat-wechsel: Memory-Scan vergisst Rubriken`
- `tracker issue cc-steuerung: PowerShell verschluckt $-Variablen`

### Gültige Skill-Namen

Die Liste gültiger Skill-Namen steht in
`projects/<[PROJECT]>/clickup-lists.md` (Abschnitt "Gültige Skill-Namen für `tracker issue`").

Bei unbekanntem Skill-Name: `ask_user_input_v0` mit den vorhandenen Skills
als Optionen. **Nie raten.**

---

## Ablauf

### 1. Skill-Name validieren

- Aus Kommando-Text extrahieren (zwischen `tracker issue ` und `:`)
- Gegen Liste aus `projects/<[PROJECT]>/clickup-lists.md` abgleichen
- Bei Unstimmigkeit: `ask_user_input_v0` mit gültigen Werten

### 2. Ziel-Listen-ID ermitteln

- Lookup in `projects/<[PROJECT]>/clickup-lists.md` Abschnitt "Skill Issues"
- Listen-ID merken für alle nachfolgenden Schritte

### 3. Dedup-Suche

- `clickup_filter_tasks(list_ids: ["<ziel-listen-id>"])`
- In Ergebnissen Titel und Description auf Ähnlichkeit zum Kurztitel prüfen
- Bei Treffer: `ask_user_input_v0`:
  - "Neu anlegen"
  - "Bestehenden nutzen" (liefert Task-ID zurück, kein Create)
  - "Abbrechen"

### 4. Issue-ID automatisch ermitteln

**Ziel-Lösung (tracker-003):** Issue-ID wird automatisch vom Skill ermittelt,
ohne User-Bestätigung der Nummer. Der User wird nur gefragt wenn der
Unique-Check nach der Anlage eine Race Condition zeigt.

**Ablauf:**

1. `clickup_filter_tasks(list_ids: ["<ziel-listen-id>"], include_closed: true)`
   — alle Issues laden, auch `done`/`complete`-Status. Ohne `include_closed: true`
   würden hohe erledigte Nummern übersprungen werden.

2. Für jeden Task: Custom Field `Issue-ID` (`e286a04a-...`) aus
   `custom_fields`-Array lesen.

3. Pattern-Match `^<skill>-(\d{3})$` (z.B. `^tracker-(\d{3})$`). Tasks mit
   ungültigem Format stillschweigend ignorieren.

4. Höchste Nummer `N_max` aus allen gültigen Matches finden.

5. Neue Issue-ID: `<skill>-<N_max + 1>` (3-stellig mit führenden Nullen).

6. **Edge Cases:**
   - Leere Liste oder keine gültigen Formate: erste Nummer = `<skill>-001`
   - Lücken (z.B. `tracker-001`, `tracker-003` vorhanden): nächste = `tracker-004`,
     **nicht** `tracker-002`. Lücken bewusst nicht füllen — sonst brechen
     Chat-Anker-Referenzen aus alten Sessions.

7. **Unique-Check nach Task-Anlage (Race Condition):** Nach `clickup_create_task`
   erneut `clickup_filter_tasks` mit derselben `list_ids` ausführen und
   zählen wieviele Tasks die soeben vergebene Issue-ID haben. Bei >1 Treffer
   (parallele Erstellung hat kollidiert): nächste Nummer `N_max + 2` vergeben,
   den neu angelegten Task via `clickup_update_task` korrigieren (Titel +
   Custom Field `Issue-ID`).

**Chat-Output für den User:**
```
Ermittelt: <skill>-NNN (höchste vorhandene: <skill>-<N_max>)
```
Keine Prosa-Frage zur Nummer. Bei Race-Condition-Korrektur: zusätzlicher
Hinweis im Chat.

### 5. Description-Template generieren

Verkürztes Template für Skill-Issues:

```markdown
## Problem
<Was ist kaputt / was fehlt / welcher Trigger fehlt>

## Lösungsansatz
<Wie lösen. "Offen" wenn noch nicht klar>

## Definition of Done
- [ ] Skill-Datei(en) angepasst
- [ ] Commit mit Hash im Custom Field
- [ ] Chat-Skill-Sync durchgeführt (SKILL.md als Artifact)

## Abhängigkeiten
<Bezug zu anderen Issues / Tasks>

## Beobachtungs-Chat
<Chat-Name in dem das Issue erkannt wurde>
```

Anpassungen nach Typ:
- **Bug** → "Schritte zur Reproduktion" statt "Problem"
- **Trigger-Fehler** → "Erwartetes Trigger-Verhalten" + "Tatsächliches Verhalten"
- **Doku-Fehler** → "Fehlerhafte Stelle" (mit Datei+Zeile) + "Korrekte Beschreibung"
- **Verbesserung** / **Refactor-Idee** → Template wie oben

### 6. Task anlegen

```
clickup_create_task(
  list_id: "<ziel-listen-id>",
  name: "<skill>-NNN: <kurztitel>",
  priority: "<ggf. aus Kontext, sonst normal>",
  markdown_description: "<Template aus Schritt 5>",
  custom_fields: [
    {"id": "<Issue-ID-Field>",          "value": "<skill>-NNN"},
    {"id": "<Typ-Field>",               "value": "<Typ-Option-ID>"},
    {"id": "<Beobachtungs-Chat-Field>", "value": "<Chat-Name>"}
  ]
)
```

Field-IDs und Option-IDs: `projects/<[PROJECT]>/clickup-fields.md` Abschnitt 2.

### 7. Pro-Task-Quittung im Chat

Direkt nach `clickup_create_task`:
```
✅ <skill>-NNN — [BPM-ANCHOR-<task-id>] — erstellt: <kurztitel>
```

### 8. Chat-Anker mit echter Task-ID nachtragen

```
clickup_update_task(
  task_id: "<neue-task-id>",
  custom_fields: [
    {"id": "<Chat-Anker-erstellt-Field>",
     "value": "[BPM-ANCHOR-<neue-task-id>] - erstellt: <kurztitel>"}
  ]
)
```

### 9. Memory `[ANKER-LIVE]` eintragen

Siehe universelle Spec in `anker-system.md` — Typ `erstellt`, Format:
`[ANKER-LIVE] <task-id>|<typ>|<timestamp>|<kurzbeschreibung>`

---

## Typ-Dropdown (Skill-Issues-Scope)

Wenn User keinen Typ angibt: `ask_user_input_v0` mit:
- Bug
- Trigger-Fehler
- Doku-Fehler
- Verbesserung
- Refactor-Idee

Option-IDs stehen in `projects/<[PROJECT]>/clickup-fields.md` Abschnitt 2
(Skill-Issues-Typ-Dropdown).

**Unterschied zu BPM-Scope:** Skill-Issues-Typ hat 5 Optionen (Bug /
Trigger-Fehler / Doku-Fehler / Verbesserung / Refactor-Idee). BPM-Scope hat
7 Optionen (Feature / Fix / Refactor / Perf / Docs / Konzept / Meta).
Nie verwechseln — Option-IDs sind pro Scope unterschiedlich.

---

## Status-Werte

Skill-Issues-Listen nutzen `to do` / `in progress` / `complete`
(siehe `projects/<[PROJECT]>/clickup-fields.md` Abschnitt 7).
Beim Anlegen greift der Default-Status der Liste (meist `to do`).

**NICHT** `done` verwenden — das ist BPM-Scope.

---

## Beispiel-Workflow (BPM-Projekt)

```
User: tracker issue tracker: Em-Dash-Problem in Custom-Field-Values

Claude intern:
  1. Skill-Name: "tracker" → gültig (aus projects/bpm/clickup-lists.md)
  2. Listen-ID Lookup: 901522952249
  3. Dedup: clickup_filter_tasks → kein Treffer
  4. Issue-ID automatisch:
     - clickup_filter_tasks(list_ids: ["901522952249"], include_closed: true)
     - Custom Field Issue-ID jedes Tasks lesen
     - Pattern ^tracker-(\d{3})$ parsen
     - Höchste Nummer: 008 (aus tracker-008)
     - Neue Issue-ID: tracker-009
     - Chat-Output: "Ermittelt: tracker-009 (höchste vorhandene: tracker-008)"
  5. Typ-Frage: ask_user_input_v0 → User: "Bug"
  6. Beobachtungs-Chat: "Bauprojektmanager Teil 28"
  7. Description-Template mit Bug-Anpassung generieren
  8. clickup_create_task(
       list_id: "901522952249",
       name: "tracker-009: Em-Dash-Problem in Custom-Field-Values",
       custom_fields: [
         {id: "<Issue-ID-Field>",          value: "tracker-009"},
         {id: "<Typ-Field>",               value: "<Bug-Option-ID>"},
         {id: "<Beobachtungs-Chat-Field>", value: "Bauprojektmanager Teil 28"}
       ]
     )
     → Task-ID 86c9xyz
  9. Unique-Check: clickup_filter_tasks → genau 1 Treffer mit tracker-009 ✓
  10. Pro-Task-Quittung:
      ✅ tracker-009 — [BPM-ANCHOR-86c9xyz] — erstellt: Em-Dash-Problem in Custom-Field-Values
  11. Chat-Anker nachtragen mit Task-ID 86c9xyz
  12. Memory [ANKER-LIVE] Eintrag
```

---

## VERBOTEN

- Skill-Name raten wenn unklar → `ask_user_input_v0`
- Issue-ID manuell vom User bestätigen lassen — Auto-Nummerierung ist Pflicht gemäß tracker-003
- `clickup_filter_tasks` ohne `include_closed: true` für Nummerierungs-Scan — höchste Nummer könnte done/complete sein und würde übersprungen
- Höchste Nummer aus Memory rekonstruieren statt live abzufragen — Memory kann veraltet sein
- Lücken in Nummerierung füllen — Chat-Anker-Referenzen gehen sonst kaputt
- Unique-Check nach Task-Anlage weglassen — Race Condition bei paralleler Erstellung erzeugt Duplikate
- Status `done` verwenden — Skill-Issues nutzen `complete`
- BPM-Scope Custom Fields verwenden (Typ `f7b8c62a`, Aufwand `ecc194e5`, etc.)
  — Skill-Issues haben eigenen Scope (Typ `5b45b13a`, Issue-ID `e286a04a`, etc.)
- Issue-ID nur im Titel setzen, aber Custom Field `Issue-ID` leer lassen —
  beide müssen gesetzt sein
- BPM-Modul-Kürzel (PM, DOC, ...) im Titel verwenden — Skill-Issues haben
  Format `<skill>-NNN:`, kein Kürzel-Block
- Meilenstein-Tags (v1, post-v1, etc.) setzen — gelten nur für BPM-Scope

---

## Abhängigkeiten

- `projects/<[PROJECT]>/clickup-lists.md` muss Abschnitt 2b mit allen
  Skill-Issue-Listen enthalten
- `projects/<[PROJECT]>/clickup-fields.md` muss Abschnitt 2 mit
  Skill-Issues-Scope (6 Fields + 5 Typ-Option-IDs) enthalten
- `anker-system.md` für Memory-`[ANKER-LIVE]`-Format
- `batch-protocol.md` wenn mehrere Issues in einer Antwort angelegt werden
