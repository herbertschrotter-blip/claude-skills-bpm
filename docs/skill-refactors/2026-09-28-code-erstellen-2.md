# Regel-Inventar – code-erstellen (Teil 2: Punkte 3 und 4) – 2026-09-28

Teil-Refactor von code-erstellen in Umbau-Phase 5, Punkte „Regel ‚Fragen nur bei offener Entscheidung‘ in alle Skills
übernehmen“ und „Branch und Push aus dem Profil lesen“ (`docs/skillsystem-umbau.md`). Teil 1 (Abschnitt
„Arbeitsverzeichnis“) steht in `docs/skill-refactors/2026-09-28-code-erstellen.md` und bleibt unberührt; die IDs hier
sind eigene (ab R001). Nach dem Refactor-Ablauf von skill-pflege (`skills/skill-pflege/references/rule-inventory.md`),
Regeln nach Urteil gesammelt; das Prüfskript mit `-RuleInventory` ist nicht gelaufen (Entwurf außerhalb des Repos).

- Skill: code-erstellen
- Stand vorher: 0c094a6 (SKILL.md, 504 Zeilen; Fragenblock Z. 57–123, Branch-Ermittlung Z. 127–137, VERBOTEN
  Z. 476–504)
- Umfang: Punkte 3 und 4; übrige Abschnitte wörtlich unverändert (auch „Arbeitsverzeichnis“ aus Teil 1)
- Quellen: SKILL.md; `references/stacks/*.md` per Grep geprüft – keine Fragen-, Branch- oder Push-Regeln
- Push: kommt im Skill nicht vor (der Commit läuft über git-commit-helper, Schritt 9) – nichts ergänzt

## Zielstruktur

Nur die geänderten Abschnitte; Description (Frontmatter Z. 1–17) byte-gleich.

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | **Grundsätze** an der Stelle von „🚨 VERBINDLICHE REGEL: Auswahlfrage bei Entscheidungen“ und „Branch-Ermittlung“: Fragen nur bei offener Entscheidung (Typische Stellen als Tabelle, Prosa-Fälle) · Branch (Branch-Policy, Rückfall ohne Skill-Profil) |
| `SKILL.md` | **VERBOTEN**: Zeile „Branch automatisch annehmen“ neu gefasst; die Prosa-Zeilen zu Branch, Task-Zuordnung, Modus und Blocking in einer Zeile „Prosa-Fragen bei festen Entscheidungsoptionen“ |

Abkürzungen im Neu-Ort: `S` = `SKILL.md`; `S#Grundsätze (Fragen)` bzw. `S#Grundsätze (Branch)` = der jeweilige Punkt.

