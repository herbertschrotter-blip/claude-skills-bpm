---
name: chat-wechsel
description: >
  Erstellt die Übergabe an die nächste Claude-Sitzung: einen vollständigen
  Handover-Prompt mit Stand, Erledigtem, offenen Punkten, nächsten Schritten,
  Entscheidungen und Regeln (aus den Profilen); in Claude Code zusätzlich vorher
  den Sitzungsabschluss im Repo (doc-pflege Modus 8). Use when users want to continue in a new chat or session, ask for
  a session handover, a continuation prompt, or a next-chat summary. Do not trigger for ChatGPT review prompts,
  generic prompt requests, or casual goodbyes like "tschüss" or "gute Nacht".
---

# Chat-Wechsel Skill

## Zweck

Übergabe, wenn eine Sitzung endet und in der nächsten weitergearbeitet wird. Zwei Wege, ein Ziel:

- **Cowork-Chat:** Ein Handover-Prompt im Chat (PROMPT-STRUKTUR unten). Der Chat hat kein Repo-Gedächtnis,
  also trägt der Prompt den Stand.
- **Claude Code:** Erst **doc-pflege Modus 8 (Sitzungsabschluss)** – Statusliste/Aufgabenquelle, Befunde,
  Stand-Abschnitt, offene Punkte, Commit + Push nach der Push-Policy –, dann **derselbe vollständige Handover-Prompt** nach
  PROMPT-STRUKTUR (Herbert, 16.09.2026: „der war in BPM immer viel umfangreicher“). Der Prompt darf den
  Repo-Stand zusammenfassen, verweist aber für Details auf HANDOFF/Bauplan statt sie zu kopieren. Der
  Startprompt des Doku-Profils (Heidi: Bauplan Abschnitt 0) steht als Einstiegszeile **im** Prompt.
  Eine Kurzform (nur Startprompt) gibt es nur, wenn der User sie ausdrücklich verlangt („kurzer Prompt“).

Projektwerte (Präfix, Listen, Commit-Format, Doc-Namen, Testbefehl) kommen aus den Profilen der CLAUDE.md
(Commit-, Tracker-, Code-, Doku-Profil); ohne Profil gilt der BPM-Weg (Memory `[CLICKUP]`, INDEX.md).

---

## Vorrang / Delegation an andere Skills

**chat-wechsel erzeugt den Handover-Prompt für die NÄCHSTE Claude-Session.
Wenn die Hauptabsicht ein ChatGPT-Review-Prompt oder ein anderer
Prompt-Typ ist, NICHT hier weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Prompt für ChatGPT-Review (zweite Meinung, Cross-LLM-Kritik) | **chatgpt-review** |
| Code schreiben | **code-erstellen** |
| ClickUp-Task-Aktion | **tracker** |
| Doc schreiben | **doc-pflege** |

Nur wenn die Hauptabsicht **ein Handover-Prompt für den nächsten Claude-Chat** ist
("neuer chat", "nächster chat", "übergabe", "session beenden"), bleibt
chat-wechsel zuständig.

**Wichtig:** Beide Skills können im selben Chat nacheinander laufen
(erst ChatGPT-Review abschließen, dann Claude-Handover). Sie triggern
aber nicht gemeinsam auf einen Satz — der User-Intent entscheidet,
welcher zuerst dran ist.

---

## Grundsätze

- **Fragen nur bei offener Entscheidung** – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen
  ist –, dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung. Typische Stellen:

  | Situation | Optionen |
  |-----------|----------|
  | Link-Prüfung findet tote Verweise | "Korrigieren", "Mit Warnung übernehmen", "Weglassen" |
  | Claude Code: uncommittete Änderungen beim Abschluss | "Jetzt committen (Modus 8)", "Als offen vermerken", "Abbrechen" |
  | Batch-Abschluss: erledigte Tasks | "Alle als Done markieren", "Einzeln wählen", "Keine" |
  | Batch-Abschluss: erledigte Tasks einzeln wählen | multi_select mit allen Task-Namen |
  | Batch-Anlage: neue Tasks aus Chat | "Alle anlegen", "Einzeln wählen", "Keine" |
  | Batch-Anlage: neue Tasks einzeln wählen | multi_select mit allen erkannten Problemen |
  | ClickUp nicht erreichbar | "Trotzdem Prompt erstellen", "Retry", "Abbrechen" |
  | Version-Angabe unklar | Aktuelle Versionen als Optionen |
  | Kein Commit-Stand erkennbar | "Version vom User eingeben", "Ohne Version", "Abbrechen" |

  Prosa nur bei einer offenen Frage ohne feste Optionen (Beispiel: "Welche Version ist aktuell?" ohne Kandidaten), wenn
  der Nutzer gerade eine klare Präferenz signalisiert hat, oder bei Erklärung/Kontext ohne echte Entscheidung.
