# PROMPT-STRUKTUR (beide Umgebungen)

Aufbau des Handover-Prompts im Cowork-Chat wie in Claude Code (`SKILL.md`, Abschnitte „ABLAUF IN CLAUDE CODE“ und
„Ablauf im Cowork-Chat“).

```
# [Projektname] Teil [N+1]

Weiterführung aus **[Projektname] Teil [N]**.

---

## Aktueller Stand
- **App-Version:** [Version]
- **Letzter Commit:** [Hash + Message]
- **Branch:** [Branch]
- **Chat-URL Teil [N]:** [aktuelle Chat-URL falls bekannt]

## Erledigt in Teil [N]
- [Erledigte Punkte/Commits]

## Offene Punkte (aus ClickUp + Chat)

### ClickUp offen (BPM: nach Liste gruppiert; Ein-Listen-Projekte: nach Status):
PlanManager:
- [Priority] [Meilenstein] <PRÄFIX>-NNN | Beschreibung
Docs:
- [Priority] [Meilenstein] <PRÄFIX>-NNN | Beschreibung
(nur Listen/Status mit offenen Tasks auflisten)

### Offene Anker aus Teil [N] (aus [ANKER-LIVE]):
| ID | Typ | Thema |
|----|-----|-------|
| TEMP-xxx | offen | Thema (noch kein Task) |
| 86c9xxx | erstellt | Thema (<PRÄFIX>-NNN) |
(nur wenn Einträge vorhanden — sonst Sektion weglassen; nur Cowork)

### Offene Punkte aus Memory (gefiltert nach Rubriken):

#### VERIFY
- [Eintragstext]

#### ARCH-OPEN
- [Eintragstext]

#### INFRA-TODO
- [Eintragstext]

#### REVIEW-PENDING
- [Eintragstext]
(leere Rubriken weglassen; wenn alle leer: ganze Sektion weglassen)

### Im Chat neu erkannt (noch nicht in ClickUp):
- Modul — Beschreibung

### Im Chat erledigt (noch nicht in ClickUp markiert):
- <PRÄFIX>-NNN | Beschreibung

### Sonstige offene Punkte (nicht in ClickUp):
- [Pending Commits]
- [Pending Doc-Updates]
- [Pending Frontmatter/Quickload-Updates]
- [Neue Fachliche Invarianten die noch eingetragen werden müssen]

## Nächste Schritte (geplant)
- [Prioritäten — basierend auf V1 + high/urgent zuerst]

## Aktive Entscheidungen
- [Architektur-Entscheidungen]
- [Offene Fragen]

## Kontext
- [Wichtige Erkenntnisse]
- [Warnungen]
- [Docs die gelesen werden sollten]
- [Docs deren Quickload/Invarianten veraltet sein könnten]

## Regeln (Erinnerung) — aus den Profilen der CLAUDE.md erzeugt, nicht fest
- Commit: <Format, Modul-Namen, Versionsquelle, Bump-Regel aus dem Commit-Profil>
- Tracker: <Präfix, Liste, Übergänge aus dem Tracker-Profil>; tracker-Skill ist einzige Schreibschnittstelle zu ClickUp
- Docs: <Pflicht-Docs, Ladereihenfolge, Aufgabenquelle aus dem Doku-Profil>
- Code: <Testbefehl, Pflicht-Branch, Auslieferung aus dem Code-Profil>
- Ein Schritt pro Antwort; nachfragen wenn Kontext fehlt → Auswahlfrage bei festen Optionen
- Wer committet: Cowork der User; Claude Code Claude selbst
(BPM ohne Profile: User committet und pusht selbst · Commit-Format [vX.Y.Z] Modul, Typ: Kurztitel · Docs Quickload-First-Pass →
Pflichtlesen → Langform · DOC-STANDARD.md · ClickUp Space "BPM Entwicklung" ist Source of Truth · Task-Nummern BPM-NNN)
```
