# Skill-Evals

## Zweck

Messbarkeit von Skill-Descriptions. Pro Skill ein Query-Katalog mit 12–16 Beispiel-Anfragen und erwartetem Trigger-Verhalten. Baseline-Score vor Description-Änderung, After-Score nach Änderung.

## Workflow

1. **Katalog** (Phase 1a.2) — pro Skill Datei mit 12–16 Queries in 4 Kategorien
2. **Baseline** (Phase 1a.3) — via Claude API jeden Query gegen das Skill-Set testen, Trefferquote festhalten
3. **Description-Refactor** (Phase 2+) — Skill-Descriptions bearbeiten
4. **Re-Run** (Phase 5.8) — gleiche Queries nochmal durchlaufen, Score vergleichen
5. **Konflikt-Tests** (Phase 5.1–5.7) — für Skill-Paare gezielte Queries, die beide triggern könnten

## Kategorien

Jeder Query gehört in genau eine Kategorie:

| Kategorie | Bedeutung |
|-----------|-----------|
| `should_trigger` | Dieser Skill MUSS triggern |
| `should_not_trigger` | KEIN Skill darf triggern (reines Gespräch, Zustimmung, Rückfrage ohne Action) |
| `other_skill` | Ein ANDERER Skill soll triggern — welcher steht dabei |
| `ambiguous` | Grenzfall — beide Interpretationen vertretbar, wird dokumentiert statt bewertet |

## Quellen für Queries

**Golden Queries** — echte Formulierungen aus dem BPM-Chat-Verlauf. Haben Priorität, weil sie reale Trigger-Situationen repräsentieren. Markiert mit `[golden]`.

**Synthetische Queries** — Variationen ähnlicher Formulierungen, um Ränder zu testen (z.B. „commit" vs „commite" vs „commiten"). Markiert mit `[synthetic]`.

## Scoring

Baseline und After-Scores werden später via Claude API ermittelt. Format pro Run:

```yaml
run: baseline | after-refactor | konflikt-test
date: 2026-04-21
skill: git-commit-helper
results:
  should_trigger: 6/6
  should_not_trigger: 3/3
  other_skill: 2/3  # 1 Fehltrigger bei "git status"
  ambiguous: dokumentiert (nicht gewertet)
notes: "ok"/"passt" sauber ausgeschlossen, "git status" triggert noch
```

## Verzeichnisstruktur

```
evals/
├── README.md               (diese Datei)
├── _template.md            (Vorlage für neue Skills)
├── git-commit-helper.md
├── chatgpt-review.md
├── tracker.md
├── code-erstellen.md
└── ... (weitere folgen in Phase 2+)
```
