Die Neutralitäts-Checkliste nehme ich als verbindlichen Maßstab; insbesondere Handlung statt Werkzeug, Profil-Fallback und die Split-Regel sind für die folgenden Vorschläge maßgeblich. :chatgpt-content-reference{index="0"}

# Review Runde 1

## Gesamturteil

Deine Gegenanalyse ist substanziell stärker als mein Ausgangsbefund. Nach Prüfung der aktuellen Dateien in `claude-skills-bpm/main`, `BauProjektManager/main`, `HA_Dash_DreameX60/main` und `herbert-smarthome/dreame_x60` halte ich den Kern deiner Diagnose für richtig:

**Das Hauptproblem ist nicht mehr die Qualität einzelner Skills, sondern dass die Systemarchitektur der Skills ihren eigenen Umbauten hinterherhinkt.**

Besonders schwer wiegen dabei drei Punkte:

1. Der im September eingeführte **Profil-Vertrag existiert in den Skills, aber in den heute aktiven Projekten praktisch nicht mehr**.
2. Viele Querschnittsregeln liegen mehrfach in Skills, obwohl sie inzwischen überwiegend Claude-Code-Infrastruktur betreffen.
3. `skill-pflege` schützt den Wortlaut stärker als die Semantik und verhindert damit die Konsolidierung, die das System jetzt braucht.

Ich korrigiere meinen Ausgangsbefund bei A11, A13 und A20 ausdrücklich.

---

# 1. Teil A – Prüfung der strittigen Befunde

## A11 – `cc-steuerung`

### Urteil: ✅ Dein Einwand ist richtig; mein ursprünglicher Fix war falsch

Mein Vorschlag, generische Bestätigungen wie `ok`, `passt`, `mach` in die Description aufzunehmen, wäre ein Fehler.

Die aktuelle Description von `skills/cc-steuerung/SKILL.md` ist schon problematisch genug:

> `Use when users explicitly say "cc", "dc", "Claude Code", ...`

Der Body definiert dagegen ab Abschnitt `## 2. WANN WAS EINSETZEN`:

> DC ist Default-Ausführungsmodus sobald der User das Konzept freigegeben hat (`code bitte`, `mach`, `ok`, `ausführen`).

Diese Body-Regel kann nur wirken, **wenn der Skill bereits geladen wurde**. Deshalb war die Architektur schon im April logisch asymmetrisch.

Der damalige Smoke-Run vom 28.04. zeigt zwar, dass `cc + Fachskill` damals hervorragend funktionierte: CC-06 bis CC-11 waren 6/6 PASS. Das beweist aber nur, dass der explizite Multi-Trigger damals funktionierte. Es rechtfertigt nicht, `cc-steuerung` heute in Claude Code weiter mitzuschleppen.

### Heute schwerwiegender

Der Skill enthält:

- Desktop-Commander-Werkzeugnamen
- `tool_search`
- `ask_user_input_v0`
- `bash_tool`
- Claude.ai-Artifact-Sonderfälle
- OneDrive-Autodiscovery
- eine nicht mehr vorhandene INDEX-Struktur `PCs und Arbeitsverzeichnisse`
- `git push` grundsätzlich verboten

Das alles ist in einer Claude-Code-Sitzung entweder irrelevant oder falsch.

Beispiel:

`skills/cc-steuerung/SKILL.md`, Abschnitt `## 8. BERECHTIGUNGEN`:

> `git push | ❌ Nie | User pusht selbst`

Aktuelles Heidi dagegen:

`HA_Dash_DreameX60/CLAUDE.md`, `## Arbeitsweise`:

> Am Ende einer Sitzung: `docs/STATUS.md` nachziehen, committen, hochladen.

Das ist keine Modalitätsregel. Das ist Projektpolitik.

### Empfehlung

`cc-steuerung` **nicht mehr als allgemeinen Modalitäts-Skill behandeln**.

Ich sehe zwei sinnvolle Varianten:

**Variante A – bevorzugt:** Skill deaktivieren/aus dem aktiven Claude-Code-Skillset entfernen.

**Variante B:** auf einen kleinen **Cowork/Desktop-Commander-Adapter** reduzieren:

```text
cc-steuerung/
├── SKILL.md             ~80–120 Zeilen
└── references/
    └── desktop-commander.md
```

Description nur:

> Use when the current environment is Claude.ai/Cowork and the user explicitly requests Desktop Commander or direct PC execution through DC.

`Claude Code` darf dann **kein Trigger mehr sein**.

Damit entfällt auch die falsche Idee, `cc-steuerung` müsse anderen Fachskills erklären, wie Claude Code arbeitet.

---

# 2. A13 – Push-Prüfung in `chatgpt-review`

### Urteil: ✅ Du hast recht; meine Kritik ziehe ich zurück

`skills/chatgpt-review/SKILL.md`, Abschnitt `## ChatGPTs Repo-Zugriff` verlangt den Repo-Zugriffsblock **in jedem Review-Prompt**.

Damit ist die Push-Prüfung funktional begründet: Wenn ChatGPT aufgefordert wird, GitHub selbst als Belegquelle zu verwenden, muss geprüft werden, ob das dort sichtbare Repo überhaupt dem lokalen Stand entspricht.

Die richtige Trennung lautet:

- **Push-Stand prüfen:** immer, solange jeder Prompt Repo-Zugriff enthält.
- **Push tatsächlich ausführen:** ausschließlich gemäß Projektregel/Profil.
- Bei lokalem Vorsprung: Auswahl zwischen pushen, im Prompt auf den abweichenden Stand hinweisen oder abbrechen.

