# Regel-Inventar – mockup-erstellen – 2026-09-28

Refactor von mockup-erstellen in Umbau-Phase 5, Punkte „Regel ‚Fragen nur bei offener Entscheidung‘ in alle Skills“ und
„Branch und Push aus dem Profil lesen“ (`docs/skillsystem-umbau.md`). Nach dem Refactor-Ablauf von skill-pflege
(`skills/skill-pflege/references/rule-inventory.md`); die Kandidaten der geänderten Abschnitte sind nach Urteil gesammelt
(Prüfskript mit `-RuleInventory` nicht gelaufen).

- Skill: mockup-erstellen
- Stand vorher: 1b0a4a4 (SKILL.md, 595 Zeilen; keine references)
- Umfang: Punkte 3 und 4; übrige Abschnitte wörtlich unverändert
- Quellen: SKILL.md (Grep nach Fragenregel, Branch und Push; references gibt es nicht)

## Zielstruktur

Nur die geänderten Abschnitte:

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | **Grundsätze** (neu, an der Stelle von „🚨 VERBINDLICHE REGEL: Auswahlfrage bei Entscheidungen“ und „Branch-Ermittlung“: Fragen, Branch) · **VERBOTEN** (Branch-Zeile angepasst, Prosa-Zeilen zusammengeführt) |

Description unverändert. Abkürzung im Neu-Ort: `S` = `SKILL.md`.

- **Branch:** nach der Branch-Policy des Skill-Profils; ohne Skill-Profil der bisherige Ablauf des Skills wörtlich
  (Chat-Kontext, Shell, Pflicht-Branch aus dem Code-Profil, ohne Shell Auswahlfrage).
- **Push:** kommt im Skill nicht vor (Schritt 5 liefert nur einen Commit-Vorschlag, ohne Push). Nach Auftrag nichts
  ergänzt. Die Entscheidung Herbert (28.09.2026) „ohne Push-Policy bleibt das bisherige Verhalten“ hat hier keine Wirkung.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#Frontmatter (Z. 3–13) | Description: HTML-Mockups nach dem Mockup-Profil; nicht für XAML/Lit-Implementierung, kleine UI-Fixes, Nicht-UI-Design | KEEP | S#Frontmatter | unverändert (Z. 1–14 byte-gleich) | | ✅ |
