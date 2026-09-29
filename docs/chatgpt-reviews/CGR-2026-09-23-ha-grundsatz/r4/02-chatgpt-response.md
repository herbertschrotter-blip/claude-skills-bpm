# Review Runde 4

Claude,

**G-21 sollte als eigene allgemeine Regel aufgenommen werden.** Sie ist nicht bloß Teil von G-07, G-15 oder G-17:

- G-07 sagt, **wie Ergebnisse dargestellt werden**.
- G-15 regelt **Lebenszyklus/Reload**.
- G-17 regelt **Diagnose und Reparatur-Hinweise (Repairs)**.
- G-21 regelt dagegen das **fachliche Verhalten eines Moduls bei unvollständigen oder ausgefallenen Eingängen**.

Das ist eine eigene Architekturfrage und verdient eine eigene Regel.

## 1. G-21 – endgültige Formulierung

Den Vorschlag würde ich leicht ändern. „Trifft dann keine Entscheidung“ ist zu streng: Ein Modul darf weiter entscheiden, wenn die ausgefallene Quelle für diese konkrete Entscheidung nicht benötigt wird oder eine ausdrücklich definierte Ersatzregel existiert.

| Nr. | Regel | Prüfbar durch | ab |
|---|---|---|---|
| **G-21 Ausfall** | Ein Modul erkennt fehlende, deaktivierte, nicht verfügbare oder unzulässig alte Quellen und verwendet sie nicht stillschweigend als aktuelle Daten. Für jede benötigte Quelle ist festgelegt, welche Ergebnisse und Aktionen davon abhängen, welches Ersatz- oder Sperrverhalten gilt und wie nach Rückkehr neu bewertet wird. Betroffene Zustände zeigen den Ausfall korrekt; benutzerlösbare dauerhafte Fehler erhalten einen Reparatur-Hinweis. | Test je kritischer Quelle: fehlt/deaktiviert/`unavailable`/veraltet → keine unzulässige Aktion, korrekter sichtbarer Zustand; Quelle zurück → automatische Neubewertung und Erholung ohne Neustart. | **1**, vollständig dokumentiert ab **2** |

Das passt auch zur aktuellen HA-Praxis: Kann eine Integration Daten vom Gerät oder Dienst nicht mehr abrufen, soll die betroffene Entity `unavailable` werden statt den letzten Wert als scheinbar aktuell weiterzuführen. Wenn der Abruf funktioniert, aber nur ein einzelner Wert fehlt, ist dagegen `unknown` vorgesehen. :chatgpt-content-reference{index="0"}

---

## 2. `unavailable` oder letzten Wert behalten?

Nicht pauschal für das ganze Modul entscheiden, sondern **nach der Bedeutung jeder Ergebnis-Entity**.

| Situation | Verhalten |
|---|---|
| Aktueller Wert hängt von ausgefallener Quelle ab | `unavailable` |
| Quelle antwortet, konkreter Wert fehlt aber | `unknown` |
| Ergebnis hängt von der ausgefallenen Quelle gar nicht ab | normal verfügbar |
| Wert beschreibt ausdrücklich Vergangenheit, z. B. „letzte Reinigung“ | letzten gültigen Wert behalten |
| Ergebnis ist ein bekannter Ausfallzustand, z. B. „Automatik blockiert“ | Entity darf verfügbar bleiben und `blocked` + Grund liefern |
| Entscheidung benötigt ausgefallene kritische Quelle | Entscheidung nicht als gültiges positives Ergebnis ausgeben; Aktion sperren |
| Es existiert eine ausdrücklich definierte sichere Ersatzregel | Ersatzregel anwenden und erkennbar machen |

Wichtig ist also:

> **Letzten bekannten Wert nicht mit aktuellem Wert verwechseln.**

`sensor.letzte_reinigung = 09:42` bleibt sinnvoll, wenn der Roboter offline ist.

`sensor.aktueller_akku = 63 %` darf dagegen nicht so aussehen, als wären 63 % noch aktuell, wenn der Roboter nicht erreichbar ist.

Und bei einem Entscheidungssensor ist beispielsweise

```text
blocked
reason: robot_unavailable
```

ein **gültiger aktueller Zustand**: Wir wissen sicher, dass das Modul derzeit nicht entscheiden/ausführen darf.

Damit müssen nicht automatisch sämtliche Entities eines Moduls `unavailable` werden.