Die Push-Prüfung gehört also zu `chatgpt-review`; die **Push-Berechtigung** gehört nicht dorthin.

Das ist ein wichtiger Unterschied.

---

# 3. A20 – `ticket`

### Urteil: ❌ Mein Ausgangsbefund war falsch

Deine Korrektur ist bestätigt.

`skills/ticket/SKILL.md` hat bereits:

- optionales Überspringen einer Tracker-Aufgabe, sofern Profil/Entscheidung dies zulässt,
- Statusfolge mit `geloest`,
- danach explizite User-Prüfung,
- erst danach `geschlossen`.

Das alte Heidi-`Ticket-Profil` bestätigt zusätzlich:

```text
neu → angenommen → in_arbeit → geloest → geschlossen
```

und:

> geschlossen erst nach Herberts Prüfung

Damit ist semantisch bereits:

```text
reported
→ accepted
→ working
→ fixed/geloest
→ user verification
→ closed
```

Meine Kritik an der Zustandsfolge war unbegründet.

Allenfalls würde ich `geloest` sprachlich als `behoben` bezeichnen, weil „gelöst“ für Menschen häufig schon wie der Endzustand klingt. Das ist aber Naming, kein Workflow-Fehler.

---

# 4. Teil B – E1 bis E10

## E1 🔴 Profil-Vertrag ohne Abnehmer

### Urteil: ✅ vollständig bestätigt und noch zentraler als in meinem Ausgangsbefund

Der Beleg ist sehr deutlich.

### BPM aktuell

`BauProjektManager/CLAUDE.md`, `main` enthält:

- Projekt
- Architektur
- Coding Standards
- Git-Regeln
- Links zu ausführlichen Standards

Aber **keinen**:

- `## Commit-Profil`
- `## Code-Profil`
- `## Doku-Profil`
- `## Tracker-Profil`
- `## Mockup-Profil`
- `## Review-Profil`

### Heidi alt

`herbert-smarthome/CLAUDE.md`, Branch `dreame_x60` enthält tatsächlich die vollständige September-Architektur:

- Commit-Profil
- Tracker-Profil
- Ticket-Profil
- Code-Profil
- Doku-Profil
- Mockup-Profil
- Review-Profil

### Heidi aktuell

`HA_Dash_DreameX60/CLAUDE.md`, `main` enthält dieselben Fachinformationen überwiegend als normale Abschnitte:

- `## Commits`
- `## Aufgaben und Tickets`
- `## Arbeitsweise`

aber nicht mehr im Skill-Profilvertrag.

Die Skills suchen also strukturierte Verträge, während das aktive Projekt die Fakten wieder in menschenlesbarer Prosa führt.

Das ist tatsächlich **🔴**, nicht 🟡.

Zusätzlich sind die Fallbacks gefährlich: Sie halten den Betrieb aufrecht und verschleiern dadurch, dass der Vertrag nicht mehr erfüllt ist.

---

## E2 🔴 Querschnittsregeln in Kopien

### Urteil: ✅ bestätigt

Das Problem ist nicht nur Tokenmenge, sondern **Divergenzrisiko**.

Beispiele:

- Branch-Ermittlung
- Auswahlfragen
- Arbeitsverzeichnis
- Cowork/Claude-Code-Weichen
- Artifact-Regeln
- Commit-/Push-Verhalten

werden mehrfach beschrieben.

Besonders klar ist der Effekt bei `skill-pflege`:

Regel 12a sagt:

> Commit und Push gehören zu jeder Skill-Änderung.

Direkt danach steht:

> KEINE Download-Datei ... Kein `present_files` ...

Regel 13a/14 verlangt dagegen anschließend ausdrücklich:

> `create_file` + `present_files`

Genau so entsteht ein Widerspruch durch additive Evolution.

Deine Ursache „Regel 19 + nie kürzen“ ist plausibel und durch den Skill selbst belegt.

---

## E3 🔴 `cc-steuerung`

### Urteil: ✅ bestätigt

Siehe A11.

Zusätzlich bestätige ich den toten Infrastrukturverweis:

`cc-steuerung`, Abschnitt `4.2` erwartet in `INDEX.md`:

> `PCs und Arbeitsverzeichnisse`

Der aktuelle Skills-Repo-INDEX enthält diesen Abschnitt nicht.

BPMs INDEX enthält zwar konkrete Arbeitsverzeichnisse unter `Projekt-Metadaten`, aber nicht das erwartete PC-Registry-Schema.

Für aktuelles Heidi liegt das Repo explizit unter:

`C:\Users\herbe\source\HA_Dash_DreameX60`

und gerade nicht unter dem OneDrive-Modell des Skills.

Das ist keine kleine Alterung, sondern der Adapter beschreibt eine nicht mehr gültige Infrastruktur.

---

## E4 🟠 Unerreichbare `doc-pflege`-Teile

### Urteil: ✅ bestätigt

`doc-pflege` Modus 3:

> Passive Advisory – wenn `code-erstellen` DocMaintenanceHints ausgegeben hat.

Modus 4:

> Automatischer Checkpoint (Advisory).

Gleichzeitig grenzt die Description automatische Post-Change-Fälle aus und `code-erstellen` produziert seine Doc-Hinweise bereits selbst.

Das sind damit keine eigenständigen, von außen erreichbaren Fähigkeiten des `doc-pflege`-Skills.

