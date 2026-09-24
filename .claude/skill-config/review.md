# Review-Konfiguration

Für den Skill chatgpt-review in diesem Repo (Skill-Profil → Review). Ersetzt das frühere `## Review-Profil` der
CLAUDE.md.

## Allgemein

- Review-Ablage: `docs/chatgpt-reviews/` – je Serie ein Ordner `CGR-<JJJJ-MM-TT>-<thema>/`
- Übersicht: `docs/chatgpt-reviews/INDEX.md`
- GitHub-Repo: `herbertschrotter-blip/claude-skills-bpm`
- Themen: `skillsystem`, `ha-grundsatz`

## Thema: skillsystem

- Beschreibung: Aufbau, Auslösen und Neutralität der Skills
- Reviewer-Rolle: erfahrener Architekt für Prompts und Skills
- Repos: `herbertschrotter-blip/claude-skills-bpm`
- Kontextquelle: `INDEX.md`, `docs/skill-quality.md`, `docs/skill-profile-v1.md`, die betroffenen `SKILL.md`; höchstens
  3–5 Blöcke
- Pflicht-Block: die Neutralitäts-Checkliste (`skills/skill-neu/SKILL.md`, Abschnitt „Neutralitäts-Checkliste“) und die
  Qualitätsregeln aus `docs/skill-quality.md`
- Ergebnis-Ort: die betroffenen Skills und `CHANGELOG.md`; bei Umbauten `docs/skillsystem-umbau.md`

## Thema: ha-grundsatz

- Beschreibung: Grundsatzregeln für Home-Assistant-Projekte und Skill `modul-bauplan`
- Reviewer-Rolle: erfahrener Home-Assistant-Architekt (Core- und eigene Integrationen, eigene Karten und Panels, HACS)
  und Architekt für modulare Systeme
- Repos: `herbertschrotter-blip/claude-skills-bpm`; zusätzlich der Referenzfall `herbertschrotter-blip/HA_Dash_DreameX60`
- Kontextquelle: im Referenzfall `docs/ARCHITEKTUR.md`, `docs/DATEN.md`, `docs/HAUSREGELN.md`, `docs/ENTSCHEIDUNGEN.md`;
  hier `docs/ha-grundsatz/`; höchstens 3–5 Blöcke
- Ergebnis-Ort: `docs/ha-grundsatz/` (Grundsatzregeln) und `skills/modul-bauplan/` (Skill)
- Pflicht-Block „Rahmen“:

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
