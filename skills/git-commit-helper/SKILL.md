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

## 🚨 VERBINDLICHE REGEL: Auswahlfrage bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS eine Auswahlfrage
gestellt werden — KEINE Prosa-Fragen.** Auswahlfrage = das Frage-Werkzeug der
jeweiligen Umgebung mit anklickbaren Optionen (im Cowork-Chat
`ask_user_input_v0`, in Claude Code `AskUserQuestion`). Der Skill nennt
kein Werkzeug fest; Claude nimmt das, das gerade zur Verfügung steht.

### Diese Fragen IMMER als Auswahlfrage:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (unbekannt) | Branch-Namen aus `git branch -a` |
| Typ unklar | Feature, Fix, Change, Refactor, Perf, Docs |
| Version-Bump unklar | MAJOR (Breaking), MINOR (Feature), PATCH (Fix) |
| Projektprofil fehlt | Profil anlegen, Einmalig angeben, Abbrechen |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen (z.B. Kurztitel)
- User hat Präferenz signalisiert

## Branch-Ermittlung

Branch aus Chat-Kontext verwenden.
Wenn Branch in dieser Session noch nicht bekannt: per Auswahlfrage fragen.
NIE automatisch einen Branch annehmen.

## Commit-Format (VERBINDLICH, in allen Projekten gleich)

```
[vX.Y.Z] Modul, Typ: Kurztitel
```

Das Format ist fest und projektübergreifend. Was sich je Projekt ändert
(Versionsquelle, Bump-Regel, Doku-Checkliste), steht im Projektprofil.

Wenn das Projekt eine Aufgaben- oder Ticket-Nummer führt (z.B. Bauplan-
Schritt, ClickUp-ID), gehört sie an den Anfang des Kurztitels oder in die
zweite Zeile der Message – nie vor das `[vX.Y.Z]`.

### Typen
- Feature → MINOR
- Fix → PATCH
- Change → PATCH/MINOR
- Refactor → PATCH
- Perf → PATCH
- Docs → PATCH

Diese Zuordnung ist der Standard. Die Bump-Regel im Projektprofil darf sie
überschreiben (z.B. „Vorabversion: jede eingespielte Änderung zählt die
Vorab-Nummer hoch, unabhängig vom Typ“).

Version aus der Versionsquelle des Projektprofils ermitteln (z.B.
Directory.Build.props bei WPF, package.json bei Node/TypeScript, pom.xml
bei Java, INDEX.md wo das Projekt sie dort führt).

## PROJEKTPROFIL (PFLICHT vor Schritt 1)

Alles Projektspezifische steht im Repo, nicht im Skill. Quelle in dieser
Reihenfolge:

1. **`CLAUDE.md` in der Repo-Wurzel**, Abschnitt `## Commit-Profil` mit
   genau diesen Zeilen:
   ```
   ## Commit-Profil
   - Modul-Namen: <feste Liste, z.B. Karte, Backend, Doku>
   - Versionsquelle: <Datei und Feld, z.B. dreame_x60/card/package.json "version">
   - Bump-Regel: <Standard | Vorabversion: jede Änderung zählt hoch | eigene Regel>
   - Doku-Checkliste: <Datei → wann anfassen, eine Zeile je Datei>
   ```
2. Fehlt der Abschnitt: **Repo selbst durchsuchen** – `docs/`-Ordner,
   `*.md` in der Wurzel und in `docs/`, bekannte Versionsdateien
   (Directory.Build.props, package.json, pom.xml, pyproject.toml, *.csproj).
   Das Gefundene als Vorschlag zeigen.
3. Dann Auswahlfrage: „Projektprofil fehlt“ → *Profil anlegen* (Abschnitt
   in CLAUDE.md schreiben, mit dem Vorschlag aus 2) / *Einmalig angeben* /
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

## SCHRITT 2 — Commit-Befehle (One-Block-Regel)

**KERNREGEL:** Eine komplette Commit-Sequenz wird IMMER in EINEM Code-Block
geliefert. Niemals aufgeteilt in mehrere Blöcke für `cd` / `add` / `commit`
/ `push`. Der User soll mit einem Klick kopieren und in eine Shell einfügen
können. Führt Claude die Befehle selbst aus (Claude Code), gilt dieselbe
Sequenz als ein Aufruf.

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
- `git log -1 --format="%h %s"` am Ende, damit Herbert den Commit-Hash sofort sieht
- Bei Renames: `git mv` als zusätzliches Glied vor `git add`
- Branch-Name aus Branch-Ermittlung einsetzen (nie hartkodiert "main" annehmen)
- Verlangt das Projekt Tests vor dem Commit (steht im Profil oder in CLAUDE.md),
  läuft der Testbefehl als erstes Glied der Sequenz; bei rotem Ergebnis kein Commit

### Mehrzeilig nur wenn User explizit darum bittet

Wenn Herbert eine besser lesbare, mehrzeilige Variante will, in EINEM Block
mit Backtick-Continuation (PowerShell) oder Backslash (Bash) liefern — nie
in mehrere Code-Blöcke aufteilen.

## SCHRITT 3 — Doc-Pflege Trigger (PFLICHT)

Die Doku-Checkliste kommt aus dem Projektprofil (`Doku-Checkliste:` je Datei
eine Zeile „Datei → wann“). Sie wird nach dem Commit abgearbeitet; jede
betroffene Datei wird genannt, geändert und im selben oder nächsten Commit
mitgenommen.

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
4. Version korrekt hochzählen (Versionsquelle und Bump-Regel aus dem Projektprofil)
5. Komplette Commit-Sequenz in EINEM Code-Block (One-Block-Regel, siehe Schritt 2)
6. Keine Erklärungen
7. Bei Renames: git mv
8. Arbeitsverzeichnis IMMER automatisch (Repo-Wurzel)
9. Doc-Pflege IMMER am Ende (Checkliste aus dem Projektprofil)
10. Projektprofil IMMER lesen, bevor Version oder Doku angefasst werden

## VERBOTEN

- Branch automatisch annehmen ohne Auswahlfrage
- Typ-Auswahl als Prosa bei Unsicherheit — IMMER Auswahlfrage
- Version-Bump als Prosa bei Unsicherheit — IMMER Auswahlfrage
- Prosa-Fragen bei festen Entscheidungsoptionen
- **Mehrere Code-Blöcke für eine Commit-Sequenz** — alles muss in EINEM Block stehen, semikolon- oder `&&`-getrennt (siehe Schritt 2 One-Block-Regel)
- **Erklärungen zwischen den Befehlen** die das Kopieren stören — Erklärungen kommen vor oder nach dem Block, nie hinein
- **Versionsquelle oder Doku-Dateien raten** — beides kommt aus dem Projektprofil oder aus der Suche im Repo, nie aus dem Gedächtnis
- **Werkzeugnamen fest verdrahten** (Desktop Commander, ask_user_input_v0, AskUserQuestion) — der Skill beschreibt die Handlung, Claude wählt das Werkzeug der Umgebung
