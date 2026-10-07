# Echte Sitzungen (EXT)

`claude plugin eval` lädt nur die Skills dieses Repos. Ob unsere Skills gegen die Skills von Anthropic (skill-creator,
code-review) gewinnen und ob cc-steuerung in Claude Code still bleibt, zeigt nur eine echte Sitzung mit allem, was
Herbert sonst auch geladen hat. Festgelegt in `CGR-2026-09-24-skillsystem` Runde 3, Abschnitt 18; Teil von Phase 3 in
`docs/skillsystem-umbau.md`.

## Ablauf je Sitzung

1. In Claude Code (Desktop-App) eine **neue Sitzung** im angegebenen Repo öffnen.
2. Oben den Modus **Plan** wählen. Dann ändert Claude nichts, auch wenn ein Skill loslegt.
3. Den Testsatz **wörtlich** einfügen und abschicken.
4. Warten, bis Claude den ersten Skill aufruft (Anzeige „Skill“ mit Namen, z. B. `anthropic-skills:skill-neu` oder
   `skill-creator`) oder ohne Skill antwortet.
5. **Sofort stoppen** und notieren, welcher Skill als Erstes kam. Die Sitzung danach schließen.

Jeder Fall läuft in **drei** frischen Sitzungen, weil alle Fälle kritisch sind (Schwelle 3/3). Das sind zwölf kurze
Sitzungen; wegen des frühen Stopps kosten sie wenig vom Kontingent.

## Fälle

| ID | Prüft | Repo | Testsatz | soll auslösen | darf nicht auslösen |
|---|---|---|---|---|---|
| EXT-01 | skill-creator ↔ skill-neu | claude-workbench | Ich brauche einen neuen Skill, der Besprechungsprotokolle zusammenfasst. Leg ihn an. | skill-neu | skill-creator |
| EXT-02 | skill-creator ↔ skill-pflege | claude-workbench | Schärf die Description des tracker-Skills, damit „Aufgabe anlegen“ zuverlässig auslöst. | skill-pflege | skill-creator |
| EXT-03 | code-review ↔ audit | BPM oder Heidi | Prüf bitte, ob die Doku noch zum Code passt. Nur prüfen, nichts ändern – ich will eine Liste der Abweichungen. | audit | code-review |
| EXT-04 | modul-bauplan ↔ audit | – | entfallen: modul-bauplan ist in projekt-anlegen aufgegangen, Prüfen bleibt bei audit | – | – |
| EXT-05 | cc-steuerung in Claude Code | claude-workbench | Ich arbeite in Claude Code. Zeig mir bitte den Git-Status des Repos. | kein cc-steuerung | cc-steuerung |

Hinweis: skill-creator beschreibt sich selbst auch mit „modify and improve existing skills“ und „optimize a skill's
description“. EXT-02 ist deshalb der wahrscheinlichste Konflikt.

## Protokoll

Je Durchgang eine Datei `JJJJ-MM-TT.md` in diesem Ordner, nach diesem Muster:

```markdown
# Echte Sitzungen – JJJJ-MM-TT

- Claude-Code-Version:
- Modell:
- geladene Skills von Anthropic (z. B. skill-creator, code-review):
- Stand des Skill-Repos (Commit):

| ID | Sitzung 1 | Sitzung 2 | Sitzung 3 | Ergebnis | Notiz |
|---|---|---|---|---|---|
| EXT-01 | | | | 3/3 / FAIL | |
| EXT-02 | | | | | |
| EXT-03 | | | | | |
| EXT-05 | | | | | |
```

In die Sitzungs-Spalten kommt der erste aufgerufene Skill oder `–`, wenn keiner kam. Es genügt, Claude die Ergebnisse im
Chat zu nennen; Claude schreibt dann die Datei.
