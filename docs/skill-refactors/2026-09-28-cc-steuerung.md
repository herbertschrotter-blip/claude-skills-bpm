# Regel-Inventar – cc-steuerung – 2026-09-28

Refactor von cc-steuerung in Umbau-Phase 5, erster Punkt (`docs/skillsystem-umbau.md`): cc-steuerung wird ein kleiner
Adapter für den Cowork-Chat und löst in Claude Code nicht mehr aus. Anlass: In der Grundmessung löste cc-steuerung im Fall
`cc-not-in-claude-code` in 1 von 3 Läufen aus, weil die Description „Claude Code“ als Auslöser nennt
(`quality/baseline/grundmessung-2026-09.md`). Nach dem Refactor-Ablauf von skill-pflege
(`skills/skill-pflege/references/rule-inventory.md`). Vorgesammelt mit
`tools/validate-skills.ps1 -Skill cc-steuerung -RuleInventory …` (81 Kandidaten), danach nach Urteil zu Regeln
zusammengefasst.

- Skill: cc-steuerung
- Stand vorher: 06b52c4 (SKILL.md, 428 Zeilen, Körper 420; keine references)
- Quellen: SKILL.md

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | Zweck · Grundsätze · Wann ausführen · Arbeitsverzeichnis · Berechtigungen · Rückmeldung · VERBOTEN · VERWEIS |
| `references/desktop-commander.md` | Desktop Commander erkennen · Schreiben · PowerShell ohne `$`-Variablen · Auswahlfrage · Lieferung eines Skills |

