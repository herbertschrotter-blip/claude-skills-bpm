# claude-skills-bpm

Skills für Claude (Cowork-Chat und Claude Code) und ihre Projekt-Konfigurationen. Aufbau und Regeln: `README.md`,
`INDEX.md`, `docs/project-architecture.md`. Antworten auf Deutsch.

## Review-Profil

Gilt für den Skill `chatgpt-review` in diesem Repo.

| Feld | Wert |
|---|---|
| Review-Ablage | `docs/chatgpt-reviews/` – je Serie ein Ordner `CGR-<JJJJ-MM-TT>-<thema>/`, Übersicht `docs/chatgpt-reviews/INDEX.md` |
| Themen | `ha-grundsatz` – Grundsatzregeln für Home-Assistant-Projekte und Skill `modul-bauplan` · `skillsystem` – Aufbau, Trigger und Neutralität der Skills |
| GitHub-Repo | `herbertschrotter-blip/claude-skills-bpm`; beim Thema `ha-grundsatz` zusätzlich der Referenzfall `herbertschrotter-blip/HA_Dash_DreameX60` |
| Pflicht-Block | `ha-grundsatz`: „Rahmen“ (unten) · `skillsystem`: Neutralitäts-Checkliste aus `skills/skill-neu/SKILL.md` Schritt 3a |
| Kontextquelle | `ha-grundsatz`: im Referenzfall `docs/ARCHITEKTUR.md`, `docs/DATEN.md`, `docs/HAUSREGELN.md`, `docs/ENTSCHEIDUNGEN.md`; hier `docs/ha-grundsatz/` · `skillsystem`: `INDEX.md`, `docs/project-architecture.md`, die betroffenen `SKILL.md`; höchstens 3–5 Blöcke |
| Reviewer-Rolle | `ha-grundsatz`: erfahrener Home-Assistant-Architekt (Core- und eigene Integrationen, eigene Karten und Panels, HACS) und Architekt für modulare Systeme · `skillsystem`: erfahrener Architekt für Prompts und Skills |
| Ergebnis-Ort | `ha-grundsatz`: `docs/ha-grundsatz/` (Grundsatzregeln) und `skills/modul-bauplan/` (Skill) · `skillsystem`: betroffene Skills und `CHANGELOG.md` |

### Pflicht-Block „Rahmen“ (Thema `ha-grundsatz`)

```
## Rahmen (PFLICHT-Hinweis)

- Herbert ist Home-Assistant-Einsteiger; gebaut wird mit Claude Code. Regeln müssen für ihn verständlich und für
  Claude eindeutig prüfbar sein.
- Ergebnis: (1) eine Doku „HA-Grundsatzregeln“ (Skill-Repo, docs/ha-grundsatz/), (2) der Skill „modul-bauplan“, der
  vom Konzept bis zum fertigen Dashboard führt und die Reihenfolge vorschlägt (Modi: Planen, Prüfen, Nachschlagen).
- Skills sind projektneutral: Projektwerte (Pfade, Präfixe, IDs) stehen in einem Profil der CLAUDE.md des jeweiligen
  Repos; Plattform-Spezifisches (Home Assistant) in einer eigenen Referenzdatei des Skills.
- Bestehende Apps (Referenzfall Heidi) werden nach den Grundsatzregeln von Grund auf neu gebaut – ohne Migration:
  kein Übergangscode, keine Rückwärtskompatibilität. Ihr heutiger Stand ist Referenzfall und Lernquelle.
- Umgebung: Home Assistant OS auf Raspberry Pi 5, HA 2026.9; Entwicklung auf Windows 11 mit Claude Code, Konfiguration
  über ein Samba-Laufwerk, Einspielen per Skript.
- Keine externen Ressourcen in Karten; nichts Geheimes ins Repo (Tokens, Koordinaten, Gerätekennungen).
- Sprache: Deutsch.
```