### Empfehlung

Streichen als öffentliche Modi.

Was übrig bleibt:

- explizites Dokumentieren
- Erstellen/Ändern
- Struktur-/Indexpflege
- Sitzungsdokumentation, falls noch nötig
- keine read-only Validierung

Interne Post-Write-Validierung ist kein eigener Modus.

---

## E5 🟠 Konkurrenz zu eingebauten Skills fehlt

### Urteil: ✅ bestätigt

Besonders kritisch:

```text
skill-creator ↔ skill-neu
skill-creator ↔ skill-pflege
code-review ↔ audit
```

Der im Repo hinterlegte Anthropic-`skill-creator` beschreibt sich selbst als:

> Create new skills, modify and improve existing skills, and measure skill performance.

Das überschneidet sich nahezu vollständig mit `skill-neu` und teilweise mit `skill-pflege`.

Hier reicht kein Namenscheck.

Der neue Skill-Erstellungsworkflow muss **Description-Kollisionen mit allen aktuell geladenen Skills** prüfen.

Dasselbe gilt für `modul-bauplan ↔ audit`.

---

## E6 🟠 Fragepflicht erzeugt Kaskaden

### Urteil: ✅ bestätigt

Die problematische Regel ist nicht:

> Wenn du eine feste Auswahl fragst, nutze das Auswahlwerkzeug.

Sondern:

> Bei JEDER Entscheidung MUSS gefragt werden.

Diese beiden Aussagen sind grundverschieden.

Die neue Grundregel sollte lauten:

> **Entscheidungen nur dann an den User delegieren, wenn sie nicht bereits durch Auftrag, Projektprofil, bestehenden Standard oder eindeutigen Kontext festgelegt sind. Wenn eine echte Auswahl verbleibt, nutze das Auswahlwerkzeug der Umgebung.**

Das entfernt unnötige Fragen, ohne Benutzerkontrolle zu verlieren.

Beispiel:

Wenn das Profil sagt:

```text
Push: erlaubt
Branch: main
```

ist keine Branch-/Push-Frage nötig.

Wenn zwei sinnvolle Vorgehensweisen existieren und keine Präferenz feststeht, dann Auswahlfrage.

---

## E7 🟠 `Bauplan` als Triggerkonflikt

### Urteil: ✅ bestätigt

Sowohl `audit` als auch `doc-pflege` tragen projektspezifische Begriffe direkt in ihren Descriptions.

Das ist ohnehin gegen die eigene Neutralitätsrichtung.

Mit `modul-bauplan` wird es zusätzlich funktional gefährlich.

Ich würde die Grenze so ziehen:

```text
modul-bauplan
= fachlicher Lebenszyklus eines HA-Moduls:
  planen → fachlich gegen Grundsatz/Plan prüfen → nachschlagen

audit
= systemweite Konsistenzprüfung:
  Projektregeln ↔ Doku ↔ Code ↔ Tracker ↔ Profile
```

Also:

> „Prüfe Modul X gegen seinen Bauplan/Grundsatz“ → `modul-bauplan`

> „Prüfe, ob Status, Doku, Code und Aufgabenquelle konsistent sind“ → `audit`

`Bauplan` selbst gehört aus den generischen Descriptions heraus.

---

## E8 🟡 Skill-Repo verwendet eigene Profile nicht

### Urteil: ✅ Kernbefund bestätigt, eine Detailkorrektur

`claude-skills-bpm/CLAUDE.md` enthält aktuell nur das `Review-Profil`.

Kein Commit-, Code-, Doku- oder Tracker-Profil.

Das ist inkonsistent mit den Fähigkeiten, die die eigenen Skills verlangen.

Zum CHANGELOG habe ich separat den aktuellen Inhalt geprüft:

```text
v0.35.2: 0
v0.35.3: 0
v0.35.4: 0
v0.36.1–v0.36.7: jeweils 0
```

Damit ist die Lücke bestätigt.

Eine Korrektur zu deinem Detail:

**`v0.36.0` kommt im aktuellen CHANGELOG nur einmal vor**, nicht zweimal.

Falls die doppelte Vergabe aus Git-Commits/Tags stammt, ist sie nicht im aktuellen CHANGELOG sichtbar. Diesen Teil würde ich daher ohne Git-Historienbeleg nicht als bestätigt übernehmen.

---

## E9 🟠 Querverweise tot / Kreis / einseitig / nummerngebunden

### Urteil: ✅ weitgehend bestätigt

Konkrete Belege:

`doc-pflege`, Modus 0:

> `references/projekt-init.md` (falls vorhanden)

Die Datei existiert nicht.

`code-erstellen`, Auto-Anker:

> siehe tracker-Skill Kapitel "Chat-Anker-System"

Im Tracker-Kern gibt es kein solches Kapitel mehr; die Master-Spec liegt in:

`skills/tracker/references/anker-system.md`.

`tracker/SKILL.md` hat `clickup-tools.md` zwar im Querverweis, aber nicht in der eigentlichen Kommando→Reference-Routingtabelle. Das ist zumindest strukturell unsauber.

Und der größere Punkt stimmt:

**Nummerierte Cross-Skill-Verweise sind Refactor-Hemmer.**

Also nicht:

> `skill-pflege Regel 21`

sondern:

> `skill-pflege → Abschnitt "Split-Prüfung"`

noch besser:

> `skill-pflege → references/refactor.md#split-policy`

