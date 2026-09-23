3m nachgedacht

Die Aufgabenstellung und der gewünschte Rahmen stammen aus deiner bereitgestellten Datei. 

Review Runde 1

Claude,

ich habe den Recherche-Brief gegen die aktuelle Home-Assistant-Dokumentation, Community-Referenzen und den Ist-Stand von Heidi geprüft. Das Grundkonzept geht klar in die richtige Richtung, aber drei Architekturentscheidungen würde ich vor dem Neubau korrigieren:

1. „Eine Quelle je Wert“ muss „ein fachlicher Eigentümer je Wert“ heißen. Eine einzige physische Datenbank für Einstellungen, Zustand, Historie und Lerndaten ist nicht das Ziel.
2. Eigene Module dieser Größenordnung gehören als Custom Integration in Home Assistant, nicht dauerhaft hinter "shell_command"/"command_line".
3. Herstelleradapter dürfen nur Lücken der HA-Abstraktion schließen. Home Assistant 2026 hat insbesondere bei Staubsaugern deutlich aufgeholt; Raumreinigung ist inzwischen standardisiert.

---

1. Recherche-Brief: geprüft, ergänzt, korrigiert

1.1 Grundarchitektur: im Wesentlichen richtig

Die Einteilung des Briefs ist fachlich sauber:

- Geräte-/Service-Integrationen bringen fremde Geräte nach Home Assistant.
- Entitäten bilden standardisierte Zustände und Fähigkeiten ab.
- Automationen und Skripte führen Verhalten aus.
- berechnete bzw. virtuelle Integrationen dürfen aus anderen HA-Zuständen neue Zustände ableiten.
- das Frontend konsumiert HA-Daten und ruft Aktionen/APIs auf.

Das entspricht der offiziellen HA-Architektur. Wichtig ist die Unterscheidung zwischen Geräteintegration und berechnender/helper-artiger Integration: Externe Geräteintegrationen sollen grundsätzlich nicht beliebig Zustände anderer Integrationen konsumieren; berechnende Integrationen wie "template" sind dagegen genau für abgeleitete Daten vorgesehen.

Für Heidi bedeutet das:

«Eine zukünftige "custom_components/heidi" wäre keine zweite Dreame-Geräteintegration, sondern eine fachliche/helper-artige Integration über der bestehenden Dreame-Integration.»

Das ist ein wichtiger Architekturpunkt.

---

1.2 Integration Quality Scale

Die Idee, die Integration Quality Scale als Qualitätscheckliste für eigene Integrationen zu verwenden, ist richtig. Bronze ist bei Core-Integrationen die Baseline; die höheren Stufen ergänzen u. a. Diagnose, Geräteverwaltung, Reparaturen und Reconfiguration. Für private Custom Integrations muss Herbert die Skala nicht formell erfüllen, aber als Prüfliste ist sie hervorragend.

Ich würde im Skill nicht die aktuelle Anzahl der Regeln hart codieren. Besser:

«„Prüfe gegen die jeweils aktuelle Integration Quality Scale; Mindestziel für eigene produktive Module: Bronze-Prinzipien plus Diagnostics, Repairs und sauberes Unload/Reload.“»

So veraltet der Skill nicht bei der nächsten HA-Version.

---

1.3 "shell_command": Recherche-Brief richtig

"Shell Command" wird nach 60 Sekunden beendet; das Timeout ist nicht konfigurierbar. Außerdem wird bei jedem Aufruf ein Prozess gestartet. Für kleine Hilfsbefehle ist das akzeptabel, für eine dauerhafte Facharchitektur nicht.

Genau die heutige Heidi-Konstruktion mit Planer, Prognose, Akku, Diagnose und Datenbankzugriff ist damit über die sinnvolle Einsatzgrenze von "shell_command" hinausgewachsen.

---

1.4 "command_line": eine Korrektur

Im Recherche-Brief steht sinngemäß ein Standard-Abfragetakt von 60 Sekunden.

Aktuell dokumentiert Home Assistant für "command_line":

- "command_timeout": Standard 15 s
- "scan_interval": Standard 30 s

nicht 60 s.

Das ist eine kleine Detailkorrektur, ändert aber nichts am Architektururteil: Polling eines Python-Programms, das wiederum Dateien/SQLite liest und JSON zurückgibt, ist bei Heidi unnötiger Overhead.

---

1.5 DataUpdateCoordinator und ereignisgesteuerte Aktualisierung

Der Recherche-Brief liegt hier richtig. Wenn eine Integration Daten gemeinsam abruft, ist "DataUpdateCoordinator" das Standardmuster. Bei vergleichbaren Daten kann "always_update=False" unnötige State-Writes vermeiden.

Für Heidi würde ich aber nicht alles über einen periodischen Coordinator laufen lassen. Vieles kann direkt auf HA-State-Changes reagieren:

- Roboterzustand
- Anwesenheit
- Ruhezeit
- Arbeitszeit
- Helfer/Config-Entities
- Start/Ende eines Laufs

Polling nur dort, wo die Datenquelle selbst keinen Push bietet.

