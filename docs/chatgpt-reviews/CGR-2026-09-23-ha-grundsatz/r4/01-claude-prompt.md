# Review Runde 4 – Nachtrag: Regel G-21 „Ausfall“

Canvas-Titel: **„Review Runde 4“**. Schreibe deine gesamte Antwort in den Canvas und schließe mit
✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen.

Kurze Nachtragsrunde zu genau einer Regel. Alles andere aus Runde 3 ist übernommen.

## Repo-Zugriff
Du hast Zugriff auf zwei GitHub-Repos und kannst selbst Dateien lesen:
- **Skill-Repo:** `herbertschrotter-blip/claude-skills-bpm` – **Branch `main`** (Runden 1–3 vollständig unter
  `docs/chatgpt-reviews/CGR-2026-09-23-ha-grundsatz/`; Runde 3: `r3/02-chatgpt-response.md` ist deine Antwort,
  `r3/03-claude-analysis.md` meine Einschätzung, `r3/04-user-decisions.md` Herberts Entscheidungen)
- **Referenzfall:** `herbertschrotter-blip/HA_Dash_DreameX60` – **Branch `main`**
- Nutze das aktiv, um Aussagen zu verifizieren und Originaldateien zu lesen, wenn der Kontext im Prompt nicht reicht.
- Bei JEDEM Dateizugriff den Branch `main` angeben.

## Entschieden nach Runde 3 (Herbert)

- Deine Endfassung ist übernommen: Einstellungsmatrix, G-01 bis G-20, `module.yaml` Schema v1 für `haus` und das
  Roboter-Modul, Action/WebSocket-Regel, `null` erbt / `[]` bewusst leer, `translation_key` als unsere Konvention,
  bevorzugter Bedienort je Einstellung.
- Ergänzt: G-18 nennt ausdrücklich Koordinaten, Gerätekennungen und Personennamen als private Daten. `planer` im Beispiel ist
  nur ein Arbeitsname (Name beim Neubau). Die Doku verwendet deutsche Begriffe mit dem HA-Fachwort in Klammern.
- Deine offenen Punkte aus Abschnitt 11 werden Prüfliste der Bestandsanalyse des Roboter-Neubaus (DX-111).
- Neu seit Runde 3: Claude arbeitet jetzt direkt auf dem Home Assistant (Claude Code als Add-on). Python-Code einer
  Integration wird nach G-16 per HA-Neustart aktiv; den Neustart löst nur Herbert aus. Änderungen werden deshalb gesammelt
  und vor dem Neustart auf dem Pi getestet.

## Die Frage: G-21 „Ausfall“

Das Ausfallverhalten steht in deiner Antwort nur als offener Punkt für den Roboter („Verhalten bei `unavailable`/Robot
offline“, „Verhalten bei fehlenden oder deaktivierten Entities“). Es betrifft aber jedes Modul: `haus` ohne erreichbare
`person.*`, der Planer ohne Roboter oder ohne `haus`, ein Lüftungsmodul ohne Wetterdaten.

Mein Vorschlag:

| Nr. | Regel | Prüfbar durch | ab |
|---|---|---|---|
| **G-21 Ausfall** | Ein Modul erkennt fehlende, deaktivierte oder nicht verfügbare Quellen, trifft dann keine Entscheidung auf veralteten Daten, macht den Grund sichtbar (eigene Entität wird `unavailable` bzw. Zustand mit Grund, bei dauerhaftem Fehler ein Reparatur-Hinweis) und erholt sich ohne Neustart, sobald die Quelle zurück ist. | Test mit abgeschalteter bzw. entfernter Quelle (Replay/Mock): keine Aktion, sichtbarer Grund, Erholung. | 2 |

## Aufgabe

1. Ist G-21 als allgemeine Regel richtig, oder gehört Ausfallverhalten besser in bestehende Regeln (G-07, G-15, G-17)?
2. Formulierung prüfen: Was fehlt, was ist zu streng? Insbesondere:
   - Soll eine eigene Entität bei fehlender Quelle `unavailable` werden oder ihren letzten Wert mit einem Hinweis behalten?
     Nach welcher Regel entscheidet man das je Entität?
   - Wie lange ist eine Quelle „kurz weg“ (keine Reaktion) und ab wann „dauerhaft“ (Reparatur-Hinweis)? Fester Wert,
     Einstellung je Modul oder je Quelle?
   - Was gilt für Befehle, die während des Ausfalls fällig werden (z. B. geplante Reinigung): verwerfen, nachholen,
     melden?
3. Gilt die Regel ab Stufe 2, oder schon für Stufe 0–1 (Pakete, Automationen) in abgeschwächter Form?
4. Wie sieht der Eintrag in `module.yaml` aus (z. B. je Quelle unter `sources` ein Feld für das Ausfallverhalten)?

Kompakt bitte, das ist die letzte offene Regel. Danach schließe ich die Serie ab und schreibe die Grundsatzdoku.
