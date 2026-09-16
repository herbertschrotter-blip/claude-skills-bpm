# Heidi — ClickUp Listen-Mapping

**Source of Truth:** ClickUp-Workspace direkt. Diese Datei ist Doku und Fallback.

---

## Space — Smart Home

**Space-ID:** `1200660000001609`

Eine Liste (kein Ordner, keine Modul-Listen):

| Liste | Listen-ID | Zweck |
|-------|-----------|-------|
| dreame_x60 – Bauplan | `1200660000004100` | Alle Aufgaben des Neubaus der Heidi-Karte (v2): eine Aufgabe je Bauplan-Schritt oder Post-2.0-Wunsch |

**Routing:** Jedes `tracker`-Kommando in diesem Projekt geht in diese eine Liste. Kein Modul-Routing.

---

## Status-Werte (exakt so, klein geschrieben)

| Status | Typ | Bedeutung im Projekt |
|--------|-----|----------------------|
| `backlog` | open | Post-2.0-Wünsche und Ideen (noch nicht eingeplant) |
| `scoping` | custom | Analyse läuft, noch nichts gebaut |
| `in design` | custom | Mockup/Plan in Arbeit |
| `ready for development` | custom | Bauplan-Karte fertig, Bau kann starten |
| `in development` | custom | Claude Code baut |
| `in review` | custom | Tests grün, Doku offen |
| `testing` | custom | eingespielt, **Sichtprüfung Herbert offen** |
| `shipped` | done | Herbert hat abgenommen |
| `cancelled` | closed | verworfen |

**Übergänge, die der Skill kennt:** `tracker start` → `in development`; `tracker done` → `testing`
(nicht `shipped` – die Abnahme macht Herbert selbst); `tracker abgenommen` (nur Herbert) → `shipped`.

---

## Nummernschema (Entscheidung Herbert, 16.09.2026)

Skill-Schema wie BPM, Präfix **DX**:

```
DX-<NNN> | <KÜRZEL> | <Kurztitel>
```

- `DX-NNN` dreistellig, global über die Liste, nie wiederverwendet. **Nächste freie Nummer: DX-056**
  (steht auch im Tracker-Profil der CLAUDE.md des Projekt-Repos; nach jedem `tracker neu` dort +1).
- Kürzel = Modul aus dem Commit-Profil: `KARTE` (dreame_x60/card), `BACKEND` (ha/: Paket,
  Automationen, Skripte, Prognose, Dashboard-YAML), `DOKU` (docs/, Bauplan-Pflege, Abnahmen),
  `TOOLS` (tools/, setup.ps1).
- Kurztitel beginnt mit der **Bauplan-Nummer** (`4.4 dx-planer …`), bei Wünschen ohne Schritt mit
  `Post-2.0:`; Befunde/Helfer zu einem Schritt tragen dessen Nummer (`0.2 GPS-Koordinaten …`,
  `2.7 [PC] Python …`). `[PC]` = Herbert führt selbst am PC aus.
- **Phasen** (`Phase N – …`) sind Parents ohne DX-Nummer und ohne Felder (Meta-Kurzform).
  Die Bauplan-Schritte sind Hauptaufgaben mit DX-Nummer, auch wenn sie unter einer Phase hängen.
- Echte Unteraufgaben (falls je nötig): `<NNN>.<SS> — <Kurzbeschreibung>` wie BPM.

Vergeben am 16.09.2026: DX-001 … DX-055 in Bauplan-Reihenfolge (0.1 → 6.5, dann Backend, dann Post-2.0).

---

## Chat-Anker

Wie BPM (`[DX-ANCHOR-<task-id>]`), sobald die Felder `Chat-Anker temp/erstellt/erledigt` auf der
Liste existieren (siehe `clickup-fields.md`). Bis dahin Quittung ohne Anker: `✅ DX-NNN — <Aktion> — <Link>`.

---

## Skill-Issues

Keine eigene Skill-Issues-Struktur in diesem Space. Skill-Issues gehen weiterhin in den
Ordner „Skill Issues“ des Spaces „Claude Skills Entwicklung“ (siehe `projects/bpm/clickup-lists.md`).
