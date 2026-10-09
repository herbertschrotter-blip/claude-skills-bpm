# Regel-Inventar – projekt-anlegen (Projekt-Generator)

## Inhalt

- Kopf
- Zielstruktur
- Inventar
- DROP-Gruppen
- Verweise von außen
- Prüfung

## Kopf

- **Skill:** `skills/projekt-anlegen/`
- **Stand vor dem Umbau:** `main` cda63e6, v0.47.1; `SKILL.md` 166 Zeilen, `references/github.md`,
  `references/stacks/home-assistant.md`, `references/stacks/python.md`
- **Anlass:** projekt-anlegen soll nach wenigen Fragen ein lauffähiges, getestetes Grundgerüst liefern (Walking
  Skeleton). Plan: `docs/skillsystem-umbau.md`, Abschnitt „Plan (09.10.2026, von Herbert freigegeben) – projekt-anlegen
  als Projekt-Generator“; Review `docs/chatgpt-reviews/CGR-2026-10-09-skillsystem/`; ClickUp 123ztrd0r0p.
- **Zweig:** `umbau-projekt-anlegen` (Worktree), Merge nach Freigabe.
- **Prüfskript:** `tools/validate-skills.ps1 -RuleInventory` läuft auf dem Pi nicht (kein PowerShell); Kandidaten von
  Hand gesammelt, Prüfung nach dem Push per GitHub Actions.
- **Stand des Inventars:** Schritt 6. Zielstruktur von Herbert freigegeben (09.10.2026); keine DROP-Zeilen.

## Zielstruktur (Vorschlag)

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | Zweck und Grenzen · Benötigte Werte · Ablauf (1 Klären · 2 Bestand prüfen · 3 Ort und Quelle der Wahrheit · 4 Plan zeigen · 5 Erzeugen · 6 Eintragen und übergeben) · Bestehendes Repo einrichten · Stacks · VERBOTEN · VERWEIS |
| `references/generator.md` (neu) | Grenze Generator ↔ Skill · Erzeugungsauftrag v1 · Bausteine und unterstützte Kombinationen · Ablauf Prepare / Verify / Publish · Herkunftsdatei · claude.ai (nur Plan) · Fehler und Rückbau |
| `references/grundsatz.md` (neu) | Drei Ebenen (Generator-Standards, Auswahlfragen, Projektdoku) · Pflichtklärungen und Fragen in Alltagssprache · Abschnitt „Grundentscheidungen“ am `Doku.Entscheidungs-Ort` |
| `references/stacks/python.md` | Arten · Grunddateien · Testgerüst (verweist auf die Bausteine) · Skill-Profil |
| `references/stacks/home-assistant.md` | unverändert bis zum Baustein HA-Integration (P2) |
| `references/github.md` | unverändert |
| `scripts/`, `templates/` (neu) | Generator, Validator, Tests; Bausteine, Manifeste, `versions.json` |

## Inventar

