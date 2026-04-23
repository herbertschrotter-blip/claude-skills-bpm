---
name: cc-steuerung
description: >
  Steuert Desktop Commander für direkte Datei-, Verzeichnis- und Terminal-
  Operationen auf Herberts PC. Use when users explicitly say "cc", "dc",
  "Claude Code", "direkt auf den PC", or want reading, writing, editing,
  building, or git commands executed on disk. Do not trigger for normal chat
  answers, code blocks in chat, or requests without explicit cc/dc intent.
---

# Claude Code Steuerung (Desktop Commander)

## Zweck

Definiert verbindlich wie Claude den `desktop-commander` MCP-Server
nutzt um direkt auf dem PC zu arbeiten: Dateien lesen/schreiben,
Terminal-Befehle ausführen, Projektstruktur prüfen.

---

## 🚨 Kernregel: Umgebungs-Erkennung über Tool-Liste (cc-steuerung-001)

**Claude erkennt die Verfügbarkeit von Desktop Commander AUSSCHLIESSLICH
über die Tool-Liste, NIEMALS über `bash_tool hostname`.**

### Richtig

- `Desktop Commander:start_process`, `Desktop Commander:write_file`,
  `Desktop Commander:edit_block` etc. erscheinen in der Tool-Liste
  → DC ist aktiv → direkt verwenden
- Am Chat-Start oder beim ersten DC-bezogenen Kommando:
  `tool_search(query: "desktop commander")` aufrufen um die DC-Tools
  in den Namespace zu laden falls sie noch nicht sichtbar sind

### Falsch

- `bash_tool hostname` liefert in der Sandbox immer `runsc` — auch wenn
  der Chat in Claude Desktop läuft und DC vollständig verfügbar ist
- `bash_tool` läuft im Claude-internen Container, **nicht** auf Herberts PC.
  Hostname-Output sagt nichts über die Verfügbarkeit externer MCP-Tools aus

### Konsequenz bei Verwechslung (Session Teil 28)

Wenn Claude `bash_tool hostname → runsc` als "ich bin nicht in Claude
Desktop" fehlinterpretiert, fällt er in den Modus "DC nicht verfügbar,
liefere Code-Block zum User-Copy-Paste". Das verschenkt die komplette
DC-Automatisierung und kostet User-Geduld am Chat-Anfang.

---

## 🚨 VERBINDLICHE REGEL: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0`
verwendet werden — KEINE Prosa-Fragen.**

### Diese Fragen IMMER mit ask_user_input_v0:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (unbekannt) | Branch-Namen aus `git branch -a` |
| Im Zweifel: Chat vs. PC-Schreiben | SUCHE/ERSETZE im Chat, Direkt auf PC per DC, Code-Block zeigen |
| 3+ Dateien betroffen | Erst analysieren (Plan), Direkt ausführen, Abbrechen |
| Dateien löschen | Löschen, Abbrechen, Andere Datei |
| Test-Path False | Pfad ist richtig, Anderer Pfad, Abbrechen |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen (z.B. PC-Name bei Self-Registration)
- User hat Präferenz signalisiert

---

## Branch-Ermittlung (PFLICHT vor GitHub-Zugriff)

1. Prüfe ob Branch bereits in dieser Session bekannt ist → verwenden
2. Wenn nicht bekannt: Alle Branches via GitHub API oder `git branch -a` via DC auflisten
3. User per ask_user_input_v0 den aktiven Branch wählen lassen
4. Gewählten Branch für die gesamte Session merken
5. NIE automatisch einen Branch annehmen (weder `main` noch einen anderen)

---

## 1. ROLLENVERTEILUNG

### Claude (das Gehirn)
- Planung, Konzepte, Architektur-Entscheidungen
- Code entwerfen und vorbereiten
- Standards und Regeln kennen und durchsetzen
- **Desktop Commander direkt aufrufen** für Datei- und Terminal-Operationen
- User beraten, Rückfragen stellen
- Code-Review, Commit-Vorschläge

### Desktop Commander (die Hände)
- Dateien lesen: `desktop-commander:read_file`
- Dateien schreiben: `desktop-commander:write_file`
- Dateien editieren: `desktop-commander:edit_block`
- Verzeichnisse listen: `desktop-commander:list_directory`
- Terminal-Befehle: `desktop-commander:start_process`
- Dateien verschieben: `desktop-commander:move_file`

