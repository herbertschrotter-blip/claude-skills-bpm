# tracker update / tracker field — Task ändern

Ablauf für gezielte Task-Änderungen.

---

## Kommando `tracker update: <BPM-NNN> → <Änderung>`

Task aktualisieren (Priority, Meilenstein, Description, Status, Custom Fields).

Bei ambiger Änderung: `ask_user_input_v0` mit Optionen.

---

## Kommando `tracker field: <BPM-NNN> <Feld> <Wert>`

Einzelnes Custom Field gezielt updaten ohne Task sonst anzupacken.

Beispiele:
- `tracker field: BPM-007 Zielversion v0.26.0`
- `tracker field: BPM-016 Aufwand L`
- `tracker field: BPM-079 Komponente SettingsView.xaml`

Bei Dropdown-Feldern (Typ, Aufwand): Option-ID aus `clickup-fields.md` nehmen.
