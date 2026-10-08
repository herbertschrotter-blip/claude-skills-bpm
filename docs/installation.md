# Installation – Ablauf, Updates, Entfernen, Fehlerquellen

Ergänzt den Schnellstart der [README](../README.md). Die Skripte: `tools/install.ps1` (Windows), `tools/install.sh`
(Linux, macOS, Home-Assistant-Add-on), beide übergeben an `tools/einrichten.py`.

## Inhalt

- Ablauf
- Was sich selbst aktualisiert
- Entfernen
- Fehlerquellen
- Testanleitung Windows

## Ablauf

1. **Bestandsaufnahme ohne Netz:** git, `python3` (wirklich ausgeführt – die Store-Verknüpfung zählt nicht), Claude Code
   samt `%USERPROFILE%\.local\bin` bzw. `~/.local/bin`, winget, Anmeldung (`claude auth status`, Feld `loggedIn`),
   Marketplace, Plugins. Liegt `claude.exe` schon unter `.local\bin`, aber nicht im PATH, repariert das Skript nur den
   PATH und installiert nicht neu.
2. **Im Hintergrund sofort:** Marketplace auffrischen, `claude update`, git auf Updates prüfen, fehlendes git mit
   `winget download` vorladen (winget ab 1.8). Python aus dem Store lässt sich nicht vorladen.
3. **Alle Fragen auf einmal:** was installiert werden soll, Desktop-App oder Terminal, Rechnername (Vorschlag: schon
   eingerichteter Name, sonst der Windows-Computername), Sammel-Repo, `skillOverrides`, geplante Aufgabe für git-Updates.
   Danach läuft alles ohne Rückfrage.
4. **Installieren:** winget-Pakete nacheinander (Sperren, UAC), der offizielle Claude-Installer gleichzeitig in einem
   eigenen Prozess – er setzt `Set-StrictMode`, `$ErrorActionPreference = "Stop"` und endet bei Fehlern mit `exit`, was
   im selben Fenster das Skript bzw. das Fenster beenden würde.
5. **Marketplace**, dann **einrichten.py**: Plugins je Rechner, Optionen `log_host`/`log_repo`, `autoUpdate`,
   `skillOverrides`, Probe der Hooks. `einrichten.py` meldet seinen Fortschritt als `##BALKEN`-Zeilen, das Skript zeigt
   einen durchgehenden Balken.
6. **Anmeldung am Ende:** `claude plugin …` läuft auch ohne Anmeldung (geprüft 08.10.2026). Steht `loggedIn` auf
   `false`, startet `claude auth login` (Browser), danach geht es weiter. **Die Anmeldung der Claude-Desktop-App zählt
   für das CLI nicht.**

Ein erneuter Start setzt nach einem Abbruch sauber fort: Jeder Schritt prüft vorher, ob er nötig ist.

**Protokoll:** `~/.claude/workbench-einrichtung.json` hält fest, was das Skript installiert oder geändert hat
(`installiert`) und was schon da war (`war-da`). Der erste Befund bleibt – was einmal „war schon da“ war, entfernt
`--entfernen` nie.

## Was sich selbst aktualisiert

| Was | Aktualisierung |
|---|---|
| Claude Code (nativer Installer) | selbst, eingebauter Updater; das Skript stößt zusätzlich `claude update` an |
| Plugins `work`, `skill-workshop`, `work-hooks` | selbst beim Start einer Sitzung (`autoUpdate: true` im Eintrag `workbench`, setzt `einrichten.py`) |
| Python aus dem Microsoft Store | selbst über den Store (innerhalb 3.12) |
| git (winget) | **nicht** – optional die geplante Aufgabe „workbench git-Update“ (montags 9 Uhr, holt nach, wenn der Rechner aus war). git ist maschinenweit installiert, deshalb kommt beim Lauf eine UAC-Abfrage; ohne Zustimmung bleibt es beim alten Stand. Sonst: Skript erneut starten, es prüft git auf Updates |

## Entfernen

```powershell
# Windows
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.ps1))) -Entfernen
```

```sh
# Linux, macOS
curl -fsSL https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.sh | sh -s -- --entfernen
```

Nimmt nur zurück, was im Protokoll als `installiert` steht, jeweils mit Rückfrage: Plugins, Marketplace, `autoUpdate`
und die eigenen `skillOverrides` (ein seither geänderter Override bleibt), PATH-Eintrag, geplante Aufgabe; Claude Code,
git und Python nur, wenn das Skript sie installiert hat (Vorschlag „nein“). Das Skill-Log (`~/.claude/skill-log`) und
`~/.claude` bleiben; der lokale Klon des Sammel-Repos nur auf ausdrückliches Ja. Bleibt etwas übrig (abgelehnt), bleibt
das Protokoll, und ein erneutes Entfernen macht weiter.

Ohne Protokoll (Einrichtung vor 08.10.2026) von Hand: `claude plugin uninstall work@workbench` (bzw. `skill-workshop`,
`work-hooks`), `claude plugin marketplace remove workbench`, in `~/.claude/settings.json` den Eintrag `workbench` unter
`extraKnownMarketplaces` und die `anthropic-skills:…`-Einträge unter `skillOverrides` löschen.