### User (der Chef)
- Entscheidet WIE geliefert wird (Chat, SUCHE/ERSETZE, oder dc/cc)
- Gibt Freigabe für Schreiboperationen
- Pusht immer selbst (git push)
- Testet selbst

---

## 2. WANN WAS EINSETZEN

### Desktop Commander einsetzen wenn (User muss "cc" oder "dc" triggern):
- Neue Dateien erstellen → direkt auf Platte, kein Kopieren
- XAML-Dateien → kein Encoding-Problem
- Aktuellen Code lesen → immer aktuell, nicht letzter GitHub-Push
- Build testen → über start_process
- Multi-File-Änderungen → mehrere Dateien nacheinander
- git status / git log → über start_process
- Projektstruktur prüfen → list_directory

### Claude OHNE DC einsetzen (kein cc/dc-Trigger):
- Planung und Konzepte besprechen
- Kleine Code-Änderungen → SUCHE/ERSETZE im Chat
- Code erklären oder reviewen
- Committed Code lesen → github:get_file_contents
- Commit-Befehle zeigen (User kopiert in Terminal)
- Docs und Markdown schreiben

---

## 3. TRIGGER-REGELN

### Diese Wörter aktivieren Desktop Commander:
- "mit claude code", "über claude code"
- "cc lies", "cc erstelle", "cc mach", "cc build"
- "dc lies", "dc erstelle", "dc mach", "dc build"
- "lass claude code", "claude code soll"
- "schreib das mit cc", "schreib auf platte"
- "direkt auf den pc"

### Diese Wörter aktivieren NICHT Desktop Commander:
- "erstelle die datei" → Code-Block im Chat
- "code erstellen" → Code-Block im Chat
- "lies den code" → github:get_file_contents oder Chat
- "ändere die datei" → SUCHE/ERSETZE Skill
- "zeig mir" → Antwort im Chat
- "commit" / "committen" → git-Befehle im Chat

### Im Zweifel:
Per ask_user_input_v0 fragen: "Wie liefern?" mit Optionen "SUCHE/ERSETZE im Chat", "Direkt auf PC per DC", "Code-Block zeigen".

---

## 4. ARBEITSVERZEICHNIS (Auto-Discovery + Self-Registration)

### 4.1 Pfad-Ermittlung (erster DC-Aufruf der Session)

Beim ersten DC-Aufruf einer Session diesen Befehl ausführen:

```powershell
powershell -NoProfile -Command "hostname; [System.Environment]::GetEnvironmentVariable('OneDrive','User')"
```

Claude parst zeilenweise:
- Zeile 1 = COMPUTERNAME (aus `hostname`)
- Zeile 2 = OneDrive-Basispfad

**Wichtig:** `$env:OneDrive` funktioniert NICHT über DC `start_process`
(Umgebungsvariablen sind im DC-Prozesskontext nicht verfügbar).
Stattdessen IMMER `[System.Environment]::GetEnvironmentVariable('OneDrive', 'User')` verwenden.
`hostname` funktioniert zuverlässig (statt `$env:COMPUTERNAME`).

**KEINE `$`-Variablen-Assignments im Command-String** — Details siehe
Abschnitt "PowerShell-Aufrufe via DC" weiter unten.

### 4.2 PC-Lookup in INDEX.md

