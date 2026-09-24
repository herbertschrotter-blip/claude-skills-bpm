# Routing-Tests der Skills

Die Fälle unter `quality/evals/` prüfen, ob Claude bei einem Auftrag den richtigen Skill aufruft und die benachbarten
nicht. Sie laufen mit `claude plugin eval` in einer abgeschotteten Sitzung, die nur die Skills dieses Repos kennt: keine
CLAUDE.md, keine Dateien des Repos im Arbeitsordner, kein MCP, kein Memory. Gemessen wird nur das Auslösen, nicht die
Arbeit des Skills danach.

## Inhalt

- Aufbau
- Regeln für Fälle
- Aufruf
- Verteilung
- Nicht abgedeckt
- Fälle

## Aufbau

- Ein Ordner je Fall: `quality/evals/<fall>/prompt.md` (Frontmatter und Testsatz) und `graders/`.
- `<skill>-fired.md`: Der Skill muss mindestens einmal aufgerufen werden. `<skill>-not-fired.md` (`min: 0`,
  `max: 0`): Der Skill darf nicht aufgerufen werden.
- Tags: `baseline` (Grundmessung), `routing`, `pilot` (die fünf Pilotfälle), `critical` (muss 3 von 3 Läufen
  bestehen), `ziel` (Ziel-Fall, darf vor dem Umbau scheitern) und die Namen aller beteiligten Skills.
  `--tag <skill>` wählt damit alle Fälle, die ein Skill berührt.
- Das Manifest `.claude-plugin/plugin.json` zeigt auf `quality/evals`. Ergebnisse landen in
  `quality/evals/results/` und gehören nicht ins Repo.

## Regeln für Fälle

- Der Testsatz muss ohne Dateien des Repos verständlich sein; die Sandbox hat keine.
- Jeder Fall prüft eine Zuständigkeit. Konfliktfälle prüfen zusätzlich, dass der Nachbar nicht auslöst.
- Schwellen: kritische Fälle 3 von 3, alle anderen mindestens 2 von 3 (`docs/skillsystem-umbau.md`, Abschnitt Tests).
- Ziel-Fälle beschreiben den Zustand nach einer Umbau-Phase und zählen erst ab dieser Phase.
- Wer einen Fall anlegt, ändert oder löscht, zieht die Tabelle unten nach.

## Aufruf

Voraussetzung ist ein angemeldetes CLI (`claude auth login`, prüfen mit `claude auth status`).

| Zweck | Befehl |
|---|---|
| alle Fälle | `claude plugin eval . --runs 3 --ablation none --no-publish --trust-plugin` |
| Fälle eines Skills | dazu `--tag <skill>` |
| ein Fall zur Fehlersuche | `claude plugin eval . --case <fall> --runs 1 --ablation none --no-publish --trust-plugin --keep-temp` |

## Verteilung

Nach Risiko, festgelegt in `CGR-2026-09-24-skillsystem` Runde 2, Abschnitt 10. Konfliktfälle zählen beim Skill, dessen
Grenze sie prüfen.

| Skill | Fälle | davon kritisch |
|---|---|---|
| code-erstellen | 8 | 0 |
| doc-pflege | 7 | 2 |
| audit | 7 | 6 |
| mockup-erstellen | 6 | 0 |
| skill-pflege | 6 | 3 |
| skill-neu | 5 | 3 |
| chat-wechsel | 4 | 0 |
| chatgpt-review | 4 | 0 |
| tracker | 4 | 3 |
| git-commit-helper | 3 | 2 |
| ticket | 3 | 2 |
| cc-steuerung | 3 | 2 |
| **gesamt** | **60** | **23** |

## Nicht abgedeckt

- audit ↔ modul-bauplan: folgt, sobald es modul-bauplan gibt (echte Sitzung EXT-04).
- Konflikte mit Anthropic-Skills (skill-creator, code-review): `plugin eval` lädt keine fremden Skills; dafür gibt es
  echte Sitzungen EXT-01 bis EXT-05 (`quality/real-environment/`).
- cc-steuerung hat keinen Fall, in dem es auslösen soll: In Claude Code soll es nie auslösen. Das Prüfskript meldet dafür
  eine Warnung.

