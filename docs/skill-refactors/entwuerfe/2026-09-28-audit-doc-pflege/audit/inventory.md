# Regel-Inventar – audit – 2026-09-28 (Grenze audit ↔ doc-pflege)

Refactor von audit in Umbau-Phase 5, Punkt „Grenzen audit ↔ doc-pflege ↔ modul-bauplan festziehen“
(`docs/skillsystem-umbau.md`). Freigegebenes Zielbild (Herbert, 28.09.2026): prüfen = audit, ändern = doc-pflege. audit
prüft zusätzlich im Skill-Repo die Skills gegen INDEX und Qualitätsregeln und übernimmt die Prüflisten aus doc-pflege
„Modus 6 — Validierung nach Profil“ als eigene Reference. Nach dem Refactor-Ablauf von skill-pflege
(`skills/skill-pflege/references/rule-inventory.md`); vorgesammelt mit
`tools/validate-skills.ps1 -Skill audit -RuleInventory …` (59 Kandidaten alt, 66 neu), danach nach Urteil zu Regeln
zusammengefasst.

- Skill: audit
- Stand vorher: 262ee9a (SKILL.md, 310 Zeilen; keine references)
- Quellen: `skills/audit/SKILL.md`; für die übernommenen Prüflisten `skills/doc-pflege/SKILL.md#Modus 6 — Validierung nach
  Profil` (Z. 316–353)
- Umfang: Description; Zweck; Vorrang / Delegation; Profile laden; Modul 6; neues Modul 7 (Skills im Skill-Repo); Nach dem
  Report; die VERBOTEN-Zeilen dazu; alle Verweise auf doc-pflege-Modusnummern. Dazu zwei Folgeänderungen, die das neue
  Modul bzw. die neue Fix-Skill-Option erzwingen: Tabellenzeile „Nach dem Report“ in den Grundsätzen (R020) und „Alle 6
  Module“ in Modus A (R026). Alle übrigen Abschnitte wörtlich unverändert (auch BPM/Heidi-Werte und Cowork-Teile, Phase 6).
- Entwurf (nicht im Repo): Scratchpad `p5b/audit/SKILL.md`, `p5b/audit/references/doku-validierung.md`

## Zielstruktur

Abkürzungen im Neu-Ort: `S` = `SKILL.md`, `R` = `references/doku-validierung.md`.