- **Branch** nach der Branch-Policy im Skill-Profil der `CLAUDE.md`: `current` → der aktuelle Branch aus der Shell
  (`git branch --show-current`); `fixed:<branch>` → der aktuelle muss dieser sein, sonst Auswahlfrage (wechseln /
  abbrechen). Ohne Shell gilt bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage. Ohne Skill-Profil: ein in dieser Sitzung schon bekannter Branch; sonst mit Shell
  `git branch --show-current` – Tatsache, keine Frage; ohne Shell die Branches über die GitHub API auflisten und per
  Auswahlfrage wählen lassen (Optionen = Branch-Namen). NIE automatisch einen Branch annehmen (weder `main` noch einen
  anderen). Den Branch für die ganze Sitzung merken und im Übergabe-Prompt unter `**Branch:**` eintragen.
- **Push** im Sitzungsabschluss (Claude Code) nach der Push-Policy des Skill-Profils:
  - `user-only`: kein Push; der Nutzer pusht selbst
  - `allowed`: Push nur, wenn der Nutzer es ausdrücklich will
  - `required-after-commit`: Push direkt nach dem Commit des Sitzungsabschlusses
  - `required-at-session-end`: alle Commits der Sitzung pushen, bevor der Handover-Prompt ausgegeben wird

  Ohne Push-Policy (kein Skill-Profil): Commit + Push im Sitzungsabschluss.

  Bleiben Commits ungepusht (`user-only`, `allowed`), nennt der Übergabe-Prompt sie unter „Sonstige offene Punkte“
  (Hash und Titel, „Push durch den Nutzer“).

---

## TRIGGER

Ja: "neuer chat", "nächster chat", "session beenden", "chat wechsel",
"weiter im nächsten chat", "mach mir den prompt", "übergabe", "neue sitzung",
"sitzung abschließen und übergabe"

Nein: "pause", "tschüss", "gute nacht"

---

## ClickUp-Integration (vor Übergabeprompt)

### Schritt 1: Offene Tasks laden

1. Space/Listen-ID und Präfix aus dem **Tracker-Profil** (Claude Code: CLAUDE.md) bzw. dem Memory-Eintrag `[CLICKUP]` (Cowork) lesen
2. `clickup_filter_tasks(list_ids/space_ids: [...], statuses: <offene Status laut projects/<name>/clickup-lists.md>)` – read-only, über den tracker-Skill
3. Tasks gruppieren: mehrere Listen → nach Liste (BPM); eine Liste → nach Status (Heidi: in development, testing, backlog)

### Schritt 2: Chat-Verlauf scannen

Chat scannen auf:
- Tasks die bearbeitet aber nicht als Done markiert wurden
- Neue Probleme die aufgetaucht aber nicht erfasst sind
- NUR nach klaren Mustern: `TODO:`, `offen:`, `neuer punkt:`, `neue aufgabe:`,
  `später:`, klare Problemformulierungen mit Handlungsbezug
- NICHT jede Erwähnung eines Problems als neuen Task interpretieren

### Schritt 3: Batch-Abschluss (Auswahlfrage!)

Strukturierte Übersicht im Chat zeigen:

```
### ClickUp Tracker — Batch-Abschluss

**Im Chat erledigt — als Done markieren?**
- <PRÄFIX>-003 | DB-Anbindung Orchestrator        (Beispiel BPM; Heidi: DX-031 | KARTE | 4.4 dx-planer …)
- <PRÄFIX>-007 | CS8629 Warning behoben
- <PRÄFIX>-012 | Token-Migration

**Im Chat neu erkannt — Task anlegen?**
- PlanManager — <neues Problem aus diesem Chat>
- Docs — <neuer Doc-Punkt>

**Weiterhin offen laut ClickUp:**
PlanManager (4):
- [high] [V1] BPM-004 | 5998er Statikplaene Erkennung
- [normal] [V1] BPM-008 | Mockup ManuellSortieren
...
Docs (1):
- [normal] [V1-Nice] BPM-015 | ADR-050 schreiben
```

