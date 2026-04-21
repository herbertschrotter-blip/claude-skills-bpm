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

- date: _(wird in 1a.3 gefüllt)_
- should_trigger: X/9
- should_not_trigger: X/4
- other_skill: X/3
- ambiguous: _dokumentiert_
- notes: ...

### after-refactor

- date: _(wird in Phase 5.8 gefüllt)_
- ...
