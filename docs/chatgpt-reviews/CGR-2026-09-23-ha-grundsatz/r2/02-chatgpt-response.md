Review Runde 2

Claude,

die Korrekturen aus Runde 1 sind weitgehend richtig. Beim Einstellungsmodell würde ich aber eine wichtige Grenze ziehen: Nicht jede veränderbare Einstellung sollte automatisch eine HA-Entität werden. Die entscheidende Frage ist, ob der Wert außerhalb der Heidi-Oberfläche als HA-Zustand bzw. Automationsparameter nützlich ist.

1. Korrekturen aus Runde 1

Punkt| Urteil| Begründung
"command_line" 60 s| ✅| Korrektur angenommen. Aktuelle offizielle Doku: Sensor/Binary Sensor standardmäßig "scan_interval: 60", "command_timeout: 15".
Dreame "clean_area"| ✅| Für Heidi darf nicht angenommen werden, dass die verwendete Tasshack-Integration die neue HA-Abstraktion bereits unterstützt. Adapter bleibt, aber Capability-basiert und später austauschbar.
Roboterzustand nicht spiegeln| ✅| Genau richtig. "vacuum.*" bleibt Eigentümer des Roboterzustands. Heidi veröffentlicht nur eigene Ergebnisse.
Entity Registry statt ID-Bildung| ✅| Richtig. "unique_id", Gerät und Integration sind die stabilen Identitäten; sichtbare Entity-IDs dürfen Benutzer ändern.
kurzer Weg Stufe 0–1| ✅| Sinnvolle Vereinfachung.
Steckbrief + "module.yaml"| ✅| Besser als Dokumentzersplitterung.
Windows + WSL| ✅| Domain und Frontend plattformneutral testen; HA-Integration in HA-kompatibler Umgebung.
Neustart bei Integrationscode| ⚠️| Als Herberts sicherer Entwicklungsablauf okay, aber nicht als allgemeine HA-Regel formulieren. Config Entries sollen unload/reload unterstützen; dadurch ist nicht für jede Änderung prinzipiell ein kompletter HA-Neustart erforderlich.

Noch wichtig: Bei Optionsänderungen gibt es 2026 "OptionsFlowWithReload"; HA kann den Config Entry danach automatisch neu laden.

---

2. Einstellungsmodell für Heidi

Ich würde vier Fragen in dieser Reihenfolge stellen:

1. Gehört der Wert einem anderen System? → dort lassen.
2. Braucht HA/Automation den Wert als laufend veränderbaren Parameter? → Config-Entity.
3. Ist es selten geänderte Integrationskonfiguration? → Options Flow.
4. Ist es Bestandteil eines fachlichen Objekts wie eines Plans? → Fachdatenbank.

Der Einrichtungsdialog ist nur für Dinge gedacht, die zur Identität/Grundkonfiguration der Integration gehören. Home Assistant trennt dabei "ConfigEntry.data" für die eigentliche Konfiguration von "ConfigEntry.options" für weitere Einstellungen.

Konkrete Zuordnung

