# Umgebung: tmux, Terminal im Browser, Handgriffe ohne Skript

## tmux am Smartphone

- Fensterleiste unten: ein Fenster antippen wechselt dorthin, wenn tmux `mouse on` hat.
- `Strg+b w` zeigt alle Fenster als Baum, `Strg+b s` die Sitzungen, `Strg+b n`/`p` nächstes/voriges Fenster.
- Ein Terminal im Browser hängt sich meist nur an **eine** tmux-Sitzung. Fenster in anderen Sitzungen sind dann nur
  über `Strg+b s` erreichbar; deshalb legt der Skill neue Fenster in der Hauptsitzung an und bietet `holen` an.

## Beispiel (Home Assistant, Add-on „Claude Terminal“)

- Das Add-on startet `tmux new-session -A -s claude -c /config claude`: Es hängt sich an die Sitzung `claude`; fehlt
  sie (nach einem Neustart des Add-ons oder wenn Claude im Hauptfenster beendet wurde), startet es ein neues, leeres
  Gespräch in `/config`. Deshalb erscheint nach dem Öffnen die Startseite statt des letzten Gesprächs.
- Optionen des Add-ons, die der Nutzer selbst einstellt (danach nur das Add-on neu starten):
  - `enable_remote_control: true` – das Hauptfenster läuft immer mit Remote Control.
  - `claude_extra_args: --continue` – das Hauptfenster setzt das letzte Gespräch aus dem Startordner fort.
  - `working_directory` – anderer Startordner.
- Das Add-on schreibt `~/.tmux.conf` bei jedem Start neu; eigene tmux-Einstellungen dort halten nicht.

## Ohne Skript

```sh
# Gespräche eines Ordners: in den Ordner wechseln, dann Auswahlliste von Claude Code
cd <ordner> && claude --resume
# bestimmtes Gespräch mit Remote Control in neuem Fenster
tmux new-window -n "<name>" -c "<ordner>" "claude --resume <id> --remote-control '<name>'"
# Ordner eines Gesprächs finden
grep -l '"sessionId":"<id>' ~/.claude/projects/*/*.jsonl | head -1
```
