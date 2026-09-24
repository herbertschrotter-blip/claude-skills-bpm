# CGR-2026-09-24-skillsystem — Befund der 12 Skills: Konsolidieren statt Regeln anbauen

**Thema:** `skillsystem` – Aufbau, Trigger und Neutralität der Skills. Anlass: ChatGPTs eigene Analyse aller 12 Skills
([00-ausgangsbefund-chatgpt.md](./00-ausgangsbefund-chatgpt.md)); Claude prüft sie und ergänzt eine eigene Analyse.
**Zeitraum:** 2026-09-24
**Branch:** `main`
**Vorgänger:** CGR-2026-04-skillsystem (r1–r6, Refactor-Phasen 1–5; damals im BPM-Repo archiviert, dort auf `main` nicht
mehr auffindbar)
**Status:** Runde 2 offen

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
- **Kernergebnis:** –