Einstellung| Eigentümer / Ort| HA-Typ / Beispiel| Grund
verwendeter Dreame-Roboter| Einrichtungsdialog| Config Entry| grundlegende Verbindung der Heidi-Integration
Automatik an/aus| Einstellungs-Entität| "switch", "translation_key: automation"| Dashboard und Automationen sollen sie direkt verwenden können
Mindest-Akku| Einstellungs-Entität| "number", "minimum_battery"| häufig relevant, automationsfähig; 10–80 %, Schritt 5
Schwelle „wenig Zeit“| Einstellungs-Entität| "number", "short_time_threshold"| laufender Entscheidungsparameter
Schnellprogramm an/aus| Einstellungs-Entität| "switch", "quick_program"| sichtbarer Betriebsparameter
Schnellprogramm Saugstufe| Einstellungs-Entität| "select", "quick_suction"| Werte müssen aus Capability/Adapter kommen
Schnellprogramm Wiederholungen| Einstellungs-Entität| "select/number", "quick_repeats"| dito
Leise-Profil| Einstellungs-Entitäten| "select", "quiet_suction"; "quiet_repeats"| laufende Heidi-Policy
Reaktion auf Anwesenheit| Heidi, Config-Entity| "select", "presence_behavior"| das Haus sagt nur wer/ob da; Heidi entscheidet, was das bedeutet
Personen, die für Heidi zählen| Heidi-Konfiguration| siehe Haus-Modul unten| gerätespezifische Policy
Arbeitszeit Tage/von/bis| Haus-Modul| Haus-Konfiguration/Entitäten| gemeinsame Haus-Schlussfolgerung, nicht Heidi-spezifisch
Heimkehr-Verhalten| Einstellungs-Entität| "select", "arrival_behavior"| Heidi-spezifische Reaktion
Fortsetzen max. Minuten| Einstellungs-Entität| "number", "resume_timeout"| operative Policy
übliche Rückkehr| Haus-Modul| Haus-Einstellung| wenn damit die übliche Rückkehr einer Person/des Haushalts gemeint ist
Prognose Personen| Haus-Modul| Haus-Konfiguration| Personenprognose ist nicht Staubsaugerlogik
Prognose Intervall| Optionsdialog| Option| technischer Tuningparameter, normalerweise nicht automatisiert
Prognose Auflösung| Optionsdialog| Option| dito
Prognose Lernwochen| Optionsdialog| Option| dito
Prognose Halbwertszeit| Optionsdialog| Option| dito
Prognose Mindesttage| Optionsdialog| Option| dito
Dunkelmodus| gar nicht als Heidi-Fachwert| HA/Frontend| Darstellung ist Benutzer-/Frontendthema
Kartendarstellung| Frontend-Konfiguration| Card config| kein Backend-Fachwert
Raumnamen Original/Deutsch| Frontend bzw. HA-Area-Namen| Card config| kein Heidi-Fachwert, sofern keine Fachlogik davon abhängt
„Lernen ab“| keine Einstellung| "button", z. B. "learning_reset"| das ist ein Befehl/Ereignis, kein dauerhafter Parameter
Pläne| Fachdatenbank| Planobjekte| zusammengesetzte Domainobjekte
Automatik-Abweichungen je Plan| im Planobjekt| DB| Override eines globalen Defaults

"EntityCategory.CONFIG" passt für veränderbare Konfigurationsentitäten ausdrücklich zum HA-Modell.

Damit entstehen wahrscheinlich nicht 30 ständig sichtbare Heidi-Config-Entities, sondern eher 10–15 operative Einstellungen. Technische und seltene Parameter verschwinden in Options Flows; reine Darstellung bleibt im Frontend.

---

3. Eigene Automatik je Plan

Dein Vorschlag ist richtig:

«Globaler Wert = Eigentümer des Defaults.
Plan = speichert ausschließlich seine Abweichung.»

Beispiel:

Global:
min_battery = 30
presence_behavior = wait
quick_program = true

Plan "Montag":
overrides:
    min_battery = 40

Plan "Freitag":
overrides: {}

Effektiver Wert:

effective = plan.override[key] ?? global[key]

Das erzeugt keine zweite Wahrheit.

Es existieren zwei verschiedene fachliche Werte:

global.minimum_battery = 30
plan[17].minimum_battery_override = 40

und daraus wird deterministisch:

effective.minimum_battery = 40

Wichtig: Nicht beim Erstellen eines Plans alle globalen Werte in den Plan kopieren. Sonst entsteht wieder Snapshot-Drift.

Die DB sollte deshalb semantisch zwischen "inherit" und Override unterscheiden können.

---

4. Persistenz von Config-Entities

Hier korrigiere ich meine Runde 1 etwas: Nicht pauschal "RestoreEntity" für alles.

Die Integration braucht einen klaren Konfigurationsspeicher.

Für Heidi würde ich:

- Config Entry / Options → HA persistiert selbst.
- Config-Entities mit dauerhaftem Heidi-Wert → zentraler Heidi-Settings-Store.
- "RestoreEntity" höchstens für einen wiederherstellbaren letzten Entity-State, nicht als zweites Settings-System.
- Plan-/Lernobjekte → SQLite.

Der entscheidende Grundsatz lautet wieder:

«Die Entity ist die HA-Repräsentation des Werts; sie darf nicht eine zweite unabhängige Kopie desselben Werts besitzen.»

Beim Start:

Store/Config
    ↓
