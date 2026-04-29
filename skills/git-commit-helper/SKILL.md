---
name: git-commit-helper
description: >
  Erstellt fertige Git-Commit-Befehle und Commit-Messages im BPM-Format
  [vX.Y.Z] Modul, Typ: Kurztitel. Use when users want to commit changes,
  need a git commit command, ask for a commit message, or want the correct
  version bump for an existing change (including PATCH/MINOR/MAJOR decisions
  or semver questions). Do not trigger for code creation, code review, git
  push, or general Zustimmung wie "ok" oder "passt".
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

## 🚨 VERBINDLICHE REGEL: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0`
verwendet werden — KEINE Prosa-Fragen.**

### Diese Fragen IMMER mit ask_user_input_v0:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (unbekannt) | Branch-Namen aus `git branch -a` |
| Typ unklar | Feature, Fix, Change, Refactor, Perf, Docs |
| Version-Bump unklar | MAJOR (Breaking), MINOR (Feature), PATCH (Fix) |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen (z.B. Kurztitel)
- User hat Präferenz signalisiert

## Branch-Ermittlung

Branch aus Chat-Kontext verwenden.
Wenn Branch in dieser Session noch nicht bekannt: Per ask_user_input_v0 fragen.
NIE automatisch einen Branch annehmen.

## Commit-Format (VERBINDLICH)

```
[vX.Y.Z] Modul, Typ: Kurztitel
```

### Typen
- Feature → MINOR
- Fix → PATCH
- Change → PATCH/MINOR
- Refactor → PATCH
- Perf → PATCH
- Docs → PATCH

Version aus INDEX.md / Directory.Build.props ermitteln.

## SCHRITT 0 — Arbeitsverzeichnis (PFLICHT)

Bei DC-Operationen: Arbeitsverzeichnis nach **cc-steuerung Kapitel 4** ermitteln.

## SCHRITT 1 — Git Status (wenn DC verfügbar)

```
dc:start_process → "cd '[Pfad]'; git status --short"
```

## SCHRITT 2 — Commit-Befehle (One-Block-Regel)

**KERNREGEL:** Eine komplette Commit-Sequenz wird IMMER in EINEM Code-Block
geliefert. Niemals aufgeteilt in mehrere Blöcke für `cd` / `add` / `commit`
/ `push`. Der User soll mit einem Klick kopieren und in eine Shell einfügen
können.

### PowerShell (Default, Windows)

Trenner: `;` (Semikolon)

```powershell
cd "[Arbeitsverzeichnis]" ; git add <spezifische-dateien> ; git commit -m "[vX.Y.Z] Modul, Typ: Kurztitel" ; git push origin <branch> ; git log -1 --format="%h %s"
```

### Bash (Linux/macOS, WSL)

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

### Mehrzeilig nur wenn User explizit darum bittet

Wenn Herbert eine besser lesbare, mehrzeilige Variante will, in EINEM Block
mit Backtick-Continuation (PowerShell) oder Backslash (Bash) liefern — nie
in mehrere Code-Blöcke aufteilen.

## SCHRITT 3 — Doc-Pflege Trigger (PFLICHT)

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

## Regeln

1. Windows-Pfade (Backslash)
2. `"` für Messages
3. Ein Commit = eine Änderung
4. Version korrekt hochzählen
5. Komplette Commit-Sequenz in EINEM Code-Block (One-Block-Regel, siehe Schritt 2)
6. Keine Erklärungen
7. Bei Renames: git mv
8. Arbeitsverzeichnis IMMER automatisch
9. Doc-Pflege IMMER am Ende (inkl. Frontmatter + Invarianten)

## VERBOTEN

- Branch automatisch annehmen ohne ask_user_input_v0
- Typ-Auswahl als Prosa bei Unsicherheit — IMMER ask_user_input_v0
- Version-Bump als Prosa bei Unsicherheit — IMMER ask_user_input_v0
- Prosa-Fragen bei festen Entscheidungsoptionen
- **Mehrere Code-Blöcke für eine Commit-Sequenz** — alles muss in EINEM Block stehen, semikolon- oder `&&`-getrennt (siehe Schritt 2 One-Block-Regel)
- **Erklärungen zwischen den Befehlen** die das Kopieren stören — Erklärungen kommen vor oder nach dem Block, nie hinein
