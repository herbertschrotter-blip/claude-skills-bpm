---
name: skill-neu
description: >
  Erstellt komplett neue BPM-Skills von Grund auf — inkl. Capture-Intent-Interview,
  Description nach BPM-Schema, Body, references/-Aufteilung und strukturiertem
  Test-Prompt-Setup. Use when users want to create a new skill from scratch, design
  a new skill system, draft a SKILL.md for a new use case, or set up test prompts
  for evaluating skill triggering. Do not trigger for changing or extending existing
  skills (use skill-pflege instead), running automated eval scripts, or general
  documentation pflege.
---

# Skill-Neu — Neue BPM-Skills von Grund auf erstellen

## Zweck

Erstellt einen **komplett neuen** Skill im BPM-Stil. Führt durch Capture-Intent-Interview, Description-Schema, Body-Aufbau, optionale references/-Aufteilung und Test-Prompt-Setup für Live-Triggering-Tests im claude.ai-Modus.

**Abgrenzung:**
- `skill-neu` = NEU erstellen (dieser Skill)
- `skill-pflege` = bestehenden Skill ÄNDERN

**Bestehenden Skill ändern? → skill-pflege.** Nicht hier weiterarbeiten — Logik und Schutzmechanismen sind dort drin.

---

## 🚨 VERBINDLICHE REGEL: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0` verwendet werden — KEINE Prosa-Fragen.**

### Diese Fragen IMMER mit ask_user_input_v0:

| Situation | Optionen |
|-----------|----------|
| Trigger-Fragen während Capture Intent | konkrete Phrasen-Vorschläge als Optionen |
| references/ ja/nein | "Inline lassen", "references/ aufteilen", "User entscheidet" |
| Domain-Organization-Pattern? | "Eine SKILL.md", "Pro Variante eine references/-Datei" |
| Test-Prompts jetzt definieren? | "Ja, jetzt", "Später", "Skill ohne Tests veröffentlichen" |
| Skill-Name-Vorschläge | 2-4 konkrete Namen als Optionen |
| Description-Stil | "Knapp + sachlich", "Pushy gegen Undertriggering", "Hybrid" |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen (z.B. "Beschreibe den Use-Case in einem Satz")
- User hat Präferenz bereits signalisiert
- Reine Erklärung/Kontext

---

## ABLAUF (Standard-Workflow)

### Schritt 1 — Capture Intent (4 Pflicht-Fragen)

Bevor irgendwas geschrieben wird, vier Dinge klären:

1. **Was soll der Skill enable?** Welche Aktionen, welcher Output?
2. **Wann triggern?** User-Phrasen, Kontexte, Schlüsselwörter
3. **Wann NICHT triggern?** Catch-all-Risiken explizit benennen (häufig vergessen, oft der wichtigste Punkt)
4. **Test-Cases nötig?** Objektiv prüfbare Outputs (z.B. fixe Workflow-Schritte, JSON-Generierung) → ja. Subjektive Outputs (Schreibstil, Kreatives) → meist nein.

Wenn der User unklar ist: pro Frage `ask_user_input_v0` mit konkreten Optionen.

**Aus aktueller Konversation extrahieren:** Falls der User vorher schon einen Workflow beschrieben hat ("mach daraus einen Skill"), die Antworten möglichst aus dem Chat-Verlauf ableiten und nur Lücken nachfragen.

---

### Schritt 2 — Interview & Research

- **Edge Cases:** Was passiert bei untypischen Inputs?
- **Existieren ähnliche Skills?** Liste durchgehen: `view /mnt/skills/user/`
- **Trigger-Konflikt-Check:** Würde der neue Skill anderen Skills die Triggers wegschnappen? Wenn ja: Description-Abgrenzung schärfen.
- **Output-Format:** Datei? Chat-Antwort? Tool-Call?
- **Namens-Kollisions-Check:** Anthropic hat Beispiel-Skills unter Namen wie `skill-creator`, `pdf`, `docx` etc. registriert. Vor Anlage prüfen ob der gewünschte Name bereits existiert (`/mnt/skills/examples/`, `/mnt/skills/public/`). Bei Kollision deutschsprachige oder BPM-präfix-Variante wählen.

Komm mit Kontext vorbereitet — reduziert die Fragelast für den User.

---

### Schritt 3 — Description nach BPM-Schema schreiben

**Pflicht-Format:** `Was + Use when + Do not trigger for`

```yaml
description: >
  <Was-Satz: was der Skill macht>. Use when users want to <konkrete
  Trigger-Phrasen>. Do not trigger for <konkrete Catch-all-Risiken>.
```

**Pushy formulieren — gegen Undertriggering.**

Anthropic-Empfehlung (Z. 67 im Original): Description darf "drängend" sein, denn Claude hat eher die Tendenz Skills NICHT zu nutzen wenn sie nützlich wären.

