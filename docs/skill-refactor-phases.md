# Skill-Refactor-Phasen — Arbeitsnahe Referenz

**Quelle:** CGR-2026-04-skillsystem-r4 ([Volltext](./chatgpt-reviews/CGR-2026-04-skillsystem/r4-chatgpt-response.md))
**Stand:** 2026-04-22
**Zweck:** Arbeitsbeschreibung der Skill-Refactor-Phasen für Claude-Sessions. Compact-Format ohne Diskussionskontext.

---

## Phase 1 — Sofort-Fixes ✅ done

Trigger-Bereinigung an 4 Skills:
- "ok" / "passt" aus `git-commit-helper` entfernt
- "antworte darauf" aus `chatgpt-review` entfernt
- Generische Alltagstrigger aus `tracker` entfernt
- Catch-all-Satz aus `code-erstellen` entfernt

**Flankierend:** Zwei-Orte-Pflege nach jedem Change (Repo + `/mnt/skills/user/`).

---

## Phase 1a — Eval-Matrix auf bereinigter Basis ✅ done

- Query-Dateien pro Skill angelegt (should-trigger / should-NOT-trigger)
- Problematische Skills priorisiert getestet
- Baseline ab hier erfasst (bewusst NACH Phase 1, nicht vor)

**Teilaufgaben:**
- 1a.1 Query-Dateien-Struktur
- 1a.2 Variante-B-PoC-Test (BPM-083)
- 1a.3 Baseline-Score (Commit `e14acee`, Skill-Repo v0.4.5)

---

## Phase 2 — Description-Schema-Refactor ✅ done

Alle 10 Skills auf Schema `Was + Use when + Do not trigger for` umgestellt. Zwei-Orte-Pflege pro Skill.

**Format:**
```yaml
description: >
  <Was-Satz>. Use when users want to <konkrete Trigger>. Do not trigger for
  <konkrete Catch-all-Risiken>.
```

---

## Phase 3 — Struktur-Refactor ✅ done

5 Subtasks:

| # | Commit | Skill | Änderung |
|---|--------|-------|----------|
| 3.1 | a680cf0 | doc-pflege | Advisory-Block aus Trigger-Identität entfernt |
| 3.2 | 5fc3d8e | code-erstellen | Delegationsblock für 5 Nachbarskills |
| 3.3 | d935aa4 | tracker | Progressive Disclosure: SKILL.md 147 Zeilen + 9 references/ |
| 3.4 | 3e63339 | skill-neu | Initial skill (11. aktiver Skill) — umbenannt von skill-creator wegen Anthropic-Namenskollision |
| 3.5 | c1277b9 | skill-pflege | Bidirektionaler Verweis auf skill-neu |

**tracker-Refactor-Reihenfolge (10 Schritte):**
1. Inventar (Abschnittsliste)
2. Link-/Verweis-Inventar (interne Abhängigkeiten)
3. Kategorisierung (Haupt vs references/)
4. Shadow-Map (alt → neu)
5. Extraktion (1:1 verschieben)
6. Konsolidierung (pro Zieldatei)
7. Neu-Schreiben Haupt-SKILL.md (nur Routing)
8. Cross-Check (kein Inhaltsverlust)
9. Zwei-Orte-Pflege
10. Query-Test

---

## Phase 4 — Memory-Integration 🟡 in progress

**Rubriken (4 Prefixe, final):**

```text
[VERIFY]         — ausstehende Prüfung / Verifikation
[ARCH-OPEN]      — offene Architektur- oder Systementscheidung
[INFRA-TODO]     — kleine Infrastruktur-/Prozessaufgabe, nicht ClickUp-würdig
[REVIEW-PENDING] — externe Rückmeldung oder Review-Antwort steht noch aus
```

**Subtasks:**
- **4.1 chat-wechsel: Memory-Scan bei Handover** (gemeinsamer Block, nicht pro Rubrik)
- **4.2 skill-neu: Memory-Disziplin** (offene Fragen → ARCH-OPEN, Verifikationen → VERIFY; umbenannt von skill-creator)
- **4.3 skill-pflege: Memory-Cleanup** (mit Bestätigung, kein stilles Remove)
- **4.4 tracker: Memory-Eskalation** (3× Handover-Wiederauftauchen → ClickUp-Task-Hinweis)
- **4.5 Rubriken-Konvention festziehen** (Doku + Retrofit der bestehenden 11 Memory-Einträge)

**Lifecycle-Regel (kritisch):**
- Memory-Eintrag gilt **NICHT** als erledigt, nur weil Claude glaubt er wäre bearbeitet
- Gilt als erledigt bei **einer** der Bedingungen:
  1. Herbert bestätigt explizit ("erledigt", "kann raus", "haken dran")
  2. Direkt durch abgeschlossenen Skill-Schritt erfüllt UND Claude nennt ihn explizit → Entfernung erst nach Bestätigung
  3. Bei Handover explizit als obsolet markiert

**Keine Auto-Logik:**
- Kein stilles Auto-Remove
- Kein Zählen "3 Chats alt = automatisch weg"

**Eskalation pragmatisch:**
- VERIFY / INFRA-TODO bei 3× aufeinanderfolgenden Handovern → Handover-Hinweis: "Dieser Punkt war jetzt in 3 Übergaben offen. Prüfen, ob ClickUp-Task sinnvoll ist."

---

## Phase 5 — Konfliktpaar-Cross-References + Abschluss-Eval 🟡 offen

- Symmetrische Cross-References in allen 7 Konfliktpaaren
- Query-Tests erneut fahren
- Ambiguitätsfälle notieren
- Letzte Schärfungen
- 5.8 Abschluss-Eval gegen Baseline

---

## Phase 6 — Chat-Anker-PoC ✅ done (out-of-band)

Nicht in ursprünglicher r4-Planung — während Phase 3 eingeführt. Komplett dokumentiert in `docs/chat-anker-konzept.md` und `skills/tracker/references/anker-system.md`.

---

## Abhängigkeiten & Reihenfolge-Begründung

- **Phase 4 vor Phase 5:** Memory-Integration erweitert Handover- und Skill-Erstellungs-Logik. Cross-References + Abschluss-Tests erst danach sinnvoll.
- **Phase 1 vor Phase 1a:** Erst offensichtlichen Müll raus, dann messen. Baseline auf bereinigter Basis.
- **Phase 3.4 vor Phase 3.5:** skill-neu muss existieren bevor skill-pflege darauf verweist.