Abkürzungen im Neu-Ort: `S` = `SKILL.md`, `D` = `references/desktop-commander.md`.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#Frontmatter (Z. 3–8) | Description: DC für Datei-, Verzeichnis- und Terminal-Operationen; Auslöser „cc“, „dc“, „Claude Code“, „direkt auf den PC“; nicht für Chat-Antworten, Code-Blöcke, ohne cc/dc-Absicht | REWRITE | S#Frontmatter | nur Cowork-Chat; „Claude Code“ vom Auslöser zum Ausschluss; „Herberts PC“ → PC des Nutzers |  | ✅ sinngemäß |
| R002 | SKILL.md#Zweck (Z. 15–17) | Legt fest, wie Claude DC nutzt, um direkt auf dem PC zu arbeiten (Dateien, Terminal, Struktur) | REWRITE | S#Zweck | auf den Cowork-Chat begrenzt |  | ✅ sinngemäß |
| R003 | SKILL.md#Vorrang (Z. 23–25) | Modalitäts-Skill: beantwortet WIE (DC, SUCHE/ERSETZE, Code-Block), nicht WAS | REWRITE | S#Zweck |  |  | ✅ sinngemäß |
| R004 | SKILL.md#Vorrang (Z. 27–32) | Rollentabelle: WAS = Fachskill, WIE = cc-steuerung | MERGE | S#Zweck | R003 |  | ✅ sinngemäß |
| R005 | SKILL.md#Vorrang (Z. 35–38) | cc-steuerung übernimmt nie einen Fachskill; „Doku mit dc“ → Inhalt bei doc-pflege, cc-steuerung liefert das WIE | REWRITE | S#Zweck |  |  | ✅ sinngemäß |
| R006 | SKILL.md#Vorrang (Z. 39–40) | Ad-hoc-Keyword-Trigger ist die einzige Lage ohne Fachaufgabe | REWRITE | S#Zweck |  |  | ✅ sinngemäß |
| R007 | SKILL.md#Vorrang (Z. 41–44) | Fachskills verweisen passiv auf cc-steuerung; kein Auslöse-Konflikt | MERGE | S#Zweck | R008 |  | ✅ sinngemäß |
| R008 | SKILL.md#Vorrang (Z. 46–49) | cc-steuerung und Fachskill gleichzeitig aktiv ist erwünscht; Konflikt nur, wenn cc-steuerung Fachlogik übernimmt oder ein Fachskill DC-Regeln selbst festlegt | REWRITE | S#Zweck |  |  | ✅ sinngemäß |
| R009 | SKILL.md#Kernregel: Umgebungs-Erkennung (Z. 53–56) | DC-Verfügbarkeit nur über die Tool-Liste erkennen, nie über `bash_tool hostname` | MOVE | D#Desktop Commander erkennen | Issue-ID im Titel entfällt |  | ✅ |
| R010 | SKILL.md#Richtig (Z. 60–62) | DC-Werkzeuge in der Tool-Liste → DC aktiv → direkt verwenden | MERGE | D#Desktop Commander erkennen | R009 |  | ✅ sinngemäß |
| R011 | SKILL.md#Richtig (Z. 63–65) | Am Chat-Start bzw. beim ersten DC-Kommando DC-Werkzeuge per `tool_search` laden, falls nicht sichtbar | MOVE | D#Desktop Commander erkennen |  |  | ✅ |
| R012 | SKILL.md#Falsch (Z. 69–72) | `bash_tool` läuft in der Sandbox (`runsc`), sagt nichts über DC | MOVE | D#Desktop Commander erkennen |  |  | ✅ |
| R013 | SKILL.md#Konsequenz bei Verwechslung (Z. 74–79) | Folge einer Verwechslung in Sitzung Teil 28: Code-Block-Modus verschenkt DC | MOVE | D#Alte Muster | DROP nicht freigegeben; ohne Sitzungsnummer als altes Muster |  | ✅ |
| R014 | SKILL.md#VERBINDLICHE REGEL (Z. 85–86) | Jede Entscheidungsfrage mit festen Optionen als `ask_user_input_v0`, keine Prosa | REWRITE | S#Grundsätze; D#Auswahlfrage | „Fragen nur bei offener Entscheidung, dann als Auswahlfrage“; Werkzeugname in D |  | ✅ sinngemäß |
| R015 | SKILL.md#Diese Fragen IMMER (Z. 92) | Branch unbekannt → Optionen aus `git branch -a` | MERGE | S#Grundsätze | R021 |  | ✅ sinngemäß |
| R016 | SKILL.md#Diese Fragen IMMER (Z. 93) | Im Zweifel Chat oder PC → SUCHE/ERSETZE, DC, Code-Block | MERGE | S#Wann ausführen | R042 |  | ✅ sinngemäß |
| R017 | SKILL.md#Diese Fragen IMMER (Z. 94) | 3+ Dateien → erst analysieren, direkt, abbrechen | MERGE | S#Wann ausführen | R070 |  | ✅ sinngemäß |
| R018 | SKILL.md#Diese Fragen IMMER (Z. 95) | Dateien löschen → löschen, abbrechen, andere Datei | MERGE | S#Berechtigungen | R082 |  | ✅ sinngemäß |
| R019 | SKILL.md#Diese Fragen IMMER (Z. 96) | Test-Path False → Pfad richtig, anderer Pfad, abbrechen | MERGE | S#Arbeitsverzeichnis | R048 |  | ✅ sinngemäß |
| R020 | SKILL.md#Prosa-Fragen NUR wenn (Z. 98–101) | Prosa nur bei offener Frage (z. B. PC-Name) oder signalisierter Präferenz | MERGE | S#Grundsätze | R014 |  | ✅ sinngemäß |
| R021 | SKILL.md#Branch-Ermittlung (Z. 107–111) | Branch: in der Sitzung bekannt → verwenden; sonst auflisten, per Auswahlfrage wählen, für die Sitzung merken; nie annehmen | REWRITE | S#Grundsätze | zuerst Branch-Policy des Skill-Profils, ohne Profil wie bisher (Phase 5: Branch aus dem Profil) |  | ✅ sinngemäß |
| R022 | SKILL.md#Claude (das Gehirn) (Z. 117–123) | Rollenbeschreibung Claude: planen, entwerfen, beraten, reviewen, Commit-Vorschläge | REWRITE | S#Zweck | DROP nicht freigegeben; als Rollen-Zeile |  | ✅ sinngemäß |
| R023 | SKILL.md#Claude (das Gehirn) (Z. 121) | Claude ruft DC direkt auf | MERGE | S#Wann ausführen | R029 |  | ✅ sinngemäß |
| R024 | SKILL.md#Desktop Commander (die Hände) (Z. 125–131) | Liste der DC-Werkzeuge | MERGE | D#Werkzeuge | R055; DROP nicht freigegeben |  | ✅ sinngemäß |
| R025 | SKILL.md#User (der Chef) (Z. 134) | Nutzer entscheidet, wie geliefert wird | MERGE | S#Wann ausführen | R042 |  | ✅ sinngemäß |
| R026 | SKILL.md#User (der Chef) (Z. 135) | Nutzer gibt Schreiboperationen frei | MERGE | S#Berechtigungen | R080 |  | ✅ sinngemäß |
| R027 | SKILL.md#User (der Chef) (Z. 136) | Nutzer pusht immer selbst | REWRITE | S#Grundsätze | Push-Policy des Skill-Profils; ohne Profil nicht pushen (Phase 5: Push aus dem Profil) |  | ✅ sinngemäß |
| R028 | SKILL.md#User (der Chef) (Z. 137) | Nutzer testet selbst | REWRITE | S#Zweck | DROP nicht freigegeben; in der Rollen-Zeile |  | ✅ sinngemäß |
| R029 | SKILL.md#2. WANN WAS EINSETZEN (Z. 143–145) | Nach Konzept-Freigabe ist DC der Standard | REWRITE | S#Wann ausführen | Issue-ID entfällt |  | ✅ sinngemäß |
| R030 | SKILL.md#2. WANN WAS EINSETZEN (Z. 145–149) | SUCHE/ERSETZE im Chat nur, wenn ausdrücklich gewünscht, DC fehlt oder die Datei außerhalb eines bekannten Repos liegt | REWRITE | S#Wann ausführen | `projects/<[PROJECT]>/`-Pfad → bekanntes Repo |  | ✅ sinngemäß |
| R031 | SKILL.md#Desktop Commander einsetzen (Z. 152) | Neue Dateien direkt auf die Platte, kein Kopieren | MERGE | S#Wann ausführen | R029 |  | ✅ sinngemäß |
| R032 | SKILL.md#Desktop Commander einsetzen (Z. 153) | XAML per DC: kein Encoding-Problem | REWRITE | D#Schreiben | DROP nicht freigegeben; als Beispiel |  | ✅ sinngemäß |
| R033 | SKILL.md#Desktop Commander einsetzen (Z. 154) | Aktuellen Code per DC lesen, nicht den letzten GitHub-Push | REWRITE | S#Grundsätze |  |  | ✅ sinngemäß |
| R034 | SKILL.md#Desktop Commander einsetzen (Z. 155–158) | Build, mehrere Dateien, git status/log/commit, Struktur prüfen per DC | MERGE | S#Berechtigungen | R079; `git commit` nach Freigabe (R080) |  | ✅ sinngemäß |
| R035 | SKILL.md#Desktop Commander einsetzen (Z. 159) | Jede Skill-Repo- oder BPM-Repo-Änderung nach Konzept-OK per DC | MERGE | S#Wann ausführen | R029; ohne Projektnamen |  | ✅ sinngemäß |
| R036 | SKILL.md#Claude OHNE DC (Z. 162–165) | Planung, Erklärung, Review, Docs im Chat ohne DC; committeten Code über GitHub lesen | MERGE | S#VERBOTEN; S#Grundsätze | R096; R033 |  | ✅ sinngemäß |
| R037 | SKILL.md#Ad-hoc-Keyword-Trigger (Z. 167–173) | Einzelbefehl mit cc/dc (z. B. „dc: git status“) → DC direkt, ohne Konzept-Schritt | REWRITE | S#Wann ausführen | Beispiel ohne Windows-Pfad |  | ✅ sinngemäß |
| R038 | SKILL.md#Default-Trigger (Z. 179–185) | Freigabe-Wörter („code bitte“, „mach“, „ok“, „passt“, „weiter“, „los“ …) → DC ohne weitere Rückfrage | MERGE | S#Wann ausführen | R029 |  | ✅ sinngemäß |
| R039 | SKILL.md#Ad-hoc Keyword-Trigger (Z. 190–194) | Wörter „cc …“, „dc …“, „schreib das mit cc“, „schreib auf platte“, „direkt auf den pc“ | MERGE | S#Wann ausführen | R037 |  | ✅ sinngemäß |
| R040 | SKILL.md#Ad-hoc Keyword-Trigger (Z. 189, 192) | Wörter „mit/über claude code“, „lass claude code“, „claude code soll“ als Auslöser | REWRITE | S#Wann ausführen | DROP nicht freigegeben; nur im Cowork-Chat |  | ✅ sinngemäß |
| R041 | SKILL.md#Diese Wörter aktivieren NICHT (Z. 196–200) | „zeig mir“, „erklär mir“, „wie funktioniert“, „soll ich“ → Antwort im Chat, DC höchstens zum Lesen | REWRITE | S#Wann ausführen |  |  | ✅ sinngemäß |
| R042 | SKILL.md#Im Zweifel (Z. 202–203) | Im Zweifel Auswahlfrage „Wie liefern?“ (DC, SUCHE/ERSETZE, Code-Block) | REWRITE | S#Wann ausführen |  |  | ✅ sinngemäß |
| R043 | SKILL.md#4.1 Pfad-Ermittlung (Z. 211–219) | Erster DC-Aufruf: `hostname` und OneDrive-Pfad des Nutzers in einem Befehl, Ausgabe zeilenweise lesen | MOVE | S#Arbeitsverzeichnis |  |  | ✅ |
| R044 | SKILL.md#4.1 Pfad-Ermittlung (Z. 221–224) | `$env:OneDrive` geht über DC nicht; `GetEnvironmentVariable` und `hostname` verwenden | MERGE | D#PowerShell ohne $-Variablen | R067 |  | ✅ sinngemäß |
| R045 | SKILL.md#4.1 Pfad-Ermittlung (Z. 226–227) | Keine `$`-Zuweisungen im Befehl | MERGE | D#PowerShell ohne $-Variablen | R061 |  | ✅ sinngemäß |
| R046 | SKILL.md#4.2 PC-Lookup in INDEX.md (Z. 231–235) | PC in der Tabelle „PCs und Arbeitsverzeichnisse“ der INDEX.md suchen; gefunden → OneDrive-Pfad + Suffix, sonst Registrierung | REWRITE | S#Arbeitsverzeichnis | Tabelle in der Doku des Projekts (meist im Router), nicht fest INDEX.md |  | ✅ sinngemäß |
| R047 | SKILL.md#4.3 Self-Registration (Z. 239–245) | Unbekannter PC: Namen erfragen, Zeile eintragen, Commit vorschlagen, weiterarbeiten | REWRITE | S#Arbeitsverzeichnis | Eintrag erst nach Zustimmung; Commit-Vorschlag nach git-commit-helper statt fester Nachricht |  | ✅ sinngemäß |
| R048 | SKILL.md#4.4 Verifikation (Z. 249–253) | Pfad prüfen; existiert er nicht → nachfragen, nicht raten, keinen anderen Pfad probieren | REWRITE | S#Arbeitsverzeichnis | Nachfrage als Auswahlfrage (R019) |  | ✅ sinngemäß |
| R049 | SKILL.md#4.5 Regeln (Z. 257) | OneDrive-Pfad nur aus der Benutzer-Umgebungsvariable | MERGE | S#Arbeitsverzeichnis | R043 |  | ✅ sinngemäß |
| R050 | SKILL.md#4.5 Regeln (Z. 258) | `hostname` identifiziert den PC | MERGE | S#Arbeitsverzeichnis | R043 |  | ✅ sinngemäß |
| R051 | SKILL.md#4.5 Regeln (Z. 259) | Keine hartkodierten absoluten Pfade | REWRITE | S#Arbeitsverzeichnis | Beispiele mit Benutzernamen entfallen |  | ✅ sinngemäß |
| R052 | SKILL.md#4.5 Regeln (Z. 260) | Projekt-Suffix steht in der Projektdoku, nicht im Skill | MERGE | S#Arbeitsverzeichnis | R046 |  | ✅ sinngemäß |
| R053 | SKILL.md#4.5 Regeln (Z. 261) | Unbekannte PCs registrieren, nie raten | MERGE | S#Arbeitsverzeichnis | R047 |  | ✅ sinngemäß |
| R054 | SKILL.md#4.5 Regeln (Z. 262) | Arbeitsverzeichnis für die Sitzung merken | REWRITE | S#Arbeitsverzeichnis |  |  | ✅ sinngemäß |
| R055 | SKILL.md#5. TOOL-ZUORDNUNG (Z. 268–278) | Tabelle Aufgabe → DC-Werkzeug | MOVE | D#Werkzeuge | DROP nicht freigegeben |  | ✅ |
| R056 | SKILL.md#Wichtig für write_file (Z. 281) | Schreiben in Teilen von höchstens 25–30 Zeilen | MOVE | D#Schreiben |  |  | ✅ |
| R057 | SKILL.md#Wichtig für write_file (Z. 282–283) | Erster Teil `rewrite`, weitere `append` | MOVE | D#Schreiben |  |  | ✅ |
| R058 | SKILL.md#Wichtig für write_file (Z. 284) | Immer absolute Pfade | MOVE | D#Schreiben |  |  | ✅ |
| R059 | SKILL.md#Artifact-Separation (Z. 288–293) | DC-Schreiben und Artifact in einer Antwort: keine Auswahlfrage im selben Block | REWRITE | D#Lieferung eines Skills | Verweis „skill-pflege Abschnitt 14a“ → `skills/skill-pflege/references/delivery.md#Cowork` |  | ✅ sinngemäß |
| R060 | SKILL.md#Artifact-Separation (Z. 295–298) | Artifact-Datei heißt exakt `SKILL.md` | MERGE | D#Lieferung eines Skills | R059; Verweis „13a“ → delivery.md |  | ✅ sinngemäß |
| R061 | SKILL.md#5a. PowerShell-Aufrufe via DC (Z. 304) | Keine `$`-Variablen in PowerShell-Befehlen über DC | MOVE | D#PowerShell ohne $-Variablen | Issue-ID entfällt |  | ✅ |
| R062 | SKILL.md#Problem (Z. 308–310) | Grund: die äußere Shell ersetzt `$…` durch leere Zeichen, Syntaxfehler | MOVE | D#PowerShell ohne $-Variablen |  |  | ✅ |
| R063 | SKILL.md#Falsch (Z. 314–317) | Beispiel `$pc = hostname` mit Fehlermeldung | MERGE | D#PowerShell ohne $-Variablen | R062 |  | ✅ sinngemäß |
| R064 | SKILL.md#Richtig: Sequentielle Ausgabe (Z. 321–326) | Befehle mit Semikolon trennen, Ausgabe zeilenweise lesen | MOVE | D#PowerShell ohne $-Variablen |  |  | ✅ |
| R065 | SKILL.md#Richtig: Komplexe Skripte (Z. 330–340) | Längere Logik als `.ps1`: schreiben, mit `-NoProfile -ExecutionPolicy Bypass -File` ausführen, danach löschen | REWRITE | D#PowerShell ohne $-Variablen | Temp-Ordner statt festem Pfad `C:\temp` |  | ✅ sinngemäß |
| R066 | SKILL.md#Richtig: Komplexe Skripte (Z. 342–343) | In der Skriptdatei funktionieren `$`-Variablen | MERGE | D#PowerShell ohne $-Variablen | R065 |  | ✅ sinngemäß |
| R067 | SKILL.md#Auch $env:-Variablen betroffen (Z. 347–350) | `$env:` ebenso betroffen; `hostname` und `GetEnvironmentVariable(…,'User')` verwenden | MOVE | D#PowerShell ohne $-Variablen |  |  | ✅ |
| R068 | SKILL.md#6. ENTSCHEIDUNGSLOGIK (Z. 356) | Claude schlägt vor, der Nutzer entscheidet | MERGE | S#Wann ausführen | R070 |  | ✅ sinngemäß |
| R069 | SKILL.md#6. ENTSCHEIDUNGSLOGIK (Z. 360) | 1–2 Dateien, klare Aufgabe → direkt ausführen | REWRITE | S#Wann ausführen |  |  | ✅ sinngemäß |
| R070 | SKILL.md#6. ENTSCHEIDUNGSLOGIK (Z. 361) | 3+ Dateien → Auswahlfrage: erst analysieren, direkt, abbrechen | REWRITE | S#Wann ausführen |  |  | ✅ sinngemäß |
| R071 | SKILL.md#6. ENTSCHEIDUNGSLOGIK (Z. 362) | Unklarer Umfang → erst lesen, dann Plan zeigen | REWRITE | S#Wann ausführen |  |  | ✅ sinngemäß |
| R072 | SKILL.md#7. KONTEXT-REGELN (Z. 368) | Projektregeln kommen aus dem Repo (Project Files, INDEX.md) | MERGE | S#Zweck | R005 |  | ✅ sinngemäß |
| R073 | SKILL.md#7. KONTEXT-REGELN (Z. 370) | Nie git push, nie neue Libraries ohne Freigabe | MERGE | S#Berechtigungen | R083; R084 |  | ✅ sinngemäß |
| R074 | SKILL.md#7. KONTEXT-REGELN (Z. 371) | Icons nur über projektdefinierte Ressourcen | REWRITE | S#Zweck | DROP nicht freigegeben; als Beispiel für Projektregeln |  | ✅ sinngemäß |
| R075 | SKILL.md#7. KONTEXT-REGELN (Z. 372) | Naming und Patterns aus Projektstandards | REWRITE | S#Zweck | DROP nicht freigegeben; als Beispiel für Projektregeln |  | ✅ sinngemäß |
| R076 | SKILL.md#8. BERECHTIGUNGEN (Z. 380) | Dateien lesen: automatisch, auch ohne Auslöser | MOVE | S#Berechtigungen |  |  | ✅ |
| R077 | SKILL.md#8. BERECHTIGUNGEN (Z. 381) | Verzeichnis listen: automatisch | MOVE | S#Berechtigungen |  |  | ✅ |
| R078 | SKILL.md#8. BERECHTIGUNGEN (Z. 382) | git status/log/diff: automatisch | MOVE | S#Berechtigungen |  |  | ✅ |
| R079 | SKILL.md#8. BERECHTIGUNGEN (Z. 383) | Build-Befehle: automatisch | MOVE | S#Berechtigungen |  |  | ✅ |
| R080 | SKILL.md#8. BERECHTIGUNGEN (Z. 384) | Dateien erstellen: nach Freigabe eines konkreten Vorschlags | MOVE | S#Berechtigungen |  |  | ✅ |
| R081 | SKILL.md#8. BERECHTIGUNGEN (Z. 385) | Dateien editieren: nach Freigabe | MOVE | S#Berechtigungen |  |  | ✅ |
| R082 | SKILL.md#8. BERECHTIGUNGEN (Z. 386) | Dateien löschen: nur nach Auswahlfrage | MOVE | S#Berechtigungen |  |  | ✅ |
| R083 | SKILL.md#8. BERECHTIGUNGEN (Z. 387) | git push: nie, Nutzer pusht selbst | REWRITE | S#Berechtigungen | nach Push-Policy des Skill-Profils, ohne Profil nie (R027) |  | ✅ sinngemäß |
| R084 | SKILL.md#8. BERECHTIGUNGEN (Z. 388) | Pakete installieren: nie ohne Freigabe | MOVE | S#Berechtigungen |  |  | ✅ |
| R085 | SKILL.md#8. BERECHTIGUNGEN (Z. 389) | Dateien außerhalb des Repos: nie | REWRITE | S#Berechtigungen | Ausnahme: die temporäre Skriptdatei (R065), die der alte Text selbst vorsah |  | ✅ sinngemäß |
| R086 | SKILL.md#Nach Lese-Operationen (Z. 395–396) | Nach dem Lesen den relevanten Inhalt zeigen | MOVE | S#Rückmeldung | DROP nicht freigegeben |  | ✅ |
| R087 | SKILL.md#Nach Schreib-Operationen (Z. 398–401) | Nach dem Schreiben: was gemacht wurde, Commit-Vorschlag (git-commit-helper), nächster Schritt | REWRITE | S#Rückmeldung |  |  | ✅ sinngemäß |
| R088 | SKILL.md#Bei Fehlern (Z. 403–406) | Fehler zeigen, Lösung vorschlagen, nicht automatisch wiederholen | MOVE | S#Rückmeldung |  |  | ✅ |
| R089 | SKILL.md#10. VERBOTEN (Z. 412) | SUCHE/ERSETZE liefern, obwohl DC da ist und das Konzept freigegeben | REWRITE | S#VERBOTEN | Issue-ID entfällt |  | ✅ sinngemäß |
| R090 | SKILL.md#10. VERBOTEN (Z. 413) | Schreiben auf einen unpräzisen Auslöser | REWRITE | S#VERBOTEN |  |  | ✅ sinngemäß |
| R091 | SKILL.md#10. VERBOTEN (Z. 414) | Schreiben bei „zeig mir“ | MERGE | S#VERBOTEN | R090 |  | ✅ sinngemäß |
| R092 | SKILL.md#10. VERBOTEN (Z. 415) | git push unter keinen Umständen | MERGE | S#VERBOTEN | R083 |  | ✅ sinngemäß |
| R093 | SKILL.md#10. VERBOTEN (Z. 416) | Secrets, Tokens, Passwörter in Befehlen | KEEP | S#VERBOTEN |  |  | ✅ |
| R094 | SKILL.md#10. VERBOTEN (Z. 417) | Dateien außerhalb des Repos lesen oder schreiben | MERGE | S#Berechtigungen | R085 |  | ✅ sinngemäß |
| R095 | SKILL.md#10. VERBOTEN (Z. 418) | Pakete ohne Freigabe installieren | MERGE | S#Berechtigungen | R084 |  | ✅ sinngemäß |
| R096 | SKILL.md#10. VERBOTEN (Z. 419) | DC für Konzepte, Planung, Diskussion | KEEP | S#VERBOTEN |  |  | ✅ |
| R097 | SKILL.md#10. VERBOTEN (Z. 420) | Hartkodierte absolute Pfade | KEEP | S#VERBOTEN |  |  | ✅ |
| R098 | SKILL.md#10. VERBOTEN (Z. 421) | Branch ohne Auswahl annehmen | MERGE | S#Grundsätze | R021 |  | ✅ sinngemäß |
| R099 | SKILL.md#10. VERBOTEN (Z. 422) | Branch-Auswahl als Prosa | MERGE | S#Grundsätze | R014 |  | ✅ sinngemäß |
| R100 | SKILL.md#10. VERBOTEN (Z. 423) | Liefer-Entscheidung als Prosa | MERGE | S#Grundsätze | R014 |  | ✅ sinngemäß |
| R101 | SKILL.md#10. VERBOTEN (Z. 424) | Löschen ohne Rückfrage | MERGE | S#Berechtigungen | R082 |  | ✅ sinngemäß |
| R102 | SKILL.md#10. VERBOTEN (Z. 425) | `bash_tool hostname` zur DC-Erkennung | REWRITE | S#VERBOTEN; D#Desktop Commander erkennen | im Kern ohne Werkzeugnamen |  | ✅ sinngemäß |
| R103 | SKILL.md#10. VERBOTEN (Z. 426) | Aus Sandbox-Ausgabe auf „nicht in Claude Desktop“ schließen | MERGE | S#VERBOTEN | R102 |  | ✅ sinngemäß |
| R104 | SKILL.md#10. VERBOTEN (Z. 427) | `$`-Variablen in PowerShell-Befehlen über DC | REWRITE | S#VERBOTEN | kurz, Einzelheiten in D |  | ✅ sinngemäß |
| R105 | SKILL.md#10. VERBOTEN (Z. 428) | `$env:…` in DC-Befehlen | MERGE | S#VERBOTEN | R104 |  | ✅ sinngemäß |
| N001 | – | Nur im Cowork-Chat; in Claude Code nie auslösen und nie Desktop Commander benutzen, dort gelten die eigenen Werkzeuge; die Nennung „Claude Code“ ist kein Auslöser | NEW | S#Frontmatter; S#Zweck; S#VERBOTEN | Phase 5, Grundmessung `cc-not-in-claude-code` |  | ✅ |