| Schwach | Stark |
|---------|-------|
| "How to build a dashboard" | "How to build a dashboard. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of data, even if they don't explicitly ask for a 'dashboard'." |

**Beispiel aus BPM (tracker):**
- Was: "Führt konkrete ClickUp-Aktionen für BPM-Tasks aus, z.B. tracker neu, tracker done, tracker update..."
- Use when: "Use when users want an explicit BPM task action in ClickUp."
- Do not trigger for: "Do not trigger for general talk about priorities, open points, brainstorming, notes, or free-form project planning without a concrete tracker command."

Wenn die "Do not trigger for"-Liste leer wäre → ist das ein Warnsignal. Catch-all-Risiken sind fast immer da, sie müssen nur erkannt werden.

---

### Schritt 4 — SKILL.md Body schreiben

**Form:**
- **Imperative Form** verwenden ("Lade Original via view", nicht "Man könnte das Original laden")
- **<500 Zeilen Ideal.** Anthropic-Richtwert. Bei Annäherung: references/-Aufteilung erwägen.
- **Theory of Mind:** Erklären WARUM eine Regel existiert, nicht nur "MUSS"
- **Beispiele inline einbauen** statt nur abstrakte Regeln
- **Principle of Lack of Surprise:** Skill-Body muss zur Description passen. Wenn die Description "macht X" sagt, darf der Body nicht heimlich auch Y und Z machen.

**Empfohlene Struktur:**
```markdown
---
[Frontmatter: name, description]
---

# <Skill-Name> — <Kurzbeschreibung>

## Zweck
[1-3 Sätze: was, wofür, Abgrenzung zu Nachbarn]

## 🚨 ask_user_input_v0 Pflicht
[falls Entscheidungen anfallen]

## ABLAUF
### Schritt 1 — ...
### Schritt 2 — ...

## VERBOTEN
- ...

## VERWEIS
[bidirektionale Verweise zu Nachbarskills]
```

---

### Schritt 5 — references/ wenn Body über ~300 Zeilen wächst

**Domain Organization Pattern** (aus Anthropic-Original Z. 100-109):

Wenn Skill mehrere Domänen/Varianten unterstützt, pro Variante eine references/-Datei:

```
cloud-deploy/
├── SKILL.md (workflow + selection logic)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

Claude lädt nur die relevante reference-Datei nach. SKILL.md bleibt schlank, der Detail-Kontext kommt on-demand.

**BPM-Beispiel:** `tracker` ist nach Phase 3.3 so aufgebaut — SKILL.md (147 Zeilen) + 9 references/-Dateien (clickup-fields, anker-system, create-task, complete-task, ...).

**Hinweis zur references/-Aufteilung:**
- Cross-Skill-References werden NICHT automatisch geladen. Wenn ein anderer Skill die Logik braucht, lokale Kopie pflegen oder via `github:get_file_contents` nachladen.
- Bei references/ >300 Zeilen: Inhaltsverzeichnis am Anfang einbauen.

---

### Schritt 6 — Two-Place anlegen (Pflicht)

**JEDE neue Skill-Datei lebt an zwei Orten:**

1. **Repo** (versioniert): `claude-skills-bpm/skills/<n>/SKILL.md`
   - Anlegen via Desktop Commander: `write_file`
   - Pfad-Pattern: `<OneDrive>\Dokumente\02 Arbeit\05 Vorlagen - Scripte\00_claude-skills-bpm\skills\<n>\SKILL.md`

2. **Artifact im Chat** (claude.ai-aktiv):
   - `create_file(path: "/home/claude/SKILL.md", content: <komplette SKILL.md>)`
   - Dateiname IMMER exakt `SKILL.md` (nicht `SKILL-<n>.md`, nicht `<n>-SKILL.md`)
   - Der User sieht das Artifact und klickt "Skill speichern" in Claude.ai

**Reihenfolge:** Erst Repo, dann Artifact. Repo ist die Wahrheit.

**KEIN** `present_files` mehr, **KEINE** Download-Datei in `/mnt/user-data/outputs/`. Der Artifact ersetzt beide Mechanismen.

---

### Schritt 7 — Test-Prompts strukturiert sammeln (Eval-Denkweise)

**Auch ohne Auto-Runner: jeder neue Skill braucht ein Test-Set.**

Pro Skill anlegen: `claude-skills-bpm/skills/<n>/test-prompts.md`

**Inhalt:**
- 3-5 "should trigger" Prompts (echte User-Sätze)
- 3-5 "should NOT trigger" Prompts (Catch-all-Risiken aus Description)
- Optional: Edge-Cases (Grenzfälle, mehrdeutige Formulierungen)

**Vorlage** (wird in test-prompts.md angelegt):

```markdown
# Test-Prompts für <skill-name>

## Should trigger (Trigger-Cases)
1. ...
2. ...

