# tracker split / tracker relate — Unteraufgaben + Beziehungen

Ablauf für Task-Aufteilung und Task-Beziehungen.

---

## Unteraufgaben

### Wann Unteraufgaben erstellen?

| Situation | Unteraufgaben? |
|-----------|---------------|
| Task ist in 1 Chat erledigt | Nein |
| Task hat 3+ klar trennbare Schritte | Ja |
| Task läuft über 3+ Chats | Ja |
| Modul-Platzhalter ("Dashboard implementieren") | Ja, wenn Modul gestartet wird |

### Wann KEINE Unteraufgaben?

- Task ist trivial (1-2 Stunden Arbeit)
- Schritte sind nicht klar trennbar
- Nur der Vollständigkeit halber

### Unteraufgaben erstellen

Via `clickup_create_task` mit `parent` Parameter:

```
clickup_create_task(
  list_id: "<gleiche Liste wie Parent>",
  name: "<Parent-NNN>.<Sub-NN> — <Beschreibung>",
  parent: "<Parent-Task-ID>",
  priority: "<von Parent erben oder eigene>",
  custom_fields: [
    {"id": "<Typ-ID>", "value": "<Typ-Option-ID>"},
    // Aufwand/Komponente je nach Bedarf
  ]
)
```

Custom Fields bei Unteraufgaben sind optional, aber Typ + Aufwand werden
empfohlen wenn bekannt.

### Hauptaufgabe automatisch Done?

Wenn alle Unteraufgaben Done → mit `ask_user_input_v0` fragen:
"Alle Unteraufgaben von BPM-XXX erledigt. Hauptaufgabe auch schließen?"
Optionen: Ja / Nein

NICHT automatisch schließen.

---

## Kommando `tracker split: <BPM-NNN>`

Hauptaufgabe in Unteraufgaben aufteilen.

1. Task laden: `clickup_get_task(task_id, subtasks: true)`
2. Claude analysiert den Task und schlägt Unteraufgaben vor
3. Per `ask_user_input_v0` bestätigen lassen:
   - "Diese X Unteraufgaben anlegen?" → Ja / Anders aufteilen / Abbrechen
4. Wenn "Anders aufteilen": weitere `ask_user_input_v0` Fragen zur Struktur
5. **Bestehende Sub-Nummern ermitteln** (Lücken beachten)
6. Pro Unteraufgabe:
   ```
   clickup_create_task(
     parent: "<task_id>",
     name: "<Parent-NNN>.<Sub-NN> — <Beschreibung>",
     markdown_description: "<verkürztes Template>",
     custom_fields: [Typ + ggf. Aufwand]
   )
   ```
7. Hauptaufgabe auf "in progress" setzen

### Beispiel-Workflow: tracker split mit ask_user_input_v0

```
User: tracker split BPM-016

Claude intern:
  1. Task laden, analysieren
  2. Bestehende Sub-Nummern prüfen (z.B. schon 01-05 vergeben → neue ab 06)
  3. Struktur-Vorschlag mit N Unteraufgaben erarbeiten
  4. ask_user_input_v0:
     Frage 1: "5 neue Unteraufgaben anlegen oder anders aufteilen?"
     Optionen: "5 anlegen", "6 (mit Tests)", "3 (kompakt)", "Abbrechen"
  5. Wenn User "5 anlegen" → loslegen
  6. Pro Unteraufgabe: 
     name: "016.<NN> — <Beschreibung>"
     parent: "<task_id>"
     markdown_description: verkürztes Template
  7. Parent auf "in progress" setzen
```

---

## Relationships (ClickUp-Dependencies)

Task-Beziehungen werden über ClickUp's eigene **Dependency-Funktion** gepflegt,
NICHT als Custom Field oder Freitext in der Description.

### Beziehungstypen

| Typ | Bedeutung | In ClickUp |
|-----|-----------|------------|
| **blocks** | Task A muss fertig sein bevor Task B starten kann | "blocking" |
| **is blocked by** | Umkehrung von blocks | "waiting on" |
| **relates to** | Lose inhaltliche Verbindung | "linked task" |
| **duplicates** | A ist Duplikat von B | "duplicate" |

### Einsatz

- BPM-007 `blocks` BPM-XX → BPM-XX kann nicht beginnen
- BPM-079 `is blocked by` BPM-079.01 → Mockup muss vor Umsetzung fertig sein
- BPM-004 `relates to` BPM-005 → Thematisch verwandt
- BPM-050 `duplicates` BPM-048 → BPM-050 zum Schließen

### API-Aufruf

Per `clickup_add_task_dependency`:
```
clickup_add_task_dependency(
  task_id: "<Task A>",
  depends_on: "<Task B>"  // Task A is_blocked_by Task B
  // oder
  dependency_of: "<Task B>"  // Task A blocks Task B
)
```

---

## Kommando `tracker relate: <BPM-A> <Beziehung> <BPM-B>`

Task-Beziehung setzen.

1. Beide Tasks laden via `clickup_search` oder direkte ID
2. Beziehungstyp prüfen:
   - Wenn unklar: `ask_user_input_v0` mit blocks/is blocked by/relates to/duplicates
3. `clickup_add_task_dependency` aufrufen mit korrekter Richtung
4. Bestätigung: "✅ BPM-A blocks BPM-B"

Beispiele:
- `tracker relate: BPM-X blocks BPM-Y`
- `tracker relate: BPM-X relates BPM-Y`

Bei unklarer Richtung: `ask_user_input_v0` mit den 4 Beziehungstypen.