1. INDEX.md laden (via `github:get_file_contents` oder `read_file`)
2. Abschnitt "PCs und Arbeitsverzeichnisse" finden
3. COMPUTERNAME (aus `hostname`) in der PC-Tabelle suchen:
   - **GEFUNDEN** → workFolder = OneDrive-Pfad + `\` + Projekt-Suffix aus INDEX.md
   - **NICHT GEFUNDEN** → Self-Registration (siehe 4.3)

### 4.3 Self-Registration (unbekannter PC)

Wenn `hostname` einen COMPUTERNAME liefert der NICHT in der INDEX.md PC-Tabelle steht:

1. User fragen: "Unbekannter PC '<n>'. Wie soll er in der Tabelle heißen? (z.B. Surface, Standrechner)"
2. User antwortet mit dem gewünschten PC-Namen
3. Neue Zeile in der PC-Tabelle via DC `edit_block` in INDEX.md eintragen
4. Commit-Vorschlag liefern: `[vX.Y.Z] Docs, Docs: Neuen PC registriert (<n>)`
5. workFolder wie oben bilden und weiterarbeiten

### 4.4 Verifikation

Nach Ermittlung des workFolder:
```powershell
Test-Path "<workFolder>"
```
Wenn `False` → Nachfragen, NICHT raten oder alternativen Pfad probieren.

### 4.5 Regeln

- `[System.Environment]::GetEnvironmentVariable('OneDrive', 'User')` ist die EINZIGE Quelle für den OneDrive-Basispfad
- `hostname` identifiziert den PC
- **Keine hardcodierten absoluten Pfade** (kein `C:\Users\herbe\...`, kein `D:\OneDrive\...`)
- Projekt-Suffix steht in INDEX.md, nicht im Skill
- Unbekannte PCs werden registriert, nie geraten
- Den ermittelten workFolder für die gesamte Session merken

---

## 5. TOOL-ZUORDNUNG

| Aufgabe | Desktop Commander Tool |
|---------|----------------------|
| Datei lesen | `read_file` (path) |
| Datei schreiben (neu) | `write_file` (path, content, mode:"rewrite") |
| Datei anhängen | `write_file` (path, content, mode:"append") |
| Datei editieren | `edit_block` (file_path, old_string, new_string) |
| Verzeichnis listen | `list_directory` (path, depth) |
| Datei verschieben | `move_file` (source, destination) |
| Terminal-Befehl | `start_process` (command, timeout_ms) |
| Datei-Info | `get_file_info` (path) |
| Mehrere Dateien lesen | `read_multiple_files` (paths) |

### Wichtig für write_file:
- Chunking: Max 25-30 Zeilen pro Aufruf
- Erste Chunk: mode="rewrite"
- Weitere Chunks: mode="append"
- Immer absolute Pfade verwenden

---

## 5a. PowerShell-Aufrufe via DC (cc-steuerung-002)

**Regel:** KEINE `$`-Variablen in DC-PowerShell-Command-Strings verwenden.

### Problem

Der Command-String wird durch eine Shell-Schicht geschickt, die `$pc`
interpoliert **bevor** er PowerShell erreicht. Innerhalb von äußeren `"..."`
werden alle `$`-Referenzen durch leere Strings ersetzt. Ergebnis: Syntax-Fehler.

### Falsch

```powershell
powershell -Command "$pc = hostname; Write-Output $pc"
```
→ Fehler: `Die Benennung "=" wurde nicht als Name eines Cmdlet ... erkannt`

### Richtig: Sequentielle Ausgabe ohne Variablen

```powershell
powershell -NoProfile -Command "hostname; [System.Environment]::GetEnvironmentVariable('OneDrive','User')"
```

Claude parst die Ausgabe zeilenweise. Jeder Befehl wird per Semikolon
getrennt, seine Ausgabe landet als eigene Zeile im stdout.

### Richtig: Komplexe Skripte als `.ps1`-Datei

Wenn Variable-Assignments, Schleifen oder längere Logik nötig sind:

1. Skript in temporäre Datei schreiben:
   ```
   write_file(path: "C:\temp\script.ps1", content: "$pc = hostname; $od = [System.Environment]::GetEnvironmentVariable('OneDrive','User'); Write-Output "$pc|$od"", mode: "rewrite")
   ```
2. Skript ausführen:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File "C:\temp\script.ps1"
   ```
3. `.ps1`-Datei nach Ausführung löschen.

Im Skript-File werden `$`-Variablen korrekt interpretiert, weil sie nicht
mehr durch die äußere Shell-Schicht müssen.

### Auch `$env:`-Variablen betroffen

`$env:OneDrive`, `$env:COMPUTERNAME` etc. funktionieren aus dem gleichen
Grund nicht zuverlässig über DC-Command-Strings. Stattdessen:
- Für PC-Name: `hostname` (Cmdlet-Aufruf, nicht Variable)
- Für Env-Variablen: `[System.Environment]::GetEnvironmentVariable('NAME','User')`

---

## 6. ENTSCHEIDUNGSLOGIK: PLAN vs DIREKT

