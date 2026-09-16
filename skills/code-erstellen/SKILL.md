---
name: code-erstellen
description: >
  Plant und erzeugt Codeänderungen im aktiven Projekt auf Basis des
  Code-Profils (Pflicht-Docs, Aufgabenquelle, Schichten, Tests, Auslieferung) –
  projektneutral: BPM (C#/WPF, INDEX.md + Quickloads), Heidi (TypeScript/Lit,
  HA-YAML, Python; Bauplan + HANDOFF) oder jedes andere Repo mit Profil. Use
  when users want to schreiben, erstellen, bauen, implementieren, fixen,
  refaktorieren, ändern, ergänzen, korrigieren, or erweitern application code —
  including views, dialogs, components, services, view models, repositories,
  handlers, validators, models, controllers, validation, persistence logic,
  data flows, schemas, migrations, automations, or any source file
  (.cs/.xaml/.ts/.js/.py/.yaml/.json). Triggers also on bug fixes, UI fixes in
  existing dialogs/screens/views/components, and implementing logic regardless
  of domain (e.g., recovery logic, business logic, parsing logic).
  Do not trigger for UI mockups (HTML-Entwürfe), git commit commands, explicit
  documentation authoring (ADR / Konzept-Doc / Frontmatter / Quickload),
  ClickUp task actions, or read-only audits.
---

# Code-Erstellen — Orchestrator Skill

## Zweck

Stellt sicher dass vor jeder Code-Erstellung die relevanten Docs
gelesen und geprüft wurden, die Akzeptanz der Aufgabe bekannt ist, Tests
laufen und die Änderung ausgeliefert wird. Welche Docs, Tests und
Auslieferungsschritte das sind, steht im **Code-Profil** des Projekts
(Abschnitt „Voraussetzung: Code-Profil“). BPM nutzt die verbindliche
Ladereihenfolge aus DOC-STANDARD.md Kapitel 8; andere Projekte ihre eigene.

---

## Vorrang / Delegation an andere Skills

**code-erstellen ist der größte Catch-all und würde sonst auch bei verwandten
Themen anspringen. Deshalb gilt lokal: wenn die Hauptabsicht einer dieser
Punkte ist, NICHT hier weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| UI-Entwurf, Layout-Klärung, Screen-Vorschlag, neues HTML-Mockup | **mockup-erstellen** |
| Großer UI-Umbau (Modus Deep) und das Profil sagt „Mockup-Pflicht: ja“ → zuerst Mockup, Abnahme abwarten, dann hier weiter | **mockup-erstellen** (Mockup-Hook) |
| Commit-Befehl, Commit-Message, Version-Bump | **git-commit-helper** |
| ADR, Konzept, Frontmatter, Quickload, Doku-Refactor | **doc-pflege** |
| ClickUp-Task-Aktion (neu, done, update, split, …) | **tracker** |
| Read-only Konsistenzprüfung zwischen Code und Docs | **audit** |

Nur wenn die Hauptabsicht **echte Code-Implementierung** ist
(Services, ViewModels, Dialoge, Persistenzlogik, Validierung, etc.),
bleibt code-erstellen zuständig.

**Wichtig:** Das ist kein globales Regelsystem, sondern lokaler Vorrang
für den größten Catch-all. Die Delegation wird hier explizit genannt, weil
code-erstellen sonst unbeabsichtigt die genannten Nachbarskills überschreibt.

---

## 🚨 VERBINDLICHE REGEL: Auswahlfrage bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS eine Auswahlfrage
gestellt werden — KEINE Prosa-Fragen.** Auswahlfrage = das Frage-Werkzeug der
jeweiligen Umgebung mit anklickbaren Optionen (Cowork-Chat `ask_user_input_v0`,
Claude Code `AskUserQuestion`). Wo unten „Auswahlfrage“ steht, ist dieses
Werkzeug gemeint.