| R002 | SKILL.md#VERBINDLICHE REGEL (Z. 59–60) | Jede Entscheidungsfrage mit festen Optionen MUSS eine Auswahlfrage sein, keine Prosa-Fragen | REWRITE | S#Grundsätze | „Fragen nur bei offener Entscheidung – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen ist –, dann als Auswahlfrage“ | | ✅ sinngemäß |
| R003 | SKILL.md#VERBINDLICHE REGEL (Z. 60–61) | Auswahlfrage = Frage-Werkzeug der Umgebung mit anklickbaren Optionen | MERGE | S#Grundsätze | R002 („mit dem Frage-Werkzeug der Umgebung“) | | ✅ sinngemäß |
| R004 | SKILL.md#VERBINDLICHE REGEL (Z. 61) | Werkzeugnamen als Beispiele: Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion` | DROP | | Werkzeugnamen im Regeltext (skill-quality, Feste Begriffe und Neutralität); die Handlung bleibt in R002 | Gruppe A, freigegeben 28.09.2026 | ✅ |
| R005 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 63) | Die Situationen der Tabelle IMMER als Auswahlfrage | REWRITE | S#Grundsätze | „Typische Stellen“ – gelten, wenn die Entscheidung offen ist | | ✅ sinngemäß |
| R006 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 67) | Branch-Ermittlung, nur wenn die Shell ihn nicht liefert → Branch-Namen aus `git branch -a` | MERGE | S#Grundsätze | R021 (Optionen dort übernommen) | | ✅ sinngemäß |
| R007 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 68) | Token-Abgleich zeigt Abweichungen → Mockup anpassen, Tokens-Datei ändern (→ code-erstellen), begründet lassen | MOVE | S#Grundsätze | Tabellenzeile wörtlich, eingerückt unter „Typische Stellen“ | | ✅ |
| R008 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 69) | Pflichtansicht fehlt → Ansicht ergänzen, Ohne speichern (Begründung), Abbrechen | MOVE | S#Grundsätze | wie R007 | | ✅ |
| R009 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 70) | Abnahme → Abgenommen, Änderungen nötig, Später | MOVE | S#Grundsätze | wie R007 | | ✅ |
| R010 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 71) | Bestehendes Mockup: Archiv vs. Überschreiben → Archivieren (_ARCHIV suffix), Überschreiben, Abbrechen | MOVE | S#Grundsätze | wie R007 | | ✅ |
| R011 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 72) | NN-Nummer belegt → Nächste freie Nummer, Andere Nummer wählen, Abbrechen | MOVE | S#Grundsätze | wie R007 | | ✅ |
| R012 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 73) | Mehrere Stil-Referenzen möglich → Referenz-Dateinamen als Optionen | MOVE | S#Grundsätze | wie R007 | | ✅ |
| R013 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 74) | Fenster-Ordner existiert bereits → Variante hinzufügen, Bestehende ersetzen, Abbrechen | MOVE | S#Grundsätze | wie R007 | | ✅ |
| R014 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 75) | Eingehende Links unklar → vorhandene Fenster aus der Sitemap + „Keine eingehenden Links“ | MOVE | S#Grundsätze | wie R007 | | ✅ |
| R015 | SKILL.md#Prosa-Fragen NUR wenn (Z. 77–79) | Prosa nur bei offener Frage ohne feste Optionen (Beispiel: Daten/Felder des Screens) | MOVE | S#Grundsätze | Überschrift wird Einleitungszeile „Prosa-Fragen NUR wenn:“, Punkt wörtlich | | ✅ |
| R016 | SKILL.md#Prosa-Fragen NUR wenn (Z. 80) | Prosa, wenn der User eine Präferenz signalisiert hat | MOVE | S#Grundsätze | wörtlich | | ✅ |
| R017 | SKILL.md#Prosa-Fragen NUR wenn (Z. 81) | Prosa, wenn Freitext-Input nötig ist | MOVE | S#Grundsätze | wörtlich | | ✅ |
| R018 | SKILL.md#Branch-Ermittlung (Z. 87) | Branch aus dem Chat-Kontext verwenden | REWRITE | S#Grundsätze | gilt jetzt als Rückfall ohne Skill-Profil; mit Profil entscheidet die Branch-Policy (N001, N002) | | ✅ sinngemäß |
| R019 | SKILL.md#Branch-Ermittlung (Z. 87–88) | Mit Shell (Claude Code: Bash/PowerShell, Cowork: DC) `git branch --show-current` | REWRITE | S#Grundsätze | im Rückfall wörtlich; bei `current` Teil von N001 | | ✅ sinngemäß |
| R020 | SKILL.md#Branch-Ermittlung (Z. 88) | Pflicht-Branch aus dem Code-Profil beachten | REWRITE | S#Grundsätze | mit Skill-Profil über `fixed:<branch>` (N002); ohne Skill-Profil wörtlich wie bisher | | ✅ sinngemäß |
| R021 | SKILL.md#Branch-Ermittlung (Z. 88–89) | Ohne Shell und unbekannt: Auswahlfrage | REWRITE | S#Grundsätze | Rückfall ohne Skill-Profil; Optionen „Branch-Namen aus `git branch -a`“ aus R006 ergänzt | | ✅ sinngemäß |
| R022 | SKILL.md#Branch-Ermittlung (Z. 89) | NIE automatisch einen Branch annehmen | MOVE | S#Grundsätze | wörtlich, gilt mit und ohne Skill-Profil | | ✅ |
| R023 | SKILL.md#VERBOTEN (Z. 583) | Branch automatisch annehmen (Shell fragen oder Auswahlfrage) | REWRITE | S#VERBOTEN | Klammer um „Branch-Policy des Skill-Profils“ ergänzt | | ✅ sinngemäß |
| R024 | SKILL.md#VERBOTEN (Z. 584) | Archiv-vs-Überschreiben-Entscheidung als Prosa – IMMER Auswahlfrage | MERGE | S#VERBOTEN | R025 (als Beispiel in der Klammer); die Situation steht zusätzlich in den typischen Stellen (R010) | | ✅ sinngemäß |
| R025 | SKILL.md#VERBOTEN (Z. 590) | Prosa-Fragen bei festen Entscheidungsoptionen | REWRITE | S#VERBOTEN | Beispiel „(z.B. Archiv-vs-Überschreiben-Entscheidung)“ ergänzt, sonst wörtlich | | ✅ sinngemäß |
| N001 | – | Branch-Policy `current` → der aktuelle Branch aus der Shell (`git branch --show-current`) | NEW | S#Grundsätze | Phase 5 „Branch aus dem Profil“; `docs/skill-profile-v1.md` | | ✅ |
| N002 | – | Branch-Policy `fixed:<branch>` → der aktuelle Branch muss dieser sein, sonst Auswahlfrage (wechseln / abbrechen) | NEW | S#Grundsätze | Phase 5 „Branch aus dem Profil“; `docs/skill-profile-v1.md` | | ✅ |
| N003 | – | Skill-Profil vorhanden, aber keine Shell: bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage | NEW | SKILL.md#Grundsätze | Entscheidung Herbert 28.09.2026 (Sammelfreigabe Phase 5) | | ✅ |

