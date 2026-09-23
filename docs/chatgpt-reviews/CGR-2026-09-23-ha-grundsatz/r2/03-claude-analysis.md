# Runde 2 – Einschätzung von Claude (23.09.2026)

Starke Runde. Die Entscheidungsmatrix für Einstellungen und die Regel „global + nur die Abweichung je Plan“ lösen genau das
Kernproblem aus `docs/DATEN.md` (sieben Automatikwerte doppelt). Fünf Aussagen habe ich nachgeprüft (Quellen unten); zwei davon
muss ich korrigieren.

## Übernehmen (Einigkeit)

1. **Entscheidungsmatrix für Einstellungen** (Einrichtung → Optionsdialog → Einstellungs-Entität → Fachobjekt → Darstellung →
   Befehl → fremdes Modul). Wird Teil von G-09 und feste Entscheidungshilfe im Skill. „Nicht jede Checkbox wird eine Entität.“
2. **Global + nur die Abweichung je Plan:** `wirksam = plan.abweichung[key] ?? global[key]`; beim Anlegen eines Plans nichts
   kopieren; die Datenbank unterscheidet „übernehmen“ von „eigener Wert“.
3. **Eigener kleiner Einstellungsspeicher je Integration statt `RestoreEntity`.** Nachgeprüft und zusätzlich begründet: HA
   schreibt die `RestoreEntity`-Werte nur **alle 15 Minuten und beim Beenden** nach `core.restore_state`. Nach einem Stromausfall
   wären die letzten Änderungen weg. Ein eigener `Store`, direkt nach jeder Änderung geschrieben, hat das Problem nicht.
4. **Prüfen an zwei Grenzen** (Bereich an der Entität, Prüfung im Rechenmodul) – eine Regel, keine doppelten Daten.
5. **Standard-Aktionen für Standard-Entitäten** (`number.set_value`, `select.select_option`, …); eigene Aktionen nur für echte
   Fachvorgänge (Pläne).
6. **Die Karte kennt keine Werte:** Bereiche und Optionen kommen von der Entität, die Optionen des Geräts übersetzt der Adapter.
7. **Grenze Haus ↔ Gerät:** `haus` liefert Fakten und Haus-Schlüsse, jedes Gerät entscheidet, welche Personen für seine Regel
   zählen und was es tut. Nachgeprüft: Heidis „Prognose“ ist die **Anwesenheitsprognose** (`presence.py`, 6 Einstellungen, rechnet
   auch die übliche Rückkehr). Sie gehört damit zu `haus`; das Lernen von Dauer, Fläche und Akku bleibt bei Heidi.
8. **Steckbrief mit 16 Abschnitten, `module.yaml` v1 klein** – ohne Entitäts-IDs, Personen, Raum-IDs, Modellnamen, Pfade,
   Standardwerte.
9. **Die drei Sperren im vollen Weg** (kein Code ohne Eigentumsregister; Rechenmodul-Tests grün vor der Integration; keine Logik
   doppelt vor der Abnahme).

## Korrekturen und Ergänzungen