### Diese Fragen IMMER als Auswahlfrage:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (nur wenn die Shell ihn nicht liefert) | Alle Branch-Namen aus `git branch -a` als Optionen |
| Modus unklar | Lite, Standard, Deep |
| Zielschicht mehrdeutig | Domain, Application, Infrastructure, UI |
| Mehrere Referenz-Implementierungen | Dateinamen als Optionen |
| Fachliche Invariante würde verletzt | "Trotzdem fortsetzen", "Abbrechen", "Andere Lösung" |
| Ausgabeformat mehrdeutig (nur Cowork) | Komplette Datei, SUCHE/ERSETZE, Download |
| ClickUp-Task-Zuordnung nach Commit | Task-Kandidaten als Optionen + "Kein Task" + "Neuen Task anlegen" |
| Mehrere Blocking Conditions | Welche Datei zuerst laden (Kandidaten) |
| Commit-Version unklar (Major/Minor/Patch) | MAJOR (Breaking), MINOR (Feature), PATCH (Fix) |
| User muss Referenzdatei angeben | Kandidaten aus Projektstruktur |
| Bestehende Daten/Configs betroffen | "Daten löschen, neu anlegen lassen", "Migration bauen", "Abbrechen" |
| Tests rot nach dem Bau | "Fix jetzt", "Test anpassen (Begründung)", "Abbrechen" |
| Mockup-Pflicht greift (Deep + UI) | "Mockup zuerst", "Ohne Mockup weiter (User-Entscheid)" |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen  
  (Beispiel: "Welcher Kurztitel für den Commit?")
- User hat gerade eine klare Präferenz signalisiert
- Es ist Erklärung/Kontext, keine echte Entscheidung
- Freitext-Input nötig (z.B. neuer Klassenname, neue Commit-Message)

### Wie die Auswahlfrage aussieht (Cowork-Syntax; Claude Code: `AskUserQuestion` mit denselben Optionen)

Einfache Auswahl:
```
ask_user_input_v0(
  questions: [
    {
      question: "Welcher Modus für diese Aufgabe?",
      options: ["Lite", "Standard", "Deep"]
    }
  ]
)
```

Branch-Auswahl:
```
ask_user_input_v0(
  questions: [
    {
      question: "Welcher Branch ist aktiv?",
      options: ["main", "feature/planmanager-v1", "feature/settings-tabs"]   // Beispiel BPM
    }
  ]
)
```

### VERBOTEN

- Branch-Liste im Chat aufzählen und auf getippte Antwort warten
- "Lite oder Standard oder Deep?" als Prosa
- "Welche Datei soll noch geladen werden?" als Prosa wenn Kandidaten bekannt
- "Passt zu <PRÄFIX>-NNN. tracker done ausführen?" als Prosa
- Eine Optionen-Aufzählung im Chat ohne Auswahlfrage

---

## Branch-Ermittlung (PFLICHT vor dem ersten Schreibzugriff)

1. Prüfe ob Branch bereits in dieser Session bekannt ist → verwenden
2. **Shell verfügbar** (Claude Code: Bash/PowerShell; Cowork: DC): `git branch --show-current`
   liefert den Branch – das ist eine Tatsache, keine Frage. Nennt das Code-Profil einen
   Pflicht-Branch (Heidi: `dreame_x60`) und der aktuelle weicht ab → Auswahlfrage
   (wechseln / trotzdem / abbrechen), nie stumm weiterarbeiten.
3. **Keine Shell** (reiner Chat, GitHub API): Branches auflisten und **per Auswahlfrage**
   den aktiven wählen lassen (Optionen = Branch-Namen)
4. Gewählten Branch für die gesamte Session merken
5. NIE automatisch einen Branch annehmen (weder `main` noch einen anderen)

---

## Arbeitsverzeichnis (PFLICHT bei Dateizugriff)

**Claude Code:** Arbeitsverzeichnis = Repo-Wurzel der Sitzung
(`git rev-parse --show-toplevel`); bei Worktrees gilt der Worktree, nie das
Haupt-Checkout. Der Rest dieses Abschnitts betrifft nur den Cowork-Chat.

