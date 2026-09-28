# Regel-Inventar – chat-wechsel – 2026-09-28

Refactor von chat-wechsel in Umbau-Phase 5, Punkte „Regel ‚Fragen nur bei offener Entscheidung‘ in alle Skills“ und
„Branch und Push aus dem Profil lesen“ (`docs/skillsystem-umbau.md`). Nach dem Refactor-Ablauf von skill-pflege
(`skills/skill-pflege/references/rule-inventory.md`); Muster: git-commit-helper (Abschnitt „Grundsätze“,
`docs/skill-refactors/2026-09-28-git-commit-helper.md`). Kandidaten nach Urteil gesammelt, ohne Vorsammeln durch das
Prüfskript (Entwurf im Scratchpad).

- Skill: chat-wechsel
- Stand vorher: 55eab72 (SKILL.md, 570 Zeilen; keine references)
- Quellen: SKILL.md
- Umfang: Punkte 3 und 4; übrige Abschnitte wörtlich unverändert (auch Projektwerte BPM/Heidi, Cowork-Teile,
  Nummern-Verweise wie „Modus 8“ – das kommt in Phase 6)

## Zielstruktur

Nur die geänderten Abschnitte:

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | Zweck (nur „Commit + Push“ an die Push-Policy gebunden) · **Grundsätze** (neu, an der Stelle von „🚨 VERBINDLICHE REGEL“ und „Branch-Ermittlung“: Fragen, Branch, Push) · ABLAUF IN CLAUDE CODE (Schritt 1: Push nach Push-Policy) · VERBOTEN (Branch- und Prosa-Zeilen) |

Description unverändert (Frontmatter Z. 1–10 zeichengleich). Abkürzung im Neu-Ort: `S` = `SKILL.md`.