1. **Neustart nach Code-Änderung ist eine Tatsache, nicht nur Herberts Vorsicht.** Das Neuladen eines Eintrags ruft die
   Einrichtung erneut auf – mit dem Python-Code, der schon geladen ist. Neuer Code wirkt erst nach einem HA-Neustart (Community:
   „You can't unless the integration explicitly supports it“; HACS verlangt nach jedem Update einen Neustart). ChatGPT vermischt
   zwei Dinge:
   - Qualitätsregel „Eintrag lässt sich entladen und neu laden“ (für geänderte Optionen, Entfernen) → gehört zu G-12/G-15.
   - Einspielen neuer Version → Neustart.
   Vorschlag für die allgemeine Regel: *Optionen ändern → Eintrag neu laden (mit `OptionsFlowWithReload` automatisch);
   Python-Code ändern → HA-Neustart; Karte ändern → Browser neu laden.* Herbert-spezifisch (Profil): „nur, wenn Heidi angedockt ist“.
2. **Was die Karte wirklich sieht:** `hass.entities` (Anzeige-Register) enthält `platform`, `device_id`, `translation_key` und
   `entity_category`, aber **keine `unique_id`**. `unique_id` und `config_entry_id` gibt es nur über die volle Liste
   (`config/entity_registry/list`). Praktischer Vertrag für die Karte: **Integration + Gerät + `translation_key`** (bei
   wiederholten Schlüsseln zusätzlich Raum oder Bereich). `unique_id` bleibt die innere Identität der Integration. Folge: Der
   `translation_key` ist die Rolle, die das Frontend sehen kann, und wird wie eine Schnittstelle behandelt: nie umbenennen.
3. **In der Matrix fehlt eine Art: Listen und Objekte, die die eigene Oberfläche bearbeitet** (Personen einer Regel, Zuordnung
   Raum ↔ Bereich, Abweichungen je Plan). HA hat keine Mehrfachauswahl-Entität. ChatGPTs Vorschlag (Optionsdialog mit
   Personen-Auswahl) ist HA-Praxis, dann lässt sich die Liste aber nur unter *Einstellungen → Geräte & Dienste* ändern – Herbert
   wollte sie ausdrücklich im Einstellungsmenü seiner Karte. Vorschlag: Solche Listen liegen im Speicher des Moduls und werden
   über eine eigene Aktion bzw. einen eigenen WebSocket-Befehl geändert – so machen es Integrationen mit eigener Oberfläche
   (nachgeprüft: Alarmo hat `store.py` und `websockets.py`). Der Optionsdialog bleibt für technische Werte, die im Alltag niemand
   ändert.
4. **G-01 genauer:** „ein Schreibweg“ passt nicht zu Einstellungs-Entitäten, die Dashboard, Automation und Sprache ändern
   können. Besser: *„Jeder Wert hat genau einen Eigentümer und einen Speicherort; jede Änderung läuft durch die Prüfung des
   Eigentümers.“*
5. **`module.yaml`-Beispiel widerspricht sich:** `forecast_learning_weeks` mit `owner: haus` steht in Heidis `settings`. Regel:
   Eine `module.yaml` führt nur, was dem Modul gehört; Fremdes steht unter `sources`/`depends_on`. Prüfbar: Jeder `owner` in der
   eigenen Datei ist die eigene Modul-ID.
6. **Heidi als eigenes Gerät – HA-Richtlinie beachten:** Seit 07/2025 sollen Helfer-Integrationen ihre Entitäten an das Gerät
   der Quelle hängen (`async_entity_id_to_device`). Den eigenen Eintrag an ein fremdes Gerät zu hängen, hört mit 2026.8 auf zu
   funktionieren. Ein eigenes Dienst-Gerät verbietet die Richtlinie nicht. Beides ist also HA-konform. Ich stimme ChatGPT für das
   eigene Gerät zu, weil Heidi mehr ist als ein abgeleiteter Wert (Pläne, Regeln, Lernen) und die Roboterseite sauber bleibt. Nie:
   Heidis Eintrag am Dreame-Gerät.
7. **Anzeige-Einstellungen:** „Card config“ heißt: ändern nur im Bearbeiten-Modus des Dashboards. HA hat dafür auch einen
   Speicher je Benutzer (`frontend/set_user_data`, für jeden Benutzer, ohne Admin). Die Karte kann dort Dunkelmodus oder
   Kartendarstellung direkt umschalten, jeder Benutzer hat seine eigene Wahl. Regel: Darstellung bleibt im Frontend – als
   Kartenkonfiguration (je Dashboard) oder Benutzerdaten (je Benutzer).
8. **„Lernen ab“:** Befehl ist richtig, aber der Zeitpunkt selbst ist ein Fachdatum (das Lernen ignoriert frühere Läufe). Also
   Aktion mit optionalem Datum, damit man auch rückwirkend neu beginnen kann; der Zeitpunkt liegt in Heidis Datenbank.
9. **In der Regelliste fehlen noch:**
   - Frontend findet Entitäten über das Register (Integration + Gerät + `translation_key`), baut nie IDs zusammen.
   - Entitäten tragen `unique_id`, `has_entity_name` und `translation_key` (HA-Qualitätsregeln).
   - Eine eigene Datenbank hat Schema-Version, Backup-Haken (`async_pre_backup`/`async_post_backup`) und Prüfung nach der Kopie.
   - Der Eintrag lässt sich entladen und neu laden.

## Zu ChatGPTs drei Rückfragen (Empfehlung an Herbert)
1. `haus` liefert Fakten, jedes Gerät wählt seine Personen – **ja**; dazu Anwesenheitsprognose, übliche Rückkehr und Arbeitszeit
   nach `haus`.
2. Heidi als eigenes Gerät – **ja** (Dienst-Gerät, Richtlinie aus Punkt 6 beachten).
3. Einstellungsspeicher je Integration, SQLite nur Fachdaten – **ja**; Listen, die die Karte bearbeitet, liegen ebenfalls im
   Speicher der Integration.

## Quellen der Nachprüfung
- [Frontend `entity_registry.ts` (Anzeige-Register ohne `unique_id`)](https://github.com/home-assistant/frontend/blob/dev/src/data/entity/entity_registry.ts)
- [Core `restore_state.py` (`STATE_DUMP_INTERVAL` 15 min, Schreiben beim Beenden)](https://github.com/home-assistant/core/blob/dev/homeassistant/helpers/restore_state.py)
- [Community: Reload custom integration](https://community.home-assistant.io/t/reload-custom-integration/686155)
- [Aktion „Reload config entry“](https://www.home-assistant.io/actions/homeassistant.reload_config_entry/)
- [Entwickler-Blog 18.07.2025: Helfer an das Gerät der Quelle hängen](https://developers.home-assistant.io/blog/2025/07/18/updated-pattern-for-helpers-linking-to-devices/)
- [Core `frontend/storage.py` (`frontend/set_user_data` je Benutzer)](https://github.com/home-assistant/core/blob/dev/homeassistant/components/frontend/storage.py)
- [Alarmo (eigener Speicher und WebSocket-Befehle)](https://github.com/nielsfaber/alarmo/tree/main/custom_components/alarmo)
