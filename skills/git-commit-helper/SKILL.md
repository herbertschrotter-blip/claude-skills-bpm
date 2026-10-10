---
name: git-commit-helper
description: >
  Erstellt fertige Git-Commit-Befehle und Commit-Messages im einheitlichen Format
  [vX.Y.Z] Modul, Typ: Kurztitel – projektneutral, Versionsquelle und
  Doku-Checkliste kommen aus dem Projektprofil (CLAUDE.md des Repos). Use when
  users want to commit changes, need a git commit command, ask for a commit
  message, or want the correct version bump for an existing change (including
  PATCH/MINOR/MAJOR decisions or semver questions). Do not trigger for code
  creation, code review, git push, or general Zustimmung wie "ok" oder "passt".
---

# Git Commit Helper

---

## Vorrang / Delegation an andere Skills

**git-commit-helper ist für Commit-Befehle, Commit-Messages und Version-Bumps.
Wenn die Hauptabsicht Code-Änderungen oder andere Aktionen sind, NICHT hier
weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Code schreiben oder ändern (Services, ViewModels, Dialoge, Logik) | **code-erstellen** |
| UI-Entwurf als HTML-Mockup | **mockup-erstellen** |
| ClickUp-Task anlegen, updaten, schließen | **tracker** |
| Doku schreiben (ADR, Konzept, Frontmatter, Quickload) | **doc-pflege** |
| Konsistenzprüfung Code ↔ Docs | **audit** |

Nur wenn die Hauptabsicht **die Commit-Erstellung selbst** ist
(Commit-Message formulieren, Version-Bump wählen, git add/commit-Befehle),
bleibt git-commit-helper zuständig.

**Wichtig:** Nach Code-Änderungen liefert code-erstellen einen
Commit-Vorschlag INLINE (Schritt 9 seiner Load Order). Das ist kein
git-commit-helper-Trigger. Dieser Skill springt erst an wenn der User
explizit "commit", "commit-message", "welche Version" o.ä. fragt ODER
wenn code-erstellen an ihn delegiert hat.

---

## Grundsätze

- **Fragen nur bei offener Entscheidung**, dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung. Typische Stellen:
  - Typ unklar: Feature, Fix, Change, Refactor, Perf, Docs
  - Version-Bump unklar: MAJOR (Breaking), MINOR (Feature), PATCH (Fix)
  - ein benötigter Wert fehlt im Skill-Profil (Abschnitt „Skill-Profil“ unten)

  Prosa nur bei einer offenen Frage ohne feste Optionen (z.B. Kurztitel) oder wenn der Nutzer eine Präferenz
  signalisiert hat.
- **Branch** nach der Branch-Policy des Skill-Profils: `current` → der aktuelle Branch aus der Shell
  (`git branch --show-current`); `fixed:<branch>` → der aktuelle Branch muss dieser sein, sonst Auswahlfrage
  (wechseln / abbrechen). Ohne Shell gilt bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage. Ohne Profil: ein in der Sitzung schon bekannter Branch, sonst die Shell; ohne Shell per
  Auswahlfrage fragen. NIE automatisch einen Branch annehmen.
- **Push** nach der Push-Policy des Skill-Profils:
  - `user-only`: kein `git push` in der Sequenz; der Nutzer pusht selbst
  - `allowed`: `git push` nur, wenn der Nutzer es ausdrücklich will
  - `required-after-commit`: `git push origin <branch>` als Glied der Sequenz
  - `required-at-session-end`: kein Push in der Sequenz; gepusht wird am Ende der Sitzung

  Ohne Push-Policy (kein Skill-Profil): `git push origin <branch>` bleibt als Glied in der Sequenz.

## Commit-Format (VERBINDLICH, in allen Projekten gleich)

```
[vX.Y.Z] Modul, Typ: Kurztitel
```

Das Format ist fest und projektübergreifend. Was sich je Projekt ändert
(Versionsquelle, Versionsregel, Doku-Checkliste), steht im Skill-Profil.

Wenn das Projekt eine Aufgaben- oder Ticket-Nummer führt (z.B. Bauplan-
Schritt, ClickUp-ID), gehört sie an den Anfang des Kurztitels oder in die
zweite Zeile der Message – nie vor das `[vX.Y.Z]`.

**Modul:** ein Name aus der Modul-Liste des Skill-Profils. Berührt eine
Änderung mehrere Module, gilt das Hauptmodul (wo die Absicht liegt); die
übrigen werden im Kurztitel genannt. Sind die Teile unabhängig, werden es
zwei Commits.