Entity

Beim Ändern:

number.set_value
    ↓
NumberEntity
    ↓
validieren
    ↓
Settings Store
    ↓
Entity-State aktualisieren

Nicht:

RestoreEntity-Wert ↔ Store-Wert ↔ SQLite-Wert

---

5. Validierung

Bereiche gehören an die Entity.

Mindestakku beispielsweise:

native_min_value = 10
native_max_value = 80
native_step = 5

Die Domain-Schicht sollte trotzdem Eingaben validieren.

Warum doppelt?

Nicht zwei Wahrheiten, sondern zwei Schutzschichten:

- Entity beschreibt den zulässigen UI-/HA-Bereich.
- Domain verhindert ungültige Zustände unabhängig vom Aufrufer.

Das ist dieselbe Regel an zwei Systemgrenzen, keine doppelte Datenhaltung.

---

6. Wie die Karte Einstellungen verändert

Für Standard-Entities immer Standard-Actions.

Beispiele:

number.set_value
select.select_option
switch.turn_on
switch.turn_off
button.press

Keine eigenen Heidi-Actions dafür bauen.

Eigene Action nur für echte Domainoperationen:

heidi.create_plan
heidi.update_plan
heidi.delete_plan
heidi.run_plan

Dadurch funktionieren Heidi-Einstellungen automatisch auch mit:

- Standard-Dashboards
- Automationen
- Sprachsteuerung
- Entwicklerwerkzeugen
- anderen Karten.

---

7. Keine festen Werte in der Karte

Die Karte darf nicht wissen:

Akku = 10..80
Saugstufe = quiet/standard/turbo

Sie liest die Entity-Capabilities.

Bei "number":

min
max
step
unit

Bei "select":

options

Bei Gerätefähigkeiten kommen die Optionen aus Heidi/Adapter.

Damit ist der Adapter die Übersetzungsgrenze:

Dreame
quiet
standard
strong
turbo

        ↓ Adapter

Heidi Capability
[quiet, standard, strong, turbo]

        ↓

SelectEntity.options

        ↓

Karte

Die Karte rendert, was vorhanden ist.

---

8. Entity Registry und "translation_key"

Ich stimme deinem Punkt 4 ausdrücklich zu.

Die Karte darf nicht mehr machen:

"sensor." + prefix + "_entscheidung"

Stattdessen müssen die Entitäten stabile "unique_id"s besitzen und über Registry-/Device-Zuordnung auffindbar sein.

"translation_key" dient primär der Lokalisierung und sollte nicht allein als globale Identität missverstanden werden. HA empfiehlt übersetzte Entity-Namen statt fest codierter natürlicher Namen.

Deshalb Contract:

integration/domain
+ config entry/device
+ unique_id / semantic role

"translation_key" unterstützt die semantische Zuordnung, ist aber nicht der alleinige Primärschlüssel.

---

9. Nachteile vieler Config-Entities

Die Nachteile sind real.

30 Entities

Technisch kein Problem, für Herbert aber schnell unübersichtlich.

Deshalb:

Operativ relevante Einstellung → Entity.

Seltenes technisches Tuning → Options Flow.

Frontendpräferenz → Frontend.

Domainobjekt → DB.

Recorder

Jede Entity kann Historie erzeugen. Bei selten geänderten Config-Entities ist die Datenmenge gering. Wirklich laute oder selten benötigte Entities können standardmäßig deaktiviert werden; HA empfiehlt dieses Muster ausdrücklich.

Geräteansicht

Nicht jede Konfiguration muss dem physischen Dreame-Gerät zugeordnet werden.

Ich würde zwei HA-Geräte erwägen:

Dreame X60
→ physischer Roboter
→ Dreame-Integration

Heidi
→ virtueller Planer/Automatik
→ Heidi-Integration

Dadurch landen Heidi-Policy und Lernlogik nicht zwischen Bürsten-, Akku- und Mop-Entitäten des Roboters.

Das ist eine eigene Architekturentscheidung, die wir im Skill ausdrücklich prüfen sollten.

---

10. Haus-Modul

Hier muss die Grenze besonders sauber sein.

"haus" besitzt:

Wer ist da?
Ist jemand da?
Ist Arbeitszeit?
Ist Ruhezeit?
ggf. Anwesenheitsprognose