**Cowork-Chat:** Wenn dieser Skill DC-Operationen auslöst (z.B. Code-Dateien lesen,
Entry Points prüfen), das Arbeitsverzeichnis nach **cc-steuerung Kapitel 4** ermitteln.

### Ablauf (erster DC-Aufruf der Session, Cowork)

1. Pfad-Ermittlung:
```powershell
$pc = hostname; $od = [System.Environment]::GetEnvironmentVariable('OneDrive', 'User'); Write-Host "$pc|$od"
```

2. INDEX.md laden → Abschnitt "PCs und Arbeitsverzeichnisse" → COMPUTERNAME matchen
   - **GEFUNDEN** → workFolder = OneDrive-Pfad + `\` + Projekt-Suffix aus INDEX.md
   - **NICHT GEFUNDEN** → Self-Registration (cc-steuerung 4.3)

3. Verifikation:
```powershell
Test-Path "<workFolder>"
```

4. workFolder für die gesamte Session merken

**Wichtig:** `$env:OneDrive` funktioniert NICHT über DC `start_process`.
IMMER `[System.Environment]::GetEnvironmentVariable('OneDrive', 'User')` verwenden.
**Keine hardcodierten absoluten Pfade** – in keiner Umgebung.

---

## Auto-Anker bei Task-Keywords (Phase 1 des Chat-Anker-Systems)

**Zweck:** Wenn im Chat ein Thema auftaucht das offensichtlich ein späterer Task wird (aber aktuell noch kein Task existiert), setzt dieser Skill automatisch einen temp-Anker. Das stellt sicher, dass die Diskussionsstelle später via `conversation_search` wiederfindbar ist.

**Gilt nur im Cowork-Chat.** In Claude Code gibt es weder Chat-Suche noch `[ANKER-LIVE]`-Memory;
dort ersetzt eine Auswahlfrage den Anker: „Task jetzt anlegen (`tracker neu`)“ / „Im
Notiz-Ort des Profils vermerken“ (Heidi: Bauplan Abschnitt 10) / „Nichts“. Anker-Präfix =
Projekt-Präfix aus `projects/<[PROJECT]>/clickup-lists.md` (BPM `BPM`, Heidi `DX`).

Konzept-Doc: `docs/chat-anker-konzept.md` (Phase 1).
Anker-Format + Memory-Registry: siehe tracker-Skill Kapitel "Chat-Anker-System".

### Task-Keywords (Trigger für Auto-Anker)

Claude erkennt folgende Formulierungen als klares Task-Signal:

- "das müssen wir noch bauen"
- "später implementieren"
- "ins backlog"
- "backlog-wert"
- "da brauchen wir einen task"
- "sollten wir im task tracken"
- "muss noch gemacht werden"
- "als task anlegen"

Wenn User diese Keywords nutzt UND das Thema noch keinen offenen Task hat → Auto-Anker setzen.

### Ablauf

1. Keyword erkannt UND Kontext ist klar (Thema identifizierbar)
2. TEMP-ID generieren:
   - Primär in der Shell (Cowork: DC PowerShell, siehe tracker-Skill "TEMP-ID Generierung")
   - Fallback: Claude erzeugt `TEMP-<yyMMddHHmm><3 Zufallsbuchstaben>`
3. Anker-Zeile im Chat-Response einfügen (möglichst am Anfang des relevanten Abschnitts):
   ```
   [<PRÄFIX>-ANCHOR-TEMP-<id>] — Idee: <kurzbeschreibung max 60 Zeichen>
   ```
4. Memory aktualisieren (Cowork):
   ```
   memory_user_edits(command: "add", control: "[ANKER-LIVE] TEMP-<id>|offen|<ISO-timestamp>|<kurzbeschreibung>")
   ```
5. Kurzer Hinweis im Chat: "Anker gesetzt — wird bei `tracker neu` mit Task-ID verknüpft."

### Wann KEIN Auto-Anker

- User spricht nur über bestehende Tasks (nicht Task-würdiger Neu-Content)
- Thema ist zu vage für eine 60-Zeichen-Kurzbeschreibung
- Innerhalb 24h existiert bereits ein Anker mit ähnlichem Thema (Duplikat-Check via `[ANKER-LIVE]`)
- User sagt explizit "kein Task daraus" o.ä.
- Mehr als 10 Anker bereits in `[ANKER-LIVE]` — User sollte erst aufräumen

**Im Zweifel: KEIN Anker.** Lieber ein paar Anker verpassen als den Chat zuspammen.

### Anti-Pattern

- Anker mitten in Code-Blöcken einfügen
- Mehrere Anker direkt hintereinander für dasselbe Thema
- Anker setzen für Dinge die der User nur erwähnt ohne Handlungsabsicht
- Anker mit generischen Beschreibungen wie "Feature X" oder "TODO"

---

## Voraussetzung: Code-Profil

Das Projekt beschreibt in einem **Code-Profil**, was dieser Skill vor, während und nach
dem Bau braucht. Ort: Abschnitt `## Code-Profil` in der `CLAUDE.md` des Repos (Claude Code
liest sie automatisch; im Cowork-Chat per DC lesen). Felder:

| Feld | Bedeutung | BPM | Heidi |
|------|-----------|-----|-------|
| Stack | Sprachen/Frameworks, Build- und Lint-Befehle | C#/WPF, .NET | TypeScript/Lit (esbuild), HA-YAML, Python |
| Pflicht-Docs | Ladereihenfolge vor dem Code | INDEX.md → Quickload → Invarianten → Pflichtlesen (DOC-STANDARD Kap. 8) | CLAUDE.md, docs/HANDOFF.md, BAUPLAN.md Abschnitt 2 (Regeln) + 4 (Vertrag) |
| Aufgabenquelle | Wo Ziel + Akzeptanz stehen | ClickUp-Task (Description-Template) | BAUPLAN.md Abschnitt 8 Karte + ClickUp DX-Task |
| Schichten / Kopplung | Wer darf wen kennen, wo wird verdrahtet | View→ViewModel, Service→Interface+DI, DB→Schema | contract → device/profile → selectors → Komponenten; Schreiben nur über DxApi |
| Tests | Befehl + Pflicht vor Commit | laut INDEX.md | `npm test` in dreame_x60/card (check, unit, build, E2E) |
| Auslieferung | Schritte nach dem Commit | laut INDEX.md | `deploy.ps1 -OnlyCard` + Ressourcen-Version; Backend: check_config + reload/restart |
| Mockup-Pflicht | Deep + UI zuerst als Mockup? | nein | ja (Herbert: große Umbauten zuerst als Mockup) |
| Notiz-Ort | Wo Befunde/Ideen ohne Task landen | Memory / Backlog | BAUPLAN.md Abschnitt 10 |

**Fehlt das Profil:** `INDEX.md` im Repo als Profil nehmen (BPM-Weg, optional DOC-STANDARD.md).
Fehlt auch das: Auswahlfrage „Profil jetzt anlegen (ich schlage Werte aus dem Repo vor)“ /
„Ohne Profil, ich nenne die Dateien“. Nie ohne Docs coden.

---

## Load Order (verbindlich)

### 1. Anfrage klassifizieren → Modus

Kriterien sind stack-neutral; in Klammern die BPM- bzw. Heidi-Lesart.