Abkürzung `S` = `SKILL.md`, `P` = `references/stacks/python.md`.

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | S#Frontmatter (Z. 3–16) | Description: was der Skill tut, Use when (anlegen, Repo erstellen/klonen, „neues Projekt“, „weiß aber nicht wie“, Repo für Skills einrichten), Do not trigger (code-erstellen, mockup-erstellen, skill-neu/-pflege, tracker, doc-pflege, git) | REWRITE | S#Frontmatter | Fassung aus CGR r3 (839 Zeichen), alle Auslöser bleiben | | ✅ sinngemäß |
| R002 | S#Zweck (Z. 23–25) | Führt von der Idee zum eingerichteten Projekt: klären, prüfen, Ort, anlegen, eintragen; danach Fachskills | REWRITE | S#Zweck und Grenzen | „anlegen“ wird „Grundgerüst erzeugen“ | | ✅ sinngemäß |
| R003 | S#Zweck (Z. 27–28) | Grenzen: Inhalt und Code → code-erstellen, Entwürfe → mockup-erstellen, Doku → doc-pflege, Aufgaben → tracker; dieser Skill nur Gerüst | REWRITE | S#Zweck und Grenzen | Grenzregel „technische Funktionsfähigkeit vs. fachliches Verhalten“ (CGR r1) | | ✅ sinngemäß |
| R004 | S#Zweck (Z. 29–31) | Bestehende Projekte → code-erstellen; Ausnahmen klonen und für Skills einrichten | KEEP | S#Zweck und Grenzen | | | ✅ |
| R005 | S#Zweck (Z. 32) | Prüfen eines Projekts gegen seine Regeln → audit | KEEP | S#Zweck und Grenzen | | | ✅ |
| R006 | S#Benötigte Werte (Z. 36–45) | Werte aus dem Skill-Profil: Ablage, Übersicht, GitHub-Owner, Geschützt, Code.Stacks, Modul.Grundsatzregeln mit Verhalten bei Fehlen | KEEP | S#Benötigte Werte | dazu `Doku.Entscheidungs-Ort` (N004) | | ✅ |
| R007 | S#Benötigte Werte (Z. 47–48) | Fehlt das Profil: Vorschlag, Anlage nur nach Zustimmung; nie Pfad oder Owner raten | KEEP | S#Benötigte Werte | | | ✅ |
| R008 | S#Ablauf (Z. 52–53) | Jeder Übergang über eine Auswahlfrage; Beantwortetes nicht erneut fragen | KEEP | S#Ablauf | | | ✅ |
| R009 | S#1. Klären (Z. 57) | Auswahlfrage mit den Arten der Stack-Reference plus „weiß ich noch nicht“ | REWRITE | S#1. Klären | wird Teil der Pflichtklärung „Was soll es tun?“ (N002) | | ✅ sinngemäß |
| R010 | S#1. Klären (Z. 59–63) | Bei „weiß ich noch nicht“ wenige Fragen: Ergebnis, Datenquelle, Bedienung, rechnen oder anzeigen | REWRITE | references/grundsatz.md#Pflichtklärungen und Fragen | Fragen in Alltagssprache, nur bei Bedarf | | ✅ sinngemäß |
| R011 | S#1. Klären (Z. 65–66) | Art vorschlagen und begründen; einfachste passende Art gewinnt (laut Stack-Reference) | KEEP | S#1. Klären | | | ✅ |
| R012 | S#1. Klären (Z. 66–67) | Nur Aussehen offen → mockup-erstellen anbieten, bevor etwas angelegt wird | KEEP | S#1. Klären | | | ✅ |
| R013 | S#2. Bestand (Z. 71) | In Übersicht und Ablage nach Ähnlichem suchen | KEEP | S#2. Bestand prüfen | ergänzt um „bestehendes System anbinden?“ (CGR r1) | | ✅ |
| R014 | S#2. Bestand (Z. 72) | Vorhandenes Repo → klonen statt neu anlegen (github.md) | KEEP | S#2. Bestand prüfen | | | ✅ |
| R015 | S#2. Bestand (Z. 73) | Projekt schon am Ort → nicht anlegen, auf code-erstellen verweisen | KEEP | S#2. Bestand prüfen | | | ✅ |
| R016 | S#3. Ort (Z. 77–78) | Eigenes Repo in Ablage bei eigenem Code, Versionen, Veröffentlichung | KEEP | S#3. Ort und Quelle der Wahrheit | | | ✅ |
| R017 | S#3. Ort (Z. 79–80) | Ordner im aktuellen Repo bei reiner Konfiguration; Zuordnung laut Stack-Reference | KEEP | S#3. Ort und Quelle der Wahrheit | Weg ohne Generator (CGR r1) | | ✅ |
| R018 | S#3. Ort (Z. 81–83) | Genau eine Quelle der Wahrheit; Arbeitsort und Weg zu anderen Orten festlegen | KEEP | S#3. Ort und Quelle der Wahrheit | | | ✅ |
| R019 | S#3. Ort (Z. 84–85) | Auslieferung festlegen und als `Code.Auslieferung` ins Profil schreiben | KEEP | S#3. Ort und Quelle der Wahrheit | dazu Rückweg (Grundsatz-Prüfung) | | ✅ |
| R020 | S#3. Ort (Z. 86) | Nichts in `Projekte.Geschützt` anlegen oder ändern | KEEP | S#3. Ort und Quelle der Wahrheit | | | ✅ |
| R021 | S#4. Plan (Z. 90–91) | Plan nennt Name, Art, Ort, Ordnerbaum, Git, GitHub/Sichtbarkeit, Profilwerte, Einträge an anderen Stellen | REWRITE | S#4. Plan zeigen | dazu Grundentscheidungen und abgeleitete Technik in Alltagssprache | | ✅ sinngemäß |
| R022 | S#4. Plan (Z. 92) | Auswahlfrage anlegen / anpassen / abbrechen | KEEP | S#4. Plan zeigen | | | ✅ |
| R023 | S#5. Anlegen (Z. 96) | Ordner und Grunddateien nach Stack-Reference; nur Gerüst, lauffähige Minimalfassung, keine Fachlogik | REWRITE | S#5. Erzeugen | unterstützte Kombination → Generator (references/generator.md); sonst nach Stack-Reference; Grenzregel R003 | | ✅ sinngemäß |
| R024 | S#5. Anlegen (Z. 97–100) | Testgerüst parallel-fähig: Worker-Zahl zur Laufzeit, kein Test beeinflusst einen anderen, Versionen angeheftet, Check mit Pfad-Mustern ins Profil | MOVE | references/generator.md#Bausteine; P#Testgerüst | im Generator fest eingebaut; ohne Generator gilt P | | ✅ |
| R025 | S#5. Anlegen (Z. 101) | Kerne und Speicher einmal als Info, nichts ins Profil | KEEP | S#5. Erzeugen | | | ✅ |
| R026 | S#5. Anlegen (Z. 102–103) | Eigenes Repo: git init, .gitignore, README, CHANGELOG, CLAUDE.md mit Profil (fehlt / none) | REWRITE | S#5. Erzeugen | Baustein `common`; ohne Generator unverändert | | ✅ sinngemäß |
| R027 | S#5. Anlegen (Z. 104) | Erster Commit im Format von git-commit-helper; Push nach Push-Policy | REWRITE | S#5. Erzeugen | erst nach grünem Verify (N006) | | ✅ sinngemäß |
| R028 | S#5. Anlegen (Z. 105) | GitHub nur nach Auswahlfrage (privat Standard); Ablauf github.md | KEEP | S#5. Erzeugen | nach dem lokalen Publish; ci-github bei GitHub standardmäßig (N008) | | ✅ |
| R029 | S#5. Anlegen (Z. 106–107) | Registrierung in der Umgebung nur ungeschützt und mit eigener Rückfrage | KEEP | S#5. Erzeugen | | | ✅ |
| R030 | S#5. Anlegen (Z. 108) | Keine Geheimnisse in Dateien; Zugangsdaten an den Ort des Stacks | KEEP | S#5. Erzeugen | | | ✅ |
| R031 | S#6. Eintragen (Z. 112) | Zeile in `Projekte.Übersicht`: Name, Art, Ort, Quelle der Wahrheit, Repo | KEEP | S#6. Eintragen und übergeben | | | ✅ |
| R032 | S#6. Eintragen (Z. 113) | Zusammenfassung: angelegt, `fehlt` im Profil, Aufgaben des Nutzers | KEEP | S#6. Eintragen und übergeben | dazu Ergebnis der Prüfungen (Tabelle) | | ✅ |
| R033 | S#6. Eintragen (Z. 114–115) | Nächster Schritt per Auswahlfrage: mockup-erstellen / code-erstellen / tracker / fertig | KEEP | S#6. Eintragen und übergeben | | | ✅ |
| R034 | S#Bestehendes Repo (Z. 119–121) | Für Repos ohne/mit unvollständigem Profil; kein Gerüst, nur Profil und Configs; Auswahlfragen | KEEP | S#Bestehendes Repo einrichten | darf nicht in den Generatorpfad (CGR r1) | | ✅ |
| R035 | S#Bestehendes Repo (Z. 123–124) | Repo lesen: CLAUDE.md, README, Build-/Testdateien, Versionsquelle, Branches, Commit-Stil, docs/ | KEEP | S#Bestehendes Repo einrichten | | | ✅ |
| R036 | S#Bestehendes Repo (Z. 125–126) | Bereiche per Mehrfachauswahl; Pflichtfelder laut skill-profile-v1 | KEEP | S#Bestehendes Repo einrichten | | | ✅ |
| R037 | S#Bestehendes Repo (Z. 127–130) | Vorschlag Profil v1 mit Herkunft, fehlt/none, Configs; anlegen/anpassen/abbrechen | KEEP | S#Bestehendes Repo einrichten | | | ✅ |
| R038 | S#Bestehendes Repo (Z. 131–133) | Profil anhängen, vorhandener Text bleibt; doppelte Werte klären; Commit und Push nach Profil | KEEP | S#Bestehendes Repo einrichten | | | ✅ |
| R039 | S#Bestehendes Repo (Z. 134–135) | Übergeben: fehlende Felder, Kerne/Speicher, nächster Schritt | KEEP | S#Bestehendes Repo einrichten | | | ✅ |
| R040 | S#Stacks (Z. 139–140) | Arten, Orte, Grunddateien, .gitignore in references/stacks/<key>.md; Schlüssel aus Code.Stacks; nur die genannte Datei laden | KEEP | S#Stacks | dazu: welche Stacks der Generator unterstützt | | ✅ |
| R041 | S#Stacks (Z. 142–143) | Liste der Stack-References | KEEP | S#Stacks | | | ✅ |
| R042 | S#Stacks (Z. 145–146) | Ohne Reference nach Art und Grunddateien fragen, nur Bestätigtes anlegen, keine Vorlagen erfinden | KEEP | S#Stacks | gilt auch: nicht unterstützte Kombination → kein improvisierter Generator | | ✅ |
| R043 | S#VERBOTEN (Z. 150) | Anlegen ohne bestätigten Plan | KEEP | S#VERBOTEN | | | ✅ |
| R044 | S#VERBOTEN (Z. 151) | Projekt zweimal anlegen | KEEP | S#VERBOTEN | | | ✅ |
| R045 | S#VERBOTEN (Z. 152) | Dateien in Geschützt anlegen/ändern/löschen | MERGE | S#VERBOTEN | R020 bleibt zusätzlich hier | | ✅ sinngemäß |
| R046 | S#VERBOTEN (Z. 153) | GitHub ohne Auswahlfrage oder gegen Push-Policy | KEEP | S#VERBOTEN | | | ✅ |
| R047 | S#VERBOTEN (Z. 154) | Geheimnisse in Dateien, Befehlen, Commits | KEEP | S#VERBOTEN | | | ✅ |
| R048 | S#VERBOTEN (Z. 155) | Pfad, Owner oder Stack raten | KEEP | S#VERBOTEN | | | ✅ |
| R049 | S#VERBOTEN (Z. 156) | Fachlogik schreiben – Gerüst endet mit lauffähiger Minimalfassung | REWRITE | S#VERBOTEN | Grenzregel R003 | | ✅ sinngemäß |
| R050 | S#VERBOTEN (Z. 157) | Bestehendes Repo: vorhandenen Text der CLAUDE.md überschreiben oder entfernen | KEEP | S#VERBOTEN | | | ✅ |
| R051 | S#VERWEIS (Z. 161–166) | Verweise: github.md, Stack-References, skill-profile-v1, Nachbarskills, Cowork über cc-steuerung | KEEP | S#VERWEIS | dazu generator.md, grundsatz.md | | ✅ |
| R052 | P#Kopf | Stack-Reference für neue Python-Projekte; Code-Regeln bei code-erstellen; neben HA zusätzlich home-assistant.md | KEEP | P | | | ✅ |
| R053 | P#Arten | Werkzeug / Bibliothek / Dienst mit Grunddateien | KEEP | P#Arten | Generator-Pilot nur Werkzeug | | ✅ |
| R054 | P#Grunddateien | pyproject.toml mit Name, Version, requires-python, Testwerkzeuge als optionale Abhängigkeiten mit fester Version | REWRITE | P#Grunddateien | kommt aus dem Baustein, Versionen aus `versions.json` | | ✅ sinngemäß |
| R055 | P#Grunddateien | README mit Aufruf und Testbefehl | KEEP | P#Grunddateien | | | ✅ |
| R056 | P#Grunddateien | .gitignore-Einträge für Python | KEEP | P#Grunddateien | | | ✅ |
| R057 | P#Testgerüst | pytest und pytest-xdist mit fester Version, aktuelle Version nachsehen, nicht raten | REWRITE | P#Testgerüst | Versionskatalog des Generators | | ✅ sinngemäß |
| R058 | P#Testgerüst | Befehl `python -m pytest -n auto`; keine Zahl eintragen; Obergrenze `--maxprocesses` auf kleinen Maschinen | KEEP | P#Testgerüst | | | ✅ |
| R059 | P#Testgerüst | Tests schreiben nur in tmp_path | KEEP | P#Testgerüst | | | ✅ |
| R060 | P#Testgerüst | Kein Test beeinflusst einen anderen (tmp_path je Test, Server-DB Kennung je Lauf und Worker) | KEEP | P#Testgerüst | | | ✅ |
| R061 | P#Testgerüst | Gerüst mit grünem Beispieltest (conftest db je Test, test_beispiel) | REWRITE | templates/python-tool, templates/storage-sqlite | Beispiel wird echter Baustein; P verweist darauf | | ✅ sinngemäß |
| R062 | P#Skill-Profil | Profilwerte: Check tests mit Pfad-Mustern, Pre-Commit-Checks, Stacks, Tests | REWRITE | P#Skill-Profil | Generator schreibt sie; dazu Format/Lint-Checks (Ruff) | | ✅ sinngemäß |
| R063 | github.md, stacks/home-assistant.md | alle Regeln | KEEP | unverändert | in diesem Umbau nicht berührt; HA folgt mit P2 | | ✅ |

