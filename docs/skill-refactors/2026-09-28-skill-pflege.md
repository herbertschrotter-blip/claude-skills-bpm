# Regel-Inventar – skill-pflege – 2026-09-28

Refactor von skill-pflege in Umbau-Phase 4 (`docs/skillsystem-umbau.md`). Vorgaben: CGR-2026-09-24-skillsystem r2 §7.
Vorgesammelt mit `tools/validate-skills.ps1 -Skill skill-pflege -RuleInventory …` (92 Kandidaten), danach nach Urteil zu
Regeln zusammengefasst; jeder Kandidat ist in einer Zeile unten enthalten.

- Skill: skill-pflege
- Stand vorher: 94f06d0 (SKILL.md, 628 Zeilen, Körper 614, keine references)
- Quellen: SKILL.md

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | Zweck · Grundsätze · Modus wählen · Safe Patch · Refactor · Description ändern · Split-Prüfung · Abschluss · Auffälligkeiten melden · VERBOTEN · VERWEIS |
| `references/rule-inventory.md` | Datei · Was als Regel zählt · Spalten · Zustände · Vorsammeln · Freigabe der DROP-Zeilen · Prüfung in beide Richtungen · Verweise · Beispiel |
| `references/delivery.md` | Reihenfolge · Was geliefert wird · Claude Code · Ein Skill je Antwort · Cowork |

