# Runde 2 – Entscheidungen von Herbert (23.09.2026)

| Frage | Entscheidung |
|---|---|
| ChatGPTs drei Rückfragen (Haus liefert Fakten und jedes Gerät wählt seine Personen; Heidi als eigenes Gerät; Einstellungsspeicher je Integration, SQLite nur Fachdaten) | **Einzeln durchgehen** – Ergebnis unten |
| Anwesenheitsprognose (`presence.py`, 6 Einstellungen), übliche Rückkehr und Arbeitszeit ins Haus-Modul `haus`? | **Ja, ins Haus-Modul** – Heidi liest sie nur noch; Heidis Lernen (Dauer, Fläche, Akku) bleibt bei Heidi |
| Wo werden Listen eingestellt (z. B. welche Personen für Heidi zählen)? | **ChatGPT fragen** – Runde 3 |

## Die drei Rückfragen einzeln

| Rückfrage | Entscheidung |
|---|---|
| 1. `haus` liefert nur Fakten, jedes Gerät wählt selbst, welche Personen für es zählen | **Ja** |
| 2. Heidi als eigenes Gerät in HA, getrennt vom Roboter | Antwort Herbert: **„Heidi ist der Roboter Dreame X60“** – kein zweites Gerät; Deutung und Name der neuen Integration: siehe unten |
| 3. Einstellungen im Speicher der Heidi-Integration, `heidi.db` nur für Pläne, Läufe, Lernen | **Ja** (ändert E-128 im Heidi-Repo: Einstellungen nicht mehr in der Datenbank) |

## Nachfrage zu 2 (Heidi ist der Roboter)

| Frage | Entscheidung |
|---|---|
| Nur ein Gerät: Einstellungen und Ergebnisse der neuen Integration erscheinen auf der Geräteseite des Roboters (HA-Muster für Helfer seit 07/2025)? | **Ja, alles beim Roboter** |
| Name der neuen Integration (nicht `heidi` – das ist der Name des Roboters, Regel 1 „nichts fest verdrahten“) | **Beim Neubau festlegen**; Grundsatz: eine Integration heißt nach ihrer Aufgabe, der Gerätename kommt aus HA |