Der Entwurf zeigt den Stand **nach** Freigabe der DROP-Gruppe A. Wird sie abgelehnt, kommen R020/R021 als Beispiel unter
den Punkt „Fragen“ zurück und bekommen einen anderen Zustand.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#VERBINDLICHE REGEL (Z. 59–60, 65) | Jede Entscheidungsfrage mit festen Optionen MUSS eine Auswahlfrage sein, keine Prosa-Fragen | REWRITE | S#Grundsätze (Fragen) | „Fragen nur bei offener Entscheidung …, dann als Auswahlfrage“ | | ✅ sinngemäß |
| R002 | SKILL.md#VERBINDLICHE REGEL (Z. 60–63) | Auswahlfrage = Frage-Werkzeug der Umgebung mit anklickbaren Optionen (Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion`); überall im Skill so gemeint | REWRITE | S#Grundsätze (Fragen) | „mit dem Frage-Werkzeug der Umgebung“; Werkzeugnamen entfallen (skill-quality.md#Neutralität, Begriff „Auswahlfrage“) | | ✅ sinngemäß |
| R003 | SKILL.md#Diese Fragen IMMER (Z. 69) | Branch-Ermittlung, wenn die Shell ihn nicht liefert → alle Branch-Namen aus `git branch -a` als Optionen | MERGE | S#Grundsätze (Branch) | R031; „Optionen = alle Branch-Namen, z.B. aus `git branch -a`“ | | ✅ sinngemäß |
| R004 | SKILL.md#Diese Fragen IMMER (Z. 70) | Modus unklar → Lite, Standard, Deep | MOVE | S#Grundsätze (Fragen) | typische Stelle, wörtlich | | ✅ |
| R005 | SKILL.md#Diese Fragen IMMER (Z. 71) | Zielschicht mehrdeutig → Domain, Application, Infrastructure, UI | MOVE | S#Grundsätze (Fragen) | typische Stelle, wörtlich | | ✅ |
| R006 | SKILL.md#Diese Fragen IMMER (Z. 72) | Mehrere Referenz-Implementierungen → Dateinamen als Optionen | MOVE | S#Grundsätze (Fragen) | typische Stelle, wörtlich | | ✅ |
| R007 | SKILL.md#Diese Fragen IMMER (Z. 73) | Fachliche Invariante würde verletzt → Trotzdem fortsetzen / Abbrechen / Andere Lösung | MOVE | S#Grundsätze (Fragen) | typische Stelle, wörtlich | | ✅ |
| R008 | SKILL.md#Diese Fragen IMMER (Z. 74) | Ausgabeformat mehrdeutig (nur Cowork) → Komplette Datei, SUCHE/ERSETZE, Download | MOVE | S#Grundsätze (Fragen) | typische Stelle, wörtlich; Cowork-Teil bleibt bis Phase 6 | | ✅ |
| R009 | SKILL.md#Diese Fragen IMMER (Z. 75) | ClickUp-Task-Zuordnung nach Commit → Kandidaten + Kein Task + Neuen Task anlegen | MOVE | S#Grundsätze (Fragen) | typische Stelle, wörtlich | | ✅ |
| R010 | SKILL.md#Diese Fragen IMMER (Z. 76) | Mehrere Blocking Conditions → welche Datei zuerst laden (Kandidaten) | MOVE | S#Grundsätze (Fragen) | typische Stelle, wörtlich | | ✅ |
| R011 | SKILL.md#Diese Fragen IMMER (Z. 77) | Commit-Version unklar → MAJOR, MINOR, PATCH | MOVE | S#Grundsätze (Fragen) | typische Stelle, wörtlich | | ✅ |
| R012 | SKILL.md#Diese Fragen IMMER (Z. 78) | User muss Referenzdatei angeben → Kandidaten aus Projektstruktur | MOVE | S#Grundsätze (Fragen) | typische Stelle, wörtlich | | ✅ |
| R013 | SKILL.md#Diese Fragen IMMER (Z. 79) | Bestehende Daten/Configs betroffen → Daten löschen + neu anlegen / Migration bauen / Abbrechen | MOVE | S#Grundsätze (Fragen) | typische Stelle, wörtlich | | ✅ |
| R014 | SKILL.md#Diese Fragen IMMER (Z. 80) | Tests rot nach dem Bau → Fix jetzt / Test anpassen (Begründung) / Abbrechen | MOVE | S#Grundsätze (Fragen) | typische Stelle, wörtlich | | ✅ |
| R015 | SKILL.md#Diese Fragen IMMER (Z. 81) | Mockup-Pflicht greift (Deep + UI) → Mockup zuerst / Ohne Mockup weiter | MOVE | S#Grundsätze (Fragen) | typische Stelle, wörtlich | | ✅ |
| R016 | SKILL.md#Prosa-Fragen NUR wenn (Z. 85–86) | Prosa bei offener Frage ohne feste Optionen (Beispiel Kurztitel) | MOVE | S#Grundsätze (Fragen) | fast wörtlich (Zeilenumbruch zusammengezogen) | | ✅ |
| R017 | SKILL.md#Prosa-Fragen NUR wenn (Z. 87) | Prosa, wenn der User gerade eine klare Präferenz signalisiert hat | MOVE | S#Grundsätze (Fragen) | wörtlich | | ✅ |
| R018 | SKILL.md#Prosa-Fragen NUR wenn (Z. 88) | Prosa bei Erklärung/Kontext ohne echte Entscheidung | MOVE | S#Grundsätze (Fragen) | wörtlich | | ✅ |
| R019 | SKILL.md#Prosa-Fragen NUR wenn (Z. 89) | Prosa bei Freitext-Input (neuer Klassenname, neue Commit-Message) | MOVE | S#Grundsätze (Fragen) | wörtlich | | ✅ |
| R020 | SKILL.md#Wie die Auswahlfrage aussieht (Z. 91–103) | Syntax-Beispiel einfache Auswahl (`ask_user_input_v0`, Modus-Frage); Claude Code: `AskUserQuestion` mit denselben Optionen | DROP | | Werkzeug-Syntax-Beispiel; Handlung in R001/R002, Optionen in R004 | Gruppe A, freigegeben 28.09.2026 | ✅ |
| R021 | SKILL.md#Wie die Auswahlfrage aussieht (Z. 105–115) | Syntax-Beispiel Branch-Auswahl (`ask_user_input_v0`, BPM-Branchnamen) | DROP | | Werkzeug-Syntax-Beispiel mit Projektwerten; Branch-Auswahl in R031 | Gruppe A, freigegeben 28.09.2026 | ✅ |
| R022 | SKILL.md#VERBINDLICHE REGEL › VERBOTEN (Z. 119) | Branch-Liste im Chat aufzählen und auf getippte Antwort warten | MERGE | S#VERBOTEN | R039 (gleiche Regel, allgemein) | | ✅ sinngemäß |
| R023 | SKILL.md#VERBINDLICHE REGEL › VERBOTEN (Z. 120) | „Lite oder Standard oder Deep?“ als Prosa | MERGE | S#VERBOTEN | R036 (Modus-Auswahl) | | ✅ sinngemäß |
| R024 | SKILL.md#VERBINDLICHE REGEL › VERBOTEN (Z. 121) | „Welche Datei soll noch geladen werden?“ als Prosa, wenn Kandidaten bekannt | MERGE | S#VERBOTEN | R036 (Blocking-Condition-Auflösung) | | ✅ sinngemäß |
| R025 | SKILL.md#VERBINDLICHE REGEL › VERBOTEN (Z. 122) | „Passt zu <PRÄFIX>-NNN. tracker done ausführen?“ als Prosa | MERGE | S#VERBOTEN | R036 (Task-Zuordnung nach Commit) | | ✅ sinngemäß |
| R026 | SKILL.md#VERBINDLICHE REGEL › VERBOTEN (Z. 123) | Optionen-Aufzählung im Chat ohne Auswahlfrage | MERGE | S#VERBOTEN | R039 | | ✅ sinngemäß |
| R027 | SKILL.md#Branch-Ermittlung (Z. 127, Überschrift) | Branch-Ermittlung ist Pflicht vor dem ersten Schreibzugriff | MOVE | S#Grundsätze (Branch) | „(PFLICHT vor dem ersten Schreibzugriff)“ | | ✅ |
| R028 | SKILL.md#Branch-Ermittlung (Z. 129) | In der Sitzung schon bekannter Branch → verwenden | MOVE | S#Grundsätze (Branch) | wörtlich; gilt jetzt als Rückfall ohne Skill-Profil | | ✅ |
| R029 | SKILL.md#Branch-Ermittlung (Z. 130–131) | Shell verfügbar: `git branch --show-current` liefert den Branch – Tatsache, keine Frage | MOVE | S#Grundsätze (Branch) | wörtlich im Rückfall; mit Skill-Profil entspricht es `current` (N002) | | ✅ |
| R030 | SKILL.md#Branch-Ermittlung (Z. 131–133) | Pflicht-Branch im Code-Profil (Beispiel Heidi) und aktueller weicht ab → Auswahlfrage wechseln / trotzdem / abbrechen, nie stumm weiter | MOVE | S#Grundsätze (Branch) | wörtlich im Rückfall; mit Skill-Profil gilt `fixed:<branch>` mit wechseln / abbrechen (N002) | | ✅ |
| R031 | SKILL.md#Branch-Ermittlung (Z. 134–135) | Keine Shell: Branches auflisten, per Auswahlfrage den aktiven wählen lassen (Optionen = Branch-Namen) | MOVE | S#Grundsätze (Branch) | fast wörtlich im Rückfall; ergänzt um R003 („alle …, z.B. aus `git branch -a`“) | | ✅ |
| R032 | SKILL.md#Branch-Ermittlung (Z. 136) | Gewählten Branch für die gesamte Sitzung merken | MOVE | S#Grundsätze (Branch) | wörtlich im Rückfall | | ✅ |
| R033 | SKILL.md#Branch-Ermittlung (Z. 137) | NIE automatisch einen Branch annehmen (weder `main` noch einen anderen) | MOVE | S#Grundsätze (Branch) | wörtlich; gilt mit und ohne Skill-Profil | | ✅ |
| R034 | SKILL.md#VERBOTEN (Z. 485) | Branch automatisch annehmen ohne User-Auswahl | REWRITE | S#VERBOTEN | „— ohne Branch-Policy, Shell oder Auswahlfrage“ (Branch-Policy `current` und Shell fragen nicht) | | ✅ sinngemäß |
| R035 | SKILL.md#VERBOTEN (Z. 486) | Branch-Auswahl als Prosa, wenn die Shell ihn nicht liefert – IMMER Auswahlfrage | MERGE | S#VERBOTEN | R036 | | ✅ sinngemäß |
| R036 | SKILL.md#VERBOTEN (Z. 490) | Task-Zuordnung nach Commit als Prosa – IMMER Auswahlfrage | REWRITE | S#VERBOTEN | „Prosa-Fragen bei festen Entscheidungsoptionen — IMMER Auswahlfrage“ mit den Fällen Branch-Auswahl, Task-Zuordnung, Modus, Blocking in Klammern | | ✅ sinngemäß |
| R037 | SKILL.md#VERBOTEN (Z. 491) | Modus-Auswahl als Prosa bei Unsicherheit – IMMER Auswahlfrage | MERGE | S#VERBOTEN | R036 | | ✅ sinngemäß |
| R038 | SKILL.md#VERBOTEN (Z. 492) | Blocking-Condition-Auflösung als Prosa, wenn Kandidaten bekannt – IMMER Auswahlfrage | MERGE | S#VERBOTEN | R036 | | ✅ sinngemäß |
| R039 | SKILL.md#VERBOTEN (Z. 500) | Optionen im Chat aufzählen und auf getippte Antwort warten | KEEP | S#VERBOTEN | Ziel von R022, R026 | | ✅ |
| N001 | – | Fragen nur, wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen ist | NEW | S#Grundsätze (Fragen) | Phase 5; skill-quality.md#Zusammenspiel | | ✅ |
| N002 | – | Branch nach der Branch-Policy des Skill-Profils: `current` → aktueller Branch aus der Shell; `fixed:<branch>` → muss dieser sein, sonst Auswahlfrage wechseln / abbrechen; ohne Skill-Profil der bisherige Ablauf (R028–R032) | NEW | S#Grundsätze (Branch) | Phase 5; docs/skill-profile-v1.md (Branch-Policy) | | ✅ |
| N003 | – | Skill-Profil vorhanden, aber keine Shell: bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage | NEW | SKILL.md#Grundsätze | Entscheidung Herbert 28.09.2026 (Sammelfreigabe Phase 5) | | ✅ |

