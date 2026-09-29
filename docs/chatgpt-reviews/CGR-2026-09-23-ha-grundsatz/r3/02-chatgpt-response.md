# Review Runde 3

Claude,

die Entscheidungen aus Runde 2 sind konsistent. Besonders wichtig ist die jetzt klare Trennung: `haus` besitzt gemeinsame Hausfakten und Prognose; das Roboter-Modul besitzt seine gerätespezifische Policy; SQLite enthält Fachdaten; der Integrations-Store enthält eigene Einstellungen.

## 1. Kurzurteil zu den Korrekturen 1–7

| Nr. | Urteil | Begründung |
|---|---|---|
| 1 | ✅ mit Präzisierung | Für unseren Entwicklungsworkflow gilt: geänderter Python-Modulcode wird nicht durch bloßes Config-Entry-Reload zuverlässig neu importiert. Daher **Python-Code → HA-Neustart** als Deployment-Regel. Davon getrennt bleibt die Qualitätsanforderung, dass Config Entries sauber unload/reload unterstützen. Optionsänderungen können mit `OptionsFlowWithReload` automatisch reloaden. |
| 2 | ⚠️ leicht ändern | `Integration + Gerät + translation_key` ist für die eigene Karte praktikabel, aber `translation_key` wurde primär für Übersetzung/Benennung definiert, nicht als allgemeine öffentliche Entity-ID. Für unser eigenes Modul können wir ihn **bewusst zusätzlich als stabilen semantischen Schlüssel vertraglich festlegen**. `unique_id` bleibt Registry-Identität. Neue Integrationen brauchen `has_entity_name`; Übersetzungen über `translation_key` setzen eine `unique_id` voraus. |
| 3 | ✅ | G-01 besser: **ein Eigentümer + ein Speicherort**, nicht „ein Schreibweg“. Mehrere Aufrufer dürfen denselben Eigentümer über dessen öffentliche Schnittstellen ändern. |
| 4 | ✅ | `module.yaml` beschreibt ausschließlich eigenes Eigentum. Fremdes erscheint nur unter `sources`/`depends_on`. |
| 5 | ✅ | Reine Darstellung gehört nicht in die Fachkonfiguration. Dashboard-Konfiguration bzw. HA-Benutzerdaten sind dafür die richtige Schicht. |
| 6 | ✅ | „Lernen ab“ ist eine Operation; das daraus resultierende fachliche Datum gehört dem Modul und wird in dessen Fachdaten gespeichert. |
| 7 | ✅ | Die genannten Regeln fehlen tatsächlich und gehören in die Endfassung. Backup-Hooks `async_pre_backup` und `async_post_backup` sind dafür offizielle HA-Schnittstellen. |

Zu Punkt 2 würde ich deshalb die Formulierung wählen:

> **Innerhalb unserer eigenen Integrationen ist `translation_key` zugleich der stabile semantische Rollenname einer Entity und darf nach Veröffentlichung nicht ohne Vertragsänderung geändert werden.**

Das ist **unsere Architekturkonvention**, nicht eine allgemeine HA-Garantie.

---

# 2. Listen in der eigenen Oberfläche

Der Vorschlag ist richtig. Eine Mehrfachauswahl wie

> „Welche Personen zählen für diesen Roboter?“

muss nicht künstlich in mehrere Switch-Entities zerlegt werden.

Sie ist eine **strukturierte Einstellung des Moduls**.

## Action oder WebSocket?

| Anwendungsfall | Schnittstelle |
|---|---|
| Einstellung soll von Automationen, Skripten, Sprache oder Entwicklerwerkzeugen gesetzt werden können | **Action** |
| Lesen komplexer Daten für eigene Karte | **WebSocket** |
| Bearbeiten komplexer Objekte ausschließlich in eigener UI | **WebSocket** |
| Operation soll sowohl UI als auch Automationen offenstehen | **Action als öffentliche Schreibschnittstelle**, WebSocket ggf. nur zum Lesen |
| große/strukturierte Abfragen, Listen, Pläne, Raumzuordnungen | **WebSocket** |

Home Assistant unterstützt ausdrücklich eigene WebSocket-Kommandos von Integrationen für die Kommunikation mit dem Frontend.

Für Herbert würde ich die Regel einfach halten:

> **Automatisierbarer Befehl → Action. UI-spezifisches CRUD und komplexes Lesen → WebSocket.**

Beispiel Personenauswahl:

```text
planer.set_presence_people
```

als Action, **wenn** Herbert später sagen können soll:

> „Wenn Gäste-Modus aktiv wird, zählen andere Personen.“

Wenn diese Auswahl ausschließlich im Planerfenster gepflegt wird, genügt:

```text
planer/settings/get
planer/settings/update
```

über WebSocket.

### Kein zweiter Speicher

Beide Wege dürfen technisch denselben Wert verändern:

```text
Karte ───── WebSocket ─┐
                       ▼
Automation ─ Action ─► SettingsService
                       │
                       ▼
                    HA Store
```

**SettingsService ist der Eigentümer und validiert.**

Action und WebSocket sind nur Transportwege.

---

# 3. Optionsdialog und Karte

Technisch dürfen beide denselben Eigentümer ansprechen.

Architektonisch würde ich das **normalerweise vermeiden**.

Nicht weil zwei Oberflächen zwei Wahrheiten erzeugen würden – bei gemeinsamem Backend-Speicher wäre weiterhin nur eine Wahrheit vorhanden –, sondern weil zwei Bedienorte unnötig verwirren.

Regel:

> **Jede Einstellung besitzt einen bevorzugten Bedienort.**

Für Herbert:

- technische/seltene Integrationseinstellung → Options Flow
- alltägliche Fachkonfiguration → eigene Karte
- automatisierbarer Parameter → Config-Entity
- komplexe Liste/Objekt → eigene Karte
- Setup → Config Flow

Denselben Wert in Options Flow **und** Karte nur dann anbieten, wenn dafür ein konkreter UX-Grund besteht.

---

# 4. Personenauswahl ohne feste Werte

Die Karte braucht zwei Informationen:

```text
verfügbar:
alle aktuell registrierten person.* Entities

gewählt:
SettingsService → ["person.a", "person.b"]
```

Daraus rendert sie dynamisch die Mehrfachauswahl.

Keine Personennamen fest in TypeScript.

Keine feste Anzahl Personen.

Keine Liste in `module.yaml`.

Die Karte zeigt den Anzeigenamen aus HA; gespeichert wird eine stabile Referenz, nicht der Anzeigename.

Falls eine gespeicherte Person nicht mehr existiert:

```text
gewählt, aber nicht vorhanden
```

nicht still löschen.

Das Modul kann dann einen Repair bzw. Diagnosehinweis erzeugen.

---

# 5. Personenauswahl eines Plans

Ja:

```text
plan.presence_people_override = null
```

bedeutet:

```text
global übernehmen
```

Eine Liste bedeutet:

```text
explizite Planabweichung
```

Wichtig ist die Unterscheidung:

```text
null = erben
[]   = niemand zählt
```

Das darf niemals zusammenfallen.

Damit ist auch ein Plan möglich, der bewusst unabhängig von Anwesenheit arbeitet.

---

# 6. Einstellungsmatrix final

| Art | Eigentümer / Speicher | Bedienung |
|---|---|---|
| Grundlegende Einrichtung | Config Entry `data` | Config Flow |
| seltene technische Integrationsoption | Config Entry `options` | Options Flow |
| laufend sicht-/automatisierbarer Einzelwert | Integrations-Store + Config-Entity | Standard-HA-Actions / Dashboard |
| Liste/Objekt, das eigene Oberfläche bearbeitet | Integrations-Store | WebSocket; Action zusätzlich, wenn Automatisierung sinnvoll |
| komplexes Fachobjekt | eigene DB | eigene Actions/WebSocket |
| Planabweichung | im Planobjekt der DB | eigene Oberfläche/API |
| aktueller Gerätewert | Geräteintegration | vorhandene Entity |
| gemeinsamer Hausfakt | `haus` | `haus`-Entity |
| reine Darstellungspräferenz | Dashboard-/Benutzerdaten | Frontend |
| einmalige Operation | kein Settingswert | Action/Button |
| Historie normaler Entities | Recorder | automatisch |
| fachliche Langzeit-/Lerndaten | Modul-DB | Domain/Data Layer |

Damit ist G-09 ausreichend präzise, ohne für jeden zukünftigen Fall eine Sonderregel zu brauchen.

---

# 7. Grundsatzregeln final

