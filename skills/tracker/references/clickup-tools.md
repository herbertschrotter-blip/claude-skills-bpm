# ClickUp-Tools — Inventar und Lade-Pattern

**Zweck:** Welche ClickUp-Tools tracker-Befehle aufrufen, in welcher Reihenfolge sie geladen werden, und wie man fehlende Tools nachlädt.

Diese Datei adressiert Issue **tracker-010**: ClickUp-Tools sind in Claude.ai deferred-loaded und ohne explizites Inventar wird mit Suchbegriffen geraten.

---

## Lade-Pattern (PFLICHT vor erstem Tool-Call)

ClickUp-Tools sind **deferred** — sie sind zu Sessionbeginn NICHT im Tool-Inventar, sondern müssen über `tool_search` aktiviert werden.

**Regel:** Wenn ein Tool nicht aufrufbar ist (`Tool '...' not found`), `tool_search` mit dem **EXAKTEN Tool-Namen** aufrufen, nicht mit Umschreibung.

```
✅ tool_search("clickup_get_task")          # lädt das Tool
❌ tool_search("clickup task subtasks")     # liefert Müll-Treffer
❌ tool_search("clickup retrieve task")     # liefert Müll-Treffer
```

Nach erfolgreichem `tool_search` ist das Tool für den Rest der Session aufrufbar.

---

## Tool-Inventar (relevant für tracker)

### Schreiben

| Tool | Zweck |
|------|-------|
| `clickup_create_task` | Neue Task anlegen (mit Custom Fields, Status, Parent, Description) |
| `clickup_update_task` | Task-Felder ändern (Status, Custom Fields, Description) |
| `clickup_delete_task` | Task löschen (User-Bestätigung Pflicht) |
| `clickup_move_task` | Task in andere Liste verschieben (ändert Home-Liste) |
| `clickup_add_task_to_list` | Task zu zusätzlicher Liste hinzufügen (Multi-List, Home bleibt) |

### Lesen

| Tool | Zweck |
|------|-------|
| `clickup_get_task` | Einzeltask abrufen, mit `subtasks=true` für Subtask-Details |
| `clickup_search` | Universalsuche (Tasks, Docs, Chat, etc.) mit Filtern (Listen, Status, Datum) |
| `clickup_get_list` | List-Details und List-ID per List-Name auflösen |
| `clickup_get_workspace_hierarchy` | Spaces/Folders/Lists-Übersicht |

### Kommentare

| Tool | Zweck |
|------|-------|
| `clickup_get_task_comments` | Kommentare einer Task lesen (mit Pagination) |
| `clickup_get_threaded_comments` | Threaded Replies zu einem Kommentar |
| `clickup_create_task_comment` | Neuen Kommentar an Task anhängen |

### Tags & Verknüpfungen

| Tool | Zweck |
|------|-------|
| `clickup_add_tag_to_task` / `clickup_remove_tag_from_task` | Tag-Zuordnung |
| `clickup_add_task_link` / `clickup_remove_task_link` | Task-zu-Task-Verknüpfung |
| `clickup_add_task_dependency` / `clickup_remove_task_dependency` | Abhängigkeiten |

### Custom Fields

| Tool | Zweck |
|------|-------|
| `clickup_get_custom_fields` | Custom-Field-Definitionen einer List/Folder/Space abrufen (für Dropdown-Option-IDs) |

### Time Tracking

| Tool | Zweck |
|------|-------|
| `clickup_start_time_tracking` / `clickup_stop_time_tracking` | Timer steuern |
| `clickup_get_current_time_entry` | Laufender Timer |
| `clickup_get_task_time_entries` | Time-Entries einer Task |
| `clickup_add_time_entry` | Manuelle Time-Buchung |
| `clickup_get_task_time_in_status` / `clickup_get_bulk_tasks_time_in_status` | Zeit pro Status |

### Members & Resolution

| Tool | Zweck |
|------|-------|
| `clickup_resolve_assignees` | Names/Emails/"me" → numerische User-IDs |
| `clickup_find_member_by_name` | Workspace-Member per Name finden |
| `clickup_get_workspace_members` | Alle Members |

### Reminders

