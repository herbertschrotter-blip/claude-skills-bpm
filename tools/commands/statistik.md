---
description: Skill-Statistik als Dashboard – Zündungen je Skill und Projekt, Verlauf je Tag, Blockaden des Skill-Wächters (Skill-Log dieses Rechners)
argument-hint: "[projekt] [seit JJJJ-MM-TT]"
---

Erzeuge das Dashboard des Skill-Logs und zeige es dem Nutzer. Keine eigene Auswertung, keine Bewertung – dafür gibt es
den Skill skill-auswertung.

1. Aus den Argumenten `$ARGUMENTS` lesen: ein Datum `JJJJ-MM-TT` → `--since`, ein anderes Wort → `--projekt`. Ohne
   Argumente: alles.
2. Ausführen (Bash):
   `python3 "${CLAUDE_PLUGIN_ROOT}/tools/skill-log/dashboard.py" --out ~/.claude/skill-log/statistik.html [--projekt …] [--since …]`
   Endet der Befehl mit Fehler: die Meldung kurz zeigen und aufhören.
3. Die Datei `~/.claude/skill-log/statistik.html` dem Nutzer zeigen: mit dem Werkzeug zum Senden von Dateien
   (SendUserFile, `display: render`), sonst den Pfad nennen und `xdg-open`/`start` vorschlagen.
4. Darunter höchstens drei Zeilen: Zeitraum, Zahl der Prompts, die drei häufigsten Skills. Nichts weiter.