**Zweite Zeile (optional):** nach einer Leerzeile ein bis drei Sätze mit
Begründung, Befund oder Verweis (Ticket, Bauplan-Abschnitt). Nie Prosa in
die erste Zeile packen.

### Typen
- Feature → MINOR
- Fix → PATCH
- Change → PATCH/MINOR
- Refactor → PATCH
- Perf → PATCH
- Docs → PATCH
- Test → PATCH
- Chore (Werkzeuge, Konfiguration, Abhängigkeiten) → PATCH

Diese Zuordnung ist der Standard. Die Versionsregel im Skill-Profil darf sie
überschreiben (z.B. „Vorabversion: jede eingespielte Änderung zählt die
Vorab-Nummer hoch, unabhängig vom Typ“ oder „neue Nummer nur bei Änderungen unter
`skills/**`“).

Version aus der Versionsquelle des Skill-Profils ermitteln (z.B.
Directory.Build.props bei WPF, package.json bei Node/TypeScript, pom.xml
bei Java, INDEX.md wo das Projekt sie dort führt; bei `changelog:<Datei>` die
Nummer des obersten Eintrags).

## Skill-Profil (PFLICHT vor Schritt 1)

Alles Projektspezifische steht im Repo, nicht im Skill. Quelle in dieser
Reihenfolge:

1. **`CLAUDE.md` in der Repo-Wurzel, Abschnitt `## Skill-Profil`** (Spezifikation `docs/skill-profile-v1.md` im
   Skill-Repo): Bereich `### Commit` (Module, Versionsquelle, Versionsregel, Push-Policy, Pre-Commit-Checks,
   Doku-Check), dazu `Branch-Policy` und `### Checks`.
2. Fehlt der Abschnitt: der ältere Abschnitt `## Commit-Profil` mit diesen Zeilen:
   ```
   ## Commit-Profil
   - Modul-Namen: <feste Liste, z.B. Karte, Backend, Doku>
   - Versionsquelle: <Datei und Feld, z.B. dreame_x60/card/package.json "version">
   - Bump-Regel: <Standard | Vorabversion: jede Änderung zählt hoch | eigene Regel>
   - Doku-Checkliste: <Datei → wann anfassen, eine Zeile je Datei>
   ```
   Modul-Namen entsprechen „Module“, Bump-Regel „Versionsregel“, Doku-Checkliste „Doku-Check“.
3. Fehlt auch der: **Repo selbst durchsuchen** – `docs/`-Ordner,
   `*.md` in der Wurzel und in `docs/`, bekannte Versionsdateien
   (Directory.Build.props, package.json, pom.xml, pyproject.toml, *.csproj).
   Das Gefundene als Vorschlag zeigen.
4. Dann Auswahlfrage: „Skill-Profil fehlt“ → *Profil anlegen* (Abschnitt
   `## Skill-Profil` in CLAUDE.md schreiben, mit dem Vorschlag aus 3) / *Einmalig angeben* /
   *Abbrechen*.

Das Profil wird nie aus dem Gedächtnis angenommen. Einmal gelesen, gilt es
für die Session.

## SCHRITT 0 — Arbeitsverzeichnis (PFLICHT)

Arbeitsverzeichnis = Repo-Wurzel, ermittelt mit
`git rev-parse --show-toplevel` in der Shell, die gerade zur Verfügung steht
(Claude Code: Bash oder PowerShell direkt; Cowork-Chat: Desktop Commander).
Bei Worktrees gilt die Wurzel des Worktrees.

## SCHRITT 1 — Git Status

```
git status --short
```

in der Shell der Umgebung ausführen. Kein Commit ohne vorherigen Status.

## SCHRITT 1a — Versionsdatei hochzählen (PFLICHT bei Version-Bump)

Die neue Version steht nicht nur in der Commit-Message: Die Versionsquelle
aus dem Skill-Profil (z.B. Directory.Build.props, package.json samt
package-lock.json, pom.xml; bei `changelog:<Datei>` ein neuer oberster Eintrag) wird auf die neue Nummer gesetzt und
gehört mit in denselben Commit. Ohne Änderung der Versionsdatei kein `[vX.Y.Z]` mit
neuer Nummer.

## SCHRITT 1b — Doku-Checkliste VOR dem Commit

Die Doku-Checkliste (Schritt 3) wird vor der Commit-Sequenz abgearbeitet,
damit Code, Version und Doku in einem Commit landen. Schritt 3 beschreibt
die Liste; ausgeführt wird sie hier, vor Schritt 2.

## SCHRITT 2 — Commit-Befehle (One-Block-Regel)

