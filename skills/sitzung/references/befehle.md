# Befehle von `scripts/sitzung.py`

Aufruf: `python3 <Skill-Ordner>/scripts/sitzung.py <befehl> [argumente] --json`. Ein Gespräch wird über den Anfang
seiner ID (acht Zeichen reichen) oder seinen genauen Namen angegeben, ein Fenster über `Sitzung:Nummer`, `Sitzung:Name`,
die Nummer in der Hauptsitzung oder den Namen. Fehler kommen als `{"fehler": "…"}` mit Exit 1.

## Gespräche

| Befehl | Was es tut |
|---|---|
| `projekte` | Ordner mit Gesprächen: Anzahl, zuletzt aktiv, wie viele laufen |
| `liste [--ordner O] [--n 15] [--alle]` | Gespräche, neueste zuerst; `--ordner` nimmt Pfad oder Ordnernamen |
| `vorschau <id> [--n 6]` | letzte Nachrichten (du / claude), gekürzt |
| `suche "<text>" [--n 10]` | Volltext über alle Gespräche, Gespräche mit den meisten Treffern zuerst, je drei Fundstellen |
| `oeffnen <id> [--name N] [--abzweigen] [--ohne-fernsteuerung] [--sitzung S]` | läuft es: hinwechseln; sonst neues Fenster im Ordner des Gesprächs mit `claude --resume`, wartet bis zu 30 s auf den Start, wechselt hin |
| `neu <ordner> [--name N] [--ohne-fernsteuerung]` | neues Fenster mit neuem Gespräch im Ordner |
| `umbenennen <id> "<name>"` | nur ruhende Gespräche; schreibt den Namen so, wie Claude Code es bei `/rename` tut |

Felder in `liste`: `id`, `name`, `titel` (automatischer Titel), `ordner`, `beginn`, `ende`, `eingaben`, `nachrichten`,
`erste`, `letzte` (erste und letzte Eingabe), `zustand` (`ruht`, `wartet`, `arbeitet`), `fenster` (wenn es läuft), `kontext` (Tokens im Kontext bei der letzten
Antwort – zeigt, wie voll das Gespräch ist).

## Fenster

| Befehl | Was es tut |
|---|---|
| `fenster` | alle Fenster aller tmux-Sitzungen: Sitzung, Nummer, Name, Ordner, Zustand, Gespräch |
| `wechseln <fenster>` | Ansicht wechselt dorthin |
| `fenster-umbenennen <fenster> "<name>"` | benennt um und schaltet die automatische Benennung ab |
| `verschieben <fenster> <stelle>` | an eine Stelle der Leiste; ist sie belegt, tauschen die beiden |
| `holen [<fenster>] [--sitzung S]` | Fenster anderer tmux-Sitzungen in die Hauptsitzung; ohne Angabe alle, das eigene nie |
| `neustart <fenster> [--erzwingen]` | Claude im Fenster neu starten, gleiches Gespräch; verweigert, wenn Claude gerade arbeitet |
| `schliessen <fenster> [--erzwingen]` | Fenster schließen; verweigert beim eigenen Fenster und wenn Claude gerade arbeitet |

## Arbeitsplatz und Aufräumen

| Befehl | Was es tut |
|---|---|
| `merken` | offene Fenster mit Gespräch nach `~/.claude/sitzung/arbeitsplatz.json` |
| `wiederherstellen` | ohne Angabe: Kandidaten (gemerkt oder beim Beenden offen); mit IDs oder `--alle`: öffnet sie ohne Wechsel der Ansicht |
| `leer [--hoechstens 1]` | ruhende Gespräche mit höchstens einer Eingabe und wenigen Antworten |
| `archivieren <id> …` | nach `~/.claude/sitzung/archiv/`; laufende nicht |
| `archiv` | archivierte Gespräche |
| `zurueckholen <id> …` | aus dem Archiv zurück |
| `loeschen <id> … --ja` | endgültig, aus Archiv oder Bestand; laufende nicht |

## Woher die Daten kommen

- Gespräche: `~/.claude/projects/<ordner-kodiert>/<id>.jsonl` (der echte Ordner steht im Feld `cwd`), daneben ein
  gleichnamiger Ordner mit Anhängen, der beim Archivieren mitwandert.
- Laufende Sitzungen: `~/.claude/sessions/<pid>.json` mit `sessionId`, `cwd`, `status` (`busy`, `idle`), `tmux`
  (`Sitzung:@Fenster.%Pane`) und `name`. Lebt der Prozess nicht mehr, ist der Eintrag verwaist – so erkennt das Skript,
  was beim letzten Beenden offen war.
- Ist `CLAUDE_CONFIG_DIR` gesetzt, gilt dieser Ordner statt `~/.claude`.
