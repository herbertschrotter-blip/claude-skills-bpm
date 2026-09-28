# Regel-Inventar – doc-pflege – 2026-09-28 (Grenze audit ↔ doc-pflege)

Refactor von doc-pflege in Umbau-Phase 5, Punkt „Grenzen audit ↔ doc-pflege ↔ modul-bauplan festziehen (doc-pflege
Modus 3, 4 und 6 als öffentliche Modi entfernen)“ und „Descriptions anpassen“ (`docs/skillsystem-umbau.md`). Zielbild von
Herbert freigegeben (28.09.2026): **prüfen = audit, ändern = doc-pflege**; doc-pflege-Modi bekommen Namen statt Nummern.
Nach dem Refactor-Ablauf von skill-pflege (`skills/skill-pflege/references/rule-inventory.md`); Muster: Inventar
`2026-09-28-git-commit-helper.md`. Kandidaten vorgesammelt mit `tools/validate-skills.ps1 -Skill doc-pflege
-RuleInventory` (63 Kandidaten, Ausgabe nur im Scratchpad), danach nach Urteil zu Regeln zusammengefasst und ergänzt.

Gehört als Datei zu `docs/skill-refactors/`; der Name `2026-09-28-doc-pflege.md` ist schon vergeben (Refactor
„Grundsätze“, 8a24710) – Vorschlag: `docs/skill-refactors/2026-09-28-doc-pflege-2.md` (wie bei code-erstellen).

- Skill: doc-pflege
- Stand vorher: 262ee9a (SKILL.md zuletzt geändert in 8a24710; 463 Zeilen; keine references)
- Quellen: SKILL.md
- Umfang: Frontmatter (Description) · Zweck · Vorrang / Delegation · die Stellen, die auf Modusnummern verweisen
  (Grundsätze: vier Zeilen der Auswahlfrage-Tabelle und die Push-Zeile; Voraussetzung: Doku-Profil: zwei Tabellenzeilen) ·
  Abschnitt „Advisory-Checkliste nach code-relevanten Änderungen“ · Abschnitt „8 Modi“ vollständig · Skill-Governance
  Punkt 5 · drei VERBOTEN-Zeilen (Modus 4 zweimal, Modus 8). Neu: Abschnitt „Prüfen nach dem Schreiben“.
  Alle übrigen Abschnitte bleiben wörtlich (auch Projektwerte BPM/Heidi, Cowork-Teile, „Doku-Profil“/„Commit-Profil“ –
  Phase 6). Die übrigen Regeln der geänderten Abschnitte „Grundsätze“, „Voraussetzung: Doku-Profil“ und „VERBOTEN“ sind
  unverändert und hier nicht aufgeführt (siehe Inventar `2026-09-28-doc-pflege.md`).

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `skills/doc-pflege/SKILL.md` | Frontmatter (**neue Description**) · **Zweck** · **Vorrang / Delegation** · Grundsätze (Auswahlfrage-Tabelle, Push: Modusnamen) · Arbeitsverzeichnis · Voraussetzung: Doku-Profil (zwei Zeilen) · Konkrete Pfade · Doc-Laderegel · Frühphasen-Regel · **Doku-Hinweise nach Code-Änderungen** (statt „Advisory-Checkliste …“, nimmt Modus 3 und 4 auf) · **Modi**: Projekt-Init, Router nachziehen, Begleit-Docs, Doku pflegen, Neue Doc oder Umbau (Neue Doc, Doc umbauen), Sitzungsabschluss · **Prüfen nach dem Schreiben** (neu) · Ausgabeformat · Skill-Governance (Punkt 5) · VERBOTEN (drei Zeilen) |
| `skills/audit/references/doku-validierung.md` | legt der audit-Entwurf an (nicht Teil dieses Entwurfs): nimmt die Prüflisten aus Modus 6 auf (R091–R115) |

Modusnamen nach Auftrag:

| alt | neu |
|---|---|
| Modus 0 — Projekt-Init (Standard-Doc-Set) | `### Projekt-Init` |
| Modus 1 — Index Sync | `### Router nachziehen` |
| Modus 2 — Companion Docs Check | `### Begleit-Docs` |
| Modus 3 — Passive Advisory, Modus 4 — Automatischer Checkpoint | kein Modus: `## Doku-Hinweise nach Code-Änderungen` |
| Modus 5 — Explicit Doc Maintenance | `### Doku pflegen` |
| Modus 6 — Validierung nach Profil | kein Auftrag mehr: Prüflisten → audit (`AV`); doc-pflege: `## Prüfen nach dem Schreiben` |
| Modus 7 — Neue Doc erstellen oder Refactoring (7a, 7b) | `### Neue Doc oder Umbau` mit `#### Neue Doc`, `#### Doc umbauen` |
| Modus 8 — Sitzungsabschluss | `### Sitzungsabschluss` |

