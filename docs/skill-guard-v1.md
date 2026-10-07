# Skill-Wächter v1

Skills zünden auf den Wortlaut des Prompts. Bei „weiter“, „ja“ oder „passt“ steht dort nichts, woran ein Skill
erkennen könnte, dass er gebraucht wird; die Entscheidung fällt erst bei der Aktion. Der Skill-Wächter prüft deshalb an
der Aktion: Ändert Claude Code, Mockups, Doku, Skills, ClickUp oder committet, muss der zuständige Skill in der Sitzung
geladen sein. Die Regeln dafür sind lernbar: skill-auswertung schärft sie anhand des Skill-Logs nach. Werkzeuge:
`tools/skill-guard/`.

## Inhalt

- Ablauf
- Regeln
- Lernen
- Einrichtung
- Grenzen

## Ablauf

| Hook | Regeln | Wenn der Pflicht-Skill fehlt |
|---|---|---|
| `PreToolUse` | `modus: blocken` | Aktion wird abgelehnt (Exit 2); Claude sieht die Begründung, lädt den Skill und wiederholt die Aktion |
| `PostToolUse` | `modus: warnen` | Aktion läuft; Claude bekommt danach einen Hinweis (`additionalContext`) und lädt den Skill für die weiteren Schritte |

- Geladene Skills liest der Wächter aus dem Transcript der Sitzung (Skill-Aufrufe und Slash-Befehle). Ein Skill bleibt
  bis zum Sitzungsende geladen. Subagenten und Workflows erben die Skills der Hauptsitzung (Transcript unter
  `<sitzung>/subagents/` → `<sitzung>.jsonl`).
- Jede Entscheidung landet als Ereignis `guard` im Skill-Log (`docs/skill-log-v1.md`): `regel`, `entscheidung`
  (`geblockt`/`gewarnt`), `tool`, `tool_use_id`, `ziel`, `pflicht`, `aktiv`.
- Ein Fehler im Wächter blockiert nie (Exit 0). `SKILL_GUARD=aus` schaltet ihn ab.

## Regeln

Datei `tools/skill-guard/regeln.json`, für alle Rechner gleich (kommt mit `git pull`). Felder je Regel:

| Feld | Inhalt |
|---|---|
| `id` | eindeutiger Name |
| `beschreibung` | Satz, den Claude in der Meldung sieht |
| `aktion` | `datei` (Edit/Write), `bash:schreibt` (Umleitung, `tee`, `sed -i`, Ziel von `cp`/`mv`, Schreiben im Python-Heredoc), `bash:commit`, `mcp:clickup-schreibt` |
| `pfad` / `ausser` | Muster wie `*.py`, `*/mockups/*` (fnmatch auf den absoluten Pfad; `*` passt auch über `/`). Dazu gilt `ausser_immer` für alle Regeln (Scratchpad, `/tmp`, `.claude/`, `.git/`) |
| `projekt` | `*` oder eine Projekt-ID aus dem Skill-Profil der `CLAUDE.md` |
| `pflicht` | Skills, von denen einer geladen sein muss |
| `modus` | `blocken`, `warnen` oder `aus` |
| `herkunft` | Befund oder Entscheidung, aus der die Regel stammt |
| `stand` | `seit`, `treffer`, `fehlalarm`, `zuletzt` – nachgerechnet von skill-auswertung |

Startregeln (07.10.2026): `code` und `mockup` blocken; `skills`, `doku`, `clickup`, `commit` warnen.

## Lernen

Bei „skills auswerten“ (Skill skill-auswertung) kommen die `guard`-Ereignisse dazu. Vorschläge – jeweils nur mit
Freigabe von Herbert in `regeln.json` übernehmen:

| Befund | Vorschlag |
|---|---|
| Lücke: Aktion ohne zuständigen Skill, die keine Regel erfasst (Transcript, Report „aktiv“) | neue Regel, Start `warnen` |
| Fehlalarm: Regel griff, der Skill war nicht nötig (Herbert widerspricht, Claude lädt den Skill nicht, Aufgabe gehört klar zu einem anderen Skill) | Ausnahme in `ausser`, weiterer Skill in `pflicht` oder `modus` zurückstufen |
| bewährt: mindestens 10 Treffer ohne Fehlalarm | `warnen` → `blocken` |
| tot: 30 Tage kein Treffer | prüfen, ggf. `aus` |

Nach jeder Auswertung `stand` aktualisieren und `regeln.json` mit der Auswertung committen.

## Einrichtung

In den globalen Einstellungen `~/.claude/settings.json` (gilt für alle Projekte), Block `hooks`, neben den Hooks des
Skill-Logs. `<befehl>`:
- Linux: `SKILL_LOG_HOST=<name> python3 <repo>/tools/skill-guard/skill_guard.py`
- Windows (PowerShell): `$env:SKILL_LOG_HOST='<name>'; python <repo>\tools\skill-guard\skill_guard.py`, dazu im Hook
  `"shell": "powershell"`

```json
"PreToolUse":  [{ "matcher": "Edit|Write|MultiEdit|NotebookEdit|Bash", "hooks": [{ "type": "command", "command": "<befehl>", "timeout": 10 }] }],
"PostToolUse": [{ "matcher": "Edit|Write|MultiEdit|NotebookEdit|Bash|mcp__.*[Cc]lick[Uu]p.*", "hooks": [{ "type": "command", "command": "<befehl>", "timeout": 10 }] }]
```

Je Rechner einmal: Repo klonen bzw. `git pull`, Einträge ergänzen. Auf dem Smartphone nichts – dort läuft Claude Code
nicht selbst, sondern steuert per Remote Control die Sitzung auf dem HA. Im Cowork-Chat und auf claude.ai gibt es keine
Hooks.

Tests: `python3 -m unittest tools/skill-guard/test_skill_guard.py`

## Grenzen

- Schreiben per Shell erkennt der Wächter über Muster. Ziele mit Shell-Variablen (`$S/datei`) lässt er aus. Im
  Python-Heredoc zählen alle genannten Dateien, auch gelesene, sobald das Skript schreibt.
- Dateien, die ein Build-Skript erzeugt (z. B. ein gebündeltes Mockup), sieht der Wächter nicht.
- Ob `PreToolUse` in Subagenten feuert, ist in der Doku von Claude Code nicht beschrieben; das Skill-Log zeigt es.
- Warnen geht nur nach der Aktion (`PostToolUse`); vor der Aktion kann ein Hook Claude keinen Hinweis geben.