Entscheidung Herbert (laut Auftrag Phase 5): Ohne Push-Policy bleibt das bisherige Verhalten des Skills – in Claude Code
Commit + Push im Sitzungsabschluss.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#Zweck (Z. 20–21) | Claude Code: erst doc-pflege Sitzungsabschluss (Statusliste, Befunde, Stand, offene Punkte, Commit + Push), dann der vollständige Handover-Prompt | REWRITE | S#Zweck | nur „Commit + Push“ → „Commit + Push nach der Push-Policy“ (N002); Rest wörtlich | | ✅ sinngemäß |
| R002 | SKILL.md#🚨 VERBINDLICHE REGEL (Z. 56–60) | Jede Entscheidungsfrage mit festen Optionen als Auswahlfrage (Frage-Werkzeug der Umgebung mit anklickbaren Optionen), keine Prosa-Fragen | REWRITE | S#Grundsätze (Fragen) | „dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung“; die Werkzeugnamen in der Klammer entfallen (Erklärung, keine Vorgabe; Begriff „Auswahlfrage“) | | ✅ sinngemäß |
| R003 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 66) | Branch-Ermittlung, nur wenn die Shell ihn nicht liefert → Auswahl aus allen Branch-Namen (`git branch -a`) | MERGE | S#Grundsätze (Branch) | R025; die Optionsquelle `git branch -a` passt nicht zu „ohne Shell“, es gilt die GitHub-API-Liste der Branch-Ermittlung | | ✅ sinngemäß |
| R004 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 67) | Link-Prüfung findet tote Verweise → Korrigieren / Mit Warnung übernehmen / Weglassen | MOVE | S#Grundsätze (Fragen) | typische Stelle, Tabellenzeile wörtlich | | ✅ |
| R005 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 68) | Claude Code: uncommittete Änderungen beim Abschluss → Jetzt committen / Als offen vermerken / Abbrechen | MOVE | S#Grundsätze (Fragen) | typische Stelle | | ✅ |
| R006 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 69) | Batch-Abschluss erledigte Tasks → Alle als Done / Einzeln wählen / Keine | MOVE | S#Grundsätze (Fragen) | typische Stelle | | ✅ |
| R007 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 70) | Batch-Abschluss einzeln → Mehrfachauswahl mit allen Task-Namen | MOVE | S#Grundsätze (Fragen) | typische Stelle | | ✅ |
| R008 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 71) | Batch-Anlage neue Tasks → Alle anlegen / Einzeln wählen / Keine | MOVE | S#Grundsätze (Fragen) | typische Stelle | | ✅ |
| R009 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 72) | Batch-Anlage einzeln → Mehrfachauswahl mit allen erkannten Problemen | MOVE | S#Grundsätze (Fragen) | typische Stelle | | ✅ |
| R010 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 73) | ClickUp nicht erreichbar → Trotzdem Prompt erstellen / Retry / Abbrechen | MOVE | S#Grundsätze (Fragen) | typische Stelle | | ✅ |
| R011 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 74) | Version-Angabe unklar → aktuelle Versionen als Optionen | MOVE | S#Grundsätze (Fragen) | typische Stelle | | ✅ |
| R012 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 75) | Kein Commit-Stand erkennbar → Version vom User eingeben / Ohne Version / Abbrechen | MOVE | S#Grundsätze (Fragen) | typische Stelle | | ✅ |
| R013 | SKILL.md#Prosa-Fragen NUR wenn (Z. 79–80) | Prosa bei offener Frage ohne feste Optionen (Beispiel „Welche Version ist aktuell?“ ohne Kandidaten) | REWRITE | S#Grundsätze (Fragen) | ein Satz „Prosa nur bei …“ mit allen drei Fällen | | ✅ sinngemäß |
| R014 | SKILL.md#Prosa-Fragen NUR wenn (Z. 81) | Prosa, wenn der User gerade eine klare Präferenz signalisiert hat | MERGE | S#Grundsätze (Fragen) | R013 | | ✅ sinngemäß |
| R015 | SKILL.md#Prosa-Fragen NUR wenn (Z. 82) | Prosa bei Erklärung/Kontext ohne echte Entscheidung | MERGE | S#Grundsätze (Fragen) | R013 | | ✅ sinngemäß |
| R016 | SKILL.md#Wie die Auswahlfrage aussieht (Z. 84) | Überschrift: Cowork-Syntax, Claude Code `AskUserQuestion`, multiSelect für Listen | DROP | | Werkzeug-Syntax; die Mehrfachauswahl für Listen steht weiter in R007 und R009 | Gruppe A, freigegeben 28.09.2026 | ✅ |
| R017 | SKILL.md#Wie die Auswahlfrage aussieht (Z. 86–95) | Codeblock `ask_user_input_v0` für eine Einfachauswahl (Branch, BPM-Branchnamen) | DROP | | Werkzeug-Syntax-Beispiel ohne eigene Vorgabe | Gruppe A, freigegeben 28.09.2026 | ✅ |
| R018 | SKILL.md#Wie die Auswahlfrage aussieht (Z. 97–108) | Codeblock `ask_user_input_v0` mit `multi_select` (BPM-Tasks) | DROP | | Werkzeug-Syntax-Beispiel ohne eigene Vorgabe | Gruppe A, freigegeben 28.09.2026 | ✅ |
| R019 | SKILL.md#🚨 VERBINDLICHE REGEL › VERBOTEN (Z. 112) | „Alle als Done markieren? (ja / nein / einzeln wählen)“ als Prosa | MERGE | S#VERBOTEN | R031 | | ✅ sinngemäß |
| R020 | SKILL.md#🚨 VERBINDLICHE REGEL › VERBOTEN (Z. 113) | „Diese Tasks anlegen? (ja / nein / einzeln wählen)“ als Prosa | MERGE | S#VERBOTEN | R031 | | ✅ sinngemäß |
| R021 | SKILL.md#🚨 VERBINDLICHE REGEL › VERBOTEN (Z. 114) | Branch-Liste im Chat aufzählen und auf getippte Antwort warten | MERGE | S#VERBOTEN | R031 (Branch-Auswahl) | | ✅ sinngemäß |
| R022 | SKILL.md#🚨 VERBINDLICHE REGEL › VERBOTEN (Z. 115) | Optionen-Aufzählung im Chat ohne Auswahlfrage | MERGE | S#VERBOTEN | R031 | | ✅ sinngemäß |
| R023 | SKILL.md#Branch-Ermittlung (Z. 121) | In der Sitzung schon bekannten Branch verwenden | REWRITE | S#Grundsätze (Branch) | jetzt erster Schritt des Rückfalls ohne Skill-Profil | | ✅ sinngemäß |
| R024 | SKILL.md#Branch-Ermittlung (Z. 122) | Mit Shell `git branch --show-current` – Tatsache, keine Frage | REWRITE | S#Grundsätze (Branch) | mit Skill-Profil bei `current` (N001), ohne Profil im Rückfall wie bisher; die Werkzeug-Klammer (Bash/PowerShell, DC) entfällt, „Shell“ genügt | | ✅ sinngemäß |
| R025 | SKILL.md#Branch-Ermittlung (Z. 123) | Ohne Shell: Branches über die GitHub API auflisten, per Auswahlfrage wählen (Optionen = Branch-Namen) | MOVE | S#Grundsätze (Branch) | Rückfall ohne Skill-Profil, fast wörtlich | | ✅ |
| R026 | SKILL.md#Branch-Ermittlung (Z. 124) | Gewählten Branch für die ganze Sitzung merken | MOVE | S#Grundsätze (Branch) | | | ✅ |
| R027 | SKILL.md#Branch-Ermittlung (Z. 125) | NIE automatisch einen Branch annehmen (weder `main` noch einen anderen) | MOVE | S#Grundsätze (Branch) | wörtlich | | ✅ |
| R028 | SKILL.md#Branch-Ermittlung (Z. 126) | Ermittelten Branch im Übergabe-Prompt unter `**Branch:**` eintragen | MOVE | S#Grundsätze (Branch) | | | ✅ |
| R029 | SKILL.md#ABLAUF IN CLAUDE CODE (Z. 394–396) | Schritt 1: Sitzungsabschluss mit Doku-Checkliste, Commit + Push; uncommittete Änderungen → Auswahlfrage | REWRITE | S#ABLAUF IN CLAUDE CODE | „Commit + Push nach der Push-Policy (Grundsätze)“ (N002); Rest wörtlich | | ✅ sinngemäß |
| R030 | SKILL.md#VERBOTEN (Z. 553) | Branch automatisch annehmen ohne User-Auswahl | REWRITE | S#VERBOTEN | „– ohne Branch-Policy, Shell oder Auswahlfrage“; Shell und `current` liefern den Branch ohne Auswahl | | ✅ sinngemäß |
| R031 | SKILL.md#VERBOTEN (Z. 554) | Branch-Auswahl als Prosa – IMMER Auswahlfrage (wenn die Shell ihn nicht liefert) | REWRITE | S#VERBOTEN | wird die verbleibende Zeile „Prosa-Fragen bei festen Entscheidungsoptionen — IMMER Auswahlfrage (Branch-Auswahl, Batch-Abschluss, ‚ja/nein/einzeln wählen‘)“ | | ✅ sinngemäß |
| R032 | SKILL.md#VERBOTEN (Z. 555) | Batch-Abschluss als Prosa – IMMER Auswahlfrage | MERGE | S#VERBOTEN | R031 | | ✅ sinngemäß |
| R033 | SKILL.md#VERBOTEN (Z. 559) | „ja/nein/einzeln wählen“-Fragen als Text statt Auswahlfrage | MERGE | S#VERBOTEN | R031 | | ✅ sinngemäß |
| N001 | – | Branch nach der Branch-Policy des Skill-Profils: `current` → aktueller Branch aus der Shell; `fixed:<branch>` → der aktuelle muss dieser sein, sonst Auswahlfrage (wechseln / abbrechen); ohne Skill-Profil der bisherige Ablauf (R023–R025) | NEW | S#Grundsätze (Branch) | Phase 5 „Branch und Push aus dem Profil“; `docs/skill-profile-v1.md` (Branch-Policy) | | ✅ |
| N002 | – | Push im Sitzungsabschluss (Claude Code) nach der Push-Policy: `user-only` kein Push, `allowed` nur auf ausdrücklichen Wunsch, `required-after-commit` direkt nach dem Commit, `required-at-session-end` alle Commits der Sitzung vor dem Handover-Prompt; ohne Push-Policy Commit + Push wie im alten Stand | NEW | S#Grundsätze (Push); S#Zweck; S#ABLAUF IN CLAUDE CODE | Entscheidung Herbert zum Rückfall; Pflichtfeld Commit.Push-Policy laut `docs/skill-profile-v1.md` | | ✅ |
| N003 | – | Nur fragen, wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen ist | NEW | S#Grundsätze (Fragen) | Phase 5 „Fragen nur bei offener Entscheidung“; `docs/skill-quality.md` (Zusammenspiel) | | ✅ |
| N004 | – | Skill-Profil vorhanden, aber keine Shell: bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage | NEW | SKILL.md#Grundsätze | Entscheidung Herbert 28.09.2026 (Sammelfreigabe Phase 5) | | ✅ |
| N005 | – | Ungepushte Commits (`user-only`, `allowed`) nennt der Übergabe-Prompt unter „Sonstige offene Punkte“ (Hash, Titel, „Push durch den Nutzer“) | NEW | SKILL.md#Grundsätze | Entscheidung Herbert 28.09.2026 (Sammelfreigabe Phase 5) | | ✅ |