Heidi besitzt:

Welche Personen interessieren Heidi?
Was tut Heidi bei Anwesenheit?
Was tut Heidi bei Heimkehr?

Das bedeutet:

Arbeitszeitdefinition → "haus".

Personenauswahl für allgemeine Haus-Anwesenheit → "haus".

„Welche davon verhindern Staubsaugen?“ → "heidi".

Das verhindert, dass das Haus-Modul irgendwann Einstellungen wie:

Nicole verhindert Heidi
Nicole verhindert Luba
Nicole verhindert Lüftung

kennen muss.

---

11. Personen dynamisch auswählen

Keine Namen oder Entity-IDs fest codieren.

Der Heidi-Config-/Options-Flow benutzt einen Entity Selector für "person"-Entities und speichert die ausgewählten Registry-Bezüge/Entity-IDs als Konfiguration.

Beispiel semantisch:

heidi.presence_people:
    - person.herbert
    - person.nicole

Das ist keine Kopie der Anwesenheit.

Es ist Heidi-Konfiguration:

«Diese Personen sind für diese Regel relevant.»

Den aktuellen Zustand liest Heidi weiterhin von den "person.*"-Entities.

Bei Plänen gilt wieder Override:

plan.presence_people_override = null

bedeutet global übernehmen.

---

12. Grundsatzregeln Version 2

Nr.| Regel| Prüfbar durch
G-01| Jeder fachliche Wert hat genau einen Eigentümer und einen Schreibweg.| "module.yaml" nennt für jeden wichtigen Wert Owner und Storage; keine zweite persistente Kopie.
G-02| Vor Eigenbau wird die niedrigste geeignete native HA-Fähigkeit verwendet.| Bestand dokumentiert Entity/Action/Helper/Template vor Custom Code.
G-03| Fachlogik liegt im Modul, nicht im Frontend.| Karte enthält keine Entscheidung, die Backend-Ergebnisse verändert.
G-04| Module kommunizieren nur über öffentliche HA-Schnittstellen.| Keine fremden DB-Zugriffe, Dateien oder direkten Python-Imports.
G-05| Fähigkeiten bestimmen Verhalten, nicht Hersteller oder Modellname.| Hersteller-/Modellprüfungen nur im Adapter.
G-06| Ein aktueller HA-relevanter Zustand wird als Entity veröffentlicht.| Contract nennt Entity und Owner.
G-07| Befehle sind Actions, keine künstlichen Zustände.| Einmalige Operationen erscheinen nicht als Settings.
G-08| Historie wird nicht ohne fachlichen Grund dupliziert.| Standardhistorie → Recorder; eigene DB nur mit begründetem Datenmodell.
G-09| Einstellungen werden nach Lebenszyklus gespeichert: Setup, Options, Config-Entity oder Domainobjekt.| Steckbrief ordnet jede Einstellung genau einer Kategorie zu.
G-10| Große/komplexe Daten gehören nicht in Entity-Attribute.| Große Datensätze laufen über API/WebSocket/DB.
G-11| Entscheidungslogik ist möglichst rein und HA-unabhängig.| "domain/" kann ohne laufendes HA getestet werden.
G-12| Größere Integrationen besitzen Diagnostics und benutzerlösbare Fehler als Repairs.| Dateien/Tests vorhanden.
G-13| Geheimnisse und private Daten kommen weder ins Repo noch ungeschützt ins Frontend.| Secret-/Pfad-/"/local"-Checks.
G-14| Herstelleradapter existieren nur für Fähigkeiten, die HA nicht ausreichend standardisiert.| Jede Adapterfunktion nennt die fehlende HA-Capability.
G-15| Tests müssen vor Deployment grün sein; Integrationsänderungen werden kontrolliert geladen/reloaded.| CI/Deploy-Skript stoppt bei Testfehler.
G-16| Contract, Code und Dokumentation werden gemeinsam geändert.| Commit-/Drift-Test vergleicht "module.yaml", Entities, Actions und Doku.

---

13. Kurzer Weg – Stufe 0–1

Für einfache Projekte:

1 Auftrag
   ↓
Was soll funktionieren?

2 Bestand
   ↓
Was kann HA bereits?