Neue Regeln (Vorschlag):

| ID | Regelkern | Neu-Ort | Bezug |
|---|---|---|---|
| N001 | Grenze: projekt-anlegen erzeugt technische Funktionsfähigkeit, code-erstellen fachliches Verhalten; beides im Auftrag → erst Gerüst, dann Übergabe | S#Zweck und Grenzen | CGR r1/r2 |
| N002 | Drei Pflichtklärungen (Zweck, Ort, erste Fassung); Technik leitet Claude ab und erklärt sie im Plan | S#1. Klären; references/grundsatz.md | CGR r1 |
| N003 | Grundsatz-Prüfung in drei Ebenen | references/grundsatz.md | CGR r1 |
| N004 | Grundentscheidungen am `Doku.Entscheidungs-Ort` des neuen Projekts | references/grundsatz.md; S#6 | CGR r1/r2 |
| N005 | Unterstützte Kombination → Generator mit Erzeugungsauftrag v1; nur freigegebene, in CI getestete Kombinationen | references/generator.md | CGR r2/r3 |
| N006 | Prepare → Verify (Format/Lint, Tests, Starttest) → Publish; rotes Verify → nichts angelegt, Ursache melden | references/generator.md; S#5 | CGR r2 |
| N007 | Generator fasst bestehende Ziele und erzeugte Projekte nie an; Herkunft in `.projekt-anlegen.json` | references/generator.md; S#VERBOTEN | CGR r2/r3 |
| N008 | ci-github bei GitHub-Repos standardmäßig | references/generator.md | CGR r2 |
| N009 | claude.ai: nur Plan, keine behauptete Erzeugung, keine improvisierten Vorlagen | references/generator.md | CGR r1/r3 |
| N010 | Nur die benötigte Datenbank, Schema-Version ab Tag 1, kein Migrationsframework auf Vorrat | references/grundsatz.md; Bausteine | CGR r1 |
| N011 | Auftrag in den Scratchpad, nie ins Projekt; `slug`/`package` leitet Claude aus dem Namen ab | references/generator.md#Aufruf, #Erzeugungsauftrag | Schritt 6 |
| N012 | Bei Rot: nichts angelegt, Phase/Schritt/Ursache nennen; nie mit abgeschalteter Prüfung wiederholen | references/generator.md#Ergebnis und Fehler | Schritt 6 |
| N013 | Vorlagen pflegen: UTF-8 ohne BOM, LF, feste Platzhalter, Versionen nur in versions.json, validate und CI vor jedem Commit, neue Kombination erst nach grüner CI | references/generator.md#Pflege der Vorlagen | CGR r3 |
| N014 | Anbindung eines vorhandenen Systems gehört in die Grundentscheidungen | SKILL.md#2. Bestand prüfen | CGR r1 |