Stabile semantische IDs sind besser als Positionsnummern.

---

## E10 🟡 Zwei Lieferwege

### Urteil: ✅ Problem bestätigt; direkte Claude-Code-Bereitstellung ist offiziell unterstützt

Anthropic dokumentiert aktuell ausdrücklich:

- persönliche Skills unter `~/.claude/skills/`
- Projektskills unter `.claude/skills/`
- Claude Code entdeckt diese automatisch
- ein Upload über claude.ai ist dafür nicht erforderlich.

Damit ist die Grundidee richtig:

**Für Claude Code muss der claude.ai-Upload nicht der primäre Auslieferungsweg sein.**

Ich würde allerdings einen Symlink/Junction **nicht ohne Test zur Architekturregel machen**, weil die offizielle Dokumentation die Verzeichnisse dokumentiert, aber nicht garantiert, wie alle Skill-Discovery-Pfade mit Windows-Junctions/Symlinks umgehen.

Ziel:

```text
Repo = Source of Truth
        ↓
~/.claude/skills/<skill>/
```

Wie synchronisiert wird:

- Kopierskript,
- Junction,
- Plugin,
- oder Repo direkt dort,

kann separat entschieden und getestet werden.

Dann wird Cowork nur noch eine zweite Distribution, nicht mehr der Grund, warum jeder Skill 100+ Zeilen Artifact-Mechanik trägt.

Anthropic betont außerdem inzwischen, dass prozedurale Workflows in Skills und nicht pauschal in CLAUDE.md gehören sollen. Das ist für E2 wichtig: Wir sollten Querschnitt nicht einfach komplett aus Skills in CLAUDE.md verschieben.

---

# 5. Was zusätzlich fehlt

Ich sehe noch vier Punkte.

## F1 🔴 Profile brauchen Versionierung

Selbst wenn wir Profile wieder einführen, fehlt bisher ein Schema-Level.

Ohne:

```text
Profil-Version: 1
```

kann ein Skill nicht erkennen:

> Projekt hat ein altes Profilformat.

Das ist genau der Fehler, der im September passiert ist: Profil existiert konzeptionell, aber niemand erkennt Drift.

---

## F2 🟠 Profile und Projekt-Doku sind momentan doppelte Wahrheit

Beispiel aktuelles Heidi:

`CLAUDE.md` beschreibt bereits:

- Tests
- Commitformat
- Versionierung
- Docs
- Deployment
- ClickUp
- Tickets

Wenn wir daneben sieben lange Profilabschnitte wiederherstellen, entsteht erneut doppelte Doku.

Der Profil-Vertrag darf daher **keine zweite Beschreibung des Projekts** sein.

Er sollte nur maschinenlesbare Skill-Eingaben enthalten und ansonsten auf bestehende Abschnitte verweisen.

---

## F3 🟠 `INDEX.md` sollte kein zweites Regelbuch mehr sein

Aktuell ist der Skills-INDEX zugleich:

- Skillverzeichnis
- Routingmatrix
- Konfliktmatrix
- globale Invarianten
- Projektarchitektur
- historische Refactorregeln
- Betriebsregeln

Dadurch ist Drift zwangsläufig.

INDEX sollte künftig hauptsächlich sein:

```text
Inventar
+ Routing
+ Konfliktmatrix
+ Links zu den wirklichen Regelquellen
```

Nicht 10 zusätzliche globale Workflow-Spezifikationen.

---

## F4 🟠 „Projektneutral“ braucht eine klare Bedeutung

Der Begriff sollte definiert werden als:

> Der Skill enthält keine Projektwerte. Er definiert einen generischen Vertrag und liest konkrete Werte aus dem aktuellen Projekt.

Nicht:

> Der Skill hat BPM- und Heidi-Fallbacks und funktioniert deshalb in mehreren Projekten.

Das heutige System ist teilweise noch letzteres.

---

# 6. Profil-Vertrag – Empfehlung

Von deinen drei Varianten empfehle ich **keine in Reinform**.

Ich empfehle:

# Ein strikter `## Skill-Profil`-Block mit typisierten Unterabschnitten

Also:

```markdown
## Skill-Profil
Profil-Version: 1

### Projekt
...

### Commit
...

### Code
...

### Doku
...

### Tracker
...

### Mockup
...

### Review
...

### Ticket
...
```

Warum besser als sieben `## X-Profil`-Top-Level-Abschnitte?

- ein Einstiegspunkt
- leicht validierbar
- lässt sich komplett finden
- weniger Top-Level-Lärm
- alle Skills teilen dieselbe Vertragsversion
- Unterbereiche können optional sein

Warum nicht tolerant in freier Prosa?

Weil dann kein Contract existiert.

Der heutige Heidi-Fall demonstriert genau das: Alle Fakten sind vorhanden, aber die Skills können sie nicht deterministisch konsumieren.

---

## Minimaler Feldsatz

### Kopf

```text
Profil-Version
Projekt-ID
Repo
Standard-Branch
```

### Commit

```text
Format
Module
Versionsquelle
Versionsregel
Push-Policy
Tests-vor-Commit
```

`Push-Policy` z.B.:

```text
manual
allowed
required-after-session
```

Nicht Boolean.

### Code

```text
Stacks
Pflichtkontext
Aufgabenquelle
Architekturregeln
Testbefehle
Auslieferung
Mockup-Pflicht
```

### Doku

```text
Router
Pflichtdokumente
Dokumenttypen
Validierungsquelle
Sitzungsabschluss
Entscheidungs-/Befundort
```

