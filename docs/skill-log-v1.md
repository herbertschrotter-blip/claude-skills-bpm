# Skill-Log v1

Das Skill-Log hält fest, welche Prompts in Claude Code eingegeben wurden und welche Skills darauf gezündet haben – auf
jedem Rechner im selben Format. Daraus lässt sich regelmäßig prüfen, ob die Skills richtig auslösen, und es entstehen
echte Fälle für `evals/`. Werkzeuge: Hook `plugins/work-hooks/hooks/skill_log.py`, Auswertung `tools/skill-log/`.

## Inhalt

- Grundregeln
- Ablage
- Ereignisse
- Felder
- Datenschutz
- Einrichtung
- Auswertung

## Grundregeln

1. **Nur Prompts und Skill-Aufrufe.** Antworten und Werkzeugergebnisse kommen nicht ins Log; wer einen Fall genauer
   braucht, findet ihn über die `session` im Transcript von Claude Code (`~/.claude/projects/<ordner>/<session>.jsonl`).
2. **Ein Format für alle Rechner.** Linux und Windows schreiben dieselben Zeilen; `host` unterscheidet sie.
3. **Das Log stört nie.** Ein Fehler im Skript endet still mit Exit 0; der Chat läuft weiter.
4. **Keine Geheimnisse.** Texte werden vor dem Schreiben maskiert (Abschnitt Datenschutz).
5. **Version.** Jede Zeile trägt `"v": 1`. Eine inkompatible Änderung bekommt eine neue Nummer und ein neues Dokument.

## Ablage

`~/.claude/skill-log/<JJJJ-MM>.jsonl` – eine Datei je Monat (UTC) und Rechner, eine JSON-Zeile je Ereignis, UTF-8.
Andere Ablage über die Umgebungsvariable `SKILL_LOG_DIR`.

## Ereignisse

| `event` | Hook in Claude Code | Wozu |
|---|---|---|
| `session` | `SessionStart` | Rechner, Ordner und Projekt der Sitzung; auch nach `/clear` und beim Fortsetzen |
| `prompt` | `UserPromptSubmit` | Was eingegeben wurde – Maßstab, ob ein Skill hätte zünden müssen |
| `skill` | `PostToolUse`, Matcher `Skill` | Welcher Skill tatsächlich geladen wurde |
| `turn_end` | `Stop` | Ende der Runde; danach gehören Skill-Aufrufe nicht mehr zu diesem Prompt |
| `guard` | `PreToolUse`/`PostToolUse` (Skill-Wächter) | Aktion ohne zuständigen Skill: geblockt oder gewarnt (`docs/skill-guard-v1.md`) |

Eine **Runde** ist ein `prompt` mit allen `skill`-Zeilen derselben Sitzung bis zum nächsten `prompt` oder `turn_end`.

## Felder

Alle Zeilen:

| Feld | Inhalt |
|---|---|
| `v` | Formatversion, `1` |
| `ts` | Zeitpunkt in UTC, `JJJJ-MM-TTThh:mm:ssZ` |
| `host` | Name des Rechners; `SKILL_LOG_HOST`, sonst der Hostname |
| `session` | Sitzungs-ID von Claude Code |
| `event` | `session`, `prompt`, `skill` oder `turn_end` |
| `project` | `Projekt-ID` aus dem Skill-Profil der nächsten `CLAUDE.md` ab dem Arbeitsordner nach oben, sonst der Ordnername |

Zusätzlich je Ereignis:

| `event` | Felder |
|---|---|
| `session` | `cwd` – Arbeitsordner; `source` – `startup`, `resume`, `clear` oder `compact` |
| `prompt` | `text` – der Prompt, maskiert, höchstens 2000 Zeichen; `slash` – Name nach einem führenden `/`, sonst `null` |
| `skill` | `skill` – Name wie aufgerufen (z. B. `anthropic-skills:tracker`); `args` – maskiert, höchstens 300 Zeichen, sonst `null`; `ok` – `false`, wenn der Aufruf scheiterte |
| `turn_end` | – |

Beispiel:

```json
{"v": 1, "ts": "2026-09-29T07:49:02Z", "host": "ha-pi", "session": "6571194f-…", "event": "prompt", "project": "ha-config", "text": "tracker status", "slash": null}
{"v": 1, "ts": "2026-09-29T07:49:05Z", "host": "ha-pi", "session": "6571194f-…", "event": "skill", "project": "ha-config", "skill": "anthropic-skills:tracker", "args": "status", "ok": true}
```

## Datenschutz

Vor dem Schreiben ersetzt das Skript durch `<MASKIERT>`:
- Werte nach `token`, `password`/`passwort`, `secret`, `api_key`, `access_key`, `bearer`, `authorization`, `schlüssel`
- GitHub-Tokens (`ghp_…`, `github_pat_…`), Schlüssel der Form `sk-…`, JWTs
- Schlüssel aus Gruppen wie `ABCD-EFGH-…` (z. B. Backup-Schlüssel von Home Assistant)

