# Regel-Inventar – chat-wechsel – Refactor Aufteilung in References

Refactor nach dem Ablauf von skill-pflege, Abschnitt Refactor (`skills/skill-pflege/references/rule-inventory.md`).
Anlass: SKILL.md lag mit 536 Zeilen über dem Richtwert von 500 Zeilen (`docs/skill-quality.md`, Abschnitt Aufbau); Abläufe
für eine Umgebung (Cowork) und eine Integration (ClickUp) gehören in References. Zielstruktur von Herbert freigegeben:
**nur verschieben, nichts streichen** – keine DROP-Zeilen; Doppelungen bleiben erhalten.

- Skill: chat-wechsel
- Stand vorher: b9dce9e (SKILL.md, 536 Zeilen; `references/neues-fenster.md`, 37 Zeilen)
- Quellen: SKILL.md, references/neues-fenster.md
- Vorsammeln: Das Prüfskript (PowerShell) läuft auf dem HA nicht (`CLAUDE.md`, Abschnitt „Arbeiten auf dem HA“). Die
  Kandidaten wurden mit einem Skript im Scratchpad nach denselben Regeln gesammelt (Description, Sätze mit Pflichtwörtern,
  Listenpunkte, nummerierte Punkte, Tabellenzeilen, nummerierte Überschriften; 211 Kandidaten im alten Stand) und nach
  Urteil ergänzt (u. a. die Abschnitte im Codeblock PROMPT-STRUKTUR, die als Pflichtformat gelten).

## Zielstruktur

| Datei | Zeilen | Abschnitte |
|---|---|---|
| `SKILL.md` | 236 | Frontmatter (zeichengleich) · Zweck · Vorrang / Delegation an andere Skills · Grundsätze (Fragen, Branch, Push) · TRIGGER · **Fall → Reference** (neu) · Memory-Scan (PFLICHT bei Handover): Zweck und Claude-Code-Teil · ABLAUF IN CLAUDE CODE · **Ablauf im Cowork-Chat** (neu, nur Verweise) · Link-Prüfung (PFLICHT vor der Ausgabe) · REGELN (1–20) · VERBOTEN (alle Punkte, Reihenfolge unverändert) |
| `references/prompt-struktur.md` | 87 | PROMPT-STRUKTUR (beide Umgebungen): der Codeblock wörtlich |
| `references/tracker-abgleich.md` | 93 | ClickUp-Integration (vor Übergabeprompt): Schritt 1–4, Batch-Abschluss mit den Beispielen der Auswahlfragen, ClickUp nicht erreichbar? |
| `references/cowork.md` | 165 | Inhalt · Memory-Scan (PFLICHT bei Handover) mit Schritt 1–6 (Rubriken, NICHT übernehmen, Eskalations-Hinweis mit Fragilitäten-Check, Link auf `../../../docs/fragilitaeten-und-fruehwarn.md`) · Chat-Anker-Übergabe (nur Cowork) · Chat-URL in Übergabe-Prompt (nur Cowork) |
| `references/neues-fenster.md` | 37 | unverändert |

In den References sind die Unterüberschriften eine Ebene höher gerückt, wo der alte Abschnitt zum Titel der Datei wurde
(tracker-abgleich, prompt-struktur); der Text ist sonst wörtlich. Jede Reference ist aus SKILL.md direkt verlinkt
(Tabelle „Fall → Reference“ und die Abläufe); `references/cowork.md` hat als einzige Reference über 100 Zeilen ein
Inhaltsverzeichnis.

Abkürzungen im Neu-Ort: `S` = `SKILL.md`, `PS` = `references/prompt-struktur.md`, `TA` = `references/tracker-abgleich.md`,
`CO` = `references/cowork.md`, `NF` = `references/neues-fenster.md`.

