# Heidi — ClickUp Custom Fields

**Source of Truth:** ClickUp-Workspace direkt (geprüft 16.09.2026: Liste und Space ohne Custom Fields).

---

## Custom Fields

**Keine.** Weder auf der Liste `dreame_x60 – Bauplan` noch im Space „Smart Home“.

Folgen für den Skill:

- `tracker neu`: nur Titel, Beschreibung (Markdown), Status, Priorität. Keine Feld-Aufrufe.
- `tracker done`: Status auf `testing`, Kommentar mit Version und Commit-Hash statt Felder
  „Commit ID“/„Commit Text“/„Erledigt“.
- `tracker field`: in diesem Projekt nicht verfügbar → Hinweis statt Fehler.
- Chat-Anker-Felder: nicht vorhanden → Quittung ohne Anker (siehe `clickup-lists.md`).

---

## Was stattdessen in die Beschreibung gehört

Entscheidung Herbert (16.09.2026): das **Skill-Template** aus `references/create-task.md`,
mit Heidi-DoD. Alle 62 Aufgaben der Liste wurden am 16.09. auf dieses Muster umgeschrieben.

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
Voraussetzung: <Karten> · Bauplan Abschnitt 8, Karte <n> · <verwandte Post-2.0-Aufgaben>

## Technische Notizen
**Nicht ändern:** … · **Tests:** … · **Dateien:** … · Gebaut (Version, Stolpersteine)
```

Regeln:
- Phasen-Aufgaben (Parent „Phase N – …“) nur Problem + Lösungsansatz + Abhängigkeiten (Meta-Kurzform).
- Aufgaben mit `[PC]` im Titel: DoD „Herbert führt aus“ + „Ergebnis im Bauplan vermerkt“.
- Checkboxen nach Status: shipped alle [x]; testing alles [x] außer Sichtprüfung; backlog alle [ ].
- Was gebaut wurde, kommt als **Gebaut (Version …)** in die Technischen Notizen, nicht in ein neues Kapitel.

Beim Abschluss ein Kommentar:

```
Gebaut (Version <x>, Commit <hash>): <was>. Sichtprüfung Herbert: <was er prüfen soll>.
```

---

## Priorität

ClickUp-Standard (`urgent`/`high`/`normal`/`low`); Bauplan-Schritte `normal`, Blocker `high`.