Dann **zwei Auswahlfragen** (multiSelect):

**Erster Aufruf — Done-Markierungen:**
```
ask_user_input_v0(
  questions: [{
    question: "Welche Tasks als Done markieren?",
    type: "multi_select",
    options: [
      "BPM-003 | DB-Anbindung Orchestrator",
      "BPM-007 | CS8629 Warning behoben",
      "BPM-012 | Token-Migration",
      "Keine"
    ]
  }]
)
```

**Zweiter Aufruf — Neue Tasks:**
```
ask_user_input_v0(
  questions: [{
    question: "Welche neuen Tasks anlegen?",
    type: "multi_select",
    options: [
      "PlanManager — <neues Problem>",
      "Docs — <neuer Doc-Punkt>",
      "Keine"
    ]
  }]
)
```

### Schritt 4: Nach Bestätigung ausführen

- Done-Tasks: `tracker done` pro ausgewähltem Task (Status laut Übergängen des Projekts – Heidi `testing`, BPM `done`; Commit-Felder bzw. Kommentar)
- Neue Tasks: `tracker neu` pro ausgewähltem Task (Fragemodus per Auswahlfrage im tracker-Skill, Präfix des Projekts)
- Cowork: Memory `[CLICKUP]` Eintrag aktualisieren: `Letzte Sync: Teil <N>`; Claude Code: `Next` im Tracker-Profil, wenn Tasks angelegt wurden

### ClickUp nicht erreichbar?

Per Auswahlfrage:
```
Frage: "ClickUp nicht erreichbar. Wie weiter?"
Optionen: "Trotzdem Prompt erstellen", "Retry", "Abbrechen"
```

Bei "Trotzdem Prompt erstellen": Hinweis in Prompt einfügen, Übergabe aus Chat-Verlauf.

---

## Memory-Scan (PFLICHT bei Handover)

**Zweck:** Offene Merker, Verifikationen und Architektur-Fragen aus Memory in den Handover-Prompt übernehmen, damit sie nicht zwischen Chats verloren gehen.

**Claude Code:** Das Memory ist ein Ordner mit Dateien (Typen `user`/`feedback`/`project`/`reference`) und
bleibt über Sitzungen erhalten – es muss **nicht** in den Prompt kopiert werden. Stattdessen: offene Punkte,
die nur im Chat entstanden sind, gehören in den Doc-Ort des Doku-Profils (Heidi: HANDOFF Abschnitt 4 /
Bauplan Abschnitt 10), erledigte Merker werden mit Herberts Bestätigung als Datei entfernt. Die Schritte 1–6
unten gelten für den Cowork-Chat.

### Schritt 1: Memory lesen (Cowork)

```
memory_user_edits(command: "view")
```

### Schritt 2: Nach 4 Rubriken filtern

Nur Einträge mit diesen Prefixen berücksichtigen:

- `[VERIFY]` — ausstehende Prüfung / Verifikation
- `[ARCH-OPEN]` — offene Architektur- oder Systementscheidung
- `[INFRA-TODO]` — kleine Infrastruktur-/Prozessaufgabe, nicht ClickUp-würdig
- `[REVIEW-PENDING]` — externe Rückmeldung oder Review-Antwort steht noch aus

### Schritt 3: NICHT übernehmen

Folgende Memory-Einträge gehören NICHT in den Handover:

- `[CLICKUP]`-Einträge (sind Projekt-Konvention, bleiben dauerhaft)
- `[SKILL-ISSUES]`-Einträge (Skill-Konvention, bleiben dauerhaft)
- `[ANKER-LIVE]`-Einträge (werden separat in Chat-Anker-Übergabe behandelt)
- Dauerhafte Konventions-Einträge ohne Rubrik-Prefix

### Schritt 4: Eskalations-Hinweis

Für jeden `[VERIFY]`- oder `[INFRA-TODO]`-Eintrag prüfen:

- Ist der Eintrag in 3 aufeinanderfolgenden Handovern aufgetaucht?
- Wenn ja: im Handover-Prompt kennzeichnen mit:
  > "Dieser Punkt war jetzt in 3 Übergaben offen. Prüfen, ob ClickUp-Task sinnvoll ist."

**Zusätzlich Fragilitäten-Check** (siehe
[docs/fragilitaeten-und-fruehwarn.md](../../docs/fragilitaeten-und-fruehwarn.md)):

Vier Fragilitäten mit dokumentierten Indikatoren werden gegen den
Chat-Verlauf geprüft. Bei Treffern wird eine Eskalationsempfehlung in den
Übergabeprompt aufgenommen:

| Fragilität | Hauptsignal |
|---|---|
| 1. cc-steuerung-Pfad-/Modalitätsfragilität | Codeblöcke statt Dateioperation, hartkodierte Pfade, `$`-Variablen |
| 2. Tracker-Anker / Task-Scope-Disziplin | Fehlender `[<PRÄFIX>-ANCHOR-…]`, `tracker done` ohne Hash, Multi-Task-Commit |
| 3. Memory-Schatten-Backlog | 5+ offene `[VERIFY]`/`[INFRA-TODO]`, 3-Handovers-Wiederkehr |
| 4. Frühphasen-Verstoss | Migration-/Legacy-Vorschläge, Backward-Compat-Logik ohne Auftrag |

Volldoku inklusive Sofortmaßnahmen und Beispielen:
[docs/fragilitaeten-und-fruehwarn.md](../../docs/fragilitaeten-und-fruehwarn.md).

### Schritt 5: Vor Prompt-Abschluss prüfen

Vor dem Finalisieren des Prompts:

1. Einträge durchgehen: Wurde in diesem Chat einer erledigt?
2. Wenn ja: Herbert fragen (per Auswahlfrage):
   > "Folgende Memory-Punkte wurden in diesem Chat bearbeitet. Entfernen?"
3. Bei Bestätigung: `memory_user_edits(command: "remove")` pro Eintrag
4. **Nie stillschweigend entfernen**

### Schritt 6: Sektion in Handover-Prompt erzeugen

Gemeinsamer Block (NICHT pro Rubrik eigener H2-Block):

```markdown
## Offene Punkte aus Memory

### VERIFY
- [Eintragstext]

### ARCH-OPEN
- [Eintragstext]

### INFRA-TODO
- [Eintragstext]

### REVIEW-PENDING
- [Eintragstext]
```

**Leere Rubriken weglassen** — nicht als leere H3-Header einfügen.

Wenn KEINE Rubrik Einträge hat: komplette Sektion `## Offene Punkte aus Memory` weglassen.

---

## Chat-Anker-Übergabe (nur Cowork)

**Zweck:** Die Live-Registry `[ANKER-LIVE]` (aus dem Chat-Anker-System, siehe tracker-Skill) muss beim Chat-Wechsel in den neuen Chat transportiert werden, weil Memory pro Session gilt. Anker-Präfix = Projekt-Präfix (`clickup-lists.md`). In Claude Code gibt es keine Anker-Registry – Abschnitt entfällt.

### Schritt 1: `[ANKER-LIVE]` aus Memory lesen

```
memory_user_edits(command: "view")
→ alle Zeilen mit Prefix "[ANKER-LIVE]" herausfiltern
```

### Schritt 2: Einträge klassifizieren

- Typ `offen` → TEMP-Anker ohne Task (Phase 1 Ausarbeitung)
- Typ `erstellt` → Task existiert, aber noch nicht erledigt
- Typ `erledigt` → sollte eigentlich nicht auftauchen (wird bei `tracker done` entfernt)

Alle Einträge werden in den Übergabeprompt übernommen — im neuen Chat stellt Claude sie wieder her.

### Schritt 3: Sektion "Offene Anker" in Übergabeprompt

```markdown
## Offene Anker aus Teil N

Folgende IDs wurden im Chat gesetzt und sind noch nicht abgeschlossen:

| ID | Typ | Thema |
|----|-----|-------|
| TEMP-01JS7KABCD | offen | Wetter-Modul GS-Worker (noch kein Task) |
| 86c9eupfk | erstellt | tracker-Skill Anker-Logik (<PRÄFIX>-NNN) |

Claude im neuen Chat: Diese Einträge in `[ANKER-LIVE]` übernehmen via
`memory_user_edits` (add pro Zeile).
```