3 Vertrag
   ↓
Welche Quellen, Zustände, Einstellungen und Aktionen?

4 Bau
   ↓
Helper / Template / Automation / Dashboard

5 Abnahme
   ↓
funktioniert / Neustart / unavailable / Doku

Ergebnis: ein Modul-Steckbrief.

Kein "module.yaml" zwingend.

---

14. Voller Weg – ab Stufe 2

1 Auftrag
2 HA-Bestand
3 Eigentumsregister
4 Modulvertrag + module.yaml
5 Ausbaustufe/Architektur
6 Mockup
7 Domain + Unit-Tests
8 HA-Integration
9 Oberfläche + Automationen
10 Diagnose / Replay / Abnahme / Deployment

Gate zwischen 4 und 5:

«Kein Code, solange Eigentümer, Eingänge, Ergebnisse und Schreibwege nicht eindeutig sind.»

Gate zwischen 7 und 8:

«Domain-Tests grün.»

Gate vor 10:

«Keine Fachlogik doppelt in UI/Automation/Integration.»

---

15. Modul-Steckbrief

Eine Datei reicht.

Empfohlene Abschnitte:

# Modul Heidi

## 1 Zweck
## 2 Nicht-Ziele
## 3 Ausbaustufe
## 4 Abhängigkeiten
## 5 Quellen
## 6 Fachlogik
## 7 Eigentumsregister
## 8 Entitäten
## 9 Einstellungen
## 10 Actions / Events / WebSocket
## 11 Speicherung und Historie
## 12 Oberfläche
## 13 Fehler / Diagnostics / Repairs
## 14 Tests
## 15 Deployment
## 16 Entscheidungen

Für Herbert lesbar.

"module.yaml" ist dagegen die maschinenlesbare Kurzfassung für Claude.

---

16. "module.yaml" Schema v1 – Heidi

schema: 1

module:
  id: heidi
  level: 3
  type: helper_integration
  integration: heidi

depends_on:
  integrations:
    - dreame_vacuum
    - haus

sources:
  - id: robot
    owner: dreame_vacuum
    interface: entity
    domain: vacuum

  - id: house
    owner: haus
    interface: entity

outputs:
  entities:
    - key: automation_allowed
      domain: binary_sensor
      owner: heidi

    - key: decision
      domain: sensor
      owner: heidi

    - key: next_run
      domain: sensor
      owner: heidi

settings:
  - key: automation
    owner: heidi
    storage: config_entity
    domain: switch

  - key: minimum_battery
    owner: heidi
    storage: config_entity
    domain: number

  - key: short_time_threshold
    owner: heidi
    storage: config_entity
    domain: number

  - key: forecast_learning_weeks
    owner: haus
    storage: options

data:
  - key: plans
    owner: heidi
    storage: sqlite

  - key: runs
    owner: heidi
    storage: sqlite

  - key: learning
    owner: heidi
    storage: sqlite

actions:
  - heidi.create_plan
  - heidi.update_plan
  - heidi.delete_plan
  - heidi.run_plan

adapters:
  - id: dreame
    reason: room_parameters_not_standardized

ui:
  type: custom_card

quality:
  diagnostics: true
  repairs: true
  shadow_mode: true
  replay_tests: true

Ich würde Schema v1 bewusst nicht größer machen.

Insbesondere keine:

- konkreten Entity-IDs
- Personen
- Raum-IDs
- Dreame-Modellnamen
- Dateipfade
- Defaultwerte

hineinnehmen.

Das gehört entweder in die Integration, den Steckbrief oder das Projektprofil.

---

17. Eine wichtige zusätzliche Entscheidung

Für die Architektur ergibt sich aus Runde 2 ein Grundsatz, den ich ausdrücklich festhalten würde:

«Nicht alles, was Herbert in einer eigenen Karte einstellen kann, muss eine HA-Entity sein.»

Sonst wird aus „HA-native“ schnell „Entity für jede Checkbox“.

Die Entscheidungsmatrix lautet:

Frage| Lösung
Braucht man es zur Einrichtung?| Config Flow
seltene Integrationseinstellung?| Options Flow
soll Automation/Dashboard den Wert laufend lesen oder ändern?| Config-Entity
Teil eines komplexen Fachobjekts?| DB
reine Darstellungspräferenz?| Frontend
einmaliger Befehl?| Action/Button
gehört einem anderen Gerät/Modul?| dort lassen

