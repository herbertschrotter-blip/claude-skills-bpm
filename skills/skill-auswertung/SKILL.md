---
name: skill-auswertung
description: >
  Wertet das Skill-Log aus (Prompts und Skill-Zündungen aus Claude-Code-Hooks, Format skill-log v1) und prüft, ob die
  Skills im Alltag richtig auslösen: Zündungen je Skill, Prompts ohne Skill, Runden mit mehreren Skills, gescheiterte
  Aufrufe. Bietet Modi von Schnellblick bis Tiefenanalyse an und gibt Befunde weiter als Eval-Fälle, Skill-Issues oder
  Vorschläge zum Nachschärfen. Use when users say "skills auswerten", "skill-log auswerten", "wie zünden die Skills",
  "Fehlzündungen prüfen", "Skill-Nutzung auswerten", "welche Skills haben gezündet", or want a periodic review of real
  skill triggering across machines. Do not trigger for running claude plugin eval or benchmarking a single skill
  (skill-creator), changing a skill's text or description (skill-pflege), creating a new skill (skill-neu), read-only
  audits of code against docs (audit), or setting up, fixing or changing the logging hooks themselves.
---

# skill-auswertung – wie zünden die Skills im Alltag?

## Zweck

Das Skill-Log hält auf jedem Rechner fest, was eingegeben wurde und welcher Skill darauf gezündet hat (Format:
`docs/skill-log-v1.md` im Skill-Repo). Dieser Skill liest das Log, findet Fehlzündungen und Fehlausfälle und gibt sie
dorthin weiter, wo sie behoben werden. Er ändert selbst keinen Skill.

- **Abgrenzung:** Skill-Texte ändern → skill-pflege. Künstliche Testläufe (`claude plugin eval`, Benchmarks eines
  Skills) → Check routing-eval bzw. skill-creator. Aufgaben und Skill-Issues anlegen → tracker. Die Hooks einrichten
  oder reparieren ist keine Auswertung, sondern Arbeit am Werkzeug (`tools/skill-log/` im Skill-Repo).
- **Maßstab**, ob ein Skill hätte zünden müssen: seine Description und die Konfliktpaare in `INDEX.md` des Skill-Repos.

## Benötigte Werte

Aus dem Skill-Profil der `CLAUDE.md` des Skill-Repos, Bereich `### Skill-Log`, Feld `Config`
(`docs/skill-profile-v1.md`). Die Config nennt:

| Abschnitt | Wofür |
|---|---|
| Log-Ordner | ein Ordner je Rechner, der ausgewertet wird |
| Ausgewertet bis | Zeitpunkt der letzten Auswertung; Startpunkt für „seit letzter Auswertung“ |
| Ablage der Befunde | wohin Eval-Fälle kommen und wie Skill-Issues angelegt werden |

Läuft die Sitzung nicht im Skill-Repo, nach dessen Pfad fragen und ihn nicht raten. Fehlt die Config oder ein Abschnitt,
dieses Feld nennen und per Auswahlfrage klären: Config ergänzen / Wert einmalig nennen / abbrechen.

## Ablauf

### 1. Überblick und Modus

Das Log kurz einlesen und in einem Satz nennen, was vorliegt: Anzahl Runden seit „Ausgewertet bis“, Rechner, Zeitraum.
Liegt nichts Neues vor, das sagen und anbieten, einen früheren Zeitraum zu wählen.

Dann **eine** Auswahlrunde mit drei Fragen (was der Auftrag schon beantwortet, entfällt):

1. **Wie gründlich?**
   - *Schnellblick* – nur Zahlen: Zündungen je Skill (automatisch / per `/name`), gescheiterte Aufrufe, Anteil der
     Runden ohne Skill. Keine Bewertung einzelner Runden.
   - *Standard* (Vorschlag) – Zahlen, dazu jede Runde ohne Skill und jede Runde mit mehreren Skills bewerten.
   - *Tiefenanalyse* – wie Standard; bei jedem Verdachtsfall im Transcript nachlesen und die Ursache in der Description
     benennen, mit Formulierungsvorschlag.
2. **Welcher Bereich?** Zeitraum (seit letzter Auswertung / letzte 7 Tage / alles), Rechner (alle / einzelne), Skills
   (alle / einzelne).
3. **Was mit den Befunden passiert?** (mehrere möglich) nur Bericht / Eval-Fälle anlegen / Skill-Issues anlegen /
   Description nachschärfen.

Bei vielen Runden (über 100 ohne Skill) vor Standard oder Tiefenanalyse sagen, wie viele es sind, und anbieten, auf
Skills oder Zeitraum einzuschränken.