**KERNREGEL:** Eine komplette Commit-Sequenz wird IMMER in EINEM Code-Block
geliefert. Niemals aufgeteilt in mehrere Blöcke für `cd` / `add` / `commit`
/ `push`. Der User soll mit einem Klick kopieren und in eine Shell einfügen
können. Führt Claude die Befehle selbst aus (Claude Code), gilt dieselbe
Sequenz als ein Aufruf.

Das Glied `git push origin <branch>` steht nur in der Sequenz, wenn die Push-Policy es verlangt oder erlaubt
(Grundsätze); sonst entfällt es.

### PowerShell (Default, Windows)

Trenner: `;` (Semikolon)

```powershell
cd "[Arbeitsverzeichnis]" ; git add <spezifische-dateien> ; git commit -m "[vX.Y.Z] Modul, Typ: Kurztitel" ; git push origin <branch> ; git log -1 --format="%h %s"
```

### Bash (Linux/macOS, WSL, Git Bash)

Trenner: `&&` (nur weitermachen wenn vorheriger Befehl OK)

```bash
cd "[Arbeitsverzeichnis]" && git add <spezifische-dateien> && git commit -m "[vX.Y.Z] Modul, Typ: Kurztitel" && git push origin <branch> && git log -1 --format="%h %s"
```

### Regeln für die Sequenz

- Spezifische Pfade nach `git add`, nicht `git add .`
- Ein Commit pro logische Änderung
- `"` für Commit-Messages (Windows-kompatibel)
- `git log -1 --format="%h %s"` am Ende, damit der Nutzer den Commit-Hash sofort sieht
- Bei Renames: `git mv` als zusätzliches Glied vor `git add`
- Branch-Name nach den Grundsätzen einsetzen (nie hartkodiert "main" annehmen)
- Pre-Commit-Checks des Skill-Profils, die für die geänderten Dateien gelten (Pfad-Muster des Checks), laufen vor dem
  Commit (Abschnitt „Prüfläufe vor dem Commit“); ohne Skill-Profil der Testbefehl, den das Projekt vor dem Commit
  verlangt (CLAUDE.md). Bei rotem Ergebnis kein Commit

### Prüfläufe vor dem Commit

Die Checks laufen auf der Maschine, nicht im Modell; ihre Laufzeit ist Wartezeit für den Nutzer.

**Claude Code:** Die Regeln unten setzt das Skript `scripts/checks.py` dieses Skills um:
`python3 <Skill-Ordner>/scripts/checks.py --vor-commit` (unter Windows je nach Installation `python`). Es liest das
Skill-Profil, wählt die passenden Checks, lässt sie gleichzeitig laufen (`(allein)` im Profil für sich), merkt sich
grüne Läufe und gibt die Tabelle aus. Exit 0 grün; 1 rot; 2 ein Befehl fehlt auf diesem Rechner (dann sagen, wo der
Check läuft, z. B. per CI); 3 Profil oder git nicht lesbar. Die Tabelle des Skripts wird unverändert gemeldet; bei Rot
die Ausgabe aus der Log-Datei lesen. Läuft das Skript nicht (kein Python), gelten die Regeln von Hand.

- **Nur passende Checks:** Ein Check aus `Pre-Commit-Checks` läuft nur, wenn mindestens eine geänderte Datei zu
  einem seiner Pfad-Muster passt (gestaged, ungestaged und neu, laut `git status --short`). Ein Check ohne
  Pfad-Muster läuft immer. Jeden übersprungenen Check ausdrücklich melden: `übersprungen: <check> – keine passende
  Datei`.
- **Gleichzeitig oder nacheinander:** Unabhängige Checks gleichzeitig starten, wenn sie sich nicht um Kerne, Dateien,
  Ports oder Datenbanken streiten. Zwei Läufe, die beide alle Kerne nutzen oder dieselbe Test-Datenbank schreiben,
  laufen nacheinander, die schnellen zuerst, damit ein rotes Ergebnis früh kommt.
- **Lange Checks** (über etwa eine Minute) im Hintergrund starten, Ausgabe in eine Datei. Danach das Ergebnis
  vollständig lesen (Zusammenfassung, Fehler, Warnungen), nicht nur die letzte Zeile oder den Exit-Code.
- **Meldung** als Tabelle, übersprungene Checks eingeschlossen:

  | Check | Dauer | Ergebnis |
  |---|---|---|
  | unit | 0:42 | grün |
  | integration | – | übersprungen – keine passende Datei |

- **Claude Code** führt die Checks vor der Commit-Sequenz aus; die Sequenz folgt erst, wenn alle gelaufenen Checks
  grün sind. **Cowork:** Die passenden Checks stehen als erste Glieder in der Sequenz, die übersprungenen nennt
  Claude vor dem Block.

### Wenn ein Glied der Sequenz fehlschlägt