Abkürzungen im Neu-Ort: `S` = `SKILL.md`, `I` = `references/rule-inventory.md`, `D` = `references/delivery.md`.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#Frontmatter (Z. 1–14) | name und description | KEEP | S#Frontmatter | unverändert (Entscheidung Herbert) | | ✅ |
| R002 | SKILL.md#Zweck (Z. 20) | Ändert bestehende Skills, ohne den Originaltext zu beschädigen | REWRITE | S#Zweck | „ohne dass Regeln unbemerkt verloren gehen“ | | ✅ sinngemäß |
| R003 | SKILL.md#Zweck (Z. 22) | Default additiv: Skill wird größer, nie kleiner; nur Präzisierungen | DROP | | durch Safe Patch/Refactor ersetzt | Gruppe B | ✅ entfällt |
| R004 | SKILL.md#Zweck (Z. 24–29) | Zwei Umgebungen: Cowork view/DC/Artifact, Claude Code Read/Edit im Repo (Pfad aus Tracker-Profil), SendUserFile | REWRITE | S#Zweck; D#Cowork | Tracker-Profil gibt es nicht mehr → Skill-Repo, sonst Pfad erfragen | | ✅ sinngemäß |
| R005 | SKILL.md#VERBINDLICHE REGEL: Auswahlfrage (Z. 33–37) | Jede Entscheidungsfrage mit festen Optionen als Auswahlfrage, keine Prosa | REWRITE | S#Grundsätze | Umbau-Regel „Fragen nur bei offener Entscheidung“ | | ✅ sinngemäß |
| R006 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 43) | Nächsten Skill updaten? → Auswahlfrage | MERGE | D#Ein Skill je Antwort | R050 | | ✅ sinngemäß |
| R007 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 44) | Löschen eines Abschnitts → Auswahlfrage | MERGE | I#Freigabe der DROP-Zeilen | R051 | | ✅ sinngemäß |
| R008 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 45) | Tippfehler im Original → Auswahlfrage | MERGE | S#Safe Patch | R054 | | ✅ sinngemäß |
| R009 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 46) | Redundanz erkannt → Auswahlfrage | MERGE | S#Grundsätze; I#Was als Regel zählt | R052 | | ✅ sinngemäß |
| R010 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 47) | Struktur-Konflikt → Auswahlfrage alt/neu/Mischform | MERGE | S#Refactor | Zielstruktur wird gezeigt und freigegeben | | ✅ sinngemäß |
| R011 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 48) | Skill-Version angeben? → Auswahlfrage | MERGE | S#Description ändern | R024 | | ✅ sinngemäß |
| R012 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 49) | Welcher Skill? → Auswahlfrage mit den Ordnern unter skills/ | REWRITE | S#Grundsätze | | | ✅ sinngemäß |
| R013 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 50) | Split-Prüfung schlägt an → Auswahlfrage | MERGE | S#Split-Prüfung | R057 | | ✅ sinngemäß |
| R014 | SKILL.md#Diese Fragen IMMER als Auswahlfrage (Z. 51) | description über 1024 Zeichen → Auswahlfrage mit Kürzungsvorschlag | MERGE | S#Description ändern | R023 | | ✅ sinngemäß |
| R015 | SKILL.md#Prosa-Fragen NUR wenn (Z. 53–57) | Prosa nur bei offener Frage, gezeigter Präferenz, Erklärung | MERGE | S#Grundsätze | R005 | | ✅ sinngemäß |
| R016 | SKILL.md#1. Original zeilengenau übernehmen (Z. 63–70) | Bestehenden Text wörtlich übernehmen (Zeichensetzung, Absätze, Überschriften, Listen, Code) | REWRITE | S#Safe Patch | gilt außerhalb des Umfangs eines Safe Patch; Refactor über Inventar | | ✅ sinngemäß |
| R017 | SKILL.md#2. Nichts löschen ohne explizite Freigabe (Z. 72–80) | Nichts löschen ohne Freigabe; Redundanz kann Absicht sein | REWRITE | S#Grundsätze; S#Safe Patch | Refactor: DROP nur mit Freigabe | | ✅ sinngemäß |
| R018 | SKILL.md#3. Nichts kürzen ohne Freigabe (Z. 82–84) | Nichts kürzen ohne Freigabe | REWRITE | S#Safe Patch | nur noch im Safe Patch | | ✅ sinngemäß |
| R019 | SKILL.md#4. Nichts umformulieren ohne Freigabe (Z. 86–90) | Nichts umformulieren ohne Freigabe; Ausnahme echter Tippfehler per Auswahlfrage | REWRITE | S#Safe Patch | Refactor: REWRITE mit Prüfung „sinngemäß“ | | ✅ sinngemäß |
| R020 | SKILL.md#4. Nichts umformulieren ohne Freigabe (Z. 92–95) | Zweite Ausnahme: beim Neutralisieren wesentliche Teile umbauen | DROP | | Neutralisieren ist jetzt ein Refactor | Gruppe B | ✅ entfällt |
| R021 | SKILL.md#5. Struktur/Reihenfolge nicht ändern (Z. 97–99) | Struktur und Reihenfolge nicht ändern | REWRITE | S#Safe Patch | nur noch im Safe Patch | | ✅ sinngemäß |
| R022 | SKILL.md#6. Frontmatter nicht anfassen (Z. 105–107) | Frontmatter nur auf ausdrückliche Anweisung ändern | REWRITE | S#Description ändern | „wenn der Auftrag es verlangt oder sich Auslöser oder Zuständigkeit ändern“ | | ✅ sinngemäß |
| R023 | SKILL.md#6. Frontmatter nicht anfassen (Z. 109–112) | description höchstens 1024 Zeichen, vor Lieferung messen, sonst Auswahlfrage | REWRITE | S#Description ändern; D#Was geliefert wird | Anlass (Datum) entfällt | | ✅ sinngemäß |
| R024 | SKILL.md#7. Versions-Info im Frontmatter ist optional (Z. 114–116) | Keine Versions-Suffixe in Name oder Datei | REWRITE | S#Description ändern | | | ✅ sinngemäß |
| R025 | SKILL.md#8. Neue Abschnitte am Anfang oder Ende einfügen (Z. 118–123) | Neues nicht mittendrin; globale Regeln nach Zweck, VERBOTEN ans Ende, Beispiele im Kontext | REWRITE | S#Safe Patch | „dort, wo ihr Thema steht; neue VERBOTEN-Punkte ans Ende“ | | ✅ sinngemäß |
| R026 | SKILL.md#9. Inline-Änderungen nur punktuell (Z. 125–127) | Inline nur die eine Zeile ändern, nicht den Absatz | MERGE | S#Safe Patch | R016 | | ✅ sinngemäß |
| R027 | SKILL.md#10. Diff-Report nach jedem Update (Z. 129–138) | Diff-Bericht: unverändert, neu, geändert, gelöscht, description-Länge, Dateiliste, Version und Commit | REWRITE | S#Abschluss | gelöscht → mit Inventar-ID | | ✅ sinngemäß |
| R028 | SKILL.md#11. Immer Original lesen VOR Änderung (Z. 144–153) | Vor der Änderung vollständig aus dem Repo lesen, nicht aus Gedächtnis oder geladener Kopie | REWRITE | S#Grundsätze; D#Cowork | | | ✅ sinngemäß |
| R029 | SKILL.md#12. Two-Place-Pflege (Z. 155–160) | Jede Änderung lebt im Repo und in der Lieferung an den Nutzer | MOVE | D (Einleitung) | | | ✅ |
| R030 | SKILL.md#12. Two-Place-Pflege (Z. 162) | Erst Repo inkl. CHANGELOG/INDEX/Commit, dann Lieferung | MOVE | D#Reihenfolge | | | ✅ |
| R031 | SKILL.md#12a. CHANGELOG, INDEX und Commit (Z. 164–171) | CHANGELOG-Eintrag, INDEX bei geänderter Zuständigkeit, Commit und Push; sonst nicht fertig | REWRITE | S#Abschluss | Werte aus dem Skill-Profil | | ✅ sinngemäß |
| R032 | SKILL.md#12a. CHANGELOG, INDEX und Commit (Z. 173) | Keine Download-Datei unter /mnt/user-data/outputs; kein present_files; Artifact ersetzt beides | REWRITE | D#Cowork | „kein present_files“ widersprach R041 und entfällt; bleibt: keine zusätzliche Download-Datei | | ✅ sinngemäß |
| R033 | SKILL.md#13. Dateiname immer exakt SKILL.md (Z. 175–177) | Datei heißt exakt SKILL.md | MOVE | D#Was geliefert wird | | | ✅ |
| R034 | SKILL.md#13. Dateiname immer exakt SKILL.md (Z. 179–182) | Mit references: Zip mit SKILL.md + references/; Nutzer ersetzt alle Dateien, Dateizahl prüfen; ohne references genügt SKILL.md | MOVE | D#Was geliefert wird | | | ✅ |
| R035 | SKILL.md#13a. Artifact-Dateiname (Z. 184–201) | Artifact-Datei exakt SKILL.md, sonst kein Button; Beispiele richtig/falsch | MERGE | D#Cowork | R033; Issue-Nummer entfällt | | ✅ sinngemäß |
| R036 | SKILL.md#13a. Artifact-Dateiname (Z. 203) | Name allein reicht nicht; present_files direkt danach | MERGE | D#Cowork | R041 | | ✅ sinngemäß |
| R037 | SKILL.md#13b. Ein Skill-Artifact pro Antwort (Z. 205–218) | Höchstens eine Skill-Lieferung je Antwort (ein Container-Platz); Repo-Edits mehrerer Skills erlaubt, Lieferungen nacheinander | REWRITE | D#Ein Skill je Antwort; D#Cowork | Issue-Nummer entfällt | | ✅ sinngemäß |
| R038 | SKILL.md#13b. Ein Skill-Artifact pro Antwort (Z. 220–222) | Beispiel Teil 31 / v0.17.11 | DROP | | Historie | Gruppe A | ✅ entfällt |
| R039 | SKILL.md#Mehrere Skills in einer Session (Z. 224–228) | Je Skill eigener Antwortblock, ein Artifact, Trennung über Antworttext | MERGE | D#Ein Skill je Antwort | R037 | | ✅ sinngemäß |
| R040 | SKILL.md#14. Artifact mit vollständigem Skill-Inhalt (Z. 230–232) | Lieferung enthält die vollständige Datei, nicht den Diff | MOVE | D#Was geliefert wird | | | ✅ |
| R041 | SKILL.md#14. Artifact mit vollständigem Skill-Inhalt (Z. 234–241) | Cowork: create_file + present_files direkt hintereinander | MOVE | D#Cowork | | | ✅ |
| R042 | SKILL.md#14a. Artifact-Separation (Z. 243–261) | Keine Auswahlfrage im selben Antwortblock wie eine Lieferung; Antwort endet mit der Lieferung | REWRITE | D#Claude Code; D#Cowork; S#VERBOTEN | Issue-Nummer entfällt | | ✅ sinngemäß |
| R043 | SKILL.md#14b. Artifact-Pflicht nach Skill-Commit (Z. 263–270) | Nach jedem Skill-Commit Lieferung in derselben oder nächsten Antwort, sonst bleibt der alte Stand aktiv | REWRITE | D (Einleitung); S#Abschluss; S#VERBOTEN | | | ✅ sinngemäß |
| R044 | SKILL.md#14b. Artifact-Pflicht nach Skill-Commit (Z. 272–276) | Auslöser: tracker done auf Skill-Aufgabe, direkte Änderung, Commit im Format | MERGE | S#Abschluss | R043 (jede Skill-Änderung endet mit Lieferung) | | ✅ sinngemäß |
| R045 | SKILL.md#14b. Artifact-Pflicht nach Skill-Commit (Z. 278–280) | Ausnahme: Commit ohne Inhaltsänderung | MOVE | D#Was geliefert wird | | | ✅ |
| R046 | SKILL.md#14b. Artifact-Pflicht nach Skill-Commit (Z. 282–284) | Auch reine references-Änderungen brauchen eine Zip-Lieferung | REWRITE | D#Was geliefert wird | Datum entfällt | | ✅ sinngemäß |
| R047 | SKILL.md#14b. Artifact-Pflicht nach Skill-Commit (Z. 286–293) | Reihenfolge Repo → CHANGELOG/Commit → Lieferung → Antwort beenden | MERGE | D#Reihenfolge | R030 | | ✅ sinngemäß |
| R048 | SKILL.md#14b. Artifact-Pflicht nach Skill-Commit (Z. 295–299) | Mehrere Skill-Commits: je Skill eine Lieferung in eigener Antwort, Bestätigung | MERGE | D#Ein Skill je Antwort | R037 | | ✅ sinngemäß |
| R049 | SKILL.md#15. Nach Speicher-Bestätigung erst weiter (Z. 301–303) | Nach „gespeichert“ erst weiter | MOVE | D#Ein Skill je Antwort | | | ✅ |
| R050 | SKILL.md#16. Immer Skill für Skill (Z. 305–315) | Skill für Skill; nach „gespeichert“ Auswahlfrage, ob der nächste drankommt | REWRITE | S#Grundsätze; D#Ein Skill je Antwort | | | ✅ sinngemäß |
| R051 | SKILL.md#17. Explizite Freigabe per Auswahlfrage (Z. 319–330) | Löschen nur mit Freigabe per Auswahlfrage (löschen/deprecated/umformulieren/abbrechen) | REWRITE | I#Freigabe der DROP-Zeilen | Sammelfreigabe je Gruppe statt je Abschnitt | | ✅ sinngemäß |
| R052 | SKILL.md#18. Nie stillschweigend löschen (Z. 332–334) | Nie still löschen, auch Duplikate nicht | REWRITE | S#Grundsätze; I#Was als Regel zählt | Duplikate als MERGE | | ✅ sinngemäß |
| R053 | SKILL.md#19. Eigenständig bleiben (Z. 340–342) | Jeder Skill vollständig lesbar; Querverweise nur als Zusatz | REWRITE | S#Grundsätze | „Self-contained contract, not duplicated implementation“ | | ✅ sinngemäß |
| R054 | SKILL.md#20. Ausnahme für Tippfehler (Z. 344–351) | Echter Tippfehler → Auswahlfrage korrigieren/lassen | MERGE | S#Safe Patch | R019 | | ✅ sinngemäß |
| R055 | SKILL.md#21. Split-Prüfung (Z. 355–367) | Bei jeder Änderung Split prüfen (Größe, ein Befehl/eine Umgebung/ein Stack, Projektwerte, Wiederholung) | REWRITE | S#Split-Prüfung | Maßstab jetzt `docs/skill-quality.md` (unter 500 Zeilen) statt „zwei von fünf Punkten“ | | ✅ sinngemäß |
| R056 | SKILL.md#21. Split-Prüfung (Z. 358) | Anlass und Vorbilder (Herbert, Datum) | DROP | | Historie | Gruppe A | ✅ entfällt |
| R057 | SKILL.md#21. Split-Prüfung (Z. 369–377) | Muster Kern/references; Befund nennen, Auswahlfrage, verschieben statt neu schreiben, verlinken, Zip; nie ohne Freigabe | REWRITE | S#Split-Prüfung | Aufteilen ist ein Refactor | | ✅ sinngemäß |
| R058 | SKILL.md#Schritt 1 — Skill identifizieren (Z. 383–386) | Skill unklar → Auswahlfrage mit Ordnerliste | MERGE | S#Grundsätze | R012 | | ✅ sinngemäß |
| R059 | SKILL.md#Schritt 2 — Original laden (Z. 388–395) | Komplett lesen, Split-Prüfung mitlaufen lassen | MERGE | S#Safe Patch; S#Refactor | R028, R055 | | ✅ sinngemäß |
| R060 | SKILL.md#Schritt 3 — Änderungs-Plan ausarbeiten (Z. 397–403) | Plan: unverändert, neu, inline, gelöscht | REWRITE | S#Safe Patch | im Refactor ist das Inventar der Plan | | ✅ sinngemäß |
| R061 | SKILL.md#Schritt 4 — User-Freigabe für den Plan (Z. 405–413) | Bei mehr als 1–2 Zeilen Plan per Auswahlfrage freigeben | REWRITE | S#Safe Patch | | | ✅ sinngemäß |
| R062 | SKILL.md#Schritt 5 — Repo-Datei editieren (Z. 415–424) | Direkt im Repo ändern; viele Stellen per Patch-Skript, das bei fehlendem Originaltext abbricht | REWRITE | S#Safe Patch; D#Cowork | | | ✅ sinngemäß |
| R063 | SKILL.md#Schritt 5 — Repo-Datei editieren (Z. 426) | Absolute Pfade; danach description-Länge messen | REWRITE | D#Cowork; S#Description ändern | | | ✅ sinngemäß |
| R064 | SKILL.md#Schritt 5a — CHANGELOG, INDEX, Commit, Push (Z. 428–431) | Commit-Format, CHANGELOG, INDEX | MERGE | S#Abschluss | R031 | | ✅ sinngemäß |
| R065 | SKILL.md#Schritt 6 — Lieferung (Z. 433–437) | Claude Code: SendUserFile, Zip aus Repo-Stand nach Commit, Caption, keine Auswahlfrage | MOVE | D#Claude Code | | | ✅ |
| R066 | SKILL.md#Schritt 6 — Lieferung (Z. 439–457) | Cowork: Artifact-Paar, Dateiname exakt | MERGE | D#Cowork | R041 | | ✅ sinngemäß |
| R067 | SKILL.md#Schritt 7 — Diff-Report im Chat (Z. 459–461) | Diff-Bericht zeigen | MERGE | S#Abschluss | R027 | | ✅ sinngemäß |
| R068 | SKILL.md#Schritt 8 — Auf Speicher-Bestätigung warten (Z. 463–465) | Nicht weiter vor „gespeichert“ | MERGE | D#Ein Skill je Antwort | R049 | | ✅ sinngemäß |
| R069 | SKILL.md#Schritt 9 — Batch: nächster Skill (Z. 467–472) | Auswahlfrage für den nächsten Skill | MERGE | D#Ein Skill je Antwort | R050 | | ✅ sinngemäß |
| R070 | SKILL.md#BEISPIEL-WORKFLOW (Z. 476–496) | Beispielablauf im Cowork-Chat | DROP | | wiederholt den Ablauf, keine eigene Vorgabe | Gruppe C | ✅ entfällt |
| R071 | SKILL.md#AUTO-ISSUE-ERKENNUNG (Z. 500–503) | Proaktiv erkannte Auffälligkeiten melden und Issue vorschlagen | REWRITE | S#Auffälligkeiten melden | Issue-Nummer entfällt | | ✅ sinngemäß |
| R072 | SKILL.md#Trigger für Auto-Issue-Erkennung (Z. 505–515) | Auslöser: Widerspruch zu Nutzer-Anweisung oder anderem Skill, tote Verweise, veraltete Pfade/IDs, Werkzeug-/Projektbindung, Split-Kandidat, Über-/Unterauslösen | REWRITE | S#Auffälligkeiten melden | | | ✅ sinngemäß |
| R073 | SKILL.md#Ablauf bei Trigger-Erkennung (Z. 517–535) | Kurz informieren, Auswahlfrage „Issue anlegen?“, bei Ja tracker issue | REWRITE | S#Auffälligkeiten melden | Hinweis auf tracker-Interna entfällt | | ✅ sinngemäß |
| R074 | SKILL.md#Was NICHT auslöst (Z. 537–542) | Nicht melden: Tippfehler, Stil, aktive Änderung des Nutzers, nie gewünschte Funktionen | REWRITE | S#Auffälligkeiten melden | | | ✅ sinngemäß |
| R075 | SKILL.md#Abgrenzung (Z. 546) | Erkennen ≠ Anlegen; nie ungefragt anlegen | REWRITE | S#Auffälligkeiten melden | | | ✅ sinngemäß |
| R076 | SKILL.md#Abgrenzung (Z. 547) | Abgrenzung zum Review-Workflow von tracker | DROP | | Erklärung über einen anderen Skill, keine Vorgabe | Gruppe C | ✅ entfällt |
| R077 | SKILL.md#MEMORY-CLEANUP (Z. 551–570) | Memory-Eintrag, den eine Änderung erledigt: hinweisen, Auswahlfrage, erst dann entfernen | REWRITE | S#Auffälligkeiten melden; D#Cowork | | | ✅ sinngemäß |
| R078 | SKILL.md#Wichtig (Z. 574–577) | Cleanup kein eigener Auslöser; nie still entfernen | MERGE | S#Auffälligkeiten melden | R077 | | ✅ sinngemäß |
| R079 | SKILL.md#Wichtig (Z. 578–580) | Gilt nur für die vier Memory-Rubriken; andere Einträge sind dauerhafte Konventionen | MOVE | D#Cowork | | | ✅ |
| R080 | SKILL.md#Abgrenzung (Z. 582–586) | Abgrenzung Memory-Cleanup zu Regel 17/18 | DROP | | Erklärung mit alten Nummern, keine Vorgabe | Gruppe C | ✅ entfällt |
| R081 | SKILL.md#MEMORY-CLEANUP (Z. 588) | Rubriken-Konvention in MEMORY-RUBRIKEN.md | MOVE | D#Cowork | | | ✅ |
| R082 | SKILL.md#MEMORY-CLEANUP (Z. 590) | „Adressiert Phase 4.3“ | DROP | | Historie | Gruppe A | ✅ entfällt |
| R083 | SKILL.md#VERBOTEN (Z. 596) | Skills aus dem Gedächtnis neu schreiben | REWRITE | S#VERBOTEN | ergänzt: „oder aus der geladenen Kopie“ | | ✅ sinngemäß |
| R084 | SKILL.md#VERBOTEN (Z. 597) | Mehrere Skills parallel in einer Antwort erstellen | MERGE | S#VERBOTEN | R037 | | ✅ sinngemäß |
| R085 | SKILL.md#VERBOTEN (Z. 598) | Zwei Skill-Artifacts in einer Antwort | MERGE | S#VERBOTEN; D#Cowork | R037 | | ✅ sinngemäß |
| R086 | SKILL.md#VERBOTEN (Z. 599) | Originalinhalte still entfernen, kürzen, zusammenfassen | REWRITE | S#VERBOTEN | Safe Patch: gar nicht; Refactor: nur freigegebene DROP-Zeile | | ✅ sinngemäß |
| R087 | SKILL.md#VERBOTEN (Z. 600) | Stilistische Verbesserungen ohne Freigabe | MERGE | S#Safe Patch | R016 | | ✅ sinngemäß |
| R088 | SKILL.md#VERBOTEN (Z. 601) | Umformulieren ohne Freigabe | MERGE | S#Safe Patch | R019 | | ✅ sinngemäß |
| R089 | SKILL.md#VERBOTEN (Z. 602) | Frontmatter ohne Anweisung ändern | MERGE | S#Description ändern | R022 | | ✅ sinngemäß |
| R090 | SKILL.md#VERBOTEN (Z. 603) | Versions-Suffixe im Dateinamen | MERGE | S#Description ändern; D#Was geliefert wird | R024 | | ✅ sinngemäß |
| R091 | SKILL.md#VERBOTEN (Z. 604) | Ohne Auswahlfrage zum nächsten Skill wechseln | MERGE | S#VERBOTEN | R050 | | ✅ sinngemäß |
| R092 | SKILL.md#VERBOTEN (Z. 605) | Diff-Bericht weglassen | MERGE | S#Abschluss | R027 | | ✅ sinngemäß |
| R093 | SKILL.md#VERBOTEN (Z. 606) | Prosa-Fragen bei festen Optionen | MERGE | S#Grundsätze | R005 | | ✅ sinngemäß |
| R094 | SKILL.md#VERBOTEN (Z. 607) | Auswahlfrage im selben Block wie die Lieferung | REWRITE | S#VERBOTEN | Issue-Nummer entfällt | | ✅ sinngemäß |
| R095 | SKILL.md#VERBOTEN (Z. 608) | Skill-Commit ohne Lieferung | REWRITE | S#VERBOTEN | | | ✅ sinngemäß |
| R096 | SKILL.md#VERBOTEN (Z. 609) | Skill mit references nur als SKILL.md liefern | KEEP | S#VERBOTEN | | | ✅ |
| R097 | SKILL.md#VERBOTEN (Z. 610) | description über 1024 Zeichen liefern | REWRITE | S#VERBOTEN | ergänzt: ohne Routing-Eval ändern | | ✅ sinngemäß |
| R098 | SKILL.md#VERBOTEN (Z. 611) | Ohne CHANGELOG-Eintrag und Commit liefern | REWRITE | S#VERBOTEN | | | ✅ sinngemäß |
| R099 | SKILL.md#VERBOTEN (Z. 612) | Splitten ohne Freigabe oder dabei neu formulieren | REWRITE | S#Split-Prüfung | Aufteilen ist ein Refactor; Umformulieren dort als REWRITE mit Prüfung | | ✅ sinngemäß |
| R100 | SKILL.md#VERBOTEN (Z. 613) | create_file ohne direkt folgendes present_files | MOVE | D#Cowork | | | ✅ |
| R101 | SKILL.md#VERBOTEN (Z. 614) | Memory-Einträge still entfernen | REWRITE | S#VERBOTEN | | | ✅ sinngemäß |
| R102 | SKILL.md#VERWEIS (Z. 619–627) | Neuer Skill → skill-neu; Faustregel „gibt es die SKILL.md schon?“ | REWRITE | S#VERWEIS | | | ✅ sinngemäß |
| N001 | – | Zwei Modi, Wahl nach Art der Änderung, nicht nach Größe | NEW | S#Modus wählen | r2 §7 | | ✅ |
| N002 | – | Muss im Safe Patch Text wegfallen oder wandern → Refactor | NEW | S#Modus wählen | r2 §7 | | ✅ |
| N003 | – | Refactor-Ablauf mit Inventar, Freigabe vor dem Schreiben, Prüfung in beide Richtungen | NEW | S#Refactor; S#VERBOTEN; I | r2 §7 | | ✅ |
| N004 | – | Inventar: Datei, Spalten, Zustände, was als Regel zählt | NEW | I | r2 §7 | | ✅ |
| N005 | – | Kandidaten per Prüfskript vorsammeln | NEW | S#Refactor; I#Vorsammeln | r2 §7 | | ✅ |
| N006 | – | Verweise über Datei#Überschrift; nicht angepasste Verweise von außen im Inventar vermerken | NEW | S#Grundsätze; S#VERBOTEN; I#Verweise | `docs/skill-quality.md` | | ✅ |
| N007 | – | Maßstab `docs/skill-quality.md`, Werte aus dem Skill-Profil | NEW | S#Zweck | r3 | | ✅ |
| N008 | – | Abschluss: Prüfskript ohne neue Fehler, Routing-Eval vor dem Upload | NEW | S#Abschluss | Skill-Profil | | ✅ |
| N009 | – | Nach Description-Änderung Routing-Eval Pflicht, bei Konfliktpaar mit Anthropic-Skill echte Sitzung | NEW | S#Description ändern | `docs/skill-quality.md` | | ✅ |
| N010 | – | Sitzung nicht im Skill-Repo → nach dem Pfad fragen | NEW | S#Zweck | ersetzt Tracker-Profil (R004) | | ✅ |
| N011 | – | Description-Schema: was, Use when, Do not trigger for; Projekte nur als Beispiel | NEW | S#Description ändern | `docs/skill-quality.md`, Aufbau | | ✅ |
| N012 | – | Im Repo entfernte Dateien löscht der Nutzer auch bei claude.ai | NEW | D#Was geliefert wird | ergänzt R034 | | ✅ |
| N013 | – | Zip im Scratchpad aus dem Stand nach dem Commit bauen und ihren Inhalt vor dem Senden auflisten | NEW | D#Claude Code | ergänzt R065 | | ✅ |
| N014 | – | Jede Reference direkt aus SKILL.md verlinkt; über 100 Zeilen mit Inhaltsverzeichnis | NEW | S#Split-Prüfung | `docs/skill-quality.md`, Aufbau | | ✅ |

