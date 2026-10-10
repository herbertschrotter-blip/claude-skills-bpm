# Lieferung eines Skills

Jede Skill-Änderung lebt an zwei Orten. Im Skill-Repo ist sie versioniert, das Repo ist die Wahrheit. Bei claude.ai
lädt Claude den Skill tatsächlich. Ohne Lieferung arbeitet Claude weiter mit dem alten Stand, obwohl das Repo längst
neu ist. Deshalb endet jede Skill-Änderung mit einer Lieferung, in derselben oder der direkt folgenden Antwort.

## Inhalt

- Reihenfolge
- Was geliefert wird
- Claude Code
- Ein Skill je Antwort
- Cowork

## Reihenfolge

1. Im Repo ändern, Prüfskript laufen lassen, CHANGELOG und INDEX nachziehen, Commit und Push. Der Abschluss steht in
   `SKILL.md`.
2. Die Routing-Eval der betroffenen Fälle laufen lassen, vor dem Upload.
3. An den Nutzer liefern. Er lädt bei claude.ai hoch und bestätigt mit „gespeichert“.
4. Die Antwort mit der Lieferung beenden.

Zuerst kommt das Repo: Die Lieferung wird aus dem Repo-Stand nach dem Commit gebaut, nie aus einem Zwischenstand.

## Was geliefert wird

- Immer die vollständige Datei, nie nur den Diff.
- Skill ohne references: die Datei `SKILL.md`.
- Skill mit references: eine Zip mit `SKILL.md` und dem Ordner `references/`, in der Struktur des Repos. Das gilt auch,
  wenn nur eine Reference geändert wurde, denn claude.ai hält den Skill als Ganzes.
- Skripte und Vorlagen, die nur Claude Code ausführt (`scripts/`, `templates/`), gehören nicht in die Zip. Bei claude.ai
  beschreiben die references den Ablauf ohne Ausführung; eine Ausführung wird dort nie behauptet.
- Die Datei heißt immer exakt `SKILL.md`, mit derselben Groß- und Kleinschreibung. Nur so erkennt claude.ai sie als
  Skill-Datei. Keine Präfixe, Suffixe oder Versionsangaben im Namen.
- Beim Upload einer Zip ersetzt der Nutzer alle Dateien. Danach muss unter „Inhalte“ die Dateizahl stimmen (SKILL.md
  plus alle references). Dateien, die im Repo entfernt wurden, löscht er dort auch.
- Die Description vorher messen: höchstens 1024 Zeichen, sonst lehnt claude.ai den Upload ab.
- Keine Lieferung braucht ein Commit, der den Inhalt nicht ändert, zum Beispiel wenn sich nur ein Pfad ändert.

## Claude Code

- Die Zip im Scratchpad bauen, aus dem Repo-Stand nach dem Commit, und ihren Inhalt vor dem Senden auflisten.
- Mit `SendUserFile` schicken. Die Caption nennt den Skill, die Version, was sich geändert hat, und „bei claude.ai
  hochladen“.
- Im selben Antwortblock keine Auswahlfrage stellen. Sie verdrängt die Dateikarte, und der Nutzer kann nicht in Ruhe
  speichern. Die Antwort endet mit der Lieferung. Das gilt für jede Lieferung, bei der der Nutzer noch etwas tun muss.

## Ein Skill je Antwort

- Je Antwort höchstens eine Skill-Lieferung. Den Kontext trennt der Antworttext, nicht ein anderer Dateiname.
- Nach jeder Lieferung auf „gespeichert“ warten. Erst dann per Auswahlfrage klären, wie es weitergeht: nächster Skill
  (Name) / Pause / anderer Skill / fertig.
- Repo-Änderungen an mehreren Skills in einer Antwort sind in Ordnung. Nur die Lieferungen laufen nacheinander.

## Cowork

Im Cowork-Chat gilt dasselbe, nur mit anderen Werkzeugen:

- **Lesen:** `view /mnt/skills/user/<skill>/SKILL.md` zeigt die geladene Kopie. Maßgeblich ist das Repo, gelesen per
  Desktop Commander (`read_file`).
- **Schreiben ins Repo:** per Desktop Commander mit `edit_block` (alter Text → neuer Text) oder `write_file`
  (vollständig neu), immer mit absoluten Pfaden.
- **Lieferung als Artifact**, immer als Paar direkt hintereinander:
  1. `create_file` mit dem Pfad `/home/claude/SKILL.md` und dem vollständigen Inhalt
  2. `present_files` mit `filepaths: ["/home/claude/SKILL.md"]`

  `create_file` allein schreibt nur in die Sandbox, es erscheint keine Dateikarte. Erst `present_files` zeigt die Karte
  mit „Skill speichern“. Der Button erscheint nur, wenn die Datei exakt `SKILL.md` heißt. Falsch sind z. B.
  `chat-wechsel-SKILL.md`, `SKILL-chat-wechsel.md` oder `skill.md`.
- **Ein Artifact je Antwort:** `/home/claude/SKILL.md` ist ein einziger Platz. Ein zweites `create_file` in derselben
  Antwort überschreibt das erste. Beide Karten zeigen dann denselben Inhalt, und ein Skill wird zweimal gespeichert,
  der andere gar nicht.
- **Keine Folgefrage:** kein `ask_user_input_v0` im selben Block wie das Artifact.
- **Keine Zusatzdatei:** keine eigene Download-Datei unter `/mnt/user-data/outputs/` anlegen. Das Artifact-Paar genügt.
- **Skills mit references:** eine Zip wie oben statt eines Artifacts.
- **Memory:** Einen Memory-Eintrag, den eine Änderung erledigt, erst nach Bestätigung mit `memory_user_edits`
  (`remove`) entfernen. Das gilt nur für die vier Rubriken `[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]` und
  `[REVIEW-PENDING]`. `[CLICKUP]`, `[SKILL-ISSUES]`, `[ANKER-LIVE]` und `[PROJECT]` sind dauerhafte Konventionen mit
  eigenen Regeln. Konvention: `MEMORY-RUBRIKEN.md` im Skill-Repo. In Claude Code entfernt man stattdessen die Datei im
  Memory-Ordner und ihre Zeile im Index.