## DROP-Gruppen

Von Herbert am 28.09.2026 freigegeben (Auswahlfrage vor dem Schreiben):

| Gruppe | IDs | Regelkern | Grund |
|---|---|---|---|
| A – Werkzeug-Syntax | R016, R017, R018 | Überschrift und zwei Codeblöcke mit `ask_user_input_v0` bzw. `AskUserQuestion` (Einfach- und Mehrfachauswahl, BPM-Beispielwerte) | Syntax eines Werkzeugs statt Handlung (`docs/skill-quality.md`, Neutralität); die Vorgabe „Mehrfachauswahl für Listen“ bleibt in den typischen Stellen R007 und R009 erhalten |

Werden einzelne IDs behalten, kehren sie unverändert als Beispiel unter die typischen Stellen zurück (Zustand MOVE).

## Verweise von außen

| Stelle | Verweis | Behandlung |
|---|---|---|
| `skills/doc-pflege/SKILL.md` (Tabelle Sitzungsabschluss, Ablauf Sitzungsabschluss) | „Commit + Push“ ohne Push-Policy | Phase 5 im doc-pflege-Entwurf (Push nach Push-Policy) |
| `docs/skill-profile-v1.md`, Pflichtfelder je Skill | chat-wechsel braucht Doku.Sitzungsabschluss, Doku.Entscheidungs-Ort, Commit.Push-Policy, Tracker.Config | Push-Policy und Branch-Policy liest der Skill jetzt; die Doku- und Tracker-Felder in Phase 6 |
| `INDEX.md` (Z. 21, 80) | Zuständigkeit; Konfliktpaar chat-wechsel ↔ chatgpt-review („generisch → ask_user_input_v0“) | kein Bezug auf die geänderten Abschnitte; INDEX-Umbau Phase 5 |
| Verweise auf „VERBINDLICHE REGEL“ oder „Branch-Ermittlung“ von chat-wechsel | keine gefunden (Suche im Repo ohne Review-Archiv) | – |

