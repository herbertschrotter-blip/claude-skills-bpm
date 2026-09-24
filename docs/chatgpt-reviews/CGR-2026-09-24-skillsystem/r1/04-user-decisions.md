# Entscheidungen Herbert – Runde 1 (24.09.2026)

## Vor Runde 1 (Auswahlfragen beim Erstellen des Prompts)

| Frage | Antwort |
|---|---|
| Wo wird mit den Skills am Repo gearbeitet? | **Fast nur Claude Code** – Cowork-Teile (Artifact, Desktop Commander, Anker, Memory-Einträge) in Zusatzdateien je Skill auslagern oder streichen |
| Wie führt ChatGPT die Runde? | **Gleicher Chat** wie der Ausgangsbefund, Denkmodell, Canvas „Review Runde 1“ |
| Commit `ecaedd7` pushen? | **Jetzt pushen** |

## Nach Runde 1 (Phase 0)

| Frage | Antwort | Folge |
|---|---|---|
| Wie lesen die Skills künftig die Projektwerte? | **Skill-Profil v1** (Empfehlung) | Ein Block `## Skill-Profil` mit Version in der CLAUDE.md jedes Repos (BPM, HA_Dash_DreameX60, Skill-Repo); Werte stehen genau einmal dort, lange Regelwerke per Verweis; Schema in Runde 2 |
| Was passiert mit cc-steuerung? | **Kleiner Cowork-Adapter** (Empfehlung war „stilllegen“) | Auf rund 100 Zeilen kürzen; löst nur im Cowork-Chat bei ausdrücklichem Desktop-Commander-Wunsch aus; „Claude Code“ ist kein Auslöser mehr |
| Skills in Claude Code direkt aus dem Repo laden? | **So lassen** (Empfehlung war „erst testen“) | Verteilung bleibt beim Upload über claude.ai; Two-Place-Pflege und Lieferung (Datei/Zip, description ≤ 1024) bleiben. Die hochgeladenen Skills erscheinen weiter auch in Claude Code – auch der Cowork-Adapter; seine Description muss Claude Code deshalb ausschließen |

## Nachträge von Herbert (während Stufe B)

- „Gibt es im Netz Leitfäden für Skills? Was sind die besten? Wie soll ein Skill sein, damit er funktioniert?“ →
  recherchiert; der offizielle Anthropic-Leitfaden „Skill authoring best practices“ wird zweiter Maßstab.
- „Lass das in die nächste Runde miteinfließen. Muss ja nicht die Schlussrunde sein.“ → **Runde 2 ist keine
  Schlussrunde.**
- „Und gibt es einen Skill-Analyse-Skill?“ → offizielle Werkzeuge `skill-creator` und `claude plugin eval`; die Frage,
  wie die Skills künftig geprüft werden, geht an ChatGPT.

## Weiter

Runde 2: Abgleich mit dem offiziellen Leitfaden, Skill-Profil v1 mit Beispielen, Spezifikation skill-pflege, Eval mit
den offiziellen Werkzeugen, Skill-Analyse. Runde 3: cc-steuerung-Adapter, Liste Phase 1, INDEX neu.