Abkürzungen im Neu-Ort: `S` = `skills/doc-pflege/SKILL.md` · `A` = `skills/audit/SKILL.md` (audit-Entwurf dieser Phase) ·
`AV` = `skills/audit/references/doku-validierung.md` (legt der audit-Entwurf an).

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#Frontmatter (Z. 4–6) | Was: erstellt, aktualisiert und validiert Projektdoku nach dem Doku-Profil (BPM: DOC-STANDARD, Frontmatter, Quickload, INDEX.md; Heidi: Bauplan, Statusliste, PD-Register, HANDOFF) – projektneutral | REWRITE | S#Frontmatter | „Schreibt, ändert und korrigiert Projektdokumentation nach dem Skill-Profil des Repos …“; Projektnamen raus (Harte Grenze), neutral: Frontmatter, Quickload, Router-Einträge, Statuslisten, Übergabe-Dokumente; „validiert“ → R003 | | ✅ sinngemäß |
| R002 | SKILL.md#Frontmatter (Z. 7–9) | Use when: schreiben, erstellen, pflegen, aktualisieren, draften, anlegen, formulieren, dokumentieren, ergänzen, refactoren documentation | REWRITE | S#Frontmatter | alle zehn Wörter wörtlich; Liste um „korrigieren, umbauen“ ergänzt (N001) | | ✅ sinngemäß |
| R003 | SKILL.md#Frontmatter (Z. 9) | Auslöser „validieren documentation“ | MOVE | A#Frontmatter | Zielbild prüfen = audit; in S nur noch als Negativgrenze (N002) | | offen (audit-Entwurf) |
| R004 | SKILL.md#Frontmatter (Z. 9–12) | including ADRs, Konzept-, Architektur-, Modul-Docs, README, CHANGELOG, BACKLOG, Frontmatter, Quickload, Kapitelvorlagen, INDEX.md-Routing, Bauplan-Statuslisten, Handoff-Dokumente, Sitzungsabschluss | REWRITE | S#Frontmatter | im Was-Teil: „neue Docs nach der Vorlage des Projekts (z. B. ADR, Konzept, Modul-Doc, Architektur, README, CHANGELOG, BACKLOG)“, „Frontmatter, Quickload, Router-Einträge, Statuslisten und Übergabe-Dokumente“; Kapitelvorlagen → „Vorlage des Projekts“; „Sitzungsabschluss“ bleibt | | ✅ sinngemäß |
| R005 | SKILL.md#Frontmatter (Z. 12–13) | Triggers also on bug fixes in documentation (typos, broken links, outdated chapters) and structural refactoring of existing docs | REWRITE | S#Frontmatter | „including bug fixes in docs (typos, broken links, outdated chapters) … structural refactoring of existing docs“; im Was-Teil „behebt kaputte Links, veraltete Kapitel“ | | ✅ sinngemäß |
| R006 | SKILL.md#Frontmatter (Z. 13) | Do not trigger for code implementation | KEEP | S#Frontmatter | wörtlich im neuen „Do not trigger“-Satz | | ✅ |
| R007 | SKILL.md#Frontmatter (Z. 14) | Do not trigger for automatic post-change advisory checks | REWRITE | S#Frontmatter | „automatic post-change doc hints after code changes“ (Begriff Doku-Hinweise) | | ✅ sinngemäß |
| R008 | SKILL.md#Frontmatter (Z. 14–15) | Do not trigger for generic project discussion without explicit doc intent | REWRITE | S#Frontmatter | „… without an explicit doc request“ (Auftrag: „ohne ausdrücklichen Doku-Auftrag“) | | ✅ sinngemäß |
| R009 | SKILL.md#Zweck (Z. 22) | Stellt Konsistenz der Projektdokumentation sicher | REWRITE | S#Zweck | „Schreibt, ändert und korrigiert Projektdokumentation, behebt Befunde aus einem Audit und macht den Sitzungsabschluss im Repo“; Abgrenzung N003 | | ✅ sinngemäß |
| R010 | SKILL.md#Zweck (Z. 22–24) | Welche Docs es gibt, Aufbau und was geprüft wird, steht im Doku-Profil | KEEP | S#Zweck | | | ✅ |
| R011 | SKILL.md#Zweck (Z. 24–26) | BPM: Frontmatter, Quickload, Kapitelstruktur nach DOC-STANDARD; Heidi: Bauplan und HANDOFF | KEEP | S#Zweck | Projektwerte, Phase 6 | | ✅ |
| R012 | SKILL.md#Zweck (Z. 26–27) | Initialisiert neue Projekte mit dem Standard-Doc-Set des Profils | KEEP | S#Zweck | | | ✅ |
| R013 | SKILL.md#Zweck (Z. 27) | Erzwingt die Vorlagen des Profils bei neuen Docs | KEEP | S#Zweck | | | ✅ |
| R014 | SKILL.md#Vorrang (Z. 33–35) | Zuständig für Schreiben, Validieren, Refactoren; bei Code, Tasks, anderen Aktionen delegieren | REWRITE | S#Vorrang | „Schreiben, Ändern, Korrigieren und Refactoren“; „eine reine Prüfung“ als Delegationsfall ergänzt; Validieren → R019 | | ✅ sinngemäß |
| R015 | SKILL.md#Vorrang (Z. 39) | Code schreiben oder ändern → code-erstellen | KEEP | S#Vorrang | | | ✅ |
| R016 | SKILL.md#Vorrang (Z. 40) | UI-Entwurf als HTML-Mockup → mockup-erstellen | KEEP | S#Vorrang | | | ✅ |
| R017 | SKILL.md#Vorrang (Z. 41) | Commit-Befehl, Message, Version-Bump → git-commit-helper | KEEP | S#Vorrang | | | ✅ |
| R018 | SKILL.md#Vorrang (Z. 42) | ClickUp-Task anlegen, updaten, schließen → tracker | KEEP | S#Vorrang | | | ✅ |
| R019 | SKILL.md#Vorrang (Z. 43) | Konsistenzprüfung Code ↔ Docs (read-only) → audit | REWRITE | S#Vorrang | Zeile erweitert: „Prüfen oder validieren ohne Änderung (read-only): Konsistenz Code ↔ Docs, Frontmatter, Quickload, Router, Statuslisten“ | | ✅ sinngemäß |
| R020 | SKILL.md#Vorrang (Z. 45–47) | Zuständig nur bei echter Doc-Arbeit (neue Doc, refactoren, Frontmatter/Quickload validieren, ADR, INDEX.md-Routing) | REWRITE | S#Vorrang | „Frontmatter/Quickload ergänzen oder korrigieren“ statt „validieren“; ergänzt „Befunde aus einem Audit beheben, Sitzungsabschluss“ | | ✅ sinngemäß |
| R021 | SKILL.md#Vorrang (Z. 49–52) | Doc-Folgen von Code-Änderungen geben code-erstellen/git-commit-helper als Advisory-Hinweise aus (Kapitel „Advisory-Checkliste …“) | REWRITE | S#Vorrang | „Doku-Hinweise“, Verweis auf Abschnitt „Doku-Hinweise nach Code-Änderungen“ | | ✅ sinngemäß |
| R022 | SKILL.md#Vorrang (Z. 52–53) | Diese Hinweise sind KEIN Trigger für doc-pflege | KEEP | S#Vorrang | | | ✅ |
| R023 | SKILL.md#Vorrang (Z. 53–54) | Der User entscheidet ausdrücklich „pflege jetzt die Doku“, bevor doc-pflege übernimmt | KEEP | S#Vorrang | | | ✅ |
| R024 | SKILL.md#Grundsätze (Z. 65) | Modus-Auswahl bei Unsicherheit → Modus 0-8 als Optionen | REWRITE | S#Grundsätze | „Modusnamen als Optionen: Projekt-Init, Router nachziehen, Begleit-Docs, Doku pflegen, Neue Doc oder Umbau, Sitzungsabschluss“ | | ✅ sinngemäß |
| R025 | SKILL.md#Grundsätze (Z. 66) | Validierungsbefund (Modus 6) mit mehreren Lösungen → Doc anpassen, Quelle anpassen, Ignorieren mit Begründung | REWRITE | S#Grundsätze | „Befund beim Prüfen nach dem Schreiben mit mehreren Lösungen“; Optionen wörtlich | | ✅ sinngemäß |
| R026 | SKILL.md#Grundsätze (Z. 67) | Sitzungsabschluss (Modus 8): fertig, offen (Rest im HANDOFF), blockiert (Befund) | REWRITE | S#Grundsätze | Nummer entfernt; Optionen wörtlich | | ✅ sinngemäß |
| R027 | SKILL.md#Grundsätze (Z. 68) | Refactoring 7b, Inhalt passt in kein Kapitel → eigenes Kapitel am Ende, vorhandenes erweitern, Abbrechen | REWRITE | S#Grundsätze | „Doc umbauen:“; Optionen wörtlich | | ✅ sinngemäß |
| R028 | SKILL.md#Grundsätze (Z. 69) | Doc-Pflege Modus bei doc-relevanter Änderung → Jetzt pflegen, Später als Task anlegen, Ignorieren | KEEP | S#Grundsätze | ohne Modusnummer, daher wörtlich; Bezug nach Wegfall von Modus 3/4 offen (Frage an Herbert) | | ✅ |
| R029 | SKILL.md#Grundsätze (Z. 82) | Push-Policy betrifft den Commit im Sitzungsabschluss (Modus 8) | REWRITE | S#Grundsätze | Nummer entfernt | | ✅ sinngemäß |
| R030 | SKILL.md#Voraussetzung: Doku-Profil (Z. 109) | Profilfeld „Validierung (Modus 6)“: was geprüft wird (BPM Stufe A/B; Heidi Statusliste ↔ ClickUp ↔ Code …) | REWRITE | S#Voraussetzung: Doku-Profil | „Validierung – Was nach dem Schreiben geprüft wird (Abschnitt ‚Prüfen nach dem Schreiben‘)“; Projektwerte wörtlich | | ✅ sinngemäß |
| R031 | SKILL.md#Voraussetzung: Doku-Profil (Z. 112) | Profilfeld „Sitzungsabschluss (Modus 8)“ | REWRITE | S#Voraussetzung: Doku-Profil | Nummer entfernt; Werte wörtlich | | ✅ sinngemäß |
| R032 | SKILL.md#Advisory-Checkliste (Z. 193) | Überschrift „Advisory-Checkliste nach code-relevanten Änderungen“ | REWRITE | S#Doku-Hinweise nach Code-Änderungen | Name nach Auftrag | | ✅ sinngemäß |
| R033 | SKILL.md#Advisory-Checkliste (Z. 195) | Dieser Abschnitt ist KEIN Trigger | REWRITE | S#Doku-Hinweise nach Code-Änderungen | „KEIN Trigger und kein Modus“ | | ✅ sinngemäß |
| R034 | SKILL.md#Advisory-Checkliste (Z. 196) | Andere Skills nutzen ihn nach einer Änderung als Nachlauf-Checkliste | KEEP | S#Doku-Hinweise nach Code-Änderungen | | | ✅ |
| R035 | SKILL.md#Advisory-Checkliste (Z. 197) | User-Intent für doc-pflege steht ausschließlich in der Description | KEEP | S#Doku-Hinweise nach Code-Änderungen | | | ✅ |
| R036 | SKILL.md#Advisory-Checkliste (Z. 198–199) | Checkliste wird passiv konsumiert (code-erstellen, git-commit-helper), aktiviert doc-pflege nicht | KEEP | S#Doku-Hinweise nach Code-Änderungen | | | ✅ |
| R037 | SKILL.md#Quelle der Checkliste (Z. 203–205) | Nachlauf-Checkliste = Doku-Checkliste des Commit-Profils; keine eigene Liste | KEEP | S#Quelle der Checkliste: das Commit-Profil | | | ✅ |
| R038 | SKILL.md#Quelle der Checkliste (Z. 205–206) | Beispiel BPM (Tabelle → DB-SCHEMA.md, Entscheidung → ADR.md …) | KEEP | S#Quelle der Checkliste: das Commit-Profil | Projektwerte, Phase 6 | | ✅ |
| R039 | SKILL.md#Quelle der Checkliste (Z. 207–208) | Beispiel Heidi (Bauschritt → Statusliste …) | KEEP | S#Quelle der Checkliste: das Commit-Profil | Projektwerte, Phase 6 | | ✅ |
| R040 | SKILL.md#Typische Fälle (Z. 212) | Nachlauf-Checkliste nach doc-relevanten Änderungen durchlaufen | KEEP | S#Typische Fälle (Change-Class-basiert) | | | ✅ |
| R041 | SKILL.md#Typische Fälle (Z. 213) | Neue Tabelle / Schemaänderung / neue Entität im Vertrag | KEEP | S#Typische Fälle (Change-Class-basiert) | | | ✅ |
| R042 | SKILL.md#Typische Fälle (Z. 214) | Neue Architekturentscheidung / Paritätsabweichung | KEEP | S#Typische Fälle (Change-Class-basiert) | | | ✅ |
| R043 | SKILL.md#Typische Fälle (Z. 215) | Neuer Code-Entry-Point | KEEP | S#Typische Fälle (Change-Class-basiert) | | | ✅ |
| R044 | SKILL.md#Typische Fälle (Z. 216) | Neues Modul / Workflow mit Benutzerwirkung | KEEP | S#Typische Fälle (Change-Class-basiert) | | | ✅ |
| R045 | SKILL.md#Typische Fälle (Z. 217) | Neue Abhängigkeit | KEEP | S#Typische Fälle (Change-Class-basiert) | | | ✅ |
| R046 | SKILL.md#Typische Fälle (Z. 218) | Neues Doc / Doc-Refactor | KEEP | S#Typische Fälle (Change-Class-basiert) | | | ✅ |
| R047 | SKILL.md#Typische Fälle (Z. 219) | Bauschritt abgeschlossen (Statusliste, Aufgabenquelle) | KEEP | S#Typische Fälle (Change-Class-basiert) | | | ✅ |
| R048 | SKILL.md#NICHT triggern bei (Z. 223) | Lokale UI-Textfixes, Styling | KEEP | S#NICHT triggern bei: | | | ✅ |
| R049 | SKILL.md#NICHT triggern bei (Z. 224) | Kleine Refactors ohne Verhaltensänderung | KEEP | S#NICHT triggern bei: | | | ✅ |
| R050 | SKILL.md#NICHT triggern bei (Z. 225) | Umbenennungen ohne Strukturwirkung | KEEP | S#NICHT triggern bei: | | | ✅ |
| R051 | SKILL.md#NICHT triggern bei (Z. 226) | Reine Formatierungen | KEEP | S#NICHT triggern bei: | | | ✅ |
| R052 | SKILL.md#NICHT triggern bei (Z. 227) | Explorative Zwischenstände | KEEP | S#NICHT triggern bei: | | | ✅ |
| R053 | SKILL.md#NICHT triggern bei (Z. 228) | Bug-Fixes ohne Architekturbezug | KEEP | S#NICHT triggern bei: | | | ✅ |
| R054 | SKILL.md#Format: Advisory (Z. 232) | Statt voller Checkpoint-Checkliste kurze Merkliste am Ende der Antwort | KEEP | S#Format: Advisory (nicht interruptiv) | | | ✅ |
| R055 | SKILL.md#Format: Advisory (Z. 234–237) | Pflichtformat `📝 Doc-Hinweis: [Doc — Grund]` | KEEP | S#Format: Advisory (nicht interruptiv) | | | ✅ |
| R056 | SKILL.md#Format: Advisory (Z. 239) | Nur zutreffende Punkte, keine Checkliste mit leeren Punkten | KEEP | S#Format: Advisory (nicht interruptiv) | | | ✅ |
| R057 | SKILL.md#Format: Advisory (Z. 240) | Der User entscheidet, ob und wann die Doc-Pflege erfolgt | KEEP | S#Format: Advisory (nicht interruptiv) | | | ✅ |
| R058 | SKILL.md#8 Modi (Z. 244) | Überschrift „8 Modi“ | REWRITE | S#Modi | nach Auftrag | | ✅ sinngemäß |
| R059 | SKILL.md#Modus 0 (Z. 246) | Überschrift „Modus 0 — Projekt-Init (Standard-Doc-Set)“ | REWRITE | S#Projekt-Init | Name nach Auftrag; „Standard-Doc-Set“ steht in Schritt 4 (R065) | | ✅ sinngemäß |
| R060 | SKILL.md#Modus 0 (Z. 248) | Wann: „neues Projekt“, „init projekt“, kein Doku-Profil und keine INDEX.md | KEEP | S#Projekt-Init | | | ✅ |
| R061 | SKILL.md#Modus 0 (Z. 250) | Details: DOC-STANDARD.md Kapitel 3 (BPM) | KEEP | S#Projekt-Init | Projektwert, Phase 6 | | ✅ |
| R062 | SKILL.md#Modus 0 (Z. 253) | 1. Grundinfos sammeln | KEEP | S#Projekt-Init | | | ✅ |
| R063 | SKILL.md#Modus 0 (Z. 254) | 2. Repo scannen | KEEP | S#Projekt-Init | | | ✅ |
| R064 | SKILL.md#Modus 0 (Z. 255) | 3. Doku-Profil in der CLAUDE.md anlegen, mit Commit-, Tracker-, Code-Profil, wenn sie fehlen | KEEP | S#Projekt-Init | | | ✅ |
| R065 | SKILL.md#Modus 0 (Z. 256) | 4. Standard-Doc-Set laut Profil generieren | KEEP | S#Projekt-Init | | | ✅ |
| R066 | SKILL.md#Modus 0 (Z. 257) | 5. Korrekte Vorlagen des Profils | KEEP | S#Projekt-Init | | | ✅ |
| R067 | SKILL.md#Modus 0 (Z. 258) | 6. Invarianten-Check | KEEP | S#Projekt-Init | | | ✅ |
| R068 | SKILL.md#Modus 0 (Z. 259) | 7. Paket dem User vorlegen | KEEP | S#Projekt-Init | | | ✅ |
| R069 | SKILL.md#Modus 1 (Z. 263) | Überschrift „Modus 1 — Index Sync“ | REWRITE | S#Router nachziehen | Name nach Auftrag | | ✅ sinngemäß |
| R070 | SKILL.md#Modus 1 (Z. 265) | Wann: neues Doc, Doc umbenannt, neuer Code-Entry-Point | KEEP | S#Router nachziehen | | | ✅ |
| R071 | SKILL.md#Modus 1 (Z. 267–269) | Router des Profils laden und Eintrag nachziehen (BPM: INDEX.md; Heidi: CLAUDE.md, HANDOFF 5) | KEEP | S#Router nachziehen | | | ✅ |
| R072 | SKILL.md#Modus 2 (Z. 273) | Überschrift „Modus 2 — Companion Docs Check“ | REWRITE | S#Begleit-Docs | Name nach Auftrag | | ✅ sinngemäß |
| R073 | SKILL.md#Modus 2 (Z. 275) | Wann: neue Tabelle, Feature, Architekturentscheidung, Abhängigkeit, neue Entität | KEEP | S#Begleit-Docs | | | ✅ |
| R074 | SKILL.md#Modus 2 (Z. 277–278) | Doku-Checkliste des Commit-Profils → betroffene Pflicht-Docs ändern | KEEP | S#Begleit-Docs | | | ✅ |
| R075 | SKILL.md#Modus 3 (Z. 282–284) | Passive Advisory, wenn code-erstellen DocMaintenanceHints ausgegeben hat | MOVE | S#Doku-Hinweise nach Code-Änderungen | „Hat code-erstellen Doku-Hinweise (DocMaintenanceHints) ausgegeben: …“; kein Modus mehr | | ✅ |
| R076 | SKILL.md#Modus 3 (Z. 286) | Hints konsumieren, Hinweise ausgeben | MOVE | S#Doku-Hinweise nach Code-Änderungen | „sie übernehmen und als Hinweise ausgeben“ | | ✅ |
| R077 | SKILL.md#Modus 4 (Z. 290–292) | Automatischer Checkpoint nach doc-relevanten Änderungen (Nachlauf-Checkliste, kein Trigger) | MOVE | S#Doku-Hinweise nach Code-Änderungen | „Nach doc-relevanten Änderungen (Typische Fälle unten) …“; „kein Trigger“ = R033 | | ✅ |
| R078 | SKILL.md#Modus 4 (Z. 294) | Kurze Advisory-Merkliste ausgeben | MOVE | S#Doku-Hinweise nach Code-Änderungen | „eine kurze Merkliste im Format unten ausgeben“ | | ✅ |
| R079 | SKILL.md#Modus 4 (Z. 295) | NICHT bei trivialen Änderungen | MOVE | S#Doku-Hinweise nach Code-Änderungen | „nicht bei trivialen Änderungen (NICHT triggern bei)“ | | ✅ |
| R080 | SKILL.md#Modus 4 (Z. 296) | NICHT den Arbeitsfluss unterbrechen | MOVE | S#Doku-Hinweise nach Code-Änderungen | „ohne den Arbeitsfluss zu unterbrechen“ | | ✅ |
| R081 | SKILL.md#Modus 5 (Z. 300) | Überschrift „Modus 5 — Explicit Doc Maintenance“ | REWRITE | S#Doku pflegen | Name nach Auftrag | | ✅ sinngemäß |
| R082 | SKILL.md#Modus 5 (Z. 302) | Wann: „pflege die Doku“, „aktualisiere alles“ | KEEP | S#Doku pflegen | wörtlich; Liste ergänzt (N004) | | ✅ |
| R083 | SKILL.md#Modus 5 (Z. 304) | Volle Prüfung aller Pflicht-Docs des Profils | REWRITE | S#Doku pflegen | „Alle Pflicht-Docs des Profils durchgehen und nachziehen, was nicht mehr stimmt“ | | ✅ sinngemäß |
| R084 | SKILL.md#Modus 5 (Z. 304) | danach Validierung nach Modus 6 | REWRITE | S#Doku pflegen; S#Prüfen nach dem Schreiben | „Danach die geänderten Docs prüfen“; Umfang nach Zielbild enger (nur geänderte Docs), die Vollprüfung macht audit (R085) | | ✅ sinngemäß |
| R085 | SKILL.md#Modus 6 (Z. 308) | Validierung nach Profil als eigener Auftrag von doc-pflege | MOVE | A | Zielbild prüfen = audit; in S Abgrenzung (N003) und nur „Prüfen nach dem Schreiben“ (N005) | | offen (audit-Entwurf) |
| R086 | SKILL.md#Modus 6 (Z. 310) | Wann: „prüfe frontmatter“, „quickload check“, „prüfe die doku“, „stimmt der bauplan“, oder ausdrücklich angefordert | MOVE | A; S#Prüfen nach dem Schreiben | in S wörtlich als Beispiele der Abgrenzung „… macht audit“; die Auslöser trägt die audit-Description | | ✅ (S); offen (A) |
| R087 | SKILL.md#Modus 6 (Z. 312) | Prüfliste kommt aus dem Feld „Validierung“ des Doku-Profils | REWRITE | S#Prüfen nach dem Schreiben | Reihenfolge: Skill-Profil `Doku.Validierungsregeln`, im älteren Doku-Profil das Feld „Validierung“, sonst `AV` (N006) | | ✅ sinngemäß |
| R088 | SKILL.md#Modus 6 (Z. 312–313) | Befunde als Tabelle (Doc, Stelle, Befund, Vorschlag) | REWRITE | S#Prüfen nach dem Schreiben | gilt für Befunde, die eine Entscheidung brauchen oder vor der Änderung schon bestanden; Befunde der eigenen Änderung behebt doc-pflege gleich (N007) | | ✅ sinngemäß |
| R089 | SKILL.md#Modus 6 (Z. 313) | Bei mehreren Lösungen Auswahlfrage | MOVE | S#Prüfen nach dem Schreiben | wörtlich; Optionen in S#Grundsätze (R025) | | ✅ |
| R090 | SKILL.md#Modus 6 (Z. 313–314) | Nichts stillschweigend korrigieren, was eine Entscheidung des Users ist (Status, Freigaben) | MOVE | S#Prüfen nach dem Schreiben | wörtlich | | ✅ |
| R091 | SKILL.md#Heidi-Prüfliste, Stufe A (Z. 319) | Statusliste ↔ ClickUp-Status ↔ Code: fertig nur mit Code, Tests, Commit | MOVE | AV | Prüfliste zu audit (Auftrag) | | offen (audit-Entwurf) |
| R092 | SKILL.md#Heidi-Prüfliste, Stufe A (Z. 320) | Jede Abweichung von v1 hat PD-Eintrag in 10a mit Status `freigegeben` | MOVE | AV | | | offen (audit-Entwurf) |
| R093 | SKILL.md#Heidi-Prüfliste, Stufe A (Z. 321) | Abschnitt 4 ↔ `contract.ts`: gleiche Entitäten und Dienste | MOVE | AV | | | offen (audit-Entwurf) |
| R094 | SKILL.md#Heidi-Prüfliste, Stufe A (Z. 322) | HANDOFF 3e nennt letzten Bauschritt und aktuelle Version | MOVE | AV | | | offen (audit-Entwurf) |
| R095 | SKILL.md#Heidi-Prüfliste, Stufe A (Z. 323) | Nichts Verbotenes im Repo (Token, GPS, `.storage`, Datenbanken, Laufprotokolle) | MOVE | AV | | | offen (audit-Entwurf) |
| R096 | SKILL.md#Heidi-Prüfliste, Stufe B (Z. 326) | ⚠️ Notiz in Abschnitt 10 ohne Datum/Aufgabe/Art/Schwere; Entscheidung fehlt bei Widerspruch/Wunsch | MOVE | AV | | | offen (audit-Entwurf) |
| R097 | SKILL.md#Heidi-Prüfliste, Stufe B (Z. 327) | ⚠️ Aufgabenkarte ohne Akzeptanz oder Tests | MOVE | AV | | | offen (audit-Entwurf) |
| R098 | SKILL.md#Heidi-Prüfliste, Stufe B (Z. 328) | ⚠️ Offene Punkte (HANDOFF 4) ohne Gegenstück in ClickUp | MOVE | AV | | | offen (audit-Entwurf) |
| R099 | SKILL.md#Heidi-Prüfliste, Stufe B (Z. 329) | ⚠️ Plan-Doc ohne Stand-Datum | MOVE | AV | | | offen (audit-Entwurf) |
| R100 | SKILL.md#Heidi-Prüfliste, Stufe B (Z. 330) | ⚠️ Version in package.json, Lock, Ressourcen-`?v=` uneinheitlich | MOVE | AV | | | offen (audit-Entwurf) |
| R101 | SKILL.md#BPM-Prüfliste, Stufe A (Z. 336) | Frontmatter vorhanden bei Kern/, Module/, Referenz/ | MOVE | AV | | | offen (audit-Entwurf) |
| R102 | SKILL.md#BPM-Prüfliste, Stufe A (Z. 337) | Alle Pflichtfelder | MOVE | AV | | | offen (audit-Entwurf) |
| R103 | SKILL.md#BPM-Prüfliste, Stufe A (Z. 338) | doc_id eindeutig | MOVE | AV | | | offen (audit-Entwurf) |
| R104 | SKILL.md#BPM-Prüfliste, Stufe A (Z. 339) | Enums korrekt | MOVE | AV | | | offen (audit-Entwurf) |
| R105 | SKILL.md#BPM-Prüfliste, Stufe A (Z. 340) | Quickload bei source_of_truth/secondary | MOVE | AV | | | offen (audit-Entwurf) |
| R106 | SKILL.md#BPM-Prüfliste, Stufe A (Z. 341) | Quickload-Kapitelfeld stimmt mit H2s | MOVE | AV | | | offen (audit-Entwurf) |
| R107 | SKILL.md#BPM-Prüfliste, Stufe A (Z. 342) | Kapitelreihenfolge nach Vorlage | MOVE | AV | | | offen (audit-Entwurf) |
| R108 | SKILL.md#BPM-Prüfliste, Stufe A (Z. 343) | Pflichtlesen verweist auf existierende Kapitel | MOVE | AV | | | offen (audit-Entwurf) |
| R109 | SKILL.md#BPM-Prüfliste, Stufe A (Z. 344) | Fachliche Invarianten höchstens 5 | MOVE | AV | | | offen (audit-Entwurf) |
| R110 | SKILL.md#BPM-Prüfliste, Stufe B (Z. 348) | ⚠️ Quickload-Kapitel stimmt nicht mit H2s | MOVE | AV | | | offen (audit-Entwurf) |
| R111 | SKILL.md#BPM-Prüfliste, Stufe B (Z. 349) | ⚠️ historical als Primary im Router | MOVE | AV | | | offen (audit-Entwurf) |
| R112 | SKILL.md#BPM-Prüfliste, Stufe B (Z. 350) | ⚠️ related_docs nicht existent | MOVE | AV | | | offen (audit-Entwurf) |
| R113 | SKILL.md#BPM-Prüfliste, Stufe B (Z. 351) | ⚠️ Kapitelvorlage nicht eingehalten | MOVE | AV | | | offen (audit-Entwurf) |
| R114 | SKILL.md#BPM-Prüfliste, Stufe B (Z. 352) | ⚠️ Fachliche Invarianten leer bei großem Modul | MOVE | AV | | | offen (audit-Entwurf) |
| R115 | SKILL.md#BPM-Prüfliste, Stufe B (Z. 353) | ⚠️ Pflichtlesen leer bei source_of_truth-Modul | MOVE | AV | | | offen (audit-Entwurf) |
| R116 | SKILL.md#Modus 7 (Z. 357) | Überschrift „Modus 7 — Neue Doc erstellen oder Refactoring“ | REWRITE | S#Neue Doc oder Umbau | Name nach Auftrag | | ✅ sinngemäß |
| R117 | SKILL.md#Modus 7 (Z. 359–361) | Wann: „neues Konzept für X“, „erstelle Modul-Doc für Y“, „refactore … nach Standard“, „docs umbauen“, oder wenn in Modus 0/2 ein neues Doc entsteht | REWRITE | S#Neue Doc oder Umbau | Beispiele wörtlich; „bei Projekt-Init oder Begleit-Docs“ statt „in Modus 0/2“ | | ✅ sinngemäß |
| R118 | SKILL.md#7a (Z. 363) | Überschrift „7a. Neue Doc erstellen“ | REWRITE | S#Neue Doc | Name nach Auftrag | | ✅ sinngemäß |
| R119 | SKILL.md#7a (Z. 365) | 1. Vorlage für den Doc-Typ aus dem Profil laden | KEEP | S#Neue Doc | | | ✅ |
| R120 | SKILL.md#7a (Z. 366) | 2. Router laden → verwandte Docs | KEEP | S#Neue Doc | | | ✅ |
| R121 | SKILL.md#7a (Z. 367) | 3. Quickloads verwandter Docs lesen → Invarianten sammeln | KEEP | S#Neue Doc | | | ✅ |
| R122 | SKILL.md#7a (Z. 368) | 4. Doc mit Frontmatter, Quickload, Kapitelstruktur erstellen | KEEP | S#Neue Doc | | | ✅ |
| R123 | SKILL.md#7a (Z. 369–379) | 5. Invarianten-Check mit Pflichtformat (Invarianten, Pflichtlesen, related_docs) | KEEP | S#Neue Doc | | | ✅ |
| R124 | SKILL.md#7a (Z. 381) | 6. INDEX.md-Routing-Eintrag vorschlagen | KEEP | S#Neue Doc | | | ✅ |
| R125 | SKILL.md#7b (Z. 383) | Überschrift „7b. Bestehendes Doc refactoren“ | REWRITE | S#Doc umbauen | Name nach Auftrag | | ✅ sinngemäß |
| R126 | SKILL.md#7b (Z. 385) | 1. Vorlage für den Doc-Typ laden | KEEP | S#Doc umbauen | | | ✅ |
| R127 | SKILL.md#7b (Z. 386) | 2. Bestehende Doc komplett laden | KEEP | S#Doc umbauen | | | ✅ |
| R128 | SKILL.md#7b (Z. 387) | 3. Inhalt auf Standard-Kapitel mappen | KEEP | S#Doc umbauen | | | ✅ |
| R129 | SKILL.md#7b (Z. 388) | 4. Frontmatter + Quickload ergänzen oder aktualisieren | KEEP | S#Doc umbauen | | | ✅ |
| R130 | SKILL.md#7b (Z. 389) | 5. Invarianten-Check | KEEP | S#Doc umbauen | | | ✅ |
| R131 | SKILL.md#7b (Z. 390) | 6. Vollständigkeits-Check gegen das Original | KEEP | S#Doc umbauen | | | ✅ |
| R132 | SKILL.md#7b (Z. 393) | KEIN Inhalt gelöscht oder gekürzt, nur umordnen | KEEP | S#Doc umbauen | | | ✅ |
| R133 | SKILL.md#7b (Z. 394) | Inhalt ohne Standard-Kapitel → eigenes Kapitel am Ende | KEEP | S#Doc umbauen | | | ✅ |
| R134 | SKILL.md#7b (Z. 395–396) | Danach Abschnitt für Abschnitt auf Vollständigkeit prüfen | KEEP | S#Doc umbauen | | | ✅ |
| R135 | SKILL.md#7b (Z. 397) | Im Zweifel ein Kapitel zu viel statt Inhalt verlieren | KEEP | S#Doc umbauen | | | ✅ |
| R136 | SKILL.md#7b (Z. 399) | VERBOTEN: Doc ohne die Vorlage des Profils erstellen | KEEP | S#Doc umbauen | | | ✅ |
| R137 | SKILL.md#7b (Z. 400) | VERBOTEN: beim Refactoring Inhalte weglassen, kürzen, zusammenfassen | KEEP | S#Doc umbauen | | | ✅ |
| R138 | SKILL.md#Modus 8 (Z. 404) | Überschrift „Modus 8 — Sitzungsabschluss“ | REWRITE | S#Sitzungsabschluss | Name nach Auftrag | | ✅ sinngemäß |
| R139 | SKILL.md#Modus 8 (Z. 406–408) | Wann: „sitzung abschließen“, „wir hören auf“, „stand festhalten“, nach dem letzten `tracker done`, oder wenn Bauplan/Profil es verlangt | KEEP | S#Sitzungsabschluss | | | ✅ |
| R140 | SKILL.md#Modus 8 (Z. 408) | Ersetzt nicht chat-wechsel, liefert ihm zu | KEEP | S#Sitzungsabschluss | | | ✅ |
| R141 | SKILL.md#Modus 8 (Z. 410) | Orte aus dem Profil, Feld „Sitzungsabschluss“ | KEEP | S#Sitzungsabschluss | | | ✅ |
| R142 | SKILL.md#Modus 8 (Z. 411–413) | 1. Aufgabenquelle/Statusliste nachziehen; unklar → Auswahlfrage fertig/offen/blockiert | KEEP | S#Sitzungsabschluss | | | ✅ |
| R143 | SKILL.md#Modus 8 (Z. 414) | 2. Befunde und Entscheidungen eintragen | KEEP | S#Sitzungsabschluss | | | ✅ |
| R144 | SKILL.md#Modus 8 (Z. 415) | 3. Stand-Abschnitt schreiben | KEEP | S#Sitzungsabschluss | | | ✅ |
| R145 | SKILL.md#Modus 8 (Z. 416–417) | 4. Offene Punkte als Checkliste, je mit ClickUp-Bezug oder Begründung | KEEP | S#Sitzungsabschluss | | | ✅ |
| R146 | SKILL.md#Modus 8 (Z. 418) | 5. Doku-Checkliste des Commit-Profils durchgehen | KEEP | S#Sitzungsabschluss | | | ✅ |
| R147 | SKILL.md#Modus 8 (Z. 419–420) | 6. Commit `[vX.Y.Z] <Doku-Modul>, Docs: Sitzungsabschluss …`; Push nach Push-Policy | KEEP | S#Sitzungsabschluss | | | ✅ |
| R148 | SKILL.md#Modus 8 (Z. 421–422) | 7. Kurzer Abschlussbericht, taugt als Einstieg für chat-wechsel | KEEP | S#Sitzungsabschluss | | | ✅ |
| R149 | SKILL.md#Modus 8 (Z. 424) | VERBOTEN: Sitzung beenden mit uncommitteten Doku-Änderungen | KEEP | S#Sitzungsabschluss | | | ✅ |
| R150 | SKILL.md#Modus 8 (Z. 424) | VERBOTEN: Statusliste „fertig“ ohne Tests und Commit | KEEP | S#Sitzungsabschluss | | | ✅ |
| R151 | SKILL.md#Modus 8 (Z. 425) | VERBOTEN: offene Punkte nur im Chat statt im Doc | KEEP | S#Sitzungsabschluss | | | ✅ |
| R152 | SKILL.md#Skill-Governance (Z. 444) | Split-Prüfung (skill-pflege Regel 21): Modi noch in einer Datei sinnvoll? | REWRITE | S#Skill-Governance | Verweis über Datei und Überschrift: `skills/skill-pflege/SKILL.md`, Abschnitt „Split-Prüfung“ | | ✅ sinngemäß |
| R153 | SKILL.md#VERBOTEN (Z. 453) | Modus 4 bei trivialen Änderungen triggern | REWRITE | S#VERBOTEN | „Doku-Hinweise bei trivialen Änderungen ausgeben“ | | ✅ sinngemäß |
| R154 | SKILL.md#VERBOTEN (Z. 454) | Modus 4 als interruptive Checkliste statt Advisory ausgeben | REWRITE | S#VERBOTEN | „Doku-Hinweise als interruptive Checkliste statt kurzer Merkliste ausgeben“ | | ✅ sinngemäß |
| R155 | SKILL.md#VERBOTEN (Z. 463) | Sitzung ohne Modus 8 beenden, wenn Docs geändert wurden | REWRITE | S#VERBOTEN | „ohne Sitzungsabschluss“ | | ✅ sinngemäß |
| N001 | – | Description: neue Auslöser „korrigieren, umbauen“; Was-Teil „behebt … Befunde aus einem Audit“, Use-when „fixing audit findings“ | NEW | S#Frontmatter | Auftrag (neue Description); Eval-Fall `audit-findings-fix` | | ✅ |
| N002 | – | Do not trigger for read-only checks or validation without changes (use audit) | NEW | S#Frontmatter | Zielbild prüfen = audit; Eval-Fälle `audit-frontmatter`, `audit-bauplan`, `audit-code-docs`, `audit-generic-check`, `audit-readonly` | | ✅ |
| N003 | – | Eine Prüfung ohne Änderungsauftrag macht audit; reine Prüfung wird delegiert | NEW | S#Zweck; S#Vorrang; S#Prüfen nach dem Schreiben | Zielbild; nimmt die Beispiele aus R086 auf | | ✅ |
| N004 | – | Doku pflegen gilt auch für Doku-Fehler (Tippfehler, kaputte Links, veraltete Kapitel) und Befunde aus einem Audit; übergebene Befunde als Aufgabenliste abarbeiten | NEW | S#Doku pflegen | Description (R005, N001); audit übergibt Doc-Befunde an doc-pflege (A, „Nach dem Report“) | | ✅ |
| N005 | – | Prüfen nach dem Schreiben: nach Doku pflegen und Neue Doc oder Umbau, nur die dabei geänderten oder angelegten Docs | NEW | S#Prüfen nach dem Schreiben; Verweise in S#Doku pflegen und S#Neue Doc oder Umbau | Auftrag (Modus 6 → „Prüfen nach dem Schreiben“) | | ✅ |
| N006 | – | Prüfregeln: Skill-Profil `Doku.Validierungsregeln`, sonst die Prüflisten in `AV` | NEW | S#Prüfen nach dem Schreiben | Auftrag; `docs/skill-profile-v1.md` (Feld Doku.Validierungsregeln); älteres Doku-Profil = R087 | | ✅ |
| N007 | – | Befunde in der eigenen Änderung gleich beheben | NEW | S#Prüfen nach dem Schreiben | Sinn der Prüfung nach dem Schreiben; alles andere als Tabelle (R088) | | ✅ |