## DROP-Gruppen

Von Herbert am 28.09.2026 freigegeben (Auswahlfrage vor dem Schreiben):

| Gruppe | IDs | Regelkern | Grund |
|---|---|---|---|
| A – Werkzeugnamen im Regeltext | R004 | „(Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion`)“ hinter der Definition der Auswahlfrage | skill-quality: „Auswahlfrage“ statt Werkzeugnamen im Regeltext; die Handlung „Auswahlfrage mit dem Frage-Werkzeug der Umgebung“ bleibt in R002 |

Der Entwurf `SKILL.md` setzt die Freigabe voraus. Wird Gruppe A nicht freigegeben, kommt die Klammer in S#Grundsätze
hinter „mit dem Frage-Werkzeug der Umgebung“ zurück, und R004 wird MOVE.

## Verweise von außen

Kein Skill, weder `INDEX.md` noch die Doku verweist auf die Abschnitte „🚨 VERBINDLICHE REGEL“ oder „Branch-Ermittlung“ von
mockup-erstellen (Suche nach `mockup-erstellen` in `skills/`, `docs/`, `INDEX.md`, `README.md`, `quality/`).

| Stelle | Verweis | Behandlung |
|---|---|---|
| `skills/code-erstellen/SKILL.md` (Mockup-Hook), Delegationstabellen in audit, doc-pflege, git-commit-helper, tracker; `skills/projekt-anlegen/SKILL.md`; `INDEX.md` | auf den Skill als Ganzes | nicht betroffen |
| `docs/skill-profile-v1.md`, Pflichtfelder je Skill | mockup-erstellen braucht Mockup.Ablage, Mockup.Designquelle, Mockup.Ansichten, Mockup.Abnahme-Ort und die Grundfelder (darunter Branch-Policy) | Branch-Policy liest der Skill jetzt; die Mockup-Felder liest er noch aus `## Mockup-Profil` (Phase 6) |

## Prüfung

- **Alt→Neu:** 25 IDs, jede mit Zustand – KEEP 1, MOVE 12, REWRITE 8, MERGE 3, DROP 1. Jede KEEP-, MOVE-, REWRITE- und
  MERGE-Zeile ist im Neu-Ort gefunden (S#Grundsätze Z. 57–81, S#VERBOTEN Z. 575 und 581).
- **Neu→Alt:** Die normativen Aussagen der geänderten Abschnitte im neuen Stand gehören alle zu einer ID oder zu N001/N002;
  keine ungewollt entstandene Regel. Push: weder im alten noch im neuen Stand eine Aussage.
- **Diff:** `git diff --no-index` gegen `skills/mockup-erstellen/SKILL.md` zeigt nur zwei Stellen – Fragenblock und
  Branch-Ermittlung (alt Z. 57–89 → neu Z. 57–81) sowie VERBOTEN (alt Z. 583–590 → neu Z. 575–581). Frontmatter
  (Z. 1–14) byte-gleich.
- **Zeilen:** 595 → 586.
- **Prüfskript:** nicht gelaufen (läuft vor dem Commit als Check skill-validation).
- **Routing-Eval:** keine eigene Messung nach v0.39.1 (Entscheidung Herbert: v0.39.1 ändert nur Regeltext nach dem Auslösen, die Description ist unverändert). Maßgeblich ist die Messung von v0.38.2 am 28.09.2026 auf 17ec20d (36 Fälle `audit`/`code-erstellen`/`doc-pflege`/`mockup-erstellen`, 100/108 Läufe, Einzelheiten in `docs/skill-refactors/2026-09-28-code-erstellen.md`, Abschnitt Prüfung); mitgetaggte Fälle liefen zusätzlich auf a0fb0a5 (`code-with-task-ref`, `doc-changelog` je 2/3, Sandbox-Muster).
