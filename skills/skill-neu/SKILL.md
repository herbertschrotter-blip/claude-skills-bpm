---
name: skill-neu
description: >
  Erstellt komplett neue Skills für das Skills-Repo von Grund auf — projektneutral
  und für Cowork wie Claude Code — inkl. Capture-Intent-Interview, Description-Schema,
  Neutralitäts-Checkliste, Body, Profil-/references/-Aufteilung und strukturiertem
  Test-Prompt-Setup. Use when users want to create a new skill from scratch, design
  a new skill system, draft a SKILL.md for a new use case, or set up test prompts
  for evaluating skill triggering. Do not trigger for changing or extending existing
  skills (use skill-pflege instead), running automated eval scripts, or general
  documentation pflege.
---

# Skill-Neu — neue Skills von Grund auf anlegen

## Zweck

Legt einen komplett neuen Skill im Skill-Repo an. Das hier ist ein Ablauf für das Repo, kein Lehrbuch: Wie man Skills
schreibt, weiß Claude. Hier steht, was dazugehört: Absicht, Kollisionsprüfung, Description, Neutralität, Eval-Fälle,
Prüfung, Commit und Lieferung.

Maßstab für jeden Skill ist `docs/skill-quality.md`, die Werte eines Projekts stehen im Skill-Profil
(`docs/skill-profile-v1.md`). Beide vor dem Schreiben lesen. Einen bestehenden Skill ändert skill-pflege; gibt es die
SKILL.md schon, hier nicht weiterarbeiten.

Die Arbeit läuft im Skill-Repo, also dem Repo mit `skills/<name>/SKILL.md` und `docs/skill-quality.md`. Läuft die
Sitzung in einem anderen Repo, fragt Claude nach dem Pfad zum Skill-Repo und rät ihn nicht. In Claude Code schreibt
Claude die Dateien direkt ins Repo. Was im Cowork-Chat anders ist, steht in `references/cowork.md`.

## Grundsätze

- **Absicht zuerst.** Nie aus dem Gedächtnis schreiben, auch wenn klar scheint, was hinein muss.
- **Fragen nur bei offener Entscheidung.** Was das bisherige Gespräch schon beantwortet („mach daraus einen Skill“),
  daraus ableiten und nur die Lücken fragen. Mit Kontext vorbereitet kommen. Ist etwas offen, dann als Auswahlfrage
  mit konkreten Vorschlägen, z. B. Auslöse-Sätze oder Namen.
- **Eval-Fälle vor dem großen Ausbau.** Erst die Fälle für Auslösen und Nicht-Auslösen, dann den Körper ausbauen.
- **Kurzvertrag statt Kopie.** Jeder Skill macht Zweck, Grenzen, benötigte Werte und Kernregeln selbst klar.
  Detailabläufe darf er verlinken.

## Ablauf

### Absicht klären

Vor dem Schreiben klären:
1. Was soll der Skill können? Welche Aktionen, welches Ergebnis?
2. Wann soll er auslösen? Sätze, Situationen, Stichwörter.
3. Wann nicht? Oft der wichtigste Punkt: Catch-all-Risiken ausdrücklich benennen.
4. Randfälle und Ausgabeform: Datei, Chat-Antwort oder Werkzeugaufruf?
5. Wie weit Evals über das Auslösen hinaus sinnvoll sind: bei objektiv prüfbaren Ergebnissen (feste Abläufe, Formate)
   ja, bei subjektiven (Stil, Kreatives) meist nur das Auslösen.
6. Was ist projekt-, was stackspezifisch? Projektwerte (Pfade, IDs, Listen, Doc-Namen, Befehle, Präfixe) kommen ins
   Skill-Profil der CLAUDE.md oder in eine Config unter `.claude/skill-config/`. Stack- und Sprachdetails kommen in
   `references/<gruppe>/<key>.md`, der Schlüssel steht im Profil. Der Skill selbst bekommt nur die Regel „lies Feld X“
   und gekennzeichnete Beispiele.

Hauptumgebung ist Claude Code; was nur im Cowork-Chat gilt, kommt in eine Reference für Cowork. Skills lohnen sich für
mehrstufige oder spezialisierte Abläufe. Ist die Aufgabe trivial, also ein Schritt, den Claude ohnehin kann, löst ein
Skill unzuverlässig aus. Dann prüfen, ob es ihn überhaupt braucht.

### Kollisionsprüfung

- **Ähnliche Skills:** die Ordner unter `skills/` durchgehen und die Descriptions aller Skills lesen, die in der
  Sitzung geladen sind, auch die von Anthropic (z. B. skill-creator, code-review).
- **Auslöser:** Würde der neue Skill einem anderen Aufträge wegnehmen oder umgekehrt? Dann die Abgrenzung schärfen.
  Jedes Konfliktpaar bekommt einen Eval-Fall. Ein Konflikt mit einem Skill von Anthropic bekommt eine echte Sitzung
  (`quality/real-environment/README.md`), weil `plugin eval` fremde Skills nicht lädt.