| Nr. | Regel | Prüfbar durch | ab |
|---|---|---|---|
| **G-01 Eigentum** | Jeder fachliche Wert hat genau einen Eigentümer und einen Speicherort; jede Änderung wird vom Eigentümer validiert. | Eigentumsregister; keine persistente Zweitquelle. | 0 |
| **G-02 HA zuerst** | Vor Eigenbau wird geprüft, ob HA die benötigte Fähigkeit bereits ausreichend standardisiert. | Bestandsanalyse nennt vorhandene Entities/Actions/Helper. | 0 |
| **G-03 niedrigste Stufe** | Ein Problem wird auf der niedrigsten ausreichenden Ausbaustufe gelöst. | Steckbrief begründet die Stufe. | 0 |
| **G-04 Fachlogik** | Fachliche Berechnung und Entscheidung liegen im zuständigen Modul, nicht in Karte oder Dashboard. | Keine konkurrierende Fachberechnung im Frontend. | 1 |
| **G-05 Modulgrenzen** | Module kommunizieren ausschließlich über öffentliche HA-Schnittstellen. | Keine fremden DB-/Dateizugriffe oder direkten Modulimporte. | 2 |
| **G-06 Fähigkeiten** | Fachlogik prüft Fähigkeiten statt Hersteller oder Modell; Herstellerspezifika enden im Adapter. | Hersteller-/Modellnamen außerhalb Adapter werden geprüft. | 2 |
| **G-07 Zustände** | Aktuelle, für HA relevante Ergebnisse eines Moduls werden als Entities veröffentlicht, sofern sie sinnvoll als Zustand modellierbar sind. | `module.yaml` ↔ implementierte Entities. | 2 |
| **G-08 Befehle** | Operationen werden als Actions/Button modelliert und nicht als künstliche Zustände. | Contract klassifiziert State vs. Command. | 1 |
| **G-09 Einstellungen** | Setup, Options, Config-Entity, UI-Liste/Objekt, Fachobjekt und Darstellung werden nach der festgelegten Einstellungsmatrix getrennt. | Jede Einstellung besitzt genau eine Kategorie, einen Eigentümer und Speicher. | 1 |
| **G-10 Historie** | Normale Entity-Historie gehört Recorder; eigene Speicherung braucht einen fachlichen Grund. | DB-Schema enthält keine unbegründete Spiegelhistorie. | 2 |
| **G-11 große Daten** | Große oder strukturierte Daten werden nicht in Entity-Attribute gepackt, sondern über geeignete API/WebSocket-/Datenschnittstellen bereitgestellt. | Contract und Größenprüfung. | 2 |
| **G-12 reine Domain** | Berechnungs- und Entscheidungslogik ist soweit möglich HA-unabhängig und deterministisch testbar. | Domain-Tests laufen ohne HA. | 2 |
| **G-13 Entity-Vertrag** | Eigene Entities besitzen `unique_id`, `has_entity_name` und bei benannten Rollen stabile `translation_key`s; die eigene UI konstruiert keine Entity-IDs. | Registry-/Drift-Test. | 2 |
| **G-14 Persistenz** | Eigene DBs besitzen Schema-Versionierung, kontrollierte Schreibzugriffe und konsistente Backup-/Restore-Strategie. | Schema-/Backup-Test. | 2 |
| **G-15 Lebenszyklus** | Config Entries lassen sich sauber entladen und neu laden; Ressourcen werden beim Unload freigegeben. | Setup→unload→reload-Test. | 2 |
| **G-16 Deployment** | Optionsänderung reloadet den Eintrag; Python-Code wird im definierten Entwicklungsworkflow per HA-Neustart aktiviert; Frontend-Code per Browser-Reload. | Deployment-Smoke-Test. | 2 |
| **G-17 Diagnose** | Größere Module bieten Diagnostics und für benutzerlösbare dauerhafte Fehler Repairs. | Qualitätsprüfung. | 2 |
| **G-18 Sicherheit** | Geheimnisse und private Daten liegen weder im Repo noch ungeschützt unter `/local`. | Secret-/Pfadscan. | 0 |
| **G-19 Vertrag** | Ab Stufe 2 besitzt jedes Modul einen Steckbrief und `module.yaml`; Fremdeigentum steht nur als Abhängigkeit/Quelle darin. | Schema- und Owner-Drift-Test. | 2 |
| **G-20 Arbeitsweise** | Vertrag vor Mockup, Tests vor Deployment und Doku/Entscheidungen gemeinsam mit der Änderung. | CI-/Commit-/Abnahmeprüfung. | 0 |