```
mode = Lite

Eskalation auf Standard:
- neue öffentliche Funktion in einem bestehenden Baustein (Service/ViewModel · Selector/Komponente)
- neuer Dialog / View / Komponente / Command
- Persistenz- oder Backend-Logik ohne neues Schema (Tabelle · HA-Helfer/Automation)
- mehrere Dateien in einem Modul
- neue Validierungs-/Statuslogik

Eskalation auf Deep:
- neue Schnittstelle / Implementierung (Interface+Service · Vertrag contract.ts, DxApi)
- Schema-Änderung (Tabelle · Entitäts-Vertrag, Paket-Helfer)
- externe Kommunikation / Import / Export (API · HA-Dienste, Integration)
- mehrere Schichten / Projekte (Karte + Backend)
- neuer Benutzerfluss / neue Seite
- Datenschutz (DSGVO/DataClassification · GPS, Tokens in Abzügen)
- Verdrahtung betroffen und nicht rein lokal (DI · Shell/Selektoren-Registrierung)
- Profil kann eigene Kriterien ergänzen
```

**Bei Unsicherheit (Anfrage passt zu mehreren Modi):** Auswahlfrage mit Optionen Lite, Standard, Deep.

**Mockup-Hook:** Modus Deep + UI betroffen + Profil „Mockup-Pflicht: ja“ → an
**mockup-erstellen** delegieren, Abnahme des Users abwarten, erst dann Schritt 2.
Ausnahme nur per Auswahlfrage („Ohne Mockup weiter“).

### 2. Aufgabenquelle und Pflicht-Docs laden

1. **Aufgabenquelle** aus dem Profil lesen (ClickUp-Task, Bauplan-Karte): Ziel,
   **Akzeptanzkriterien**, „Nicht ändern“, Voraussetzungen. Jede Akzeptanz-Zeile wird
   ein Testfall (Schritt 7b) und eine Zeile im Impact Check.
2. **Pflicht-Docs** in der Reihenfolge des Profils laden. BPM: INDEX.md → Task-to-Doc
   Routing → Primary/Secondary/Reference. Heidi: CLAUDE.md (automatisch), HANDOFF.md
   Abschnitt 3e, BAUPLAN.md Abschnitt 2 und 4, bei Domänen-Logik Abschnitt 6.

### 3. Quickload-First-Pass (BPM: DOC-STANDARD Kapitel 8; andere Projekte: Ladereihenfolge des Profils)

**Verbindliche Ladereihenfolge (BPM):**

```
1. INDEX.md → Routing (welche Doc?)
2. Frontmatter + AI-Quickload lesen → Filter (relevant? welches Kapitel?)
3. Fachliche Invarianten prüfen → Sofort sichtbar ohne Langform
4. Pflichtlesen-Kapitel laden → Immer wenn Modul betroffen
5. Weitere Kapitel nur bei Bedarf nachladen
```

**Ablauf:**
1. Relevante Docs aus INDEX-Routing identifizieren (Primary zuerst)
2. Für jede Doc: Nur erste ~30 Zeilen laden (Frontmatter + Quickload)
3. Fachliche Invarianten sofort in den Impact Check übernehmen
4. Pflichtlesen-Kapitel: IMMER laden wenn Modul betroffen → Blocking Condition
5. Aus Quickload-Kapitel-Feld entscheiden welche Kapitel relevant sind
6. Nur relevante Kapitel als Langform nachladen
7. Quickload nicht vorhanden? → Fallback: ganze Doc laden

**Limits:**
- Lite: Quickload max 3 Docs, Langform max 2
- Standard: Quickload max 6 Docs, Langform max 4
- Deep: Quickload max 10 Docs, Langform max 8

### 4. Code Entry Points laden

Kopplungsregeln aus dem Profil („Schichten / Kopplung“). Beispiele:

BPM:
- View → ViewModel prüfen
- Neuer Service → Interface + DI (App.xaml.cs)
- Neuer Dialog → Theme-/Dialog-Referenz
- DB-Änderung → ProjectDatabase.cs + DB-SCHEMA.md

Heidi:
- Neue Entität/Dienst → `contract.ts` (+ Bauplan Abschnitt 4), dann Selector, dann Komponente
- Schreiben nach HA nur über `DxApi`; Komponenten lesen nur Views aus Selektoren
- Backend-Änderung (Paket/Automation) → deployen, `check_config`, reload/restart
- Nichts fest verdrahten, was Roboter oder HA liefern (Räume, Optionen, Namen)