### Schritt 4: Nach Prompt-Erstellung — Memory leeren

Alle `[ANKER-LIVE]`-Einträge des alten Chats aus Memory entfernen:

```
memory_user_edits(command: "remove", line_number: <N>)
```

Pro Eintrag einen Remove-Call. Die Daten reisen per Übergabeprompt — nicht per Memory — in den neuen Chat.

### Keine Anker vorhanden?

Sektion komplett weglassen. Nicht als leere Tabelle in den Prompt schreiben.

---

## Link-Prüfung (PFLICHT vor der Ausgabe)

Jeder Verweis im Prompt muss stimmen, sonst startet die nächste Sitzung mit falschen Annahmen
(Beispiel: `heidi-panel-v2.js`, das seit dem Umbau `dreame_x60.js` heißt).

1. **Dateien und Pfade:** jede genannte Datei existiert (Claude Code: Glob; Cowork: DC `list_directory`)
2. **Abschnitte:** genannte Kapitel/Abschnitte existieren in der Datei (Grep auf die Überschrift)
3. **Task-IDs:** jede `<PRÄFIX>-NNN` existiert im Tracker mit dem genannten Status (tracker read-only, `clickup_get_task`)
4. **Versionen:** Version im Prompt = Versionsquelle des Commit-Profils (Heidi: package.json)
5. Tote Verweise → Auswahlfrage „Korrigieren / Mit Warnung übernehmen / Weglassen“; nie stumm übernehmen

---

## ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt)

1. **doc-pflege Modus 8 (Sitzungsabschluss)** ausführen: Statusliste/Aufgabenquelle ↔ Tracker, Befunde und
   Entscheidungen, Stand-Abschnitt (Heidi: HANDOFF 3e), offene Punkte als Checkliste (HANDOFF 4), Doku-Checkliste
   des Commit-Profils, Commit + Push nach der Push-Policy (Grundsätze). Uncommittete Änderungen → Auswahlfrage.
2. **ClickUp-Abgleich** wie oben (Batch-Abschluss über tracker), **Memory**: erledigte Merker mit Bestätigung entfernen.
3. **Link-Prüfung** auf den Stand-Abschnitt und den Startprompt.
4. **Handover-Prompt nach PROMPT-STRUKTUR ausgeben** (vollständig, als Markdown-Codeblock). Erste Zeile darin ist
   der Startprompt des Doku-Profils, z.B.:

```
> Lies CLAUDE.md, docs/HANDOFF.md (Abschnitt 3e + 4) und docs/dreame_x60/BAUPLAN.md. Nimm die nächste offene
> Aufgabe aus der Statusliste (Abschnitt 1): <DX-NNN | Kürzel | Schritt>. Prüfe Voraussetzungen, lies ihre Karte
> in Abschnitt 8 und arbeite nur diese Aufgabe ab (Skills: tracker start, code-erstellen nach Code-Profil).
> Regeln: Abschnitt 2. Widerspruch Code ↔ Bauplan → Befund in Abschnitt 10, Aufgabe blockiert, stoppen.
```

   Quelle des Musters: Feld „Startprompt“ im Doku-Profil (Heidi: Bauplan Abschnitt 0). Danach folgen die
   Abschnitte der PROMPT-STRUKTUR: Aktueller Stand, Erledigt in dieser Sitzung, Offene Punkte (ClickUp nach
   Status, Chat, Sonstiges), Nächste Schritte, Aktive Entscheidungen, Kontext/Warnungen, Regeln aus den Profilen.
   Memory-Sektion: in Claude Code die relevanten Memory-Dateien nennen (Titel), nicht kopieren.
5. Fertig. Kurzform (nur Startprompt) nur auf ausdrücklichen Wunsch.

---

## PROMPT-STRUKTUR (beide Umgebungen)