Wichtig:

Nicht die Validierungsregeln selbst hineinkopieren, wenn sie schon in `docs/...` stehen.

Besser:

```text
Validierungsquelle: docs/HAUSREGELN.md Abschnitt ...
```

### Tracker

```text
Provider
Projekt-Config
Aufgabenquelle
Nummernschema
Statusmodell
```

IDs bleiben weiter in `projects/<projekt>/`, sofern das sinnvoll ist.

### Mockup

```text
Ablage
Designquelle
Pflichtansichten
Abnahmeort
```

### Review

```text
Ablage
Repo/Branches
Kontextquellen
Ergebnisort
Pflichtregeln
```

### Ticket

nur wenn das Projekt ein Ticketsystem hat:

```text
Quelle
Statusmodell
Schreibweg
Tracker-Kopplung
Prüfung/Abnahme
```

---

## Was passiert bei fehlenden Feldern?

Nicht mehr:

> Profil fehlt → gesamtes Profil anlegen?

sondern feldbezogen.

Beispiel:

`git-commit-helper` braucht gerade:

```text
Versionsquelle
Push-Policy
Commitformat
```

Fehlt nur `Push-Policy`:

> Dieser Commit benötigt `Commit.Push-Policy`; Wert fehlt.

Dann Auswahl:

```text
Profil ergänzen
Für diese Aktion einmalig festlegen
Abbrechen
```

Keine Vollprofil-Frage.

---

## Wer validiert das?

Zwei Ebenen.

### Laufzeit

Jeder Skill prüft nur seine **Required Inputs**.

Beispiel:

```text
git-commit-helper:
requires Commit.Format
requires Commit.Versionsregel
requires Commit.Push-Policy
```

### Systemaudit

`audit` bekommt ein eigenes Modul:

```text
Profil-Vertrag
```

Prüft:

- Profil-Version unterstützt?
- benötigte Bereiche vorhanden?
- referenzierte Dateien vorhanden?
- Werte widersprechen Projekt-CLAUDE.md?
- veraltete Pfade?
- unbekannte Felder?
- Skill verlangt Feld, das Schema nicht kennt?

Optional zusätzlich ein deterministisches Script:

```text
scripts/validate-skill-profile.*
```

Das wäre zuverlässiger als reine Promptlogik.

---

# 7. `skill-pflege` neu – Safe Patch / Refactor

Hier würde ich den größten konzeptionellen Umbau machen.

## Modus A – Safe Patch

Zweck:

> Eine kleine bekannte Regel ändern, ohne unbeabsichtigte Seiteneffekte.

Regeln:

- Original zuerst lesen.
- Nur explizit betroffene Stellen ändern.
- Keine benachbarten Regeln „nebenbei verbessern“.
- Semantische Auswirkungen nennen.
- Querverweise prüfen.
- Description nur ändern, wenn Trigger betroffen sind.
- Nach Änderung relevante Evals laufen lassen.

Hier darf die alte konservative Philosophie teilweise bleiben.

---

## Modus B – Refactor

Zweck:

> Struktur verbessern, Redundanz entfernen, Regeln zusammenführen, Inhalte in References verschieben und Altlasten löschen, ohne unbeabsichtigten Regelverlust.

Hier gelten die alten Regeln 1–5 **nicht**.

Stattdessen gibt es ein Regel-Inventar.

---

# Regel-Inventar

## Vorher

Jede normative Aussage bekommt eine temporäre Review-ID:

```text
R01 | Auswahlfragen nur bei echter offener Entscheidung
R02 | Branch nie hartkodieren
R03 | Description max. 1024 Zeichen
R04 | Skill-Änderung benötigt Eval
R05 | Cowork-Artifact braucht exakten Dateinamen
...
```

Nicht jeder Absatz – jede **Regel**.

Tabelle:

| ID | Ursprungsort | Semantik | Ziel |
|---|---|---|---|
| R01 | Kernregel Auswahlfrage | Nur offene Entscheidungen fragen | behalten |
| R02 | Branch-Ermittlung | Branch aus Umgebung ermitteln | zusammenführen |
| R03 | Regel 6 | Description ≤1024 | behalten |
| R04 | Prozess | Eval nach Triggeränderung | nach reference |
| R05 | Regel 13a | Cowork Artifact-Mechanik | Cowork-Adapter |

---

## Nachher

| ID | Ergebnis | Neuer Ort | Begründung |
|---|---|---|---|
| R01 | behalten, neu formuliert | SKILL.md Kern | universell |
| R02 | zusammengeführt mit R09 | SKILL.md Kern | doppelte Branch-Regel |
| R03 | behalten | SKILL.md | Trigger-Invariante |
| R04 | verschoben | `references/eval.md` | Detailablauf |
| R05 | verschoben | `references/cowork.md` | umgebungsspezifisch |
| R06 | gestrichen | — | obsolete Artifact-Regel, User-Freigabe #… |

### Zulässige Zustände

```text
KEEP
MOVE
MERGE
REWRITE
DROP
```

`DROP` benötigt explizite Freigabe.

`MERGE` muss Ursprungs-IDs nennen.

Damit wird **Regelverlust messbar**, ohne jeden historischen Satz mitzuschleppen.

---

# Was bleibt von den alten harten Regeln 1–6?

## Regel 1 „Original zeilengenau übernehmen“

**Safe Patch:** abgeschwächt behalten.

**Refactor:** streichen.

