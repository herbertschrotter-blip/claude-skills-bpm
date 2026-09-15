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

Beim Anlegen einer Aufgabe (Muster aus dem Bauplan, Abschnitt 8):

```
<Bauplan-Nummer> <Titel>
Ziel: …
Akzeptanz: …
Tests: …
Dateien: …
Bauplan: docs/dreame_x60/BAUPLAN.md Abschnitt <n>
```

Beim Abschluss ein Kommentar:

```
Gebaut (Version <x>, Commit <hash>): <was>. Sichtprüfung Herbert: <was er prüfen soll>.
```

---

## Priorität

ClickUp-Standard (`urgent`/`high`/`normal`/`low`); Bauplan-Schritte `normal`, Blocker `high`.