Die Maskierung fängt typische Fälle, nicht jeden. Geheimnisse gehören ohnehin nicht in Prompts.

`SKILL_LOG_RAW=1` schreibt zusätzlich die **ungekürzten und unmaskierten** Hook-Daten nach `raw-<JJJJ-MM>.jsonl` – nur
zur Fehlersuche einschalten und danach die Datei löschen.

## Einrichtung

Über das Plugin `work` aus dem Marketplace `workbench` (dieses Repo), je Rechner einmal:

```
claude plugin marketplace add herbertschrotter-blip/claude-workbench
claude plugin install work@workbench
```

Das Plugin bringt die Hooks für Skill-Log und Skill-Wächter mit (eingetragen im Plugin-Eintrag `work` in `.claude-plugin/marketplace.json`, Skripte unter `plugins/work-hooks/hooks/`). Den Rechnernamen im Log setzt
`env` in `~/.claude/settings.json`: `"env": { "SKILL_LOG_HOST": "<name>" }` (ohne ihn steht der Hostname im Log, im
HA-Add-on eine Container-ID). Abschalten je Rechner: `SKILL_LOG=0` bzw. `SKILL_GUARD=0` im selben Block. Updates:
`claude plugin update work@workbench` oder Auto-Update im Menü `/plugin` einschalten. Rechner, auf denen die Skills aus claude.ai kommen und `skillOverrides` nicht greift (Claude-Desktop-App), installieren statt `work` und `skill-workshop` nur `work-hooks@workbench` (Hooks ohne Skills); nie `work` und `work-hooks` zusammen.

Ohne Plugin (alter Weg) trägt man die Hooks von Hand in `~/.claude/settings.json` ein; Block `hooks`. `<befehl>` ist der Aufruf des
Skripts:
- Linux: `SKILL_LOG_HOST=<name> python3 <repo>/plugins/work-hooks/hooks/skill_log.py`
- Windows (PowerShell): `$env:SKILL_LOG_HOST='<name>'; python <repo>\plugins\work-hooks\hooks\skill_log.py`, dazu im Hook
  `"shell": "powershell"`

```json
"hooks": {
  "SessionStart":     [{ "hooks": [{ "type": "command", "command": "<befehl>", "timeout": 10 }] }],
  "UserPromptSubmit": [{ "hooks": [{ "type": "command", "command": "<befehl>", "timeout": 10 }] }],
  "PostToolUse":      [{ "matcher": "Skill", "hooks": [{ "type": "command", "command": "<befehl>", "timeout": 10 }] }],
  "Stop":             [{ "hooks": [{ "type": "command", "command": "<befehl>", "timeout": 10 }] }]
}
```

Vorhandene Einträge in `hooks` bleiben erhalten; die vier Einträge kommen dazu. Damit Transcripts für Nachfragen lange
genug bleiben, `"cleanupPeriodDays": 365` setzen (Standard 30 Tage). Das Skript braucht Python 3 ohne Zusatzpakete.

## Auswertung

`python3 tools/skill-log/skill_log_report.py [ordner …] [--since JJJJ-MM-TT] [--host …] [--project …] [--transcripts …]`

- zeigt je Skill die Zündungen, getrennt nach automatisch und per `/name`, und die gescheiterten Aufrufe; ein
  Slash-Aufruf eines Skills (`/projekt-anlegen`) zählt per `/name`, auch wenn dabei kein Ereignis `skill` entsteht
- trennt die Runden nach Art (`art`): `prompt`, `system` (Meldungen von Hintergrundaufgaben und Subagenten,
  `<task-notification>`, `<agent-message>`) und `leer` (nur Bild); bewertet werden nur Prompts
- führt je Runde die Skills, die in der Sitzung schon geladen waren (`aktiv`); sie bleiben bis zum Sitzungsende im
  Kontext. Was eine Sitzung vor dem Log geladen hatte (Gabelung `fork`, `resume`), liest das Skript aus ihrem
  Transcript unter `--transcripts` (Standard `~/.claude/projects`, `''` schaltet es ab). Ein Prompt ohne Skill mit
  aktivem Skill ist meist kein Fehlausfall
- markiert Runden als `unsicher`, wenn der Prompt vor dem `turn_end` der vorigen Runde kam (Nachricht während Claude
  noch arbeitet); ein Skill-Aufruf darin kann zur vorigen Runde gehören
- listet Runden mit mehreren Skills (möglicher Konflikt), unsicher zugeordnete Runden und Prompts ohne Skill
  (möglicher Fehlausfall)
- mehrere Ordner zusammen auswerten, z. B. das Log des Laptops neben dem des HA
- `--json` gibt die Runden aus – Grundlage für neue Fälle in `evals/` (`should_trigger`, `should_not_trigger`)
- zählt die Entscheidungen des Skill-Wächters je Regel (`guard` je Runde; `docs/skill-guard-v1.md`)
- Tests: `python3 -m unittest tools/skill-log/test_skill_log_report.py`
