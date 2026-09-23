# CGR-2026-09-23-ha-grundsatz — Grundsatzregeln für Home-Assistant-Projekte und Skill „modul-bauplan“

**Thema:** `ha-grundsatz` – Grundsatzregeln (Doku `docs/ha-grundsatz/`) und der Skill `modul-bauplan`, der vom Konzept bis zum
fertigen Dashboard führt; Referenzfall Heidi (`herbertschrotter-blip/HA_Dash_DreameX60`), die danach neu gebaut wird
**Zeitraum:** 2026-09-23
**Branch:** `main` (beide Repos)
**Status:** Runde 3 offen (Schlussrunde)

---

## Runden-Übersicht

### Runde 1 — Deep Research: Praxis, Bewertung Heidi, Kritik am Konzept
- **Artefakte:** [r1/](./r1/)
- **Fokus:** Recherche zur gängigen und bewährten Praxis (offiziell und Community), Bewertung des Referenzfalls Heidi,
  Kritik an Schichten, Regeln, Ausbaustufen, Haus-Modul und Adapter, Antworten auf die offenen Grundsatzfragen, Vorschlag für
  Grundsatzregeln und Skill-Ablauf
- **Kernergebnis:** Eigenes Modul mit Logik ab Stufe 2 = eigene Integration, Heidi wird direkt als `custom_components/heidi`
  neu gebaut (nur über die Dreame-Integration); native HA-Fähigkeit vor Adapter (Dreame-Adapter bleibt, weil `clean_area`
  fehlt); Haus-Modul `haus` als eigenes Repo und eigene Integration (nur „Haus-Schluss“); Module sprechen nur über öffentliche
  HA-Schnittstellen; `module.yaml` Pflicht ab Stufe 2; kurzer Weg für Stufe 0–1. Offen: das Einstellungsmodell
  („ein Eigentümer je Datum“) → Runde 2.

### Runde 2 — Einstellungsmodell konkret, Grundsatzregeln Version 2, kurzer und voller Weg
- **Artefakte:** [r2/](./r2/)
- **Fokus:** Heidis Einstellungen durchgespielt (Ort je Einstellung, eigene Automatik je Plan, Speichern und Prüfen,
  Nachteile, Einstellungen des Haus-Moduls); Grundsatzregeln G-01 … G-16 in Version 2; kurzer Weg (Stufe 0–1) und voller Weg
  (ab Stufe 2); Vorlage Modul-Steckbrief und `module.yaml` Schema v1
- **Kernergebnis:** Entscheidungsmatrix für Einstellungen (Einrichtung, Optionsdialog, Einstellungs-Entität, Fachobjekt,
  Darstellung, Befehl, fremdes Modul); global + nur die Abweichung je Plan; Einstellungen im Speicher der Integration statt
  `RestoreEntity`, SQLite nur für Fachdaten; `haus` liefert Fakten samt Anwesenheitsprognose und üblicher Rückkehr, jedes Gerät
  wählt seine Personen; „Heidi“ ist der Roboter – kein eigenes Planer-Gerät, die Entitäten hängen am Roboter-Gerät; eine
  Integration heißt nach ihrer Aufgabe (Name beim Neubau). Offen: Listen, die die eigene Oberfläche bearbeitet → Runde 3.

### Runde 3 — Schlussrunde: Listen in der eigenen Oberfläche, Korrekturen, Endfassung
- **Artefakte:** [r3/](./r3/)
- **Fokus:** Listen wie die Personenauswahl im Einstellungsmenü der Karte (Aktion oder WebSocket, ein Speicherort); sieben
  Korrekturen von Claude (Neustart nach Code-Änderung, Vertrag der Karte ohne `unique_id`, G-01, Eigentümer-Regel in
  `module.yaml`, Darstellung je Benutzer, „Lernen ab“, fehlende Regeln); Endfassung von Matrix, Regeln und `module.yaml`
- **Kernergebnis:** –