---

1.6 Config Flow und Options Flow: klarer Standard

Der Recherche-Brief ist hier richtig. Moderne Integrationen sollen über Config Entries/Config Flows eingerichtet werden. Options Flows sind für änderbare Integrationsoptionen vorgesehen.

Die jüngste HA-Richtung ist eindeutig: Der alte Configurator wird 2027 entfernt; Config Flow und Config Entry sind der vorgesehene Weg.

---

1.7 Einstellungen als "EntityCategory.CONFIG"

Auch das ist korrekt, aber der Grundsatz muss differenzierter werden.

"EntityCategory.CONFIG" ist ausdrücklich für Entitäten gedacht, mit denen Geräte-/Integrationskonfiguration verändert wird.

Daraus folgt:

- Config Flow: Grundkonfiguration, die selten geändert wird.
- Options Flow: Integrationseinstellungen, die gelegentlich geändert werden.
- Config-Entities ("number", "select", "switch", "time" usw.): Einstellungen, die sichtbar, automatisierbar und laufend veränderbar sein sollen.
- Datenbank: keine Standardablage für normale HA-Konfiguration.

Damit widerspricht die derzeitige Idee „alle Einstellungen in "heidi.db"“ teilweise der HA-Praxis.

---

1.8 Frontend: eine Korrektur

Der Satz

«„Keine eingebauten "ha-*"-Bausteine“»

ist zu absolut.

Aktuelle HA-Entwicklerinformation sagt sinngemäß: Custom Cards können HA-Frontend-Komponenten verwenden, interne APIs und interne Komponenten sind aber nicht stabil garantiert.

Die bessere Regel lautet:

«Keine undokumentierten HA-internen Komponenten als unverzichtbare Grundlage verwenden. Wo HA-Komponenten benutzt werden, hinter einer kleinen lokalen Wrapper-Schicht kapseln.»

Das schützt vor Frontend-Änderungen, ohne auf nützliche Standardbausteine zu verzichten.

---

2. Wichtige Änderung 2026: Staubsauger-Raumreinigung ist jetzt HA-standardisiert

Das ist für Heidi der wichtigste neue Recherchebefund.

Home Assistant 2026.3 führte "vacuum.clean_area" ein. Robotersegmente werden dabei einmal HA-Bereichen zugeordnet. Aktionen verwenden anschließend HA-Areas statt Hersteller-Raum-IDs.

Die Vacuum-Entity-API kennt inzwischen:

- "async_get_segments()"
- "async_clean_segments()"
- "Segment"
- standardisiertes Area-Mapping
- Erkennung geänderter Segmente

Roborock, Ecovacs und Matter implementieren diese Architektur bereits.

Damit korrigiere ich Regel 7 deutlich:

«Nicht grundsätzlich „Adapter je Hersteller“.

Erst prüfen, ob HA eine standardisierte Capability anbietet. Nur fehlende Funktionen kommen in einen Herstelleradapter.»

Für Heidi heißt das konkret:

Raum reinigen
    ↓
vacuum.clean_area
    ↓
HA-Area-Mapping
    ↓
Dreame-Integration

und nicht:

Heidi-Karte
    ↓
Dreame-Raum-ID
    ↓
eigener Dreame-Adapter

Sofern die verwendete Dreame-Integration "CLEAN_AREA" unterstützt, sollte Heidi diese Standardfunktion benutzen.

Das Prinzip der "xiaomi-vacuum-map-card", je Plattform unterschiedliche Service-Templates einzubauen, war historisch sinnvoll und ist als Community-Referenz interessant.

2026 sollte Herbert diese Plattformadapter aber nur noch dort übernehmen, wo HA selbst keine gemeinsame Schnittstelle besitzt.

---

3. Referenzfall Heidi

3.1 Was bereits sehr gut ist

A. Frontend-Schichtung

Die bestehende Kartenarchitektur ist deutlich besser als typische Hobby-Dashboards:

contract
  ↓
device/profile
  ↓
selectors
  ↓
components

Schreiben → DxApi

"contract.ts" zentralisiert die HA-Schnittstelle, "profile.ts" beschreibt Fähigkeiten dynamisch, Selektoren isolieren HA-State und "DxApi" zentralisiert Schreibzugriffe.

Das ist ein gutes Muster und sollte erhalten bleiben.

B. Keine festen Gerätemodelle

Gerät, Räume und verfügbare Optionen werden möglichst entdeckt statt hart codiert.

Das ist exakt die richtige Richtung.

C. Reine Fachfunktionen

"planer_entscheider.py", "checkliste.py" und Teile der TS-Domainlogik sind bereits als reine Funktionen konzipiert.

Das ist vermutlich das wertvollste Stück des heutigen Backends: Diese Logik lässt sich praktisch unverändert in die neue Integration übernehmen.

D. Tests

Typprüfung, Unit-Tests, Build und Playwright-E2E sind für ein privates HA-Projekt überdurchschnittlich gut.

E. Deployment

Der heutige "deploy.ps1" mit gezieltem Kopieren und Ressourcenversionierung ist ebenfalls eine gute Grundlage.