## Fälle

Stand 24.09.2026, 60 Fälle.

| Fall | Skill | Testsatz | soll auslösen | darf nicht auslösen | Art |
|---|---|---|---|---|---|
| `code-implement` | code-erstellen | Implementiere eine Wiederholungslogik für den fehlgeschlagenen Dateiimport und ergänze die passenden Tests. | code-erstellen | – | normal, Pilot |
| `code-bugfix` | code-erstellen | Im Import-Dialog stürzt die App ab, wenn die ausgewählte Datei leer ist. Behebe den Fehler. | code-erstellen | ticket | normal |
| `code-from-approved-mockup` | code-erstellen | Der Entwurf für den Dialog „Projekt anlegen“ ist abgenommen. Setz ihn jetzt in XAML um. | code-erstellen | mockup-erstellen | normal |
| `code-small-ui-fix` | code-erstellen | Im Profil-Dialog ist der Speichern-Button zu schmal, der Text wird abgeschnitten. Mach ihn breiter. | code-erstellen | mockup-erstellen | normal |
| `code-with-task-ref` | code-erstellen | Setz BPM-082 um: Im DocumentTypeRecognizer soll die Erkennung auch Plannummern mit Bindestrich finden. | code-erstellen | tracker | normal |
| `code-refactor` | code-erstellen | Refaktoriere den PlanParser: Die drei fast gleichen Parse-Methoden sollen eine gemeinsame Hilfsmethode nutzen. | code-erstellen | – | normal |
| `code-ha-automation` | code-erstellen | Schreib mir eine Home-Assistant-Automation in YAML: Wenn alle das Haus verlassen haben, soll der Saugroboter starten. | code-erstellen | – | normal |
| `code-generic-change` | code-erstellen | Ändere die Zeitüberschreitung beim Upload von 30 auf 60 Sekunden. | code-erstellen | doc-pflege | normal |
| `doc-write` | doc-pflege | Pflege die Projektdoku: Der Architekturabschnitt ist seit der letzten Änderung veraltet – bring ihn auf den neuen Stand. | doc-pflege | audit | kritisch, Pilot |
| `doc-adr` | doc-pflege | Schreib ein ADR zur Entscheidung, dass SQLite die einzige Quelle für Projektdaten ist. | doc-pflege | code-erstellen | normal |
| `doc-concept` | doc-pflege | Leg ein neues Konzept-Dokument für den Foto-Import an: Zweck, Ablauf und offene Fragen. | doc-pflege | code-erstellen | normal |
| `doc-fix-links` | doc-pflege | In der README sind zwei Links kaputt und das Kapitel zur Installation ist veraltet. Bring das bitte in Ordnung. | doc-pflege | audit | kritisch |
| `doc-changelog` | doc-pflege | Trag die Änderungen von heute im CHANGELOG ein. | doc-pflege | git-commit-helper | normal |
| `doc-no-trigger-discussion` | doc-pflege | Was hältst du grundsätzlich davon, Architekturentscheidungen als ADRs festzuhalten? Nur deine Meinung, bitte nichts anlegen. | – | doc-pflege | normal |
| `doc-session-close` | doc-pflege | Wir hören für heute auf. Mach bitte den Sitzungsabschluss in der Projektdoku: Stand und offene Punkte eintragen. | doc-pflege | – | normal |
| `audit-readonly` | audit | Prüfe bitte, ob die INDEX.md und die Beschreibungen der Skills zusammenpassen. Nur prüfen und die Befunde nennen, nichts ändern. | audit | doc-pflege | kritisch, Pilot, Ziel |
| `audit-code-docs` | audit | Prüf bitte, ob die Doku zum Import-Modul noch zum Code passt. Nur prüfen, nichts ändern – ich will eine Liste der Abweichungen. | audit | doc-pflege, code-erstellen | kritisch |
| `audit-frontmatter` | audit | Validiere bitte Frontmatter und Quickloads aller Docs. Nur lesen und die Befunde auflisten, nichts korrigieren. | audit | doc-pflege | kritisch |
| `audit-bauplan` | audit | Mach einen Bauplan-Check: Stimmen Statusliste und Entitäts-Vertrag noch mit dem Code überein? Nur prüfen. | audit | doc-pflege | kritisch |
| `audit-generic-check` | audit | Prüf mal alles durch, ob im Projekt noch alles zusammenpasst. | audit | doc-pflege, code-erstellen | kritisch |
| `audit-no-trigger-code-review` | audit | Schau dir diese Funktion an und sag mir, ob sie einen Fehler hat: (dazu eine kurze Python-Funktion) | – | audit | normal |
| `audit-findings-fix` | audit | Die Befunde aus dem Audit von gestern bitte jetzt beheben: Die veralteten Kapitel in der Architektur-Doku aktualisieren. | doc-pflege | audit | kritisch |
| `mockup-new-dialog` | mockup-erstellen | Mach mir ein Mockup für den neuen Einstellungen-Dialog, am besten zwei Varianten. | mockup-erstellen | code-erstellen | normal |
| `mockup-sketch-dashboard` | mockup-erstellen | Wie könnte das Dashboard für den Saugroboter aussehen? Skizzier es mir als HTML-Entwurf, bevor wir etwas bauen. | mockup-erstellen | code-erstellen | normal |
| `mockup-then-implement` | mockup-erstellen | Entwirf zuerst ein Mockup für die Projektliste, danach bauen wir sie ein. | mockup-erstellen | – | normal |
| `mockup-layout-variants` | mockup-erstellen | Ich brauche drei Layoutvarianten für die Kartenansicht, damit ich mich entscheiden kann. | mockup-erstellen | – | normal |
| `mockup-no-trigger-component` | mockup-erstellen | Bau die Lit-Komponente für die Raumkarte. Das Design ist schon abgenommen. | code-erstellen | mockup-erstellen | normal |
| `mockup-no-trigger-db-schema` | mockup-erstellen | Entwirf das Datenbankschema für die Zeiterfassung: Tabellen, Schlüssel und Beziehungen. | – | mockup-erstellen | normal |
| `skill-update` | skill-pflege | Ergänze im bestehenden chat-wechsel-Skill eine Regel, dass tote Dateiverweise vor der Übergabe gemeldet werden. | skill-pflege | skill-neu | kritisch, Pilot |
| `skill-pflege-description` | skill-pflege | Schärf die Description des tracker-Skills, damit „Aufgabe anlegen“ zuverlässig auslöst. | skill-pflege | skill-neu, tracker | kritisch |
| `skill-pflege-typo` | skill-pflege | In der SKILL.md von git-commit-helper sind zwei Tippfehler. Korrigier die bitte. | skill-pflege | git-commit-helper | normal |
| `skill-pflege-reference` | skill-pflege | Im tracker-Skill fehlt in references/create-task.md der Ablauf für Projekte ohne Custom Fields. Ergänz den bitte. | skill-pflege | tracker | normal |
| `skill-pflege-restructure` | skill-pflege | Bau den mockup-erstellen-Skill um: Lange Abschnitte in references auslagern, damit die SKILL.md unter 500 Zeilen kommt. | skill-pflege | skill-neu, mockup-erstellen | kritisch |
| `skill-pflege-no-trigger-other-repo` | skill-pflege | Ergänze in den Hausregeln meines Heidi-Repos (docs/HAUSREGELN.md) eine Regel, dass Tokens nie ins Repo gehören. | – | skill-pflege | normal |
| `skill-neu-create` | skill-neu | Ich brauche einen neuen Skill, der Home-Assistant-Module vom Konzept bis zum fertigen Dashboard plant. | skill-neu | skill-pflege | kritisch |
| `skill-neu-draft` | skill-neu | Entwirf eine SKILL.md für einen neuen Skill, der Besprechungsprotokolle zusammenfasst. | skill-neu | skill-pflege | kritisch |
| `skill-neu-test-prompts` | skill-neu | Richte für meinen neuen Skill „rechnung-pruefen“ Test-Prompts ein, mit denen ich prüfen kann, ob er richtig auslöst. | skill-neu | – | normal |
| `skill-neu-no-trigger-extend` | skill-neu | Erweitere den audit-Skill um eine Prüfung der Skill-Descriptions. | skill-pflege | skill-neu, audit | kritisch |
| `skill-neu-no-trigger-eval-run` | skill-neu | Lass die automatischen Eval-Tests für die Skills laufen und zeig mir das Ergebnis. | – | skill-neu, skill-pflege | normal |
| `chat-wechsel-handover` | chat-wechsel | Mach mir den Übergabe-Prompt für den nächsten Chat. | chat-wechsel | chatgpt-review | normal |
| `chat-wechsel-new-chat` | chat-wechsel | neuer chat bitte, wir machen morgen weiter | chat-wechsel | – | normal |
| `chat-wechsel-no-trigger-goodbye` | chat-wechsel | Danke dir, gute Nacht! | – | chat-wechsel | normal |
| `chat-wechsel-no-trigger-other-prompt` | chat-wechsel | Schreib mir einen Prompt, mit dem ich in einem Bildgenerator ein Logo für mein Projekt erzeugen kann. | – | chat-wechsel, chatgpt-review | normal |
| `chatgpt-review-prompt` | chatgpt-review | Dazu will ich eine zweite Meinung von ChatGPT. Mach mir den Review-Prompt. | chatgpt-review | chat-wechsel | normal |
| `chatgpt-review-next-round` | chatgpt-review | Hier ist die Antwort von ChatGPT auf Runde 2: Er hält den Ansatz für zu kompliziert und schlägt eine Konfigurationsdatei vor. Mach den Folgeprompt für Runde 3. | chatgpt-review | chat-wechsel | normal |
| `chatgpt-review-no-trigger-claude-handover` | chatgpt-review | Fass den Stand für die nächste Claude-Sitzung zusammen, damit ich dort weitermachen kann. | chat-wechsel | chatgpt-review | normal |
| `chatgpt-review-no-trigger-vague` | chatgpt-review | Was meinst du, passt das so? | – | chatgpt-review, chat-wechsel | normal |
| `tracker-new` | tracker | tracker neu: PM — Umlaute im Dateinamen brechen den Plan-Import | tracker | code-erstellen | kritisch |
| `tracker-issue` | tracker | Leg ein Skill-Issue für doc-pflege an: Modus 6 erkennt tote Links nicht. | tracker | skill-pflege, doc-pflege | kritisch |
| `tracker-done` | tracker | tracker done: BPM-082, der Commit ist drin. | tracker | ticket, git-commit-helper | kritisch |
| `tracker-no-trigger-brainstorm` | tracker | Lass uns mal überlegen, was wir als Nächstes priorisieren sollten. | – | tracker | normal |
| `commit-command` | git-commit-helper | Mach mir den Commit-Befehl für die Änderungen am Import-Dialog. | git-commit-helper | code-erstellen | kritisch |
| `commit-version-bump` | git-commit-helper | Ist das PATCH oder MINOR? Ich habe im Export eine neue Option ergänzt. | git-commit-helper | – | normal |
| `commit-no-trigger-push` | git-commit-helper | Push bitte den aktuellen Stand nach GitHub. | – | git-commit-helper | kritisch |
| `ticket-number` | ticket | ticket HT-0007 | ticket | tracker, code-erstellen | kritisch |
| `ticket-list` | ticket | Welche Tickets sind noch offen? ticket liste | ticket | tracker | kritisch |
| `ticket-no-trigger-bug-without-number` | ticket | In der Kartenansicht springt die Roboterposition hin und her. Kannst du das beheben? | code-erstellen | ticket | normal |
| `cc-not-in-claude-code` | cc-steuerung | Ich arbeite in Claude Code. Zeig mir bitte den Git-Status des Repos. | – | cc-steuerung | kritisch, Pilot |
| `cc-prefix-code` | cc-steuerung | cc: implementiere im ImportService eine Wiederholung bei Netzwerkfehlern. | code-erstellen | – | normal |
| `cc-no-trigger-file-read` | cc-steuerung | Lies die README.md und sag mir kurz, worum es in dem Projekt geht. | – | cc-steuerung | kritisch |
