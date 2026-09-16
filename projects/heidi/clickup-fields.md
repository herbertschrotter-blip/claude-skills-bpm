# Heidi — ClickUp Custom Fields

**Source of Truth:** ClickUp-Workspace direkt. Diese Datei ist Doku.

Entscheidung Herbert (16.09.2026): **alle 10 Felder wie BPM** (gleiche Namen, gleiche Typen, gleiche
Optionen), damit der tracker-Skill in beiden Projekten identisch läuft.

---

## Custom Fields (Liste `dreame_x60 – Bauplan`, 1200660000004100)

Die ClickUp-API kann keine Felder anlegen – Herbert legt sie in der Oberfläche an (Liste oder Space
„Smart Home“). Danach IDs per `clickup_get_custom_fields(list_id)` auslesen und hier eintragen.

| Feld | ID | Typ | Phase | Inhalt |
|------|----|----|----|--------|
| **Typ** | _(offen)_ | drop_down | neu | Feature/Fix/Refactor/Perf/Docs/Konzept/Meta |
| **Aufwand** | _(offen)_ | drop_down | neu | S (<1h)/M (1-4h)/L (halber Tag)/XL (>1 Tag) |
| **Zielversion** | _(offen)_ | short_text | neu | Kartenversion, z.B. "2.0.0-alpha.30" |
| **Komponente** | _(offen)_ | short_text | neu | Hauptdatei/Modul, z.B. `dx-planer.ts` |
| **Zugehörige Docs** | _(offen)_ | text | neu | z.B. `docs/dreame_x60/BAUPLAN.md Karte 4.4` |
| **Commit ID** | _(offen)_ | short_text | done | 7-char Hash |
| **Commit Text** | _(offen)_ | text | done | Erste Zeile Commit-Message |
| **Erledigt** | _(offen)_ | date | done | YYYY-MM-DD |
| **Chat-Anker temp** | _(offen)_ | short_text | neu | TEMP-ID aus Ausarbeitungsphase |
| **Chat-Anker erstellt** | _(offen)_ | short_text | neu | `[DX-ANCHOR-<task-id>] - erstellt: …` |
| **Chat-Anker erledigt** | _(offen)_ | short_text | done | `[DX-ANCHOR-<task-id>] - erledigt: …` |

Option-IDs für Typ und Aufwand: nach dem Anlegen ergänzen.

**Bis die Felder existieren:** `tracker done` setzt Status + Kommentar (Version, Commit-Hash);
`tracker field` meldet „Feld noch nicht angelegt“.

---

## Titel-Format

Siehe `clickup-lists.md` Abschnitt „Nummernschema“: `DX-<NNN> | <KÜRZEL> | <Kurztitel>`.

---

## Status-Werte pro Listen-Typ

Eine Liste, neun Status (siehe `clickup-lists.md`). Übergänge: `tracker start` → `in development`,
`tracker done` → `testing` (Abnahme auf `shipped` macht Herbert), verworfen → `cancelled`.

---

## Description-Template

Das Skill-Template aus `references/create-task.md` mit Heidi-DoD. Alle 62 Aufgaben der Liste wurden
am 16.09.2026 darauf umgeschrieben.

```markdown
## Problem
<Was fehlt / ist kaputt – gern mit Herberts Wunsch als Zitat und Datum>

## Lösungsansatz
<Ziel-Text der Bauplan-Karte; nummerierte Bausteine bei größeren Schritten>

## Acceptance Criteria
- [ ] <Akzeptanz-Zeilen der Bauplan-Karte, je eine Checkbox>

## Definition of Done
- [ ] Code implementiert, `npm test` grün
- [ ] Bauplan-Statusliste, HANDOFF aktualisiert
- [ ] Commit gemacht
- [ ] Sichtprüfung Herbert

## Abhängigkeiten / Related
Voraussetzung: <Karten> · Bauplan Abschnitt 8, Karte <n> · <verwandte Aufgaben>

## Technische Notizen
**Nicht ändern:** … · **Tests:** … · **Dateien:** … · Gebaut (Version, Stolpersteine)
```

Regeln:
- Phasen-Aufgaben (Parent „Phase N – …“) nur Problem + Lösungsansatz + Abhängigkeiten (Meta-Kurzform).
- Aufgaben mit `[PC]` im Titel: DoD „Herbert führt aus“ + „Ergebnis im Bauplan vermerkt“.
- Checkboxen nach Status: shipped alle [x]; testing alles [x] außer Sichtprüfung; backlog alle [ ].
- Was gebaut wurde, kommt als **Gebaut (Version …)** in die Technischen Notizen.

Beim Abschluss zusätzlich ein Kommentar:

```
Gebaut (Version <x>, Commit <hash>): <was>. Sichtprüfung Herbert: <was er prüfen soll>.
```

---

## Priorität

ClickUp-Standard (`urgent`/`high`/`normal`/`low`); Bauplan-Schritte `normal`, Blocker `high`, Post-2.0 `low`.
