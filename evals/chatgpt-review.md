# Eval: chatgpt-review

## Skill-Description (aktuell)

```yaml
description: >
  Erstellt strukturierte Prompts für ein technisches Review-Gespräch zwischen
  Claude und ChatGPT. Use when users want a ChatGPT review prompt, a cross-LLM
  second opinion, a reply prompt for an ongoing ChatGPT review exchange, or a
  synthesized response to ChatGPT feedback. Do not trigger for normalen
  Chat-Handover, allgemeine Prompts ohne ChatGPT-Bezug, or vague replies like
  "antworte darauf" without explicit review context.
```

Stand: `ea6895f` — 2026-04-21 (Phase 1.2)

---

## Query-Katalog

### should_trigger

| # | Query | Typ | Notiz |
|---|-------|-----|-------|
| 1 | `besprich das mit ChatGPT` | [golden] | Teil 10 — Standard-Trigger |
| 2 | `lass ChatGPT drüberschauen` | [golden] | Teil 10 |
| 3 | `erstelle mir einen ChatGPT Review Prompt` | [golden] | Teil 22 |
| 4 | `zweite Meinung von ChatGPT` | [golden] | Teil 10 |
| 5 | `Cross-Review mit ChatGPT` | [golden] | Teil 10 |
| 6 | `Runde 3 erstellen` | [golden] | Teil 1 — Folgeprompt in laufendem Review |
| 7 | `ChatGPT hat geantwortet, was jetzt?` | [synthetic] | explizite Review-Reaktion |
| 8 | `erstelle den Folgeprompt für ChatGPT` | [synthetic] | explizit Folgeprompt |
| 9 | `ChatGPT sagt X, was antwortest du?` | [synthetic] | explizite Review-Reaktion |

### should_not_trigger

| # | Query | Typ | Notiz |
|---|-------|-----|-------|
| 1 | `antworte darauf` | [golden] | Teil 22 — war unerwünschter Trigger, Phase 1.2 Fix |
| 2 | `reagier darauf` | [synthetic] | generische Reaktions-Aufforderung |
| 3 | `was sagst du dazu?` | [synthetic] | Frage an Claude, nicht Review-Intent |
| 4 | `ok` | [synthetic] | Zustimmung |

### other_skill

| # | Query | Typ | Erwarteter Skill | Notiz |
|---|-------|-----|------------------|-------|
| 1 | `neuer chat` | [golden] | `chat-wechsel` | Übergabe ≠ Review |
| 2 | `mach mir einen prompt für GPT zu einem anderen Thema` | [synthetic] | — (kein Skill) | Prompt-Engineering ohne Review-Kontext |
| 3 | `schreib mir einen commit-message-prompt` | [synthetic] | `git-commit-helper` | Commit ≠ Review |

### ambiguous

| # | Query | Typ | Interpretation A | Interpretation B | Notiz |
|---|-------|-----|------------------|------------------|-------|
| 1 | `antworte darauf` (während laufendem ChatGPT-Review) | [synthetic] | triggert (Review-Kontext erkennbar) | triggert nicht (Description fordert "explicit review context") | Kontext-Erkennung erforderlich — ist "explicit" strikt wörtlich oder per Chat-Verlauf? |
| 2 | `Gegenmeinung bitte` | [synthetic] | triggert (cross-LLM second opinion) | triggert nicht (kein ChatGPT genannt) | "cross-LLM second opinion" aus Description, aber ohne ChatGPT-Nennung |

---

## Run-Log

### baseline

- date: 2026-04-21
- tester: Claude Opus 4.7 (Blind-Modus — nur Name + Description)
- should_trigger: 8/9
- should_not_trigger: 4/4
- other_skill: 2/3
- ambiguous: _dokumentiert_
- notes:
  - Query 6 `Runde 3 erstellen`: Ohne Chat-Kontext kein erkennbarer ChatGPT-Bezug. Description fordert "ongoing ChatGPT review exchange" — für einen blinden Router nicht ableitbar aus 3 Wörtern. Phase-2-Hinweis: "Runde N" als Keyword aufnehmen, oder akzeptieren dass dieser Query nur kontextbasiert triggert.
  - Query other_skill 2 `mach mir einen prompt für GPT zu einem anderen Thema`: Grenzfall — "GPT" statt "ChatGPT", plus "anderes Thema" als Ausschluss-Hinweis. Im Blind-Modus mehrdeutig gewertet, daher als Fehltrigger.
  - Ausschluss bei `antworte darauf` / `reagier darauf` / `was sagst du dazu?` / `ok` greift sauber.

### after-refactor

- date: 2026-04-24
- tester: Claude Opus 4.7 (Selbst-Simulation, kein echter API-Blind-Run)
- methode: Zwei Durchläufe — Blind-Modus (nur Name + Description) und Vollmodus (inkl. Body-Delegations-Tabelle aus Phase 5.6)
- commit-range: baseline `ea6895f` → after `5c88d8d` (Phase 5.6 added symmetrische Delegations-Tabelle)
- confidence: mittel — Selbst-Simulation, methodische Grenze offen dokumentiert (siehe notes)

#### Blind-Modus (Description-only)

- should_trigger: 8/9
- should_not_trigger: 4/4
- other_skill: 2/3
- ambiguous: _dokumentiert_
- delta vs baseline: ±0 — Description in Phase 5 nur marginal angepasst (Wording nahe Baseline)

#### Vollmodus (Description + Body-Delegation)

- should_trigger: 8/9
- should_not_trigger: 4/4
- other_skill: 3/3 (+1 ggü. Blind/Baseline — `mach mir einen prompt für GPT zu einem anderen Thema` wird durch die Delegations-Tabelle "Handover → chat-wechsel, Code → code-erstellen" klarer als non-Review erkannt und landet in der "keiner triggert automatisch"-Zone)
- ambiguous: _dokumentiert_
- delta vs baseline: +1 bei other_skill (2/3 → 3/3), ambiguity-Quote gleich

#### notes

- Query 6 `Runde 3 erstellen` bleibt im Blind-Modus problematisch — ohne Chat-Kontext kein erkennbarer ChatGPT-Bezug. Im Vollmodus marginal besser, aber immer noch kontext-abhängig.
  → als ⚠️ **[ARCH-OPEN]** dokumentieren: "Runde N" als Keyword in Description prüfen.
- Phase 5.6 hat die Symmetrie zu chat-wechsel explizit gemacht. Das entschärft den Paar-Konflikt bei "mach mir den Prompt" (mehrdeutig zwischen chat-wechsel / chatgpt-review).
- Die neue Body-Regel "bei generischem Prompt-Request ohne Kontext: per ask_user_input_v0 klären" wird im Vollmodus-Score indirekt positiv bewertet (schafft keinen Fehltrigger mehr).
- Methodische Einschränkung wie bei git-commit-helper (siehe dort).
- verbleibende ❌: keine
- verbleibende ⚠️: Query 6 (kontext-abhängiger Trigger, Description-Schärfung denkbar)