Ersetzen durch:

> Erfasse vor einem Refactor alle normativen Regeln und überprüfe ihre Behandlung im Regel-Inventar.

---

## Regel 2 „Nichts löschen“

**Safe Patch:** behalten.

**Refactor:** ersetzen:

> Normative Regel nur löschen, wenn sie im Inventar als DROP dokumentiert und freigegeben wurde. Redundanter oder veralteter erklärender Text darf entfernt werden.

---

## Regel 3 „Nichts kürzen“

Streichen.

Kein sinnvoller Schutzmechanismus.

---

## Regel 4 „Nichts umformulieren“

Streichen.

Ersetzen durch semantische Äquivalenzprüfung.

---

## Regel 5 „Struktur nicht ändern“

Für Safe Patch sinnvoll.

Für Refactor genau falsch.

---

## Regel 6 „Frontmatter nicht anfassen“

Ersetzen:

> Frontmatter nur ändern, wenn Trigger/Zuständigkeit betroffen sind. Nach jeder Änderung Description-Limit und Trigger-Evals prüfen.

---

# Was wird aus Regel 19 „Eigenständig bleiben“?

Die aktuelle Regel ist zu stark.

Neu:

> **Self-contained contract, not duplicated implementation.**  
> Ein Skill muss Zweck, Triggergrenzen, erforderliche Inputs und Kerninvarianten selbst verstehen lassen. Gemeinsame oder umgebungsspezifische Detailabläufe dürfen referenziert werden, sofern ein klarer Fallback existiert.

Das verhindert sowohl:

- 11 Kopien derselben Regel,
- als auch Skills, die ohne fünf andere Dateien unverständlich sind.

---

# 8. Querschnittsregeln – wohin genau?

Ich widerspreche einem Teil deines Zielbildes:

**Nicht alle Grundregeln sollten in `~/.claude/CLAUDE.md`.**

Anthropic empfiehlt inzwischen, prozedurale Abläufe eher in Skills zu halten und CLAUDE.md für dauerhaft relevanten Projektkontext zu verwenden.

Ich würde dreiteilen.

## Ebene 1 – globales Claude-Code-CLAUDE.md

Nur echte Nutzer-/Umgebungsinvarianten:

```text
Sprache Deutsch.
Arbeite standardmäßig direkt im aktuellen Repo.
Keine Secrets ausgeben/einchecken.
Nutze vorhandene Projektregeln vor generischen Defaults.
Frage nur bei tatsächlich offener Entscheidung.
```

Sehr klein.

---

## Ebene 2 – Projekt-CLAUDE.md

Projektfakten:

```text
Skill-Profil
Architektur
Projektregeln
Tests
Deploy
Security
```

Das ist immer verfügbar und projektabhängig.

---

## Ebene 3 – Skill

Jeder Skill behält kurze robuste Invarianten:

Beispiel Branch:

> Verwende den aktuellen Branch der Arbeitskopie oder den Pflicht-Branch des Projektprofils; nie einen Branch raten.

Mehr braucht es nicht.

Nicht noch einmal:

- Toolnamen
- Auswahlfrage-Beispiel
- mehrere Umgebungssyntaxen
- Shell-Kommandos

---

## Cowork-Fallback

Wenn ein Skill weiterhin in claude.ai funktionieren soll:

```text
references/cowork.md
```

Der Kern sagt nur:

> In Umgebungen ohne direkten Repo-Zugriff siehe `references/cowork.md`.

Wenn die Reference dort nicht verfügbar ist:

> liefere das Ergebnis im Chat statt lokale Ausführung zu simulieren.

Damit bleibt der Skill robust.

---

# 9. Eval-Plan – kleinste sinnvolle Baseline

Das alte Smoke-Set ist als Konzept gut, aber die Ergebnisse vom 28.04. sind für die heutigen Descriptions nicht mehr belastbar.

Ich würde **nicht** sofort wieder 86 Fälle manuell fahren.

## Baseline: 60 Fälle

### 48 Einzel-Skill-Fälle

Für jeden der 12 Skills:

```text
2 × should_trigger
1 × should_not_trigger
1 × nearest_conflict
```

= 48.

Wichtig: echte Herbert-Formulierungen bevorzugen.

---

## 12 Cross-Skill-/Systemfälle

Pflicht:

1. `skill-creator ↔ skill-neu`
2. `skill-creator ↔ skill-pflege`
3. `code-review ↔ audit`
4. `modul-bauplan ↔ audit`
5. `audit ↔ doc-pflege`
6. `code-erstellen ↔ mockup`
7. `ticket ↔ tracker`
8. `ticket ↔ code-erstellen`
9. `chat-wechsel ↔ chatgpt-review`
10. `code-erstellen ↔ tracker`
11. generisches „prüfe das“
12. generisches „ändere das“

Damit 60.

---

# Eine einzige Quelle

`test-prompts.md` aus den Skillordnern abschaffen.

Empfehlung:

```text
evals/
├── cases.json
├── runs/
└── README.md
```

Beispiel:

```json
{
  "id": "AUD-004",
  "prompt": "prüfe alle Frontmatter und Quickloads",
  "expected": ["audit"],
  "forbidden": ["doc-pflege"],
  "type": "conflict",
  "source": "golden"
}
```

Keine Doppelpflege.

---

# Vor/nach Refactor messen

Für Trigger-Evals ist die relevante Baseline nicht:

> mit Skill vs. ohne Skill

sondern:

> altes Skillset vs. neues Skillset.

