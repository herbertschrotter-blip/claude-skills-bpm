# Skill-Qualität

Verbindliche Regeln für alle Skills dieses Repos. Neue Skills (skill-neu) und Änderungen (skill-pflege) werden daran
gemessen. Das Mechanische prüft `tools/validate-skills.ps1`, was ein Urteil braucht, prüft audit. Grundlage sind Anthropics
[Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) und
die Review-Serie [CGR-2026-09-24-skillsystem](./chatgpt-reviews/CGR-2026-09-24-skillsystem/README.md).

## Inhalt

- Verbindliche Qualitätsregeln: Aufbau, Inhalt, Neutralität, Zusammenspiel
- Feste Begriffe
- Skill-Prüfung: mechanisch, Urteil, Verhalten
- Dokumentationsregeln

## Verbindliche Qualitätsregeln

### Aufbau

- **Frontmatter:**
  - `name`: kebab-case, höchstens 64 Zeichen, gleich dem Ordnernamen, ohne „anthropic“ und „claude“
  - `description`
- **Description:**
  - sagt, was der Skill tut und wann er gebraucht wird
  - dritte Person, konkrete Stichwörter
  - ein Teil „Do not trigger for …“ (Hausregel)
  - höchstens 1024 Zeichen (Grenze des Uploads bei claude.ai)
  - keine spitzen Klammern
  - Projekte nicht als Zuständigkeit
- **SKILL.md-Körper unter 500 Zeilen.** Abläufe, die nur einen Befehl, eine Umgebung, eine Integration oder einen Stack
  betreffen, stehen in `references/`.
- **References** werden direkt aus SKILL.md verlinkt; keine Kette SKILL.md → A → B. Eine Reference über 100 Zeilen beginnt
  mit einem Inhaltsverzeichnis.

### Inhalt

- **Knapp:** Nur hinein, was Claude nicht ohnehin weiß.
- **Keine Historie im Regeltext:** keine Daten, Sitzungen, Issue-Nummern oder Versionsstände. Historie gehört in den
  CHANGELOG, ins Review-Archiv oder in einen Abschnitt „Alte Muster“ einer Reference.
- **Freiheitsgrad nach Fragilität:** MUSS und NIE nur bei Status, Datenverlust, Geheimnissen, Push, Version und
  Commit-Voraussetzungen. Wo Urteil gefragt ist (Doku schreiben, Mockup), Spielraum lassen.
- **Eine Standardlösung** vorgeben statt vieler Optionen.
- **Beispiele** konkret und als Beispiel gekennzeichnet.
- **Einheitliche Begriffe** (Tabelle unten).

### Neutralität

- **Handlung statt Werkzeug:** „Auswahlfrage“, „Shell“, „Datei lesen“. Ein MCP-Werkzeug, ohne das die Handlung nicht geht,
  steht voll qualifiziert (`Server:tool`) im Integrationsabschnitt oder in einer Reference.
- **Keine Projektwerte im Skill:** Pfade, IDs, Präfixe, Doc-Namen und Befehle kommen aus dem Skill-Profil des Projekts
  ([skill-profile-v1.md](./skill-profile-v1.md)) oder aus seinen Configs unter `.claude/skill-config/`.
- **Kein Stack im Kern:** Stack-Details stehen in `references/stacks/<key>.md`.
- **Fehlt ein benötigter Wert:** nur nach diesem Wert fragen (Profil ergänzen / einmalig nennen / abbrechen), nie raten.
- **Hauptumgebung ist Claude Code.** Was nur im Cowork-Chat gilt (Artifact, Desktop Commander, Memory-Einträge,
  Chat-Anker), steht in einer Reference für Cowork.

### Zusammenspiel

- **Fragen** nur, wenn nach Auftrag, Profil, Regel und Kontext eine echte Entscheidung offen ist – dann mit dem
  Auswahlwerkzeug der Umgebung.
- **Querschnittsregeln nicht kopieren.** Sprache, Branch, Repo-Wurzel, Push und Fragen stehen in der CLAUDE.md bzw. im
  Skill-Profil; ein Skill nennt sie höchstens in einem Satz.
- **Eigenständigkeit:** *Self-contained contract, not duplicated implementation.* Jeder Skill macht Zweck, Grenzen,
  benötigte Werte und Kernregeln selbst klar. Detailabläufe darf er verlinken.
- **Verweise auf andere Skills** über Datei und Überschrift, nie über Nummern wie Kapitel, Regel, Modus oder Schritt.

## Feste Begriffe

