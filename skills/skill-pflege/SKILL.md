---
name: skill-pflege
description: >
  Ändert und erweitert bestehende Skills im Skills-Repo (claude-skills-bpm),
  ohne deren Originalinhalt ungewollt zu kürzen oder umzuschreiben – aus dem
  Cowork-Chat wie aus Claude Code. Use when users want to ändern,
  erweitern, ergänzen, einbauen, einfügen, schärfen, refactoren,
  aktualisieren, anpassen, präzisieren, korrigieren, or update an existing
  skill — including adding new rules, adjusting trigger wording, refining
  descriptions, fixing typos, updating references, or restructuring
  existing SKILL.md content. Do not trigger for creating a brand new skill
  from scratch (use skill-neu instead), running skill evals, designing a
  new skill system, or changing skills in unrelated repos.
---

# Skill-Pflege — bestehende Skills sicher ändern

## Zweck

Ändert bestehende Skills im Skill-Repo, ohne dass Regeln unbemerkt verloren gehen. Dafür gibt es zwei Modi:

- **Safe Patch**: eine gezielte Änderung, alles andere bleibt wörtlich, wie es ist.
- **Refactor**: kürzen, zusammenführen, verschieben und umbauen. Ein Regel-Inventar zeigt dabei für jede alte Regel,
  wo sie geblieben ist.

Maßstab für jeden Skill ist `docs/skill-quality.md` im Skill-Repo. Commit-Format, Versionsregel, Checks, Push und
Auslieferung stehen im Skill-Profil der `CLAUDE.md`. Einen ganz neuen Skill legt skill-neu an.

Die Arbeit läuft im Skill-Repo, also dem Repo mit `skills/<name>/SKILL.md` und `docs/skill-quality.md`. Läuft die
Sitzung in einem anderen Repo, fragt Claude nach dem Pfad zum Skill-Repo und rät ihn nicht. In Claude Code liest und
ändert Claude die Dateien direkt im Repo und liefert den fertigen Skill als Datei an den Nutzer. Was im Cowork-Chat
anders ist, steht in `references/delivery.md` im Abschnitt Cowork.

## Grundsätze

- **Aus dem Repo arbeiten.** Vor jeder Änderung SKILL.md und alle references des Skills vollständig aus dem Repo lesen.
  Nicht aus der geladenen Kopie arbeiten, die kann älter sein, und nie aus dem Gedächtnis.
- **Nichts geht still verloren.** Eine Regel, die wegfällt, liegt im Safe Patch außerhalb des Umfangs und bleibt
  unberührt, oder sie ist im Refactor eine freigegebene DROP-Zeile. Auch Doppelungen werden nicht still entfernt;
  Redundanz kann Absicht sein.
- **Fragen nur bei offener Entscheidung.** Nur fragen, wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich
  etwas offen ist, und dann als Auswahlfrage. Typische Stellen:
  - welcher Skill gemeint ist (Optionen: die Ordner unter `skills/`)
  - welcher Modus passt
  - Freigabe von DROP-Gruppen
  - Split
  - Description über 1024 Zeichen
  - ein echter Tippfehler im Original
- **Ein Skill nach dem anderen.** Bei mehreren Skills gilt je Skill: ändern, abschließen, liefern. Vor dem nächsten die
  Bestätigung „gespeichert“ abwarten und per Auswahlfrage fragen, ob er drankommt.
- **Eigenständig, aber nicht kopiert.** Jeder Skill macht Zweck, Grenzen, benötigte Werte und Kernregeln selbst klar.
  Detailabläufe darf er verlinken.
- **Verweise über Datei und Überschrift**, z. B. `skills/<skill>/SKILL.md#<Überschrift>`, nie über Nummern wie Regel,
  Kapitel, Modus oder Schritt.

## Modus wählen

| Änderung | Modus |
|---|---|
| eine Regel ergänzen oder korrigieren, Tippfehler, toter Verweis, Description gezielt ändern, kein Umbau | Safe Patch |
| kürzen, zusammenführen, in references verschieben, Struktur ändern, mehrere alte Regeln ersetzen, tote Regeln entfernen | Refactor |

Es entscheidet die Art der Änderung, nicht ihre Größe. Zeigt sich während eines Safe Patch, dass Text wegfallen oder
wandern muss, geht die Arbeit als Refactor weiter. Passt beides, entscheidet eine Auswahlfrage.

## Safe Patch