## DROP-Gruppen

- **Gruppe A – Historie** (Daten, Sitzungen, Anlässe, Phasen): R038, R056, R082. Die Issue-Nummern in Überschriften
  (skill-pflege-003 … -007) entfallen innerhalb der REWRITE-/MOVE-Zeilen.
- **Gruppe B – durch Safe Patch und Refactor ersetzt:** R003 (additiv, nie kleiner), R020 (Ausnahme Neutralisieren).
- **Gruppe C – Erklärung ohne eigene Vorgabe:** R070 (Beispielablauf Cowork), R076 (Abgrenzung zu tracker), R080
  (Abgrenzung mit alten Nummern).

## Verweise von außen

| Stelle | Verweis | Behandlung |
|---|---|---|
| `skills/doc-pflege/SKILL.md` (Z. 446) | „skill-pflege Regel 21“ | Phase 6 (doc-pflege) → `skills/skill-pflege/SKILL.md#Split-Prüfung` |
| `skills/tracker/references/complete-task.md` (Z. 133–134, 147) | „Regel 14b“, „Regel 14“, „Regel 15 + 16“ | Phase 6 (tracker) → `skills/skill-pflege/references/delivery.md` |
| `skills/skill-neu/SKILL.md` | „Regel 21“, „Regel 14“, „13b, 14a, Regel 6, 13“, Abschnitt AUTO-ISSUE-ERKENNUNG, „additive Default-Philosophie“ (Z. 529) | Phase 4 (skill-neu), gleich im Anschluss |
| `skills/cc-steuerung/SKILL.md` (Z. 292–297) | „`skill-pflege/SKILL.md` Abschnitt 14a/13a“ | Phase 5 (cc-steuerung wird Cowork-Adapter) → `skills/skill-pflege/references/delivery.md#Cowork` |
| `INDEX.md` Skill-Tabelle, Meta-Skills, Invarianten 5 und 8 | additiv; Two-Place über Artifact | mit diesem Commit angepasst |
| `README.md` Two-Place-Pflege, Kapitel 11, `docs/`-Tabelle und Baum | Regelquelle SKILL.md; „Repo + Artifact“ | mit diesem Commit angepasst |