### 5. Impact Check

Zeilen stack-neutral; in Klammern die BPM- bzw. Heidi-Lesart.

```
📋 Impact Check:
- UI / Styles / Design-Tokens (XAML/Theme · Lit-Templates/--dx-*): [Ja/Nein]
- Zustand / Bindings / Commands (ViewModel · Selektoren/Views): [Ja/Nein]
- Domäne / Schnittstelle (Interface · contract.ts, domain/*): [Ja/Nein]
- Persistenz / Backend (SQLite/Dateisystem · HA-Paket, Automationen, Skripte): [Ja/Nein]
- Verdrahtung (DI · Shell, ALL_SELECTORS, Registrierung): [Ja/Nein]
- Externe Kommunikation (API · HA-Dienste, Integration, WebSocket): [Ja/Nein]
- Datenschutz (DSGVO · GPS/Tokens in Abzügen, secrets): [Ja/Nein]
- Settings / Konfiguration: [Ja/Nein]
- Lebenszyklus (App-Start · Karten-Init, hass-Ticks/Render): [Ja/Nein]
- Logging / Fehlerbehandlung (· Toast, Teilfehler): [Ja/Nein]
- Bestehende Daten/Configs betroffen?: [Ja/Nein] (Frühphasen-Prinzip, BPM: INDEX.md)
- Referenzimplementierung: [Name oder Nein]
- Fachliche Invarianten verletzt?: [Liste oder Nein] (Heidi: Bauplan Regeln Abschnitt 2, „Nicht ändern“ der Karte)
- Akzeptanzkriterien der Aufgabenquelle: [Liste → werden Testfälle]
- Tests betroffen (Profil-Befehl): [welche Dateien]
- Auslieferung nötig (Profil): [Ja/Nein, welcher Schritt]
```

### 6. Blocking Conditions

Blockiere Code-Erstellung wenn:
- Zielschicht unklar → Auswahlfrage (Domain / Application / Infrastructure / UI · Heidi: domain / ha / components / Backend)
- Referenzdatei nicht gefunden → Auswahlfrage mit Kandidaten oder "Ohne Referenz"
- Verdrahtung betroffen aber nicht geladen → erst laden (BPM: App.xaml.cs · Heidi: Shell/selectors.ts)
- Externe Kommunikation ohne Datenschutz-Doc → erst laden (BPM: DSGVO-Architektur.md · Heidi: CLAUDE.md „Nie ins Repo“)
- UI ohne Design-Doc → erst laden (BPM: UI-Doc/Theme · Heidi: Mockup bento.html, tokens.ts)
- Schema/Vertrag ohne Doc → erst laden (BPM: DB-SCHEMA.md · Heidi: Bauplan Abschnitt 4)
- **Pflichtlesen-Kapitel nicht geladen obwohl Modul betroffen** → laden
- **Akzeptanzkriterien der Aufgabenquelle nicht gelesen** → erst lesen
- **Mockup-Pflicht greift und kein abgenommenes Mockup** → mockup-erstellen (siehe Schritt 1)
- **Fachliche Invariante würde verletzt werden** → Auswahlfrage (Trotzdem fortsetzen / Abbrechen / Andere Lösung)
- **Migration / Backward-Compatibility wäre nötig** → Auswahlfrage (Daten löschen + neu anlegen / Migration explizit gewünscht / Abbrechen) — Frühphasen-Prinzip (BPM: INDEX.md)

→ NICHT blind coden, per Auswahlfrage nachfragen welche Datei noch geladen werden muss.

### 7. Code erzeugen

Standards aus Project Files, Referenzimplementierungen als Muster. Nichts fest
verdrahten, was das Profil als dynamisch nennt.

### 7b. Tests (Pflicht, Befehl aus dem Profil)

