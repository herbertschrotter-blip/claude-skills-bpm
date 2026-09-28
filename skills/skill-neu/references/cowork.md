# skill-neu im Cowork-Chat

Der Ablauf ist derselbe wie in `SKILL.md`. Hier stehen nur die Werkzeuge und Regeln, die es nur im Cowork-Chat gibt.

## Inhalt

- Vorhandene Skills
- Schreiben
- Lieferung
- Commit
- Memory
- Skripte

## Vorhandene Skills

- Die geladenen eigenen Skills zeigt `view /mnt/skills/user/`. Maßgeblich ist aber das Skill-Repo, gelesen per
  Desktop Commander (`read_file`).
- Namen, die Anthropic belegt, stehen unter `/mnt/skills/examples/` und `/mnt/skills/public/` (z. B. `skill-creator`,
  `pdf`, `docx`). Vor der Namenswahl dort nachsehen.

## Schreiben

- Neue Dateien per Desktop Commander `write_file` ins Skill-Repo, immer mit absoluten Pfaden.
- Details eines anderen Skills liest Claude aus dem Repo nach, per Desktop Commander `read_file` oder
  `github:get_file_contents`.

## Lieferung

Wie in `skills/skill-pflege/references/delivery.md`, Abschnitt Cowork:
- Artifact als Paar direkt hintereinander: `create_file` mit `/home/claude/SKILL.md` und dem vollständigen Inhalt,
  danach `present_files` mit demselben Pfad.
- Der Dateiname ist exakt `SKILL.md`, sonst erscheint kein „Skill speichern“-Button.
- Ein Artifact je Antwort und kein `ask_user_input_v0` im selben Block. Bei references eine Zip statt des Artifacts.

## Commit

Im Cowork-Chat committet der Nutzer selbst. Claude liefert den fertigen Befehl (git-commit-helper).

## Memory

Memory ist für offene Merker gedacht, nicht für Aufgaben. Es gibt vier Rubriken, festgelegt in `MEMORY-RUBRIKEN.md` im
Skill-Repo. Beim Anlegen eines Skills:
- offene Struktur- oder Auslösefragen → `[ARCH-OPEN]`
- spätere Prüfung des Auslösens im Betrieb → `[VERIFY]`
- eine ausstehende Antwort aus einem externen Review → `[REVIEW-PENDING]`

Keine Aufgaben mit Commit, Zielversion oder mehreren Schritten ins Memory legen; die gehören per `tracker neu` in den
Tracker. Keine neuen Rubriken erfinden. Einen erledigten Eintrag erst nach Bestätigung durch den Nutzer entfernen, mit
`memory_user_edits` (`remove`). In Claude Code liegt das Memory als Datei im Memory-Ordner; dort Datei und Indexzeile
entfernen.

## Skripte

Im Cowork-Chat gibt es keine Shell und keine Subagenten, `scripts/` ist dort kaum nutzbar. Der Skill muss ohne seine
Skripte funktionieren.