## DROP-Gruppen

Keine. Keine Regel entfällt.

## Verweise von außen

| Stelle | Verweis | wann / wohin |
|---|---|---|
| `INDEX.md` Konfliktpaar projekt-anlegen ↔ code-erstellen | „neues Projekt … → projekt-anlegen; Änderung im bestehenden Projekt → code-erstellen“ | Schritt 6, neuer Text nach CGR r2 |
| `skills/code-erstellen/SKILL.md` | neue Regel: Grundentscheidungen am `Doku.Entscheidungs-Ort` lesen | Schritt 6 (eigener Safe Patch) |
| `skills/skill-pflege/references/delivery.md` | claude.ai-Zip ohne `scripts/` und `templates/` | Schritt 6 |
| `quality/evals/projekt-anlegen-*` | 7 Fälle unverändert, 10 neue | Schritt 6/7 |
| `.github/workflows/` | neuer Workflow `test-project-generator.yml` | Schritt 4/5 |

## Prüfung

- **Alt→Neu:** 63 von 63 IDs mit Zustand; Regelkern jeder KEEP-, MOVE-, REWRITE- und MERGE-Zeile im neuen Text
  gefunden (Suche per Skript, 09.10.2026).
- **Neu→Alt:** normative Aussagen in `SKILL.md`, `references/generator.md`, `references/grundsatz.md` und
  `references/stacks/python.md` gesichtet; vier ohne Zuordnung als N011–N014 nachgetragen, keine ungewollte.
- **Description:** 839 Zeichen (vorher 1020).
- **Prüfskript:** GitHub Actions nach dem Push (auf dem Pi kein PowerShell).
- **Routing-Eval:** offen (Schritt 7, 17 Fälle).