## DROP-Gruppen

Keine. Modus 3, 4 und 6 fallen als Modi weg, ihre Regeln bleiben erhalten: Modus 3 und 4 im Abschnitt „Doku-Hinweise nach
Code-Änderungen“ (R075–R080), Modus 6 als Auftrag und mit seinen Prüflisten bei audit (R085, R086, R091–R115), die
Befund-Regeln in „Prüfen nach dem Schreiben“ (R087–R090). Enger wird nur der Umfang der Prüfung in „Doku pflegen“: nach
dem Schreiben werden nur die geänderten Docs geprüft (R084) – so im freigegebenen Zielbild.

## Verweise von außen

| Stelle | Verweis | Behandlung |
|---|---|---|
| `skills/audit/SKILL.md` Z. 85 | „Profil anlegen (doc-pflege Modus 0)“ | audit-Entwurf dieser Phase: „doc-pflege, Projekt-Init“ |
| `skills/audit/SKILL.md` Z. 206–207 | „siehe doc-pflege Modus 6 (Validierung nach Profil; BPM Stufe A …, Heidi-Prüfliste ebendort)“ | audit-Entwurf: auf `AV` umstellen; ohne `AV` im selben Commit ist der Verweis in S tot (Fehler im Prüfskript) |
| `skills/audit/SKILL.md` Z. 276 | „Doc-Befunde → doc-pflege Modus 5/6“ | audit-Entwurf: „doc-pflege, Doku pflegen“ |
| `skills/audit/SKILL.md` Frontmatter | Auslöser für Validierung (Frontmatter, Quickload, Bauplan) | audit-Entwurf übernimmt „validieren“ (R003) und die Prüfanfragen aus R086 |
| `skills/chatgpt-review/SKILL.md` Z. 475 | im Commit 262ee9a „Schreiben tut doc-pflege (Modus 7a/2)“ | im Arbeitsstand des Repos während dieses Entwurfs schon auf „doc-pflege (Neue Doc, Begleit-Docs)“ geändert (uncommittet, nicht aus diesem Entwurf) – passt zu den neuen Namen |
| `skills/chat-wechsel/SKILL.md` (Description, Z. 20, 358, 492, 505) | im Commit 262ee9a „doc-pflege Modus 8“ | im Arbeitsstand ebenso schon auf „doc-pflege, Sitzungsabschluss“ geändert (uncommittet, nicht aus diesem Entwurf) – passt |
| `skills/code-erstellen/SKILL.md` Z. 354, 441 | „Commit + DocMaintenanceHints (→ git-commit-helper + doc-pflege)“ | passt: der Begriff steht jetzt in S#Doku-Hinweise nach Code-Änderungen |
| `INDEX.md` Z. 24 | doc-pflege: „Projektdoku anlegen, pflegen, validieren; Sitzungsabschluss“ | Doku-Check (Zuständigkeit geändert): „validieren“ raus, „Audit-Befunde beheben“ rein; Konfliktpaar „audit ↔ doc-pflege“ fehlt (nur prüfen → audit; ändern, Befunde beheben → doc-pflege) – im selben Commit wie der Umbau |
| `README.md` Z. 79 | doc-pflege: „Erstellt und pflegt Projektdokumentation nach Doku-Profil (BPM: DOC-STANDARD.md)“ | passt inhaltlich; keine Pflicht |
| `docs/skill-profile-v1.md`, Pflichtfelder je Skill | doc-pflege: Doku.Router, Doku.Standard, Doku.Entscheidungs-Ort; Commit.Push-Policy | doc-pflege liest jetzt auch `Doku.Validierungsregeln` (mit Rückfall auf `AV`); ob das Feld dort genannt wird, entscheidet Herbert |
| `docs/skillsystem-umbau.md` Z. 176 | Phase-5-Punkt „Grenzen audit ↔ doc-pflege … (doc-pflege Modus 3, 4 und 6 … entfernen)“ | nach Commit und Eval abhaken |
| `quality/evals/tracker-issue/prompt.md` | „Skill-Issue für doc-pflege an: Modus 6 erkennt tote Links nicht“ | Prompt-Text eines tracker-Falls, für das Auslösen ohne Bedeutung; bleibt oder wird in Phase 7 angepasst |
| `CHANGELOG.md` Z. 194–196, 568, 788–790; `docs/skill-refactor-phases.md` Z. 53 | Modus 6, Advisory-Checkliste | Historie, bleibt |
| `skills/tracker/references/anti-patterns.md` | „doc-pflege nach Doc-Update“ | passt |

