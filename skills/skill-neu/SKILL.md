---
name: skill-neu
description: >
  Erstellt komplett neue Skills für das Skills-Repo von Grund auf — projektneutral
  und für Cowork wie Claude Code — inkl. Capture-Intent-Interview, Description-Schema,
  Neutralitäts-Checkliste, Body, Profil-/references/-Aufteilung und strukturiertem
  Test-Prompt-Setup. Use when users want to create a new skill from scratch, design
  a new skill system, draft a SKILL.md for a new use case, or set up test prompts
  for evaluating skill triggering. Do not trigger for changing or extending existing
  skills (use skill-pflege instead), running automated eval scripts, or general
  documentation pflege.
---

# Skill-Neu — Neue Skills von Grund auf erstellen

## Zweck

Erstellt einen **komplett neuen** Skill im Stil des Skills-Repos. Führt durch Capture-Intent-Interview, Description-Schema, Neutralitäts-Checkliste, Body-Aufbau, Profil-/references/-Aufteilung und Test-Prompt-Setup für Live-Triggering-Tests.

**Neue Skills sind von Anfang an neutral** (seit 16.09.2026, nach dem Umbau von tracker, code-erstellen,
doc-pflege, audit, mockup-erstellen, skill-pflege): Sie beschreiben Handlungen, nicht Werkzeuge; sie
kennen kein Projekt und keine Sprache – Projektwerte stehen in einer Profil-Sektion der CLAUDE.md des
Repos oder in `projects/<name>/`, Sprachliches in `references/<gruppe>/<key>.md`. Sie laufen im
Cowork-Chat und in Claude Code.

**Abgrenzung:**
- `skill-neu` = NEU erstellen (dieser Skill)
- `skill-pflege` = bestehenden Skill ÄNDERN

**Bestehenden Skill ändern? → skill-pflege.** Nicht hier weiterarbeiten — Logik und Schutzmechanismen sind dort drin.

---

## 🚨 VERBINDLICHE REGEL: Auswahlfrage bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS eine Auswahlfrage gestellt werden — KEINE Prosa-Fragen.** Auswahlfrage = Frage-Werkzeug der Umgebung mit anklickbaren Optionen (Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion`).

### Diese Fragen IMMER als Auswahlfrage:

| Situation | Optionen |
|-----------|----------|
| Trigger-Fragen während Capture Intent | konkrete Phrasen-Vorschläge als Optionen |
| references/ ja/nein | "Inline lassen", "references/ aufteilen", "User entscheidet" |
| Domain-Organization-Pattern? | "Eine SKILL.md", "Pro Variante eine references/-Datei" |
| Projektspezifisches gefunden (Frage 5) | "Profil-Sektion in CLAUDE.md", "projects/<name>/", "Beides", "Nichts projektspezifisch" |
| Sprachspezifisches gefunden (Frage 5) | "references/<gruppe>/<key>.md", "Inline mit Kennzeichnung", "Nichts sprachspezifisch" |
| Neutralitäts-Checkliste hat offene Punkte | "Jetzt beheben", "Bewusst so lassen (Begründung in den Skill)", "Abbrechen" |
| Test-Prompts jetzt definieren? | "Ja, jetzt", "Später", "Skill ohne Tests veröffentlichen" |
| Skill-Name-Vorschläge | 2-4 konkrete Namen als Optionen |
| Description-Stil | "Knapp + sachlich", "Pushy gegen Undertriggering", "Hybrid" |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen (z.B. "Beschreibe den Use-Case in einem Satz")
- User hat Präferenz bereits signalisiert
- Reine Erklärung/Kontext

---

## ABLAUF (Standard-Workflow)

### Schritt 1 — Capture Intent (5 Pflicht-Fragen)

Bevor irgendwas geschrieben wird, fünf Dinge klären:

1. **Was soll der Skill enable?** Welche Aktionen, welcher Output?
2. **Wann triggern?** User-Phrasen, Kontexte, Schlüsselwörter
3. **Wann NICHT triggern?** Catch-all-Risiken explizit benennen (häufig vergessen, oft der wichtigste Punkt)
4. **Test-Cases nötig?** Objektiv prüfbare Outputs (z.B. fixe Workflow-Schritte, JSON-Generierung) → ja. Subjektive Outputs (Schreibstil, Kreatives) → meist nein.
5. **Was ist projekt-, was sprachspezifisch?** Alles, was nur für ein Repo gilt (Pfade, IDs, Listen,
   Doc-Namen, Deploy-Befehle, Präfixe) → **Profil-Sektion** in der CLAUDE.md des Repos (Muster: Commit-,
   Tracker-, Code-, Doku-, Mockup-Profil) oder `projects/<name>/` im Skills-Repo (wenn der Skill die Werte
   auch ohne das Repo braucht, wie tracker). Alles, was nur für eine Sprache/einen Stack gilt →
   `references/<gruppe>/<key>.md` (Muster: `code-erstellen/references/stacks/`). Der Skill selbst
   bekommt nur die Regel „lies Feld X aus dem Profil“ und Beispiele, die als solche gekennzeichnet sind.