### 2. Einlesen

- In Claude Code das Auswertungsskript des Skill-Repos nutzen (`tools/skill-log/skill_log_report.py`, Zahlen als
  Bericht, Runden mit `--json`). Ohne Skript die JSONL-Dateien direkt lesen und Runden bilden, wie
  `docs/skill-log-v1.md` sie beschreibt.
- Mehrere Log-Ordner zusammen auswerten; `host` hält sie auseinander.

### 3. Bewerten (Standard und Tiefenanalyse)

Jede Runde ohne Skill und jede mit mehreren Skills bekommt ein Urteil:

| Urteil | Bedeutung |
|---|---|
| richtig | kein Skill nötig bzw. alle gezündeten Skills passend |
| Fehlausfall | Skill X hätte zünden müssen, hat aber nicht |
| Fehlzündung | Skill X hat gezündet, war aber nicht zuständig |
| Konflikt | zwei Skills gezündet, wo einer zuständig war (Konfliktpaar aus `INDEX.md`) |
| unklar | Grenzfall; nicht als Fehler zählen, nur aufführen |

- Kurze Zustimmungen, Rückfragen und Gespräch ohne Auftrag sind *richtig* ohne Skill; nicht einzeln aufführen, nur
  zählen.
- Runden mit genau einem Skill werden nur geprüft, wenn der Aufruf gescheitert ist (`ok: false`) oder der Nutzer es
  im Bereich verlangt.
- **Tiefenanalyse:** Für jeden Fehlausfall, jede Fehlzündung und jeden Konflikt das Transcript der Sitzung lesen
  (`session` aus dem Log). Den Satz der Description benennen, der das Verhalten erklärt oder fehlt, und einen
  Formulierungsvorschlag machen. Nur lesen – Transcripts nie ändern und nichts daraus weitergeben, was nach Geheimnis
  aussieht.

### 4. Bericht

Im Chat, knapp:
1. Zahlen: Runden, mit/ohne Skill, Tabelle je Skill (automatisch, per `/name`, Fehler).
2. Befunde (ab Standard): je Fall Datum, Projekt, Prompt (gekürzt), Urteil, zuständiger Skill; bei Tiefenanalyse die
   Ursache und der Vorschlag.
3. Muster: derselbe Skill mehrfach betroffen, dasselbe Stichwort mehrfach übersehen.

### 5. Weitergeben

Nur, was im Modus gewählt wurde, und je Befund mit Auswahlfrage (übernehmen / überspringen), außer der Nutzer gibt
alle auf einmal frei:
- **Eval-Fälle:** aus dem echten Prompt einen Fall nach den Regeln der Eval-Fälle des Skill-Repos (`quality/README.md`):
  Fehlausfall → „soll auslösen“, Fehlzündung → „darf nicht auslösen“, Konflikt → beides. Den Prompt so umformulieren,
  dass er ohne Repo-Dateien verständlich ist und keine privaten Daten enthält.
- **Skill-Issues:** über tracker (`tracker issue <skill>: …`), mit Prompt, Urteil und Vorschlag.
- **Description nachschärfen:** an skill-pflege übergeben, mit Befund und Vorschlag. Nie selbst in `skills/**`
  schreiben.

### 6. Stand festhalten

Nach der Auswertung „Ausgewertet bis“ in der Config auf den Zeitpunkt der letzten ausgewerteten Runde setzen und mit
den angelegten Eval-Fällen committen (Format und Push nach dem Skill-Profil). Beim Schnellblick nur auf Wunsch.

## VERBOTEN

- Skill-Texte oder Descriptions selbst ändern – das macht skill-pflege
- Eval-Fälle oder Skill-Issues ohne Freigabe anlegen
- Prompts mit privaten Daten oder Geheimnissen ungefiltert in Eval-Fälle, Issues oder den Bericht übernehmen
- Log- oder Transcript-Dateien ändern oder löschen
- „Ausgewertet bis“ vorrücken, ohne dass die Runden bis dahin ausgewertet wurden
- eine Runde als Fehler zählen, ohne die Description des betroffenen Skills gelesen zu haben

## VERWEIS

- Format und Einrichtung des Logs: `docs/skill-log-v1.md`; Skripte: `tools/skill-log/` (beides im Skill-Repo)
- Eval-Fälle: `quality/README.md`; Konfliktpaare: `INDEX.md`
- Ändern von Skills: skill-pflege. Aufgaben und Skill-Issues: tracker. Künstliche Testläufe: Check routing-eval im
  Skill-Profil, skill-creator.