---

4. Was beim Neubau nicht übernommen werden sollte

4.1 "shell_command" / "command_line" als Backendbus

Heute ruft HA die eigentliche Fachanwendung über externe Python-Prozesse auf.

Für wenige Skripte wäre das okay. Bei Heidi existieren inzwischen jedoch:

- Planer
- Entscheidungslogik
- Checklisten
- Anwesenheit
- Diagnose
- Akkulernen
- Laufprotokoll
- Datenbank
- Kartenfläche
- Auftragsverwaltung

Das ist faktisch bereits eine Anwendung.

Neubauempfehlung: "custom_components/heidi".

---

4.2 Base64 als interner Transport

Dass JSON zwischen HA-Templates und Python-Prozessen base64-kodiert wird, ist ein klares Symptom der falschen Transportebene.

In einer Custom Integration existieren Python-Objekte direkt im selben Prozess. Dann entfallen:

- Base64
- Shell quoting
- JSON-Serialisierung für interne Aufrufe
- Prozessstart
- stdout als Rückkanal

Base64 sollte im Neubau praktisch verschwinden.

---

4.3 Der Frontend-Contract kennt noch zu viel Dreame

Heute erkennt "device.ts" explizit "dreame_vacuum", bildet Entitätspräfixe und rekonstruiert Fähigkeiten aus Herstellerentitäten.

Das war für v1/v2 sinnvoll.

Im Neubau würde ich den Vertrag umdrehen:

Dreame Integration
        ↓
custom_components/heidi
        ↓
stabiler Heidi-Contract
        ↓
Heidi-Karte

Die Karte sollte möglichst Heidi verstehen, nicht Dreame.

Beispiel:

binary_sensor.heidi_automatik_freigabe
sensor.heidi_entscheidung
sensor.heidi_naechster_lauf
sensor.heidi_lernstatus

und Aktionen:

heidi.plan_save
heidi.plan_delete
heidi.start_plan

Gerätenahe Standardaktionen dagegen direkt über HA:

vacuum.clean_area
vacuum.pause
vacuum.return_to_base

---

5. Das größte Problem im aktuellen Datenmodell

E-128 sagt:

«Alle Daten des Projekts – Messdaten, Einstellungen und Zustand – in eine SQLite-Datenbank.»

Die Motivation ist richtig: doppelte Wahrheiten vermeiden.

Die Lösung ist aber zu zentralistisch.

Ich würde den Grundsatz ändern von:

«eine Datenbank für alles»

zu:

«ein Eigentümer für jedes Datum»

Das ist nicht dasselbe.

Empfohlenes Eigentumsmodell

Art| Eigentümer
aktueller Roboterzustand| Dreame-/Vacuum-Entitäten
aktueller Hauszustand| Haus-Modul-Entitäten
normale Geräte-/Modulkonfiguration| Config Entry / Options / Config-Entities
kleine interne Integrationzustände| HA "Store"
normaler Zeitverlauf von Entitäten| HA Recorder
Langzeitstatistik geeigneter Sensoren| HA Statistics/Recorder
spezielle Heidi-Laufdaten| "heidi.db"
Lern-/Trainingsdaten| "heidi.db"
komplexe Planobjekte| "heidi.db" sinnvoll
große Kartendaten| eigener WebSocket/API-Pfad, nicht Entity-Attribute

Der HA Recorder ist ausdrücklich für Entitätshistorie zuständig und versorgt History, Activity und Graphen. Standardmäßig werden zehn Tage Rohhistorie gehalten.

Für kleinen persistenten Integrationszustand existiert außerdem HA "Store"; Core selbst benutzt dieses Muster umfangreich.

Die eigene SQLite-Datenbank bleibt also sinnvoll – aber als Fachdatenspeicher, nicht als Ersatz für HA-Konfiguration und HA-State.

---

6. Warum diese Änderung bei Heidi wichtig ist

"docs/DATEN.md" zeigt exakt das Problem, das E-128 lösen wollte: sieben Einstellungen existieren heute doppelt und werden teilweise an unterschiedlichen Stellen gelesen.

Das ist ein echter Architekturfehler.

Aber daraus folgt nicht:

«Alles muss in SQLite.»

Sondern:

«Jede Einstellung bekommt einen einzigen Eigentümer und einen einzigen Schreibweg.»

Beispiel Mindestakku:

number.heidi_min_battery

kann gleichzeitig:

- UI-konfigurierbar
- Automationsquelle
- persistiert
- typisiert
- begrenzt
- von der Integration direkt lesbar

sein.

Dafür braucht es keinen zweiten DB-Katalog.

---

7. Haus-Modul: grundsätzlich richtig, aber kleiner schneiden

E-136 ist architektonisch stark:

«Anwesenheit, Ruhezeiten und Arbeitszeit werden Haus-weit bereitgestellt.»

Das Problem ist nicht die Idee, sondern die Gefahr eines zukünftigen God Modules.

Ich würde drei Ebenen unterscheiden:

FAKTEN
person.*
binary_sensor.*_presence
calendar.*
time/schedule
        ↓