Wenn der User unklar ist: pro Frage Auswahlfrage mit konkreten Optionen.

**Aus aktueller Konversation extrahieren:** Falls der User vorher schon einen Workflow beschrieben hat ("mach daraus einen Skill"), die Antworten möglichst aus dem Chat-Verlauf ableiten und nur Lücken nachfragen.

---

### Schritt 2 — Interview & Research

- **Edge Cases:** Was passiert bei untypischen Inputs?
- **Existieren ähnliche Skills?** Liste durchgehen: Ordner `skills/` im Skills-Repo (Cowork alternativ `view /mnt/skills/user/`)
- **Trigger-Konflikt-Check:** Würde der neue Skill anderen Skills die Triggers wegschnappen? Wenn ja: Description-Abgrenzung schärfen.
- **Output-Format:** Datei? Chat-Antwort? Tool-Call?
- **Namens-Kollisions-Check:** Anthropic hat Beispiel-Skills unter Namen wie `skill-creator`, `pdf`, `docx` etc. registriert. Vor Anlage prüfen ob der gewünschte Name bereits existiert (Cowork: `/mnt/skills/examples/`, `/mnt/skills/public/`; Claude Code: Liste der verfügbaren Skills der Sitzung). Bei Kollision deutschsprachige Variante wählen (z.B. `skill-neu` statt `skill-creator`).
- **Umgebungen:** Läuft der Skill im Cowork-Chat, in Claude Code oder beidem? Standard: beide. Jede Stelle, die liest, schreibt, fragt oder liefert, braucht dann die Umgebungsweiche (Neutralitäts-Checkliste, Schritt 3a).

Komm mit Kontext vorbereitet — reduziert die Fragelast für den User.

---

### Schritt 2a — Auto-Issue-Erkennung (skill-pflege-002)

Während der Skill-Erstellung proaktiv erkennen wenn:

- Neuer Skill hätte Trigger-Überlappung mit bestehendem Skill (Konflikt-Risiko)
- Bestehender Skill enthält veraltete Pfade/IDs die gerade auffallen (tote Referenzen)
- User-Wünsche im aktuellen Chat widersprechen Regeln bestehender Skills

Bei Erkennung:

1. User informieren (kurze Prosa): "Beim Anlegen aufgefallen: X widerspricht Y in Skill Z"
2. Auswahlfrage:
   ```
   Frage: "Issue für Skill Z anlegen?"
   Optionen: "Ja, <skill>-NNN", "Später selbst", "Kein Issue nötig"
   ```
3. Bei Zustimmung: `tracker issue <skill>: <kurztitel>` (Issue-ID via tracker-003 automatisch)

**NICHT** auslösen bei: Tippfehlern, stilistischen Unterschieden, User-initiierten aktiven Änderungen im aktuellen Chat, fehlenden Features die nie angefragt wurden.

Vollständige Spec: `skill-pflege/SKILL.md` Abschnitt "AUTO-ISSUE-ERKENNUNG".

---

### Schritt 3 — Description nach dem Repo-Schema schreiben

**Pflicht-Format:** `Was + Use when + Do not trigger for` — **maximal 1024 Zeichen** (Zeilen des
`description: >`-Blocks getrimmt und mit Leerzeichen verbunden). claude.ai lehnt den Upload sonst ab.
Länge vor jeder Lieferung messen.

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

**Beispiel aus dem Repo (tracker, v0.26):**
- Was: "Führt konkrete ClickUp-Aktionen für Projekt-Tasks und Skill-Issues aus, z.B. tracker neu, tracker done, tracker update..."
- Use when: "Use when users want to anlegen, erstellen, … a ClickUp task or issue — including Projekt-Tasks (BPM, Heidi, …)."
- Do not trigger for: "Do not trigger for general talk about priorities, open points, brainstorming, notes, or free-form project planning without a concrete tracker command."