1. Skill und references aus dem Repo lesen und dabei die Split-Prüfung mitlaufen lassen.
2. Den Umfang genau benennen: welche Regeln, welche Stellen.
3. Nur diese Stellen ändern. Alles außerhalb bleibt wörtlich, in derselben Reihenfolge und Struktur. Dazu gehören
   Zeichensetzung, Absätze, Überschriften, Listen und Codeblöcke. Nicht kürzen, nicht umformulieren und nichts
   nebenbei „verbessern“. Inline nur die betroffene Zeile ändern, nicht den ganzen Absatz. Für einen echten
   Tippfehler außerhalb des Umfangs gibt es eine Auswahlfrage (korrigieren / so lassen).
4. Neue Regeln dort einfügen, wo ihr Thema steht: neue VERBOTEN-Punkte ans Ende der Liste, Beispiele in ihren
   Abschnitt, übergreifende Regeln zu den Grundsätzen.
5. Bei vielen Stellen ein Patch-Skript im Scratchpad benutzen, das bei fehlendem Originaltext abbricht, statt still
   weiterzumachen.
6. Ist die Änderung größer als ein, zwei Zeilen, den Plan zeigen und per Auswahlfrage freigeben lassen. Der Plan nennt:
   was bleibt (Überschriften), was neu kommt (Text), was sich ändert (vorher/nachher), was entfällt (sollte leer sein).
7. Verweise prüfen, die auf die geänderten Stellen zeigen, im Skill und aus anderen Skills.
8. Abschluss (unten).

## Refactor

Ein Refactor darf kürzen, zusammenführen, verschieben und neu formulieren. Abgesichert wird er durch das Regel-Inventar
unter `docs/skill-refactors/<Datum>-<skill>.md`. Format, Zustände und Prüfungen: `references/rule-inventory.md`.

1. Skill und alle references aus dem Repo lesen.
2. Kandidaten vorsammeln: das Prüfskript aus dem Skill-Profil (Check skill-validation) mit
   `-Skill <skill> -RuleInventory docs/skill-refactors/<Datum>-<skill>.md` aufrufen.
3. Das Inventar nach Urteil vervollständigen: jede normative Aussage bekommt eine Zeile, Doppelungen werden als MERGE
   geführt.
4. Die Zielstruktur entwerfen: den Kern in SKILL.md, Abläufe für einen Befehl, eine Umgebung oder einen Stack in
   references.
5. Jeder Zeile einen Zustand (KEEP, MOVE, MERGE, REWRITE, DROP) und einen Neu-Ort geben. Neue Regeln werden als NEW
   geführt.
6. Zielstruktur und DROP-Gruppen mit Begründung zeigen. Die Zielstruktur und jede Gruppe per Auswahlfrage freigeben
   lassen, **bevor** geschrieben wird.
7. Umbauen.
8. Alt→Neu prüfen: Jede alte ID hat einen Zustand, und jeder Neu-Ort ist im neuen Text zu finden.
9. Neu→Alt prüfen: Kandidaten des neuen Stands in eine Datei im Scratchpad erzeugen. Jede normative Aussage gehört zu
   einer ID oder ist NEW.
10. Verweise prüfen, im Skill und aus anderen Skills. Was jetzt nicht mitgeändert wird, kommt im Inventar unter
    „Verweise von außen“.
11. Qualität prüfen nach `docs/skill-quality.md`: Größe, Historie im Regeltext, Umgebungswerkzeuge im Kern, Projektwerte.
12. Abschluss (unten). Inventar und Umbau kommen in denselben Commit; das Eval-Ergebnis wird danach im Inventar
    nachgetragen.

## Description ändern

- Frontmatter nur ändern, wenn der Auftrag es verlangt oder sich Auslöser oder Zuständigkeit ändern.
- Höchstens 1024 Zeichen: die Zeilen des Blocks getrimmt und mit Leerzeichen verbunden. claude.ai lehnt den Upload
  sonst ab. Nach jeder Änderung messen. Liegt sie darüber: Auswahlfrage mit Kürzungsvorschlag.
- Schema: was der Skill tut, „Use when …“, „Do not trigger for …“. Projekte nur als Beispiel, nie als Zuständigkeit.
- Danach ist die Routing-Eval der betroffenen Fälle Pflicht. Hat der Skill ein Konfliktpaar mit einem Skill von
  Anthropic, kommt die passende echte Sitzung dazu (`quality/real-environment/README.md`).
- Keine Versionsangaben in Name, Description oder Dateiname. Die Datei heißt immer `SKILL.md`.

## Split-Prüfung

Bei jeder Änderung kurz prüfen, ob der Schnitt zwischen Kern und references noch stimmt (`docs/skill-quality.md`,
Abschnitt Aufbau):