## Fehlerquellen

Was das Skript selbst abfängt, steht mit ✓; sonst die Lösung.

| Fehler | Erkennung / Lösung |
|---|---|
| ✓ Claude Code installiert, aber `.local\bin` nicht im PATH | Skript trägt den Pfad dauerhaft in den Benutzer-PATH ein (Registry `HKCU\Environment`, als REG_EXPAND_SZ) und in die laufende Sitzung. Nie `[Environment]::SetEnvironmentVariable('Path', …, 'User')` – das schreibt REG_SZ und zerstört Einträge mit `%USERPROFILE%` |
| ✓ PATH-Änderung wirkt nicht in offenen Fenstern | Neue Fenster sehen ihn; die **Claude-Desktop-App neu starten**, damit die Hooks `python3` finden |
| ✓ Nicht angemeldet | `claude auth login` am Ende; die Desktop-App-Anmeldung zählt fürs CLI nicht |
| ✓ winget fehlt oder ist alt (Windows LTSC/Server, alter App-Installer) | Meldung; App-Installer aus dem Microsoft Store holen oder git/Python von Hand installieren |
| ✓ Microsoft Store per Gruppenrichtlinie gesperrt (Firmenrechner), Store-Zustimmung/Region | Meldung mit der winget-Ausgabe. Lösung: Python von python.org **und** den Befehl `python3` bereitstellen (siehe nächste Zeile) oder IT fragen |
| ✓ App-Ausführungsalias `python3` abgeschaltet / nur python.org-Python (`python`, aber kein `python3`) | Skript erkennt es und meldet es. Lösung: Einstellungen → Apps → Erweiterte App-Einstellungen → App-Ausführungsaliase → „python3.exe“ einschalten (Store-Python), bzw. Store-Python installieren lassen |
| ✓ PowerShell im Constrained Language Mode (AppLocker/WDAC) | Abbruch mit Meldung (`$ExecutionContext.SessionState.LanguageMode`); IT fragen |
| ✓ Execution Policy | `irm … \| iex` ist nicht betroffen; für `-File` steht `-ExecutionPolicy Bypass` im Aufruf |
| ✓ TLS 1.2 unter Windows PowerShell 5.1 | Skript schaltet TLS 1.2 zu |
| ✓ PowerShell „Als Administrator“ oder als anderer Benutzer | Rückfrage; eingerichtet wird immer für das Profil des laufenden Kontos → normales Fenster verwenden |
| ✓ PowerShell ISE | ohne Balken, Hinweis; besser ein normales Fenster |
| ✓ Mehrere Claude-Installationen (npm und nativ) | Hinweis; prüfen mit `claude doctor` |
| ✓ Kaputte `~/.claude/settings.json` | `einrichten.py` meldet Zeile/Spalte, ändert nichts; reparieren oder `settings.json.bak` zurückholen |
| ✓ Verwaltete Einstellungen (`managed-settings`, `strictKnownMarketplaces`) erlauben den Marketplace nicht | Meldung; IT fragen |
| ✓ Download von Claude Code scheitert (Region, Proxy, Firewall, Virenscanner blockiert `claude.exe`) | Meldung mit den letzten Zeilen des Installers; Region: [unterstützte Länder](https://www.anthropic.com/supported-countries); Proxy: `HTTPS_PROXY` setzen; Virenscanner: Ausnahme für `%USERPROFILE%\.local\bin` |
| ✓ ARM64-Windows | Hinweis; Claude Code und Store-Python haben ARM64-Fassungen |
| ✓ Abbruch mitten drin | Skript erneut starten, es setzt fort |
| Benutzerordner mit Leerzeichen/Umlauten, OneDrive-umgeleitete Ordner | Argumente werden gequotet; `.claude` liegt immer unter `%USERPROFILE%`, nicht unter OneDrive. Bei Problemen den Pfad in der Fehlermeldung prüfen |
| Proxy für git | `git config --global http.proxy …` |

## Testanleitung Windows

1. Normales PowerShell-Fenster (nicht ISE, nicht „Als Administrator“).
2. `irm https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.ps1 | iex`
   (direkt nach einem Push kann GitHub noch einige Minuten den alten Stand liefern – dann die Adresse mit dem
   Commit-Hash statt `main` verwenden).
3. Prüfen: Balken läuft in einer Zeile; alle Fragen kommen am Anfang; danach keine Rückfrage mehr bis zur Anmeldung;
   am Ende „FERTIG“.
4. Neues Fenster: `claude --version` (PATH dauerhaft), `claude plugin list`, `Get-Content ~\.claude\workbench-einrichtung.json`.
5. Skript noch einmal starten: alles „OK“, nichts wird neu installiert.
6. Optional: `Get-ScheduledTask 'workbench git-Update'`.
7. Optional Entfernen (siehe oben) und danach erneut einrichten.
