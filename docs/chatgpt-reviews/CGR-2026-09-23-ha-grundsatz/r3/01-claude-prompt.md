# Review Runde 3 – Schlussrunde: Listen in der eigenen Oberfläche, Korrekturen, Endfassung

Canvas-Titel: **„Review Runde 3“**. Schreibe deine gesamte Antwort in den Canvas und schließe mit
✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen.

Das ist die **letzte Runde**. Danach schreibe ich die Grundsatzdoku (`docs/ha-grundsatz/`) und den Skill `modul-bauplan`.

## Repo-Zugriff
Du hast Zugriff auf zwei GitHub-Repos und kannst selbst Dateien lesen:
- **Skill-Repo:** `herbertschrotter-blip/claude-skills-bpm` – **Branch `main`** (Runden 1 und 2 vollständig unter
  `docs/chatgpt-reviews/CGR-2026-09-23-ha-grundsatz/`, je Runde Prompt, Antwort, Einschätzung, Entscheidungen)
- **Referenzfall:** `herbertschrotter-blip/HA_Dash_DreameX60` – **Branch `main`**
- Nutze das aktiv, um Aussagen zu verifizieren, Querverweise zu prüfen und Originaldateien zu lesen, wenn der Kontext im
  Prompt nicht reicht.
- Bei JEDEM Dateizugriff den Branch `main` angeben.

## Stand nach Runde 2 – entschieden (Herbert)

1. **Deine Entscheidungsmatrix für Einstellungen** wird Teil von G-09 und feste Entscheidungshilfe im Skill.
2. **Global + nur die Abweichung je Plan** (`wirksam = plan.abweichung[key] ?? global[key]`, beim Anlegen nichts kopieren).
3. **Einstellungen im eigenen Speicher der Integration** (`Store`, direkt nach jeder Änderung geschrieben), **nicht**
   `RestoreEntity` – HA schreibt `core.restore_state` nur alle 15 Minuten und beim Beenden, nach einem Stromausfall wären die
   letzten Änderungen weg. SQLite nur für Fachdaten (Pläne, Läufe, Lernen).
4. **`haus` liefert Fakten und Haus-Schlüsse:** wer ist da, jemand da, Ruhezeit, Arbeitszeit – und zusätzlich die
   **Anwesenheitsprognose** (heute Heidis `presence.py` mit 6 Einstellungen) und die **übliche Rückkehr**. Jedes Geräte-Modul
   wählt selbst, welche Personen für seine Regeln zählen. Das Lernen von Dauer, Fläche und Akku bleibt beim Roboter-Modul.
5. **„Heidi“ ist der Name des Roboters, nicht der Name des Moduls.** Es gibt kein eigenes Planer-Gerät: Die neue Integration
   hängt ihre Entitäten an das Gerät des Roboters (HA-Richtlinie für Helfer vom 18.07.2025, `async_entity_id_to_device`); den
   eigenen Konfigurationseintrag an ein fremdes Gerät hängen funktioniert seit HA 2026.8 nicht mehr.
6. **Eine Integration heißt nach ihrer Aufgabe, nicht nach dem Gerät;** den Gerätenamen liefert HA. Der konkrete Name kommt
   beim Neubau – verwende in Beispielen den Platzhalter **`planer`**.

## Meine Korrekturen zu Runde 2 (nachgeprüft – bitte je Punkt: einverstanden oder nicht, mit Grund)

1. **Neustart nach Code-Änderung ist eine Tatsache, keine Vorsicht.** Das Neuladen eines Eintrags ruft die Einrichtung erneut
   auf – mit dem Python-Code, der schon geladen ist; neuer Code wirkt erst nach einem HA-Neustart (Community-Thread „Reload
   custom integration“: „You can't unless the integration explicitly supports it“; HACS verlangt nach jedem Update einen
   Neustart). Deshalb zwei getrennte Regeln: *Qualität:* der Eintrag lässt sich entladen und neu laden (für Optionen und
   Entfernen). *Einspielen:* Optionen → Eintrag neu laden (mit `OptionsFlowWithReload` automatisch); Python-Code → HA-Neustart;
   Karte → Browser neu laden.