| Tool | Zweck |
|------|-------|
| `clickup_create_reminder` / `clickup_update_reminder` / `clickup_search_reminders` | Persönliche Reminders |

### Documents

| Tool | Zweck |
|------|-------|
| `clickup_create_document` / `clickup_create_document_page` / `clickup_update_document_page` | Docs anlegen/ändern |
| `clickup_get_document_pages` / `clickup_list_document_pages` | Doc-Pages lesen |

---

## Befehl → Tool-Mapping

| tracker-Befehl | Primäre Tools | Hinweis |
|---|---|---|
| `tracker neu` | `clickup_create_task` + `clickup_update_task` (für Anker-Felder) | Custom-Field-IDs aus `clickup-fields.md` |
| `tracker update` | `clickup_update_task` | Pro Task-Quittung im Chat (Anker-System) |
| `tracker done` | `clickup_update_task` (Status `done` + Erledigt + Commit ID + Commit Text + Anker erledigt) | DC liest Commit-Hash, dann Update |
| `tracker status` | `clickup_get_task` mit `subtasks=true` | Für Roadmap-Abgleich Repo↔ClickUp |
| `tracker suche` | `clickup_search` mit Filtern | `location.subcategories` = List-IDs, `task_statuses` = `["unstarted"\|"active"\|"done"\|"closed"\|"archived"]` |
| `tracker next` | `clickup_search` mit Sort `created_at desc`, count=1 | Letzten erstellten Task in Liste finden für Auto-Nummerierung |
| `tracker split` | `clickup_create_task` (Subtasks mit Parent) + ggf. `clickup_update_task` | Pro Subtask Anker setzen |
| `tracker relate` | `clickup_add_task_link` | Beidseitige Verknüpfung |
| `tracker field` | `clickup_get_custom_fields` (Schema lesen) + `clickup_update_task` (Wert setzen) | Bei unbekannten Field-IDs zuerst Schema holen |

---

## Häufige Workspace-IDs (BPM-Kontext)

Workspace: `90152410319`

### BPM Entwicklung Space (`901510792907`)

Alle BPM-Listen siehe `projects/bpm/clickup-lists.md` (laufend gepflegt). Beispiele: PM, DOC, KON, SET, etc.

### Claude Skills Entwicklung Space (`901510833068`)

- ClaudeSkills (Roadmap, P0-P4): `901522935159`
- Skill-Issues Folder: `901515724728`
  - tracker: `901522952249`
  - cc-steuerung, skill-pflege, skill-neu, code-erstellen, doc-pflege, audit, mockup-erstellen, chat-wechsel, chatgpt-review, git-commit-helper (je eigene Liste)

---

## Custom-Field-Schema

Siehe **`clickup-fields.md`** (separat) für die UUIDs der Custom Fields:

- Typ, Aufwand, Zielversion, Komponente
- Commit ID, Commit Text, Erledigt
- Chat-Anker erstellt, Chat-Anker erledigt, Chat-Anker temp
- Issue-ID (Skill-Issue-Listen)

Bei Dropdown-Feldern (Typ, Aufwand) werden NICHT die Display-Namen ("Feature", "S (<1h)") gesetzt, sondern die Option-UUIDs. Diese stehen in `clickup-fields.md`.

---

## Anti-Patterns

- ❌ `tool_search` mit Umschreibung wenn der Tool-Name bekannt ist — bringt Müll-Treffer
- ❌ Custom-Field-Wert als Display-Name setzen ("Feature" statt UUID) — wird abgelehnt
- ❌ Tasks anlegen ohne `tracker next` zu prüfen — führt zu Doppel-Nummerierung in Skill-Issue-Listen
- ❌ Massen-Updates ohne Pro-Task-Quittung im Chat (siehe `anker-system.md`)
- ❌ `clickup_delete_task` ohne explizite User-Bestätigung — Daten verloren

---

## Recovery bei "Tool not found"

```
1. Tool-Name notieren (z.B. "clickup_get_task")
2. tool_search("clickup_get_task")  # exakter Name!
3. Tool-Aufruf wiederholen
4. Falls weiter "not found": MCP-Verbindung im Connector prüfen (User informieren)
```

Connector-Status prüft der User in Claude.ai unter `Verzeichnis → Konnektoren → ClickUp`.