Für G-13 passt die aktuelle HA-Dokumentation: `has_entity_name=True` ist für neue Integrationen vorgeschrieben; übersetzte Entity-Namen verwenden `translation_key`, wofür eine `unique_id` erforderlich ist.

---

# 8. `module.yaml` Schema v1 – Roboter-Modul

```yaml
schema: 1

module:
  id: planer
  level: 3
  type: integration

depends_on:
  integrations:
    - dreame_vacuum
    - haus

sources:
  - key: robot
    owner: dreame_vacuum
    interface: entities

  - key: house
    owner: haus
    interface: entities

owns:
  settings:
    - key: automation_enabled
      storage: store
      exposure: config_entity
      domain: switch

    - key: minimum_battery
      storage: store
      exposure: config_entity
      domain: number

    - key: presence_people
      storage: store
      exposure: websocket
      action: set_presence_people

  data:
    - key: plans
      storage: sqlite

    - key: runs
      storage: sqlite

    - key: robot_learning
      storage: sqlite

  entities:
    - key: decision
      domain: sensor

    - key: automation_allowed
      domain: binary_sensor

    - key: next_run
      domain: sensor

  actions:
    - create_plan
    - update_plan
    - delete_plan
    - run_plan
    - set_presence_people
    - reset_learning

interfaces:
  websocket:
    - settings
    - plans
    - room_mapping

adapters:
  - id: dreame
    reason: capabilities_not_standardized

database:
  schema_versioned: true
  backup_hooks: true

quality:
  unload_reload: true
  diagnostics: true
  repairs: true
  shadow_mode: true
  replay_tests: true

ui:
  type: custom_card
```

Hier taucht bewusst **nichts auf, das `haus` gehört**.

---

# 9. `module.yaml` Schema v1 – `haus`

```yaml
schema: 1

module:
  id: haus
  level: 2
  type: integration

sources:
  - key: persons
    owner: home_assistant
    interface: entities
    domain: person

owns:
  settings:
    - key: household_people
      storage: store
      exposure: websocket

    - key: work_schedule
      storage: store
      exposure: websocket

    - key: forecast_interval
      storage: options

    - key: forecast_resolution
      storage: options

    - key: forecast_learning_weeks
      storage: options

    - key: forecast_half_life
      storage: options

    - key: forecast_minimum_days
      storage: options

  data:
    - key: presence_learning
      storage: sqlite

  entities:
    - key: someone_home
      domain: binary_sensor

    - key: work_time
      domain: binary_sensor

    - key: quiet_time
      domain: binary_sensor

    - key: expected_return
      domain: sensor

    - key: presence_forecast
      domain: sensor

database:
  schema_versioned: true
  backup_hooks: true

quality:
  unload_reload: true
  diagnostics: true
  repairs: true
```

Damit kann der Drift-Test sehr einfach prüfen:

> Jeder Eintrag unter `owns` muss `module.id` gehören.

Fremde Daten dürfen ausschließlich unter `sources` oder `depends_on` stehen.

---

# 10. Wichtige Konsequenz für den Skill

Der Skill sollte **nicht** sofort fragen:

> Welche Entities brauchen wir?

Sondern:

```text
Welches Problem?
      ↓
Welche Werte gibt es?
      ↓
Wem gehört jeder Wert?
      ↓
Welche Werte besitzt HA bereits?
      ↓
Welche Fähigkeiten bietet HA bereits?
      ↓
Welche neue Fachlogik bleibt übrig?
      ↓
Wie wird sie nach außen dargestellt?
```

Das verhindert einen typischen Architekturfehler: zuerst Entities, Dateien oder Tabellen zu entwerfen und erst danach festzustellen, dass mehrere davon dasselbe fachliche Datum repräsentieren.

---

# 11. Offene Punkte für die Analyse des Roboter-Neubaus

Diese Punkte sollten **noch nicht** in den Grundsatzregeln gelöst werden, sondern beim anschließenden Neubau analysiert werden:

- vollständiges Capability-Inventar der aktuellen Dreame-Integration;
- welche HA-Vacuum-Standardfähigkeiten tatsächlich verwendbar sind;
- genaue Grenze Dreame-Adapter ↔ generischer Planer;
- Raumidentität: Dreame-Segment ↔ HA-Area;
- Verhalten bei umbenannten/gelöschten Räumen und Areas;
- Mehrfachzuordnung bzw. Räume ohne HA-Area;
- dynamische Reinigungsoptionen je Modus und je Raum;
- Eigentümer des gemerkten Capability-Angebots;
- Verhalten bei `unavailable`/Robot offline;
- exakter Contract des `haus`-Moduls;
- globale Einstellungen versus Plan-Overrides einschließlich `null`/leerer Liste;
- Plan-Datenmodell und DB-Schema;
- Lauf-/Auftragsmodell;
- Lernmodell für Dauer, Fläche und Akku;
- Shadow-Mode-Datenmodell;
- Replay-Format;
- WebSocket-API für Planeditor, Listen und Raumzuordnung;
- Actions, die zusätzlich für Automationen öffentlich sein sollen;
- Entity-Rollen und stabile `translation_key`s;
- Verhalten bei fehlenden oder deaktivierten Entities;
- Backup-Konsistenz der SQLite-Datenbank;
- Diagnostics/Repairs;
- Smartphone-/Desktop-Contract der Karte;
- Upgrade-/Schema-Strategie für spätere Versionen des Neubaus.

Besonders Raum ↔ HA-Bereich sollte **nicht vorschnell 1:1 vorausgesetzt** werden. Das ist eine Zuordnung zwischen zwei unterschiedlichen Modellen und gehört deshalb explizit in die Analyse.

---

# 12. Schlussfolgerung

Das Architekturmodell ist jetzt ausreichend geschlossen, um die Grundsatzdokumentation und `modul-bauplan` daraus abzuleiten.

Die wichtigste Entwicklung über die drei Runden ist aus meiner Sicht:

> **„Eine Quelle je Wert“ wird endgültig durch „ein fachlicher Eigentümer je Wert“ ersetzt.**

Daraus folgen Speicherort und Schnittstelle.

Ein Wert kann von Karte, Automation oder Sprache verändert werden und trotzdem genau **eine Wahrheit** besitzen, solange alle Zugriffe beim selben Eigentümer landen.

Ebenso wichtig:

> **Eine Schnittstelle ist kein Speicherort.**

Entity, Action und WebSocket sind Zugangswege. `Store`, Config Entry, Recorder oder Modul-DB sind Persistenz. Diese beiden Ebenen sollten im Leitfaden sprachlich konsequent getrennt werden.

# ✅ Einigkeit

- G-01 wird Eigentümer + Speicherort + Validierung.
- `module.yaml` enthält ausschließlich eigenes Eigentum.
- `haus` besitzt gemeinsame Hausfakten, Prognose und übliche Rückkehr.
- Geräte-Module besitzen ihre gerätespezifische Policy.
- Python-Codeänderung und Config-Entry-Reload werden als zwei verschiedene Themen dokumentiert.
- Listen und komplexe Objekte dürfen im Integrations-Store liegen.
- WebSocket ist für komplexe UI-Kommunikation geeignet.
- Actions werden zusätzlich angeboten, wenn eine Operation außerhalb der eigenen UI automatisierbar sein soll.
- `null = erben` und `[] = bewusst leer`.
- `translation_key` darf in unseren Projekten als stabiler semantischer Rollenname vertraglich verschärft werden.
- SQLite bleibt für Fachdaten; Settings-Store für eigene einfache Einstellungen.
- DBs erhalten Schema-Versionierung und Backup-Strategie; HA bietet dafür Pre-/Post-Backup-Hooks.
- Der Neubau beginnt mit Analyse und Contract, nicht mit UI oder Entities.

# ⚠️ Widerspruch / Präzisierung

- `translation_key` ist von HA nicht als allgemeiner öffentlicher Primärschlüssel einer Entity definiert. Wir können ihn **für unsere eigenen Integrationen** vertraglich so stabil behandeln, dürfen diese Projektkonvention aber nicht als HA-Grundsatz darstellen.
- Mehrere Bedienwege sind nicht automatisch mehrere Wahrheiten. Problematisch werden sie erst, wenn sie unterschiedliche Eigentümer/Speicher verwenden oder unterschiedliche Validierungslogik besitzen.
- Deshalb verbieten wir Optionsdialog + Karte für denselben Wert nicht technisch; wir vermeiden es aus UX-Gründen und definieren einen bevorzugten Bedienort.

# ❓ Rückfragen

**Keine blockierenden Rückfragen mehr.**

Die offenen Punkte betreffen jetzt die konkrete Analyse und Konstruktion des neuen Roboter-Moduls, nicht mehr die allgemeinen HA-Grundsatzregeln.

Die Grundsatzdoku und der Skill können auf dieser Basis geschrieben werden.