## DROP-Gruppen

Vorgeschlagen, von Herbert **nicht freigegeben** (keine Gruppe gewählt) – alle Regeln bleiben, keine DROP-Zeile:

- **Gruppe A – Historie:** R013 (Folge einer Verwechslung in einer früheren Sitzung) → als „Alte Muster“ in D. Die
  Issue-IDs in Überschriften (cc-steuerung-001, -002, -003) entfallen mit ihren Regeln (R009, R029, R061, R089), die
  Regeln selbst bleiben.
- **Gruppe B – Wissen oder Erklärung ohne eigene Vorgabe:** R022 (Rollenbeschreibung Claude), R024 (Liste der
  DC-Werkzeuge), R055 (Tabelle Aufgabe → Werkzeug), R086 (nach dem Lesen Inhalt zeigen) → Rollen-Zeile im Zweck,
  Werkzeugtabelle in D, Rückmeldung.
- **Gruppe C – Fach- und Projektregeln:** R028 (Nutzer testet selbst), R032 (XAML ohne Encoding-Problem), R074 (Icons
  aus Projektressourcen), R075 (Naming aus Projektstandards) → als Beispiele im Zweck bzw. in D.
- **Gruppe D – „Claude Code“ als Auslösewort:** R040 („mit/über claude code“, „lass claude code“, „claude code soll“) →
  bleibt als Auslöser, aber nur im Cowork-Chat; die Description schließt Claude Code als Umgebung aus.

