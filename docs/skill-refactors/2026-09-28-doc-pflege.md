# Regel-Inventar – doc-pflege – 2026-09-28

Refactor von doc-pflege in Umbau-Phase 5, Punkte „Regel ‚Fragen nur bei offener Entscheidung‘ in alle Skills“ und
„Branch und Push aus dem Profil lesen“ (`docs/skillsystem-umbau.md`). Nach dem Refactor-Ablauf von skill-pflege
(`skills/skill-pflege/references/rule-inventory.md`); Muster: Inventar `2026-09-28-git-commit-helper.md`. Kandidaten
nach Urteil gesammelt (kein `-RuleInventory`-Lauf auf das Repo).

- Skill: doc-pflege
- Stand vorher: 416e115 (SKILL.md, 465 Zeilen; keine references)
- Quellen: SKILL.md
- Umfang: Punkte 3 und 4; übrige Abschnitte wörtlich unverändert (auch Projektwerte BPM/Heidi, Cowork-Teile,
  Modus-Nummern, „Doku-Profil“/„Commit-Profil“ – Phase 6)

## Zielstruktur

Nur geänderte Abschnitte:

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | **Grundsätze** (neu, an der Stelle von „🚨 VERBINDLICHE REGEL: Auswahlfrage bei Entscheidungen“ und „Branch-Ermittlung“: Fragen, Branch, Push) · **Modus 8 — Sitzungsabschluss** (Schritt 6: Push nach Push-Policy) · **VERBOTEN** (Branch-Zeile ergänzt, Prosa-Zeilen zusammengeführt) |

Description unverändert (Frontmatter Z. 1–16 byte-identisch). Abkürzung im Neu-Ort: `S` = `SKILL.md`.