## Prüfung

- **Freigabe:** Zielbild und Modusnamen von Herbert freigegeben (28.09.2026, Auftrag Phase 5). Zielstruktur dieses
  Entwurfs noch nicht per Auswahlfrage freigegeben; keine DROP-Zeile.
- **Alt→Neu:** 155 alte IDs mit Zustand (KEEP 81, MOVE 36, REWRITE 38, MERGE 0, DROP 0) und N001–N007. Jeder Neu-Ort in
  S ist im Entwurf gelesen. Offen sind die Neu-Orte in `A` und `AV` (R003, R085, R086, R091–R115): Sie entstehen im
  audit-Entwurf und werden dort abgeglichen.
- **Neu→Alt:** Kandidaten des Entwurfs mit `-RuleInventory` in eine Scratchpad-Kopie gesammelt (58 Kandidaten). Alle
  gehören zu einer R-ID (die neuen Zeilen: Delegation → R019, Auswahlfrage-Tabelle → R024–R027, Profilzeilen → R030/R031,
  „KEIN Trigger und kein Modus“ → R033, Doku pflegen → R083/N004, VERBOTEN → R153–R155). Von Hand dazu: Zweck-Satz (R009,
  N003), Vorrang (R014, R020, R021), „So wird sie genutzt“ (R075–R080), Modus-Überschriften, Doku pflegen (R082–R084,
  N004), Neue Doc oder Umbau (R117, N005), Prüfen nach dem Schreiben (R086–R090, N003, N005–N007), Skill-Governance
  (R152). Keine Aussage ohne Zuordnung.