## Verweise von außen

| Stelle | Verweis | Behandlung |
|---|---|---|
| `skills/audit/SKILL.md`, `skills/doc-pflege/SKILL.md`, `skills/mockup-erstellen/SKILL.md` | „Arbeitsverzeichnis nach cc-steuerung Kapitel 4“ | erledigt in v0.38.2 (Phase 5, Cowork-Pfadermittlung): Verweis auf den Abschnitt „Arbeitsverzeichnis“ |
| `skills/code-erstellen/SKILL.md` | „cc-steuerung Kapitel 4“, „Self-Registration (cc-steuerung 4.3)“ | erledigt in v0.38.2: kopierter Ablauf entfernt, Verweis auf den Abschnitt (`docs/skill-refactors/2026-09-28-code-erstellen.md`) |
| `skills/tracker/SKILL.md`, `skills/tracker/references/complete-task.md` | „baut auf cc-steuerung-003 auf (DC ist dort Default-Ausführungsmodus)“ | Phase 6 (tracker): auf `skills/cc-steuerung/SKILL.md#Wann ausführen` |
| `skills/chat-wechsel/SKILL.md`, `INDEX.md` Invarianten | „cc-steuerung-Pfad-/Modalitätsfragilität“ | Phase 5 (INDEX neu) bzw. Phase 6 (chat-wechsel) |
| `INDEX.md` Skill-Tabelle, Invariante 3 und 9 | Auslöser „claude code soll“, „Claude Code“; „PC-Lookup in INDEX.md“ | mit diesem Commit angepasst |
| `README.md` Skill-Tabelle und Baum | „auf Herberts PC“; nur `SKILL.md` | mit diesem Commit angepasst |

