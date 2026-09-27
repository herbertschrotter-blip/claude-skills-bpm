# Grundmessung der Skills (September 2026)

Vergleichsbasis für alle Umbauten ab Phase 4 (`docs/skillsystem-umbau.md`). Gemessen wurden die unveränderten Skills
(Stand v0.36.9, unter `skills/` gleich seit Commit 12f90b8) mit den 60 Fällen aus `quality/evals/` (Katalog und Regeln:
`quality/README.md`), je drei Läufe:

`claude plugin eval . --runs 3 --ablation none --no-publish --trust-plugin --keep-temp`

- **Teil 1** am 24.09.2026, 20:59–21:58: 30 Fälle; der Lauf wurde auf Herberts Wunsch abgebrochen, das Ergebnis ist aus
  den Lauf-Protokollen nachgerechnet (`teil-1-2026-09-24.md`).
- **Teil 2** am 27./28.09.2026, 22:34–0:34: die übrigen 30 Fälle und `audit-findings-fix` mit neu formuliertem Testsatz
  (f67de05; die Messung aus Teil 1 zählt für diesen Fall nicht). Gesamtauswertung von `plugin eval`: 120 Minuten,
  Gegenwert zum Listenpreis 40,88 USD (Max-Abo, keine Rechnung). Für Teil 1 gibt es keine Kostenangabe.

## Ergebnis

- **55 von 60 Fällen bestanden, 172 von 180 Läufen (95,6 %).**
- **Kritische Fälle: 20 von 23 bestanden.**
- Zeitüberschreitungen (180 Sekunden) und die Schrittgrenze (8) trafen vor allem mockup-erstellen, skill-neu und
  skill-pflege, weil Claude nach dem Aufruf weiterarbeitet. Sie änderten kein Ergebnis: Der Skill war jeweils vorher
  aufgerufen.

| Skill | Fälle bestanden | Läufe bestanden |
|---|---|---|
| code-erstellen | 6/8 | 20/24 |
| doc-pflege | 7/7 | 21/21 |
| audit | 5/7 | 18/21 |
| mockup-erstellen | 6/6 | 18/18 |
| skill-pflege | 6/6 | 18/18 |
| skill-neu | 5/5 | 15/15 |
| chat-wechsel | 4/4 | 12/12 |
| chatgpt-review | 4/4 | 12/12 |
| tracker | 4/4 | 12/12 |
| git-commit-helper | 3/3 | 9/9 |
| ticket | 3/3 | 9/9 |
| cc-steuerung | 2/3 | 8/9 |
| **gesamt** | **55/60** | **172/180** |

## Nicht bestanden

| Fall | Ergebnis | Bewertung |
|---|---|---|
| `audit-readonly` (kritisch, Ziel) | 1/3 | Ziel-Fall: Die audit-Description deckt die Prüfung von Skills noch nicht ab; zählt ab Phase 5. |
| `cc-not-in-claude-code` (kritisch) | 2/3 | Echter Fehler: cc-steuerung löst in Claude Code aus; die Description nennt „Claude Code“ als Auslöser (Phase 5). |
| `audit-findings-fix` (kritisch) | 2/3 | Ein Lauf durchsucht zuerst den leeren Arbeitsordner und hört ohne Skill auf. |
| `code-generic-change` | 1/3 | wie oben, zwei Läufe |
| `code-refactor` | 1/3 | wie oben, zwei Läufe |

**Muster bei den letzten drei:** Bei knappen Aufträgen, die auf vorhandenen Code oder vorhandene Doku zeigen, sucht Claude
zuerst die Dateien. Die Sandbox hat keine; Claude meldet das und ruft keinen Skill auf. Wie oft das in einem echten Repo
passiert, misst diese Grundmessung nicht. Für eine spätere Messung: Fälle mit kleinen Beispieldateien im Arbeitsordner
ausstatten (`scaffold_script` von `plugin eval`), damit der Suchschritt etwas findet.

## Wie spätere Messungen verglichen werden