Zustände: KEEP = wörtlich in derselben Datei unter derselben Überschrift (auch wenn der Abschnitt innerhalb von SKILL.md
die Position gewechselt hat); MOVE = wörtlich oder fast wörtlich in eine Reference; REWRITE = nur der Verweis im Satz
ist neu formuliert. MERGE kommt nicht vor: Doppelungen bleiben laut Freigabe an beiden Stellen stehen; die Spalte Bezug
nennt die andere Stelle („Doppelung mit …“). Keine DROP-Zeilen.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#Frontmatter (Z. 1–10) | Description: Übergabe an die nächste Sitzung (Handover-Prompt, in Claude Code vorher Sitzungsabschluss); Use when …; Do not trigger for ChatGPT-Review-Prompts, generische Prompts, Verabschiedungen | KEEP | S#Frontmatter | zeichengleich |  | ✅ |
| R002 | SKILL.md#Zweck (Z. 16) | Übergabe, wenn eine Sitzung endet und in der nächsten weitergearbeitet wird; zwei Wege, ein Ziel | KEEP | S#Zweck |  |  | ✅ |
| R003 | SKILL.md#Zweck (Z. 18–19) | Cowork-Chat: Handover-Prompt im Chat nach PROMPT-STRUKTUR; der Prompt trägt den Stand | REWRITE | S#Zweck | „(PROMPT-STRUKTUR unten)“ → Verweis auf `references/prompt-struktur.md` |  | ✅ sinngemäß |
| R004 | SKILL.md#Zweck (Z. 20–21) | Claude Code: erst doc-pflege Modus 8 (Statusliste, Befunde, Stand, offene Punkte, Commit + Push nach Push-Policy), dann derselbe vollständige Handover-Prompt | KEEP | S#Zweck |  |  | ✅ |
| R005 | SKILL.md#Zweck (Z. 22) | Begründung: Zitat Herbert vom 16.09.2026 zum Umfang des Prompts | KEEP | S#Zweck | Historie im Regeltext (Prüfskript-Warnung) – DROP-Kandidat, bleibt laut Auftrag |  | ✅ |
| R006 | SKILL.md#Zweck (Z. 22–23) | Prompt darf den Repo-Stand zusammenfassen, verweist für Details auf HANDOFF/Bauplan statt zu kopieren | KEEP | S#Zweck | Doppelung mit R158 |  | ✅ |
| R007 | SKILL.md#Zweck (Z. 23–24) | Startprompt des Doku-Profils steht als Einstiegszeile im Prompt | KEEP | S#Zweck | Doppelung mit R107 |  | ✅ |
| R008 | SKILL.md#Zweck (Z. 25) | Kurzform (nur Startprompt) nur auf ausdrücklichen Wunsch | KEEP | S#Zweck | Doppelung mit R112, R158, R179 |  | ✅ |
| R009 | SKILL.md#Zweck (Z. 27–28) | Projektwerte aus den Profilen der CLAUDE.md; ohne Profil gilt der BPM-Weg (Memory `[CLICKUP]`, INDEX.md) | KEEP | S#Zweck | Projektwert BPM im Kern – DROP-Kandidat |  | ✅ |
| R010 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 34–36) | Hauptabsicht ChatGPT-Review- oder anderer Prompt → nicht hier weiterarbeiten, delegieren | KEEP | S#Vorrang / Delegation an andere Skills |  |  | ✅ |
| R011 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 40) | ChatGPT-Review-Prompt → chatgpt-review | KEEP | S#Vorrang / Delegation an andere Skills |  |  | ✅ |
| R012 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 41) | Code schreiben → code-erstellen | KEEP | S#Vorrang / Delegation an andere Skills |  |  | ✅ |
| R013 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 42) | ClickUp-Task-Aktion → tracker | KEEP | S#Vorrang / Delegation an andere Skills |  |  | ✅ |
| R014 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 43) | Doc schreiben → doc-pflege | KEEP | S#Vorrang / Delegation an andere Skills |  |  | ✅ |
| R015 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 45–47) | Nur bei Hauptabsicht Handover-Prompt für den nächsten Claude-Chat bleibt chat-wechsel zuständig | KEEP | S#Vorrang / Delegation an andere Skills |  |  | ✅ |
| R016 | SKILL.md#Vorrang / Delegation an andere Skills (Z. 49–52) | chat-wechsel und chatgpt-review können nacheinander laufen, lösen nicht gemeinsam auf einen Satz aus; der User-Intent entscheidet | KEEP | S#Vorrang / Delegation an andere Skills |  |  | ✅ |
| R017 | SKILL.md#Grundsätze (Z. 58–59) | Fragen nur bei offener Entscheidung, dann als Auswahlfrage | KEEP | S#Grundsätze |  |  | ✅ |
| R018 | SKILL.md#Grundsätze (Z. 63) | Tote Verweise der Link-Prüfung → Korrigieren / Mit Warnung übernehmen / Weglassen | KEEP | S#Grundsätze | Doppelung mit R103 |  | ✅ |
| R019 | SKILL.md#Grundsätze (Z. 64) | Claude Code: uncommittete Änderungen beim Abschluss → Jetzt committen / Als offen vermerken / Abbrechen | KEEP | S#Grundsätze | Doppelung mit R104, R180 |  | ✅ |
| R020 | SKILL.md#Grundsätze (Z. 65) | Batch-Abschluss erledigter Tasks → Alle als Done / Einzeln wählen / Keine | KEEP | S#Grundsätze |  |  | ✅ |
| R021 | SKILL.md#Grundsätze (Z. 66) | Batch-Abschluss einzeln → Mehrfachauswahl mit allen Task-Namen | KEEP | S#Grundsätze |  |  | ✅ |
| R022 | SKILL.md#Grundsätze (Z. 67) | Batch-Anlage neuer Tasks → Alle anlegen / Einzeln wählen / Keine | KEEP | S#Grundsätze |  |  | ✅ |
| R023 | SKILL.md#Grundsätze (Z. 68) | Batch-Anlage einzeln → Mehrfachauswahl mit allen erkannten Problemen | KEEP | S#Grundsätze |  |  | ✅ |
| R024 | SKILL.md#Grundsätze (Z. 69) | ClickUp nicht erreichbar → Trotzdem Prompt erstellen / Retry / Abbrechen | KEEP | S#Grundsätze | Doppelung mit R056 |  | ✅ |
| R025 | SKILL.md#Grundsätze (Z. 70) | Version-Angabe unklar → aktuelle Versionen als Optionen | KEEP | S#Grundsätze |  |  | ✅ |
| R026 | SKILL.md#Grundsätze (Z. 71) | Kein Commit-Stand erkennbar → Version vom User eingeben / Ohne Version / Abbrechen | KEEP | S#Grundsätze |  |  | ✅ |
| R027 | SKILL.md#Grundsätze (Z. 73–74) | Prosa nur bei offener Frage ohne feste Optionen, klar signalisierter Präferenz oder Erklärung ohne Entscheidung | KEEP | S#Grundsätze |  |  | ✅ |
| R028 | SKILL.md#Grundsätze (Z. 75–77) | Branch nach Branch-Policy: `current` → aktueller Branch aus der Shell; `fixed:<branch>` → muss dieser sein, sonst Auswahlfrage (wechseln / abbrechen) | KEEP | S#Grundsätze |  |  | ✅ |
| R029 | SKILL.md#Grundsätze (Z. 77) | Ohne Shell: bei `fixed:<branch>` dieser Branch, bei `current` Auswahlfrage | KEEP | S#Grundsätze |  |  | ✅ |
| R030 | SKILL.md#Grundsätze (Z. 77–79) | Ohne Skill-Profil: bekannter Branch; sonst Shell; ohne Shell Branches über die GitHub API per Auswahlfrage | KEEP | S#Grundsätze |  |  | ✅ |
| R031 | SKILL.md#Grundsätze (Z. 79–80) | NIE automatisch einen Branch annehmen | KEEP | S#Grundsätze | Doppelung mit R165 |  | ✅ |
| R032 | SKILL.md#Grundsätze (Z. 80) | Branch für die Sitzung merken und im Prompt unter `**Branch:**` eintragen | KEEP | S#Grundsätze |  |  | ✅ |
| R033 | SKILL.md#Grundsätze (Z. 81–82) | Push nach Push-Policy – `user-only`: kein Push, der Nutzer pusht selbst | KEEP | S#Grundsätze |  |  | ✅ |
| R034 | SKILL.md#Grundsätze (Z. 83) | `allowed`: Push nur auf ausdrücklichen Wunsch | KEEP | S#Grundsätze |  |  | ✅ |
| R035 | SKILL.md#Grundsätze (Z. 84) | `required-after-commit`: Push direkt nach dem Commit des Sitzungsabschlusses | KEEP | S#Grundsätze |  |  | ✅ |
| R036 | SKILL.md#Grundsätze (Z. 85) | `required-at-session-end`: alle Commits der Sitzung vor dem Handover-Prompt pushen | KEEP | S#Grundsätze |  |  | ✅ |
| R037 | SKILL.md#Grundsätze (Z. 87) | Ohne Push-Policy (kein Skill-Profil): Commit + Push im Sitzungsabschluss | KEEP | S#Grundsätze |  |  | ✅ |
| R038 | SKILL.md#Grundsätze (Z. 89–90) | Ungepushte Commits (`user-only`, `allowed`) unter „Sonstige offene Punkte“ mit Hash, Titel, „Push durch den Nutzer“ | KEEP | S#Grundsätze |  |  | ✅ |
| R039 | SKILL.md#TRIGGER (Z. 96–98) | Auslöser: neuer chat, nächster chat, session beenden, chat wechsel, übergabe, neue sitzung … | KEEP | S#TRIGGER |  |  | ✅ |
| R040 | SKILL.md#TRIGGER (Z. 100) | Kein Auslöser: pause, tschüss, gute nacht | KEEP | S#TRIGGER |  |  | ✅ |
| R041 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) (Z. 104) | ClickUp-Abgleich läuft vor dem Übergabeprompt (Überschrift) | MOVE | TA#ClickUp-Integration (vor Übergabeprompt) | Überschrift wird Titel der Reference; Doppelung mit R147 |  | ✅ |
| R042 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 1: Offene Tasks laden (Z. 108) | Space/Listen-ID und Präfix aus dem Tracker-Profil (Claude Code) bzw. Memory `[CLICKUP]` (Cowork) | MOVE | TA#Schritt 1: Offene Tasks laden | Begriff „Tracker-Profil“ veraltet (Skill-Profil → Tracker.Config) – Auffälligkeit |  | ✅ |
| R043 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 1: Offene Tasks laden (Z. 109) | Offene Tasks read-only über den tracker-Skill laden (Status laut `projects/<name>/clickup-lists.md`) | MOVE | TA#Schritt 1: Offene Tasks laden | `projects/` ist Altlast – Auffälligkeit |  | ✅ |
| R044 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 1: Offene Tasks laden (Z. 110) | Gruppieren: mehrere Listen → nach Liste; eine Liste → nach Status | MOVE | TA#Schritt 1: Offene Tasks laden |  |  | ✅ |
| R045 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 2: Chat-Verlauf scannen (Z. 114–115) | Chat scannen auf bearbeitete, nicht als Done markierte Tasks | MOVE | TA#Schritt 2: Chat-Verlauf scannen |  |  | ✅ |
| R046 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 2: Chat-Verlauf scannen (Z. 116) | Chat scannen auf neue, nicht erfasste Probleme | MOVE | TA#Schritt 2: Chat-Verlauf scannen |  |  | ✅ |
| R047 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 2: Chat-Verlauf scannen (Z. 117–118) | NUR nach klaren Mustern (`TODO:`, `offen:`, `neuer punkt:` …, Problem mit Handlungsbezug) | MOVE | TA#Schritt 2: Chat-Verlauf scannen |  |  | ✅ |
| R048 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 2: Chat-Verlauf scannen (Z. 119) | NICHT jede Erwähnung eines Problems als neuen Task deuten | MOVE | TA#Schritt 2: Chat-Verlauf scannen |  |  | ✅ |
| R049 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 3: Batch-Abschluss (Auswahlfrage!) (Z. 121–144) | Batch-Abschluss: strukturierte Übersicht im Chat (Done?, neu anlegen?, weiterhin offen laut ClickUp) | MOVE | TA#Schritt 3: Batch-Abschluss (Auswahlfrage!) |  |  | ✅ |
| R050 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 3: Batch-Abschluss (Auswahlfrage!) (Z. 146) | Danach zwei Auswahlfragen mit Mehrfachauswahl | MOVE | TA#Schritt 3: Batch-Abschluss (Auswahlfrage!) |  |  | ✅ |
| R051 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 3: Batch-Abschluss (Auswahlfrage!) (Z. 148–162) | Erste Auswahlfrage: welche Tasks als Done (Beispiel mit Option „Keine“) | MOVE | TA#Schritt 3: Batch-Abschluss (Auswahlfrage!) | Werkzeug-Syntax `ask_user_input_v0` (Prüfskript-Warnung) – DROP-Kandidat wie Gruppe A im Refactor vom 28.09. |  | ✅ |
| R052 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 3: Batch-Abschluss (Auswahlfrage!) (Z. 164–177) | Zweite Auswahlfrage: welche neuen Tasks anlegen (Beispiel mit Option „Keine“) | MOVE | TA#Schritt 3: Batch-Abschluss (Auswahlfrage!) | wie R051 – DROP-Kandidat |  | ✅ |
| R053 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 4: Nach Bestätigung ausführen (Z. 181) | Done-Tasks: `tracker done` je ausgewähltem Task (Status laut Übergängen des Projekts) | MOVE | TA#Schritt 4: Nach Bestätigung ausführen |  |  | ✅ |
| R054 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 4: Nach Bestätigung ausführen (Z. 182) | Neue Tasks: `tracker neu` je ausgewähltem Task | MOVE | TA#Schritt 4: Nach Bestätigung ausführen |  |  | ✅ |
| R055 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › Schritt 4: Nach Bestätigung ausführen (Z. 183) | Cowork: Memory `[CLICKUP]` „Letzte Sync“ aktualisieren; Claude Code: `Next` im Tracker-Profil, wenn Tasks angelegt wurden | MOVE | TA#Schritt 4: Nach Bestätigung ausführen |  |  | ✅ |
| R056 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › ClickUp nicht erreichbar? (Z. 185–191) | ClickUp nicht erreichbar → Auswahlfrage Trotzdem Prompt erstellen / Retry / Abbrechen | MOVE | TA#ClickUp nicht erreichbar? | Doppelung mit R024 |  | ✅ |
| R057 | SKILL.md#ClickUp-Integration (vor Übergabeprompt) › ClickUp nicht erreichbar? (Z. 193) | Bei „Trotzdem Prompt erstellen“: Hinweis in den Prompt, Übergabe aus dem Chat-Verlauf | MOVE | TA#ClickUp nicht erreichbar? |  |  | ✅ |
| R058 | SKILL.md#Memory-Scan (PFLICHT bei Handover) (Z. 197) | Memory-Scan ist PFLICHT bei der Übergabe (Überschrift) | KEEP | S#Memory-Scan (PFLICHT bei Handover); CO#Memory-Scan (PFLICHT bei Handover) | Überschrift steht in SKILL.md und in `references/cowork.md` |  | ✅ |
| R059 | SKILL.md#Memory-Scan (PFLICHT bei Handover) (Z. 199) | Zweck: offene Merker, Verifikationen, Architektur-Fragen aus dem Memory in den Prompt übernehmen | KEEP | S#Memory-Scan (PFLICHT bei Handover) |  |  | ✅ |
| R060 | SKILL.md#Memory-Scan (PFLICHT bei Handover) (Z. 201–202) | Claude Code: Memory ist ein Ordner, bleibt erhalten, wird nicht in den Prompt kopiert | KEEP | S#Memory-Scan (PFLICHT bei Handover) | Doppelung mit R110 |  | ✅ |
| R061 | SKILL.md#Memory-Scan (PFLICHT bei Handover) (Z. 202–204) | Claude Code: im Chat entstandene offene Punkte in den Doc-Ort des Doku-Profils | KEEP | S#Memory-Scan (PFLICHT bei Handover) |  |  | ✅ |
| R062 | SKILL.md#Memory-Scan (PFLICHT bei Handover) (Z. 204) | Claude Code: erledigte Merker mit Bestätigung als Datei entfernen | KEEP | S#Memory-Scan (PFLICHT bei Handover) | Doppelung mit R105 |  | ✅ |
| R063 | SKILL.md#Memory-Scan (PFLICHT bei Handover) (Z. 204–205) | Die Memory-Schritte gelten für den Cowork-Chat | REWRITE | S#Memory-Scan (PFLICHT bei Handover) | „Schritte 1–6 unten“ → Verweis auf `references/cowork.md`, Abschnitt Memory-Scan |  | ✅ sinngemäß |
| R064 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 1: Memory lesen (Cowork) (Z. 207–211) | Cowork: Memory lesen | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 1: Memory lesen (Cowork) |  |  | ✅ |
| R065 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 2: Nach 4 Rubriken filtern (Z. 213–215) | Nur Einträge mit den vier Rubrik-Präfixen berücksichtigen | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 2: Nach 4 Rubriken filtern | Doppelung mit R154 |  | ✅ |
| R066 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 2: Nach 4 Rubriken filtern (Z. 217) | `[VERIFY]` – ausstehende Prüfung | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 2: Nach 4 Rubriken filtern |  |  | ✅ |
| R067 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 2: Nach 4 Rubriken filtern (Z. 218) | `[ARCH-OPEN]` – offene Architektur-/Systementscheidung | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 2: Nach 4 Rubriken filtern |  |  | ✅ |
| R068 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 2: Nach 4 Rubriken filtern (Z. 219) | `[INFRA-TODO]` – kleine Infrastruktur-/Prozessaufgabe | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 2: Nach 4 Rubriken filtern |  |  | ✅ |
| R069 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 2: Nach 4 Rubriken filtern (Z. 220) | `[REVIEW-PENDING]` – externe Rückmeldung steht aus | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 2: Nach 4 Rubriken filtern |  |  | ✅ |
| R070 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 3: NICHT übernehmen (Z. 222–226) | `[CLICKUP]`-Einträge nicht übernehmen | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 3: NICHT übernehmen | Doppelung mit R173 |  | ✅ |
| R071 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 3: NICHT übernehmen (Z. 227) | `[SKILL-ISSUES]`-Einträge nicht übernehmen | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 3: NICHT übernehmen | Doppelung mit R173 |  | ✅ |
| R072 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 3: NICHT übernehmen (Z. 228) | `[ANKER-LIVE]` nicht im Memory-Block, sondern in der Chat-Anker-Übergabe | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 3: NICHT übernehmen |  |  | ✅ |
| R073 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 3: NICHT übernehmen (Z. 229) | Dauerhafte Konventions-Einträge ohne Rubrik-Präfix nicht übernehmen | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 3: NICHT übernehmen |  |  | ✅ |
| R074 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis (Z. 231–237) | `[VERIFY]`/`[INFRA-TODO]` in 3 Übergaben in Folge → im Prompt mit dem Eskalationssatz kennzeichnen | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis |  |  | ✅ |
| R075 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis (Z. 239–244) | Fragilitäten-Check: vier Fragilitäten gegen den Chat-Verlauf prüfen, bei Treffern Eskalationsempfehlung in den Prompt | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis | Linkpfad `../../docs/` → `../../../docs/` (von references/ aus) |  | ✅ |
| R076 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis (Z. 248) | Fragilität cc-steuerung-Pfad/Modalität: Codeblöcke statt Dateioperation, harte Pfade, `$`-Variablen | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis |  |  | ✅ |
| R077 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis (Z. 249) | Fragilität Tracker-Anker/Task-Scope: fehlender Anker, `tracker done` ohne Hash, Multi-Task-Commit | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis |  |  | ✅ |
| R078 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis (Z. 250) | Fragilität Memory-Schatten-Backlog: 5+ offene Einträge, 3-Handovers-Wiederkehr | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis |  |  | ✅ |
| R079 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis (Z. 251) | Fragilität Frühphasen-Verstoß: Migration/Legacy/Backward-Compat ohne Auftrag | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis |  |  | ✅ |
| R080 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis (Z. 253–254) | Volldoku der Fragilitäten verlinkt | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 4: Eskalations-Hinweis | Linkpfad `../../docs/` → `../../../docs/` |  | ✅ |
| R081 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 5: Vor Prompt-Abschluss prüfen (Z. 256–260) | Vor Prompt-Abschluss: Einträge durchgehen, ob einer im Chat erledigt wurde | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 5: Vor Prompt-Abschluss prüfen |  |  | ✅ |
| R082 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 5: Vor Prompt-Abschluss prüfen (Z. 261–262) | Wenn ja: per Auswahlfrage fragen, ob die bearbeiteten Punkte entfernt werden | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 5: Vor Prompt-Abschluss prüfen | Doppelung mit R155 |  | ✅ |
| R083 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 5: Vor Prompt-Abschluss prüfen (Z. 263) | Bei Bestätigung: je Eintrag entfernen | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 5: Vor Prompt-Abschluss prüfen |  |  | ✅ |
| R084 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 5: Vor Prompt-Abschluss prüfen (Z. 264) | Nie stillschweigend entfernen | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 5: Vor Prompt-Abschluss prüfen | Doppelung mit R155, R175 |  | ✅ |
| R085 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 6: Sektion in Handover-Prompt erzeugen (Z. 266–284) | Memory-Sektion im Prompt als gemeinsamer Block, nicht je Rubrik ein H2-Block (Format) | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 6: Sektion in Handover-Prompt erzeugen | Doppelung mit R119 |  | ✅ |
| R086 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 6: Sektion in Handover-Prompt erzeugen (Z. 286) | Leere Rubriken weglassen, keine leeren H3-Header | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 6: Sektion in Handover-Prompt erzeugen | Doppelung mit R174 |  | ✅ |
| R087 | SKILL.md#Memory-Scan (PFLICHT bei Handover) › Schritt 6: Sektion in Handover-Prompt erzeugen (Z. 288) | Keine Rubrik mit Einträgen → ganze Sektion weglassen | MOVE | CO#Memory-Scan (PFLICHT bei Handover) › Schritt 6: Sektion in Handover-Prompt erzeugen |  |  | ✅ |
| R088 | SKILL.md#Chat-Anker-Übergabe (nur Cowork) (Z. 292–294) | Nur Cowork: `[ANKER-LIVE]` muss beim Wechsel in den neuen Chat transportiert werden; Anker-Präfix = Projekt-Präfix | MOVE | CO#Chat-Anker-Übergabe (nur Cowork) | `clickup-lists.md` als Quelle veraltet – Auffälligkeit |  | ✅ |
| R089 | SKILL.md#Chat-Anker-Übergabe (nur Cowork) (Z. 294) | Claude Code: keine Anker-Registry, Abschnitt entfällt | MOVE | CO#Chat-Anker-Übergabe (nur Cowork) |  |  | ✅ |
| R090 | SKILL.md#Chat-Anker-Übergabe (nur Cowork) › Schritt 1: `[ANKER-LIVE]` aus Memory lesen (Z. 296–301) | `[ANKER-LIVE]` aus dem Memory lesen und herausfiltern | MOVE | CO#Chat-Anker-Übergabe (nur Cowork) › Schritt 1: `[ANKER-LIVE]` aus Memory lesen |  |  | ✅ |
| R091 | SKILL.md#Chat-Anker-Übergabe (nur Cowork) › Schritt 2: Einträge klassifizieren (Z. 303–305) | Typ `offen` → TEMP-Anker ohne Task | MOVE | CO#Chat-Anker-Übergabe (nur Cowork) › Schritt 2: Einträge klassifizieren | „Phase 1 Ausarbeitung“ – Historie/Konzeptbezug, DROP-Kandidat |  | ✅ |
| R092 | SKILL.md#Chat-Anker-Übergabe (nur Cowork) › Schritt 2: Einträge klassifizieren (Z. 306) | Typ `erstellt` → Task existiert, nicht erledigt | MOVE | CO#Chat-Anker-Übergabe (nur Cowork) › Schritt 2: Einträge klassifizieren |  |  | ✅ |
| R093 | SKILL.md#Chat-Anker-Übergabe (nur Cowork) › Schritt 2: Einträge klassifizieren (Z. 307) | Typ `erledigt` sollte nicht auftauchen (wird bei `tracker done` entfernt) | MOVE | CO#Chat-Anker-Übergabe (nur Cowork) › Schritt 2: Einträge klassifizieren |  |  | ✅ |
| R094 | SKILL.md#Chat-Anker-Übergabe (nur Cowork) › Schritt 2: Einträge klassifizieren (Z. 309) | Alle Einträge in den Übergabeprompt übernehmen, im neuen Chat wiederherstellen | MOVE | CO#Chat-Anker-Übergabe (nur Cowork) › Schritt 2: Einträge klassifizieren | Doppelung mit R153 |  | ✅ |
| R095 | SKILL.md#Chat-Anker-Übergabe (nur Cowork) › Schritt 3: Sektion "Offene Anker" in Übergabeprompt (Z. 311–325) | Sektion „Offene Anker aus Teil N“ (Tabelle ID/Typ/Thema, Anweisung an den neuen Chat) | MOVE | CO#Chat-Anker-Übergabe (nur Cowork) › Schritt 3: Sektion "Offene Anker" in Übergabeprompt | Doppelung mit R118 |  | ✅ |
| R096 | SKILL.md#Chat-Anker-Übergabe (nur Cowork) › Schritt 4: Nach Prompt-Erstellung — Memory leeren (Z. 327–335) | Nach der Prompt-Erstellung alle `[ANKER-LIVE]`-Einträge entfernen, je Eintrag ein Remove; Daten reisen per Prompt | MOVE | CO#Chat-Anker-Übergabe (nur Cowork) › Schritt 4: Nach Prompt-Erstellung — Memory leeren | Doppelung mit R153, R171 |  | ✅ |
| R097 | SKILL.md#Chat-Anker-Übergabe (nur Cowork) › Keine Anker vorhanden? (Z. 337–339) | Keine Anker → Sektion weglassen, keine leere Tabelle | MOVE | CO#Chat-Anker-Übergabe (nur Cowork) › Keine Anker vorhanden? | Doppelung mit R172 |  | ✅ |
| R098 | SKILL.md#Link-Prüfung (PFLICHT vor der Ausgabe) (Z. 343–346) | Link-Prüfung PFLICHT vor der Ausgabe: jeder Verweis im Prompt muss stimmen | KEEP | S#Link-Prüfung (PFLICHT vor der Ausgabe) | Beispiel `heidi-panel-v2.js` ist Projekt-/Historienbeispiel – DROP-Kandidat |  | ✅ |
| R099 | SKILL.md#Link-Prüfung (PFLICHT vor der Ausgabe) (Z. 348) | Jede genannte Datei existiert | KEEP | S#Link-Prüfung (PFLICHT vor der Ausgabe) | „Cowork: DC `list_directory`“ = Umgebungswerkzeug im Kern – Auffälligkeit |  | ✅ |
| R100 | SKILL.md#Link-Prüfung (PFLICHT vor der Ausgabe) (Z. 349) | Genannte Abschnitte existieren | KEEP | S#Link-Prüfung (PFLICHT vor der Ausgabe) |  |  | ✅ |
| R101 | SKILL.md#Link-Prüfung (PFLICHT vor der Ausgabe) (Z. 350) | Jede Task-ID existiert mit dem genannten Status (tracker read-only) | KEEP | S#Link-Prüfung (PFLICHT vor der Ausgabe) |  |  | ✅ |
| R102 | SKILL.md#Link-Prüfung (PFLICHT vor der Ausgabe) (Z. 351) | Version im Prompt = Versionsquelle | KEEP | S#Link-Prüfung (PFLICHT vor der Ausgabe) |  |  | ✅ |
| R103 | SKILL.md#Link-Prüfung (PFLICHT vor der Ausgabe) (Z. 352) | Tote Verweise → Auswahlfrage; nie stumm übernehmen | KEEP | S#Link-Prüfung (PFLICHT vor der Ausgabe) | Doppelung mit R018, R176 |  | ✅ |
| R104 | SKILL.md#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) (Z. 356–360) | Claude Code: doc-pflege Modus 8 zuerst (Statusliste, Befunde, Stand, offene Punkte, Doku-Checkliste, Commit + Push nach Push-Policy); uncommittete Änderungen → Auswahlfrage | KEEP | S#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) |  |  | ✅ |
| R105 | SKILL.md#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) (Z. 361) | ClickUp-Abgleich (Batch-Abschluss über tracker); Memory: erledigte Merker mit Bestätigung entfernen | REWRITE | S#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) | „wie oben“ → Link auf `references/tracker-abgleich.md` |  | ✅ sinngemäß |
| R106 | SKILL.md#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) (Z. 362) | Link-Prüfung auf Stand-Abschnitt und Startprompt | KEEP | S#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) |  |  | ✅ |
| R107 | SKILL.md#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) (Z. 363–365) | Handover-Prompt nach PROMPT-STRUKTUR vollständig als Markdown-Codeblock; erste Zeile ist der Startprompt | REWRITE | S#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) | Link auf `references/prompt-struktur.md` ergänzt |  | ✅ sinngemäß |
| R108 | SKILL.md#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) (Z. 366–371) | Beispiel eines Startprompts (als Beispiel gekennzeichnet) | KEEP | S#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) |  |  | ✅ |
| R109 | SKILL.md#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) (Z. 373–375) | Muster aus dem Feld „Startprompt“ des Doku-Profils; danach die Abschnitte der PROMPT-STRUKTUR | KEEP | S#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) |  |  | ✅ |
| R110 | SKILL.md#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) (Z. 376) | Claude Code: Memory-Dateien nennen (Titel), nicht kopieren | KEEP | S#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) |  |  | ✅ |
| R111 | SKILL.md#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) (Z. 377–379) | Neues Fenster nur in tmux: prüfen, per Auswahlfrage anbieten, Fenster mit `claude --remote-control`, Prompt einfügen, nicht absenden | KEEP | S#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) | Verweis als Markdown-Link formatiert |  | ✅ |
| R112 | SKILL.md#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) (Z. 380) | Fertig; Kurzform nur auf ausdrücklichen Wunsch | KEEP | S#ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt) |  |  | ✅ |
| R113 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 384) | PROMPT-STRUKTUR gilt in beiden Umgebungen (Überschrift) | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) | Titel der Reference |  | ✅ |
| R114 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 386–389) | Titel `[Projektname] Teil [N+1]`, Weiterführung aus Teil [N] | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R115 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 391–397) | Aktueller Stand: App-Version, letzter Commit, Branch, Chat-URL Teil [N] | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R116 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 399–400) | Erledigt in Teil [N] | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R117 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 402–409) | Offene Punkte: ClickUp offen, gruppiert nach Liste bzw. Status; nur Listen/Status mit offenen Tasks | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R118 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 411–416) | Offene Anker nur bei Einträgen, nur Cowork | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R119 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 418–431) | Offene Punkte aus Memory nach Rubriken; leere Rubriken bzw. ganze Sektion weglassen | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R120 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 433–434) | Im Chat neu erkannt (noch nicht in ClickUp) | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R121 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 436–437) | Im Chat erledigt (noch nicht in ClickUp markiert) | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R122 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 439–443) | Sonstige offene Punkte: Pending Commits, Doc-, Frontmatter-/Quickload-Updates, neue Invarianten | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R123 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 445–446) | Nächste Schritte nach V1 + high/urgent zuerst | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) | Doppelung mit R150 |  | ✅ |
| R124 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 448–450) | Aktive Entscheidungen: Architektur, offene Fragen | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R125 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 452–456) | Kontext: Erkenntnisse, Warnungen, zu lesende Docs, veraltete Quickloads | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R126 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 458) | Regeln-Block aus den Profilen der CLAUDE.md erzeugt, nicht fest | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) | Doppelung mit R157 |  | ✅ |
| R127 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 459) | Regel Commit aus dem Commit-Profil | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R128 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 460) | Regel Tracker aus dem Tracker-Profil; tracker-Skill ist einzige Schreibschnittstelle zu ClickUp | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) | Doppelung mit R168 |  | ✅ |
| R129 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 461) | Regel Docs aus dem Doku-Profil | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R130 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 462) | Regel Code aus dem Code-Profil | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R131 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 463) | Ein Schritt pro Antwort; bei festen Optionen Auswahlfrage | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R132 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 464) | Wer committet: Cowork der User, Claude Code Claude | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) |  |  | ✅ |
| R133 | SKILL.md#PROMPT-STRUKTUR (beide Umgebungen) (Z. 465–466) | Rückfall BPM ohne Profile (User pusht, Commit-Format, Doku-Reihenfolge, ClickUp Space, BPM-NNN) | MOVE | PS#PROMPT-STRUKTUR (beide Umgebungen) | Projektwerte BPM – DROP-Kandidat |  | ✅ |
| R134 | SKILL.md#Chat-URL in Übergabe-Prompt (nur Cowork) (Z. 471–473) | Nur Cowork: URL des endenden Chats unter `**Chat-URL Teil [N]:**` in den Prompt (für Nachpflege) | MOVE | CO#Chat-URL in Übergabe-Prompt (nur Cowork) | Doppelung mit R152 |  | ✅ |
| R135 | SKILL.md#Chat-URL in Übergabe-Prompt (nur Cowork) (Z. 475–477) | URL, die der User gepostet hat, verwenden | MOVE | CO#Chat-URL in Übergabe-Prompt (nur Cowork) |  |  | ✅ |
| R136 | SKILL.md#Chat-URL in Übergabe-Prompt (nur Cowork) (Z. 478–480) | Sonst letzten Chat abfragen und prüfen, ob er passt | MOVE | CO#Chat-URL in Übergabe-Prompt (nur Cowork) |  |  | ✅ |
| R137 | SKILL.md#Chat-URL in Übergabe-Prompt (nur Cowork) (Z. 481) | Keine URL ermittelbar → Feld leer lassen + Hinweis | MOVE | CO#Chat-URL in Übergabe-Prompt (nur Cowork) |  |  | ✅ |
| R138 | SKILL.md#Chat-URL in Übergabe-Prompt (nur Cowork) (Z. 483) | Nicht raten, lieber leer als falsch | MOVE | CO#Chat-URL in Übergabe-Prompt (nur Cowork) | Doppelung mit R170 |  | ✅ |
| R139 | SKILL.md#REGELN (Z. 489) | Automatisch sammeln, nicht nachfragen, was rein soll | KEEP | S#REGELN | Doppelung mit R159 |  | ✅ |
| R140 | SKILL.md#REGELN (Z. 490) | Chat-Nummer korrekt N+1 | KEEP | S#REGELN |  |  | ✅ |
| R141 | SKILL.md#REGELN (Z. 491) | Nichts vergessen, inkl. pending Frontmatter, neue Invarianten | KEEP | S#REGELN | Doppelung mit R160, R164 |  | ✅ |
| R142 | SKILL.md#REGELN (Z. 492) | Kompakt aber vollständig | KEEP | S#REGELN |  |  | ✅ |
| R143 | SKILL.md#REGELN (Z. 493) | Kopierfähig als Markdown-Codeblock | KEEP | S#REGELN |  |  | ✅ |
| R144 | SKILL.md#REGELN (Z. 494) | Version prüfen | KEEP | S#REGELN |  |  | ✅ |
| R145 | SKILL.md#REGELN (Z. 495) | Keine Datei, direkt im Chat; Claude Code vorher Stand ins Repo (Modus 8) | KEEP | S#REGELN | Doppelung mit R161 |  | ✅ |
| R146 | SKILL.md#REGELN (Z. 496) | Pending Quickload-Änderungen explizit nennen | KEEP | S#REGELN |  |  | ✅ |
| R147 | SKILL.md#REGELN (Z. 497) | ClickUp-Abgleich VOR dem Übergabeprompt: offene Tasks laden + Chat scannen | KEEP | S#REGELN |  |  | ✅ |
| R148 | SKILL.md#REGELN (Z. 498) | Batch-Abschluss per Auswahlfrage, nicht als Prosa-Liste | KEEP | S#REGELN | Doppelung mit R166 |  | ✅ |
| R149 | SKILL.md#REGELN (Z. 499) | Keine automatischen ClickUp-Mutationen ohne Auswahlfrage-Bestätigung | KEEP | S#REGELN | Doppelung mit R167 |  | ✅ |
| R150 | SKILL.md#REGELN (Z. 500) | Nächste Schritte aus V1 + Priority ableiten | KEEP | S#REGELN |  |  | ✅ |
| R151 | SKILL.md#REGELN (Z. 501) | Sonstige offene Punkte zusätzlich zu ClickUp auflisten | KEEP | S#REGELN | Doppelung mit R169 |  | ✅ |
| R152 | SKILL.md#REGELN (Z. 502) | Aktuelle Chat-URL in den Prompt (Nachpflege) | KEEP | S#REGELN |  |  | ✅ |
| R153 | SKILL.md#REGELN (Z. 503) | `[ANKER-LIVE]` in den Prompt kopieren, danach aus dem Memory leeren | KEEP | S#REGELN |  |  | ✅ |
| R154 | SKILL.md#REGELN (Z. 504) | Memory-Scan nach 4 Rubriken als Sektion `## Offene Punkte aus Memory` | KEEP | S#REGELN |  |  | ✅ |
| R155 | SKILL.md#REGELN (Z. 505) | Memory-Cleanup nur mit Bestätigung per Auswahlfrage, nie stillschweigend | KEEP | S#REGELN |  |  | ✅ |
| R156 | SKILL.md#REGELN (Z. 506) | Link-Prüfung vor der Ausgabe: Dateien, Abschnitte, Task-IDs, Version | KEEP | S#REGELN | Doppelung mit R098, R176 |  | ✅ |
| R157 | SKILL.md#REGELN (Z. 507) | Regeln-Block aus den Profilen, nicht aus fester Liste | KEEP | S#REGELN |  |  | ✅ |
| R158 | SKILL.md#REGELN (Z. 508) | Claude Code: erst Modus 8, dann vollständiger Prompt; Kurzform nur auf Wunsch; Details verweisen statt kopieren | KEEP | S#REGELN |  |  | ✅ |
| R159 | SKILL.md#VERBOTEN (Z. 514) | VERBOTEN: nachfragen, was rein soll (Prosa) | KEEP | S#VERBOTEN |  |  | ✅ |
| R160 | SKILL.md#VERBOTEN (Z. 515) | VERBOTEN: offene Punkte vergessen | KEEP | S#VERBOTEN |  |  | ✅ |
| R161 | SKILL.md#VERBOTEN (Z. 516) | VERBOTEN: als Datei liefern | KEEP | S#VERBOTEN |  |  | ✅ |
| R162 | SKILL.md#VERBOTEN (Z. 517) | VERBOTEN: ohne Version/Chat-Nummer | KEEP | S#VERBOTEN |  |  | ✅ |
| R163 | SKILL.md#VERBOTEN (Z. 518) | VERBOTEN: Nummern verwechseln | KEEP | S#VERBOTEN |  |  | ✅ |
| R164 | SKILL.md#VERBOTEN (Z. 519) | VERBOTEN: pending Frontmatter/Invarianten vergessen | KEEP | S#VERBOTEN |  |  | ✅ |
| R165 | SKILL.md#VERBOTEN (Z. 520) | VERBOTEN: Branch automatisch annehmen ohne Branch-Policy, Shell oder Auswahlfrage | KEEP | S#VERBOTEN |  |  | ✅ |
| R166 | SKILL.md#VERBOTEN (Z. 521) | VERBOTEN: Prosa-Fragen bei festen Optionen | KEEP | S#VERBOTEN |  |  | ✅ |
| R167 | SKILL.md#VERBOTEN (Z. 522) | VERBOTEN: Tasks ohne Auswahlfrage-Bestätigung erstellen/schließen | KEEP | S#VERBOTEN |  |  | ✅ |
| R168 | SKILL.md#VERBOTEN (Z. 523) | VERBOTEN: ClickUp-Schreiboperationen direkt statt über tracker | KEEP | S#VERBOTEN |  |  | ✅ |
| R169 | SKILL.md#VERBOTEN (Z. 524) | VERBOTEN: Pending Commits/Doc-/Frontmatter-Updates vergessen, weil ClickUp da ist | KEEP | S#VERBOTEN |  |  | ✅ |
| R170 | SKILL.md#VERBOTEN (Z. 525) | VERBOTEN: Chat-URLs raten oder erfinden | KEEP | S#VERBOTEN |  |  | ✅ |
| R171 | SKILL.md#VERBOTEN (Z. 526) | VERBOTEN: `[ANKER-LIVE]` nach der Übergabe im alten Memory belassen | KEEP | S#VERBOTEN |  |  | ✅ |
| R172 | SKILL.md#VERBOTEN (Z. 527) | VERBOTEN: leere Anker-Tabelle im Prompt | KEEP | S#VERBOTEN |  |  | ✅ |
| R173 | SKILL.md#VERBOTEN (Z. 528) | VERBOTEN: `[CLICKUP]`/`[SKILL-ISSUES]` in den Prompt übernehmen | KEEP | S#VERBOTEN |  |  | ✅ |
| R174 | SKILL.md#VERBOTEN (Z. 529) | VERBOTEN: leere Rubrik-H3-Blöcke | KEEP | S#VERBOTEN |  |  | ✅ |
| R175 | SKILL.md#VERBOTEN (Z. 530) | VERBOTEN: Memory-Einträge ohne ausdrückliche Bestätigung entfernen | KEEP | S#VERBOTEN |  |  | ✅ |
| R176 | SKILL.md#VERBOTEN (Z. 531) | VERBOTEN: Prompt mit toten Verweisen ausgeben | KEEP | S#VERBOTEN |  |  | ✅ |
| R177 | SKILL.md#VERBOTEN (Z. 532) | VERBOTEN: BPM-Regeln oder BPM-NNN in den Prompt eines anderen Projekts | KEEP | S#VERBOTEN |  |  | ✅ |
| R178 | SKILL.md#VERBOTEN (Z. 533) | VERBOTEN: in Claude Code den Stand nur in den Prompt statt ins Repo; Modus 8 zuerst | KEEP | S#VERBOTEN |  |  | ✅ |
| R179 | SKILL.md#VERBOTEN (Z. 534) | VERBOTEN: in Claude Code ungefragt nur den kurzen Startprompt | KEEP | S#VERBOTEN |  |  | ✅ |
| R180 | SKILL.md#VERBOTEN (Z. 535) | VERBOTEN: Sitzung mit uncommitteten Änderungen ohne Auswahlfrage übergeben | KEEP | S#VERBOTEN |  |  | ✅ |
| R181 | SKILL.md#VERBOTEN (Z. 536) | VERBOTEN: Prompt im neuen Fenster selbst absenden oder altes Fenster schließen | KEEP | S#VERBOTEN | Doppelung mit R190 |  | ✅ |
| R182 | references/neues-fenster.md#Neues Fenster für die nächste Sitzung (Claude Code mit tmux) (Z. 3–5) | Neues Fenster nur in Claude Code mit tmux; Prompt eingefügt, abgeschickt vom Nutzer | KEEP | NF#Neues Fenster für die nächste Sitzung (Claude Code mit tmux) |  |  | ✅ |
| R183 | references/neues-fenster.md#Ablauf (Z. 9–11) | Umgebung aus der Shell prüfen; kein tmux → nur Prompt + ein Satz, hier aufhören | KEEP | NF#Ablauf |  |  | ✅ |
| R184 | references/neues-fenster.md#Ablauf (Z. 12–14) | Projekt-Repo aus der Shell; außerhalb des Repos aus dem Chat; unklar → Auswahlfrage | KEEP | NF#Ablauf |  |  | ✅ |
| R185 | references/neues-fenster.md#Ablauf (Z. 15–17) | tmux-Sitzung des Projekts wählen; mehrere Kandidaten → Auswahlfrage | KEEP | NF#Ablauf |  |  | ✅ |
| R186 | references/neues-fenster.md#Ablauf (Z. 18–19) | Rückfrage per Auswahlfrage: Neues Fenster einrichten / Nur Prompt, mit Fenstername und Sitzung | KEEP | NF#Ablauf |  |  | ✅ |
| R187 | references/neues-fenster.md#Ablauf (Z. 20–23) | Fenster `<Projekt> Teil <N+1>` im Repo mit Remote Control anlegen, höchstens etwa 30 s warten | KEEP | NF#Ablauf |  |  | ✅ |
| R188 | references/neues-fenster.md#Ablauf (Z. 24–27) | Prompt per Bracketed Paste einfügen, Ankunft prüfen, nicht absenden | KEEP | NF#Ablauf |  |  | ✅ |
| R189 | references/neues-fenster.md#Ablauf (Z. 28–31) | Melden: Fenster, Sitzung, Remote-Control-Link, Navigation, altes Fenster beenden; Prompt zusätzlich im Chat | KEEP | NF#Ablauf |  |  | ✅ |
| R190 | references/neues-fenster.md#Regeln (Z. 35) | Altes Fenster nie selbst schließen, Prompt nie selbst absenden | KEEP | NF#Regeln |  |  | ✅ |
| R191 | references/neues-fenster.md#Regeln (Z. 36) | Keine Pfade raten: Repo und Sitzung aus Shell oder Auswahlfrage | KEEP | NF#Regeln |  |  | ✅ |
| R192 | references/neues-fenster.md#Regeln (Z. 37) | Remote Control Standard; bei Ablehnung `claude -n` | KEEP | NF#Regeln |  |  | ✅ |
| N001 | – | Tabelle „Fall → Reference“: Prompt-Aufbau, ClickUp-Abgleich, Cowork-Teile, neues Fenster je mit Link | NEW | SKILL.md#Fall → Reference | Split-Muster aus `docs/skill-quality.md`/skill-pflege (Tabelle Fall → Reference); keine neue Vorgabe |  | ✅ |
| N002 | – | Ablauf im Cowork-Chat: ClickUp-Abgleich, Memory-Scan, Chat-Anker-Übergabe, Chat-URL, Link-Prüfung, Prompt als Codeblock im Chat – je mit Verweis | NEW | SKILL.md#Ablauf im Cowork-Chat | Überleitung; Inhalte aus R003, R147, R154, R155, R153, R096, R134, R098, R143, R145 – keine neue Vorgabe |  | ✅ |
| N003 | – | Einleitung der Reference: gilt in beiden Umgebungen, Einstieg über SKILL.md | NEW | references/prompt-struktur.md#PROMPT-STRUKTUR (beide Umgebungen) | Überleitung zu R113 |  | ✅ |
| N004 | – | Einleitung der Reference: gilt in beiden Umgebungen vor dem Handover-Prompt, Einstieg über SKILL.md | NEW | references/tracker-abgleich.md#ClickUp-Integration (vor Übergabeprompt) | Überleitung zu R041/R147 |  | ✅ |
| N005 | – | Einleitung und Inhaltsverzeichnis der Reference; Hinweis, dass Zweck und Claude-Code-Teil des Memory-Scans in SKILL.md stehen | NEW | references/cowork.md (Kopf, Inhalt, Memory-Scan) | Überleitung; Inhaltsverzeichnis nach `docs/skill-quality.md` (Reference über 100 Zeilen) |  | ✅ |