Wenn die "Do not trigger for"-Liste leer wäre → ist das ein Warnsignal. Catch-all-Risiken sind fast immer da, sie müssen nur erkannt werden.

---

### Schritt 3a — Neutralitäts-Checkliste (Pflicht, vor dem Body)

Jeder neue Skill muss diese Punkte erfüllen, bevor er geliefert wird. Offene Punkte → Auswahlfrage
(„Jetzt beheben“ / „Bewusst so lassen, Begründung in den Skill“ / „Abbrechen“). Das ist genau die
Arbeit, die am 16.09.2026 an sechs bestehenden Skills nachgeholt werden musste – beim Neubau ist sie billig.

| # | Punkt | Richtig | Falsch |
|---|-------|---------|--------|
| 1 | **Handlung statt Werkzeug** | „Auswahlfrage“, „Shell der Umgebung“, „Datei lesen“, „Lieferung an den User“ | `ask_user_input_v0`, „per DC“, `view`, `create_file` als Vorschrift |
| 2 | **Umgebungsweiche** | Ein Satz im Zweck: Cowork = Werkzeug A, Claude Code = Werkzeug B; danach nur noch die Handlung | Skill funktioniert nur in einer Umgebung, ohne es zu sagen |
| 3 | **Keine Projektwerte** | Pfade, IDs, Listen, Präfixe, Doc-Namen, Deploy-Befehle aus Profil-Sektion (CLAUDE.md) oder `projects/<name>/` | `901522848097`, `Docs/Referenz/DOC-STANDARD.md`, `BPM-NNN` als Regel |
| 4 | **Keine Sprache im Skill** | Sprach-/Stack-Details in `references/<gruppe>/<key>.md`, Schlüssel im Profil | „ViewModel“, „App.xaml.cs“, „npm test“ als Regel |
| 5 | **Beispiele gekennzeichnet** | „Beispiel (BPM)“, „Heidi: …“ – erkennbar als Muster, nicht als Vorgabe | Projektbeispiel liest sich wie die Regel |
| 6 | **Profil-Fallback** | Fehlt das Profil → Auswahlfrage „Profil anlegen (Vorschlag aus dem Repo)“ / „Ohne Profil, Werte nennen“ | Skill rät oder nimmt BPM an |
| 7 | **Lieferung je Umgebung** | Cowork: Artifact-Paar; Claude Code: SendUserFile (Zip bei references) | nur `create_file`/`present_files` |
| 8 | **description ≤ 1024 Zeichen** | gemessen | nicht gemessen |
| 9 | **Split-Regel** (skill-pflege Regel 21) | SKILL.md = Zweck, Kernregeln, Routing, Kurz-VERBOTEN; Abläufe je Kommando/Ausprägung in `references/` | alles in einer 600-Zeilen-Datei |
| 10 | **Memory je Umgebung** | Cowork Memory-Einträge; Claude Code Memory-Ordner mit Dateien | `memory_user_edits` als einzige Form |

Vorbilder im Repo: `tracker` (Präfix, Felder, Listen aus `projects/<name>/`), `code-erstellen`
(Code-Profil + `references/stacks/`), `doc-pflege` (Doku-Profil), `mockup-erstellen` (Mockup-Profil).

### Schritt 4 — SKILL.md Body schreiben

**Form:**
- **Imperative Form** verwenden ("Lies das Original", nicht "Man könnte das Original laden")
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

## 🚨 Auswahlfrage bei Entscheidungen
[falls Entscheidungen anfallen; nennt Cowork ask_user_input_v0 und Claude Code AskUserQuestion einmal, danach nur „Auswahlfrage“]

## Voraussetzung: <Name>-Profil
[nur wenn Frage 5 Projektspezifisches ergab: Felder, BPM- und Heidi-Beispiel, Fallback]

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

**Beispiele im Repo:** `tracker` — SKILL.md (Routing + Kernregeln) + 14 references/-Dateien (clickup-fields, anker-system, create-task, complete-task, …); `code-erstellen` — `references/stacks/<key>.md` je Sprache, Schlüssel im Code-Profil des Projekts. Wann gesplittet wird: skill-pflege Regel 21 (Größe, nur ein Kommando/eine Umgebung/ein Stack, Projektwerte, Wiederholungen).