Entscheidung Herbert (Umbau Phase 5): Ohne Push-Policy bleibt das bisherige Verhalten – im Sitzungsabschluss Commit +
Push.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#🚨 VERBINDLICHE REGEL (Z. 58–61) | Jede Entscheidungsfrage mit festen Optionen als Auswahlfrage, keine Prosa-Fragen | REWRITE | S#Grundsätze | „Fragen nur bei offener Entscheidung …, dann als Auswahlfrage“; Prosa-Verbot bleibt in R012–R014 und R025 | | ✅ sinngemäß |
| R002 | SKILL.md#🚨 VERBINDLICHE REGEL (Z. 61–62) | Auswahlfrage = Frage-Werkzeug der Umgebung mit anklickbaren Optionen | MERGE | S#Grundsätze | R001 („mit dem Frage-Werkzeug der Umgebung“; anklickbare Optionen = fester Begriff Auswahlfrage) | | ✅ sinngemäß |
| R003 | SKILL.md#🚨 VERBINDLICHE REGEL (Z. 62) | Werkzeugnamen in Klammern: Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion` | DROP | | Werkzeug-Syntax im Regeltext | Gruppe A, freigegeben 28.09.2026 | ✅ |
| R004 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 64) | Die Situationen der Tabelle immer als Auswahlfrage | REWRITE | S#Grundsätze | „Typische Stellen:“ – Auswahlfrage, wenn dort eine Entscheidung offen ist | | ✅ sinngemäß |
| R005 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 68) | Branch-Ermittlung (nur wenn die Shell ihn nicht liefert) → Branch-Namen aus `git branch -a` | MERGE | S#Grundsätze (Branch) | R018 (Optionen dort in Klammern) | | ✅ sinngemäß |
| R006 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 69) | Modus-Auswahl bei Unsicherheit → Modus 0-8 | MOVE | S#Grundsätze | Tabellenzeile wörtlich | | ✅ |
| R007 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 70) | Validierungsbefund (Modus 6) mit mehreren Lösungen → Doc anpassen, Quelle anpassen, Ignorieren mit Begründung | MOVE | S#Grundsätze | Tabellenzeile wörtlich | | ✅ |
| R008 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 71) | Sitzungsabschluss (Modus 8): fertig, offen (Rest im HANDOFF), blockiert (Befund) | MOVE | S#Grundsätze | Tabellenzeile wörtlich | | ✅ |
| R009 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 72) | Refactoring 7b, Inhalt passt in kein Kapitel → eigenes Kapitel am Ende, vorhandenes erweitern, Abbrechen | MOVE | S#Grundsätze | Tabellenzeile wörtlich | | ✅ |
| R010 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 73) | Doc-relevante Änderung → Jetzt pflegen, Später als Task anlegen, Ignorieren | MOVE | S#Grundsätze | Tabellenzeile wörtlich | | ✅ |
| R011 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 74) | Schema-/DB-Änderung dokumentieren → Reset-Anweisung, Migrations-Kapitel (User will explizit), Abbrechen | MOVE | S#Grundsätze | Tabellenzeile wörtlich | | ✅ |
| R012 | SKILL.md#Prosa-Fragen NUR wenn (Z. 76–78) | Prosa bei offener Frage ohne feste Optionen (Projektname, Modulname, Freitext-Beschreibung) | MOVE | S#Grundsätze | Punkt wörtlich; Überschrift → „Prosa-Fragen nur, wenn:“ | | ✅ |
| R013 | SKILL.md#Prosa-Fragen NUR wenn (Z. 79) | Prosa, wenn der User eine Präferenz signalisiert hat | MOVE | S#Grundsätze | Punkt wörtlich | | ✅ |
| R014 | SKILL.md#Prosa-Fragen NUR wenn (Z. 80) | Prosa, wenn Freitext-Input nötig ist | MOVE | S#Grundsätze | Punkt wörtlich | | ✅ |
| R015 | SKILL.md#Branch-Ermittlung (Z. 86) | Branch aus dem Chat-Kontext verwenden | REWRITE | S#Grundsätze (Branch) | gilt jetzt im Rückfall „Ohne Skill-Profil“; mit Profil N002 | | ✅ sinngemäß |
| R016 | SKILL.md#Branch-Ermittlung (Z. 86–87) | Mit Shell (Claude Code: Bash/PowerShell, Cowork: DC) `git branch --show-current` | REWRITE | S#Grundsätze (Branch) | Rückfall wörtlich; mit Profil `current` → Shell (N002) | | ✅ sinngemäß |
| R017 | SKILL.md#Branch-Ermittlung (Z. 87–88) | Nennt das Profil einen Pflicht-Branch und der aktuelle weicht ab → Auswahlfrage | REWRITE | S#Grundsätze (Branch) | mit Profil `fixed:<branch>` (N002); im Rückfall „das Profil“ → „ein älteres Profil der `CLAUDE.md`“ | | ✅ sinngemäß |
| R018 | SKILL.md#Branch-Ermittlung (Z. 88) | Ohne Shell und unbekannt: per Auswahlfrage fragen | MOVE | S#Grundsätze (Branch) | wörtlich im Rückfall; ergänzt um die Optionen aus R005 | | ✅ |
| R019 | SKILL.md#Branch-Ermittlung (Z. 89) | NIE automatisch einen Branch annehmen | MOVE | S#Grundsätze (Branch) | wörtlich | | ✅ |
| R020 | SKILL.md#Voraussetzung: Doku-Profil (Z. 114) | Profilfeld Sitzungsabschluss, Beispiel Heidi: „… Commit + Push“ | KEEP | S#Voraussetzung: Doku-Profil | Projektwert (Heidi-Beispiel), bleibt bis Phase 6 | | ✅ |
| R021 | SKILL.md#Modus 8 — Sitzungsabschluss (Z. 421) | Commit `[vX.Y.Z] <Doku-Modul>, Docs: Sitzungsabschluss <Datum> – <Kurztitel>` über git-commit-helper | KEEP | S#Modus 8 — Sitzungsabschluss | Format wörtlich | | ✅ |
| R022 | SKILL.md#Modus 8 — Sitzungsabschluss (Z. 421) | Nach dem Commit pushen („+ Push“) | REWRITE | S#Modus 8 — Sitzungsabschluss; S#Grundsätze (Push) | „Push nach der Push-Policy (Grundsätze)“; ohne Push-Policy weiter Commit + Push | | ✅ sinngemäß |
| R023 | SKILL.md#VERBOTEN (Z. 458) | Branch automatisch annehmen (Shell fragen oder Auswahlfrage) | REWRITE | S#VERBOTEN | „Branch-Policy“ in der Klammer ergänzt | | ✅ sinngemäß |
| R024 | SKILL.md#VERBOTEN (Z. 459) | Modus-Auswahl als Prosa bei Unsicherheit – IMMER Auswahlfrage | MERGE | S#VERBOTEN | R025 | | ✅ sinngemäß |
| R025 | SKILL.md#VERBOTEN (Z. 460) | Prosa-Fragen bei festen Entscheidungsoptionen | REWRITE | S#VERBOTEN | Beispiel „(z.B. Modus-Auswahl bei Unsicherheit)“ aus R024 ergänzt | | ✅ sinngemäß |
| N001 | – | Nur fragen, wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen ist | NEW | S#Grundsätze | Phase 5 „Fragen nur bei offener Entscheidung“; `docs/skill-quality.md#Zusammenspiel` | | ✅ |
| N002 | – | Branch nach Branch-Policy: `current` → aktueller Branch aus der Shell; `fixed:<branch>` → muss dieser sein, sonst Auswahlfrage (wechseln / abbrechen) | NEW | S#Grundsätze (Branch) | Phase 5 „Branch aus dem Profil“; `docs/skill-profile-v1.md` | | ✅ |
| N003 | – | Push nach Push-Policy: `user-only` kein Push (User pusht); `allowed` nur auf ausdrücklichen Wunsch; `required-after-commit` / `required-at-session-end` Push nach dem Commit | NEW | S#Grundsätze (Push); S#Modus 8 — Sitzungsabschluss | Phase 5 „Push aus dem Profil“; Rückfall ohne Push-Policy = R022 | | ✅ |
| N004 | – | Skill-Profil vorhanden, aber keine Shell: bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage | NEW | SKILL.md#Grundsätze | Entscheidung Herbert 28.09.2026 (Sammelfreigabe Phase 5) | | ✅ |