## DROP-Gruppen

Keine. Die Zielstruktur verschiebt nur; laut Freigabe wird nichts gestrichen.

Beim Umbau aufgefallene Kandidaten für einen späteren Refactor (bleiben jetzt stehen, sind in der Spalte Bezug markiert):

| Gruppe | IDs | Grund |
|---|---|---|
| Historie im Regeltext | R005, R091, R098 (Beispiel) | Datum und Zitat „Herbert, 16.09.2026“; „Phase 1 Ausarbeitung“; Umbenennungsbeispiel `heidi-panel-v2.js` |
| Werkzeug-Syntax | R051, R052 | Codeblöcke `ask_user_input_v0` – dieselbe Art wie die am 28.09. freigegebene DROP-Gruppe A; die Vorgabe (zwei Auswahlfragen mit Mehrfachauswahl und „Keine“) steht schon in R050, R021, R023 |
| Projektwerte im Skill | R009, R133 | Rückfall „BPM-Weg“ ohne Profil; BPM-Rückfallregeln im Regeln-Block |
| Doppelungen | R008/R112/R158/R179; R018/R103/R156/R176; R024/R056; R084/R155/R175; R097/R172; R139/R159; R031/R165 u. a. (Spalte Bezug) | Regeln stehen in Abschnitt, REGELN und VERBOTEN mehrfach; Redundanz kann Absicht sein |

