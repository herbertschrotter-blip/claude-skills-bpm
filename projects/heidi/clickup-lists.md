# Heidi — ClickUp Listen-Mapping

**Source of Truth:** ClickUp-Workspace direkt. Diese Datei ist Doku und Fallback.

---

## Space — Smart Home

**Space-ID:** `1200660000001609`

Drei Listen (kein Ordner, keine Modul-Listen):

| Liste | Listen-ID | Zweck |
|-------|-----------|-------|
| dreame_x60 – Bauplan | `1200660000004100` | Alle Aufgaben des Neubaus der Heidi-Karte (v2): eine Aufgabe je Bauplan-Schritt oder Post-2.0-Wunsch (`DX-NNN`) |
| dreame_x60 – Tickets | `1200660000004800` | Fehler-Tickets (`HT-NNNN`) aus „Fehler melden“ und der Auswertung – eine Aufgabe je Ticket (Entscheidung Herbert 19.09.2026: Bugs fluten die DX-Liste nicht) |
| dreame_x60 - Audit | `1200660000005341` | Punkte aus dem Audit vom 22.09.2026 (`Audit_NNNN`, 0001–0090, Pakete 1–12). Arbeitsliste und Belege im Repo `Dreame_Dash`: `docs/AUDIT.md`, `docs/AUDIT-BERICHT.md` |

**Routing:** `tracker`-Kommandos gehen in die Bauplan-Liste. **Ausnahme:** Aufgaben aus dem Skill `ticket` (Titel beginnt mit `HT-`) gehen in die Liste Tickets – Titel `HT-NNNN | <KÜRZEL> | <Kurztitel>`, die Ticketnummer ist die Aufgabennummer (kein DX-Zähler, `Next` bleibt unverändert), Tag `bug` (Aufgabentyp „Bug“, sobald er im Workspace existiert). Die Custom Fields der Bauplan-Liste gibt es in der Liste Tickets noch nicht: Commit, Version und Anker dort als Kommentar, Quittung `✅ HT-NNNN — <Aktion> — <ClickUp-Link>`. Status-Werte sind gleich (Space-Status).

**Ausnahme Audit:** Aufgaben mit Titel `Audit_NNNN | <KÜRZEL> | <Kurztitel>` liegen in der Liste Audit
(`1200660000005341`). Die Nummer ist vierstellig mit Unterstrich, kein DX-Zähler (`Next` bleibt
unverändert); neue Audit-Punkte nur auf Anweisung von Herbert, dann auch in `docs/AUDIT.md` eintragen.
Kürzel wie unten plus `HA` (HA-Oberfläche/Konfiguration) und `HERBERT` (macht Herbert selbst). Die
Liste hat die Custom Fields der Bauplan-Liste **ohne** „Bauplan-Phase“ (siehe `clickup-fields.md`).
Quittung ohne Anker: `✅ Audit_NNNN — <Aktion> — <ClickUp-Link>`. Status und Übergänge wie beim Bauplan.

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

- `DX-NNN` dreistellig, global über die Liste, nie wiederverwendet. **Nächste freie Nummer: steht im
  Tracker-Profil der CLAUDE.md des Projekt-Repos** (dort führend, nach jedem `tracker neu` +1; Stand 20.09.2026: DX-078).
- Kürzel = Modul aus dem Commit-Profil: `KARTE` (dreame_x60/card), `BACKEND` (ha/: Paket,
  Automationen, Skripte, Prognose, Dashboard-YAML), `DOKU` (docs/, Bauplan-Pflege, Abnahmen),
  `TOOLS` (tools/, setup.ps1).
- Kurztitel beginnt mit der **Bauplan-Nummer** (`4.4 dx-planer …`), bei Wünschen ohne Schritt mit
  `Post-2.0:`; Befunde/Helfer zu einem Schritt tragen dessen Nummer (`0.2 GPS-Koordinaten …`,
  `2.7 [PC] Python …`). `[PC]` = Herbert führt selbst am PC aus.
- **Keine Phasen-Parents mehr (Entscheidung Herbert 20.09.2026):** alle DX-Aufgaben stehen einzeln
  (flach) in der Liste; die Phase steht im Feld **Bauplan-Phase** (siehe `clickup-fields.md`), nach dem
  sich die Liste gruppieren lässt. Die sieben früheren Aufgaben `Phase 0 … Phase 6` sind archiviert
  (nicht gelöscht). `tracker neu` sucht deshalb **keinen Parent**, sondern setzt das Feld.
- Echte Unteraufgaben (falls je nötig): `<NNN>.<SS> — <Kurzbeschreibung>` wie BPM (Beispiele: 048.01–048.04 unter DX-048;
  älter und abweichend benannt: F.2a/b/c unter DX-069).
- **Modul-Sammelaufgaben mitpflegen (Pflicht, Hinweis Herbert 21.09.2026):** je Modul gibt es eine Meta-Aufgabe mit der
  Schrittliste – R = DX-064, A = DX-056, B = DX-057, C = DX-058, D = DX-059, E = DX-060, F = DX-061, G = DX-062. Bei jedem
  `tracker neu` (neue DX-Aufgabe → Zeile ergänzen), `tracker done` (→ „testing“ vermerken) und nach Herberts Abnahme
  (→ abhaken) die Schrittliste der passenden Sammelaufgabe im selben Arbeitsgang aktualisieren (Scope-Check Punkt 4).
- Unteraufgaben herauslösen oder Feld-Optionen ändern kann die ClickUp-Anbindung nicht (kein `parent`
  in `update_task`, `move_task` nur für Hauptaufgaben) – das geht nur in der ClickUp-Oberfläche
  (markieren → Mehr → „In Aufgaben umwandeln“; gestrichene Aufgaben einzeln über ihr Menü „Konvertieren zu“).

Vergeben am 16.09.2026: DX-001 … DX-055 in Bauplan-Reihenfolge (0.1 → 6.5, dann Backend, dann Post-2.0); DX-056 … DX-062 Modul-Aufgaben (Meta, Bauplan Abschnitt 1a).

---

## Chat-Anker

Wie BPM (`[DX-ANCHOR-<task-id>]`), sobald die Felder `Chat-Anker temp/erstellt/erledigt` auf der
Liste existieren (siehe `clickup-fields.md`). Bis dahin Quittung ohne Anker: `✅ DX-NNN — <Aktion> — <Link>`.

---

## Skill-Issues

Keine eigene Skill-Issues-Struktur in diesem Space. Skill-Issues gehen weiterhin in den
Ordner „Skill Issues“ des Spaces „Claude Skills Entwicklung“ (siehe `projects/bpm/clickup-lists.md`).