Das sollte meiner Einschätzung nach Bestandteil von G-09 und eine feste Entscheidungshilfe im Skill werden.

---

18. Noch eine Korrektur zur Entwicklung

Die Formulierung

«„Code-Änderung Integration = HA-Neustart“»

sollte im Herbert-Profil stehen, nicht als allgemeine HA-Grundsatzregel.

Eine ordentlich gebaute Config-Entry-Integration soll unload/reload unterstützen. Home Assistant nennt genau das als Qualitätsanforderung.

Für Herbert kann der sichere Workflow trotzdem sein:

Tests
→ Deploy
→ prüfen ob Roboter/andere abhängige Geräte untätig
→ Integration reload, wenn Änderung reload-sicher
→ HA-Neustart bei Python-Codeänderungen im Entwicklungsworkflow, wenn erforderlich
→ Smoke-Test

Damit bleibt der Skill technisch korrekt und Herberts tatsächlicher Ablauf trotzdem einfach.

---

19. Ergebnis für Heidi

Mit diesem Modell verschwindet das heutige Kernproblem aus "docs/DATEN.md": Dort existieren sieben Automatikwerte gleichzeitig als HA-Helfer und in "planer.json", teilweise sogar mit unterschiedlichen wirksamen Quellen.

Im Neubau gibt es beispielsweise:

minimum_battery
Owner: Heidi Settings
HA representation: NumberEntity
Persistence: Heidi settings store
Global value: 30

Plan 17:
minimum_battery_override: 40

Effective for Plan 17:
40

Nur ein globaler Wert, ein expliziter Plan-Override und ein daraus berechnetes Ergebnis.

Das ist die konkrete Bedeutung von:

«Ein Eigentümer je Datum.»

---

✅ Einigkeit

- "custom_components/heidi" ab Stufe 2
- Heidi kommuniziert ausschließlich über HA/Dreame-Integration
- separates "haus"-Modul
- "module.yaml" ab Stufe 2
- native HA-Capability vor Adapter
- Dreame-Adapter aktuell weiterhin notwendig
- Roboterzustände nicht in Heidi spiegeln
- Registry/Unique-ID statt zusammengesetzter Entity-ID
- kurzer Workflow für Stufe 0–1
- ein Steckbrief statt Dokumentzersplitterung
- Windows für Domain/UI, HA-kompatible Umgebung für Integration
- globale Einstellungen + sparse Plan-Overrides
- Shadow Mode, Replay und Drift-Prüfung

⚠️ Widerspruch / Präzisierung

- Meine Angabe aus Runde 1 zu "command_line" war falsch: 60 s ist für Sensoren aktuell korrekt.
- Nicht jede Einstellung gehört als Entity nach HA.
- "RestoreEntity" nicht als universellen Settings-Speicher verwenden.
- "translation_key" nicht als alleinige technische Identität der Entity verwenden.
- „Integrationscode geändert = zwingend kompletter HA-Neustart“ nicht als allgemeine Regel festschreiben; unload/reload ist Teil einer sauber gebauten Config-Entry-Integration.
- Arbeitszeit und allgemeine Anwesenheitsprognose gehören nach der jetzt beschlossenen Trennung eher "haus" als Heidi.

❓ Rückfragen

Für die nächste Runde sehe ich nur noch drei Entscheidungen, bevor Grundsatzdoku und Skill konkret gebaut werden können:

1. Soll "haus" allgemeine Haushaltsfakten liefern und jedes Gerätemodul selbst auswählen, welche Personen für seine Regeln relevant sind? Meine Empfehlung: ja.
2. Soll Heidi als eigenes virtuelles Gerät im HA Device Registry erscheinen, getrennt vom physischen Dreame X60? Meine Empfehlung: ja; das hält die Geräteansicht sauber.
3. Sollen operative Config-Entities ihren dauerhaften Wert in einem kleinen gemeinsamen Settings-Store der jeweiligen Integration besitzen und SQLite ausschließlich Fachdaten wie Pläne/Läufe/Lernen enthalten? Meine Empfehlung: ja.
