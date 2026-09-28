# Regel-Inventar – chatgpt-review – 2026-09-28

Refactor von chatgpt-review in Umbau-Phase 5, Punkte „Regel ‚Fragen nur bei offener Entscheidung‘ in alle Skills“ und
„Branch und Push aus dem Profil lesen“ (`docs/skillsystem-umbau.md`). Nach dem Refactor-Ablauf von skill-pflege
(`skills/skill-pflege/references/rule-inventory.md`); Muster: Inventar git-commit-helper
(`docs/skill-refactors/2026-09-28-git-commit-helper.md`). Kandidaten nach Urteil gesammelt, ohne Prüfskript.

- Skill: chatgpt-review
- Stand vorher: 6dabd46 (SKILL.md, 547 Zeilen; keine references)
- Quellen: SKILL.md; `docs/skill-profile-v1.md` (Branch-Policy, Push-Policy, Pflichtfelder: Review.Config,
  Commit.Push-Policy)
- Umfang: Punkte 3 und 4; übrige Abschnitte wörtlich unverändert (auch Projektwerte BPM/Heidi, Cowork-Teile,
  Nummern-Verweise, „Review-Profil“ statt Review-Config – Phase 6). Weitere Auswahlfrage-Stellen außerhalb der
  geänderten Abschnitte (Vorrang: Typ klären; Review-Profil fehlt; Thema/neues Thema; Stufe A; Phase 3; Grundhaltung)
  bleiben wörtlich und haben hier keine Zeile.

## Zielstruktur

Nur geänderte Abschnitte:

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | ~~Branch-Ermittlung~~ (entfällt, geht in Grundsätze auf) · **Grundsätze** (neu an der Stelle von „🚨 VERBINDLICHE REGEL: Auswahlfrage bei Entscheidungen“: Fragen, Branch, Push) mit Unterabschnitt **Typische Stellen für eine Auswahlfrage** · ChatGPTs Repo-Zugriff (Push-Prüfung: Satz zur Push-Policy) · VERBOTEN (drei Zeilen angepasst, eine neu) |

Description unverändert (Z. 1–11 byte-gleich geprüft). Abkürzung im Neu-Ort: `S` = `SKILL.md`. Durch den Wegfall von
„Branch-Ermittlung“ steht „Voraussetzung: Review-Profil“ jetzt direkt vor „Grundsätze“; die Reihenfolge der übrigen
Abschnitte bleibt.

