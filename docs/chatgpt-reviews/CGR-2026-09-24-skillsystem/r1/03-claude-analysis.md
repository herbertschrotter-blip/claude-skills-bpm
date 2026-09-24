# Einschätzung Runde 1 (Claude)

## Kurzfazit

ChatGPT übernimmt die Gegenanalyse fast vollständig: E1–E10 bestätigt, A11 (cc-steuerung), A13 (Push-Prüfung) und A20
(ticket) ausdrücklich korrigiert, die eigene Reihenfolge zugunsten „Profile und Messung vor dem Kürzen“ aufgegeben.
Neu und brauchbar: F1 Profil-Version, F2 keine zweite Projektbeschreibung, F3 INDEX als Inventar statt Regelbuch, F4 eine
klare Bedeutung von „projektneutral“; dazu konkrete Entwürfe für ein `## Skill-Profil` v1, für skill-pflege mit
Regel-Inventar (KEEP/MOVE/MERGE/REWRITE/DROP) und für eine Eval-Baseline mit 60 Fällen und einem Freigabe-Tor.
Offene Architekturfragen sieht ChatGPT keine mehr; die drei Entscheidungen der Phase 0 liegen bei Herbert.

## Zustimmung

- **Skill-Profil v1:** ein Block mit Version und Unterabschnitten; fehlende Werte werden feldweise erfragt („Profil
  ergänzen / einmalig festlegen / abbrechen“) statt „ganzes Profil anlegen?“; jeder Skill prüft nur seine Pflichtfelder;
  audit bekommt ein Modul „Profil-Vertrag“.
- **Drei Ebenen für Querschnittsregeln** (globale CLAUDE.md sehr klein, Projekt-CLAUDE.md mit dem Profil, im Skill ein
  Satz). Das ist eine Präzisierung meines Zielbilds, kein echter Widerspruch: Ich hatte dort nur Grundregeln vorgesehen,
  keine Abläufe.
- **Regel 19 neu:** „Self-contained contract, not duplicated implementation“.
- **skill-pflege:** zwei Modi; die alten harten Regeln 1–5 gelten nur noch für Safe Patch.
- **Grenze modul-bauplan ↔ audit:** fachlicher Lebenszyklus eines Moduls gegen systemweite Konsistenz; „Bauplan“ raus aus
  generischen Descriptions.
- **Evals:** eine Quelle, dieselben Fälle vor und nach dem Umbau, Freigabe-Tor.
- **Reihenfolge Phase 0–7.**

## Widerspruch und Schärfungen

1. **E8, v0.36.0:** ChatGPT hat den CHANGELOG geprüft; gemeint war die Vergabe in Git. Die Commits `4c498ce` (ticket,
   Feature) und `3a34d48` (tracker, Docs) tragen beide `[v0.36.0]`. Der Befund bleibt.
2. **F2 genauer:** „Das Profil verweist auf bestehende Abschnitte“ passt für Regelwerke (Validierungsregeln,
   Architektur). Für **Werte** (Versionsquelle, Push-Policy, Testbefehl, Standard-Branch) gilt umgekehrt: Der Wert steht
   genau einmal im Profil, die Prosa verweist darauf oder entfällt. Sonst bleibt die doppelte Wahrheit (heute Heidis
   Abschnitt „Commits“).
3. **Regel-Inventar:** Schreibt Claude das Inventar frei, kann es Regeln genauso übersehen wie beim Umschreiben. Deshalb
   (a) Regeln mechanisch vorsammeln (Marker MUSS/NIE/IMMER/Pflicht, VERBOTEN-Listen, Tabellen „IMMER als Auswahlfrage“),
   (b) Abgleich in beide Richtungen (neue Regeln im neuen Text müssen ebenfalls im Inventar stehen), (c) DROP als
   Sammelfreigabe über die Tabelle statt einer Frage je Regel (E6), (d) das Inventar als Datei mit dem Commit ablegen.
4. **Eval ausführbar machen:** 60 Fälle × 3 Wiederholungen von Hand sind für Herbert zu viel. Nötig ist ein Skript in
   Claude Code (Lauf ohne Oberfläche, erste Skill-Nutzung je Fall auswerten). Wegen des Zufalls Schwellen statt
   „100 %“: kritisch 3/3, sonst mindestens 2/3. Fälle nach Risiko verteilen: mehr für die Auffang-Skills (code-erstellen,
   doc-pflege, audit, mockup-erstellen), weniger für Befehls-Skills (ticket, tracker, chatgpt-review).
5. **Descriptions erst nach der Baseline ändern** – auch „Bauplan“ raus (E7). Sonst misst die Baseline schon den neuen Stand.
6. **chat-wechsel:** Ob Claude Code noch einen vollständigen Handover-Prompt braucht, hat Herbert am 16.09. entschieden
   (ja; v0.35.4, „Kurzform nur auf Wunsch“). Nicht wieder aufmachen, außer Herbert will es.
7. **Verteilung:** Das eigentliche Risiko sind doppelte Skills. Solange die claude.ai-Kopien aktiv sind, sieht Claude Code
   `audit` und `anthropic-skills:audit` nebeneinander. Umstellen heißt also auch: claude.ai-Kopien entfernen oder bewusst
   nur behalten, was im Chat gebraucht wird. Erst mit einem Skill testen.
8. **Ort der Tracker-Config:** `projects/<name>/` im Skill-Repo ist ein zweiter Ort für Projektwerte und bei Heidi schon
   abgedriftet (E1 d). Der Grund dafür – Werte ohne Repo-Zugriff im Chat – fällt mit „fast nur Claude Code“ weg. Vorschlag:
   ins Projekt-Repo, das Profil verweist darauf.
9. **Abstimmung mit ha-grundsatz:** Dort entstehen `module.yaml` v1 und der Modul-Steckbrief. Das Skill-Profil beschreibt
   die Arbeit im Repo (Commit, Tests, Doku, Tracker), `module.yaml` das Modul fachlich. Keine Felder doppelt; das Profil
   darf auf `module.yaml` verweisen.
10. Nebenbei: `clickup-tools.md` steht auch nicht in der Querverweis-Tabelle von tracker, nur im Abschnitt zum Laden der
    Werkzeuge (Z. 416).

## Entscheidungen für Herbert (Phase 0)

1. Profil-Vertrag: ein Block `## Skill-Profil` v1?
2. cc-steuerung: stilllegen oder kleiner Cowork-Adapter?
3. Verteilung: Skills in Claude Code direkt aus dem Repo laden – erst testen oder sofort?

## Vorschlag Runde 2 (Schlussrunde)

Ergebnisse statt weiterer Diskussion: das Schema Skill-Profil v1 mit Pflichtfeldern je Skill und einem Beispiel je Repo
(Heidi, BPM, Skill-Repo); die Spezifikation für skill-pflege Refactor mit Regel-Inventar; ein Eval-Skript samt Format der
Fälle; die endgültige Liste der Phase 1; Ort der Tracker-Config; Abgrenzung zu `module.yaml`.