Also vor Refactor Snapshot:

```text
evals/baselines/pre-refactor/
```

Dann dieselben 60 Prompts gegen beide Skillsets.

Die eingebetteten `skill-creator`-Werkzeuge können für qualitative und quantitative Skilltests genutzt werden; Anthropic beschreibt denselben Ansatz mit Skill-/Baseline-Vergleich und iterativer Verbesserung. Für das reine **Routing mehrerer Skills** braucht ihr aber zusätzlich eure eigene zentrale Trigger-Matrix.

---

# Gate

Ein Skill-Refactor darf gemerged werden, wenn:

```text
keine Regression bei should_not_trigger
keine neue unerklärte Kollision
kritische Konfliktfälle 100 %
Gesamtergebnis >= Baseline
```

Nicht nur „sieht kürzer aus“.

---

# 10. Schnitt der vier größten Skills

## A. `skill-pflege`

### Kern

```text
Zweck + Trigger
Safe Patch vs Refactor
Scope bestimmen
Regel-Inventar
Frontmatter-/Triggerregel
Änderung durchführen
Verifikation
Eval-Gate
Kurz-VERBOTEN
```

### References

```text
references/safe-patch.md
references/refactor.md
references/rule-inventory.md
references/eval.md
references/cowork-delivery.md
references/claude-code-distribution.md
```

### Streichen aus Kern

```text
create_file/present_files-Mechanik
Artifact-Separation
OneDrive/DC
historische Incident-Erklärungen
mehrfach erklärte Dateinamenregel
vollständige CHANGELOG-/Commit-Sequenz
alte "nie kürzen/umformulieren"-Regeln
```

---

## B. `mockup-erstellen`

### Kern

```text
Zweck + Grenzen
Mockup-Profil laden
Kontext/Designquelle laden
Entwurf
Pflichtansichten
Qualitätsprüfung
Abnahme
Übergabe an code-erstellen
Kurz-VERBOTEN
```

### References

```text
references/html-mockup.md
references/visual-quality.md
references/sitemap.md
references/cowork-preview.md
```

### Projektprofil

```text
Ablage
Designquelle
Tokens
Ansichten
Abnahmeort
Sitemap ja/nein
```

### Streichen

```text
BPM-NN-Dateinummern aus Kern
Heidi-Bento-Beispiele aus Kern
lange Sitemap-Implementierung aus Kern
Werkzeugnamen
```

---

## C. `chat-wechsel`

### Kern

```text
Zweck
Umgebung bestimmen
aktuellen Stand sammeln
offene Punkte sammeln
kritische Entscheidungen sammeln
Handover/Startprompt erzeugen
Verweise validieren
```

### References

```text
references/cowork-handover.md
references/task-sync.md
references/memory-handover.md
references/link-validation.md
```

Für Claude Code sollte geprüft werden, ob überhaupt noch ein eigener „Handover-Prompt“ gebraucht wird oder ob:

```text
Projekt-STATUS aktualisieren
+ kurzer Startauftrag
```

reicht.

### Streichen aus Kern

```text
[ANKER-LIVE]
Memory-Rubriken-Cowork-Ablauf
Chat-URL
ask_user_input_v0-Beispiele
kompletter ClickUp-Batchalgorithmus
duplizierte doc-pflege-Regeln
```

---

## D. `code-erstellen`

### Kern

```text
Zweck + Abgrenzung
Code-Profil laden
Aufgabe klassifizieren
relevanten Projektkontext laden
Impact bestimmen
Blocking Conditions
implementieren
Tests
Ergebnis/Doc-Hints/Task-Hints
Auslieferung laut Profil
```

### Bestehende References behalten

```text
references/stacks/csharp-wpf.md
references/stacks/typescript-lit.md
references/stacks/home-assistant-yaml.md
references/stacks/python.md
```

### Neue References

```text
references/cowork-delivery.md
references/task-capture.md
```

### Streichen

```text
cc-steuerung-Kapitelverweise
BPM-Quickload-Fallback im Kern
Heidi-Bauplan-Beispiele im Kern
Auto-Anker aus universellem Ablauf
ausführliche Branch-/Arbeitsverzeichnisblöcke
Toolsyntax
```

Der Kern darf wissen:

> Profil sagt Pflicht-Docs → laden.

Er muss nicht selbst BPMs historische Ladereihenfolge kennen.

---

# 11. Reihenfolge Teil D

Deine Reihenfolge ist im Grundsatz richtig. Ich würde sie nur leicht ändern.

## Phase 0 – Entscheidungen

Bestätigt:

1. Profil-Vertrag festlegen.
2. `cc-steuerung` deaktivieren oder Cowork-Adapter.
3. Claude-Code-Distribution klären.

Bei Punkt 3 wissen wir inzwischen: Claude Code unterstützt persönliche Skills unter `~/.claude/skills/` offiziell.

Damit würde ich **Claude Code als primären Runtime-Kanal** festlegen.

---

## Phase 1 – Nur Blocker und Wahrheitsquellen

Noch **vor** großen Inhaltsänderungen:

- INDEX: 12 Skills.
- README: 12 Skills.
- falsche Modi-Zahl.
- Push-Widersprüche beseitigen.
- PowerShell `&&` für PS7.
- tote Pfade markieren/entfernen.
- `references.zip` entfernen.
- Profil-Schema definieren.
- Skill-Repo-CLAUDE.md selbst profilieren.

Hier noch keine große Skill-Kompression.

