# CGR-2026-10-09-skillsystem — projekt-anlegen als Projekt-Generator

**Thema:** `skillsystem` – projekt-anlegen soll nach wenigen gezielten Fragen einen lauffähigen Basiscode liefern
(Walking Skeleton): Bauweise, Grenze zu code-erstellen, Fragenkatalog, Grundsatz-Prüfung, Daten-Grundgerüst,
Stack-Reihenfolge.
**Zeitraum:** 2026-10-09
**Branch:** `main`
**Status:** Abgeschlossen (09.10.2026)
**Ergebnis:** Plan „projekt-anlegen als Projekt-Generator“ in [docs/skillsystem-umbau.md](../../skillsystem-umbau.md),
ClickUp-Aufgabe in der Liste ClaudeSkills

---

## Runden-Übersicht

### Runde 1 — Konzept Walking Skeleton, Bauweise A/B/C
- **Artefakte:** [r1/](./r1/)
- **Fokus:** Vorlagen + Generator vs. Claude nach Rezept vs. Mischung; Grenze zu code-erstellen; Fragen und
  Grundsatz-Prüfung; Daten-Grundgerüst; erster Stack und Abnahme
- **Kernergebnis:** Bauweise C (deterministischer Kern aus Bausteinen + Manifeste, eigenes Skript), Grenze
  „technische Funktionsfähigkeit vs. fachliches Verhalten“, drei Pflichtklärungen, nur benötigte Datenbank mit
  Schema-Version; Herbert: HA lauffähig = automatischer HA-Test, claude.ai nur Plan, Pilot Python + SQLite → HA.
  Befund Test-Isolation je Worker (Safe Patch an beiden python.md).

### Runde 2 — Pilot konkret: Erzeugungsauftrag, Bausteine, Skeleton, Prüfung, Skill-Änderungen
- **Artefakte:** [r2/](./r2/)
- **Fokus:** JSON-Schema, Bausteine und Manifest, Beispiel-Funktion und Starttest, Generator-CI, neue
  SKILL.md-Gliederung und Description, INDEX-Konfliktpaar, Vorbereitung HA-Integration
- **Kernergebnis:** Generator ohne Stack-Sonderfälle (Struktur und Checks aus Manifesten), JSON-Auftrag v1,
  strukturierter Renderer, Walking Skeleton „status“, Prepare / Verify & Publish, eigener Workflow, Regel für
  code-erstellen, Umsetzungsreihenfolge in sieben Schritten; Description-Entwurf verliert Auslöser (Klonen, deutsche
  Sätze). Herbert: noch eine Runde.

### Runde 3 — Description, neue Eval-Fälle, Ordner und Lieferung, Details
- **Artefakte:** [r3/](./r3/)
- **Fokus:** Description um 900 Zeichen mit allen Auslösern; ~10 neue Routing-Fälle; `scripts/` + `templates/`,
  Lieferung bei claude.ai, Prüfskript; Herkunftsdatei, TOML-Renderer, Linux/Windows
- **Kernergebnis:** Description 839 Zeichen mit allen Auslösern; 7 + 10 Routing-Fälle; `scripts/` + `templates/`,
  eigener Validator, claude.ai nur SKILL.md + references/; `.projekt-anlegen.json` ohne Datum; begrenzter
  TOML-Renderer mit `tomllib`-Prüfung; UTF-8 ohne BOM, LF; Veröffentlichen per `rename` ins nicht existierende Ziel,
  auf Linux und Windows getestet; unterstützte Kombinationen nur explizit und CI-getestet. Keine Blocker.

## Ergebnis

Projekt-anlegen wird ein Generator für ein Walking Skeleton: Bauweise C (deterministischer Kern aus Bausteinen mit
Manifesten, eigenes Skript mit Standardbibliothek), Grenze „technische Funktionsfähigkeit (projekt-anlegen) vs.
fachliches Verhalten (code-erstellen)“, drei Pflichtklärungen, Technik leitet Claude ab, nur die benötigte Datenbank
mit Schema-Version, Prepare / Verify & Publish, eigener CI-Workflow, Pilot Python-Werkzeug (optional SQLite), danach
HA-Integration (automatischer HA-Test). Umsetzung in sieben Schritten auf dem Zweig `umbau-projekt-anlegen`.
