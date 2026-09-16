# Heidi — ClickUp Custom Fields

**Source of Truth:** ClickUp-Workspace direkt. Diese Datei ist Doku.

Entscheidung Herbert (16.09.2026): **alle 10 Felder wie BPM** (gleiche Namen, gleiche Typen, gleiche
Optionen), damit der tracker-Skill in beiden Projekten identisch läuft.

---

## Custom Fields (Liste `dreame_x60 – Bauplan`, 1200660000004100)

Von Herbert am 16.09.2026 auf der Liste angelegt; IDs per `clickup_get_custom_fields(list_id)` gelesen.
`Aufwand` und `Commit Text` sind dieselben Workspace-Felder wie bei BPM (gleiche IDs).

| Feld | ID | Typ | Phase | Inhalt |
|------|----|----|----|--------|
| **Typ** | `81d3400a-0d7f-4296-88ef-6499ca9c455e` | drop_down | neu | Feature/Fix/Refactor/Perf/Docs/Konzept/Meta |
| **Aufwand** | `ecc194e5-2c67-46a7-b4d1-177ce3512c10` | drop_down | neu | S (<1h)/M (1-4h)/L (halber Tag)/XL (>1 Tag) |
| **Zielversion** | `0d81392b-1508-4748-aa4d-a2245f9de922` | short_text | neu | Kartenversion, z.B. "2.0.0-alpha.30" |
| **Komponente** | `43ba3a26-d744-4021-b199-6ee837b349f6` | short_text | neu | Hauptdatei/Modul, z.B. `dx-planer.ts` |
| **Zugehörige Docs** | `867894a0-1567-4fda-99d1-4180642c8d43` | text | neu | z.B. `docs/dreame_x60/BAUPLAN.md Karte 4.4` |
| **Commit ID** | `fc348167-6b50-4e64-8587-c95e962af846` | short_text | done | 7-char Hash |
| **Commit Text** | `cae9f6cb-e0eb-44aa-81f8-df2e1194111e` | text | done | Erste Zeile Commit-Message |
| **Erledigt** | `5dbb8110-f9be-47f5-ba22-09e6d456ff0c` | date | done | YYYY-MM-DD |
| **Chat-Anker temp** | `a83995c0-dc54-4edc-b295-eed8093cbe3b` | short_text | neu | TEMP-ID aus Ausarbeitungsphase |
| **Chat-Anker erstellt** | `192dfca6-2202-4854-ad16-526d5d17ce22` | short_text | neu | `[DX-ANCHOR-<task-id>] - erstellt: …` |
| **Chat-Anker erledigt** | `77be78d2-5e47-4d8a-bab2-aed601e83c92` | short_text | done | `[DX-ANCHOR-<task-id>] - erledigt: …` |

### Typ-Dropdown (Option-IDs)

| Option | Option-ID |
|--------|-----------|
| Feature | `08492894-c36a-4e56-886f-000a11065661` |
| Fix | `1ad19304-d2da-483e-a3f9-9091014a81d6` |
| Refactor | `a0e0ccb0-9beb-4510-939f-d4eb8b9590b4` |
| Perf | `893c5e32-21b1-476e-b05a-47ab5219c280` |
| Docs | `d5008a6c-7be7-488c-9f3d-1f0959d0133f` |
| Konzept | `a5a4b1a3-37ac-4b6b-9ad5-87a8f0b8e3ed` |
| Meta | `159158db-47e8-4f7a-8964-f26a585592fb` |

### Aufwand-Dropdown (Option-IDs, identisch zu BPM)

| Option | Option-ID |
|--------|-----------|
| S (<1h) | `805fd010-b820-46b1-acaa-8b2e047904e6` |
| M (1-4h) | `0298c9b6-9116-4c9e-bb74-d78a41bfe975` |
| L (halber Tag) | `7646181a-b2ff-4eaa-a61b-0d378c0e91d3` |
| XL (>1 Tag) | `6b7587cc-2031-44c4-8b95-74a2d73c87a7` |

### Feld-Regeln für Heidi

- **Zielversion:** Bauplan-Schritte `2.0.0`, gebaute Schritte die konkrete Kartenversion (z.B. `2.0.0-alpha.28`), Wünsche `Post-2.0`.
- **Komponente:** Hauptdatei relativ zu `dreame_x60/card/` (Karte) bzw. Repo-Pfad (Backend/Doku/Tools).
- **Zugehörige Docs:** `docs/dreame_x60/BAUPLAN.md Abschnitt 8, Karte <n>` plus weitere Docs.
- **Commit ID/Text/Erledigt:** beim Übergang nach `testing` (Heidi-„done“) setzen; Erledigt = Datum des Commits.
- **Chat-Anker:** `[DX-ANCHOR-<task-id>] - erstellt: <kurz>` / `- erledigt: Commit <hash>`. Alle 55 nummerierten Aufgaben wurden am 16.09.2026 befüllt; Phasen bleiben ohne Felder.

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
