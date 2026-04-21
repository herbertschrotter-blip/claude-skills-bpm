---
name: git-commit-helper
description: >
  Generiert fertige Git-Terminal-Befehle mit korrektem Commit-Format:
  [vX.Y.Z] Modul, Typ: Kurztitel. Triggert bei "commit", "committen",
  "git commit", "mach den commit", "push das". Auch bei "ok", "passt"
  nach Code-Blöcken. Wird von code-erstellen als letzter Schritt aufgerufen.
---

# Git Commit Helper

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

## SCHRITT 2 — Commit-Befehle

```bash
cd [Arbeitsverzeichnis]
git add <spezifische-dateien>
git commit -m "[vX.Y.Z] Modul, Typ: Kurztitel"
```

- Spezifische Pfade, nicht `git add .`
- Ein Commit pro logische Änderung
- `"` für Messages (Windows)

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
5. cd nur beim ersten Block
6. Keine Erklärungen
7. Bei Renames: git mv
8. Arbeitsverzeichnis IMMER automatisch
9. Doc-Pflege IMMER am Ende (inkl. Frontmatter + Invarianten)

## VERBOTEN

- Branch automatisch annehmen ohne ask_user_input_v0
- Typ-Auswahl als Prosa bei Unsicherheit — IMMER ask_user_input_v0
- Version-Bump als Prosa bei Unsicherheit — IMMER ask_user_input_v0
- Prosa-Fragen bei festen Entscheidungsoptionen