| Datei | Abschnitt alt | Abschnitt neu |
|---|---|---|
| `SKILL.md` | Frontmatter (Z. 3–11) | Frontmatter: neue Description (901 Zeichen) |
| `SKILL.md` | Zweck (Z. 16–23) | Zweck: Skill-Profil als Quelle, Rückfall auf Doku-/Code-Profil, Skill-Repo, eigene Prüflisten nur als Rückfall |
| `SKILL.md` | Vorrang / Delegation (Z. 27–49) | gleicher Abschnitt: doc-pflege auch für „Befunde beheben“, neue Zeile skill-pflege, Skill-Prüfung |
| `SKILL.md` | Grundsätze, Tabellenzeile „Nach dem Report“ (Z. 63) | Option um skill-pflege erweitert |
| `SKILL.md` | Profile laden (Z. 79–85) | Schritt 1 Skill-Profil (Pflichtfelder, fehlende Werte), Schritte 2–4 der bisherige Weg |
| `SKILL.md` | Modus A (Z. 103) | „Alle Module (Modul 7 nur im Skill-Repo)“ |
| `SKILL.md` | Modul 6 (Z. 204–226) | Modul 6: neutrale Frage, Vorrang `Doku.Validierungsregeln`, Verweis auf `R`; Kurzprüfungen nach `R` |
| `SKILL.md` | – | **Modul 7 — Skills (im Skill-Repo)** (neu, nach Modul 6) |
| `SKILL.md` | Nach dem Report (Z. 266–282) | Skill-Befunde → `tracker issue`, Fix-Skill-Option mit skill-pflege, doc-pflege über Überschrift |
| `SKILL.md` | VERBOTEN (Z. 299, 306, 307, 309, 310) | Z. 306 umformuliert, die übrigen unverändert |
| `references/doku-validierung.md` | – | neu (65 Zeilen, kein Inhaltsverzeichnis nötig): Kopf (Zweck, Vorrang), Heidi-Prüfliste, BPM-Prüfliste, Heidi-Kurzprüfung, BPM-Kurzprüfung |

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#Frontmatter (Z. 4–7) | Description, Was-Teil: prüft read-only Konsistenz Code ↔ Projektdoku nach Doku- und Code-Profil, mit BPM- und Heidi-Beispielen | REWRITE | S#Frontmatter | „nach dem Skill-Profil des Repos: Doku gegen Code, Doku-Validierung (z. B. Frontmatter, Quickload, Router, Statuslisten)“; Projektnamen entfallen (Vorgabe Auftrag) | | ✅ sinngemäß |
| R002 | SKILL.md#Frontmatter (Z. 7–9) | Use when: consistency audit, documentation-vs-code check, Frontmatter/Quickload validation, Bauplan check, systematic read-only review of project rules | REWRITE | S#Frontmatter | „Bauplan check“ (Projektbegriff) geht in „Doku gegen Code“ und „Statuslisten“ auf; übrige Fälle wörtlich; Eval-Risiko `audit-bauplan` (Prüfung) | | ✅ sinngemäß |
| R003 | SKILL.md#Frontmatter (Z. 9–10) | Do not trigger: code implementation | REWRITE | S#Frontmatter | „code implementation (code-erstellen)“ | | ✅ sinngemäß |
| R004 | SKILL.md#Frontmatter (Z. 10) | Do not trigger: build debugging | KEEP | S#Frontmatter | | | ✅ |
| R005 | SKILL.md#Frontmatter (Z. 10–11) | Do not trigger: general code review without doc/context comparison | REWRITE | S#Frontmatter | „general code review of a function or diff without doc comparison“ – „Diff“ nach Auftrag, „function“ ergänzt, weil `audit-no-trigger-code-review` eine einzelne Funktion zeigt | | ✅ sinngemäß |
| R006 | SKILL.md#Zweck (Z. 18) | Prüft, ob Code und Docs konsistent sind | REWRITE | S#Zweck | „Prüft read-only, ob Code, Projektdoku, Aufgaben im Tracker und – im Skill-Repo – die Skills zueinander passen“ | | ✅ sinngemäß |
| R007 | SKILL.md#Zweck (Z. 18–21) | Was geprüft wird, steht in den Profilen: Feld „Validierung“ des Doku-Profils, „Schichten / Kopplung“ und „Aufgabenquelle“ des Code-Profils, Stack-Referenzen von code-erstellen | REWRITE | S#Zweck | zuerst Skill-Profil (`Doku.Validierungsregeln`, `Doku.Router`, `Code.Architekturregeln`, `Code.Aufgabenquelle`); die alten Felder als Rückfall „in Repos ohne Skill-Profil“ wörtlich | | ✅ sinngemäß |
| R008 | SKILL.md#Zweck (Z. 21–22) | audit führt keine eigenen Prüfregeln; Read-only-Läufer über diese Regeln | REWRITE | S#Zweck | „erfindet keine Prüfregeln“; Ausnahme Rückfall-Prüflisten ist N005 | | ✅ sinngemäß |
| R009 | SKILL.md#Zweck (Z. 22–23) | Beispiele BPM (INDEX-Routing, Frontmatter, Quickload, Schema, DI) und Heidi (Bauplan, Vertrag, HANDOFF, PD-Register) | KEEP | S#Zweck | Projektbeispiele bleiben bis Phase 6; nur neu umbrochen | | ✅ |
| R010 | SKILL.md#Vorrang / Delegation (Z. 29–31) | audit ist strikt read-only; bei Fix, Implementierung oder Doc-Pflege delegieren | KEEP | S#Vorrang / Delegation | | | ✅ |
| R011 | SKILL.md#Vorrang / Delegation (Z. 35) | Code schreiben oder ändern → code-erstellen | KEEP | S#Vorrang / Delegation | | | ✅ |
| R012 | SKILL.md#Vorrang / Delegation (Z. 36) | Doku schreiben, ADR, Konzept, Frontmatter-Pflege → doc-pflege | REWRITE | S#Vorrang / Delegation | „Doku schreiben oder Befunde beheben, …“ (Zielbild: ändern = doc-pflege) | | ✅ sinngemäß |
| R013 | SKILL.md#Vorrang / Delegation (Z. 37) | UI-Entwurf als HTML-Mockup → mockup-erstellen | KEEP | S#Vorrang / Delegation | | | ✅ |
| R014 | SKILL.md#Vorrang / Delegation (Z. 38) | Commit-Befehl, Commit-Message → git-commit-helper | KEEP | S#Vorrang / Delegation | | | ✅ |
| R015 | SKILL.md#Vorrang / Delegation (Z. 39) | ClickUp-Task-Aktion → tracker | KEEP | S#Vorrang / Delegation | | | ✅ |
| R016 | SKILL.md#Vorrang / Delegation (Z. 41–43) | Nur bei Hauptabsicht read-only Konsistenzprüfung (Audit-Report, Frontmatter-Check, Code-vs-Doc-Abgleich, INDEX-Validierung) bleibt audit zuständig | REWRITE | S#Vorrang / Delegation | Aufzählung um „Skill-Prüfung im Skill-Repo“ ergänzt | | ✅ sinngemäß |
| R017 | SKILL.md#Vorrang / Delegation (Z. 45) | Nach einem Audit-Report bietet audit keine Fixes selbst an | KEEP | S#Vorrang / Delegation | | | ✅ |
| R018 | SKILL.md#Vorrang / Delegation (Z. 46–49) | Empfohlene Aktionen per Auswahlfrage an den passenden Skill (code-erstellen Code-Fixes, doc-pflege Doc-Fixes) oder als Aufgaben über tracker | REWRITE | S#Vorrang / Delegation | Klammer um „skill-pflege für Skill-Befunde“ ergänzt; Zeilenumbruch angepasst | | ✅ sinngemäß |
| R019 | SKILL.md#Vorrang / Delegation (Z. 49) | audit ist der Analyse-Skill, nicht der Fix-Skill | KEEP | S#Vorrang / Delegation | | | ✅ |
| R020 | SKILL.md#Grundsätze (Z. 63) | Nach dem Report: Optionen Als Tasks anlegen (tracker), An code-erstellen/doc-pflege, Nur Report | REWRITE | S#Grundsätze | Folgeänderung zu R048: „An code-erstellen/doc-pflege/skill-pflege“ | | ✅ sinngemäß |
| R021 | SKILL.md#Profile laden (Z. 79) | Profile laden ist Pflicht vor jedem Audit | KEEP | S#Profile laden | Überschrift unverändert | | ✅ |
| R022 | SKILL.md#Profile laden (Z. 81–82) | Aus der CLAUDE.md `## Doku-Profil` (Validierung, Pflicht-Docs, Router) und `## Code-Profil` (Schichten/Kopplung, Aufgabenquelle, Stacks, Tests) laden | REWRITE | S#Profile laden (2.) | jetzt Rückfall „Fehlt der Abschnitt:“ nach dem Skill-Profil (N007); Feldlisten wörtlich | | ✅ sinngemäß |
| R023 | SKILL.md#Profile laden (Z. 83) | Stack-Referenzen `skills/code-erstellen/references/stacks/<key>.md` je Schlüssel in `Stacks:` | REWRITE | S#Profile laden (3.) | „in `Code.Stacks` bzw. `Stacks:`“ | | ✅ sinngemäß |
| R024 | SKILL.md#Profile laden (Z. 84) | Fehlt das Doku-Profil: `INDEX.md` + `DOC-STANDARD.md` (BPM-Weg) | MOVE | S#Profile laden (4.) | „Fehlt auch das Doku-Profil“ | | ✅ |
| R025 | SKILL.md#Profile laden (Z. 84–85) | Fehlt beides: Auswahlfrage „Profil anlegen (doc-pflege Modus 0)“ / „Ohne Profil, ich nenne die Docs“ – nie raten | REWRITE | S#Profile laden (4.) | Verweis über Überschrift: „doc-pflege, Projekt-Init“ | | ✅ sinngemäß |
| R026 | SKILL.md#Modus A — Vollaudit (Z. 103) | Vollaudit = alle 6 Module | REWRITE | S#Modus A — Vollaudit | Folgeänderung zu N012: „Alle Module (Modul 7 nur im Skill-Repo)“ | | ✅ sinngemäß |
| R027 | SKILL.md#Modul 6 (Z. 206–207) | Detaillierte Prüfregeln in doc-pflege Modus 6 (BPM Stufe A/B, Heidi-Prüfliste) | REWRITE | S#Modul 6 | Verweis auf `references/doku-validierung.md` („je Projekt Stufe A (Blocker) und Stufe B (Warnung) sowie die Kurzprüfung“); Listen dort N020–N044 | | ✅ sinngemäß |
| R028 | SKILL.md#Modul 6 (Z. 209) | Heidi-Kurzprüfung: Karten mit allen Feldern (Voraussetzung, Ziel, Nicht ändern, Akzeptanz) | MOVE | R#Heidi-Kurzprüfung | wörtlich; Label wird Überschrift | | ✅ |
| R029 | SKILL.md#Modul 6 (Z. 210) | Heidi-Kurzprüfung: Statusliste ohne Lücken | MOVE | R#Heidi-Kurzprüfung | wörtlich | | ✅ |
| R030 | SKILL.md#Modul 6 (Z. 210) | Heidi-Kurzprüfung: keine Notiz ohne Datum/Art/Schwere | MOVE | R#Heidi-Kurzprüfung | wörtlich | | ✅ |
| R031 | SKILL.md#Modul 6 (Z. 210) | Heidi-Kurzprüfung: PD-Tabelle vollständig gefüllt | MOVE | R#Heidi-Kurzprüfung | wörtlich | | ✅ |
| R032 | SKILL.md#6a. Frontmatter-Vollständigkeit (Z. 215) | Frontmatter vorhanden? | MOVE | R#6a. Frontmatter-Vollständigkeit | wörtlich, Überschrift eine Ebene höher | | ✅ |
| R033 | SKILL.md#6a. Frontmatter-Vollständigkeit (Z. 215) | Pflichtfelder? | MOVE | R#6a. Frontmatter-Vollständigkeit | wörtlich | | ✅ |
| R034 | SKILL.md#6a. Frontmatter-Vollständigkeit (Z. 215) | doc_id eindeutig? | MOVE | R#6a. Frontmatter-Vollständigkeit | wörtlich | | ✅ |
| R035 | SKILL.md#6b. Quickload-Vollständigkeit (Z. 218) | Quickload vorhanden bei source_of_truth/secondary? | MOVE | R#6b. Quickload-Vollständigkeit | wörtlich | | ✅ |
| R036 | SKILL.md#6b. Quickload-Vollständigkeit (Z. 219) | Kapitel-Feld stimmt mit H2s? | MOVE | R#6b. Quickload-Vollständigkeit | wörtlich | | ✅ |
| R037 | SKILL.md#6c. Cross-Checks (Z. 222) | INDEX referenziert nur Docs mit gültigem Frontmatter? | MOVE | R#6c. Cross-Checks | wörtlich | | ✅ |
| R038 | SKILL.md#6c. Cross-Checks (Z. 223) | source_of_truth hat Quickload? | MOVE | R#6c. Cross-Checks | wörtlich | | ✅ |
| R039 | SKILL.md#6c. Cross-Checks (Z. 224) | historical NICHT als Primary im Router? | MOVE | R#6c. Cross-Checks | wörtlich | | ✅ |
| R040 | SKILL.md#6c. Cross-Checks (Z. 225) | Keine doppelten doc_ids? | MOVE | R#6c. Cross-Checks | wörtlich | | ✅ |
| R041 | SKILL.md#6c. Cross-Checks (Z. 226) | Fachliche Invarianten nicht widersprüchlich zwischen Docs? | MOVE | R#6c. Cross-Checks | wörtlich | | ✅ |
| R042 | SKILL.md#Nach dem Report (Z. 268–269) | audit ändert nichts, lässt Befunde aber nicht im Chat liegen: direkt nach dem Report eine Auswahlfrage | KEEP | S#Nach dem Report | | | ✅ |
| R043 | SKILL.md#Nach dem Report (Z. 271) | „Als Tasks anlegen“ → `tracker neu` mit Schema und Präfix des Projekts | KEEP | S#Nach dem Report | | | ✅ |
| R044 | SKILL.md#Nach dem Report (Z. 272) | Ein Sammel-Task pro Modul, Befunde als Checkliste in der Beschreibung | KEEP | S#Nach dem Report | Ausnahme Skill-Befunde ist N018 | | ✅ |
| R045 | SKILL.md#Nach dem Report (Z. 272–273) | ❌-Befunde Priorität `high`, ⚠️ `normal` | KEEP | S#Nach dem Report | | | ✅ |
| R046 | SKILL.md#Nach dem Report (Z. 273) | Bei ≤ 3 Befunden auch je Befund ein Task (Auswahlfrage) | KEEP | S#Nach dem Report | | | ✅ |
| R047 | SKILL.md#Nach dem Report (Z. 274) | Alle ClickUp-Operationen über den tracker-Skill, nie direkt | KEEP | S#Nach dem Report | | | ✅ |
| R048 | SKILL.md#Nach dem Report (Z. 275–276) | „An code-erstellen / doc-pflege“ → Befunde als Aufgabenliste an den Fix-Skill (Code → code-erstellen, Doc → doc-pflege Modus 5/6) | REWRITE | S#Nach dem Report | Option „An code-erstellen / doc-pflege / skill-pflege“; „doc-pflege, Abschnitt „Doku pflegen““ statt Modusnummern; Skill-Befunde N019 | | ✅ sinngemäß |
| R049 | SKILL.md#Nach dem Report (Z. 276–277) | Der Fix-Skill startet erst nach eigener Bestätigung | KEEP | S#Nach dem Report | Zeilenumbruch angepasst | | ✅ |
| R050 | SKILL.md#Nach dem Report (Z. 278) | „Nur Report“ → Report bleibt; Hinweis, dass Befunde ohne Task wieder auftauchen | KEEP | S#Nach dem Report | | | ✅ |
| R051 | SKILL.md#Nach dem Report (Z. 280–282) | Heidi: Befunde mit Entscheidungsbedarf als Notiz-Vorschlag für Bauplan Abschnitt 10; eintragen tut doc-pflege | KEEP | S#Nach dem Report | Projektwert bleibt bis Phase 6 | | ✅ |
| R052 | SKILL.md#VERBOTEN (Z. 299) | Dateien ändern (read-only) | KEEP | S#VERBOTEN | gilt auch für den JSON-Bericht in Modul 7 (N014) | | ✅ |
| R053 | SKILL.md#VERBOTEN (Z. 306) | Eigene Prüfregeln erfinden statt Doku-/Code-Profil und Stack-Referenzen zu lesen | REWRITE | S#VERBOTEN | „statt Skill-Profil (bzw. Doku-/Code-Profil), Stack-Referenzen und `references/doku-validierung.md` zu lesen“ | | ✅ sinngemäß |
| R054 | SKILL.md#VERBOTEN (Z. 307) | BPM-Prüfpunkte (DB-Schema, DI, Frontmatter) nicht auf ein Projekt anwenden, das sie laut Profil nicht hat | KEEP | S#VERBOTEN | gilt jetzt auch für die Listen in `R` | | ✅ |
| R055 | SKILL.md#VERBOTEN (Z. 309) | Report nicht ohne Auswahlfrage „Tasks / Fix-Skill / Nur Report“ beenden | KEEP | S#VERBOTEN | | | ✅ |
| R056 | SKILL.md#VERBOTEN (Z. 310) | ClickUp nicht direkt schreiben (nur über tracker, nur nach Auswahlfrage) | KEEP | S#VERBOTEN | gilt auch für `tracker issue` (N018) | | ✅ |
| N001 | – | Description, Was-Teil: Aufgaben im Tracker gegen die Aufgabenquelle, im Skill-Repo die Skills gegen INDEX und Qualitätsregeln; Befunde mit Datei und Stelle an Fix-Skill oder tracker; ändert selbst nichts | NEW | S#Frontmatter | Zielbild Herbert; Wortlaut nach Auftrag | | ✅ |
| N002 | – | Use when: prüfen, checken, auditieren, validieren ohne Änderung; Prüfung, ob INDEX und Skill-Descriptions zusammenpassen | NEW | S#Frontmatter | Ziel-Eval-Fall `audit-readonly` | | ✅ |
| N003 | – | Do not trigger: Doku schreiben oder Befunde beheben (doc-pflege) | NEW | S#Frontmatter | Zielbild „ändern = doc-pflege“; Fälle `audit-findings-fix`, `doc-fix-links`, `doc-write` | | ✅ |
| N004 | – | Im Skill-Repo kommen `docs/skill-quality.md` und die Skill-Tabelle der `INDEX.md` als Prüfgrundlage dazu (Modul 7) | NEW | S#Zweck | | | ✅ |
| N005 | – | Eigene Prüflisten nur für die Doku-Validierung, solange ein Projekt sie nicht im Skill-Profil führt (`references/doku-validierung.md`) | NEW | S#Zweck | Ausnahme zu R008 | | ✅ |
| N006 | – | Skill ändern (auch Skill-Befunde beheben) → skill-pflege | NEW | S#Vorrang / Delegation | Auftrag | | ✅ |
| N007 | – | Zuerst `## Skill-Profil` lesen (Spezifikation `docs/skill-profile-v1.md`); Pflichtfelder für audit: Grundfelder, `Doku.Router`, `Doku.Validierungsregeln`; `Code.Architekturregeln`, wenn Code geprüft wird; `Tracker.Config`, wenn der Tracker geprüft wird | NEW | S#Profile laden (1.) | `docs/skill-profile-v1.md#Pflichtfelder je Skill` | | ✅ |
| N008 | – | Dazu, was die Module brauchen: `Code.Stacks`, `Code.Aufgabenquelle`, `Doku.Pflichtdokumente`, im Skill-Repo der Check `skill-validation` | NEW | S#Profile laden (1.) | Gegenstück zu den Feldern der Rückfall-Profile (R022) | | ✅ |
| N009 | – | Fehlt ein Pflichtfeld oder steht es auf `fehlt`: genau dieses Feld melden, fragen nach „Fehlende Werte“; das Profil ergänzt nicht audit, sondern doc-pflege (Projekt-Init) oder der Nutzer | NEW | S#Profile laden (1.) | `docs/skill-profile-v1.md#Fehlende Werte`; read-only wie R010 | | ✅ |
| N010 | – | Modul 6, neutrale Frage: Halten die Docs die Validierungsregeln des Projekts ein? | NEW | S#Modul 6 | Muster der übrigen Module (Ablauf, Schritt 2) | | ✅ |
| N011 | – | Vorrang hat `Doku.Validierungsregeln` des Skill-Profils (ohne Skill-Profil: Feld „Validierung“ des Doku-Profils); die Listen der Reference gelten, solange ein Projekt dort keine führt | NEW | S#Modul 6; R#Kopf | Auftrag | | ✅ |
| N012 | – | Modul 7 nur im Skill-Repo (Repo mit `skills/<name>/SKILL.md` und `docs/skill-quality.md`), sonst entfällt es | NEW | S#Modul 7 | Erkennung wie `skills/skill-pflege/SKILL.md#Zweck` | | ✅ |
| N013 | – | Modul 7, neutrale Frage: Passen die Skills zu INDEX und Qualitätsregeln? | NEW | S#Modul 7 | | | ✅ |
| N014 | – | Mechanik: Check `skill-validation` des Skill-Profils mit JSON-Bericht in eine Datei außerhalb des Repos; Fehler → ❌, Warnungen → ⚠️ | NEW | S#Modul 7 | `docs/skill-quality.md#Mechanisch`; „außerhalb des Repos“ wegen R052 | | ✅ |
| N015 | – | Urteil nach `docs/skill-quality.md`, Abschnitt „Urteil – audit“: Description zu breit/eng, Kollisionen, Neutralität, Doppelungen, Schnitt Kern/References, Eval-Fälle realistisch | NEW | S#Modul 7 | Verweis statt Kopie (Querschnittsregeln nicht kopieren) | | ✅ |
| N016 | – | INDEX ↔ Descriptions: jeder Ordner unter `skills/` hat eine Zeile der Skill-Tabelle und umgekehrt; Zuständigkeit und Auslöser decken sich mit der Description | NEW | S#Modul 7 | Ziel-Eval-Fall `audit-readonly` | | ✅ |
| N017 | – | Skill-Befunde → skill-pflege bzw. `tracker issue <skill>` | NEW | S#Modul 7 | Auftrag | | ✅ |
| N018 | – | Nach dem Report, „Als Tasks anlegen“: Skill-Befunde als `tracker issue <skill>: Audit: …`, je Skill ein Issue mit den Befunden als Checkliste | NEW | S#Nach dem Report | Routing der Skill-Issues je Skill-Liste (`.claude/skill-config/tracker.md`); Gegenstück zu R044 | | ✅ |
| N019 | – | Nach dem Report, Fix-Skill: Skill-Befunde → skill-pflege | NEW | S#Nach dem Report | Auftrag | | ✅ |
| N020 | – | Heidi Stufe A: Statusliste (Bauplan Abschnitt 1) ↔ ClickUp-Status ↔ Code; fertig nur mit Code, Tests und Commit | NEW | R#Heidi-Prüfliste | wörtlich aus `skills/doc-pflege/SKILL.md#Modus 6 — Validierung nach Profil` (Z. 319); dort MOVE im doc-pflege-Inventar | | ✅ |
| N021 | – | Heidi Stufe A: jede Abweichung von v1 hat einen PD-Eintrag in 10a mit Status `freigegeben` | NEW | R#Heidi-Prüfliste | wie N020 (Z. 320) | | ✅ |
| N022 | – | Heidi Stufe A: Abschnitt 4 (Entitäts-Vertrag) ↔ `contract.ts`: gleiche Entitäten, gleiche Dienste | NEW | R#Heidi-Prüfliste | wie N020 (Z. 321) | | ✅ |
| N023 | – | Heidi Stufe A: HANDOFF 3e nennt letzten Bauschritt und aktuelle Version | NEW | R#Heidi-Prüfliste | wie N020 (Z. 322) | | ✅ |
| N024 | – | Heidi Stufe A: nichts Verbotenes im Repo (Token, GPS, `.storage`, Datenbanken, Laufprotokolle) | NEW | R#Heidi-Prüfliste | wie N020 (Z. 323) | | ✅ |
| N025 | – | Heidi Stufe B: Notiz in Abschnitt 10 ohne Datum, Aufgabe, Art oder Schwere; Entscheidung Herbert fehlt | NEW | R#Heidi-Prüfliste | wie N020 (Z. 326) | | ✅ |
| N026 | – | Heidi Stufe B: Aufgabenkarte ohne Akzeptanz oder ohne Tests | NEW | R#Heidi-Prüfliste | wie N020 (Z. 327) | | ✅ |
| N027 | – | Heidi Stufe B: offene Punkte (HANDOFF 4) ohne Gegenstück in ClickUp | NEW | R#Heidi-Prüfliste | wie N020 (Z. 328) | | ✅ |
| N028 | – | Heidi Stufe B: Plan-Doc ohne Stand-Datum | NEW | R#Heidi-Prüfliste | wie N020 (Z. 329) | | ✅ |
| N029 | – | Heidi Stufe B: Version in package.json, Lock und Ressourcen-`?v=` uneinheitlich | NEW | R#Heidi-Prüfliste | wie N020 (Z. 330) | | ✅ |
| N030 | – | BPM Stufe A: Frontmatter vorhanden bei Kern/, Module/, Referenz/ | NEW | R#Stufe A — Formal (Blocker) | wie N020 (Z. 336); Überschrift zwei Ebenen höher | | ✅ |
| N031 | – | BPM Stufe A: alle Pflichtfelder | NEW | R#Stufe A — Formal (Blocker) | wie N020 (Z. 337) | | ✅ |
| N032 | – | BPM Stufe A: doc_id eindeutig | NEW | R#Stufe A — Formal (Blocker) | wie N020 (Z. 338) | | ✅ |
| N033 | – | BPM Stufe A: Enums korrekt | NEW | R#Stufe A — Formal (Blocker) | wie N020 (Z. 339) | | ✅ |
| N034 | – | BPM Stufe A: Quickload bei source_of_truth/secondary | NEW | R#Stufe A — Formal (Blocker) | wie N020 (Z. 340) | | ✅ |
| N035 | – | BPM Stufe A: Quickload-Kapitel-Feld stimmt mit H2s | NEW | R#Stufe A — Formal (Blocker) | wie N020 (Z. 341) | | ✅ |
| N036 | – | BPM Stufe A: Kapitelreihenfolge nach Vorlage | NEW | R#Stufe A — Formal (Blocker) | wie N020 (Z. 342) | | ✅ |
| N037 | – | BPM Stufe A: Pflichtlesen verweist auf existierende Kapitel | NEW | R#Stufe A — Formal (Blocker) | wie N020 (Z. 343) | | ✅ |
| N038 | – | BPM Stufe A: Fachliche Invarianten höchstens 5 | NEW | R#Stufe A — Formal (Blocker) | wie N020 (Z. 344) | | ✅ |
| N039 | – | BPM Stufe B: Quickload-Kapitel stimmt nicht mit H2s | NEW | R#Stufe B — Semantisch (Warnung) | wie N020 (Z. 348) | | ✅ |
| N040 | – | BPM Stufe B: historical als Primary im Router | NEW | R#Stufe B — Semantisch (Warnung) | wie N020 (Z. 349) | | ✅ |
| N041 | – | BPM Stufe B: related_docs nicht existent | NEW | R#Stufe B — Semantisch (Warnung) | wie N020 (Z. 350) | | ✅ |
| N042 | – | BPM Stufe B: Kapitelvorlage nicht eingehalten | NEW | R#Stufe B — Semantisch (Warnung) | wie N020 (Z. 351) | | ✅ |
| N043 | – | BPM Stufe B: Fachliche Invarianten leer bei großem Modul | NEW | R#Stufe B — Semantisch (Warnung) | wie N020 (Z. 352) | | ✅ |
| N044 | – | BPM Stufe B: Pflichtlesen leer bei source_of_truth-Modul | NEW | R#Stufe B — Semantisch (Warnung) | wie N020 (Z. 353) | | ✅ |