## Prüfung

- **Freigabe:** DROP-Gruppen A, B und C von Herbert am 28.09.2026 freigegeben (je Gruppe eine Auswahlfrage, vor dem
  Schreiben).
- **Alt→Neu:** alle 102 alten IDs mit Zustand (KEEP 2, MOVE 12, MERGE 34, REWRITE 46, DROP 8); jeder Neu-Ort im neuen
  Text gelesen. Dabei gefunden und nachgetragen: zwei Teile von R055/R057 (Kriterium „wächst an derselben Stelle“ und
  das Muster für den Kern) fehlten zunächst in `SKILL.md#Split-Prüfung`.
- **Neu→Alt:** `-RuleInventory` auf den neuen Stand: 55 Kandidaten, alle einer ID oder NEW zugeordnet; dabei N011
  (Description-Schema) nachgetragen.
- **Größe:** SKILL.md 628 → rund 195 Zeilen (Körper 614 → rund 180), dazu `references/rule-inventory.md` und
  `references/delivery.md`; Prüfskript 0 Fehler, Warnungen 6 → 2 (beide aus der unveränderten Description:
  „claude-skills-bpm“).
- **Routing-Eval:** am 28.09.2026 auf 3bbdbe3, `--tag skill-pflege` (11 Fälle × 3 Läufe, `-j 3`): **11 von 11 Fällen,
  33 von 33 Läufen**; alle 7 kritischen Fälle 3/3, beide Negativfälle (`skill-neu-no-trigger-eval-run`,
  `skill-pflege-no-trigger-other-repo`) bestanden. Grundmessung für dieselben Fälle ebenfalls 33/33, also kein
  Rückschritt und kein neuer Konflikt. 16 Läufe endeten an der Grenze von 8 Schritten oder 180 Sekunden, jeweils nach dem
  Skill-Aufruf. Das Ergebnis ändert sich dadurch nicht, gleich wie in der Grundmessung. Dauer 18 Minuten, Gegenwert
  18,64 USD. Freigabe nach `docs/skill-quality.md`, Abschnitt Verhalten: erfüllt.
- **Gegenprüfung** (28.09.2026, zweite Sitzung): Alt→Neu ohne Verlust. Neu→Alt: N012–N014 nachgetragen; diese Sätze
  haben kein Pflichtwort und waren deshalb keine Kandidaten. Behoben mit Safe Patch v0.37.1: Die Routing-Eval steht in
  `SKILL.md#Abschluss` jetzt nach Commit und Push wie in `references/delivery.md#Reihenfolge`, und `SKILL.md#Refactor`
  verlangt die Freigabe der Zielstruktur (R010). README: „additiv“ an zwei Stellen ersetzt. Eine Routing-Eval für
  v0.37.1 entfällt, weil sich Description und Auslöser nicht geändert haben.