1. Für jede Akzeptanz-Zeile aus Schritt 2 einen Test schreiben oder erweitern
   (Unit für Domäne/Selektoren, E2E für Bedienung; Heidi: `tests/unit/*.test.ts`, `tests/e2e/*.js`)
2. **Claude Code:** Testbefehl des Profils ausführen (Heidi: `npm test` in `dreame_x60/card`,
   zusätzlich `npm run lint`). Exit-Code 0 ist Bedingung für Schritt 9.
   **Cowork:** Testbefehl im Commit-Block mitliefern; der User führt aus und meldet das Ergebnis.
3. **Tests rot** → Auswahlfrage: „Fix jetzt“ / „Test anpassen (Begründung in Aufgabenquelle)“ /
   „Abbrechen“. Nie einen roten Test still löschen oder überspringen.
4. Ergebnis kurz melden (Anzahl, Dauer, was rot war und warum). Kein „Tests laufen“ ohne Ausgabe.

### 8. Ausgabeformat (nur Cowork-Chat → suche-ersetze)

**Claude Code:** entfällt – Dateien werden direkt mit Edit/Write geändert; Ausgabe im Chat ist
die Zusammenfassung (Dateien, Tests, Commit), nicht der Code.

**Cowork:**
- Neue Datei → komplett
- < 600 Zeilen UND > 30% geändert → komplett
- ≥ 600 Zeilen → SUCHE/ERSETZE
- XAML → Download

**Bei Mehrdeutigkeit:** Auswahlfrage mit den möglichen Formaten.

### 9. Commit + DocMaintenanceHints (→ git-commit-helper + doc-pflege)

Format, Versionsquelle und Bump-Regel kommen aus dem **Commit-Profil** des Repos
(git-commit-helper). Die Doku-Zeilen sind die **Doku-Checkliste des Commit-Profils** –
unten das BPM-Beispiel; Heidi: Bauplan-Statusliste, Abschnitt 10/10a, HANDOFF 3e,
Abschnitt 4 + contract.ts bei neuen Entitäten.

```
[vX.Y.Z] Modul, Typ: Kurztitel

📝 Doc-Pflege nötig (BPM-Beispiel):
- INDEX.md: [Ja/Nein]
- DB-SCHEMA.md: [Ja/Nein]
- CHANGELOG.md: [Ja/Nein]
- ADR.md: [Ja/Nein]
- Frontmatter: [welche Docs]
- Quickload: [welche Docs]

🧪 Tests: [Befehl, Ergebnis, Exit-Code]
📂 Gelesene Dateien: [Liste]
📋 Quickload-Only: [Liste]
⚠️ Annahmen: [falls vorhanden]
🚫 Nicht geladen: [Begründung]
```

**Version-Bump unklar?** Auswahlfrage:
- MAJOR (Breaking Change)
- MINOR (neues Feature)
- PATCH (Bugfix)
(Bump-Regel des Commit-Profils hat Vorrang, z.B. Vorabversion: jede Änderung zählt hoch.)

### 9b. Auslieferung (Schritte aus dem Profil)

Nur wenn das Profil eine Auslieferung nennt. **Claude Code** führt sie aus und prüft das
Ergebnis; **Cowork** liefert die Befehle. Heidi: `.\tools\deploy.ps1 -OnlyCard`, danach
Ressourcen-Version über `tools/ha-ws.js lovelace/resources/update`; Backend-Änderung:
`check_config`, dann reload bzw. restart. Zum Schluss dem User sagen, was er wie
sichtprüfen soll (Strg+F5, welche Seite, welches Verhalten).

### 10. ClickUp Tracker-Abgleich (optional)

Nach erfolgreichem Commit prüfen:
1. Gibt es einen offenen ClickUp-Task der zu dieser Änderung passt?
   - `clickup_search` mit Schlüsselwörtern aus dem Commit-Titel
