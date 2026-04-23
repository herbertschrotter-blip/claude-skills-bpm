# Review-Workflow vor Task-Übergang

Verbindlicher Scope-Check BEVOR ein Task auf done gesetzt wird, ein neuer
gestartet wird, oder der Arbeitsfokus auf einen anderen Task wechselt.

Fixt `tracker-006` (fehlender Scope-Check führte in Session Teil 28 zu
versickernden Besprechungs-Ergebnissen bei 7.1 → 7.6).

---

## Zweck

Wenn im Chat neue Regeln, Entscheidungen oder Strukturänderungen besprochen
werden, ändert sich oft der Scope bestehender Tasks. Ohne expliziten Check
werden Parent-Scope, Sibling-Subtasks oder verweisende offene Tasks nicht
mit aktualisiert — Besprechungs-Ergebnisse gehen verloren.

Der Review-Workflow stellt sicher, dass **vor jedem Task-Übergang** alle
betroffenen Tasks geprüft und ggf. angepasst werden.

---

## Trigger

Der Check MUSS ausgeführt werden bevor:

1. `tracker done` ausgeführt wird
2. `tracker start` auf einen **neuen** Task ausgeführt wird
3. `tracker start` auf einen **bereits gestarteten** Task ausgeführt wird (Task-Wechsel)
4. Der Arbeitsfokus im Dialog wechselt (Fokus-Entscheidung gemäß `start-task.md`)
5. Nach expliziter User-Bestätigung wie `"das merken wir uns so"` / `"so machen wir's"` / `"passt, weiter"`

---

## 4-Punkte-Scope-Check

### Punkt 1: Aktueller Task — Description ändert sich?

Prüfen ob die im Chat besprochenen Erkenntnisse die Task-Description
betreffen (Problem, Lösungsansatz, Acceptance Criteria, Definition of Done,
Technische Notizen).

**API:**
```
clickup_get_task(task_id: <aktueller Task>)
```

**Entscheidung:**
- Description passt noch → weiter zu Punkt 2
- Description veraltet → `clickup_update_task` mit neuer `markdown_description`

### Punkt 2: Parent-Task — Scope/Description betroffen?

**API:**
```
task = clickup_get_task(task_id: <aktueller Task>)
if task.parent:
    parent = clickup_get_task(task_id: task.parent)
```

**Prüfen:**
- Parent-Scope (Problem, Lösungsansatz) noch korrekt?
- Parent-DoD noch erreichbar mit dem geänderten Subtask-Scope?
- Parent-Acceptance-Criteria noch vollständig oder fehlen jetzt welche?

**Entscheidung:**
- Parent passt → weiter zu Punkt 3
- Parent muss angepasst werden → `clickup_update_task` auf Parent
- Parent-Scope ist jetzt zu groß/klein → ggf. neue Subtask anlegen oder Scope verschieben

### Punkt 3: Sibling-Subtasks im selben Parent — betroffen?

**API:**
```
if task.parent:
    siblings = clickup_filter_tasks(
        list_ids: [<list-id des Parents>],
        include_closed: true
    )
    # Filter: siblings wo parent == task.parent, task_id != aktueller task
```

**Alternative wenn Parent Subtasks kennt:**
```
parent_detail = clickup_get_task(task_id: parent.id, subtasks: true)
# parent_detail.subtasks enthält alle Kinder
```

**Prüfen:**
- Gibt es Siblings deren Scope sich durch die neue Regel ändert?
- Würden Siblings jetzt überflüssig / doppelt abgedeckt?
- Fehlen jetzt neue Siblings die vorher nicht geplant waren?

**Entscheidung:**
- Siblings passen → weiter zu Punkt 4
- Sibling-Description veraltet → `clickup_update_task`
- Sibling überflüssig → Status auf `closed`/`complete` mit Begründung in Description oder Komm
- Neuer Sibling nötig → `clickup_create_task` mit `parent` gesetzt, korrekter NN.NN-Nummerierung

### Punkt 4: Verweisende offene Tasks — betroffen?

Tasks die den aktuellen Task über `linked_tasks`, `dependencies` oder
Text-Verweise in ihrer Description referenzieren.

