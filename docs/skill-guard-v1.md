# Skill-Wächter v1

Skills zünden auf den Wortlaut des Prompts. Bei „weiter“, „ja“ oder „passt“ steht dort nichts, woran ein Skill
erkennen könnte, dass er gebraucht wird; die Entscheidung fällt erst bei der Aktion. Der Skill-Wächter prüft deshalb an
der Aktion: Ändert Claude Code, Mockups, Doku, Skills, ClickUp oder committet, muss der zuständige Skill in der Sitzung
geladen sein. Die Regeln dafür sind lernbar: skill-auswertung schärft sie anhand des Skill-Logs nach. Werkzeuge:
`plugins/work/hooks/`.

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

- Geladene Skills liest der Wächter aus dem Transcript der Sitzung (Skill-Aufrufe, Slash-Befehle und nach einer
  Compaction der Anhang `invoked_skills`). Ein Skill bleibt
  bis zum Sitzungsende geladen. Subagenten und Workflows erben die Skills der Hauptsitzung (Transcript unter
  `<sitzung>/subagents/` → `<sitzung>.jsonl`).
- Jede Entscheidung landet als Ereignis `guard` im Skill-Log (`docs/skill-log-v1.md`): `regel`, `entscheidung`
  (`geblockt`/`gewarnt`), `tool`, `tool_use_id`, `ziel`, `pflicht`, `aktiv`.
- Ein Fehler im Wächter blockiert nie (Exit 0). `SKILL_GUARD=aus` schaltet ihn ab.

## Regeln

Datei `plugins/work/hooks/regeln.json`, für alle Rechner gleich (kommt mit dem Plugin-Update). Felder je Regel:

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
| `stand` | `seit`, `treffer`, `fehlalarm`, `zuletzt` – nachgerechnet von skill-auswertung; `rueckblick` = Abspielen der Regeln gegen alte Transcripts |

Startregeln (07.10.2026): `code` und `mockup` blocken; `skills`, `doku`, `clickup`, `commit` warnen. Nach dem Rückblick
über 29.09.–07.10. (erste Lernrunde): `doku` blockt (89 Treffer, 0 Fehlalarme), `clickup` erlaubt auch projekt-anlegen
und skill-neu (Fehlalarm beim Anlegen von Issue-Listen). Der Rückblick steht je Regel unter `stand.rueckblick`.

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

Über das Plugin `work` aus dem Marketplace `workbench` (dieses Repo), je Rechner einmal:

```
claude plugin marketplace add herbertschrotter-blip/claude-skills-bpm
claude plugin install work@workbench
```

Das Plugin bringt die Hooks für Skill-Log und Wächter mit (eingetragen im Plugin-Eintrag `work` in `.claude-plugin/marketplace.json`, Skripte unter `plugins/work/hooks/`). Den Rechnernamen im Log setzt
`env` in `~/.claude/settings.json`: `"env": { "SKILL_LOG_HOST": "<name>" }` (ohne ihn steht der Hostname im Log, im
HA-Add-on eine Container-ID). Abschalten je Rechner: `SKILL_LOG=0` bzw. `SKILL_GUARD=0` im selben Block. Updates:
`claude plugin update work@workbench` oder Auto-Update im Menü `/plugin` einschalten.

Ohne Plugin (alter Weg) trägt man die Hooks von Hand in `~/.claude/settings.json` ein; Block `hooks`, neben den Hooks des
Skill-Logs. `<befehl>`:
- Linux: `SKILL_LOG_HOST=<name> python3 <repo>/plugins/work/hooks/skill_guard.py`
- Windows (PowerShell): `$env:SKILL_LOG_HOST='<name>'; python <repo>\plugins\work\hooks\skill_guard.py`, dazu im Hook
  `"shell": "powershell"`

```json
"PreToolUse":  [{ "matcher": "Edit|Write|MultiEdit|NotebookEdit|Bash", "hooks": [{ "type": "command", "command": "<befehl>", "timeout": 10 }] }],
"PostToolUse": [{ "matcher": "Edit|Write|MultiEdit|NotebookEdit|Bash|mcp__.*[Cc]lick[Uu]p.*", "hooks": [{ "type": "command", "command": "<befehl>", "timeout": 10 }] }]
```

Beides nie zugleich: Hooks von Hand und Plugin würden doppelt prüfen und loggen. Auf dem Smartphone nichts – dort läuft Claude Code
nicht selbst, sondern steuert per Remote Control die Sitzung auf dem HA. Im Cowork-Chat und auf claude.ai gibt es keine
Hooks.

Tests: `python3 -m unittest plugins/work/hooks/test_skill_guard.py` (die Mechanik läuft gegen feste Modi, die echte
`regeln.json` wird nur auf Gültigkeit geprüft – so bricht kein Test, wenn eine Regel hochgestuft wird)

## Grenzen

- Schreiben per Shell erkennt der Wächter über Muster. Ziele mit Shell-Variablen (`$S/datei`) lässt er aus. Im
  Python-Heredoc zählen alle genannten Dateien, auch gelesene, sobald das Skript schreibt.
- Dateien, die ein Build-Skript erzeugt (z. B. ein gebündeltes Mockup), sieht der Wächter nicht.
- Ob `PreToolUse` in Subagenten feuert, ist in der Doku von Claude Code nicht beschrieben; das Skill-Log zeigt es.
- Warnen geht nur nach der Aktion (`PostToolUse`); vor der Aktion kann ein Hook Claude keinen Hinweis geben.