- **Name:** nach `docs/skill-quality.md`, Abschnitt Aufbau, und gleich keinem vorhandenen Skill, auch keinem von
  Anthropic. Bei Kollision eine deutsche Variante wählen (Beispiel: skill-neu statt skill-creator). Zwei bis vier
  Namen als Auswahlfrage vorschlagen.
- **Auffälligkeiten:** Fällt dabei an bestehenden Skills etwas auf (Überlappung, tote Verweise, veraltete Pfade oder
  IDs, Widerspruch zu einer Anweisung des Nutzers), kurz hinweisen und per Auswahlfrage ein Skill-Issue anbieten:
  anlegen / später selbst / nicht nötig. Nie ungefragt anlegen. Nicht melden: Tippfehler, Stilunterschiede, was der
  Nutzer gerade selbst ändert, nie gewünschte Funktionen. Ablauf wie in `skills/skill-pflege/SKILL.md`, Abschnitt
  Auffälligkeiten melden.

### Description

- Die Description entscheidet allein darüber, ob der Skill auslöst. Hier liegt die meiste Arbeit.
- Schema: was der Skill tut, „Use when …“, „Do not trigger for …“. Dritte Person, konkrete Stichwörter.
- Eher drängend formulieren, denn Claude neigt dazu, einen passenden Skill nicht zu nutzen. Den Stil (knapp /
  drängend / gemischt) nur fragen, wenn er offen ist.
- Mindestens drei konkrete „Do not trigger“-Fälle. Eine leere Liste ist ein Warnsignal, Catch-all-Risiken gibt es
  fast immer.
- Projekte nur als Beispiel in Klammern, nie als Zuständigkeit („<Projekt>-Skills“).
- Höchstens 1024 Zeichen: die Zeilen des Blocks getrimmt und mit Leerzeichen verbunden. claude.ai lehnt den Upload
  sonst ab. Vor jeder Lieferung messen.
- Der Körper macht nichts, was die Description nicht erwarten lässt.

### Neutralität

Jeder neue Skill erfüllt diese Punkte, bevor er geliefert wird:
- **Handlung statt Werkzeug:** „Auswahlfrage“, „Datei lesen“, „Lieferung an den Nutzer“. Ein MCP-Werkzeug, ohne das
  die Handlung nicht geht, steht voll qualifiziert im Integrationsabschnitt oder in einer Reference.
- **Umgebung:** Der Kern nennt nur die Handlung. Werkzeuge des Cowork-Chats (Desktop Commander, Artifact,
  Memory-Einträge) stehen in einer Reference für Cowork.
- **Keine Projektwerte:** Pfade, IDs, Listen, Präfixe, Doc-Namen und Befehle kommen aus dem Skill-Profil oder einer
  Config.
- **Keine Sprache und kein Stack im Kern:** Details in `references/<gruppe>/<key>.md`.
- **Beispiele gekennzeichnet:** „Beispiel (Projekt): …“ – erkennbar als Muster, nicht als Vorgabe.
- **Fehlende Werte:** Fehlt ein Wert im Skill-Profil, nennt der Skill genau dieses Feld und fragt per Auswahlfrage:
  Profil ergänzen / Wert einmalig nennen / abbrechen (`docs/skill-profile-v1.md`, Abschnitt Fehlende Werte). Nie raten
  und nie ein Projekt annehmen.
- **Memory:** Merker gehören ins Memory der Umgebung, Aufgaben in den Tracker (Cowork: `references/cowork.md`).

Offene Punkte: Auswahlfrage jetzt beheben / bewusst so lassen (Begründung in den Skill) / abbrechen.

### Körper und references

- Imperativ schreiben und erklären, warum eine Regel gilt, statt MUSS zu häufen. MUSS und NIE nur dort, wo
  `docs/skill-quality.md` sie vorsieht.
- Beispiele konkret und als Beispiel gekennzeichnet.
- Aufbau: Frontmatter, Zweck mit Abgrenzung zu den Nachbarn, falls nötig die benötigten Profilfelder mit Fallback,
  Ablauf, VERBOTEN, VERWEIS. Querschnittsregeln wie Fragen, Sprache, Branch und Push nicht kopieren.
- Körper unter 500 Zeilen. Abläufe für einen Befehl, eine Umgebung, eine Integration oder einen Stack kommen in
  `references/`. Mehrere Ausprägungen werden `references/<gruppe>/<key>.md`; der Schlüssel steht im Profil, geladen
  wird nur die genannte Datei. Maßstab: `skills/skill-pflege/SKILL.md`, Abschnitt Split-Prüfung. Ob aufgeteilt wird,
  nur bei offener Entscheidung fragen.
