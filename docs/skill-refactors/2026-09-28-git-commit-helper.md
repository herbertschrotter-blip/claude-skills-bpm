# Regel-Inventar – git-commit-helper – 2026-09-28

Refactor von git-commit-helper in Umbau-Phase 5, Punkte „Regel ‚Fragen nur bei offener Entscheidung‘ in alle Skills“ und
„Branch und Push aus dem Profil lesen“ (`docs/skillsystem-umbau.md`). Dafür liest der Skill jetzt zuerst das
Skill-Profil v1 (`docs/skill-profile-v1.md`), mit Rückfall auf das ältere `## Commit-Profil`. Nach dem Refactor-Ablauf von
skill-pflege (`skills/skill-pflege/references/rule-inventory.md`); vorgesammelt mit
`tools/validate-skills.ps1 -Skill git-commit-helper -RuleInventory …` (37 Kandidaten), danach nach Urteil zu Regeln
zusammengefasst.

- Skill: git-commit-helper
- Stand vorher: 8a3e1f8 (SKILL.md, 273 Zeilen; keine references)
- Quellen: SKILL.md

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | Vorrang (unverändert) · **Grundsätze** (neu: Fragen, Branch, Push) · Commit-Format · **Skill-Profil** (statt „PROJEKTPROFIL“) · Schritt 0–3 · Regeln · VERBOTEN |

Description unverändert. Abkürzung im Neu-Ort: `S` = `SKILL.md`.