```
# [Projektname] Teil [N+1]

Weiterführung aus **[Projektname] Teil [N]**.

---

## Aktueller Stand
- **App-Version:** [Version]
- **Letzter Commit:** [Hash + Message]
- **Branch:** [Branch]
- **Chat-URL Teil [N]:** [aktuelle Chat-URL falls bekannt]

## Erledigt in Teil [N]
- [Erledigte Punkte/Commits]

## Offene Punkte (aus ClickUp + Chat)

### ClickUp offen (BPM: nach Liste gruppiert; Ein-Listen-Projekte: nach Status):
PlanManager:
- [Priority] [Meilenstein] <PRÄFIX>-NNN | Beschreibung
Docs:
- [Priority] [Meilenstein] <PRÄFIX>-NNN | Beschreibung
(nur Listen/Status mit offenen Tasks auflisten)

### Offene Anker aus Teil [N] (aus [ANKER-LIVE]):
| ID | Typ | Thema |
|----|-----|-------|
| TEMP-xxx | offen | Thema (noch kein Task) |
| 86c9xxx | erstellt | Thema (<PRÄFIX>-NNN) |
(nur wenn Einträge vorhanden — sonst Sektion weglassen; nur Cowork)

### Offene Punkte aus Memory (gefiltert nach Rubriken):

#### VERIFY
- [Eintragstext]

#### ARCH-OPEN
- [Eintragstext]

#### INFRA-TODO
- [Eintragstext]

#### REVIEW-PENDING
- [Eintragstext]
(leere Rubriken weglassen; wenn alle leer: ganze Sektion weglassen)

### Im Chat neu erkannt (noch nicht in ClickUp):
- Modul — Beschreibung

### Im Chat erledigt (noch nicht in ClickUp markiert):
- <PRÄFIX>-NNN | Beschreibung

### Sonstige offene Punkte (nicht in ClickUp):
- [Pending Commits]
- [Pending Doc-Updates]
- [Pending Frontmatter/Quickload-Updates]
- [Neue Fachliche Invarianten die noch eingetragen werden müssen]

## Nächste Schritte (geplant)
- [Prioritäten — basierend auf V1 + high/urgent zuerst]

## Aktive Entscheidungen
- [Architektur-Entscheidungen]
- [Offene Fragen]

## Kontext
- [Wichtige Erkenntnisse]
- [Warnungen]
- [Docs die gelesen werden sollten]
- [Docs deren Quickload/Invarianten veraltet sein könnten]

## Regeln (Erinnerung) — aus den Profilen der CLAUDE.md erzeugt, nicht fest
- Commit: <Format, Modul-Namen, Versionsquelle, Bump-Regel aus dem Commit-Profil>
- Tracker: <Präfix, Liste, Übergänge aus dem Tracker-Profil>; tracker-Skill ist einzige Schreibschnittstelle zu ClickUp
- Docs: <Pflicht-Docs, Ladereihenfolge, Aufgabenquelle aus dem Doku-Profil>
- Code: <Testbefehl, Pflicht-Branch, Auslieferung aus dem Code-Profil>
- Ein Schritt pro Antwort; nachfragen wenn Kontext fehlt → Auswahlfrage bei festen Optionen
- Wer committet: Cowork der User; Claude Code Claude selbst
(BPM ohne Profile: User committet und pusht selbst · Commit-Format [vX.Y.Z] Modul, Typ: Kurztitel · Docs Quickload-First-Pass →
Pflichtlesen → Langform · DOC-STANDARD.md · ClickUp Space "BPM Entwicklung" ist Source of Truth · Task-Nummern BPM-NNN)
```

---

## Chat-URL in Übergabe-Prompt (nur Cowork)

Die URL des aktuellen Chats (der gerade endet) wird in den Übergabe-Prompt unter `**Chat-URL Teil [N]:**` geschrieben, damit sie im nächsten Chat für Nachpflege (z.B. tracker done bei retrospektiven Tasks) verfügbar ist.

Ermittlung der aktuellen Chat-URL:

1. Wenn User die URL am Chat-Start oder während der Session gepostet hat → verwenden
2. Sonst: `recent_chats(n: 1, sort_order: "desc")` aufrufen
   - Oberster Treffer sollte dieser Chat sein (wenn indexiert)
   - Prüfen ob der Inhalt passt (Chat-Titel, letzte Nachrichten)
3. Wenn keine URL ermittelbar: Feld im Prompt leer lassen + Hinweis

**Nicht raten.** Lieber Feld leer als falsche URL.

---

## REGELN