Nicht im Inventar, weil außerhalb des Umfangs und wörtlich unverändert: Grundsätze (bis auf R020), Arbeitsverzeichnis,
Doc-Laderegel, Modus B, Ablauf, Module 1–5, Report-Format, Ampel, Tool-Strategie, VERBOTEN Z. 300–305 und 308. Nicht
übernommen aus doc-pflege Modus 6 wurde der einleitende Absatz (Prüfliste aus dem Feld „Validierung“; Befunde als Tabelle
Doc/Stelle/Befund/Vorschlag; bei mehreren Lösungen Auswahlfrage; nichts stillschweigend korrigieren): Die Quelle deckt
N011 ab, das Befundformat regelt audit im Report-Format, Korrekturen macht audit nicht (R010). Er bleibt Sache des
doc-pflege-Inventars.

## DROP-Gruppen

Keine.

MERGE-Kandidaten, bewusst nicht zusammengeführt (Auftrag: Listen wörtlich übernehmen), zur Entscheidung durch Herbert:
Die BPM-Kurzprüfung doppelt Teile der BPM-Prüfliste – R033/R034 ↔ N031/N032, R035/R038 ↔ N034, R036 ↔ N035/N039,
R039 ↔ N040, R040 ↔ N032. Die Heidi-Kurzprüfung doppelt R030 ↔ N025.

