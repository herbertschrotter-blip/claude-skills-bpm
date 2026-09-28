---
name: cc-steuerung
description: >
  Regelt im Cowork-Chat, wie Claude über Desktop Commander direkt auf dem PC
  des Nutzers arbeitet: Dateien lesen und schreiben, Befehle in der Shell
  ausführen, das Arbeitsverzeichnis ermitteln. Legt nur fest, wie ausgeführt
  wird; der Fachskill bleibt für den Inhalt zuständig. Use when users in the
  Cowork chat say "cc" or "dc" (e.g. "cc lies", "dc: git status") or want work
  done "direkt auf den PC" or "auf Platte". Do not trigger in Claude Code
  sessions, which have their own file and shell tools, nor because a request
  mentions Claude Code, nor for normal chat answers, code blocks in chat, or
  requests without explicit cc/dc intent.
---

# cc-steuerung – Desktop Commander im Cowork-Chat

## Zweck

Im Cowork-Chat arbeitet Claude über Desktop Commander (DC) direkt auf dem PC des Nutzers: Dateien lesen und schreiben,
Befehle ausführen, die Struktur eines Repos prüfen. Dieser Skill legt fest, **wie** das geschieht (per DC, als
SUCHE/ERSETZE im Chat oder als Code-Block), nicht **was** getan wird.

- **Nur im Cowork-Chat.** In Claude Code gilt dieser Skill nicht: Dort liest, schreibt und startet Claude Befehle mit den
  eigenen Werkzeugen. Dass eine Anfrage „Claude Code“ nennt, macht sie nicht zu einem Auftrag für diesen Skill.
- **Modalität, kein Fachskill.** Den Inhalt bestimmt der Fachskill (code-erstellen, doc-pflege, mockup-erstellen,
  tracker, audit, git-commit-helper …). „Schreib die Doku mit dc“ heißt: doc-pflege schreibt, cc-steuerung liefert den
  Weg auf die Platte. Beide sind dann gleichzeitig aktiv, das ist gewollt. Ein Konflikt entsteht nur, wenn dieser Skill
  Fachlogik übernimmt oder ein Fachskill DC-Regeln selbst festlegt, statt hierher zu verweisen.
- **Einzelbefehle** wie „dc: git status“ sind der einzige Fall ohne Fachaufgabe.
- **Fach- und Projektregeln** kommen aus dem Fachskill und dem Repo, zum Beispiel Icons nur aus den Ressourcen des
  Projekts oder Namen und Muster nach dessen Standards.
- **Rollen:** Claude plant, entwirft und schlägt vor. DC führt aus. Der Nutzer gibt frei und testet selbst.

## Grundsätze

- **Fragen nur bei offener Entscheidung**, dann als Auswahlfrage. Prosa nur bei einer offenen Frage ohne feste Optionen,
  etwa nach dem Namen eines PCs.
- **Branch** nach der Branch-Policy im Skill-Profil der `CLAUDE.md`. Ohne Profil: einen in der Sitzung schon gewählten
  Branch verwenden; sonst mit `git branch -a` auflisten, per Auswahlfrage wählen lassen und für die Sitzung merken. Nie
  einen Branch annehmen, auch nicht `main`.
- **Push** nach der Push-Policy im Skill-Profil. Ohne Profil pusht der Nutzer selbst.
- **Arbeitsstand von der Platte lesen**, nicht über GitHub: Dort liegt nur der letzte Push.

## Wann ausführen

- **Nach Freigabe ist DC der Standard.** Stimmt der Nutzer einem konkreten Vorschlag zu („code bitte“, „mach“, „ok“,
  „passt“, „geht klar“, „weiter“, „los“), schreibt Claude per DC direkt auf die Platte, ohne weitere Rückfrage. Neue
  Dateien entstehen dort, nicht als Vorlage zum Kopieren.
- **Einzelbefehl mit cc oder dc** („dc: git status“, „cc lies …“, „mit cc: build ausführen“, „schreib das mit cc“,
  „schreib auf Platte“, „direkt auf den PC“): sofort per DC ausführen, ohne Konzept-Schritt. Im Cowork-Chat meinen auch
  „lass Claude Code …“, „Claude Code soll …“ und „mit/über Claude Code“ die Ausführung per DC.
- **Kein Schreibauftrag:** „zeig mir“, „erklär mir“, „wie funktioniert“, „soll ich“. Die Antwort kommt im Chat; DC
  höchstens zum Lesen.