Rotes Testergebnis, abgelehnter Push, Hook-Fehler oder Konflikt: Sequenz
bricht am fehlerhaften Glied ab (dafür `&&` bzw. Prüfung des Exit-Codes).
Ursache in einem Satz nennen, nichts überspringen, keinen Teil-Commit
„trotzdem“ pushen. Erst wenn die Ursache behoben ist, die ganze Sequenz
erneut liefern.

### Mehrzeilig nur wenn User explizit darum bittet

Wenn der Nutzer eine besser lesbare, mehrzeilige Variante will, in EINEM Block
mit Backtick-Continuation (PowerShell) oder Backslash (Bash) liefern — nie
in mehrere Code-Blöcke aufteilen.

## SCHRITT 3 — Doc-Pflege Trigger (PFLICHT)

Die Doku-Checkliste kommt aus dem Skill-Profil (`Doku-Check`; im älteren Commit-Profil `Doku-Checkliste:` je Datei
eine Zeile „Datei → wann“). Sie wird vor der Commit-Sequenz abgearbeitet
(Schritt 1b); jede betroffene Datei wird genannt, geändert und im selben
Commit mitgenommen.

Fehlt die Checkliste im Profil: `docs/` und `*.md` im Repo auflisten und per
Auswahlfrage klären, welche Dateien bei dieser Änderung dran sind; das
Ergebnis als Vorschlag für die Checkliste ins Profil übernehmen.

Beispiel einer Checkliste (Projekt mit ADR/Quickload-Standard):

```
Checkliste:
- [ ] Neues Doc? → INDEX.md
- [ ] Neues Feature? → CHANGELOG.md
- [ ] DB geändert? → DB-SCHEMA.md
- [ ] Neue Architekturentscheidung? → ADR.md
- [ ] Neues Konzept? → INDEX.md + BACKLOG.md
- [ ] Neuer Entry Point? → INDEX.md
- [ ] Doc geändert? → Frontmatter + Quickload aktuell?
- [ ] Fachliche Invarianten betroffen? → Quickload prüfen
```

Beispiel einer Checkliste (Projekt mit Bauplan/Übergabe):

```
Checkliste:
- [ ] Bauschritt fertig? → Statusliste im Bauplan
- [ ] Befund oder Entscheidung? → Bauplan Abschnitt „Notizen aus dem Bau“
- [ ] Stand geändert? → HANDOFF.md
- [ ] Neue Entität oder Dienst? → Entitäts-Vertrag im Bauplan
```

## Regeln

1. Pfade in der Schreibweise der jeweiligen Shell (PowerShell: Backslash; Bash: Slash)
2. `"` für Messages
3. Ein Commit = eine Änderung
4. Version korrekt hochzählen (Versionsquelle und Versionsregel aus dem Skill-Profil)
5. Komplette Commit-Sequenz in EINEM Code-Block (One-Block-Regel, siehe Schritt 2)
6. Keine Erklärungen
7. Bei Renames: git mv
8. Arbeitsverzeichnis IMMER automatisch (Repo-Wurzel)
9. Doc-Pflege IMMER vor dem Commit (Checkliste aus dem Skill-Profil), damit Code und Doku zusammen landen
10. Skill-Profil IMMER lesen, bevor Version oder Doku angefasst werden
11. Versionsdatei gehört in denselben Commit wie die Versionsnummer in der Message
12. Bei mehreren Commits in einer Antwort: je Commit ein eigener Block (One-Block-Regel gilt je Commit)

## VERBOTEN

- Branch automatisch annehmen – ohne Branch-Policy, Shell oder Auswahlfrage
- Pushen gegen die Push-Policy des Skill-Profils
- Prosa-Fragen bei festen Entscheidungsoptionen (Typ, Version-Bump, fehlender Profilwert)
- **Mehrere Code-Blöcke für eine Commit-Sequenz** — alles muss in EINEM Block stehen, semikolon- oder `&&`-getrennt (siehe Schritt 2 One-Block-Regel)
- **Erklärungen zwischen den Befehlen** die das Kopieren stören — Erklärungen kommen vor oder nach dem Block, nie hinein
- **Versionsquelle oder Doku-Dateien raten** — beides kommt aus dem Skill-Profil oder aus der Suche im Repo, nie aus dem Gedächtnis
- **Werkzeugnamen fest verdrahten** (Desktop Commander, ask_user_input_v0, AskUserQuestion) — der Skill beschreibt die Handlung, Claude wählt das Werkzeug der Umgebung
- **Checks ohne passende Datei ausführen oder übersprungene Checks verschweigen** (Abschnitt „Prüfläufe vor dem Commit“)