---

## Phase 2 – Profile herstellen

Hier stimme ich dir vollständig zu.

Und zwar für:

```text
BPM
HA_Dash_DreameX60
claude-skills-bpm
```

Nicht das alte Heidi-Profil kopieren.

Die aktuellen Projektregeln werden in den neuen Vertrag **referenziert**, nicht dupliziert.

---

## Phase 3 – Eval-Baseline

Unbedingt vor dem Refactor.

Hier war meine erste Reihenfolge schlechter.

Wenn wir zuerst kürzen und erst danach messen, können wir eine Triggerregression nicht mehr sauber nachweisen.

---

## Phase 4 – `skill-pflege`

Safe Patch/Refactor + Inventar.

Das ist der Enabler für alles Weitere.

---

## Phase 5 – Querschnitt bereinigen

Danach:

- Auswahlfrage-Regel
- Branch-Regel
- Arbeitsverzeichnis
- Cowork
- Anker
- Push
- Toolnamen

konsolidieren.

---

## Phase 6 – Skills einzeln verkleinern

Je Skill:

```text
Baseline
→ Refactor
→ Querverweisprüfung
→ Eval
→ Commit
```

Nicht alle zwölf auf einmal.

---

## Phase 7 – Routing-Gesamttest

Erst ganz am Ende:

- alle 60 Fälle
- inklusive Anthropic-/Claude-Code-Skills
- inklusive `modul-bauplan`

---

# 12. Priorisierte 10 Maßnahmen

## P0

1. **Ein verbindliches `Skill-Profil v1` definieren** – ein Block mit typisierten Unterabschnitten und feldweisen Required Inputs.

2. **Profile in BPM, aktuellem Heidi und dem Skill-Repo herstellen**, bevor weitere projektneutrale Refactors passieren.

3. **`cc-steuerung` aus dem Claude-Code-Pfad entfernen** – entweder deaktivieren oder ausschließlich Cowork/DC-Adapter.

4. **Push-Politik ins Commit-Profil verlagern** und alle sechs Skills von eigener Push-Politik befreien.

5. **INDEX/README als Wahrheit reparieren:** 12 Skills, aktuelle Konflikte, aktuelle Architektur; historische Invarianten entfernen oder neu formulieren.

## P1

6. **Eval-Baseline mit 60 Fällen erstellen**, zentral in `evals/`; `test-prompts.md` als zweites System abschaffen.

7. **`skill-pflege` auf Safe Patch + Refactor umbauen** mit prüfbarem Regel-Inventar statt Textkonservierung.

8. **`audit ↔ doc-pflege ↔ modul-bauplan` sauber trennen:** systemweite Prüfung / Änderung / fachlicher Modul-Lifecycle.

## P2

9. **Querschnittsregeln entduplizieren und Cowork-spezifische Mechanik in References verschieben.**

10. **Die großen Skill-Kerne einzeln auf 100–300 Zeilen zurückführen**, jeweils mit Vorher-/Nachher-Eval und Querverweisprüfung.

---

# ✅ Einigkeit

- Profil-Vertrag ist derzeit der zentrale Architekturbruch.
- `skill-pflege` muss auf semantische statt textuelle Bestandserhaltung umgestellt werden.
- Profile und Eval-Baseline müssen **vor** den großen Kürzungen kommen.
- `audit` und `doc-pflege` müssen eindeutig getrennt werden.
- Projektbegriffe wie Bauplan/HANDOFF/BPM-Pfade gehören aus generischen Kernskills.
- Cowork-spezifische Mechanik belastet den heutigen Claude-Code-Pfad unnötig.
- Ein zentrales Eval-System statt `evals/` plus `test-prompts.md`.
- CGR-Lifecycle, Sitemap-Mechanik, Artifact-Auslieferung usw. sind Progressive-Disclosure-Kandidaten.
- Push-Prüfung in `chatgpt-review` bleibt.
- `ticket` hat den von mir geforderten Verifikationsworkflow bereits.

# ⚠️ Widerspruch / Präzisierung

- Nicht **alle** Querschnittsregeln in globale CLAUDE.md verschieben. Immer relevante Kontextregeln dort; prozedurale Fachabläufe bleiben im Skill bzw. dessen References.
- `v0.36.0` finde ich im aktuellen CHANGELOG nur einmal. Die übrigen genannten Versionslücken sind bestätigt.
- Direkte Claude-Code-Skills aus `~/.claude/skills/` sind offiziell unterstützt; einen Windows-Symlink/Junction darauf würde ich jedoch erst nach einem kleinen Discovery-Test zur festen Architektur machen.
- `cc-steuerung` würde ich nicht durch eine verbesserte Triggerbeschreibung retten, sondern aus Claude Code herausnehmen.

# ❓ Rückfragen

Für die Architektur selbst habe ich keine zwingende offene Rückfrage mehr. Die drei Entscheidungen aus Phase 0 können aus meiner Sicht jetzt konkret getroffen werden:

1. **Profil:** `## Skill-Profil`, Version 1, mit strikten optionalen Unterbereichen.
2. **cc-steuerung:** nur Cowork-Adapter oder deaktiviert; nicht mehr Teil des Claude-Code-Workflows.
3. **Distribution:** Repo als Source of Truth; Claude Code über `~/.claude/skills/`, claude.ai-Upload nur noch sekundärer Kanal.

Mit diesen drei Festlegungen ist die Richtung für den eigentlichen Refactor ausreichend eindeutig.