## Verweise von außen

| Stelle | Verweis | Behandlung |
|---|---|---|
| `skills/doc-pflege/SKILL.md#Modus 6 — Validierung nach Profil` (Z. 308–353) | Prüflisten Heidi und BPM | im selben Umbau: doc-pflege gibt sie ab (MOVE nach `skills/audit/references/doku-validierung.md`); Wortlaut in beiden Inventaren gleich halten |
| `skills/doc-pflege/SKILL.md#Vorrang / Delegation` (Z. 43) | „Konsistenzprüfung Code ↔ Docs (read-only) → audit“ | passt; Erweiterung um Doku-Validierung Sache des doc-pflege-Inventars |
| `INDEX.md`, Skill-Tabelle (Z. 19, 24) | audit „Konsistenz zwischen Code und Doku prüfen …“; doc-pflege „anlegen, pflegen, validieren“ | Doku-Check des Profils (Zuständigkeit geändert): im Commit dieses Umbaus nachziehen – audit auch Doku-Validierung und Skill-Prüfung, doc-pflege ohne „validieren“ |
| `INDEX.md`, Konfliktpaare (Z. 48–61) | kein Paar audit ↔ doc-pflege, audit ↔ skill-pflege | Vorschlag: „prüfen → audit; ändern oder Befunde beheben → doc-pflege“ und „Skills prüfen → audit; Skill ändern → skill-pflege“ |
| `skills/code-erstellen/SKILL.md` (Z. 45), `skills/tracker/SKILL.md` (Z. 272), `skills/git-commit-helper/SKILL.md` (Z. 29), `skills/projekt-anlegen/SKILL.md` (Z. 32) | Delegation an audit (Konsistenzprüfung / Prüfen) | passt, keine Änderung nötig |
| `docs/skill-quality.md#Urteil – audit`, Einleitung Z. 4 | „was ein Urteil braucht, prüft audit“ | passt; Modul 7 verweist darauf |
| `docs/skill-profile-v1.md#Prüfung` | audit prüft in jedem Repo das ganze Profil (Version, Vollständigkeit, `ref:`-Ziele, Widersprüche, unbekannte Felder) | audit hat dafür noch keinen Prüfpunkt (nur Heidi-Punkt in Modul 1) – offene Frage |
| `docs/skill-refactors/2026-09-28-doc-pflege.md` (Z. 79) | audit Z. 93/214 „doc-pflege Modus 0/6“ für Phase 6 vorgemerkt | mit diesem Umbau erledigt |
| `quality/evals/audit-readonly/prompt.md` | Beschreibung „Bis Phase 5 erwarteter Fehlfall …“ | nach der Routing-Eval anpassen |
| `docs/skillsystem-umbau.md` (Z. 176) | Punkt „Grenzen audit ↔ doc-pflege ↔ modul-bauplan festziehen“ | nach Commit und Eval abhaken |

