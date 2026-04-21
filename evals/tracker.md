# Eval: tracker

## Skill-Description (aktuell)

```yaml
description: >
  Verwaltet BPM-Tasks in ClickUp über explizite Tracker-Kommandos wie
  "tracker neu", "tracker done", "tracker update", "tracker suche",
  "tracker status", "tracker next", "tracker split", "tracker relate",
  und "tracker field". Use when users want a concrete ClickUp action for a
  BPM task. Do not trigger for allgemeine Gespräche über offene Punkte,
  Backlog-Diskussionen, Priorisierung ohne ClickUp-Aktion, or free-form notes.
```

Stand: `74cda17` — 2026-04-21 (Phase 1.3)

---

## Query-Katalog

### should_trigger

| # | Query | Typ | Notiz |
|---|-------|-----|-------|
| 1 | `tracker neu: PM — neue Regex-Erkennung` | [golden] | Standard-Workflow, Teil 18+ |
| 2 | `tracker done BPM-007` | [golden] | Standard-Workflow, Teil 19 |
| 3 | `tracker status` | [golden] | Standard-Workflow |
| 4 | `tracker split BPM-016` | [golden] | Teil 18 — Unteraufgaben |
| 5 | `tracker suche Regex` | [synthetic] | search-Kommando |
| 6 | `tracker next` | [synthetic] | next-Kommando |
| 7 | `tracker update BPM-042 Priorität auf high` | [synthetic] | update-Kommando |
| 8 | `tracker relate BPM-007 blocks BPM-019` | [synthetic] | relate-Kommando |
| 9 | `tracker field BPM-007 Zielversion v0.26.0` | [synthetic] | field-Kommando |

### should_not_trigger

| # | Query | Typ | Notiz |
|---|-------|-----|-------|
| 1 | `was ist offen?` | [golden] | Teil 22 — war unerwünschter Trigger, Phase 1.3 Fix |
| 2 | `was muss ich noch machen?` | [golden] | Phase 1.3 Fix — allgemeine Gesprächsphrase |
| 3 | `merk dir das` | [golden] | geht in Memory, nicht ClickUp |
| 4 | `remember this` | [golden] | geht in Memory, nicht ClickUp |
| 5 | `notiz: fehlendes Logging in X` | [synthetic] | Notiz ohne ClickUp-Absicht (Skill fragt nach) |
| 6 | `offene punkte heute?` | [synthetic] | generischer Backlog-Talk ohne explizites tracker-Kommando |
| 7 | `nicht vergessen: Feature Y` | [synthetic] | unklar ob Task oder nur Notiz (Skill-Regel: nachfragen) |

### other_skill

| # | Query | Typ | Erwarteter Skill | Notiz |
|---|-------|-----|------------------|-------|
| 1 | `neuer chat` | [golden] | `chat-wechsel` | Session-Ende ≠ Task-Aktion |
| 2 | `implementiere die Regex-Erkennung` | [synthetic] | `code-erstellen` | Code-Aktion, auch wenn indirekt Task-bezogen |
| 3 | `commit bitte` | [synthetic] | `git-commit-helper` | Commit ≠ Task |

### ambiguous

| # | Query | Typ | Interpretation A | Interpretation B | Notiz |
|---|-------|-----|------------------|------------------|-------|
| 1 | `neue aufgabe: Regex für 5998er fixen` | [synthetic] | triggert (implizites tracker neu) | triggert nicht (Description fordert expliziten Kommando-Prefix) | „neue aufgabe" war früher Trigger, nach Phase 1.3 fraglich |
| 2 | `das ist erledigt` nach Commit | [synthetic] | triggert (impliziter done-Intent für offenen Task) | triggert nicht (kein BPM-Nummer/keine explizite Nennung) | Kontext-Abhängigkeit |

---

## Run-Log

### baseline

- date: _(wird in 1a.3 gefüllt)_
- should_trigger: X/9
- should_not_trigger: X/7
- other_skill: X/3
- ambiguous: _dokumentiert_
- notes: ...

### after-refactor

- date: _(wird in Phase 5.8 gefüllt)_
- ...
