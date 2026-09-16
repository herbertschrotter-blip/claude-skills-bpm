# tracker update / tracker field — Task ändern

Ablauf für gezielte Task-Änderungen.

---

## Kommando `tracker update: <Task-ID> → <Änderung>`

Task aktualisieren (Priority, Meilenstein, Description, Status, Custom Fields).
Task-ID im Format `<PRÄFIX>-NNN` des Projekts (z.B. `BPM-NNN`, `DX-NNN`) oder Issue-ID (`tracker-NNN`).

Bei ambiger Änderung: Auswahlfrage mit Optionen.

---

## Kommando `tracker field: <Task-ID> <Feld> <Wert>`

Einzelnes Custom Field gezielt updaten ohne Task sonst anzupacken.

Beispiele (BPM-Projekt):
- `tracker field: BPM-007 Zielversion v0.26.0`
- `tracker field: BPM-016 Aufwand L`
- `tracker field: BPM-079 Komponente SettingsView.xaml`

Bei Dropdown-Feldern (Typ, Aufwand, etc.): Option-ID aus
`projects/<[PROJECT]>/clickup-fields.md` nehmen — nie raten.
