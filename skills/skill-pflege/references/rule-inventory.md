# Regel-Inventar für einen Refactor

Ein Refactor darf Text entfernen, zusammenführen und umformulieren. Damit dabei keine Regel unbemerkt verloren geht,
bekommt jede Regel des alten Stands eine Zeile im Inventar, und beide Richtungen werden geprüft.

## Inhalt

- Datei
- Was als Regel zählt
- Spalten
- Zustände
- Vorsammeln
- Freigabe der DROP-Zeilen
- Prüfung in beide Richtungen
- Verweise
- Beispiel

## Datei

`docs/skill-refactors/<JJJJ-MM-TT>-<skill>.md` im Skill-Repo. Aufbau:

1. Kopf: Skill, Stand vor dem Umbau (Commit, Zeilen), Quellen
2. Zielstruktur: Dateien und ihre Abschnitte
3. Inventar-Tabelle
4. DROP-Gruppen mit Grund
5. Verweise von außen
6. Prüfung: Ergebnis von Alt→Neu, Neu→Alt, Prüfskript und Routing-Eval

Datum und Anlass stehen hier und nicht im Regeltext des Skills. Das Inventar wird zusammen mit dem Umbau committet.

## Was als Regel zählt

Eine Regel ist nicht jeder Absatz, sondern jede normative Aussage:
- was Claude tun, lassen, fragen oder prüfen soll
- Pflichtwerte und Grenzen (Längen, Namen, Formate)
- jeder Eintrag in einer Entscheidungs- oder VERBOTEN-Liste
- die Description mit ihren „Do not trigger“-Fällen
- Statusübergänge und Reihenfolgen

Erklärungen und Begründungen gehören zu der Regel, die sie begründen, und bekommen keine eigene Zeile. Ein Beispiel
zählt nur, wenn es eine Vorgabe trägt, etwa ein Pflichtformat. Steht eine Regel mehrfach im Text, bekommt jede Stelle
eine Zeile. Die weiteren Stellen werden als MERGE auf die erste geführt.

## Spalten

`| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |`

| Spalte | Inhalt |
|---|---|
| ID | `R001` … in der Reihenfolge des alten Texts; neue Regeln `N001` … |
| Alt-Ort | `Datei#Überschrift (Z. n)` im alten Stand |
| Regelkern | die Regel in einem Satz |
| Zustand | einer der sechs Zustände unten |
| Neu-Ort | `Datei#Überschrift` im neuen Stand; bei DROP leer |
| Bezug | MERGE: die ID, in der die Regel aufgeht; DROP: der Grund; sonst eine kurze Notiz, was sich ändert |
| Freigabe | nur bei DROP: die freigegebene Gruppe |
| Prüfung | `✅` gefunden; `✅ sinngemäß` bei REWRITE und MERGE |

## Zustände

| Zustand | Bedeutung |
|---|---|
| KEEP | bleibt wörtlich am selben Ort |
| MOVE | wandert wörtlich oder fast wörtlich an einen anderen Ort, oft in eine Reference |
| MERGE | geht in einer anderen Regel auf; Bezug nennt deren ID |
| REWRITE | bleibt inhaltlich und wird neu formuliert |
| DROP | entfällt; nur mit Freigabe |
| NEW | entsteht neu im neuen Text |

## Vorsammeln

Das Prüfskript (Check skill-validation im Skill-Profil) mit `-Skill <skill> -RuleInventory <Datei>` schreibt einen
Entwurf mit Kandidaten. Kandidaten sind:
- die Description
- Sätze mit Pflichtwörtern
- Listenpunkte unter VERBOTEN
- Tabellenzeilen
- nummerierte Regel-Überschriften

Eine vorhandene Datei überschreibt das Skript nicht. Die Kandidaten sind kein vollständiges Regelverständnis. Das Urteil
erledigt den Rest:
- Sätze über mehrere Zeilen zu einer Regel zusammenfassen
- Überschriften-Zeilen stehen für die Regel darunter
- Regeln ohne Pflichtwort ergänzen, z. B. Ablaufschritte oder Bedingungen im Fließtext
- jeden Kandidaten in genau einer Inventar-Zeile unterbringen

## Freigabe der DROP-Zeilen

Nicht je Regel fragen. Die DROP-Zeilen nach ihrem Grund in Gruppen fassen, zum Beispiel:
- Historie: Daten, Sitzungen, Issue-Nummern, Anlässe
- durch eine neue Regel ersetzt
- doppelt
- Erklärung ohne eigene Vorgabe
- Wissen, das Claude ohnehin hat

Je Gruppe die Liste zeigen (ID – Regelkern – Grund) und eine Auswahlfrage stellen: freigeben / einzelne behalten (IDs
nennen) / abbrechen. Behaltene Zeilen bekommen einen anderen Zustand. Geschrieben wird erst nach der Freigabe aller
Gruppen. Die Freigabe steht in der Spalte Freigabe.

## Prüfung in beide Richtungen

- **Alt→Neu:** Jede ID hat einen Zustand. Für KEEP, MOVE, REWRITE und MERGE ist der Neu-Ort im neuen Text zu finden
  (Suche nach dem Regelkern bzw. Lesen des Abschnitts).
- **Neu→Alt:** Kandidaten des neuen Stands in eine Datei im Scratchpad erzeugen. Jede normative Aussage dort gehört zu
  einer ID oder zu einer NEW-Zeile. Findet sich keine Zuordnung, gibt es zwei Möglichkeiten: Die Regel ist gewollt neu,
  dann wird eine NEW-Zeile nachgetragen. Oder sie ist beim Umbau ungewollt entstanden, dann wird sie entfernt.
- Beide Prüfungen füllen die Spalte Prüfung. Das Ergebnis und die Zahlen stehen im Abschnitt Prüfung des Inventars.

## Verweise

Verweise im Skill und aus anderen Skills zeigen auf Datei und Überschrift, nie auf Nummern. Vor dem Commit alle Skills,
`INDEX.md` und die Doku nach dem Namen des umgebauten Skills durchsuchen. Verweise, die in diesem Refactor nicht
angepasst werden, kommen unter „Verweise von außen“ in eine Tabelle: Stelle, Verweis, wann und wohin er korrigiert wird.

## Beispiel

Ausschnitt aus einem Inventar (Muster):

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R017 | SKILL.md#Nichts löschen (Z. 72) | Nichts löschen ohne Freigabe | REWRITE | SKILL.md#Grundsätze | Refactor: DROP nur mit Freigabe | | ✅ sinngemäß |
| R033 | SKILL.md#Dateiname (Z. 175) | Datei heißt exakt SKILL.md | MOVE | references/delivery.md#Was geliefert wird | | | ✅ |
| R085 | SKILL.md#VERBOTEN (Z. 598) | Zwei Lieferungen in einer Antwort | MERGE | references/delivery.md#Ein Skill je Antwort | R037 | | ✅ sinngemäß |
| R038 | SKILL.md#Ein Artifact (Z. 220) | Beispiel aus einer alten Sitzung | DROP | | Historie | Gruppe A | ✅ |