**API:**
```
# 1. Direkte Links aus Task-Detail
task_detail = clickup_get_task(task_id: <aktueller Task>)
linked = task_detail.linked_tasks  # Array mit verlinkten Task-IDs
deps   = task_detail.dependencies  # Array mit Dependency-Infos

# 2. Text-Verweise in anderen offenen Tasks
# Suche in offenen Tasks nach Text-Erwähnungen der aktuellen Task-ID
clickup_search(
    keywords: "<aktuelle Task-ID oder Issue-ID>",
    filters: {task_statuses: ["unstarted", "active"]}
)
```

**Prüfen:**
- Verweist ein offener Task auf den Scope/das Verhalten, das sich jetzt ändert?
- Würde die Änderung die Ausführung eines anderen offenen Tasks blockieren oder erleichtern?
- Muss die Reihenfolge der Abarbeitung angepasst werden?

**Entscheidung:**
- Keine Betroffenheit → Check abgeschlossen
- Verweisender Task muss angepasst werden → Description update oder neue Dependency
- Verweisender Task wird jetzt unnötig → mit User besprechen (ask_user_input_v0)

---

## Nach dem Check: Reihenfolge neu vorschlagen

Wenn der Check Änderungen ergeben hat die die Abarbeitungs-Reihenfolge
beeinflussen:

```
ask_user_input_v0:
  question: "Nach dem Scope-Check hat sich die Reihenfolge geändert. Wie weitermachen?"
  options:
    - "Mit geplantem Task weitermachen"
    - "Stattdessen betroffenen Task XY zuerst"
    - "Pause - ich schaue mir das an"
```

Wenn keine Änderungen nötig waren: Direkt mit dem ursprünglichen Task-Übergang
weitermachen (ohne extra Nachfrage).

---

## Wann der Check ENTFÄLLT

- Bei reinen Pflege-Updates (`tracker update` auf ein einzelnes Feld ohne Scope-Änderung)
- Bei Zero-Change-Tasks (Memory-Edit, Description-Tippfehler)
- Wenn der User explizit sagt `"Scope-Check überspringen"` / `"skip review"` — dann einmalig entfällt der Check, nicht permanent

---

## VERBOTEN

- Scope-Check vor Task-Übergang weglassen (auch bei vermeintlich "kleinen" Tasks)
- Nur Punkt 1 prüfen und Punkte 2-4 überspringen — alle 4 Punkte sind Pflicht wenn Trigger greift
- Task auf done setzen während verweisende offene Tasks den Scope ändern würden
- Start auf neuen Task ohne Check auf Auswirkungen auf bereits laufende Tasks
- User-Bestätigung `"so machen wir's"` annehmen ohne Parent/Siblings zu prüfen
- Gefundene Änderungen nur mündlich notieren, nicht in ClickUp eintragen
- Check nach dem Task-Übergang nachholen — muss VORHER passieren

---

## Beispiel-Ablauf (aus Session Teil 28, Auslöser dieser Regel)

```
Kontext: Phase 7 der ClaudeSkills-Refactor. Task 7.1 wird auf done gesetzt.
Im Chat wurde zwischen 7.1 und 7.6 beschlossen, dass alle Skill-internen
Projekt-Daten aus projects/bpm/ gelesen werden müssen.

OHNE Review-Workflow:
  → 7.1 wird auf done gesetzt
  → 7.6 wird gestartet
  → Erst beim Umsetzen von 7.6 wird bemerkt dass 7.2, 7.3 und 7.4 auch
    den neuen projects/bpm/-Ansatz brauchen, aber ihre Description das
    nicht reflektiert.
  → Chaos, Nachbesserungs-Loop.

MIT Review-Workflow (bevor 7.1 auf done gesetzt wird):
  Punkt 1: 7.1 Description → passt noch.
  Punkt 2: Parent Phase-7 → Scope passt, aber DoD erwähnt projects/bpm/ nicht.
           → Parent-DoD ergänzen.
  Punkt 3: Siblings 7.2, 7.3, 7.4, 7.5, 7.6 → alle haben Description aus
           vor-projects/bpm/-Zeit.
           → Descriptions aller Siblings updaten mit dem neuen Ansatz.
  Punkt 4: Verweisende offene Tasks → tracker-001/002 verweisen auf 7.x
           → keine Scope-Änderung für diese, aber sie werden später von 7.6
             abhängig sein → Dependency setzen.

  Danach ask_user_input_v0: "Siblings sind jetzt konsistent. Direkt mit 7.6
  weitermachen oder die ursprünglich geplante Reihenfolge 7.2 → 7.3 einhalten?"
```
