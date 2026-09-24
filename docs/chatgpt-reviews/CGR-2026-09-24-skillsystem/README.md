# CGR-2026-09-24-skillsystem — Befund der 12 Skills: Konsolidieren statt Regeln anbauen

**Thema:** `skillsystem` – Aufbau, Trigger und Neutralität der Skills. Anlass: ChatGPTs eigene Analyse aller 12 Skills
([00-ausgangsbefund-chatgpt.md](./00-ausgangsbefund-chatgpt.md)); Claude prüft sie und ergänzt eine eigene Analyse.
**Zeitraum:** 2026-09-24
**Branch:** `main`
**Vorgänger:** CGR-2026-04-skillsystem (r1–r6, Refactor-Phasen 1–5; damals im BPM-Repo archiviert, dort auf `main` nicht
mehr auffindbar)
**Status:** Abgeschlossen (24.09.2026)
**Ergebnis:** [Umbau-Plan `docs/skillsystem-umbau.md`](../../skillsystem-umbau.md), dazu je Phase eine Aufgabe in ClickUp
(Liste ClaudeSkills, siehe unten)

---

## Runden-Übersicht

### Runde 1 — Claudes Einschätzung zum Befund, eigene Analyse, Zielbild
- **Artefakte:** [r1/](./r1/)
- **Fokus:** ChatGPTs Befunde einzeln geprüft (bestätigt / teilweise / Widerspruch); eigene Befunde, vor allem die
  fehlenden Profile in allen Projekten, Querschnittsregeln in elf Kopien, veralteter Eval-Stand, cc-steuerung ohne
  Neutralisierung; Ursachen; Zielbild und Reihenfolge. Herbert arbeitet fast nur noch in Claude Code (24.09.2026).
- **Kernergebnis:** ChatGPT bestätigt E1–E10 und korrigiert sich bei cc-steuerung, Push-Prüfung und ticket. Einigkeit:
  Profile und Eval-Baseline vor dem Kürzen; skill-pflege mit Safe Patch und Refactor (Regel-Inventar); audit prüft,
  doc-pflege ändert, modul-bauplan begleitet den Modul-Lebenszyklus; eine Eval-Quelle; Querschnitt in drei Ebenen.
  Herbert entscheidet: **Skill-Profil v1** (ein Block mit Version), **cc-steuerung als kleiner Cowork-Adapter**,
  **Verteilung bleibt beim Upload über claude.ai**.

### Runde 2 — Abgleich mit den offiziellen Leitfäden, Skill-Profil v1, skill-pflege, Eval, Skill-Analyse
- **Artefakte:** [r2/](./r2/)
- **Fokus:** Die 12 Skills gegen Anthropics „Skill authoring best practices“ (Checkliste); Endfassung Skill-Profil v1 mit
  Pflichtfeldern je Skill und drei Beispielen (Heidi, BPM, Skill-Repo); Spezifikation skill-pflege mit Regel-Inventar;
  Eval mit `claude plugin eval` und `skill-creator`; wie die Skills künftig geprüft werden (Herberts Frage nach einem
  Skill-Analyse-Skill). Runde 3 folgt mit cc-steuerung-Adapter, Liste Phase 1 und INDEX neu.
- **Kernergebnis:** ChatGPT übernimmt S1–S8. Einigkeit:
  - MCP-Werkzeuge voll qualifiziert nur in Integrationsabschnitten; MUSS/NIE nur, wo es heikel ist; keine Historie in
    Skills; skill-neu wird Governance-Ablauf.
  - Skill-Profil v1 mit Checks und den Werten `none`/`fehlt`/`ref:`; `projects/` zieht in die Projekt-Repos.
  - skill-pflege mit Safe Patch und Refactor, Inventar unter `docs/skill-refactors/`.
  - `claude plugin eval` misst das Auslösen, echte Sitzungen die Konflikte mit Anthropic-Skills, `skill-creator` die
    Qualität.
  - Kein Skill-Analyse-Skill: Prüfskript, audit und skill-pflege teilen sich die Prüfung.

  Claudes Korrekturen: Stack-Referenzen bleiben; Review braucht eine eigene Config; Checks mit Pfaden; Python fehlt auf
  dem Büro-PC. Herbert entscheidet für das Skill-Repo: **Push nach jedem Commit**, **neue Nummer nur bei
  Skill-Änderungen**, **Tests zuerst als Pilot**.

### Runde 3 — Umbau-Plan
- **Artefakte:** [r3/](./r3/)
- **Fokus:** Skill-Profil v1 letzte Fassung und fertiges Profil des Skill-Repos; Orte der Projekt-Configs und Umzug von
  `projects/`; cc-steuerung als Cowork-Adapter; INDEX neu mit Verbleib der Invarianten; Prüfskript; Eval-Pilot als
  Dateien; Dateiliste Phase 1; Gesamtplan mit Abnahme je Phase
- **Kernergebnis:** ChatGPT übernimmt K1–K9 und liefert den Umbau-Plan: Skill-Profil v1 mit Checks und Pfaden, Configs
  unter `.claude/skill-config/`, cc-steuerung-Adapter mit fertiger Description, INDEX als Verzeichnis für das Auslösen,
  Prüfskript in PowerShell 7, Test-Manifest und fünf Pilotfälle, Phasen 1–7 mit Abnahme – „Serie abschließbar“. Claudes
  Schärfungen: `routing-eval` ist kein Pre-Commit-Check; Versionsquelle ist der CHANGELOG; der INDEX beeinflusst die
  Grundmessung nicht; Phase 2 läuft in drei Repos auf zwei PCs. Herbert schließt die Serie ab: Plan-Datei plus
  ClickUp-Aufgaben, Phase 1 startet sofort.

## Ergebnisse

- **Plan:** [docs/skillsystem-umbau.md](../../skillsystem-umbau.md) – Entscheidungen, neue Regeln, Tests, Phasen 1–7
- **Ausgangsbefund ChatGPT:** [00-ausgangsbefund-chatgpt.md](./00-ausgangsbefund-chatgpt.md)
- **ClickUp (Liste ClaudeSkills, Space Claude Skills Entwicklung):**

  | Phase | Aufgabe |
  |---|---|
  | 1 | [📦 Umbau 2026-09 · Phase 1 — Infrastruktur und Skill-Repo](https://app.clickup.com/t/123ztrcxedg) (in Arbeit) |
  | 2 | [📦 Umbau 2026-09 · Phase 2 — Profile der Projekte](https://app.clickup.com/t/123ztrcxedj) |
  | 3 | [📦 Umbau 2026-09 · Phase 3 — Grundmessung](https://app.clickup.com/t/123ztrcxedk) |
  | 4 | [📦 Umbau 2026-09 · Phase 4 — skill-pflege und skill-neu](https://app.clickup.com/t/123ztrcxedm) |
  | 5 | [📦 Umbau 2026-09 · Phase 5 — Querschnitt](https://app.clickup.com/t/123ztrcxedp) |
  | 6 | [📦 Umbau 2026-09 · Phase 6 — Skill für Skill verkleinern](https://app.clickup.com/t/123ztrcxedq) |
  | 7 | [📦 Umbau 2026-09 · Phase 7 — Gesamtabnahme](https://app.clickup.com/t/123ztrcxedr) |