## DROP-Gruppen

Von Herbert am 28.09.2026 freigegeben (Auswahlfrage vor dem Schreiben):

| Gruppe | IDs | Regelkern | Grund | Freigabe |
|---|---|---|---|---|
| A – Werkzeug-Syntax | R003 | Werkzeugnamen `ask_user_input_v0` (Cowork) und `AskUserQuestion` (Claude Code) als Beispiel für die Auswahlfrage | Werkzeugnamen einer Umgebung im Regeltext (`docs/skill-quality.md`, Neutralität „Handlung statt Werkzeug“ und fester Begriff „Auswahlfrage“); die Handlung steht als „Frage-Werkzeug der Umgebung“ in N001/R001 | offen |

Bei „behalten“: hinter „mit dem Frage-Werkzeug der Umgebung“ die Klammer „(Cowork `ask_user_input_v0`, Claude Code
`AskUserQuestion`)“ wieder einsetzen; R003 wird dann MOVE.

## Verweise von außen

| Stelle | Verweis | Behandlung |
|---|---|---|
| `skills/chat-wechsel/SKILL.md` (Z. 20, 394–396) | „doc-pflege Modus 8 (Sitzungsabschluss) … Commit + Push“ | Push gilt jetzt nach Push-Policy; beim Phase-5-Punkt „Push“ in chat-wechsel angleichen; Nummern-Verweis „Modus 8“ in Phase 6 |
| `skills/git-commit-helper/SKILL.md` (Entwurf, Grundsätze) | `required-at-session-end`: „gepusht wird am Ende der Sitzung“ | passt: doc-pflege pusht im Sitzungsabschluss nach dem Commit (N003) |
| `docs/skill-profile-v1.md`, Pflichtfelder je Skill | doc-pflege: Doku.Router, Doku.Standard, Doku.Entscheidungs-Ort | passt (Branch-Policy ist Grundfeld; Push-Policy hat einen Rückfall); ob Commit.Push-Policy dort genannt wird, entscheidet Herbert |
| `skills/audit/SKILL.md` (Z. 93, 214), `INDEX.md` (Z. 24) | doc-pflege Modus 0/6, „9 Modi (0–8)“ | von diesem Refactor nicht berührt; Phase 6 |

## Prüfung

- **Alt→Neu:** 25 IDs, alle mit Zustand (KEEP 2, MOVE 11, MERGE 3, REWRITE 8, DROP 1). Die 24 Nicht-DROP-Zeilen sind
  im Entwurf gefunden (Lesen der Abschnitte Grundsätze, Voraussetzung: Doku-Profil, Modus 8, VERBOTEN).
- **Neu→Alt:** normative Aussagen der geänderten Abschnitte von Hand gesammelt (Grundsätze: Fragen-Satz, 6
  Tabellenzeilen, 3 Prosa-Punkte, Branch-Satz mit Policy und Rückfall, Push mit 3 Policy-Zeilen und Rückfall; Modus 8
  Schritt 6; 2 VERBOTEN-Zeilen). Alle gehören zu einer R-ID oder zu N001–N003; keine ungewollt neue Regel.
- **Diff** (`git diff --no-index` Repo ↔ Entwurf): drei Hunks – Z. 58–89 → Grundsätze; Modus 8 Schritt 6; VERBOTEN
  Z. 458–460. Sonst keine Unterschiede. Frontmatter Z. 1–16 byte-identisch (`cmp`).
- **Zeilen:** 465 vorher → 463 nachher.
- **Prüfskript:** nicht gelaufen (laut Auftrag nicht nötig); läuft als Check skill-validation vor dem Commit.
- **Routing-Eval:** keine eigene Messung nach v0.39.1 (Entscheidung Herbert: v0.39.1 ändert nur Regeltext nach dem Auslösen, die Description ist unverändert). Maßgeblich ist die Messung von v0.38.2 am 28.09.2026 auf 17ec20d (36 Fälle `audit`/`code-erstellen`/`doc-pflege`/`mockup-erstellen`, 100/108 Läufe, Einzelheiten in `docs/skill-refactors/2026-09-28-code-erstellen.md`, Abschnitt Prüfung); mitgetaggte Fälle liefen zusätzlich auf a0fb0a5 (`code-with-task-ref`, `doc-changelog` je 2/3, Sandbox-Muster).
