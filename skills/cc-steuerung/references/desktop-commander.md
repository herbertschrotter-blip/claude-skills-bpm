# Desktop Commander im Cowork-Chat

Werkzeuge und Fallstricke zu `skills/cc-steuerung/SKILL.md`. Gilt nur im Cowork-Chat.

## Desktop Commander erkennen

- Ob Desktop Commander (DC) verfügbar ist, zeigt nur die Tool-Liste. Stehen dort `Desktop Commander:start_process`,
  `Desktop Commander:write_file`, `Desktop Commander:edit_block` usw., ist DC aktiv und wird direkt benutzt.
- Sind die Werkzeuge nicht sichtbar: am Chat-Start bzw. beim ersten DC-Kommando `tool_search` mit „desktop commander“
  aufrufen, das lädt sie.
- Nie `bash_tool hostname` zur Erkennung benutzen. `bash_tool` läuft in der Sandbox des Chats und meldet immer `runsc`,
  auch wenn der Chat in Claude Desktop läuft und DC verfügbar ist. Die Ausgabe sagt nichts über den PC des Nutzers.

## Werkzeuge

| Aufgabe | Werkzeug (`Desktop Commander:…`) |
|---|---|
| Datei lesen | `read_file`; mehrere Dateien: `read_multiple_files` |
| Datei neu schreiben / anhängen | `write_file` mit `mode: "rewrite"` / `mode: "append"` |
| Datei ändern | `edit_block` (alter Text → neuer Text) |
| Verzeichnis listen | `list_directory` |
| Datei verschieben | `move_file` |
| Befehl ausführen | `start_process` (mit `timeout_ms`) |
| Datei-Info | `get_file_info` |

## Schreiben

- Immer absolute Pfade, gebildet aus dem Arbeitsverzeichnis.
- `write_file` in Teilen von höchstens 25–30 Zeilen: der erste Teil mit `mode: "rewrite"`, die weiteren mit
  `mode: "append"`.
- Direkt auf die Platte geschriebene Dateien haben keine Kopier- und Encoding-Probleme, etwa bei XAML.

## PowerShell ohne `$`-Variablen

- Keine `$`-Variablen in Befehlen, die über `start_process` laufen. Die äußere Shell-Schicht ersetzt `$pc` und
  Ähnliches durch leere Zeichen, bevor PowerShell den Befehl sieht. Aus
  `powershell -Command "$pc = hostname; Write-Output $pc"` wird so ein Syntaxfehler („Die Benennung "=" wurde nicht
  als Name eines Cmdlet … erkannt“).
- Das gilt auch für `$env:OneDrive` und `$env:COMPUTERNAME`. Stattdessen `hostname` und
  `[System.Environment]::GetEnvironmentVariable('NAME','User')`.
- Mehrere Werte: Befehle mit Semikolon trennen und die Ausgabe zeilenweise lesen.
- Längere Logik mit Variablen oder Schleifen: als `.ps1`-Datei in den Temp-Ordner schreiben, mit
  `powershell -NoProfile -ExecutionPolicy Bypass -File <Datei>` ausführen und danach löschen. In der Datei
  funktionieren `$`-Variablen, weil sie nicht durch die äußere Shell müssen.

## Auswahlfrage

Die Auswahlfrage ist im Cowork-Chat das Werkzeug `ask_user_input_v0`.

## Lieferung eines Skills

Schreibt Claude per DC ins Skill-Repo und liefert den Skill als Artifact, gilt: keine Auswahlfrage im selben
Antwortblock, und die Datei heißt exakt `SKILL.md`. Vollständige Regeln: `skills/skill-pflege/references/delivery.md`,
Abschnitt Cowork.

## Alte Muster

- Wer `runsc` aus `bash_tool hostname` als „nicht in Claude Desktop“ las, fiel in den Modus „DC nicht verfügbar,
  Code-Block zum Kopieren“. Das verschenkte die Ausführung per DC und kostete am Chat-Anfang Zeit.