## Prüfung

- **Freigabe:** Umfang, Description-Text und Zielstruktur aus dem freigegebenen Zielbild (Herbert, 28.09.2026) und dem
  Auftrag; keine DROP-Zeile.
- **Alt→Neu:** 56 alte IDs mit Zustand (KEEP 23, MOVE 15, REWRITE 18, MERGE 0, DROP 0) und N001–N044; jeder Neu-Ort im
  Entwurf gelesen.
- **Neu→Alt:** Kandidaten des Entwurfs mit `tools/validate-skills.ps1 -RuleInventory` in eine Scratchpad-Datei erzeugt
  (66 Kandidaten aus SKILL.md und Reference); jeder Kandidat eines geänderten Abschnitts gehört zu einer R-ID oder zu
  N001–N044, die übrigen liegen in unveränderten Abschnitten. Von Hand ergänzt: Aussagen ohne Pflichtwort in Zweck,
  Modul 6, Modul 7 und Nach dem Report – alle zugeordnet; keine ungewollt entstandene Regel.
- **Diff:** `git diff --no-index` zwischen `skills/audit/SKILL.md` und Entwurf zeigt nur die Abschnitte des Umfangs plus
  R020 und R026; die Reference ist neu.
- **Zeilen:** SKILL.md 310 → 337; neu `references/doku-validierung.md` 65 Zeilen (unter 100, kein Inhaltsverzeichnis).
- **Description:** 526 → 901 Zeichen (Zeilen getrimmt, mit Leerzeichen verbunden), keine spitzen Klammern, keine
  Projektnamen.
- **Prüfskript:** auf einem Spiegel der versionierten Dateien im Scratchpad mit dem Entwurf (`-Root … -Skill audit`):
  0 Fehler; Warnungen des Skills 4 → 3 (entfallen: „description nennt ein Projekt“, „3 Querverweise über Nummern“;
  bleibt: Windows-Pfad Z. 167 in Modul 2b; Projektbegriffe 35 → 29 Zeilen in SKILL.md, neu 7 Zeilen in der Reference).
- **Routing-Eval:** wird nach dem Commit eingetragen. Betroffen: alle Fälle mit Tag `audit` und `doc-pflege`, zusammen
  mit der neuen Description von doc-pflege; besonders `audit-readonly` (Ziel-Fall), `audit-bauplan` („Bauplan check“
  steht nicht mehr in der Description), `audit-no-trigger-code-review`, `audit-findings-fix`, `doc-fix-links`,
  `doc-write`.
