# Einschätzung Runde 2 (Claude)

## Kurzfazit

ChatGPT liefert baubare Entwürfe und übernimmt S1–S8 vollständig. Im Einzelnen:
- Abgleich der 12 Skills mit der Checkliste des Leitfadens.
- Auflösung der Widersprüche zwischen Leitfaden und unseren Regeln: MCP-Namen, Pflicht-Formulierungen, Historie,
  Fragepflicht.
- Skill-Profil v1 mit Checks-Abschnitt und den Werten `none`/`fehlt`/`ref:`, dazu drei Beispiele.
- Spezifikation für skill-pflege mit Inventar-Datei und dem Zustand `NEW`.
- Eval mit `claude plugin eval` für das Auslösen und `skill-creator` für die Qualität, 60 Fälle nach Risiko, Pilot mit
  Kostengrenze.
- Kein dreizehnter Skill.

Alle Aussagen zu `plugin eval`, die ich nachgeprüft habe, stimmen mit der Doku überein:
- Negativfall mit `min: 0` und `max: 0`.
- Die abgeschottete Sitzung lädt weder CLAUDE.md noch Memory, MCP-Server, andere Plugins oder andere Skills.
- `--runs`, Standard `max_turns` 10.
- Das Kostenbeispiel 0,41 $ für sechs Läufe.

## Zustimmung

- MCP-Werkzeuge: Die Kernlogik beschreibt die Handlung; ein zwingend nötiges MCP-Werkzeug steht voll qualifiziert im
  Integrationsabschnitt oder in einer Referenz. Damit ist die Spannung zur Neutralitäts-Checkliste gelöst.
- MUSS/NIE nur, wo es heikel ist (Status, Datenverlust, Geheimnisse, Push, Version, Commit-Voraussetzungen, Inventar).
- Historie raus aus den Skills, hin zu CHANGELOG, Review-Archiv oder einem Abschnitt „alte Muster“.
- skill-neu wird vom Lehrgang zum Governance-Ablauf.
- Skill-Profil v1: Werte genau einmal, `ref:` für Regelwerke, feldweises Verhalten bei fehlenden Werten.
- `projects/<name>/` verschwindet aus dem Skill-Repo (S7).
- skill-pflege:
  - Safe Patch und Refactor.
  - Inventar unter `docs/skill-refactors/`, das Datum steht dort und nicht im Skill.
  - Abgleich in beide Richtungen, DROP als Sammelfreigabe.
  - Verweise über Datei und Überschrift statt über Nummern.
  - Lieferung in `references/delivery.md`.
- Eval: zwei Ebenen. `plugin eval` misst Konflikte innerhalb unserer Skills, ein kleiner Satz echter Sitzungen die
  Konflikte mit Anthropic-Skills. `test-prompts.md` entfällt. Tests nur mit den Modellen, die Herbert wirklich nutzt.
- Kein Skill-Analyse-Skill: Ein Prüfskript liefert die mechanischen Fakten, audit urteilt, skill-pflege nutzt dieselbe
  Prüfung als Abschluss. Kein Umbenennen der Skills.

## Korrekturen

1. **code-erstellen, „References eine Ebene tief“ ❌ ist falsch.** Der Leitfaden meint Verweisketten
   (SKILL.md → a.md → b.md), nicht die Ordnertiefe; sein eigenes Beispiel legt Dateien unter `reference/finance.md` ab.
   `references/stacks/<key>.md` wird direkt aus SKILL.md geladen und erfüllt die Regel. Die Stack-Referenzen bleiben, wo
   sie sind.
2. **Synchronisierungspfad:** Auf Herberts PC liegen die von claude.ai synchronisierten Skills nicht unter
   `~/.claude/skills/synced/` (der Ordner `~/.claude/skills` existiert nicht). Die Desktop-App legt sie unter
   `AppData\Roaming\Claude\…\skills-plugin\…\skills\` ab, sie erscheinen als `anthropic-skills:<name>`. Die Kernaussage –
   claude.ai ist die Quelle, lokale Kopien werden überschrieben – stimmt.
3. **Der Abschnitt Review im Profil ist zu dünn.** chatgpt-review braucht Themen, Reviewer-Rolle, die GitHub-Repos und je
   Thema einen Pflicht-Block. Das Review-Profil dieses Repos ist deshalb eine Tabelle je Thema; in flache
   `Feld: Wert`-Zeilen passt das nicht. Vorschlag: `Review.Config: <Datei>` wie bei Tracker.
4. **Checks brauchen eine Zuordnung zu Pfaden.** „Pre-Commit-Checks: card bzw. backend nach Änderung“ im Heidi-Beispiel ist
   kein Check-Name. Vorschlag: `card: npm test; npm run lint [card/**]`, dann `Pre-Commit-Checks: card; backend` (je
   nach geänderten Pfaden).
5. **Zähler für Aufgabennummern** (früher „Nächste freie Nummer“ im Tracker-Profil) gehört in die Tracker-Config im
   Projekt-Repo.
6. **„fehlt“ bei Heidi teils ableitbar:** Die Pflichtdokumente stehen in `docs/README.md` (Spalte „Wann lesen“), die
   Aufgabenquelle ist `docs/STATUS.md` plus ClickUp. Das füllen wir beim echten Profil mit Herbert.
7. **`projects/` nicht einfach löschen:** `projects/bpm/clickup-lists.md` enthält auch die Skill-Issue-Listen des
   Skill-Repos selbst – die wandern in dessen eigene Tracker-Config. `memory-format.md` (Memory-Einträge im Cowork-Chat)
   geht in den Cowork-Adapter oder entfällt.
8. **Kosten genauer:** Laut Doku begrenzt `--max-cost-usd` nur die Schätzung nach Listenpreis, nicht das Kontingent eines
   Abos. Bei Herberts claude.ai-Konto zählen die Läufe gegen das Nutzungskontingent; eine eigene Rechnung entsteht nur bei
   einem API-Schlüssel mit Abrechnung nach Verbrauch.

## Entscheidungen für Herbert

1. Push im Skill-Repo (Wert für `Commit.Push-Policy`).
2. Versionsnummer und CHANGELOG im Skill-Repo (Wert für `Commit.Versionsregel`).
3. Evals: Pilot, volle Grundmessung oder nur von Hand.

## Vorschlag Runde 3

Umsetzbarer Umbau-Plan:
- ChatGPTs acht offene Punkte.
- Meine Korrekturen 3–7.
- Das Skill-Profil des Skill-Repos mit Herberts Werten.