HAUS-INFERENZ
jemand_da
homeoffice
ruhezeit
arbeitszeit
        ↓
GERÄTEPOLICY
Heidi darf fahren?
Luba darf mähen?
Lüftung darf laut laufen?

Das Haus-Modul soll nur die mittlere Ebene besitzen.

Heidi entscheidet weiterhin selbst:

«„Was bedeutet Ruhezeit für einen Staubsauger?“»

Der Mäher entscheidet:

«„Was bedeutet Ruhezeit für Mähen?“»

Damit bleibt das Haus-Modul klein und projektneutral.

---

8. Datenaustausch zwischen Modulen

Regel 4 lautet heute:

«nur über Entitäten.»

Das ist fast richtig, aber zu eng.

Ich würde daraus machen:

«Module kommunizieren ausschließlich über öffentliche Home-Assistant-Schnittstellen. Keine fremden Datenbanken, Dateien oder Python-Interna.»

Erlaubt:

- Entitäten für aktuellen Zustand
- Actions/Dienste für Befehle
- Events für Ereignisse
- WebSocket/API für große oder anfragebasierte Daten

Entitäten sind bevorzugt, wenn ein aktueller Zustand dargestellt wird.

Ein Ereignis wie:

heidi_run_completed

muss nicht künstlich als Sensor modelliert werden.

---

9. Bewertung der Regeln 1–10

Regel| Bewertung| Änderung
1 Eine Quelle je Wert| ✅ Kern richtig| „ein Eigentümer je Datum“, nicht „alles DB“
2 Modul rechnet, UI zeigt| ✅| UI darf Präsentationslogik besitzen, aber keine fachliche Wahrheit
3 Ergebnisse als Entitäten| ✅| Zustände ja; große Daten/Abrufdaten nicht zwanghaft
4 Module nur über Entitäten| ⚠️| erweitern auf Entitäten + Actions + Events + APIs
5 Module entscheiden, HA führt aus| ✅| sehr guter Grundsatz
6 Fähigkeiten statt Modelle| ✅| unbedingt behalten
7 Adapter je Hersteller| ⚠️| nur für HA-Lücken
8 Haus-Modul| ✅| Fakten/Policy sauber trennen
9 Ausbaustufen| ✅| um „Custom Integration“ explizit ergänzen
10 Tests/Doku/Mockup| ✅| zusätzlich Architektur-/Contract-Gate

---

10. Ab wann Custom Integration?

Für mich ist die Entscheidung eindeutig.

YAML bleibt richtig für

- kleine Automationen
- einfache Template-Sensoren
- wenige Helfer
- Blueprints
- einfache Zusammenführung vorhandener HA-Entitäten

Custom Integration wird richtig, sobald mehrere dieser Punkte gelten

- eigener persistenter Zustand
- eigene Fachlogik
- mehrere Ergebnisentitäten
- eigene Actions
- mehrere Trigger/Listener
- eigene Datenbank
- Diagnostik
- eigenes Frontend
- komplexe asynchrone Abläufe
- wiederverwendbares Modul

Heidi erfüllt praktisch alle Punkte.

Deshalb:

«Heidi Neubau direkt als Custom Integration.»

Nicht erst später migrieren.

Das spart sogar Komplexität, weil die heutige Shell-/JSON-/Base64-Brückentechnik entfällt.

---

11. Empfohlene Heidi-Zielarchitektur

Dreame HACS Integration
        │
        │ Standard-Entitäten / Vacuum-Actions
        ▼
┌────────────────────────────┐
│ custom_components/heidi    │
│                            │
│ adapter/                   │
│   dreame.py                │ nur HA-Lücken
│                            │
│ domain/                    │
│   planner.py               │ reine Funktionen
│   decision.py              │ reine Funktionen
│   learning.py              │ reine Funktionen
│   house_policy.py          │ Heidi-spezifisch
│                            │
│ sensor.py                  │ Ergebnisse
│ binary_sensor.py           │ Ergebnisse
│ number/select/switch.py    │ veränderbare Einstellungen
│ services.py                │ Heidi-spezifische Actions
│ websocket.py               │ große Daten / Diagramme
│ storage.py                 │ DB-Abstraktion
│ diagnostics.py             │ Diagnose
│ repairs.py                 │ Benutzerprobleme
└─────────────┬──────────────┘
              │
              ├──► heidi.db
              │    Pläne
              │    Laufprotokoll
              │    Lernen
              │    Spezialhistorie
              │
              ├──► HA-Entitäten
              │
              └──► Actions / WebSocket
                        │
                        ▼
                Heidi Custom Card

Die Frontend-Architektur von HA ist ausdrücklich unidirektional aufgebaut; zusätzliche Daten können über WebSocket-Abonnements bereitgestellt werden.

---

12. Einstellungen: konkrete Empfehlung

Nicht eine einzige Technik für alle Einstellungen.

A. Config Flow

Für:

- zu verwendender Roboter
- Grundverknüpfungen
- Datenbankmodus
- grundlegende Modulaktivierung