- **Diff** (`git diff --no-index` Repo ↔ Entwurf): Änderungen nur in Frontmatter (Z. 4–15), Zweck (Z. 22), Vorrang
  (Z. 33–35, 43, 46–47, 51–52), Grundsätze (Z. 65–68, 82), Voraussetzung: Doku-Profil (Z. 109, 112), Advisory-Abschnitt
  (Z. 193, 195, neu 5 Zeilen nach Z. 199), Modi (Z. 244–404: Überschriften, Modus 3–6 ersetzt, Z. 361), neuer Abschnitt
  vor „Ausgabeformat“, Skill-Governance Z. 444, VERBOTEN Z. 453–454 und 463. Alles andere byte-gleich (LF, Zeilenende).
- **Zeilen:** 463 → 422 (`wc -l`); Körper laut Prüfskript 448 → 405 (unter 500). Split-Prüfung: kein neuer Split nötig;
  die Prüflisten wandern zu audit, Projektwerte bleiben bis Phase 6.
- **Description:** 857 → 980 Zeichen (Zeilen getrimmt, mit Leerzeichen verbunden, gezählt wie `tools/validate-skills.ps1`);
  keine spitzen Klammern, kein BPM/Heidi, dritte Person, „Use when … Do not trigger for …“.
- **Prüfskript** (Scratchpad-Kopie des Repos mit dem Entwurf, `-Skill doc-pflege`): mit Platzhalter für `AV` 0 Fehler,
  1 Warnung (49 Zeilen mit Projektbegriffen, vorher 57); ohne `AV` 1 Fehler „toter Verweis
  `skills/audit/references/doku-validierung.md`“ – der audit-Entwurf muss im selben Commit kommen. Entfallen sind die
  Warnungen „description nennt ein Projekt“ und „Querverweis über Nummern“ (skill-pflege Regel 21).
- **Routing-Eval:** wird nach dem Commit eingetragen (betroffen: `--tag doc-pflege --tag audit`, u. a. `doc-write`,
  `doc-fix-links`, `audit-findings-fix`, `audit-frontmatter`, `audit-bauplan`, `audit-code-docs`, `audit-generic-check`,
  `audit-readonly`, `doc-session-close`, `doc-no-trigger-discussion`).
