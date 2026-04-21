# Eval: &lt;skill-name&gt;

## Skill-Description (aktuell)

```yaml
# hier die aktuelle Description aus SKILL.md Frontmatter einfügen
```

Stand: `<commit-hash>` — `<datum>`

---

## Query-Katalog

### should_trigger

Dieser Skill MUSS triggern.

| # | Query | Typ | Notiz |
|---|-------|-----|-------|
| 1 | ... | [golden] / [synthetic] | Quelle / Variante / Grund |

### should_not_trigger

KEIN Skill darf triggern (reines Gespräch, Zustimmung, Smalltalk).

| # | Query | Typ | Notiz |
|---|-------|-----|-------|
| 1 | ... | [golden] / [synthetic] | Warum kein Trigger |

### other_skill

Ein anderer Skill soll triggern — dieser Skill darf NICHT triggern.

| # | Query | Typ | Erwarteter Skill | Notiz |
|---|-------|-----|------------------|-------|
| 1 | ... | [golden] / [synthetic] | `<skill-name>` | Abgrenzungsgrund |

### ambiguous

Grenzfall — beide Interpretationen vertretbar. Wird dokumentiert, nicht gewertet.

| # | Query | Typ | Interpretation A | Interpretation B | Notiz |
|---|-------|-----|------------------|------------------|-------|
| 1 | ... | [golden] / [synthetic] | triggert | triggert nicht | ... |

---

## Run-Log

### baseline

- date: _(wird in 1a.3 gefüllt)_
- should_trigger: X/Y
- should_not_trigger: X/Y
- other_skill: X/Y
- ambiguous: _dokumentiert_
- notes: ...

### after-refactor

- date: _(wird in Phase 5.8 gefüllt)_
- ...