## DROP-Gruppen

Von Herbert am 28.09.2026 freigegeben (Auswahlfrage vor dem Schreiben):

| Gruppe | IDs | Regelkern | Grund |
|---|---|---|---|
| A – Werkzeug-Syntax-Beispiele | R020, R021 | Zwei `ask_user_input_v0(...)`-Codeblöcke (Modus, Branch) samt Hinweis „Claude Code: `AskUserQuestion` mit denselben Optionen“ | Syntax eines bestimmten Werkzeugs im Kern (skill-quality.md#Neutralität); die Handlung steht in R001/R002, die Optionen in R004 und R031; R021 trägt zudem BPM-Branchnamen |

Freigabe: freigeben / einzelne behalten (IDs nennen) / abbrechen.

## Verweise von außen

| Stelle | Verweis | Behandlung |
|---|---|---|
| `INDEX.md`, Invarianten „1. `ask_user_input_v0` bei Entscheidungen“ und „2. Branch-Ermittlung“ | Werkzeugname; Branch „bei jedem GitHub-Zugriff aus `git branch -a` per `ask_user_input_v0`“ – passt nicht mehr zu Branch-Policy `current` | Phase 5, Punkt „INDEX neu … Invarianten 1–10 an ihren neuen Ort“ |
| `skills/tracker/SKILL.md` (Z. 424), `skills/tracker/references/anti-patterns.md` (Z. 21) | code-erstellen nach Commit: Auswahlfrage „Passt zu <Task>. `tracker done`?“ | passt; typische Stelle R009 und Schritt 10 bleiben |
| `docs/skill-refactors/2026-09-28-git-commit-helper.md`, Verweise von außen | „Commit-Profil“ und „Doku-Checkliste des Commit-Profils“ in code-erstellen Schritt 9 | kein Branch/Push, daher nicht in diesem Teil → Phase 6 |
| `docs/skill-refactors/2026-09-28-code-erstellen.md` (Teil 1) | Abschnitt „Arbeitsverzeichnis“ | unberührt |

## Prüfung

- **Freigabe:** DROP-Gruppe A offen; der Entwurf nimmt die Freigabe an.
- **Alt→Neu:** 39 IDs mit Zustand (KEEP 1, MOVE 23, MERGE 9, REWRITE 4, DROP 2); jeder Neu-Ort im Entwurf gelesen.
- **Neu→Alt:** Der Abschnitt „Grundsätze“ und die zwei neuen VERBOTEN-Zeilen sind vollständig zugeordnet (R001–R019,
  R027–R034, R036, N001, N002); keine ungewollt neue Regel.
- **Diff:** `git diff --no-index` zeigt nur die Hunks „Grundsätze“ (alt Z. 57–137 → neu Z. 57–94) und VERBOTEN (alt
  Z. 485–492 → neu Z. 442–446). Frontmatter Z. 1–17 byte-gleich, Abschnitt „Arbeitsverzeichnis“ identisch.
- **Größe:** SKILL.md 504 → 458 Zeilen.
- **Prüfskript:** nicht gelaufen (Entwurf außerhalb des Repos).
- **Routing-Eval:** keine eigene Messung nach v0.39.1 (Entscheidung Herbert: v0.39.1 ändert nur Regeltext nach dem Auslösen, die Description ist unverändert). Maßgeblich ist die Messung von v0.38.2 am 28.09.2026 auf 17ec20d (36 Fälle `audit`/`code-erstellen`/`doc-pflege`/`mockup-erstellen`, 100/108 Läufe, Einzelheiten in `docs/skill-refactors/2026-09-28-code-erstellen.md`, Abschnitt Prüfung); mitgetaggte Fälle liefen zusätzlich auf a0fb0a5 (`code-with-task-ref`, `doc-changelog` je 2/3, Sandbox-Muster).