## Verweise von außen

Suche nach `chat-wechsel`, `PROMPT-STRUKTUR`, `ClickUp-Integration`, `Chat-Anker`, `Memory-Scan`, `Chat-URL`,
`Link-Prüfung` und `Batch-Abschluss` in `skills/`, `INDEX.md`, `README.md`, `MEMORY-RUBRIKEN.md`, `docs/` und `quality/`
(ohne Review-Archiv, frühere Inventare und CHANGELOG).

| Stelle | Verweis | Behandlung |
|---|---|---|
| `docs/fragilitaeten-und-fruehwarn.md` (Kopf, Z. 7–10) | „`chat-wechsel` Memory-Scan Schritt 4“ | in diesem Refactor korrigiert → `references/cowork.md`, Abschnitt „Schritt 4: Eskalations-Hinweis“ |
| `docs/fragilitaeten-und-fruehwarn.md` (Querverweise, Z. 250–251) | „chat-wechsel/SKILL.md Memory-Scan Schritt 4“ | in diesem Refactor korrigiert → `chat-wechsel/references/cowork.md`, Abschnitt „Schritt 4: Eskalations-Hinweis“ |
| `INDEX.md` (Z. 21, 41, 57, 88, 89) | Zuständigkeit, Konfliktpaar, Memory-Rubriken, Fragilitäten | nennt nur den Skill, keine Überschrift – passt |
| `MEMORY-RUBRIKEN.md` (Z. 57, 96, 120) | „`chat-wechsel` scannt beim Handover …“ | nennt nur den Skill – passt |
| `skills/tracker/SKILL.md` (Integration), `skills/tracker/references/anti-patterns.md`, `batch-protocol.md`, `chat-url-handling.md`, `anker-system.md` | Batch-Abschluss, Chat-URL und Anker-Übergabe bei chat-wechsel | nennen nur den Skill – passt; `anker-system.md` spricht von „lokalen Kopien“ in chat-wechsel, die liegen jetzt in `references/cowork.md` (kein Pfad genannt) |
| `skills/chatgpt-review/SKILL.md`, `skills/ticket/SKILL.md`, `skills/doc-pflege/SKILL.md` | Delegation bzw. Zulieferung an chat-wechsel | nennen nur den Skill – passt |
| `docs/chat-anker-konzept.md`, `docs/skill-refactor-phases.md`, `evals/` | Konzept und Historie | Archiv, kein Verweis auf eine Überschrift von SKILL.md – bleibt |
| `docs/skill-profile-v1.md` (Pflichtfelder je Skill) | chat-wechsel braucht Doku.Sitzungsabschluss, Doku.Entscheidungs-Ort, Commit.Push-Policy, Tracker.Config | kein Bezug auf verschobene Abschnitte |