## Prüfung

- **Freigabe:** Zielstruktur und Description von Herbert am 28.09.2026 freigegeben (Auswahlfrage vor dem Schreiben).
  DROP-Gruppen A–D nicht freigegeben, alle Regeln bleiben.
- **Alt→Neu:** alle 105 alten IDs mit Zustand (KEEP 3, MOVE 23, MERGE 41, REWRITE 38, DROP 0) und N001; jeder Neu-Ort im
  neuen Text gelesen.
- **Neu→Alt:** `-RuleInventory` auf den neuen Stand: 30 Kandidaten, alle einer ID zugeordnet (Berechtigungen R076–R085
  und R034, VERBOTEN R089–R104 und N001, Werkzeuge R055, Schreiben R058, PowerShell R066). Sätze ohne Pflichtwort nach
  Urteil zugeordnet; keine ungewollt neue Regel.
- **Größe:** SKILL.md 428 → 113 Zeilen (Körper 420 → 101), dazu `references/desktop-commander.md` (59 Zeilen).
  Prüfskript 0 Fehler, Warnungen 6 → 1. Die verbleibende Warnung „kein Eval-Fall, der diesen Skill auslösen soll“ ist
  gewollt: `plugin eval` läuft in Claude Code, dort soll cc-steuerung nie auslösen.
