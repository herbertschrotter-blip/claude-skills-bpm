# BSM — ClickUp Listen-Mapping

**Source of Truth:** ClickUp-Workspace direkt. Diese Datei ist Doku und Fallback.

## Space — Smart Home

**Space-ID:** `1200660000001609`

| Liste | Listen-ID | Zweck |
|-------|-----------|-------|
| BSM Baustrommanager | `1200660000007163` | Alle Aufgaben des Fahrplans (`docs/fahrplan.md`): Datenbank, Notprogramm, Schwachstellen aus der Bewertung, Betrieb in der Firma (`BSM-NNN`) |

**Routing:** alle `tracker`-Kommandos dieses Projekts gehen in diese Liste. Melden-Tickets (`FE-/WU-/AN-NNNN`) nicht
(Skill `ticket`).

## Status-Werte (exakt so, klein geschrieben – Space-Status wie Heidi)

| Status | Typ | Bedeutung im Projekt |
|--------|-----|----------------------|
| `backlog` | open | eingeplant im Fahrplan, noch nicht begonnen |
| `scoping` | custom | Analyse/Bauplan läuft |
| `in design` | custom | Mockup in Arbeit |
| `ready for development` | custom | Plan fertig, Bau kann starten |
| `in development` | custom | Claude Code baut |
| `in review` | custom | Tests grün, Doku offen |
| `testing` | custom | eingespielt, **Prüfung durch Herbert offen** |
| `shipped` | done | Herbert hat abgenommen |
| `cancelled` | closed | verworfen |

**Übergänge:** `tracker start` → `in development`; `tracker done` → `testing` (nicht `shipped` – abnehmen macht
Herbert); `tracker abgenommen` (nur Herbert) → `shipped`.

## Nummernschema (Entscheidung Herbert, 05.10.2026)

```
BSM-<NNN> | <KÜRZEL> | <Schritt> <Kurztitel>
```

- `BSM-NNN` dreistellig, global über die Liste, nie wiederverwendet. **Nächste freie Nummer: im Tracker-Profil der
  CLAUDE.md des Projekt-Repos** (dort führend, nach jedem `tracker neu` +1; Stand 05.10.2026: BSM-030).
- `<Schritt>` = Nummer im Fahrplan (`A1` … `H4`); neue Aufgaben bekommen einen Schritt im Fahrplan (dort eintragen).
- Kürzel: `DB` (eigene Datenbank, db/, Datenbank-Phasen), `NOTPROG` (Notprogramm in den Shellys), `SHELLY` (Geräte,
  Hardware, Firmware, Router), `SEITE` (frontend, Mockups), `KERN` (Integration: steuerung, funktionen, logik),
  `DOKU` (docs, README, Präsentation), `BETRIEB` (Firma, Datenschutz, Stabilisieren, Einarbeitung).
- **Etappe als Tag** (Entscheidung Herbert 05.10.2026): `etappe-a` … `etappe-h`, Gruppieren in ClickUp nach Tag. Das
  Feld „Bauplan-Phase“ (Heidi-Optionen) bleibt leer.
- Keine Parents; alle BSM-Aufgaben flach. Vergeben am 05.10.2026: BSM-001 … BSM-029 in Fahrplan-Reihenfolge.

## Chat-Anker

Wie BPM/Heidi: `[BSM-ANCHOR-<task-id>]`, Felder `Chat-Anker temp/erstellt/erledigt` sind auf der Liste vorhanden.

## Skill-Issues

Keine eigene Struktur; Skill-Issues gehen in den Ordner „Skill Issues“ des Spaces „Claude Skills Entwicklung“ (siehe
`projects/bpm/clickup-lists.md`).