Nach `docs/skillsystem-umbau.md`, Abschnitt Tests: Ein Umbau ist freigegeben, wenn kein kritischer Fall unter 3/3 fällt,
der heute 3/3 hat; kein heute bestandener Negativfall kippt; die Gesamtquote nicht unter 172/180 liegt; neue Konflikte
erklärt sind und das Prüfskript keine neuen Fehler meldet. `audit-readonly` und `cc-not-in-claude-code` sollen nach
Phase 5 bestehen.

## Fälle

Spalte „aufgerufen“: je Lauf die aufgerufenen Skills, `–` = keiner.

| Fall | Teil | Art | bestanden | Status | aufgerufen |
|---|---|---|---|---|---|
| `audit-bauplan` | 1 | kritisch | 3/3 | bestanden | audit / audit / audit |
| `audit-code-docs` | 1 | kritisch | 3/3 | bestanden | audit / audit / audit |
| `audit-findings-fix` | 2 | kritisch | 2/3 | nicht bestanden | – / doc-pflege / doc-pflege |
| `audit-frontmatter` | 1 | kritisch | 3/3 | bestanden | audit / audit / audit |
| `audit-generic-check` | 1 | kritisch | 3/3 | bestanden | audit / audit / audit |
| `audit-no-trigger-code-review` | 1 | normal | 3/3 | bestanden | – / – / – |
| `audit-readonly` | 1 | kritisch, Ziel | 1/3 | nicht bestanden | – / – / audit |
| `cc-no-trigger-file-read` | 1 | kritisch | 3/3 | bestanden | – / – / – |
| `cc-not-in-claude-code` | 1 | kritisch | 2/3 | nicht bestanden | – / cc-steuerung / – |
| `cc-prefix-code` | 1 | normal | 3/3 | bestanden | code-erstellen / code-erstellen / code-erstellen |
| `chat-wechsel-handover` | 1 | normal | 3/3 | bestanden | chat-wechsel / chat-wechsel / chat-wechsel |
| `chat-wechsel-new-chat` | 1 | normal | 3/3 | bestanden | chat-wechsel / chat-wechsel / chat-wechsel |
| `chat-wechsel-no-trigger-goodbye` | 1 | normal | 3/3 | bestanden | – / – / – |
| `chat-wechsel-no-trigger-other-prompt` | 1 | normal | 3/3 | bestanden | – / – / – |
| `chatgpt-review-next-round` | 1 | normal | 3/3 | bestanden | chatgpt-review / chatgpt-review / chatgpt-review |
| `chatgpt-review-no-trigger-claude-handover` | 1 | normal | 3/3 | bestanden | chat-wechsel / chat-wechsel / chat-wechsel |
| `chatgpt-review-no-trigger-vague` | 1 | normal | 3/3 | bestanden | – / – / – |
| `chatgpt-review-prompt` | 1 | normal | 3/3 | bestanden | chatgpt-review / chatgpt-review / chatgpt-review |
| `code-bugfix` | 1 | normal | 3/3 | bestanden | code-erstellen / code-erstellen / code-erstellen |
| `code-from-approved-mockup` | 1 | normal | 3/3 | bestanden | code-erstellen / code-erstellen / code-erstellen |
| `code-generic-change` | 1 | normal | 1/3 | nicht bestanden | – / – / code-erstellen |
| `code-ha-automation` | 1 | normal | 3/3 | bestanden | code-erstellen / code-erstellen / code-erstellen |
| `code-implement` | 1 | normal | 3/3 | bestanden | code-erstellen / code-erstellen / code-erstellen |
| `code-refactor` | 1 | normal | 1/3 | nicht bestanden | – / – / code-erstellen |
| `code-small-ui-fix` | 1 | normal | 3/3 | bestanden | code-erstellen / code-erstellen / code-erstellen |
| `code-with-task-ref` | 1 | normal | 3/3 | bestanden | code-erstellen / code-erstellen / code-erstellen |
| `commit-command` | 1 | kritisch | 3/3 | bestanden | git-commit-helper / git-commit-helper / git-commit-helper |
| `commit-no-trigger-push` | 1 | kritisch | 3/3 | bestanden | – / – / – |
| `commit-version-bump` | 1 | normal | 3/3 | bestanden | git-commit-helper / git-commit-helper / git-commit-helper |
| `doc-adr` | 1 | normal | 3/3 | bestanden | doc-pflege / doc-pflege / doc-pflege |
| `doc-changelog` | 2 | normal | 3/3 | bestanden | doc-pflege / doc-pflege / doc-pflege |
| `doc-concept` | 2 | normal | 3/3 | bestanden | doc-pflege / doc-pflege / doc-pflege |
| `doc-fix-links` | 2 | kritisch | 3/3 | bestanden | doc-pflege / doc-pflege / doc-pflege |
| `doc-no-trigger-discussion` | 2 | normal | 3/3 | bestanden | – / – / – |
| `doc-session-close` | 2 | normal | 3/3 | bestanden | doc-pflege / doc-pflege / doc-pflege |
| `doc-write` | 2 | kritisch | 3/3 | bestanden | doc-pflege / doc-pflege / doc-pflege |
| `mockup-layout-variants` | 2 | normal | 3/3 | bestanden | mockup-erstellen / mockup-erstellen / mockup-erstellen |
| `mockup-new-dialog` | 2 | normal | 3/3 | bestanden | mockup-erstellen / mockup-erstellen / mockup-erstellen |
| `mockup-no-trigger-component` | 2 | normal | 3/3 | bestanden | code-erstellen / code-erstellen / code-erstellen |
| `mockup-no-trigger-db-schema` | 2 | normal | 3/3 | bestanden | code-erstellen / – / code-erstellen |
| `mockup-sketch-dashboard` | 2 | normal | 3/3 | bestanden | mockup-erstellen / mockup-erstellen+dataviz / mockup-erstellen |
| `mockup-then-implement` | 2 | normal | 3/3 | bestanden | mockup-erstellen / mockup-erstellen / mockup-erstellen |
| `skill-neu-create` | 2 | kritisch | 3/3 | bestanden | skill-neu / skill-neu / skill-neu |
| `skill-neu-draft` | 2 | kritisch | 3/3 | bestanden | skill-neu / skill-neu / skill-neu |
| `skill-neu-no-trigger-eval-run` | 2 | normal | 3/3 | bestanden | – / – / – |
| `skill-neu-no-trigger-extend` | 2 | kritisch | 3/3 | bestanden | skill-pflege / skill-pflege / skill-pflege |
| `skill-neu-test-prompts` | 2 | normal | 3/3 | bestanden | skill-neu / skill-neu / skill-neu |
| `skill-pflege-description` | 2 | kritisch | 3/3 | bestanden | skill-pflege / skill-pflege / skill-pflege |
| `skill-pflege-no-trigger-other-repo` | 2 | normal | 3/3 | bestanden | doc-pflege / doc-pflege / doc-pflege |
| `skill-pflege-reference` | 2 | normal | 3/3 | bestanden | skill-pflege / skill-pflege / skill-pflege |
| `skill-pflege-restructure` | 2 | kritisch | 3/3 | bestanden | skill-pflege / skill-pflege / skill-pflege |
| `skill-pflege-typo` | 2 | normal | 3/3 | bestanden | skill-pflege / skill-pflege / skill-pflege |
| `skill-update` | 2 | kritisch | 3/3 | bestanden | skill-pflege / skill-pflege / skill-pflege |
| `ticket-list` | 2 | kritisch | 3/3 | bestanden | ticket / ticket / ticket |
| `ticket-no-trigger-bug-without-number` | 2 | normal | 3/3 | bestanden | code-erstellen / code-erstellen / code-erstellen |
| `ticket-number` | 2 | kritisch | 3/3 | bestanden | ticket / ticket / ticket |
| `tracker-done` | 2 | kritisch | 3/3 | bestanden | tracker / tracker / tracker |
| `tracker-issue` | 2 | kritisch | 3/3 | bestanden | tracker / tracker / tracker |
| `tracker-new` | 2 | kritisch | 3/3 | bestanden | tracker / tracker / tracker |
| `tracker-no-trigger-brainstorm` | 2 | normal | 3/3 | bestanden | – / – / – |
