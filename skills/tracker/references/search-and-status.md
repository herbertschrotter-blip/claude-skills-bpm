# tracker status / next / suche / listen

Lese-Operationen auf den ClickUp-Tracker.

---

## Kommando `tracker status`

1. `clickup_filter_tasks(space_ids, statuses: ["open", "in progress"])`
2. Gruppiert nach Liste. Beispiel (BPM-Projekt):
```
**PlanManager** (6 offen)
- [high] [v1] [M] BPM-001 | PM | DB-Anbindung Orchestrator
  └─ (3 Unteraufgaben, 1 erledigt)
- [normal] [v1] [L] BPM-002 | PM | 5998er Statikplaene
```

Modul-Kürzel und Meilenstein-Tags sind projekt-spezifisch — siehe
`projects/<[PROJECT]>/clickup-fields.md`. Anzeige kann Typ und Aufwand als
weitere Kurz-Indikatoren enthalten. Ohne Custom Fields: nur
`[prio] <Status> <Titel>`, gruppiert nach Status statt nach Liste; als
„offen“ zählen alle Status außer `shipped`/`done`/`cancelled`.

---

## Kommando `tracker next`

1. Offene Tasks laden
2. Prio-Sortierung: urgent > high > normal > low. Meilenstein-Tag (z.B. `v1`)
   kann zusätzliche Gewichtung geben (Projekt-Regeln in
   `projects/<[PROJECT]>/clickup-fields.md`).
3. Aufwand berücksichtigen: "heute nur S-Tasks" per User-Wunsch möglich
4. Abhängigkeiten prüfen (blocked_by!)
5. Vorschlag: `"Nächster Schritt: <Task-ID> | <Kürzel> | ..."`
   (ohne Felder: Reihenfolge der Projekt-Nummer, z.B. Bauplan-Reihenfolge;
   `testing`-Tasks zuerst nennen, weil dort die Abnahme des Users fehlt)
6. Per Auswahlfrage: "Diesen Task angehen?" → Ja / Nächsten vorschlagen / Eigener Task-Name

---

## Kommando `tracker suche: <Stichwort>`

Tasks durchsuchen mit Liste/Kürzel/Status/Priority/Tag/Typ/Aufwand.

---

## Kommando `tracker listen`

Alle Listen im Space mit Task-Anzahl.