---

## 3. Keine universelle Ausfallzeit

Ich würde **keinen globalen Wert wie 5 oder 15 Minuten** in die Grundsatzregeln schreiben.

Drei Fälle sind zu unterscheiden:

### Explizites `unavailable`

Wenn HA bereits meldet:

```text
vacuum.xyz = unavailable
```

braucht das Roboter-Modul keine zusätzliche Wartezeit.

Die Quelle ist jetzt nicht verfügbar.

### Erwartete Aktualisierung bleibt aus

Bei Quellen, deren Aktualität fachlich relevant ist, braucht die Quelle eine eigene Frischegrenze:

```text
Wetterdaten:
max_age = ...

Positionsdaten:
max_age = ...

Anwesenheitsprognose:
max_age = ...
```

Diese Grenze ergibt sich aus der Fachbedeutung und Aktualisierungsrate der Quelle.

### Kurzzeitige Kommunikationsfehler

Polling-/API-Integrationen sollen Verbindungsfehler selbst behandeln und sich automatisch erholen. `DataUpdateCoordinator` unterstützt dieses Muster; bei Fehlern werden abhängige Coordinator-Entities entsprechend nicht verfügbar und bei erfolgreicher Aktualisierung wieder hergestellt. HA unterstützt inzwischen außerdem `retry_after` für kontrollierte Wiederholungen. :chatgpt-content-reference{index="1"}

Daher:

> **Kein globales „nach X Minuten ist Ausfall“.**

Stattdessen besitzt nur eine Quelle, bei der „zu alt“ fachlich relevant ist, eine definierte `max_age`/Frischegrenze.

---

## 4. Wann ein Reparatur-Hinweis?

Auch hier **nicht nach einer festen Zeit**.

Das ist wichtig: HA empfiehlt Reparatur-Hinweise ausdrücklich für Probleme, bei denen der Benutzer sinnvoll etwas tun kann. Ein Repair soll nicht bloß melden, dass gerade irgendetwas nicht funktioniert. :chatgpt-content-reference{index="2"}

Beispiele:

| Problem | Repair? |
|---|---:|
| Roboter 3 Minuten offline | ❌ |
| Wetterdienst vorübergehend nicht erreichbar | ❌ |
| Internet kurz weg | ❌ |
| konfigurierte Quell-Entity wurde gelöscht | ✅ |
| benötigte Entity dauerhaft deaktiviert | ✅ |
| ausgewählte `person.*` existiert nicht mehr | ✅ |
| Authentifizierung ungültig | eigener Reauth-Mechanismus |
| Gerät länger offline, Benutzer kann nichts außer warten | normalerweise ❌ |
| Konfiguration ist dauerhaft ungültig und Benutzer kann sie korrigieren | ✅ |

Die Unterscheidung lautet daher nicht primär:

```text
kurz ↔ dauerhaft
```

sondern:

```text
vorübergehender Betriebsfehler
        ↕
benutzerlösbarer Konfigurations-/Strukturfehler
```

Ein Zeitkriterium darf zusätzlich sinnvoll sein, ist aber **modulspezifisch**, nicht G-21-global.

---

## 5. Was passiert mit fälligen Befehlen?

Auch das darf G-21 nicht pauschal mit „verwerfen“ oder „nachholen“ beantworten.

Jeder zeitabhängige Auftrag braucht eine **Ausfallstrategie**.

Für geplante Vorgänge sind vier Varianten ausreichend:

| Strategie | Bedeutung |
|---|---|
| `drop` | nach verpasstem Zeitpunkt nicht mehr ausführen |
| `defer` | warten, solange der Auftrag noch gültig ist |
| `retry` | fehlgeschlagene technische Ausführung erneut versuchen |
| `fail` | Auftrag abbrechen und Fehler melden |

Für einen Roboterplan würde ich standardmäßig **`defer + re_evaluate`** verwenden:

```text
Reinigung um 10:00 fällig
        ↓
Roboter unavailable
        ↓
Auftrag bleibt fällig/blockiert
        ↓
Roboter wieder verfügbar
        ↓
ALLE Bedingungen neu prüfen
        ↓
noch innerhalb des zulässigen Fensters?
Anwesenheit?
Ruhezeit?
Akku?
Plan noch aktiv?
        ↓
erst dann eventuell starten
```

Ganz wichtig:

> **Nach einem Ausfall wird nicht einfach der alte Entschluss ausgeführt, sondern mit aktuellen Daten neu entschieden.**

Das ist für den Planer wesentlich sicherer als eine Warteschlange alter Gerätebefehle.

Ein manueller Action-Aufruf verhält sich anders: Kann er jetzt nicht ausgeführt werden, soll er fehlschlagen und einen verständlichen Fehler liefern. HA verlangt für fehlgeschlagene Actions entsprechende Exceptions; Kommunikationsfehler werden als `HomeAssistantError` gemeldet. :chatgpt-content-reference{index="3"}

---

## 6. Stufe 0–1

Ich würde G-21 deshalb **ab Stufe 1** gelten lassen.

### Stufe 0 – nur vorhandenes HA

Keine eigene Logik:

> Ausfallverhalten liegt bei der verwendeten HA-Integration.

Keine zusätzliche Pflicht.

### Stufe 1 – Template/Automation/Script

Sobald Herbert eigene Entscheidungen baut, muss mindestens gelten:

```text
Quelle unknown/unavailable?
        ↓
keine gefährliche/falsche Aktion
```

Beispiel:

Eine Automation darf `unavailable` nicht versehentlich durch Typumwandlung als `0`, `false` oder einen sonstigen gültigen Fachwert interpretieren.

Dafür braucht Stufe 1 aber **kein `module.yaml` und keine Repairs-Infrastruktur**.

### Ab Stufe 2

Volle G-21:

- Quellen klassifizieren;
- Abhängigkeiten definieren;
- Frische festlegen, wenn relevant;
- Sperr-/Fallback-Verhalten;
- Recovery;
- Auftragsstrategie;
- Tests;
- ggf. Repair.

---

# 7. `module.yaml` – Ausfallverhalten

Ich würde das **je Quelle** beschreiben, aber klein halten.

```yaml
schema: 1

module:
  id: planer
  level: 3
  type: integration

sources:
  - key: robot
    owner: dreame_vacuum
    interface: entities
    outage:
      critical_for:
        - decision
        - run_plan
      on_unavailable: block
      recovery: re_evaluate
      repair: user_actionable_only

  - key: house
    owner: haus
    interface: entities
    outage:
      critical_for:
        - automatic_start
      on_unavailable: block
      recovery: re_evaluate
      repair: user_actionable_only

  - key: weather
    owner: weather
    interface: entity
    outage:
      critical_for:
        - ventilation_decision
      max_age: PT30M
      on_unavailable: block
      recovery: re_evaluate
      repair: user_actionable_only

owns:
  entities:
    - key: decision
      domain: sensor

  actions:
    - run_plan

failure_policy:
  scheduled:
    strategy: defer
    on_recovery: re_evaluate
  manual:
    strategy: fail
```

`max_age` ist **optional**.

Beim Roboter brauchen wir es normalerweise nicht, wenn die Dreame-Entity selbst korrekt `unavailable` meldet.

Bei Wetterdaten oder anderen Quellen, die technisch noch einen Wert besitzen können, obwohl dieser fachlich zu alt ist, kann `max_age` sinnvoll sein.

`critical_for` verhindert außerdem einen zu groben Fehler im Modell:

> Nicht jede ausgefallene Quelle legt automatisch das gesamte Modul lahm.

---

# 8. Eine kleine Änderung am ursprünglichen Vorschlag

Diese Formulierung:

> „trifft dann keine Entscheidung auf veralteten Daten“

würde ich ersetzen durch:

> **„verwendet ausgefallene oder unzulässig alte Quellen nicht stillschweigend als aktuelle Daten.“**

Das ist präziser.

Denn ein Modul darf bei einem Ausfall durchaus entscheiden:

```text
Entscheidung = blockiert
Grund = Roboter nicht verfügbar
```

oder:

```text
Lüftung = nicht automatisch verändern
Grund = Wetterdaten fehlen
```

Das sind sogar sehr wichtige Entscheidungen.

Was verboten werden soll, ist:

```text
letzter Wetterwert = 5 °C
↓
Wetterquelle seit 8 Stunden tot
↓
Modul behandelt 5 °C weiterhin als aktuelle Außentemperatur
```

---

# 9. Zusammenspiel mit G-07, G-15 und G-17

G-21 bleibt eigenständig, verweist aber auf die drei bestehenden Regeln:

```text
G-21 erkennt und behandelt den Ausfall
   │
   ├── G-07 → wie betroffene Zustände als Entities erscheinen
   │
   ├── G-15 → automatische technische Erholung / Reload-Lebenszyklus
   │
   └── G-17 → Diagnose und ggf. Repair
```

Damit gibt es keine unnötige Doppelung.

HA selbst verfolgt dieselbe Richtung: Die Integration Quality Scale fordert sowohl korrektes `unavailable`-Verhalten als auch automatische Erholung von Verbindungsproblemen; Setup-Probleme durch vorübergehend nicht erreichbare Geräte sollen automatisch erneut versucht werden, ohne HA-Neustart. :chatgpt-content-reference{index="4"}

---

# 10. Endfassung G-21

Für die Grundsatzdoku würde ich exakt diese Kurzfassung verwenden:

| Nr. | Regel | Prüfbar durch | ab |
|---|---|---|---|
| **G-21 Ausfall** | **Ein Modul erkennt fehlende, deaktivierte, nicht verfügbare oder unzulässig alte Quellen und verwendet sie nicht stillschweigend als aktuelle Daten. Für benötigte Quellen sind Sperr-/Ersatzverhalten und Wiederanlauf festgelegt; betroffene Zustände zeigen den Ausfall korrekt, und benutzerlösbare dauerhafte Fehler erhalten einen Reparatur-Hinweis.** | **Ausfalltest je kritischer Quelle: Quelle fehlt/deaktiviert/`unavailable`/veraltet → keine unzulässige Aktion und sichtbarer korrekter Zustand; Quelle zurück → automatische Neubewertung und Erholung ohne Neustart.** | **1; vollständiger Vertrag ab 2** |

Im erläuternden Text direkt darunter gehören vier Unterregeln:

1. **Aktualität:** Aktuelle Werte nicht aus veralteten Daten vortäuschen; historische Werte dürfen bestehen bleiben.
2. **Frische:** Keine globale Ausfallzeit; `max_age` nur je Quelle, wenn fachlich erforderlich.
3. **Repair:** Nur für benutzerlösbare Probleme, nicht als Offline-Timer.
4. **Aufträge:** `drop`, `defer`, `retry` oder `fail` festlegen; nach Wiederkehr bei fachlichen Entscheidungen grundsätzlich neu bewerten.

Damit ist G-21 allgemein genug für Roboter, `haus`, Pool, Lüftung, Wetter und spätere Module, ohne ihnen dasselbe Ausfallverhalten aufzuzwingen.

# ✅ Einigkeit

- G-21 wird als **eigene Regel** aufgenommen.
- Sie gilt in abgeschwächter Form bereits **ab Stufe 1**, vollständig ab Stufe 2.
- Kein stilles Weiterrechnen mit veralteten kritischen Daten.
- Nicht pauschal alle Modul-Entities `unavailable`.
- Aktuelle abhängige Werte → `unavailable`; fehlender Einzelwert bei erfolgreichem Abruf → `unknown`; historische Werte dürfen ihren letzten gültigen Zustand behalten. :chatgpt-content-reference{index="5"}
- Keine allgemeine „5-Minuten-Regel“.
- Frischegrenzen werden nur dort je Quelle definiert, wo sie fachlich nötig sind.
- Repairs nur bei sinnvoll benutzerlösbaren Problemen. :chatgpt-content-reference{index="6"}
- Fällige Aufträge besitzen eine explizite Strategie.
- Nach Rückkehr einer Quelle werden fachliche Entscheidungen neu bewertet.
- `module.yaml` dokumentiert Ausfallverhalten je Quelle; Auftragsverhalten liegt auf Modulebene.

# ⚠️ Widerspruch

Nur eine Präzisierung gegenüber dem ursprünglichen Vorschlag:

**„Bei Ausfall keine Entscheidung“ ist zu streng.** Richtig ist: **keine Entscheidung oder Aktion, die eine ausgefallene/veraltete kritische Quelle stillschweigend als gültig voraussetzt.** Ein explizites `blocked`, ein definierter sicherer Fallback oder eine von der Quelle unabhängige Entscheidung bleiben erlaubt.

# ❓ Rückfragen

**Keine.**

Mit G-21 in dieser Fassung ist die Regelserie aus meiner Sicht vollständig genug für die Grundsatzdokumentation und den Skill.

**Serie abschließbar.**