## Prüfung

- **Alt→Neu:** 192 IDs, alle mit Zustand (KEEP 111, MOVE 77, REWRITE 4, MERGE 0, DROP 0). Für jede ID wurde der alte
  Textblock (nicht leere Zeilen, bekannte Änderungen eingesetzt, Überschriftenebene ignoriert) per Skript im Scratchpad als
  zusammenhängender Block in den neuen Dateien gesucht und die Überschrift an der Fundstelle mit dem Neu-Ort verglichen:
  192 von 192 gefunden. Alle 211 Kandidaten des alten Stands liegen im Bereich einer ID; die 7 ohne eigene Zeile sind
  Tabellenköpfe und Überschriften, die für die Regeln darunter stehen. Jede nicht leere Zeile des alten Stands steht
  wörtlich im neuen Stand, bis auf 9 Zeilen mit geänderten Verweisen (Z. 18, 19, 204, 205, 240, 254, 361, 363, 379).
- **Neu→Alt:** 232 Kandidaten im neuen Stand: 205 gehören zu einer ID, 20 zu N001–N005, 7 sind Tabellenköpfe und
  Überschriften (zugehörig zu R011–R014, R018–R026, R042, R045, R053, R076–R079, R159 ff.). Keine ungewollt neue Regel;
  N001–N005 sind Überleitungen und Verweise ohne neue Vorgabe.
- **Description:** zeichengleich (Frontmatter Z. 1–10 unverändert).
- **Zeilen:** SKILL.md 536 → 236; References 37 → 382 (prompt-struktur 87, tracker-abgleich 93, cowork 165,
  neues-fenster 37).
- **Prüfskript:** auf dem HA nicht lauffähig; Nachbau der Prüfungen im Scratchpad: keine toten Verweise (auch der
  korrigierte Link auf `docs/fragilitaeten-und-fruehwarn.md`), Inhaltsverzeichnis in `references/cowork.md` vorhanden.
  Warnungen wie vorher: Historie (R005), Nummern-Querverweise „doc-pflege Modus 8“ (Description, Zweck, Ablauf, REGELN),
  Werkzeugnamen `ask_user_input_v0` jetzt in `references/tracker-abgleich.md` statt in SKILL.md; `memory_user_edits` und
  `recent_chats` stehen jetzt in `references/cowork.md` (dort erlaubt). Das echte Prüfskript läuft nach dem Push per
  GitHub Actions.
- **Routing-Eval:** steht aus (nach dem Commit, `--tag chat-wechsel`); Description unverändert, auslöserelevante
  Abschnitte (TRIGGER, Vorrang) wörtlich.