2. **Wenn Kandidaten gefunden → Auswahlfrage:**
   ```
   Frage: "Commit passt zu folgenden Tasks. Welcher soll auf Done?"
   Optionen:
   - "<PRÄFIX>-004 | 5998er Statikplaene Erkennung"   (Beispiel BPM)
   - "<PRÄFIX>-007 | andere passende Task"
   - "Kein Task passt"
   - "Neuen Task anlegen"
   ```
3. Bei "Neuen Task anlegen" → `tracker neu` aufrufen
4. Bei Task-Auswahl → `tracker done` aufrufen
5. NICHT automatisch schließen — nur vorschlagen
6. Alle ClickUp-Operationen über den **tracker-Skill**, NICHT direkt

Beispiel-Ausgabe nach Commit:

```
[v0.25.30] PlanManager, Fix: 5998er Statikplaene Erkennung

📝 Doc-Pflege nötig: Nein
🎯 ClickUp: 1 passender Task gefunden
```
→ dann Auswahlfrage mit dem Task als Option

---

## Modus-Übersicht

| Modus | Quickload | Langform | Code | Impact | Tests |
|-------|-----------|----------|------|--------|-------|
| Lite | max 3 | max 2 | 1-3 | Kurz | bestehende laufen lassen |
| Standard | max 6 | max 4 | 3-8 | Voll | + je Akzeptanz-Zeile ein Test |
| Deep | max 10 | max 8 | 5-12+ | Voll + Blocking | + E2E für den Benutzerfluss; Mockup-Hook |

---

## VERBOTEN

- Code ohne Pflicht-Docs des Profils (BPM: INDEX.md; Heidi: Bauplan-Karte + Abschnitt 2/4)
- Quickload-First-Pass überspringen
- Pflichtlesen-Kapitel ignorieren
- Fachliche Invarianten ignorieren
- Annahmen ohne geladene Dateien
- Impact Check weglassen
- DocMaintenanceHints weglassen
- Branch automatisch annehmen ohne User-Auswahl
- **Branch-Auswahl als Prosa** — IMMER Auswahlfrage (wenn die Shell ihn nicht liefert)
- Hardcodierte absolute Pfade bei Dateizugriff (DC oder Claude Code)
- ClickUp-Tasks direkt erstellen/schließen (→ immer über tracker-Skill)
- Tasks automatisch als Done markieren ohne User-Bestätigung
- **Task-Zuordnung nach Commit als Prosa** — IMMER Auswahlfrage
- **Modus-Auswahl als Prosa bei Unsicherheit** — IMMER Auswahlfrage
- **Blocking-Condition-Auflösung als Prosa** wenn Kandidaten bekannt — IMMER Auswahlfrage
- **Commit bei roten Tests** oder ohne den Testbefehl des Profils ausgeführt zu haben (Claude Code)
- **Roten Test löschen oder überspringen** ohne Auswahlfrage und Begründung
- **Akzeptanzkriterien der Aufgabenquelle ignorieren** — sie sind die Testliste
- **Deep-UI-Umbau ohne Mockup**, wenn das Profil Mockup-Pflicht sagt — außer der User entscheidet es per Auswahlfrage
- **Auslieferung vergessen**, wenn das Profil eine nennt — nach dem Commit ist die Änderung erst fertig, wenn sie läuft
- **Stack-Begriffe eines Projekts (WPF, DI, SQLite, XAML) für ein anderes annehmen** — Schichten und Kopplung aus dem Profil
- Optionen im Chat aufzählen und auf getippte Antwort warten
- Migration / Backward-Compatibility automatisch bauen ohne User-Freigabe (siehe Frühphasen-Prinzip in INDEX.md)
- **Auto-Anker bei vagen Themen setzen** — lieber keinen Anker als einen unscharfen
- **Anker mit generischen Beschreibungen** ("Feature X", "TODO") — immer konkret benennen
- **Anker setzen ohne Memory-Update** (Cowork) — Chat-Zeile UND `[ANKER-LIVE]`-Eintrag gehören zusammen; in Claude Code stattdessen Auswahlfrage tracker neu / Notiz-Ort
