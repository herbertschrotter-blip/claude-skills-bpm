# Einschätzung Runde 3 (Claude)

## Kurzfazit

ChatGPT liefert einen umsetzbaren Umbau-Plan und übernimmt K1–K9. Der Plan enthält:
- die endgültige Fassung von Skill-Profil v1, dazu das fertige Profil des Skill-Repos
- eine Review-Config für mehrere Themen und die festen Orte `.claude/skill-config/` in jedem Projekt-Repo
- den Umzug von `projects/`: BPM und die Skill-Issues werden getrennt, Heidi wird aus dem heutigen Stand neu aufgebaut
- cc-steuerung als Cowork-Adapter mit fertiger Description
- INDEX als Verzeichnis für das Auslösen, dazu den neuen Ort jeder Invariante
- das Prüfskript in PowerShell 7
- das Test-Manifest und fünf Pilotfälle als Dateien
- die Dateiliste für Phase 1 und den Gesamtplan Phase 1–7 mit Abnahme

ChatGPT schließt mit „Serie abschließbar“.

Nachgeprüft an der Doku von `plugin eval`:
- Mindestversion Claude Code 2.1.269 (hier installiert: 2.1.278)
- `allowed_tools: [Read, Glob, Grep, Skill]` ist gültig, alle vier gehören zu den erlaubten Nur-Lese-Werkzeugen
- `experimental.evals` für einen anderen Eval-Ordner
- `min: 0` und `max: 0` für „darf nicht auslösen“
- `--tag`, `--runs`, `--ablation none`, `--no-publish`

Alle Aussagen stimmen.

## Zustimmung

Ich trage den Plan mit, bis auf die vier Schärfungen unten. Das sind Umsetzungsdetails, keine offenen Grundsatzfragen.
Die Serie ist abschließbar.

## Schärfungen für die Umsetzung

1. **routing-eval ist kein Pre-Commit-Check.** Im Profil des Skill-Repos steht
   `Pre-Commit-Checks: skill-validation; routing-eval` mit dem Geltungsbereich `[skills/**]`. Dann liefe vor jedem Commit an
   einem Skill die Eval-Suite: 15 Läufe im Pilot, später 180, jedes Mal auf Herberts Kontingent. Besser:
   - Vor dem Commit läuft nur `skill-validation`.
   - `routing-eval` wird zum Tor vor dem Upload bei claude.ai und nach jeder Änderung an einer Description oder an
     auslöserelevanten Abschnitten. Dabei nur die betroffenen Fälle (`--case`/`--tag`).
   - Die ganze Suite läuft in Phase 3 und Phase 7.
2. **Die Version nicht doppelt führen.** `Versionsquelle: profile` plus `Aktuelle-Version: 0.36.9` legt die Nummer in die
   CLAUDE.md, zusätzlich zum CHANGELOG – das widerspricht „Werte genau einmal“. Besser: `Versionsquelle: CHANGELOG.md`
   (oberster Eintrag). Dafür muss Phase 1 den CHANGELOG einmal nachziehen:
   - v0.35.2–v0.35.4 fehlen, darunter die Verhaltensänderung an chat-wechsel in v0.35.4
   - v0.36.1–v0.36.9 stammen aus der alten Regel und bekommen einen gemeinsamen Nachtrag
   - die doppelte v0.36.0 wird dort vermerkt
3. **Der INDEX beeinflusst die Grundmessung nicht.** `plugin eval` lädt nur die Skills des Plugins; `INDEX.md` gehört
   nicht dazu und liegt auch nicht in der abgeschotteten Sitzung. Der INDEX-Umbau darf deshalb auch vor dem Pilot kommen.
   ChatGPTs Reihenfolge (danach) ist trotzdem in Ordnung.
4. **Phase 2 läuft in drei Repos und auf zwei PCs.** Das Heidi-Repo liegt nicht auf dem Büro-PC
   (`C:\Users\herbe\source\HA_Dash_DreameX60`). Profil und Configs für BPM und Heidi entstehen deshalb je in einer
   Sitzung im jeweiligen Repo. Bei BPM gilt `Push-Policy: user-only`: Den Commit mit dem Profil pusht Herbert.

## Entscheidungen für Herbert (Abschluss)

1. Serie abschließen?
2. Ergebnisse übernehmen: Plan als Datei im Repo, dazu Aufgaben in ClickUp, oder nur die Zusammenfassung im Archiv?
3. Nächster Schritt: Phase 1 in einer neuen Sitzung oder gleich hier?