B. Options Flow

Für selten geänderte Betriebsparameter.

C. Config-Entities

Für Dinge, die Herbert im Alltag oder in Automationen ändern könnte:

number.heidi_min_battery
number.heidi_fast_threshold
select.heidi_return_behavior
switch.heidi_automation
time.heidi_work_start
time.heidi_work_end

D. SQLite

Für zusammengesetzte Objekte:

Plan
Plan-Schritte
Lauf
Raum-Lernwert
Auftrag
Diagnoseevent

Das wäre wesentlich näher an HA-Konventionen als ein universeller Einstellungskatalog in SQLite.

---

13. Recorder, SQLite oder InfluxDB?

Recorder

Immer zuerst für normale Entitätshistorie.

Projekt-SQLite

Ja, wenn Daten fachlich strukturierter sind als einfache Zeitreihen:

- Reinigungsläufe
- Raumkombinationen
- Lernmodelle
- Planer
- Auftragshistorie

Heidi ist dafür ein legitimer Fall.

InfluxDB

Nicht als Standardbestandteil der Grundsatzregeln.

InfluxDB lohnt sich erst, wenn Herbert wirklich geräteübergreifend größere Langzeitanalysen machen will:

- Strom
- Raumklima
- Pool
- Lüftung
- Netzwerk
- Roboter
- Wetter

Für den Modulbauplan sollte deshalb gelten:

«Recorder → zuerst.
Eigene DB → bei fachlichen Daten.
InfluxDB → optionales Analytics-System, nicht Source of Truth.»

---

14. Oberfläche: Karte, Panel oder Standard-Dashboard?

Ich würde drei Stufen definieren.

Standardkarten

Wenn das Modul nur:

- Status
- wenige Einstellungen
- wenige Buttons
- Charts

braucht.

Custom Card

Wenn es eine eigenständige interaktive Komponente gibt.

Beispiel:

- Roboterkarte
- Planer
- Raumsteuerung

Custom Panel

Nur wenn es tatsächlich eine vollständige Anwendung mit eigener Navigation ist.

Home Assistant unterstützt sowohl Custom Cards als auch Custom Panels und Dashboard Strategies.

Für Heidi ist die heutige app-artige Oberfläche gerechtfertigt.

Für Pool, Netzdiagnose oder einen einfachen Lüftungsrechner wäre sie wahrscheinlich unnötig.

---

15. Diagnose und Reparaturen

Das fehlt als Grundsatz noch deutlich.

Jede größere Custom Integration sollte zwei Dinge besitzen:

Diagnostics

HA bietet dafür einen offiziellen Downloadmechanismus. Geheime Daten müssen dabei geschwärzt werden.

Repairs

Probleme, die Herbert selbst lösen kann, sollten als HA-Reparaturhinweis erscheinen.

Beispiele:

Dreame-Raumzuordnung hat sich geändert
Datenbank nicht schreibbar
alte Datenbankversion
notwendige Entität fehlt
Haus-Modul nicht installiert

Das ist für Herbert als HA-Einsteiger wesentlich besser als Logdateien durchsuchen.

---

16. Backup

Die aktuelle Heidi-Idee, vor dem HA-Backup eine konsistente Datenbankkopie zu erzeugen, hat den richtigen Gedanken.

In einer eigenen Integration würde ich aber die offizielle Backup-Plattform verwenden:

async_pre_backup()
async_post_backup()

Home Assistant sieht genau dafür Hooks vor.

Die separate 02:50-Uhrzeit sollte damit im Neubau entfallen.

---

17. Sicherheit

Audit_0083 ist wichtig: Dateien unter "/config/www" sind über "/local" ohne Authentifizierung erreichbar.

Das bestätigt auch die offizielle Frontend-Doku.

Damit sollte eine Grundsatzregel lauten:

«Personenbezogene, ortsbezogene oder diagnostische Daten nie über "/local" ausliefern.»

Große private Daten → authentifizierter WebSocket/API-Endpunkt.

---

18. Die 13 Hausregel-Widersprüche bestätigen das Architekturproblem

"HAUSREGELN.md" zeigt u. a.:

- unterschiedliche Definitionen von Anwesenheit
- doppelte Arbeitszeit
- geschrieben wird Datei, gelesen Helfer
- unterschiedliche Ruhezeitlogik
- zwei Zustandstexte
- Szenen ignorieren Hauptschalter

Das ist kein lokaler Bug.

Es ist die typische Folge davon, dass dieselbe fachliche Entscheidung in:

- Templates
- Automationen
- Python
- Karte

mehrfach implementiert wird.

Daher ist Regel 2 besonders wichtig:

«Eine fachliche Entscheidung wird genau einmal gerechnet.»

---

19. Vorschlag für die „HA-Grundsatzregeln“

Ich würde die Dokumentation nicht als lange Sammlung einzelner Tipps schreiben, sondern als verbindlichen Architekturstandard.

Empfohlene Struktur:

docs/ha-grundsatz/
│
├── 00-grundprinzipien.md
├── 01-ausbaustufen.md
├── 02-modul-architektur.md
├── 03-entitaeten-und-actions.md
├── 04-daten-und-speicher.md
├── 05-einstellungen.md
├── 06-automationen.md
├── 07-frontend.md
├── 08-tests.md
├── 09-diagnose-und-sicherheit.md
├── 10-deployment-versionen.md
└── referenz-ha-2026.md

"referenz-ha-2026.md" enthält Plattformwissen.

Der Skill selbst enthält keine festen Heidi-Pfade oder Entitätsnamen.

---

20. Kernregeln, die ich dort verbindlich machen würde

G-01 Ein Eigentümer pro Datum

Jeder Wert besitzt genau einen fachlichen Eigentümer.

G-02 Native HA-Funktion zuerst

Vor eigener Logik prüfen:

1. Standard-Entity
2. Standard-Action
3. Helper
4. Template
5. Automation
6. erst dann eigenes Modul

Das deckt sich auch mit dem Community-Skill "home-assistant-best-practices", dessen Kernprinzip ebenfalls „native HA constructs first“ ist.

G-03 Module besitzen Fachlogik

Keine fachlichen Entscheidungen im Frontend.

G-04 Öffentliche HA-Schnittstellen zwischen Modulen

Keine fremden Dateien, DB-Tabellen oder Python-Imports.

G-05 Capability vor Hersteller

Native HA-Capability → sonst Adapter.

G-06 State ist Entität

Wenn etwas einen aktuellen Zustand besitzt und für HA interessant ist, wird es Entität.

G-07 Command ist Action

Befehle werden nicht als Zustandsänderung missbraucht.

G-08 Historie nicht duplizieren

HA Recorder verwenden, außer die Fachdomäne verlangt ein eigenes Datenmodell.

G-09 Einstellungen passend modellieren

Config Flow / Options / Config-Entities statt Universal-JSON oder Universal-DB.

G-10 Große Daten nicht in Entity-Attribute pressen

WebSocket/API verwenden.

G-11 Pure Domain Core

Entscheidungslogik möglichst HA-unabhängig und deterministisch.

G-12 Diagnostics + Repairs

Für größere Custom Integrations Pflicht.

G-13 Keine Geheimnisse

Keine Tokens, Koordinaten, Gerätekennungen oder personenbezogenen Logs im Repo.

G-14 Kein privater Inhalt in "/local"

G-15 Tests vor Deployment

G-16 Dokumentation im selben Commit

---

21. Namensschema

Hier würde ich bewusst nicht versuchen, jede Entity-ID vollständig zu erzwingen.

Home Assistant erlaubt Benutzern inzwischen explizit, Entity-IDs selbst zu benennen bzw. zu ordnen.

Deshalb:

Integration-Domain

heidi
hausregeln
netzdiagnose
poolanalyse

klein, "snake_case".

Unique IDs

Stabil und niemals aus sichtbaren Namen ableiten.

Beispiel:

heidi:automation_allowed
heidi:next_run
heidi:min_battery

Entity-Namen

Über "translation_key" + "has_entity_name".

Nicht vollständige Entity-ID im Code als primären Vertrag behandeln.

Actions

Verborientiert:

heidi.plan_create
heidi.plan_update
heidi.plan_delete
heidi.learning_reset

Standardoperationen nicht neu erfinden:

vacuum.clean_area
vacuum.pause
vacuum.return_to_base

---

22. Repo-Struktur eines größeren Moduls

Für Heidi etwa:

HA_Dash_DreameX60/
│
├── custom_components/
│   └── heidi/
│       ├── __init__.py
│       ├── manifest.json
│       ├── config_flow.py
│       ├── const.py
│       ├── coordinator.py
│       ├── sensor.py
│       ├── binary_sensor.py
│       ├── number.py
│       ├── select.py
│       ├── switch.py
│       ├── services.yaml
│       ├── diagnostics.py
│       ├── repairs.py
│       ├── backup.py
│       ├── websocket.py
│       │
│       ├── adapters/
│       │   └── dreame.py
│       │
│       └── domain/
│           ├── planner.py
│           ├── decision.py
│           ├── learning.py
│           └── models.py
│
├── card/
├── tests/
├── docs/
├── tools/
└── CLAUDE.md

Die "domain/"-Schicht darf keine HA-Abhängigkeiten benötigen.

Damit kann Claude Code den Großteil der Logik auch unter Windows testen.

Nur Integrationstests brauchen WSL/Devcontainer.

---

23. Ausbaustufen – überarbeitete Version

Die aktuelle Staffelung ist grundsätzlich gut.

Ich würde sie so definieren:

Stufe 0
HA vorhandene Funktion direkt benutzen

Stufe 1
Helper / Template / Automation / Script

Stufe 2
eigenes Fachmodul als Custom Integration

Stufe 3
eigene Custom Card

Stufe 4
eigener Panel-/App-Bereich

Stufe 5
Herstelleradapter, falls HA keine gemeinsame Capability hat

Wichtig:

«Adapter kommt zuletzt, nicht automatisch nach Custom Integration.»

---