- SKILL.md-Körper unter 500 Zeilen
- Abläufe, die nur einen Befehl, eine Umgebung, eine Integration oder einen Stack betreffen, liegen in `references/`
- Stellen, die sich je Ausprägung wiederholen, werden eine Datei je Ausprägung (`references/<gruppe>/<key>.md`)
- eine Stelle, die bei jeder Erweiterung länger wird (Beispielsammlungen, Fehlerlisten), gehört in eine Reference
- Projektwerte gehören ins Skill-Profil oder in die Config des Projekts
- jede Reference ist direkt aus SKILL.md verlinkt; über 100 Zeilen beginnt sie mit einem Inhaltsverzeichnis

Muster: SKILL.md enthält Zweck, Kernregeln, je Reference einen Verweis und ein kurzes VERBOTEN. Bei mehreren Befehlen
oder Fällen gibt es eine Tabelle „Befehl/Fall → Reference“.

Trifft etwas zu: den Befund kurz nennen (was, warum, wohin) und per Auswahlfrage entscheiden lassen. Optionen:
aufteilen / so lassen / später als Skill-Issue. Nie ohne Freigabe aufteilen. Aufteilen ist ein Refactor.

## Abschluss

Gilt für beide Modi.

1. **Prüfskript** (Check skill-validation im Skill-Profil) mit `-Skill <skill>`: keine neuen Fehler.
2. **Diff-Bericht** im Chat:
   - was unverändert blieb (Kurzform)
   - was neu ist (Text)
   - was geändert ist (vorher/nachher)
   - was entfallen ist (mit Inventar-ID und Grund)
   - Länge der Description
   - Dateien der Lieferung
   - Version und Commit
3. **Version und Doku** nach dem Skill-Profil: neue Nummer mit CHANGELOG-Eintrag; INDEX, wenn sich Zuständigkeit oder
   Auslöser ändern.
4. **Commit** im Format des Skill-Profils, **Push** nach dessen Push-Policy. Ohne CHANGELOG-Eintrag und Commit ist die
   Änderung nicht fertig, auch nicht nach dem Upload.
5. **Routing-Eval** der betroffenen Fälle nach dem Commit und vor dem Upload (Check routing-eval im Skill-Profil, dazu
   `--tag <skill>`). Freigabe nach `docs/skill-quality.md`, Abschnitt Verhalten. Kein Pre-Commit-Check.
6. **Lieferung** nach `references/delivery.md`: zuerst das Repo, dann SKILL.md bzw. Zip an den Nutzer zum Upload bei
   claude.ai. Ohne Lieferung arbeitet Claude weiter mit dem alten Stand.

## Auffälligkeiten melden

Fällt bei der Arbeit etwas auf, das über den Auftrag hinausgeht, kurz darauf hinweisen und per Auswahlfrage anbieten,
ein Skill-Issue anzulegen (über tracker). Optionen: anlegen / später selbst / nicht nötig. Nie ungefragt anlegen.
Anlässe:
- eine Regel widerspricht einer ausdrücklichen Anweisung des Nutzers oder einem anderen Skill
- tote Verweise, veraltete Pfade oder IDs
- Werkzeug- oder Projektbindung im Skill
- ein Split-Kandidat
- ein Skill löst zu oft oder zu selten aus

Nicht melden: Tippfehler, Stilunterschiede zwischen Skills, was der Nutzer gerade selbst ändert, nie gewünschte
Funktionen.

Erledigt eine Skill-Änderung einen offenen Merker im Memory: darauf hinweisen, per Auswahlfrage bestätigen lassen und
erst dann entfernen. Das ist kein eigener Auslöser, nur der Nachgang einer Änderung.

## VERBOTEN

- Skills aus dem Gedächtnis oder aus der geladenen Kopie neu schreiben
- Text still entfernen, kürzen oder zusammenfassen: im Safe Patch außerhalb des Umfangs gar nicht, im Refactor nur als
  freigegebene DROP-Zeile
- Refactor ohne Regel-Inventar oder ohne Prüfung in beide Richtungen
- Querverweise über Nummern (Regel, Kapitel, Modus, Schritt)
- eine Description über 1024 Zeichen liefern oder sie ohne Routing-Eval ändern
- Skill-Commit ohne Lieferung an den Nutzer; Lieferung ohne CHANGELOG-Eintrag und Commit
- Skill mit references nur als SKILL.md liefern
- mehrere Skills in einer Antwort liefern oder zum nächsten wechseln, bevor „gespeichert“ bestätigt und per
  Auswahlfrage geklärt ist
- Auswahlfrage im selben Antwortblock wie eine Lieferung
- Memory-Einträge ohne Bestätigung entfernen

## VERWEIS

- Ganz neuer Skill → skill-neu. Faustregel: Gibt es die SKILL.md schon, ist skill-pflege zuständig.
- Regeln für Skills: `docs/skill-quality.md`; Skill-Profil: `docs/skill-profile-v1.md`.
- Regel-Inventar: `references/rule-inventory.md`. Lieferung und Cowork: `references/delivery.md`.