**Hinweis zur references/-Aufteilung:**
- Cross-Skill-References werden NICHT automatisch geladen. Wenn ein anderer Skill die Logik braucht, lokale Kopie pflegen oder aus dem Skills-Repo nachladen (Claude Code: Read auf den Repo-Pfad aus dem Tracker-Profil; Cowork: `github:get_file_contents`/DC).
- Ausprägungen (Sprache, Stack, Variante) als `references/<gruppe>/<key>.md`; der Schlüssel steht im Profil des Projekts, der Skill lädt nur die genannten.
- Bei references/ >300 Zeilen: Inhaltsverzeichnis am Anfang einbauen.

---

### Schritt 6 — Two-Place anlegen (Pflicht)

**JEDE neue Skill-Datei lebt an zwei Orten:**

1. **Repo** (versioniert): `claude-skills-bpm/skills/<n>/SKILL.md` (+ `references/`, `test-prompts.md`)
   - Cowork: via Desktop Commander `write_file`; Pfad-Pattern `<OneDrive>\Dokumente\02 Arbeit\05 Vorlagen - Scripte\00_claude-skills-bpm\skills\<n>\SKILL.md`
   - Claude Code: Write auf den Skills-Repo-Pfad (OneDrive-relativ im Tracker-Profil der CLAUDE.md)
   - Dazu im Repo: `CHANGELOG.md`-Eintrag `[vX.Y.Z]`, Zeile in `INDEX.md` (Skill-Tabelle + Zuständigkeiten), Commit + Push (Schritt 10)

2. **Lieferung an den User** (damit der Skill bei claude.ai aktiv wird):
   - **Cowork:** Artifact `create_file(path: "/home/claude/SKILL.md", …)` + `present_files` (Tool-Call-Paar, skill-pflege Regel 14); Dateiname IMMER exakt `SKILL.md`
   - **Claude Code:** `SendUserFile` mit der SKILL.md; hat der Skill `references/`, eine **Zip** mit SKILL.md + references/ (Herbert legt den Skill bei claude.ai aus der Zip an)
   - Der User speichert bei claude.ai und bestätigt „gespeichert“

**Reihenfolge:** Erst Repo (inkl. CHANGELOG/INDEX/Commit), dann Lieferung. Repo ist die Wahrheit.

**Lieferregeln aus skill-pflege gelten auch hier:** ein Skill pro Antwort (13b), keine Auswahlfrage im
selben Antwort-Block wie die Lieferung (14a), description ≤ 1024 Zeichen (Regel 6), Zip bei references (13).

**🔴 Artifact-Dateiname (KRITISCH, skill-pflege-004):**

Der Artifact-Dateiname MUSS **exakt** `SKILL.md` sein (Groß-Klein-Schreibung). Sonst erscheint der "Skill speichern"-Button in Claude.ai nicht.

RICHTIG: `create_file(path="/home/claude/SKILL.md", ...)`

FALSCH (kein Button):
- `create_file(path="/home/claude/chat-wechsel-SKILL.md", ...)`
- `create_file(path="/home/claude/SKILL-chat-wechsel.md", ...)`
- `create_file(path="/home/claude/chat-wechsel.md", ...)`
- `create_file(path="/home/claude/skill.md", ...)` ← klein, auch falsch

Mehrere Skills in einer Session: Pro Skill eigener Antwort-Block, pro Antwort-Block genau EINE Lieferung, Kontext-Trennung über Antwort-Text statt Dateinamen-Variation.

---

### Schritt 7 — Test-Prompts strukturiert sammeln (Eval-Denkweise)

**Auch ohne Auto-Runner: jeder neue Skill braucht ein Test-Set.**

Pro Skill anlegen: `claude-skills-bpm/skills/<n>/test-prompts.md`