2. **Was die Karte sieht:** `hass.entities` (Anzeige-Register, `config/entity_registry/list_for_display`) enthält `platform`,
   `device_id`, `translation_key`, `entity_category` – aber **keine `unique_id`** (nur in der vollen Liste
   `config/entity_registry/list`). Vorschlag für den Vertrag der Karte: **Integration + Gerät + `translation_key`** (bei
   wiederholten Schlüsseln zusätzlich Bereich oder Raum); `unique_id` bleibt die innere Identität der Integration; der
   `translation_key` wird wie eine Schnittstelle behandelt und nie umbenannt. Oder siehst du einen besseren Weg?
3. **G-01 genauer:** *„Jeder Wert hat genau einen Eigentümer und einen Speicherort; jede Änderung läuft durch die Prüfung des
   Eigentümers.“* – „ein Schreibweg“ passt nicht, weil Dashboard, Automation und Sprache dieselbe Einstellung ändern dürfen.
4. **`module.yaml` führt nur, was dem Modul gehört.** Dein Beispiel hatte `forecast_learning_weeks` mit `owner: haus` in Heidis
   `settings`. Fremdes steht unter `sources`/`depends_on`; ein Drift-Test prüft, dass jeder `owner` die eigene Modul-ID ist.
5. **Darstellung:** Kartenkonfiguration (je Dashboard, nur im Bearbeiten-Modus änderbar) **oder** HA-Benutzerdaten
   (`frontend/set_user_data`, je Benutzer, ohne Admin) – dann schaltet die Karte Dunkelmodus oder Kartendarstellung direkt um.
6. **„Lernen ab“:** Befehl als Aktion mit optionalem Datum (auch rückwirkend); der Zeitpunkt ist ein Fachdatum in der
   Datenbank des Moduls.
7. **Fehlende Regeln:** Frontend findet Entitäten über das Register, baut nie IDs; Entitäten mit `unique_id`,
   `has_entity_name`, `translation_key`; eigene Datenbank mit Schema-Version, Backup-Haken (`async_pre_backup`/
   `async_post_backup`) und Prüfung nach der Kopie; Eintrag lässt sich entladen und neu laden; Name nach der Aufgabe.

## Offene Frage von Herbert: Listen, die die eigene Oberfläche bearbeitet

Herbert will zum Beispiel die Personen, die den Roboter „stören“, im **Einstellungsmenü seiner Karte** auswählen – nicht im
HA-Dialog „Konfigurieren“ unter Geräte & Dienste. Dasselbe gilt für die Abweichung je Plan (eigene Personenauswahl eines Plans)
und später für die Zuordnung Raum ↔ HA-Bereich. HA hat keine Mehrfachauswahl-Entität.

Mein Vorschlag: Solche Listen liegen im Speicher der Integration und werden über eine eigene Aktion oder einen eigenen
WebSocket-Befehl geändert – so machen es Integrationen mit eigener Oberfläche (Alarmo: `store.py` + `websockets.py`). Der
Optionsdialog bleibt für technische Werte, die im Alltag niemand ändert.

Bitte beantworte:
1. Eigene **Aktion** oder eigener **WebSocket-Befehl** – wofür was (in Automationen nutzbar gegenüber nur für die Oberfläche)?
2. Dürfen Optionsdialog **und** Karte denselben Wert ändern, ohne dass zwei Speicherorte entstehen – oder besser nur ein Weg?
3. Wie zeigt die Karte die Auswahl ohne feste Werte (alle `person.*` aus HA, die gewählten von der Integration)?
4. Wo liegt die Personenauswahl eines Plans (im Plan-Objekt, `null` = global übernehmen)?

## Lieferung (Endfassung, kompakt)
1. Kurzurteil zu meinen Korrekturen 1–7.
2. Antwort auf die Listen-Frage (1–4).
3. **Einstellungsmatrix final** – mit der neuen Zeile „Liste/Objekt, das die eigene Oberfläche bearbeitet“.
4. **Grundsatzregeln final:** höchstens 20 Regeln, je Regel ein Satz „Regel“, ein Satz „prüfbar durch“ und „gilt ab Stufe“.
5. **`module.yaml` Schema v1 final:** Beispiel Roboter-Modul (Platzhalter `planer`) und ein kurzes Beispiel `haus`, beide nach
   der Eigentümer-Regel.
6. **Offene Punkte für den Neubau des Roboter-Moduls** (Stichpunkte, z. B. Raum ↔ Bereich, Fähigkeitsliste des Adapters) – als
   Startliste für die Analyse, die danach kommt.

Tabellen und Stichpunkte, Code nur für das Schema.