Entscheidung Herbert (Umbau Phase 5): Ohne Push-Policy (kein Skill-Profil) bleibt das bisherige Verhalten – Auswahlfrage,
bei „Jetzt pushen“ pusht Claude Code selbst, Cowork liefert den Befehl.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#Frontmatter (Z. 3–10) | Description: Prompts und Folgeprompts für ChatGPT-Review, CGR-Archiv, nach Review-Profil; nicht für Handover, Claude-Prompts, vage Antworten | KEEP | S#Frontmatter | unverändert | | ✅ |
| R002 | SKILL.md#Branch-Ermittlung (Z. 51) | Branch aus dem Chat-Kontext verwenden | REWRITE | S#Grundsätze | jetzt Rückfall „Ohne Skill-Profil“ | | ✅ sinngemäß |
| R003 | SKILL.md#Branch-Ermittlung (Z. 51–52) | Mit Shell (Claude Code: Bash/PowerShell, Cowork: DC) `git branch --show-current` | REWRITE | S#Grundsätze | im Rückfall wörtlich; mit Profil `current` derselbe Befehl (N001) | | ✅ sinngemäß |
| R004 | SKILL.md#Branch-Ermittlung (Z. 52) | Ohne Shell und unbekannt: per Auswahlfrage fragen | REWRITE | S#Grundsätze | Rückfall: „ist er dann noch unbekannt (keine Shell, oder die Shell liefert keinen): Auswahlfrage“; Optionen aus R009 | | ✅ sinngemäß |
| R005 | SKILL.md#Branch-Ermittlung (Z. 53) | NIE automatisch einen Branch annehmen | MOVE | S#Grundsätze | wörtlich | | ✅ |
| R006 | SKILL.md#VERBINDLICHE REGEL (Z. 76–77) | Jede Entscheidungsfrage mit festen Optionen MUSS als Auswahlfrage, keine Prosa-Fragen | REWRITE | S#Grundsätze | „Fragen nur bei offener Entscheidung – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen ist –, dann als Auswahlfrage“ | | ✅ sinngemäß |
| R007 | SKILL.md#VERBINDLICHE REGEL (Z. 77–78) | Auswahlfrage = Frage-Werkzeug der Umgebung mit anklickbaren Optionen | REWRITE | S#Grundsätze | „mit dem Frage-Werkzeug der Umgebung“ | | ✅ sinngemäß |
| R008 | SKILL.md#VERBINDLICHE REGEL (Z. 78) | Werkzeugnamen: Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion` | DROP | | Werkzeugnamen im Regeltext (`docs/skill-quality.md`: Begriff „Auswahlfrage“, Handlung statt Werkzeug); Inhalt steckt in R007 | Gruppe A, freigegeben 28.09.2026 | ✅ |
| R009 | SKILL.md#Diese Fragen IMMER (Z. 84) | Branch-Ermittlung, nur wenn die Shell ihn nicht liefert → Branch-Namen aus `git branch -a` | MERGE | S#Grundsätze | R004 | | ✅ sinngemäß |
| R010 | SKILL.md#Diese Fragen IMMER (Z. 85) | Ungepushte Commits vor einem Prompt mit Repo-Zugriff → Jetzt pushen, Im Prompt vermerken, Abbrechen | REWRITE | S#Typische Stellen für eine Auswahlfrage | Situation ergänzt „(nicht bei Push-Policy `required-after-commit`)“, Optionen wörtlich (N002) | | ✅ sinngemäß |
| R011 | SKILL.md#Diese Fragen IMMER (Z. 86) | Phase 3: Ergebnisse übernehmen → Ergebnis-Ort, Tasks, Beides, Nur Zusammenfassung | MOVE | S#Typische Stellen für eine Auswahlfrage | wörtlich | | ✅ |
| R012 | SKILL.md#Diese Fragen IMMER (Z. 87) | Rundenstand aus Archiv widerspricht Chat → Archiv gilt, Chat gilt, Abbrechen | MOVE | S#Typische Stellen für eine Auswahlfrage | wörtlich | | ✅ |
| R013 | SKILL.md#Diese Fragen IMMER (Z. 88) | Phase 2 Stufe A: Entscheidungspunkte je Thema + immer „ChatGPT fragen“ | MOVE | S#Typische Stellen für eine Auswahlfrage | wörtlich | | ✅ |
| R014 | SKILL.md#Diese Fragen IMMER (Z. 89) | Uneinigkeit Claude/ChatGPT → Claude, ChatGPT, Mittelweg, Abbrechen | MOVE | S#Typische Stellen für eine Auswahlfrage | wörtlich | | ✅ |
| R015 | SKILL.md#Diese Fragen IMMER (Z. 90) | Review-Phase wechseln → Phase 2, Phase 3, weiter | MOVE | S#Typische Stellen für eine Auswahlfrage | wörtlich | | ✅ |
| R016 | SKILL.md#Prosa-Fragen NUR wenn (Z. 92–96) | Prosa nur bei offener Frage ohne feste Optionen, signalisierter Präferenz oder nötigem Freitext | REWRITE | S#Grundsätze | ein Satz, alle drei Fälle erhalten | | ✅ sinngemäß |
| R017 | SKILL.md#Serie abschließen (Z. 255–256) | Commit der Archivdateien im Format; Claude Code committet selbst, Cowork liefert den Befehl | KEEP | S#Serie abschließen | kein Push genannt; siehe Offene Fragen | | ✅ |
| R018 | SKILL.md#ChatGPTs Repo-Zugriff (Z. 276, 279) | Prompt-Block: Branch `[aktueller Branch]` immer verwenden, nicht `main`; bei jedem Dateizugriff angeben | KEEP | S#ChatGPTs Repo-Zugriff | Auffälligkeit bei `fixed:main`, siehe Offene Fragen | | ✅ |
| R019 | SKILL.md#ChatGPTs Repo-Zugriff (Z. 283) | Branch nicht hardcoden, den in der Sitzung ermittelten verwenden | KEEP | S#ChatGPTs Repo-Zugriff | ermittelt jetzt nach S#Grundsätze | | ✅ |
| R020 | SKILL.md#ChatGPTs Repo-Zugriff (Z. 285–287) | Push-Prüfung Pflicht vor jedem Prompt mit Repo-Zugriff: `git fetch --quiet && git log origin/<branch>..HEAD --oneline` | KEEP | S#ChatGPTs Repo-Zugriff | | | ✅ |
| R021 | SKILL.md#ChatGPTs Repo-Zugriff (Z. 287–288) | Bei ungepushten Commits Auswahlfrage; „Jetzt pushen“: Claude Code pusht selbst, Cowork liefert den Befehl | REWRITE | S#ChatGPTs Repo-Zugriff; S#Grundsätze | „Dann nach der Push-Policy (Abschnitt „Grundsätze“): ohne Rückfrage pushen oder Auswahlfrage …“; das bisherige Verhalten steht wörtlich als Rückfall ohne Push-Policy im Grundsatz Push (N002) | | ✅ sinngemäß |
| R022 | SKILL.md#ChatGPTs Repo-Zugriff (Z. 288–289) | Option „Im Prompt vermerken“ (Block „Stand auf GitHub ist <hash> …“) / „Abbrechen“ | KEEP | S#ChatGPTs Repo-Zugriff | | | ✅ |
| R023 | SKILL.md#ChatGPTs Repo-Zugriff (Z. 289) | Ohne Shell: User fragen, ob gepusht ist | KEEP | S#ChatGPTs Repo-Zugriff | | | ✅ |
| R024 | SKILL.md#ChatGPTs Repo-Zugriff (Z. 290) | Uncommittete Änderungen an genannten Dateien nennen (`git status --short`) | KEEP | S#ChatGPTs Repo-Zugriff | | | ✅ |
| R025 | SKILL.md#Phase 1: Initialprompt (Z. 427) | Repo-Zugriff-Block mit aktuellem Branch immer einfügen – nach Push-Prüfung | KEEP | S#Phase 1: Initialprompt | | | ✅ |
| R026 | SKILL.md#Stufe B (Z. 460) | Repo-Zugriff-Block mit aktuellem Branch immer einfügen | KEEP | S#Stufe B | | | ✅ |
| R027 | SKILL.md#VERBOTEN (Z. 534) | Branch automatisch annehmen (Shell fragen oder Auswahlfrage) | REWRITE | S#VERBOTEN | „– ohne Branch-Policy, Shell oder Auswahlfrage“ | | ✅ sinngemäß |
| R028 | SKILL.md#VERBOTEN (Z. 535) | Multiple-Choice als Prosa statt Auswahlfrage | REWRITE | S#VERBOTEN | „Prosa-Fragen bei festen Entscheidungsoptionen (Multiple-Choice, Stufe-A-Entscheidungspunkte)“ | | ✅ sinngemäß |
| R029 | SKILL.md#VERBOTEN (Z. 536) | Stufe-A-Entscheidungspunkte als Prosa statt Auswahlfrage | MERGE | S#VERBOTEN | R028 | | ✅ sinngemäß |
| R030 | SKILL.md#VERBOTEN (Z. 537) | Uneinigkeit ohne Auswahlfrage auflösen | KEEP | S#VERBOTEN | eigene Regel (User entscheidet), keine reine Prosa-Wiederholung | | ✅ |
| R031 | SKILL.md#VERBOTEN (Z. 539) | Prompt mit Repo-Zugriff-Block ohne Push-Prüfung | KEEP | S#VERBOTEN | gilt unabhängig von der Push-Policy | | ✅ |
| R032 | SKILL.md#VERBOTEN (Z. 541) | Phase 3 ohne Auswahlfrage „Ergebnisse übernehmen“ beenden | KEEP | S#VERBOTEN | | | ✅ |
| N001 | – | Branch nach der Branch-Policy: `current` → aktueller Branch aus der Shell; `fixed:<branch>` → muss dieser sein, sonst Auswahlfrage (wechseln / abbrechen); ohne Skill-Profil R002–R005 | NEW | S#Grundsätze | Phase 5 „Branch aus dem Profil“; `docs/skill-profile-v1.md` | | ✅ |
| N002 | – | Push bei der Push-Prüfung nach der Push-Policy: `user-only` → Befehl liefern, User pusht; `allowed`/`required-at-session-end` → Auswahlfrage, bei „Jetzt pushen“ pusht Claude; `required-after-commit` → ohne Rückfrage pushen; ohne Push-Policy wie bisher | NEW | S#Grundsätze; S#ChatGPTs Repo-Zugriff; S#Typische Stellen für eine Auswahlfrage | Phase 5 „Push aus dem Profil“; Rückfall nach Entscheidung Herbert; `required-at-session-end` siehe Offene Fragen | | ✅ |
| N003 | – | Pushen gegen die Push-Policy des Skill-Profils ist verboten | NEW | S#VERBOTEN | wie git-commit-helper | | ✅ |
| N004 | – | Skill-Profil vorhanden, aber keine Shell: bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage | NEW | SKILL.md#Grundsätze | Entscheidung Herbert 28.09.2026 (Sammelfreigabe Phase 5) | | ✅ |