## Prüfung

Von Herbert am 28.09.2026 freigegeben (Auswahlfrage vor dem Schreiben):
  REWRITE und MERGE ist der Neu-Ort im Entwurf gefunden.
- **Neu→Alt:** Alle normativen Aussagen der geänderten Stellen (Zweck Z. 21, Grundsätze Z. 56–87, Ablauf Z. 357,
  VERBOTEN Z. 514–515) gehören zu einer ID oder zu N001–N003. Keine ungewollt neue Regel.
- **Diff** (`git diff --no-index` gegen `skills/chat-wechsel/SKILL.md`): Unterschiede nur in Zweck Z. 21, im Block
  „VERBINDLICHE REGEL“ + „Branch-Ermittlung“ (Z. 56–126 → Grundsätze Z. 56–87), in Ablauf Schritt 1 und in VERBOTEN.
  Description zeichengleich.
- **Zeilen:** 570 → 529.
- **Prüfskript:** nicht gelaufen (Entwurf im Scratchpad); läuft vor dem Commit.
- **Routing-Eval:** am 28.09.2026 auf a0fb0a5, `--tag chat-wechsel --tag chatgpt-review --tag git-commit-helper --tag tracker` (22 Fälle, 66 Läufe, `-j 3`, 17 min, 23,06 USD): 64/66 (Grundmessung derselben Fälle 66/66). Alle Fälle von chat-wechsel, chatgpt-review, git-commit-helper und tracker 3/3, alle kritischen Fälle 3/3, kein Negativfall gekippt. Die zwei Abweichungen sind mitgetaggte Fälle anderer Skills (`code-with-task-ref`, `doc-changelog` je 2/3) mit einem Lauf ohne jeden Skill-Aufruf (Sandbox-Muster der Grundmessung). Freigabe nach `docs/skill-quality.md`, Abschnitt Verhalten: erfüllt. Description unverändert, daher keine echte Sitzung.