**Inhalt:**
- 3-5 "should trigger" Prompts (echte User-Sätze)
- 3-5 "should NOT trigger" Prompts (Catch-all-Risiken aus Description)
- Optional: Edge-Cases (Grenzfälle, mehrdeutige Formulierungen)
- **Je Umgebung mindestens 1–2 Prompts** (Cowork-Chat und Claude Code), weil Triggering und Wortwahl
  dort verschieden sind („dc“/„auf platte“ gibt es in Claude Code nicht; dort heißt es „commit“, „bau“, „prüfe“)

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
| Datum | Umgebung (Cowork/Claude Code) | Prompt-ID | Erwartung | Ergebnis | Bemerkung |
|-------|-------------------------------|-----------|-----------|----------|-----------|
```

---

### Schritt 8 — Live-Test in neuer Sitzung (beide Umgebungen)

Statt automatisierter Eval-Runner (die in claude.ai nicht verfügbar sind):

1. User öffnet **neuen Claude-Chat** bzw. eine **neue Claude-Code-Sitzung** (sonst hat die aktuelle den Skill schon im Speicher); beide Umgebungen testen, wenn der Skill für beide gedacht ist
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

**Iteration:** Änderung → Two-Place pflegen (über skill-pflege, weil der Skill jetzt existiert) → neue Sitzung → erneut testen → Test-Log fortschreiben.

---

### Schritt 10 — Commit (Skill-Repo-Format)

```text
[vX.Y.Z] <skill-name>, Feature: <kurztitel>
```

- **MINOR-Bump** für neuen Skill (z.B. v0.6.0 → v0.7.0)
- **PATCH-Bump** für Description-Nachschärfung (z.B. v0.7.0 → v0.7.1)
- Im selben Commit: `CHANGELOG.md`-Eintrag mit denselben Worten, `INDEX.md`-Zeile, `test-prompts.md`

**Cowork:** User committet selbst, Claude liefert den fertigen Befehl (git-commit-helper).
**Claude Code:** Claude committet und pusht selbst (Branch `main` des Skills-Repos) und nennt den Hash.

---

## ANATOMIE EINES SKILLS

```
skill-name/
├── SKILL.md (PFLICHT)
│   ├── YAML Frontmatter (name, description PFLICHT)
│   └── Markdown Body
├── test-prompts.md (PFLICHT für alle Skills des Repos)
└── Bundled Resources (optional)
    ├── scripts/    – ausführbarer Code (in claude.ai oft nicht verfügbar)
    ├── references/ – on-demand geladene Doku
    └── assets/     – Templates, Icons
