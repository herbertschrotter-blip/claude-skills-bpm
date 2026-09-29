# CGR-2026-09-23-ha-grundsatz — Grundsatzregeln für Home-Assistant-Projekte und Skill „modul-bauplan“

**Thema:** `ha-grundsatz` – Grundsatzregeln (Doku `docs/ha-grundsatz/`) und der Skill `modul-bauplan`, der vom Konzept bis zum
fertigen Dashboard führt; Referenzfall Heidi (`herbertschrotter-blip/HA_Dash_DreameX60`), die danach neu gebaut wird
**Zeitraum:** 2026-09-23 bis 2026-09-29
**Branch:** `main` (beide Repos)
**Status:** Abgeschlossen (29.09.2026)

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
- **Kernergebnis:** Endfassung übernommen: Einstellungsmatrix, Grundsatzregeln G-01 … G-20, `module.yaml` Schema v1 für
  `haus` und das Roboter-Modul; „ein fachlicher Eigentümer je Wert“ ersetzt „eine Quelle je Wert“; eine Schnittstelle ist
  kein Speicherort; automatisierbarer Befehl → Aktion, Bearbeiten in der eigenen Oberfläche → WebSocket, beides beim selben
  Eigentümer; `null` erbt, `[]` ist bewusst leer; `translation_key` als unsere Konvention. Die 24 offenen Punkte zum
  Roboter werden Prüfliste in DX-111. Offen: Regel G-21 „Ausfall“ → Runde 4.

### Runde 4 — Nachtrag: Regel G-21 „Ausfall“
- **Artefakte:** [r4/](./r4/)
- **Fokus:** Ausfallverhalten als allgemeine Regel: fehlende oder nicht verfügbare Quellen, sichtbarer Grund, Erholung,
  fällige Befehle während des Ausfalls, Eintrag in `module.yaml`
- **Kernergebnis:** G-21 als eigene Regel (ab Stufe 1, vollständig ab 2): ausgefallene oder zu alte Quellen nie
  stillschweigend als aktuell verwenden; je Entität nach Bedeutung (`unavailable` / `unknown` / Vergangenheitswert bleibt /
  `blocked` mit Grund); keine globale Ausfallzeit, `max_age` nur je Quelle; Reparatur-Hinweis nur bei benutzerlösbaren
  Fehlern; Aufträge mit `drop` / `defer` / `retry` / `fail`, Pläne `defer` mit Neubewertung; in `module.yaml` `outage` je
  Quelle und `failure_policy` je Modul.

---

## Ergebnis der Serie

- **Grundsatzregeln G-01 … G-21** (Endfassung: Runde 3 Abschnitt 7, G-18 ergänzt um Koordinaten, Gerätekennungen und
  Personennamen; G-21 aus Runde 4 Abschnitt 10), **Einstellungsmatrix** (Runde 3 Abschnitt 6), **`module.yaml` Schema v1**
  (Runde 3 Abschnitte 8–9, Ausfallverhalten aus Runde 4 Abschnitt 7 mit den Anmerkungen aus `r4/03`), **Ablauf „Planen“**
  (Runde 3 Abschnitt 10), kurzer und voller Weg (Runde 2).
- **Leitsätze:** ein fachlicher Eigentümer je Wert; eine Schnittstelle ist kein Speicherort; nichts Veraltetes als aktuell
  ausgeben.
- **Ergebnis-Ort:** `docs/ha-grundsatz/` (Grundsatzdoku, nächster Schritt) und `skills/modul-bauplan/` (Skill).
- **Im Referenzfall:** Entscheidungen E-137 bis E-141 im Heidi-Repo (`docs/ENTSCHEIDUNGEN.md`); die offenen Punkte zum
  Roboter-Neubau (Runde 3 Abschnitt 11) sind Prüfliste der Bestandsanalyse DX-111.