| Begriff | Bedeutung | Nicht verwenden |
|---|---|---|
| Auswahlfrage | Frage mit anklickbaren Optionen | Werkzeugnamen im Regeltext |
| Aufgabe | Eintrag im Tracker (ClickUp) | Task (außer in Werkzeug- und Feldnamen) |
| Ticket | Fehler-Ticket eines Projekts (Skill ticket) | Ticket für eine Tracker-Aufgabe |
| Skill-Profil | Block `## Skill-Profil` in der CLAUDE.md eines Repos | Projektprofil, Commit-Profil, Projekt-Config |
| Config | Datei unter `.claude/skill-config/` im Projekt-Repo | `projects/<name>/` |
| Grundmessung | Eval-Lauf der unveränderten Skills vor einem Umbau | – |

## Skill-Prüfung

### Mechanisch – `tools/validate-skills.ps1`

```powershell
pwsh -NoProfile -File tools/validate-skills.ps1                     # alle Skills
pwsh -NoProfile -File tools/validate-skills.ps1 -Skill tracker      # nur geänderte Skills
pwsh -NoProfile -File tools/validate-skills.ps1 -JsonPath quality/results/skill-validation.json
```

- **Fehler (Exit 1):** Frontmatter, Name, Description, tote Verweise, doppelte Namen, fehlende zentrale Dateien,
  unbekannte Profil-Version.
- **Warnungen (Exit 0):** Länge, Inhaltsverzeichnis, Historie, Werkzeugnamen einer Umgebung, Nummern-Querverweise,
  Windows-Pfade, Projektbegriffe, Altlasten, fehlende Eval-Fälle.
- **Exit 2:** Das Skript selbst ist gescheitert.
- **Wann:** vor jedem Commit, der `skills/**` berührt, für die geänderten Skills.

### Urteil – audit

audit beurteilt, was kein Skript kann:
- Ist die Description zu breit oder zu eng?
- Kollidiert sie trotz anderer Wörter mit einem anderen Skill?
- Braucht es die Regel? Passt ihr Freiheitsgrad?
- Ist der Skill projektneutral? Sind zwei Regeln inhaltlich doppelt?
- Ist ein Beispiel veraltet?
- Ist der Schnitt in Kern und References sinnvoll?
- Ist der Skill eine eigene Fähigkeit wert?
- Sind die Eval-Fälle realistisch?

### Verhalten

- **`claude plugin eval`** misst, welcher unserer Skills auslöst.
  - Fälle unter `quality/evals/`, Test-Manifest `.claude-plugin/plugin.json`.
  - Pflicht vor dem Upload bei claude.ai und nach jeder Änderung an einer Description oder an auslöserelevanten
    Abschnitten; dann nur die betroffenen Fälle (`--case`/`--tag`). Die ganze Suite läuft vor und nach einem großen Umbau.
  - Schwellen: kritische Fälle 3 von 3 Läufen, sonst mindestens 2 von 3.
  - Freigabe eines Umbaus:
    - kein kritischer Fall unter 3/3
    - kein bestandener Negativfall kippt
    - die Gesamtquote liegt nicht unter der Grundmessung
    - neue Konflikte sind erklärt
    - das Prüfskript meldet keine neuen Fehler
- **Echte Sitzungen** für Konflikte mit Skills, die `plugin eval` nicht lädt (Anthropic-Skills wie `skill-creator` und
  `code-review`): Protokoll unter `quality/real-environment/<Datum>.md`.
- **`skill-creator`** misst die Qualität eines einzelnen Skills (mit/ohne Skill, Description-Optimierung). Seine Skripte
  brauchen Python.
- **Kosten:** Jeder Lauf ist eine echte Claude-Sitzung und zählt gegen das claude.ai-Kontingent. `--max-cost-usd` begrenzt
  nur eine Schätzung nach Listenpreis.

## Dokumentationsregeln

- `INDEX.md` ist das Verzeichnis der Skills: Zuständigkeiten, Konfliktpaare, Verweise auf die Regelquellen – kein zweites
  Regelbuch.
- `README.md` ist der Einstieg.
- `CHANGELOG.md`: ein Eintrag je Versionsnummer. Eine neue Nummer gibt es nur bei einer Skill-Änderung; der oberste
  Eintrag ist die aktuelle Version.
- Review-Serien liegen unter `docs/chatgpt-reviews/`, Regel-Inventare von Refactors unter `docs/skill-refactors/`.
- Regeln tragen keine Historie; Daten und Anlässe gehören in diese Archive.