Claude entscheidet NICHT selbst — Claude schlägt vor, User entscheidet.

| Umfang | Claude Verhalten |
|--------|-----------------|
| 1-2 Dateien, klare Aufgabe | Direkt ausführen |
| 3+ Dateien | Per ask_user_input_v0 fragen: "Das betrifft ~N Dateien. Erst analysieren oder direkt?" Optionen: "Erst analysieren (Plan)", "Direkt ausführen", "Abbrechen" |
| Unklarer Umfang | Erst read_file/list_directory, dann Plan zeigen |

---

## 7. KONTEXT-REGELN

Projektspezifische Regeln kommen aus den Project Files und INDEX.md.
Allgemeine Regeln:
- Nie git push, nie neue Libraries ohne Freigabe
- Icons nur über projektdefinierte Ressourcen
- Naming und Patterns aus Projektstandards

---

## 8. BERECHTIGUNGEN

| Aktion | Erlaubt? | Bedingung |
|--------|----------|-----------|
| Dateien lesen | ✅ Automatisch | Bei cc/dc-Trigger |
| Verzeichnis listen | ✅ Automatisch | Bei cc/dc-Trigger |
| git status / log / diff | ✅ Automatisch | Bei cc/dc-Trigger |
| Build-Befehle | ✅ Automatisch | Bei cc/dc-Trigger |
| Dateien erstellen | ⚠️ Nur mit cc/dc-Trigger | User sagt es explizit |
| Dateien editieren | ⚠️ Nur mit cc/dc-Trigger | User sagt es explizit |
| Dateien löschen | ⚠️ Rückfrage Pflicht | Immer erst per ask_user_input_v0 fragen |
| git push | ❌ Nie | User pusht selbst |
| Packages installieren | ❌ Nie | Keine Dependencies ohne Freigabe |
| Dateien außerhalb Repo | ❌ Nie | — |

---

## 9. RÜCKGABE AN USER

### Nach Lese-Operationen:
- Relevanten Inhalt zeigen (gekürzt wenn sehr lang)

### Nach Schreib-Operationen:
1. **Was gemacht wurde** — 1-2 Sätze
2. **Commit-Vorschlag** — im git-commit-helper Format
3. **Nächster Schritt** — was als nächstes kommt

### Bei Fehlern:
- Fehlermeldung zeigen
- Lösungsvorschlag machen
- NICHT automatisch nochmal versuchen

---

## 10. VERBOTEN

- Desktop Commander aufrufen ohne expliziten cc/dc-Trigger vom User
- Dateien schreiben wenn User "zeig mir" sagt
- git push — unter keinen Umständen
- Secrets, Tokens oder Passwörter in Befehlen
- Dateien außerhalb des Projekt-Repos lesen/schreiben
- Neue Libraries/Packages installieren ohne Freigabe
- Desktop Commander für Konzepte/Planung/Diskussion nutzen
- Hardcodierte absolute Pfade verwenden (immer dynamisch ermitteln)
- Branch automatisch annehmen ohne User-Auswahl
- Branch-Auswahl als Prosa — IMMER ask_user_input_v0
- Liefer-Entscheidung (Chat/PC) als Prosa — IMMER ask_user_input_v0
- Löschen ohne ask_user_input_v0-Rückfrage
- **`bash_tool hostname` zur DC-Erkennung nutzen** — liefert immer `runsc` und sagt NICHTS über DC-Verfügbarkeit aus (cc-steuerung-001)
- **Aus `bash_tool`-Output auf "nicht in Claude Desktop" schließen** — `bash_tool` ist die interne Container-Sandbox, nicht der User-PC. DC-Verfügbarkeit wird ausschließlich über die Tool-Liste ermittelt
- **`$`-Variablen in DC-PowerShell-Command-Strings verwenden** — die äußere Shell-Schicht interpoliert `$pc` zu leerem String bevor PowerShell den Befehl sieht. Sequentielle Ausgabe per Semikolon oder `.ps1`-Datei verwenden (cc-steuerung-002)
- **`$env:OneDrive` / `$env:COMPUTERNAME` in DC-Commands** — aus dem gleichen Grund nicht zuverlässig. Stattdessen `hostname` und `[System.Environment]::GetEnvironmentVariable(...)` verwenden