## Should NOT trigger (Catch-all-Tests)
1. ...
2. ...

## Edge Cases (optional)
1. ...

## Test-Log
| Datum | Prompt-ID | Erwartung | Ergebnis | Bemerkung |
|-------|-----------|-----------|----------|-----------|
```

---

### Schritt 8 — Live-Test im neuen Chat (claude.ai-Modus)

Statt automatisierter Eval-Runner (die in claude.ai nicht verfügbar sind):

1. User öffnet **neuen Claude-Chat** (sonst hat aktueller Chat den Skill schon im Speicher)
2. Sendet jeden Test-Prompt einzeln
3. Notiert: hat triggert? (ja/nein)
4. **3× pro Prompt** für Variance-Check (Triggering ist nicht deterministisch)
5. Ergebnisse zurück in `test-prompts.md` Test-Log eintragen

**Kritisch verstehen — Triggering-Mechanik (Anthropic-Original Z. 396-400):**

> Skills appear in Claude's `available_skills` list with their name + description, and Claude decides whether to consult a skill based on that description. The important thing to know is that Claude only consults skills for tasks it can't easily handle on its own — simple, one-step queries like "read this PDF" may not trigger a skill even if the description matches perfectly, because Claude can handle them directly with basic tools. Complex, multi-step, or specialized queries reliably trigger skills when the description matches.

Konsequenzen:
- **Triviale Prompts triggern nicht zuverlässig** — das ist normal, kein Description-Bug
- Test-Prompts sollten substantiell sein (mehrstufig, spezialisiert)
- Wenn ein Prompt 0/3 triggert: prüfen ob Prompt zu trivial ODER Description zu schwach

---

### Schritt 9 — Description nachschärfen (manuelle Optimization)

**Wenn Trigger-Rate <80%** (z.B. 1/3 oder 2/3 von "should trigger"-Prompts):
- Description "pushy"-er formulieren
- Konkrete Trigger-Phrasen explizit einbauen
- Synonym-Liste erweitern

**Wenn Catch-all-Trigger** (irrtümliches Triggern bei "should NOT trigger"-Prompts):
- "Do not trigger for"-Liste konkret erweitern um die problematische Phrase
- Trigger-Phrasen im "Use when" enger formulieren

**Iteration:** Änderung → Two-Place pflegen → neuer Chat → erneut testen → Test-Log fortschreiben.

---

### Schritt 10 — Commit (Skill-Repo-Format)

```text
[vX.Y.Z] <skill-name>, Feature: <kurztitel>
```

- **MINOR-Bump** für neuen Skill (z.B. v0.6.0 → v0.7.0)
- **PATCH-Bump** für Description-Nachschärfung (z.B. v0.7.0 → v0.7.1)

**User committet selbst.** Claude liefert nur den fertigen Befehl als Vorschlag.

---

## ANATOMIE EINES SKILLS

```
skill-name/
├── SKILL.md (PFLICHT)
│   ├── YAML Frontmatter (name, description PFLICHT)
│   └── Markdown Body
├── test-prompts.md (PFLICHT bei BPM-Skills)
└── Bundled Resources (optional)
    ├── scripts/    – ausführbarer Code (in claude.ai oft nicht verfügbar)
    ├── references/ – on-demand geladene Doku
    └── assets/     – Templates, Icons