```

**In claude.ai relevant:** SKILL.md + references/ + assets/. `scripts/` selten nutzbar (kein Subagent, kein Shell-Tool im Chat). In Claude Code sind Shell und Skripte verfügbar – der Skill darf sie nutzen, muss aber ohne sie funktionieren (Umgebungsweiche).

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

## DESCRIPTION-SCHEMA (Repo-Konvention)

**Pflicht-Komponenten:**
1. **Was-Satz** (1-2 Sätze): Was macht der Skill?
2. **Use when** (1-2 Sätze): Konkrete Trigger-Phrasen/Situationen
3. **Do not trigger for** (1-2 Sätze): Konkrete Catch-all-Risiken

**Beispiele aus existierenden Skills (Stand v0.28/v0.32 – neutral, Projekte nur als Beispiel genannt):**

`code-erstellen`:
> Plant und erzeugt Codeänderungen im aktiven Projekt nach dessen Code-Profil (Pflicht-Docs, Aufgabenquelle, Stack-Referenzen, Tests, Auslieferung) – projektneutral für BPM (C#/WPF), Heidi (TypeScript/Lit, HA-YAML, Python) oder jedes Repo mit Profil. Use when users want to schreiben, erstellen, bauen, implementieren, fixen, … application code … Do not trigger for UI mockups (HTML-Entwürfe), git commit commands, explicit documentation authoring, ClickUp task actions, or read-only audits.

`mockup-erstellen`:
> Erstellt UI-Mockups als HTML-Entwürfe für neue Screens, Dialoge und Layoutvarianten – nach dem Mockup-Profil des Projekts (BPM: Docs/Mockups mit Sitemap; Heidi: dreame_x60/mockups im Bento-Design mit --dx-Tokens). Use when users want to mocken, entwerfen, skizzieren, … Do not trigger for direct XAML or Lit component implementation, small UI fixes in existing code, or non-UI design topics like database design.

`chat-wechsel`:
> Erstellt einen Handover-Prompt für die nächste Claude-Session inklusive aktuellem Stand, offenen Punkten und relevanten Next Steps. Use when users want to continue in a new chat, ask for a session handover, a continuation prompt, or a next-chat summary. Do not trigger for ChatGPT review prompts, generic prompt requests, or casual goodbyes like "tschüss" or "gute Nacht".

**Muster erkennbar:** Jeder Skill listet mindestens 3-4 konkrete "Do not trigger"-Fälle. Das ist die wichtigste Anti-Catch-all-Maßnahme. Und: Projekte kommen in der Description nur als **Beispiele in Klammern** vor, nie als Zuständigkeit („BPM-Skills“, „BPM-Code“).

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

## MEMORY-DISZIPLIN

Memory ist für offene Merker, Verifikationen und Architekturfragen gedacht,
nicht für vollwertige Tasks.

### 4 Rubriken (Master-Doku: `MEMORY-RUBRIKEN.md`)

| Rubrik | Wofür |
|---|---|
| `[VERIFY]` | Spätere Routing-/Trigger-Verifikation im Live-Betrieb |
| `[ARCH-OPEN]` | Offene Struktur- oder Trigger-Fragen |
| `[INFRA-TODO]` | Kleine Infra-Aufgabe, nicht ClickUp-würdig |
| `[REVIEW-PENDING]` | Externe Review-Antwort steht noch aus |

### Beim Anlegen oder Redesign eines Skills

- Offene Struktur- oder Trigger-Fragen → `[ARCH-OPEN]`
- Spätere Routing-/Trigger-Verifikation im Live-Betrieb → `[VERIFY]`
- Externe Review-Antwort steht noch aus → `[REVIEW-PENDING]`

### Regeln

- **Keine ClickUp-würdigen Aufgaben in Memory ablegen** — wenn substantielle
  Arbeit anfällt, `tracker neu` statt Memory-Eintrag
- **Keine neuen Rubriken erfinden** — die 4 Rubriken sind verbindlich
- **Erledigung nur nach Herbert-Bestätigung:** wenn ein Memory-Eintrag durch
  den Skill-Abschluss erledigt wurde, zuerst bestätigen lassen, dann entfernen
  (Cowork `memory_user_edits remove`; Claude Code Memory-Datei + Indexzeile) – kein stilles Löschen

### Abgrenzung

- **Memory** = offene Merker/Fragen, kleine Todos ohne Versionsrelevanz
- **ClickUp** = substantielle Arbeit mit Commit, Zielversion, mehreren Schritten

Vollständige Konvention + Abgrenzung + Lifecycle: `MEMORY-RUBRIKEN.md`.

Adressiert Phase 4.2.

---

## VERBOTEN

- Skill aus dem Gedächtnis schreiben (immer mit Capture Intent zuerst — auch wenn man "weiß was rein muss")
- Description ohne expliziten "Do not trigger for"-Teil
- Eval-Scripts oder Subagent-Spawn erfinden (nicht in claude.ai verfügbar — `aggregate_benchmark.py`, `run_loop.py`, `package_skill.py` nicht referenzieren)
- skill-pflege-Aufgaben übernehmen → Verweis auf skill-pflege
- Skill-Body baut auf Tools/Pfade die in der Description nicht angedeutet sind (Principle of Lack of Surprise)
- Two-Place vergessen (immer Repo mit CHANGELOG/INDEX/Commit + Lieferung an den User)
- Test-Prompts weglassen (auch wenn klein — `test-prompts.md` mindestens als Platzhalter mit 2-3 Cases)
- Skill ohne Konflikt-Check zu existierenden Skills veröffentlichen (Trigger-Überlappung prüfen)
- Skill-Namen vergeben ohne Kollisions-Check (Cowork `/mnt/skills/examples/`, `/mnt/skills/public/`; Claude Code Skill-Liste der Sitzung) – Anthropic-Beispiele blockieren z.B. `skill-creator`
- **Prosa-Fragen bei festen Entscheidungsoptionen** — IMMER Auswahlfrage
- **Skill liefern, bevor die Neutralitäts-Checkliste (Schritt 3a) abgehakt ist** – Werkzeugnamen als Vorschrift, Projektwerte oder Sprache im Skill, fehlende Umgebungsweiche
- **Projekt in der Description als Zuständigkeit nennen** („BPM-Skills“, „BPM-Code“) – Projekte nur als Beispiel
- **description über 1024 Zeichen** – Upload wird abgelehnt
- **Skill mit references nur als SKILL.md liefern** – Zip mit references/
- **Memory-Disziplin ignorieren** — ClickUp-würdige Aufgaben in Memory ablegen, neue Rubriken erfinden oder Memory-Einträge ohne Herbert-Bestätigung entfernen (siehe MEMORY-DISZIPLIN-Abschnitt + `MEMORY-RUBRIKEN.md`)

---

## VERWEIS

**Bestehenden Skill ändern? → `skill-pflege`**

`skill-pflege` ist der Schwester-Skill für Änderungen. Er hat eigene Schutzmechanismen (Original zeilengenau übernehmen, additive Default-Philosophie, Diff-Report). `skill-neu` macht ausschließlich Neu-Erstellung.

Faustregel:
- Existiert die SKILL.md schon? → `skill-pflege`
- Datei wird ganz neu angelegt? → `skill-neu` (hier)