## DROP-Gruppen

Von Herbert am 28.09.2026 freigegeben (Auswahlfrage vor dem Schreiben):

| Gruppe | IDs | Regelkern | Grund |
|---|---|---|---|
| A – Werkzeugnamen im Regeltext | R008 | Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion` als Namen des Frage-Werkzeugs | `docs/skill-quality.md` (Feste Begriffe, Neutralität): „Auswahlfrage“ statt Werkzeugname; die Handlung bleibt in R007 („Frage-Werkzeug der Umgebung“) |

Wird Gruppe A nicht freigegeben: R008 → KEEP, Klammer „(Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion`)“
hinter „Frage-Werkzeug der Umgebung“ im Grundsatz wieder einsetzen.

## Offene Fragen (Herbert)

1. **`required-at-session-end` bei der Push-Prüfung:** Entwurf behandelt es wie `allowed` (Auswahlfrage, vorgezogener
   Push bei „Jetzt pushen“), weil ChatGPT den Stand auf GitHub braucht. Alternative: kein Push vor Sitzungsende, nur
   „Im Prompt vermerken“ / „Abbrechen“ (so liest git-commit-helper die Policy für seine Sequenz).
2. **Commit der Archivdateien (Serie abschließen, R017):** Der Skill nennt dort keinen Push. Bei
   `required-after-commit` folgt der Push aus dem Profil; soll der Skill das ausdrücklich sagen? Nicht ergänzt.