```

**In claude.ai relevant:** SKILL.md + references/ + assets/. `scripts/` selten nutzbar (kein Subagent, kein Shell-Tool im Chat).

---

## PROGRESSIVE DISCLOSURE (3 Loading-Levels)

Skills nutzen ein 3-Level-Lade-System:

1. **Metadata** (name + description) — IMMER im Kontext (~100 Wörter pro Skill)
2. **SKILL.md Body** — bei Trigger geladen (<500 Zeilen Ideal)
3. **Bundled Resources** — on-demand (unbegrenzt)

**Konsequenzen für Design:**
- Description trägt das ganze Triggering — investiere die meiste Zeit hier
- SKILL.md Body ist "Workflow-Anleitung" — was Claude tun soll, wenn Skill aktiv ist
- references/ für Detail-Wissen, Tabellen, lange Listen, alternative Pfade

---

## DESCRIPTION-SCHEMA (BPM-Konvention)

**Pflicht-Komponenten:**
1. **Was-Satz** (1-2 Sätze): Was macht der Skill?
2. **Use when** (1-2 Sätze): Konkrete Trigger-Phrasen/Situationen
3. **Do not trigger for** (1-2 Sätze): Konkrete Catch-all-Risiken

**Beispiele aus existierenden BPM-Skills:**

`code-erstellen`:
> Plant und erzeugt BPM-Codeänderungen auf Basis von INDEX.md, Quickloads, Pflichtlesen und fachlichen Invarianten. Use when users want to implement or change application code, create or modify services, dialogs, data flows, validation, persistence logic, or code across BPM modules. Do not trigger for UI mockups, git commit commands, explicit documentation authoring, ClickUp task actions, or read-only audits.

`mockup-erstellen`:
> Erstellt BPM-UI-Mockups als HTML-Entwürfe für neue Screens, Dialoge und Layoutvarianten. Use when users want a mockup, a screen design, a UI proposal, a layout draft, or need to clarify how a screen should look before coding. Do not trigger for direct XAML implementation, small UI fixes in existing code, or non-UI design topics like architecture or database design.

`chat-wechsel`:
> Erstellt einen Handover-Prompt für die nächste Claude-Session inklusive aktuellem Stand, offenen Punkten und relevanten Next Steps. Use when users want to continue in a new chat, ask for a session handover, a continuation prompt, or a next-chat summary. Do not trigger for ChatGPT review prompts, generic prompt requests, or casual goodbyes like "tschüss" or "gute Nacht".

**Muster erkennbar:** Jeder Skill listet mindestens 3-4 konkrete "Do not trigger"-Fälle. Das ist die wichtigste Anti-Catch-all-Maßnahme.

---

## WRITING STYLE (Anthropic-Empfehlung)

- **Imperative Form** — direkte Anweisungen statt Beschreibungen
- **Theory of Mind** — erklären WARUM, nicht nur "MUSS"
- **Vermeide heavy-handed musty MUSTs** — Begründung schlägt Befehl
- **Allgemein halten**, nicht super-narrow auf spezifische Beispiele
- **Erst Draft, dann mit frischen Augen überarbeiten**

**Beispielpattern für Output-Formate:**

```markdown
## Report-Struktur
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Beispielpattern für Trigger-Beispiele:**

```markdown
## Commit-Message-Format

**Beispiel 1:**
Input: User-Auth mit JWT hinzugefügt
Output: feat(auth): JWT-basierte Authentifizierung

**Beispiel 2:**
Input: Null-Check im Invoice-Service
Output: fix(billing): Null-Invoice-Number verhindern
```

---

## TRIGGERING-MECHANIK (kritisch verstehen)

Aus Anthropic-Original Z. 396-400:

- Claude hat eine Liste `available_skills` mit jedem Skill (Name + Description, sonst nichts)
- Claude entscheidet **basierend auf Description**, ob er einen Skill konsultiert
- **Claude triggert nur bei nicht-trivialen Tasks.** Einfache Einschritt-Queries ("read this PDF") triggern oft NICHT, auch wenn Description perfekt passt — Claude kann die Aufgabe direkt lösen
- **Komplexe, mehrstufige, spezialisierte Queries triggern zuverlässig**, wenn Description matched

**Designkonsequenzen:**
- Skills sind für mehrstufige/spezialisierte Workflows gemacht
- Triviale Helfer-Skills (z.B. "format date") triggern unzuverlässig — das ist Architektur, nicht Bug
- Test-Prompts müssen substantiell sein
- Wenn der Skill für triviale Aufgaben gedacht ist, prüfen ob er überhaupt nötig ist

---

## VERBOTEN

- Skill aus dem Gedächtnis schreiben (immer mit Capture Intent zuerst — auch wenn man "weiß was rein muss")
- Description ohne expliziten "Do not trigger for"-Teil
- Eval-Scripts oder Subagent-Spawn erfinden (nicht in claude.ai verfügbar — `aggregate_benchmark.py`, `run_loop.py`, `package_skill.py` nicht referenzieren)
- skill-pflege-Aufgaben übernehmen → Verweis auf skill-pflege
- Skill-Body baut auf Tools/Pfade die in der Description nicht angedeutet sind (Principle of Lack of Surprise)
- Two-Place vergessen (immer Repo + lokal)
- Test-Prompts weglassen (auch wenn klein — `test-prompts.md` mindestens als Platzhalter mit 2-3 Cases)
- Skill ohne Konflikt-Check zu existierenden Skills veröffentlichen (Trigger-Überlappung prüfen)
- Skill-Namen vergeben ohne Kollisions-Check gegen `/mnt/skills/examples/` und `/mnt/skills/public/` (Anthropic-Beispiele blockieren z.B. `skill-creator`)
- **Prosa-Fragen bei festen Entscheidungsoptionen** — IMMER `ask_user_input_v0`

---

## VERWEIS

**Bestehenden Skill ändern? → `skill-pflege`**

`skill-pflege` ist der Schwester-Skill für Änderungen. Er hat eigene Schutzmechanismen (Original zeilengenau übernehmen, additive Default-Philosophie, Diff-Report). `skill-neu` macht ausschließlich Neu-Erstellung.

Faustregel:
- Existiert die SKILL.md schon? → `skill-pflege`
- Datei wird ganz neu angelegt? → `skill-neu` (hier)
