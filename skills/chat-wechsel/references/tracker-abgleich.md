# ClickUp-Integration (vor Übergabeprompt)

Gilt in beiden Umgebungen vor dem Handover-Prompt (`SKILL.md`, Abschnitte „ABLAUF IN CLAUDE CODE“ und „Ablauf im
Cowork-Chat“).

## Schritt 1: Offene Tasks laden

1. Space/Listen-ID und Präfix aus dem **Tracker-Profil** (Claude Code: CLAUDE.md) bzw. dem Memory-Eintrag `[CLICKUP]` (Cowork) lesen
2. `clickup_filter_tasks(list_ids/space_ids: [...], statuses: <offene Status laut projects/<name>/clickup-lists.md>)` – read-only, über den tracker-Skill
3. Tasks gruppieren: mehrere Listen → nach Liste (BPM); eine Liste → nach Status (Heidi: in development, testing, backlog)

## Schritt 2: Chat-Verlauf scannen

Chat scannen auf:
- Tasks die bearbeitet aber nicht als Done markiert wurden
- Neue Probleme die aufgetaucht aber nicht erfasst sind
- NUR nach klaren Mustern: `TODO:`, `offen:`, `neuer punkt:`, `neue aufgabe:`,
  `später:`, klare Problemformulierungen mit Handlungsbezug
- NICHT jede Erwähnung eines Problems als neuen Task interpretieren

## Schritt 3: Batch-Abschluss (Auswahlfrage!)

Strukturierte Übersicht im Chat zeigen:

```
### ClickUp Tracker — Batch-Abschluss

**Im Chat erledigt — als Done markieren?**
- <PRÄFIX>-003 | DB-Anbindung Orchestrator        (Beispiel BPM; Heidi: DX-031 | KARTE | 4.4 dx-planer …)
- <PRÄFIX>-007 | CS8629 Warning behoben
- <PRÄFIX>-012 | Token-Migration

**Im Chat neu erkannt — Task anlegen?**
- PlanManager — <neues Problem aus diesem Chat>
- Docs — <neuer Doc-Punkt>

**Weiterhin offen laut ClickUp:**
PlanManager (4):
- [high] [V1] BPM-004 | 5998er Statikplaene Erkennung
- [normal] [V1] BPM-008 | Mockup ManuellSortieren
...
Docs (1):
- [normal] [V1-Nice] BPM-015 | ADR-050 schreiben
```

Dann **zwei Auswahlfragen** (multiSelect):

**Erster Aufruf — Done-Markierungen:**
```
ask_user_input_v0(
  questions: [{
    question: "Welche Tasks als Done markieren?",
    type: "multi_select",
    options: [
      "BPM-003 | DB-Anbindung Orchestrator",
      "BPM-007 | CS8629 Warning behoben",
      "BPM-012 | Token-Migration",
      "Keine"
    ]
  }]
)
```

**Zweiter Aufruf — Neue Tasks:**
```
ask_user_input_v0(
  questions: [{
    question: "Welche neuen Tasks anlegen?",
    type: "multi_select",
    options: [
      "PlanManager — <neues Problem>",
      "Docs — <neuer Doc-Punkt>",
      "Keine"
    ]
  }]
)
```

## Schritt 4: Nach Bestätigung ausführen

- Done-Tasks: `tracker done` pro ausgewähltem Task (Status laut Übergängen des Projekts – Heidi `testing`, BPM `done`; Commit-Felder bzw. Kommentar)
- Neue Tasks: `tracker neu` pro ausgewähltem Task (Fragemodus per Auswahlfrage im tracker-Skill, Präfix des Projekts)
- Cowork: Memory `[CLICKUP]` Eintrag aktualisieren: `Letzte Sync: Teil <N>`; Claude Code: `Next` im Tracker-Profil, wenn Tasks angelegt wurden

## ClickUp nicht erreichbar?

Per Auswahlfrage:
```
Frage: "ClickUp nicht erreichbar. Wie weiter?"
Optionen: "Trotzdem Prompt erstellen", "Retry", "Abbrechen"
```

Bei "Trotzdem Prompt erstellen": Hinweis in Prompt einfügen, Übergabe aus Chat-Verlauf.