## Verweise von außen

| Stelle | Verweis | Behandlung |
|---|---|---|
| `INDEX.md`, Invariante 1 (Z. 95) | „Jede ‚A oder B?‘-Frage geht durch `ask_user_input_v0`“ | Phase 5 „INDEX neu … Invarianten an ihren neuen Ort“ |
| `INDEX.md`, Invariante 2 „Branch-Ermittlung“ (Z. 97–99) | Branch immer per Auswahlfrage aus `git branch -a` | Phase 5 „INDEX neu“; widerspricht der Branch-Policy (`current` ohne Frage) |
| `INDEX.md`, Konfliktpaar chat-wechsel ↔ chatgpt-review (Z. 80) | „generisch → ask_user_input_v0“ | Phase 5 „INDEX neu“ |
| `docs/skill-profile-v1.md`, Pflichtfelder je Skill | chatgpt-review braucht Review.Config, Commit.Push-Policy | Push-Policy liest der Skill jetzt; Review.Config noch nicht (liest `## Review-Profil`) – Phase 6 |
| `CLAUDE.md`, Abschnitt „Review-Profil“ | Verweis bleibt, bis chatgpt-review die Config liest | Phase 5/6 |

## Prüfung

Von Herbert am 28.09.2026 freigegeben (Auswahlfrage vor dem Schreiben):
  Neu-Ort für KEEP/MOVE/REWRITE/MERGE im Entwurf gefunden.
- **Neu→Alt:** alle normativen Aussagen der geänderten Abschnitte (Grundsätze mit Tabelle, Push-Prüfung, VERBOTEN) einer
  R-ID oder N001–N003 zugeordnet; keine ungewollte neue Regel.
- **Diff:** `git diff --no-index` gegen `skills/chatgpt-review/SKILL.md` zeigt nur Branch-Ermittlung (entfernt),
  VERBINDLICHE REGEL → Grundsätze, eine Zeile Push-Prüfung und VERBOTEN; Frontmatter Z. 1–11 identisch.
- **Zeilen:** vorher 547, nachher 546.
- **Prüfskript:** nicht gelaufen (Entwurf im Scratchpad).
- **Routing-Eval:** wird nach dem Commit eingetragen.
