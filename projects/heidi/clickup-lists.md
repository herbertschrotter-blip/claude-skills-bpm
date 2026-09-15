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

## Nummernschema

Kein BPM-Zähler. Aufgaben tragen die **Bauplan-Nummer** am Anfang des Titels
(`4.3e Einrichtungsprüfung …`) oder das Präfix `Post-2.0:` für Wünsche ohne Bauplan-Schritt.
Unteraufgaben ohne eigene Nummer.

---

## Chat-Anker

Nicht verwendet. Keine Anker-Felder, keine `[…-ANCHOR-…]`-Zeilen. Die Quittung nach einer
Task-Operation lautet nur `✅ <Titel> — <Aktion>` mit dem ClickUp-Link.

---

## Skill-Issues

Keine eigene Skill-Issues-Struktur in diesem Space. Skill-Issues gehen weiterhin in den
Ordner „Skill Issues“ des Spaces „Claude Skills Entwicklung“ (siehe `projects/bpm/clickup-lists.md`).