1. Automatisch sammeln — nicht nachfragen was rein soll
2. Chat-Nummer korrekt — N+1
3. Nichts vergessen — inkl. pending Frontmatter, neue Invarianten
4. Kompakt aber vollständig
5. Kopierfähig als Markdown-Codeblock
6. Version prüfen
7. Keine Datei — direkt im Chat; Claude Code: zusätzlich vorher Stand ins Repo (Modus 8)
8. Pending Quickload-Änderungen explizit nennen
9. **ClickUp-Abgleich VOR Übergabeprompt** — offene Tasks laden + Chat scannen
10. **Batch-Abschluss per Auswahlfrage** (nicht Prosa-Liste)
11. **Keine automatischen ClickUp-Mutationen ohne Auswahlfrage-Bestätigung**
12. **Nächste Schritte basierend auf V1 + Priority ableiten**
13. **Sonstige offene Punkte** (Pending Commits, Frontmatter, Invarianten) ZUSÄTZLICH zu ClickUp auflisten
14. **Aktuelle Chat-URL** in Übergabe-Prompt einfügen (für Nachpflege)
15. **`[ANKER-LIVE]` aus Memory in Übergabeprompt kopieren** und danach aus Memory leeren — Anker reisen per Prompt, nicht per Memory
16. **Memory-Scan nach 4 Rubriken** (`[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]`, `[REVIEW-PENDING]`) durchführen und als Sektion `## Offene Punkte aus Memory` in Prompt einfügen
17. **Memory-Cleanup nur mit Bestätigung** — bei Einträgen die in diesem Chat bearbeitet wurden per Auswahlfrage fragen, nie stillschweigend entfernen
18. **Link-Prüfung vor der Ausgabe** — Dateien, Abschnitte, Task-IDs, Version (Abschnitt „Link-Prüfung“)
19. **Regeln-Block aus den Profilen** erzeugen, nicht aus einer festen Liste
20. **Claude Code: erst doc-pflege Modus 8, dann vollständiger Handover-Prompt** — Kurzform nur auf Wunsch; Details verweisen auf HANDOFF/Bauplan statt sie zu kopieren

---

## VERBOTEN

- Nachfragen was rein soll (Prosa)
- Offene Punkte vergessen
- Als Datei liefern
- Ohne Version/Chat-Nummer
- Nummern verwechseln
- Pending Frontmatter/Invarianten vergessen
- Branch automatisch annehmen – ohne Branch-Policy, Shell oder Auswahlfrage
- **Prosa-Fragen bei festen Entscheidungsoptionen** — IMMER Auswahlfrage (Branch-Auswahl, Batch-Abschluss, "ja/nein/einzeln wählen")
- **Tasks automatisch in ClickUp erstellen/schließen ohne Auswahlfrage-Bestätigung**
- **ClickUp-Schreiboperationen direkt ausführen (→ tracker-Skill nutzen)**
- **Pending Commits/Doc-Updates/Frontmatter-Updates vergessen nur weil ClickUp da ist**
- Chat-URLs raten oder erfinden — bei Unsicherheit Feld leer lassen
- **`[ANKER-LIVE]`-Einträge im alten Chat-Memory belassen nach Übergabe** — müssen geleert werden
- **Anker-Sektion im Prompt als leere Tabelle einfügen wenn keine Anker vorhanden** — dann Sektion komplett weglassen
- **`[CLICKUP]`- oder `[SKILL-ISSUES]`-Memories in Handover-Prompt übernehmen** — das sind dauerhafte Konventionen, nicht offene Punkte
- **Rubriken `[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]`, `[REVIEW-PENDING]` als leere H3-Blöcke einfügen** wenn Rubrik keine Einträge hat
- **Memory-Einträge stillschweigend entfernen nach Abschluss** — Herbert muss explizit bestätigen
- **Prompt mit toten Verweisen ausgeben** (umbenannte Dateien, fehlende Abschnitte, falsche Task-IDs oder Version)
- **BPM-Regeln oder BPM-NNN in den Prompt eines anderen Projekts schreiben** — Regeln und Präfix aus den Profilen
- **In Claude Code den Stand nur in den Prompt schreiben statt ins Repo** (HANDOFF/Bauplan) — Modus 8 kommt immer zuerst
- **In Claude Code ungefragt nur den kurzen Startprompt liefern** — der User erwartet den vollständigen Handover-Prompt
- **Sitzung mit uncommitteten Änderungen übergeben** ohne Auswahlfrage