24. Skill „modul-bauplan“ – bessere Reihenfolge

Der bisherige Ablauf ist gut, aber der Contract sollte vor dem Mockup entstehen.

Modus PLANEN

Phase 0 – Auftrag

Ergebnis:

problem.md

Enthält:

- Problem
- Nutzer
- gewünschtes Verhalten
- Erfolgskriterien
- ausdrücklich nicht enthaltene Funktionen

Phase 1 – HA-Bestandsaufnahme

Prüfen:

- bestehende Integration
- Entitäten
- Actions
- Geräte
- Areas
- Labels
- Standard-Capabilities

Ergebnis:

bestand.md

Hier wird bereits entschieden:

«Kann HA das ohne eigenes Modul?»

Phase 2 – Eigentum und Grenzen

Für jeden Wert:

Quelle
Eigentümer
Leser
Schreiber
Persistenz
Historie

Ergebnis:

datenvertrag.md

Phase 3 – Modulcontract

Definieren:

- Eingänge
- Ergebnisentitäten
- Config-Entities
- Actions
- Events
- WebSocket-Daten
- Abhängigkeiten

Ergebnis:

contract.md

Phase 4 – Ausbaustufe entscheiden

Jetzt erst:

nur HA?
Custom Integration?
Custom Card?
Panel?
Adapter?

Phase 5 – Mockup

Mockup verwendet ausschließlich den Contract aus Phase 3.

Damit kann das UI nicht neue Backend-Wahrheiten erfinden.

Phase 6 – Domain Core

Pure Funktionen und Tests.

Phase 7 – HA Integration

Config Entry, Entitäten, Actions, Storage, Diagnostics, Repairs.

Phase 8 – Oberfläche

Standardkarten zuerst; eigene Karte nur wenn begründet.

Phase 9 – Automationen

Automationen koordinieren bereits vorhandene Zustände und Actions.

Keine Fachlogik duplizieren.

Phase 10 – Abnahme

Prüfen:

- Tests
- Neustart
- Reload
- unavailable
- fehlende Entitäten
- Backup
- Restore
- Geräteoffline
- Browser mobil/desktop
- keine Secrets
- keine "/local"-Lecks

---

25. Modus PRÜFEN

"modul-bauplan prüfen" sollte nicht einfach allgemeinen Code Review machen.

Es prüft gezielt gegen nummerierte Grundsatzregeln.

Befundformat:

🔴 BLOCKER
Regel: G-01 Ein Eigentümer pro Datum
Datei: ...
Stelle: ...
Befund: ...
Folge: ...
Empfehlung: ...

Schwere:

🔴 Blocker
Architektur verhindert korrektes Zielbild

🟠 Hoch
führt wahrscheinlich zu Drift, Sicherheits- oder Wartungsproblemen

🟡 Mittel
nicht HA-typisch oder unnötig komplex

⚪ Hinweis
Verbesserung ohne akuten Architekturfehler

Wichtig:

Der Prüfer soll nicht jeden kleinen Style-Punkt melden.

Nur Befunde, die den Neubau beeinflussen.

---

26. Modus NACHSCHLAGEN

Beispiel:

/modul-bauplan Wie speichere ich eine Einstellung?

Antwortstruktur:

Empfohlener HA-Weg
↓
welche Grundregel
↓
wann Alternative sinnvoll
↓
kleines Beispiel
↓
offizielle HA-Quelle

Keine langen Architekturreviews.

---

27. Community-Referenzen

Der Community-Skill "home-assistant-best-practices" bestätigt eine wichtige Richtung:

«Native HA-Konstrukte vor Templates und eigener Logik.»

"awesome-home-assistant" ist sinnvoll als Entdeckungsquelle, aber nicht als Normquelle. Es ist eine kuratierte Sammlung von Integrationen, Karten, Apps und öffentlichen HA-Konfigurationen.

Die Xiaomi Vacuum Map Card zeigt ein interessantes historisches Adaptermuster für verschiedene Roboterplattformen.

Dieses Muster sollte im neuen Leitfaden aber explizit mit folgendem Satz versehen werden:

«Plattformadapter nur verwenden, wenn die aktuelle HA-Version noch keine gemeinsame Domain-Capability anbietet.»

---

28. Fünf Ideen über die übliche Praxis hinaus

Idee 1 – Maschinenlesbarer Modulvertrag

Jedes Projekt erhält:

module:
  id: heidi
  type: helper_integration

sources:
  - vacuum
  - house

outputs:
  entities:
    - automation_allowed
    - decision
    - next_run

actions:
  - plan_create
  - plan_update

storage:
  plans: sqlite
  history: recorder
  learning: sqlite

Der Skill kann daraus Architektur, Tests und Doku prüfen.

Das verhindert Drift zwischen Doku und Code.

---

Idee 2 – Eigentumsregister

Für jedes wichtige Datum:

min_battery
Owner: number.heidi_min_battery
Writers: User/Automation
Readers: Heidi Planner
History: Recorder

Claude kann automatisiert prüfen, ob derselbe Wert noch irgendwo als JSON/DB/Helfer dupliziert ist.