- **Description:** 362 → 635 Zeichen.
- **Routing-Eval:** am 28.09.2026 auf d72524f, `--tag cc-steuerung` (3 Fälle × 3 Läufe, `-j 3`, 83 s, 1,84 USD):
  `cc-not-in-claude-code` (kritisch) **3/3** (Grundmessung 2/3, damit behoben), `cc-no-trigger-file-read` (kritisch,
  Negativfall) 3/3 wie in der Grundmessung, `cc-prefix-code` 2/3 (Grundmessung 3/3). Im abweichenden Lauf rief das Modell
  keinen Skill auf und endete an der Grenze von 8 Schritten; cc-steuerung löste nicht aus, es gibt keinen Konflikt.
  Wiederholung nur dieses Falls (`--case cc-prefix-code`, 52 s, 1,06 USD): 3/3, der Ausreißer war Zufall. Gesamt 8/9
  Läufe wie in der Grundmessung, aber alle Fälle über ihrer Schwelle (Grundmessung: ein kritischer Fall darunter).
  Freigabe nach `docs/skill-quality.md`, Abschnitt Verhalten: erfüllt.
- **Lieferung:** Zip mit `SKILL.md` und `references/desktop-commander.md` aus d72524f, am 28.09.2026 an Herbert zum
  Upload bei claude.ai.
- **Echte Sitzung EXT-05:** nach dem Upload zu wiederholen (Vergleichswert 3/3, `quality/real-environment/README.md`).