- Jede Reference direkt aus SKILL.md verlinken. Über 100 Zeilen beginnt sie mit einem Inhaltsverzeichnis.
- References eines anderen Skills werden nicht mitgeladen. Braucht der Skill dessen Logik, bekommt er einen
  Kurzvertrag und liest die Details bei Bedarf aus dem Skill-Repo.
- Skripte unter `scripts/` sind in Claude Code nutzbar. Der Skill muss aber auch ohne sie funktionieren.

### Eval-Fälle

- Vor der Freigabe mindestens drei Fälle unter `quality/evals/` nach `quality/README.md`: Auslösen, Nicht-Auslösen bei
  den Catch-all-Risiken und je Konfliktpaar ein Fall, in dem der Nachbar nicht auslösen darf.
- Testsätze sind echte, substanzielle Aufträge (mehrstufig, spezialisiert) und ohne Dateien des Repos verständlich.
  Triviale Sätze lösen auch bei guter Description nicht zuverlässig aus.
- Tags nach `quality/README.md`: der Skillname, dazu `critical` für Grenzen, die nie kippen dürfen. Die Tabellen
  „Verteilung“ und „Fälle“ dort nachziehen.

### Prüfen

1. **Prüfskript** (Check skill-validation im Skill-Profil) mit `-Skill <skill>`: keine Fehler.
2. **Routing-Eval** der neuen Fälle nach dem Commit und vor dem Upload (Check routing-eval im Skill-Profil, dazu
   `--tag <skill>`), drei Läufe je Fall. Schwellen und Freigabe nach `docs/skill-quality.md`, Abschnitt Verhalten.
3. **Echte Sitzung**, wenn es ein Konfliktpaar mit einem Skill von Anthropic gibt (`quality/real-environment/README.md`).
4. **Nachschärfen:** Löst ein Fall zu selten aus, prüfen, ob der Satz zu trivial oder die Description zu schwach ist.
   Dann konkrete Sätze und Synonyme in „Use when“ aufnehmen und drängender formulieren. Löst er falsch aus, die Phrase
   in „Do not trigger for“ aufnehmen und „Use when“ enger fassen. Danach erneut messen.
5. **Nach dem Upload** die reale Nutzung beobachten. Jedes echte Fehlrouting wird ein Eval-Fall.

### Doku, Commit, Lieferung

- Ins Skill-Repo kommen `skills/<name>/SKILL.md` und `references/`, dazu der CHANGELOG-Eintrag, die Zeile in `INDEX.md`
  (Skill-Tabelle und Zuständigkeiten) und die Eval-Fälle, alles im selben Commit. Format, Version (neuer Skill: MINOR)
  und Push-Policy stehen im Skill-Profil.
- Danach liefern, wie skill-pflege es vorgibt (`skills/skill-pflege/references/delivery.md`): erst das Repo, dann die
  Lieferung; die vollständige SKILL.md, bei references eine Zip; ein Skill je Antwort; keine Auswahlfrage im selben
  Antwortblock wie die Lieferung. Der Nutzer lädt bei claude.ai hoch und bestätigt „gespeichert“. Das Repo ist die
  Wahrheit.
- Jede weitere Änderung am neuen Skill, auch das Nachschärfen, läuft über skill-pflege.

## VERBOTEN

- einen Skill aus dem Gedächtnis schreiben, ohne die Absicht geklärt zu haben
- eine Description ohne „Do not trigger for“, mit einem Projekt als Zuständigkeit oder über 1024 Zeichen
- einen Körper, der auf Werkzeuge oder Pfade baut, die die Description nicht erwarten lässt
- Eval-Skripte oder Subagenten erfinden, die es nicht gibt; vorhanden sind `claude plugin eval` und skill-creator
- Aufgaben von skill-pflege übernehmen
- einen Skill ohne Kollisionsprüfung (Auslöser und Name) oder ohne mindestens drei Eval-Fälle freigeben
- liefern, bevor die Neutralität geprüft ist
- ohne CHANGELOG-Eintrag, INDEX-Zeile und Commit liefern, oder committen, ohne zu liefern
- einen Skill mit references nur als SKILL.md liefern
- Aufgaben ins Memory statt in den Tracker legen, neue Memory-Rubriken erfinden oder Einträge ohne Bestätigung entfernen

## VERWEIS

- Bestehenden Skill ändern → skill-pflege. Faustregel: Gibt es die SKILL.md schon, ist skill-pflege zuständig; wird
  die Datei ganz neu angelegt, skill-neu.
- Regeln für Skills: `docs/skill-quality.md`; Skill-Profil: `docs/skill-profile-v1.md`; Eval-Fälle: `quality/README.md`.
- Lieferung: `skills/skill-pflege/references/delivery.md`. Cowork: `references/cowork.md`.