Gerade die sieben heutigen Heidi-Dubletten wären damit sofort sichtbar.

---

Idee 3 – Shadow Mode als Standardmuster

Heidi macht das bereits teilweise hervorragend.

Neue Entscheidungslogik wird zuerst nur veröffentlicht:

sensor.heidi_decision

mit:

would_start
reason
blocked_by
next_possible_time

Noch keine Aktion.

Erst nach realen Vergleichsdaten wird scharf geschaltet.

Ich würde dieses Muster in den Grundsatzregeln ausdrücklich festschreiben.

---

Idee 4 – Ereignis-Replay

Bei wichtigen Entscheidungsmodulen anonymisierte Eingangsdaten protokollieren:

timestamp
presence
quiet
battery
vacuum_state
schedule

Dann kann Claude Code einen vergangenen Tag offline erneut durch den Entscheidungsalgorithmus laufen lassen.

Damit kann man Änderungen prüfen:

«„Was hätte die neue Logik letzten Dienstag anders gemacht?“»

Für Automatiklogik ist das extrem wertvoll.

---

Idee 5 – Architektur-Drift-Test

Automatisch prüfen:

- unbekannte Entity-IDs im Frontend
- direkte "hass.callService" außerhalb "DxApi"
- direkte DB-Öffnung außerhalb "storage.py"
- Herstellername außerhalb Adapter
- Secret-artige Werte
- "/local" mit privaten Daten
- doppelte Einstellungsquellen

Damit werden Herberts Grundsatzregeln zu ausführbaren Regeln, nicht nur Dokumentation.

Das ist meiner Einschätzung nach der größte Hebel für Claude Code.

---

29. Die 10 wichtigsten Empfehlungen

1. E-128 ändern: nicht „eine DB für alles“, sondern „ein Eigentümer je Datum“.
2. Heidi im Neubau direkt als Custom Integration bauen.
3. Reine Entscheidungslogik aus dem heutigen Projekt übernehmen; Shell-/Base64-Schicht verwerfen.
4. Native HA-Capabilities immer vor Herstelleradaptern verwenden; insbesondere "vacuum.clean_area".
5. Heidi-Frontend nur gegen einen stabilen Heidi-Contract bauen, nicht direkt gegen Dreame-Details.
6. Config Flow, Options und Config-Entities für Einstellungen verwenden; SQLite nur für echte Fachdaten.
7. Haus-Modul als unabhängige berechnende Integration bauen und Fakten von gerätespezifischen Policies trennen.
8. Diagnostics, Repairs und Backup-Hooks als Pflichtbestandteil größerer Module aufnehmen.
9. Im Skill zuerst Daten-/Contract-Design, dann Mockup, dann Implementierung.
10. Grundsatzregeln maschinenprüfbar machen: Modulvertrag, Eigentumsregister und Architektur-Drift-Tests.

---

✅ Einigkeit

- eine fachliche Wahrheit je Wert
- reine Domainlogik
- keine Geschäftslogik in der Karte
- Ergebnisse als HA-Zustände sichtbar machen
- Fähigkeiten statt Modelle
- Haus-weite Logik aus Heidi herauslösen
- Tests vor Commit
- Doku und Code gemeinsam ändern
- große Oberflächen vorher mocken
- Heidi als Referenzfall nutzen, aber nicht migrieren

⚠️ Widerspruch / Änderung

- Eine zentrale SQLite-Datenbank für alle Einstellungen und Zustände: zu weitgehend.
- Datenaustausch ausschließlich über Entitäten: zu eng; Actions, Events und WebSocket gehören ebenfalls zum öffentlichen HA-Contract.
- Adapter je Hersteller: nur noch für nicht standardisierte Fähigkeiten.
- "command_line" Standardintervall 60 s: aktuell 30 s.
- keine "ha-*"-Frontendkomponenten: zu absolut; problematisch sind vor allem undokumentierte/interne Abhängigkeiten.
- Frontend erkennt Herstellergerät selbst: im Neubau sollte das Backend diese Abstraktion übernehmen.

❓ Rückfragen

Für Runde 2 würde ich nur noch drei Architekturentscheidungen explizit festzurren:

1. Soll "custom_components/heidi" ausschließlich über die bestehende Dreame-Integration arbeiten, also niemals selbst direkt mit Dreame-Cloud/API kommunizieren?
2. Soll das Haus-Modul ein eigenes Repo/eine eigene Integration werden, z. B. "custom_components/hausregeln", sodass Heidi, Luba, Pool und Lüftung ausschließlich dessen HA-Entitäten konsumieren?
3. Soll der Skill "modul-bauplan" einen maschinenlesbaren "module.yaml"/"architecture.yaml" als verpflichtendes Ergebnis erzeugen?

Meine Empfehlung wäre bei allen drei Punkten ja.Die zwei größten Änderungen gegenüber dem ursprünglichen Entwurf sind damit klar: Heidi direkt als Custom Integration neu bauen und „eine Quelle je Wert“ nicht mit „eine Datenbank für alles“ gleichsetzen.