- **SUCHE/ERSETZE im Chat** nur, wenn der Nutzer es ausdrücklich will, DC nicht verfügbar ist oder die Datei außerhalb
  eines bekannten Repos liegt. Ohne DC sonst ein Code-Block.
- **Umfang:** 1–2 Dateien und eine klare Aufgabe → direkt ausführen. Ab 3 Dateien → Auswahlfrage: erst analysieren (Plan)
  / direkt ausführen / abbrechen. Unklarer Umfang → erst lesen, dann den Plan zeigen. Claude schlägt vor, der Nutzer
  entscheidet.
- **Im Zweifel** fragen, wie geliefert wird: direkt per DC / SUCHE/ERSETZE im Chat / Code-Block.

## Arbeitsverzeichnis

Beim ersten DC-Aufruf der Sitzung:

1. PC-Name und OneDrive-Pfad in einem Befehl holen und die Ausgabe zeilenweise lesen (Zeile 1 PC-Name, Zeile 2
   OneDrive-Pfad). Der OneDrive-Pfad kommt nur aus dieser Benutzer-Umgebungsvariable, der PC-Name aus `hostname`:
   ```powershell
   powershell -NoProfile -Command "hostname; [System.Environment]::GetEnvironmentVariable('OneDrive','User')"
   ```
2. Den PC in der Tabelle der PCs in der Doku des Projekts suchen, meist im Router-Dokument wie `INDEX.md`. Dort steht
   das Suffix des Repos, nicht im Skill. Arbeitsverzeichnis = OneDrive-Pfad + `\` + Suffix.
3. Unbekannter PC: nach seinem Namen fragen, mit Zustimmung eine Zeile in die Tabelle eintragen, einen Commit nach
   git-commit-helper vorschlagen und weiterarbeiten. Nie raten.
4. Den Pfad prüfen (`Test-Path`). Existiert er nicht: Auswahlfrage (Pfad ist richtig / anderer Pfad / abbrechen). Keinen
   anderen Pfad ausprobieren.
5. Das Arbeitsverzeichnis für die Sitzung merken. Keine fest eingetragenen absoluten Pfade.

## Berechtigungen

| Aktion | Erlaubt |
|---|---|
| Dateien lesen, Verzeichnisse listen | automatisch, auch ohne Auslöser |
| `git status`, `git log`, `git diff` | automatisch |
| Build | automatisch |
| Dateien erstellen oder ändern | nach Freigabe eines konkreten Vorschlags |
| `git commit` | nach Freigabe, Format nach git-commit-helper |
| Dateien löschen | nur nach Auswahlfrage (löschen / abbrechen / andere Datei) |
| `git push` | nach der Push-Policy des Skill-Profils; ohne Profil nie |
| Pakete installieren | nie ohne Freigabe |
| Dateien außerhalb des Repos | nie; einzige Ausnahme ist eine temporäre Skriptdatei (`references/desktop-commander.md`) |

## Rückmeldung

- Nach dem Lesen: den relevanten Inhalt zeigen, bei langen Dateien gekürzt.
- Nach dem Schreiben: was gemacht wurde (1–2 Sätze), ein Commit-Vorschlag nach git-commit-helper, der nächste Schritt.
- Bei Fehlern: die Meldung zeigen und eine Lösung vorschlagen. Nicht automatisch wiederholen.

## VERBOTEN

- Diesen Skill in Claude Code anwenden oder dort Desktop Commander benutzen
- SUCHE/ERSETZE im Chat liefern, obwohl DC verfügbar und das Konzept freigegeben ist
- Schreiben auf einen unpräzisen Auslöser wie „zeig mir“ oder „wie funktioniert“
- Aus der Sandbox des Chats auf die Verfügbarkeit von DC schließen
- `$`-Variablen, auch `$env:…`, in PowerShell-Befehlen über DC
- Secrets, Tokens oder Passwörter in Befehlen
- Hartkodierte absolute Pfade
- DC für Konzepte, Planung oder Diskussion

## VERWEIS

- Bedienung von Desktop Commander (erkennen, Werkzeuge, schreiben, PowerShell, Auswahlfrage, Lieferung, alte Muster):
  `references/desktop-commander.md`
- Commit-Format: git-commit-helper. Skill-Profil: `docs/skill-profile-v1.md` im Skill-Repo.