Entscheidung Herbert (28.09.2026): Ohne Push-Policy (kein Skill-Profil) bleibt `git push` wie bisher in der Sequenz.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#Frontmatter (Z. 3–10) | Description: Commit-Befehle und -Messages im Format, Versionsquelle und Doku-Checkliste aus dem Projektprofil; nicht für Code, Review, git push, Zustimmung | KEEP | S#Frontmatter | unverändert | | ✅ |
| R002 | SKILL.md#Vorrang (Z. 19–21) | Zuständig für Commit-Befehle, Messages, Bumps; sonst delegieren | KEEP | S#Vorrang | | | ✅ |
| R003 | SKILL.md#Vorrang (Z. 23–29) | Delegationstabelle an code-erstellen, mockup-erstellen, tracker, doc-pflege, audit | KEEP | S#Vorrang | | | ✅ |
| R004 | SKILL.md#Vorrang (Z. 31–33) | Nur bei Commit-Erstellung selbst zuständig | KEEP | S#Vorrang | | | ✅ |
| R005 | SKILL.md#Vorrang (Z. 35–39) | Inline-Vorschlag von code-erstellen ist kein Auslöser; erst bei ausdrücklichem Commit-Wunsch oder Delegation | KEEP | S#Vorrang | | | ✅ |
| R006 | SKILL.md#VERBINDLICHE REGEL (Z. 43–49) | Jede Entscheidungsfrage mit festen Optionen als Auswahlfrage, Werkzeug der Umgebung | REWRITE | S#Grundsätze | „Fragen nur bei offener Entscheidung, dann als Auswahlfrage“ | | ✅ sinngemäß |
| R007 | SKILL.md#Diese Fragen IMMER (Z. 55) | Branch unbekannt → Auswahl aus `git branch -a` | MERGE | S#Grundsätze | R013 | | ✅ sinngemäß |
| R008 | SKILL.md#Diese Fragen IMMER (Z. 56) | Typ unklar → Feature, Fix, Change, Refactor, Perf, Docs | MOVE | S#Grundsätze | typische Stelle | | ✅ |
| R009 | SKILL.md#Diese Fragen IMMER (Z. 57) | Version-Bump unklar → MAJOR, MINOR, PATCH | MOVE | S#Grundsätze | typische Stelle | | ✅ |
| R010 | SKILL.md#Diese Fragen IMMER (Z. 58) | Projektprofil fehlt → Profil anlegen, einmalig angeben, abbrechen | MERGE | S#Skill-Profil | R024 | | ✅ sinngemäß |
| R011 | SKILL.md#Prosa-Fragen NUR wenn (Z. 60–63) | Prosa nur bei offener Frage (Kurztitel) oder signalisierter Präferenz | MERGE | S#Grundsätze | R006 | | ✅ sinngemäß |
| R012 | SKILL.md#Branch-Ermittlung (Z. 67) | Branch aus dem Chat-Kontext verwenden | REWRITE | S#Grundsätze | „in der Sitzung schon bekannter Branch“, nach Branch-Policy | | ✅ sinngemäß |
| R013 | SKILL.md#Branch-Ermittlung (Z. 68–69) | Branch unbekannt → Auswahlfrage; nie automatisch annehmen | REWRITE | S#Grundsätze | zuerst Branch-Policy, ohne Profil die Shell, erst ohne Shell die Auswahlfrage (Phase 5) | | ✅ sinngemäß |
| R014 | SKILL.md#Commit-Format (Z. 73–78) | Format `[vX.Y.Z] Modul, Typ: Kurztitel` fest und projektübergreifend; Projektspezifisches im Profil | REWRITE | S#Commit-Format | „Projektprofil“ → „Skill-Profil“, „Bump-Regel“ → „Versionsregel“ | | ✅ sinngemäß |
| R015 | SKILL.md#Commit-Format (Z. 80–82) | Aufgaben-/Ticket-Nummer an den Anfang des Kurztitels oder in die zweite Zeile, nie vor `[vX.Y.Z]` | KEEP | S#Commit-Format | | | ✅ |
| R016 | SKILL.md#Commit-Format (Z. 84–87) | Modul aus der Modul-Liste; mehrere → Hauptmodul, Rest im Kurztitel; unabhängig → zwei Commits | REWRITE | S#Commit-Format | Modul-Liste des Skill-Profils | | ✅ sinngemäß |
| R017 | SKILL.md#Commit-Format (Z. 89–91) | Zweite Zeile optional, 1–3 Sätze; nie Prosa in der ersten Zeile | KEEP | S#Commit-Format | | | ✅ |
| R018 | SKILL.md#Typen (Z. 93–101) | Typ → Bump-Zuordnung | KEEP | S#Typen | | | ✅ |
| R019 | SKILL.md#Typen (Z. 103–105) | Zuordnung ist Standard; die Bump-Regel des Profils darf sie überschreiben | REWRITE | S#Typen | Versionsregel des Skill-Profils; zweites Beispiel „neue Nummer nur bei Änderungen unter `skills/**`“ | | ✅ sinngemäß |
| R020 | SKILL.md#Typen (Z. 107–109) | Version aus der Versionsquelle des Profils ermitteln (Beispiele) | REWRITE | S#Typen | Skill-Profil; ergänzt um `changelog:<Datei>` (oberster Eintrag) | | ✅ sinngemäß |
| R021 | SKILL.md#PROJEKTPROFIL (Z. 113–114) | Alles Projektspezifische steht im Repo; Quellen in fester Reihenfolge | REWRITE | S#Skill-Profil | Überschrift „Skill-Profil“ | | ✅ sinngemäß |
| R022 | SKILL.md#PROJEKTPROFIL (Z. 116–124) | Quelle 1: `## Commit-Profil` mit Modul-Namen, Versionsquelle, Bump-Regel, Doku-Checkliste | REWRITE | S#Skill-Profil | jetzt Quelle 2 (Rückfall) mit Zuordnung zu den v1-Feldern; Quelle 1 ist N001 | | ✅ sinngemäß |
| R023 | SKILL.md#PROJEKTPROFIL (Z. 125–128) | Fehlt der Abschnitt: Repo durchsuchen (docs/, *.md, Versionsdateien), Vorschlag zeigen | MOVE | S#Skill-Profil | jetzt Quelle 3 | | ✅ |
| R024 | SKILL.md#PROJEKTPROFIL (Z. 129–131) | Dann Auswahlfrage: Profil anlegen (mit Vorschlag) / einmalig angeben / abbrechen | REWRITE | S#Skill-Profil | angelegt wird ein `## Skill-Profil` | | ✅ sinngemäß |
| R025 | SKILL.md#PROJEKTPROFIL (Z. 133–134) | Profil nie aus dem Gedächtnis; einmal gelesen gilt es für die Sitzung | KEEP | S#Skill-Profil | | | ✅ |
| R026 | SKILL.md#SCHRITT 0 (Z. 138–141) | Arbeitsverzeichnis = Repo-Wurzel per `git rev-parse --show-toplevel`; Worktree | KEEP | S#SCHRITT 0 | | | ✅ |
| R027 | SKILL.md#SCHRITT 1 (Z. 146–149) | `git status --short`; kein Commit ohne Status | KEEP | S#SCHRITT 1 | | | ✅ |
| R028 | SKILL.md#SCHRITT 1a (Z. 153–157) | Versionsquelle auf die neue Nummer setzen, im selben Commit; ohne das kein neues `[vX.Y.Z]` | REWRITE | S#SCHRITT 1a | Skill-Profil; bei `changelog:` ein neuer oberster Eintrag | | ✅ sinngemäß |
| R029 | SKILL.md#SCHRITT 1b (Z. 161–163) | Doku-Checkliste vor der Commit-Sequenz abarbeiten | KEEP | S#SCHRITT 1b | | | ✅ |
| R030 | SKILL.md#SCHRITT 2 (Z. 167–171) | One-Block-Regel; in Claude Code dieselbe Sequenz als ein Aufruf | KEEP | S#SCHRITT 2 | | | ✅ |
| R031 | SKILL.md#PowerShell (Z. 173–179) | PowerShell-Sequenz mit `;`, inklusive `git push origin <branch>` | REWRITE | S#SCHRITT 2 | Push-Glied nur nach Push-Policy (N002); Vorlage unverändert | | ✅ sinngemäß |
| R032 | SKILL.md#Bash (Z. 181–187) | Bash-Sequenz mit `&&`, inklusive Push | REWRITE | S#SCHRITT 2 | wie R031 | | ✅ sinngemäß |
| R033 | SKILL.md#Regeln für die Sequenz (Z. 191) | Spezifische Pfade nach `git add` | KEEP | S#Regeln für die Sequenz | | | ✅ |
| R034 | SKILL.md#Regeln für die Sequenz (Z. 192) | Ein Commit pro logische Änderung | KEEP | S#Regeln für die Sequenz | | | ✅ |
| R035 | SKILL.md#Regeln für die Sequenz (Z. 193) | `"` für Commit-Messages | KEEP | S#Regeln für die Sequenz | | | ✅ |
| R036 | SKILL.md#Regeln für die Sequenz (Z. 194) | `git log -1` am Ende, damit Herbert den Hash sieht | REWRITE | S#Regeln für die Sequenz | „der Nutzer“ | | ✅ sinngemäß |
| R037 | SKILL.md#Regeln für die Sequenz (Z. 195) | Renames mit `git mv` | KEEP | S#Regeln für die Sequenz | | | ✅ |
| R038 | SKILL.md#Regeln für die Sequenz (Z. 196) | Branch-Name aus der Branch-Ermittlung, nie hartkodiert `main` | REWRITE | S#Regeln für die Sequenz | „nach den Grundsätzen“ | | ✅ sinngemäß |
| R039 | SKILL.md#Regeln für die Sequenz (Z. 197–198) | Tests vor dem Commit (Profil/CLAUDE.md) als erstes Glied; rot → kein Commit | REWRITE | S#Regeln für die Sequenz | Pre-Commit-Checks des Skill-Profils, die für die geänderten Dateien gelten; ohne Profil wie bisher | | ✅ sinngemäß |
| R040 | SKILL.md#Wenn ein Glied fehlschlägt (Z. 202–206) | Abbruch am fehlerhaften Glied, Ursache nennen, nichts überspringen, kein Teil-Commit pushen, dann ganze Sequenz neu | KEEP | S#Wenn ein Glied der Sequenz fehlschlägt | | | ✅ |
| R041 | SKILL.md#Mehrzeilig (Z. 210–212) | Mehrzeilig nur auf Wunsch (Herbert), in EINEM Block | REWRITE | S#Mehrzeilig | „der Nutzer“ | | ✅ sinngemäß |
| R042 | SKILL.md#SCHRITT 3 (Z. 216–219) | Doku-Checkliste aus dem Profil, vor der Sequenz, im selben Commit | REWRITE | S#SCHRITT 3 | `Doku-Check` des Skill-Profils bzw. `Doku-Checkliste` des alten Commit-Profils | | ✅ sinngemäß |
| R043 | SKILL.md#SCHRITT 3 (Z. 221–223) | Fehlt die Checkliste: docs/ und *.md auflisten, Auswahlfrage, Vorschlag fürs Profil | KEEP | S#SCHRITT 3 | | | ✅ |
| R044 | SKILL.md#SCHRITT 3 (Z. 225–237) | Beispiel-Checkliste (ADR/Quickload) | KEEP | S#SCHRITT 3 | | | ✅ |
| R045 | SKILL.md#SCHRITT 3 (Z. 239–247) | Beispiel-Checkliste (Bauplan/Übergabe) | KEEP | S#SCHRITT 3 | Projektbeispiele bleiben bis Phase 6 | | ✅ |
| R046 | SKILL.md#Regeln (Z. 251) | Pfade in der Schreibweise der Shell | KEEP | S#Regeln | | | ✅ |
| R047 | SKILL.md#Regeln (Z. 252) | `"` für Messages | KEEP | S#Regeln | | | ✅ |
| R048 | SKILL.md#Regeln (Z. 253) | Ein Commit = eine Änderung | KEEP | S#Regeln | | | ✅ |
| R049 | SKILL.md#Regeln (Z. 254) | Version korrekt hochzählen (Versionsquelle und Bump-Regel aus dem Projektprofil) | REWRITE | S#Regeln | Skill-Profil, Versionsregel | | ✅ sinngemäß |
| R050 | SKILL.md#Regeln (Z. 255) | One-Block-Regel | KEEP | S#Regeln | | | ✅ |
| R051 | SKILL.md#Regeln (Z. 256) | Keine Erklärungen | KEEP | S#Regeln | | | ✅ |
| R052 | SKILL.md#Regeln (Z. 257) | Renames: git mv | KEEP | S#Regeln | | | ✅ |
| R053 | SKILL.md#Regeln (Z. 258) | Arbeitsverzeichnis immer automatisch | KEEP | S#Regeln | | | ✅ |
| R054 | SKILL.md#Regeln (Z. 259) | Doc-Pflege immer vor dem Commit (Checkliste aus dem Projektprofil) | REWRITE | S#Regeln | Skill-Profil | | ✅ sinngemäß |
| R055 | SKILL.md#Regeln (Z. 260) | Projektprofil immer lesen, bevor Version oder Doku angefasst werden | REWRITE | S#Regeln | Skill-Profil | | ✅ sinngemäß |
| R056 | SKILL.md#Regeln (Z. 261) | Versionsdatei im selben Commit wie die Nummer | KEEP | S#Regeln | | | ✅ |
| R057 | SKILL.md#Regeln (Z. 262) | Mehrere Commits: je Commit ein Block | KEEP | S#Regeln | | | ✅ |
| R058 | SKILL.md#VERBOTEN (Z. 266) | Branch automatisch annehmen ohne Auswahlfrage | REWRITE | S#VERBOTEN | „ohne Branch-Policy, Shell oder Auswahlfrage“ | | ✅ sinngemäß |
| R059 | SKILL.md#VERBOTEN (Z. 267) | Typ-Auswahl als Prosa | MERGE | S#VERBOTEN | R061 | | ✅ sinngemäß |
| R060 | SKILL.md#VERBOTEN (Z. 268) | Version-Bump als Prosa | MERGE | S#VERBOTEN | R061 | | ✅ sinngemäß |
| R061 | SKILL.md#VERBOTEN (Z. 269) | Prosa-Fragen bei festen Entscheidungsoptionen | REWRITE | S#VERBOTEN | Beispiele Typ, Version-Bump, fehlender Profilwert in Klammern | | ✅ sinngemäß |
| R062 | SKILL.md#VERBOTEN (Z. 270) | Mehrere Code-Blöcke für eine Sequenz | KEEP | S#VERBOTEN | | | ✅ |
| R063 | SKILL.md#VERBOTEN (Z. 271) | Erklärungen zwischen den Befehlen | KEEP | S#VERBOTEN | | | ✅ |
| R064 | SKILL.md#VERBOTEN (Z. 272) | Versionsquelle oder Doku-Dateien raten | REWRITE | S#VERBOTEN | Skill-Profil | | ✅ sinngemäß |
| R065 | SKILL.md#VERBOTEN (Z. 273) | Werkzeugnamen fest verdrahten | KEEP | S#VERBOTEN | | | ✅ |
| N001 | – | Erste Quelle ist `## Skill-Profil` (v1): Bereich Commit, Branch-Policy, Checks; altes Commit-Profil als Rückfall mit Feldzuordnung | NEW | S#Skill-Profil | Phase 5 „Branch und Push aus dem Profil“; `docs/skill-profile-v1.md` | | ✅ |
| N002 | – | Push nach Push-Policy (`user-only`, `allowed`, `required-after-commit`, `required-at-session-end`); ohne Push-Policy bleibt `git push` in der Sequenz | NEW | S#Grundsätze; S#SCHRITT 2 | Entscheidung Herbert zum Rückfall | | ✅ |
| N003 | – | Pushen gegen die Push-Policy ist verboten | NEW | S#VERBOTEN | | | ✅ |
| N004 | – | Skill-Profil vorhanden, aber keine Shell: bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage | NEW | SKILL.md#Grundsätze | Entscheidung Herbert 28.09.2026 (Sammelfreigabe Phase 5) | | ✅ |

## DROP-Gruppen

Keine.

## Verweise von außen

| Stelle | Verweis | Behandlung |
|---|---|---|
| `skills/code-erstellen/SKILL.md`, `skills/doc-pflege/SKILL.md` | „Commit-Profil“, „Doku-Checkliste des Commit-Profils“ | Phase 5/6 beim jeweiligen Skill (Fragen, Branch, Push bzw. Refactor) |
| `docs/skill-profile-v1.md`, Pflichtfelder je Skill | git-commit-helper braucht Commit.Format, Module, Versionsquelle, Versionsregel, Push-Policy, Pre-Commit-Checks | passt; der Skill liest diese Felder jetzt |

## Prüfung

Wird nach dem Umbau eingetragen.
