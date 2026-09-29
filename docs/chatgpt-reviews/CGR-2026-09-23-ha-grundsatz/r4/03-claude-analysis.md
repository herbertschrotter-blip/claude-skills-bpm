# Runde 4 – Einschätzung von Claude

Stand: 29.09.2026, Claude Code auf dem Home Assistant.

## Kurzfassung

ChatGPT nimmt G-21 als eigene Regel auf und schärft meinen Vorschlag an der richtigen Stelle: Nicht „bei Ausfall keine
Entscheidung“, sondern „ausgefallene oder zu alte Quellen nicht stillschweigend als aktuell verwenden“. Ein ausdrückliches
„blockiert, Grund: Roboter nicht verfügbar“ ist selbst eine gültige Entscheidung. Keine Rückfragen, Serie abschließbar. Ich
stimme zu.

## Zustimmung

- **Eigene Regel** statt Teil von G-07/G-15/G-17; die Verweise auf diese drei Regeln kommen in den Erläuterungstext.
- **Gilt ab Stufe 1** in einfacher Form: Eine Automation darf `unavailable` nie als `0` oder `false` deuten. Das ist für
  Herberts Pakete sofort relevant (Beispiel für die Doku: `float(0)`-Umwandlung in Templates).
- **Je Entität nach Bedeutung:** aktueller Wert → `unavailable`, einzelner Wert fehlt → `unknown`, Vergangenheitswert
  bleibt, Entscheidungsentität zeigt `blocked` mit Grund.
- **Keine globale Ausfallzeit;** `max_age` nur je Quelle, wo „zu alt“ fachlich zählt.
- **Reparatur-Hinweis nur, wenn Herbert etwas tun kann** – nicht als Offline-Wecker.
- **Aufträge:** `drop` / `defer` / `retry` / `fail`, für Pläne `defer` mit Neubewertung aller Bedingungen nach der
  Rückkehr; manuelle Aktionen schlagen mit verständlichem Fehler fehl.

## Anmerkungen für die Doku

1. **Werte für `on_unavailable` festlegen.** Das Beispiel kennt nur `block`. Für das Schema v1 als feste Liste:
   `block` (Aktion sperren, Grund zeigen), `fallback` (benannte Ersatzregel, im Steckbrief beschrieben), `ignore` (Quelle
   für diese Ergebnisse nicht kritisch). `recovery` bleibt vorerst nur `re_evaluate`.
2. **Beispiel trennen.** Die Wetter-Quelle mit `ventilation_decision` steht im Beispiel des Planers; sie gehört in ein
   eigenes Lüftungs-Beispiel, damit das Planer-Beispiel stimmig bleibt.
3. **`repair: user_actionable_only`** ist die einzige sinnvolle Einstellung und damit eigentlich die Regel selbst. Im
   Schema weglassen und als feste Regel in G-21 schreiben – ein Feld, das immer denselben Wert hat, prüft nichts.
4. **Quellenangaben:** Die Antwort enthält Verweise der ChatGPT-Oberfläche (`:chatgpt-content-reference{…}`), die im Archiv
   stehen bleiben, in der Doku aber durch Links auf die HA-Entwicklerdoku ersetzt werden.

## Vorschlag

Serie abschließen. G-21 in der Endfassung von Abschnitt 10 übernehmen, mit den vier Unterregeln und den Anmerkungen 1–3.
Ergebnis-Ort ist `docs/ha-grundsatz/` – das wird der nächste Schritt (Grundsatzdoku aus den Runden 1–4).
