---
name: chatgpt-review
description: >
  Erstellt Prompts und Folgeprompts für ein technisches Review-Gespräch zwischen
  Claude und ChatGPT (inkl. Runden-Folgeprompts wie "Runde 3 erstellen"). Use
  when users want a ChatGPT review prompt, a second opinion from ChatGPT, a
  reply prompt to ChatGPT feedback, or a structured cross-LLM critique. Do not
  trigger for normal chat handovers, prompts for the next Claude session, or
  vague replies without explicit ChatGPT review context.
---

# ChatGPT Review-Gespräch

Ermöglicht strukturiertes Review zwischen Claude und ChatGPT.
Der User kopiert Prompts zwischen beiden und entscheidet.

---

## Vorrang / Delegation an andere Skills

**chatgpt-review erzeugt Prompts für ein Review-Gespräch mit ChatGPT
(zweite Meinung, Cross-LLM-Kritik). Wenn die Hauptabsicht ein anderer
Prompt-Typ oder Workflow ist, NICHT hier weiterarbeiten, sondern
delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Handover-Prompt für nächste Claude-Session | **chat-wechsel** |
| Code schreiben | **code-erstellen** |
| ClickUp-Task-Aktion | **tracker** |
| Doc schreiben (ADR, Konzept) | **doc-pflege** |

Nur wenn die Hauptabsicht **ein ChatGPT-Review-Prompt oder Folgeprompt**
ist ("Review-Prompt für GPT", "zweite Meinung", "ChatGPT fragen",
"Cross-LLM-Kritik"), bleibt chatgpt-review zuständig.

**Wichtig:** Generische "mach mir den Prompt"-Aufforderungen ohne ChatGPT-
oder Claude-Kontext triggern KEINEN der beiden Skills automatisch — per
`ask_user_input_v0` den Typ klären: "Claude-Handover (chat-wechsel) oder
ChatGPT-Review (chatgpt-review)?"

---

## Branch-Ermittlung

Branch aus Chat-Kontext verwenden.
Wenn Branch in dieser Session noch nicht bekannt: Per ask_user_input_v0 fragen.
NIE automatisch einen Branch annehmen.

## 🚨 VERBINDLICHE REGEL: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0`
verwendet werden — KEINE Prosa-Fragen.**

### Diese Fragen IMMER mit ask_user_input_v0:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (unbekannt) | Branch-Namen aus `git branch -a` |
| Phase 2 Stufe A: Entscheidungspunkte | je nach Review-Thema + immer "ChatGPT fragen" |
| Bei Uneinigkeit Claude/ChatGPT | Claude zustimmen, ChatGPT zustimmen, Mittelweg, Abbrechen |
| Review-Phase wechseln | In Phase 2, In Phase 3, Weiter in aktueller Phase |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen
- User hat Präferenz signalisiert
- Freitext-Input nötig

## Vor dem Start: ChatGPT-Modell

Falls der User schon gesagt hat welches Modell: nicht nochmal fragen.

## CGR-Ablagesystem (Phase 4.6)

Jede Review-Runde wird im BPM-Repo unter `Docs/Referenz/chatgpt-reviews/`
archiviert. Die Archivierung läuft **inkrementell** — pro Runde 4 Dateien,
angelegt in der jeweiligen Gesprächsphase.

### ID-Schema

```
CGR-<YYYY-MM-DD>-<thema>-r<runde>
```

- `YYYY-MM-DD` = Vollständiges Startdatum der Serie (Tag der ersten Runde)
- `<thema>` = kebab-case aus Themen-Enum
- `r<runde>` = Rundennummer (r1, r2, r3, ...)

### Themen-Enum

- `skillsystem` — Skill-System-Architektur, Trigger, Description-Schema
- `docs-refactor` — Dokumentationsstruktur, Frontmatter, INDEX, Quickloads
- `bpm-architektur` — BPM-Code-Architektur (SQLite, Domain, Infra)
- `datenschutz-dbschema` — DSGVO, DB-Schema, Whitelist
- **Neues Thema** — `ask_user_input_v0` mit Option "neues Thema", dann
  Namensvorschlag per Prosa-Frage, danach INDEX.md-Enum erweitern

### Ablagestruktur pro Serie

```
<BPM-Repo>/Docs/Referenz/chatgpt-reviews/
└── CGR-YYYY-MM-DD-<thema>/
    ├── README.md          ← Serie-Übersicht, Runden-Zusammenfassung
    ├── r1/
    │   ├── 01-claude-prompt.md       ← Claudes Prompt an ChatGPT
    │   ├── 02-chatgpt-response.md    ← ChatGPTs Antwort im Canvas
    │   ├── 03-claude-analysis.md     ← Claudes Einschätzung/Reaktion
    │   └── 04-user-decisions.md      ← Herberts Antworten + Entscheidungen
    ├── r2/ ...
    └── r3/ ...
```

### Globaler Index

```
<BPM-Repo>/Docs/Referenz/chatgpt-reviews/INDEX.md
```

Pro Serie eine Zeile in der Tabelle "Aktueller Stand". Bei neuer Runde:
Status-Update. Bei Serie-Abschluss: Kernergebnis eintragen.

### Serie starten (vor Phase 1)

Wenn der User eine neue Review-Serie startet, VOR Phase 1 Initialprompt:

1. **Thema ermitteln** via `ask_user_input_v0`:
   ```
   Frage: "Thema der Review-Serie?"
   Optionen: "skillsystem", "docs-refactor", "bpm-architektur",
             "datenschutz-dbschema", "neues Thema"
   ```
   Bei "neues Thema": Prosa-Frage nach Kurzname (kebab-case).

2. **CGR-ID festziehen:** `CGR-<aktuelles-YYYY-MM-DD>-<thema>`
   (aktuelles Datum nehmen, nicht fragen)

3. **BPM-Repo-Pfad ermitteln:**
   - Memory scannen nach `[PROJECT]`-Eintrag (enthält BPM-Repo-Pfad)
   - Falls nicht vorhanden: Prosa-Frage nach lokalem Repo-Pfad

4. **Ordner anlegen** via DC:
   ```
   DC create_directory <BPM-Repo>/Docs/Referenz/chatgpt-reviews/CGR-YYYY-MM-DD-<thema>/
   ```

5. **README.md Stub** via DC:
   ```markdown
   # CGR-YYYY-MM-DD-<thema> — <Serie-Titel>

   **Thema:** <Beschreibung>
   **Zeitraum:** <YYYY-MM-DD>
   **Ursprungs-Chat:** <optional>
   **Status:** Runde 1 offen

   ---

   ## Runden-Übersicht

   ### Runde 1 — <Titel>
   - **Artefakte:** [r1/](./r1/)
   - **Fokus:** ...
   - **Kernergebnis:** ...
   ```

6. **INDEX.md erweitern:**
   ```
   DC edit_block <BPM-Repo>/Docs/Referenz/chatgpt-reviews/INDEX.md
     → neue Zeile in Tabelle "Aktueller Stand"
   ```

### Runde starten (innerhalb laufender Serie)

Wenn innerhalb einer bestehenden Serie eine neue Runde beginnt:

1. **r<N>/-Ordner anlegen** via DC:
   ```
   DC create_directory <BPM-Repo>/.../CGR-YYYY-MM-DD-<thema>/r<N>/
   ```

2. **4 Platzhalter-Dateien** erst bei Befüllung anlegen — nicht vorab
   alle 4 leer anlegen. Lifecycle siehe unten.

### Lifecycle pro Runde (4 Datei-Checkpoints)

| Phase | Aktion | Datei |
|-------|--------|-------|
| Phase 1 Initialprompt erstellt | `01-claude-prompt.md` via DC schreiben | r<N>/01-claude-prompt.md |
| User pastet ChatGPT-Antwort | `02-chatgpt-response.md` via DC schreiben | r<N>/02-chatgpt-response.md |
| Phase 2 Stufe A Claude-Analyse | `03-claude-analysis.md` via DC schreiben | r<N>/03-claude-analysis.md |
| User-Entscheidungen nach Stufe A | `04-user-decisions.md` via DC schreiben | r<N>/04-user-decisions.md |

**Regel:** Jede Datei wird direkt in der zugehörigen Gesprächsphase
angelegt — nicht gesammelt am Rundenende. So bleibt das Archiv auch bei
Chat-Abbruch lückenlos.

### Serie abschließen

Wenn User signalisiert "Serie fertig" / "keine weitere Runde":

1. **README.md finalisieren:**
   - Kernergebnisse pro Runde
   - Links zu resultierenden ADRs / Commits
   - Status: "Abgeschlossen"
2. **INDEX.md Status-Update:** Status-Spalte auf "Abgeschlossen",
   Kernergebnis-Spalte befüllen.

### Retroaktive Nutzung

Der Skill verwaltet auch bestehende Serien-Ordner:
- Neue Runde in bestehender Serie: regulärer "Runde starten"-Ablauf
- Historische Runden nachrüsten: on-demand, kein Pflicht-Workflow

---

## ChatGPTs Repo-Zugriff (PFLICHT in jedem Prompt)

ChatGPT hat die Möglichkeit selbst Dateien aus dem GitHub-Repo zu lesen.
**In JEDEM Prompt** (Initial, Folgeprompt, Audit) muss folgender Block enthalten sein:

```
## Repo-Zugriff

Du hast Zugriff auf das GitHub-Repo und kannst selbst Dateien lesen:
- **Repo:** [Owner/Repo aus INDEX.md]
- **Branch: `[aktueller Branch]`** — IMMER diesen Branch verwenden, NICHT `main`!
- Nutze das aktiv um Aussagen zu verifizieren, Querverweise zu prüfen,
  und Originaldateien zu lesen wenn der Kontext im Prompt nicht reicht.
- Bei JEDEM Dateizugriff den Branch `[aktueller Branch]` angeben!
```

**Regeln:**
- Branch NICHT hardcoden — immer den in dieser Session ermittelten Branch verwenden
- Owner/Repo aus INDEX.md Projekt-Metadaten lesen
- Wenn der Branch noch nicht gepusht ist: User darauf hinweisen dass
  ChatGPT die neuen Dateien nicht sehen kann

## Doc-Laderegel

Beim Erstellen des Initialprompts die verbindliche Ladereihenfolge
(DOC-STANDARD.md Kapitel 8) nutzen:

1. INDEX.md → Welche Docs sind für das Review-Thema relevant?
2. Quickloads der relevanten Docs lesen
3. Fachliche Invarianten sammeln
4. Relevante Quickloads + Invarianten als Kontext in den Prompt packen

So weiß ChatGPT z.B. "SQLite ist SoR" oder "alles über
IExternalCommunicationService" ohne dass der User es manuell einfügt.

**Format im Prompt:**

```
## Projektkontext (aus Quickloads)

### [Doc-Name] (source_of_truth)
- Zweck: [aus Quickload]
- Fachliche Invarianten:
  - [aus Quickload]

### [Doc-Name] (secondary)
- Zweck: [aus Quickload]
```

Nur Quickloads einfügen die relevant sind — nicht alle Docs.
Max 3-5 Quickloads im Prompt, sonst wird er zu lang.

## Frühphasen-Hinweis (PFLICHT in jedem Initialprompt)

INDEX.md hat das Kapitel "Projekt-Phase (VERBINDLICH)". Solange dieses Kapitel
besteht, MUSS jeder Initialprompt einen Frühphasen-Block enthalten, damit
ChatGPT keine Migrations-/Backward-Compatibility-Vorschläge macht die wir
ausdrücklich nicht wollen.

**Block der eingefügt werden muss:**

```
## Frühphase (PFLICHT-Hinweis)

BPM ist in früher Entwicklung ohne Produktivdaten.

Konsequenzen für deine Architektur-Vorschläge:
- KEINE Migrations-Logik vorschlagen
- KEINE Backward-Compatibility-Patterns
- KEINE Legacy-Tolerance in Parsern/Loadern/Deserializern
- Bei Schema-/Config-/DB-Änderungen: stattdessen "Datei löschen, neu anlegen lassen"
  als gewollter Standardweg

Ausnahme: Nur wenn explizit "Migration bauen" im Prompt steht.

Quelle: INDEX.md Kapitel "Projekt-Phase".
```

**Regel:**
- Der Block kommt als eigener Abschnitt in den Initialprompt, **vor** "Projektkontext"
- Bei Folgeprompts (Runde 2, 3, ...) nicht nochmal einfügen — einmal pro Review reicht
- Wenn der User explizit Migration will, Block weglassen und im Prompt erwähnen warum

---

## Gesprächsphasen

### Phase 1: Initialprompt

```
## Rolle
Du bist ein erfahrener [Rolle] und führst ein technisches
Review-Gespräch mit einem Kollegen (Claude/Anthropic).

## Gesprächsformat
Dieses Gespräch läuft über einen Vermittler (den User).
- Sprich direkt zu deinem Kollegen, NICHT zum User
- Kein Meta-Kommentar über das Format
- Schreibe deine GESAMTE Antwort in Canvas
- CANVAS-TITEL: "Review Runde X"
- Fasse am Ende JEDER Antwort zusammen:
  ✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen

## Repo-Zugriff
[Block von oben einfügen mit aktuellem Branch]

## Gesprächsregeln
- Ehrlich und kritisch
- Probleme konkret benennen
- Verbesserungen mit Code/Pseudocode zeigen
- Rückfragen bei fehlendem Kontext
- Fokus halten, keine allgemeinen Exkurse
- Kompakt, Code nur wenn nötig
[FALLS FOKUS:] - Fokus: [Thema]

## Frühphase (PFLICHT-Hinweis)
[Block aus "Frühphasen-Hinweis" oben einfügen]

## Projektkontext (aus Quickloads)
[Relevante Quickloads + Invarianten hier einfügen]

## Das Konzept
[Vollständiges Konzept/Code/Architektur]

## Aufgabe
[Spezifische Prüfpunkte]
```

**Wichtig:**
- ALLEN Kontext aus dem Chat sammeln
- Code vollständig, nicht gekürzt
- Quickloads verwandter Docs als Projektkontext einbauen
- Fachliche Invarianten explizit aufführen
- Repo-Zugriff Block mit aktuellem Branch IMMER einfügen

**Archivierung (CGR-System):**
- Vor dem Erstellen: sicherstellen dass `CGR-YYYY-MM-DD-<thema>/r<N>/` existiert
  (anlegen via DC wenn neu)
- Nach dem Erstellen: Prompt-Text 1:1 als `r<N>/01-claude-prompt.md` ablegen
- Bei Runde 1: zusätzlich Serie-Stub anlegen (siehe "Serie starten")

### Phase 2: Antwort/Reaktion

#### Stufe A — Einschätzung + ask_user_input_v0

**Vor Stufe A: ChatGPT-Antwort archivieren.**
User hat die Antwort in den Chat gepastet. Vor der Einschätzung:
- ChatGPT-Antwort 1:1 als `r<N>/02-chatgpt-response.md` ablegen via DC

**Dann Stufe A:**

1. Eigene Einschätzung zusammenfassen
2. Einschätzung zusätzlich als `r<N>/03-claude-analysis.md` ablegen via DC
3. `ask_user_input_v0` mit Entscheidungspunkten (max 3 Fragen)
4. Immer Option "ChatGPT fragen" anbieten

#### Stufe B — Folgeprompt (nach User-Antwort)

**Vor Stufe B: User-Entscheidungen archivieren.**
- User-Antworten auf die Stufe-A-Fragen als `r<N>/04-user-decisions.md`
  ablegen via DC

**Dann Folgeprompt für Runde N+1:**

- Basierend auf User-Entscheidungen
- Canvas-Rundennummer korrekt mitzählen
- Repo-Zugriff Block mit aktuellem Branch IMMER einfügen
- ✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen
- **Vor dem Folgeprompt: neuen Runden-Ordner `r<N+1>/` anlegen**
- **Folgeprompt als `r<N+1>/01-claude-prompt.md` ablegen**

### Phase 3: Abschluss

- Konsens
- Meinungsverschiedenheiten
- Offene Punkte
- Nächste Schritte
- Optional: überarbeitetes Konzept

**Archivierung (Serie-Abschluss):**
- `README.md` der Serie finalisieren: Kernergebnisse, Links zu ADRs/Commits,
  Status auf "Abgeschlossen"
- `INDEX.md` Status-Update: Status-Spalte "Abgeschlossen", Kernergebnis
  in entsprechender Spalte
- Letzte `04-user-decisions.md` in letzter Runde ablegen (falls noch nicht)

---

## Grundhaltung

Gleichwertiger Gesprächspartner:
- Nur zustimmen wenn überzeugt
- Aktiv widersprechen wenn nötig
- Eigene Vorschläge einbringen
- Bei Uneinigkeit: User per ask_user_input_v0 entscheiden lassen

---

## Formatierung

**Zwei Ablage-Orte für Prompts:**

1. **Primär: BPM-Repo-Archiv** (via DC, CGR-System):
   ```
   <BPM-Repo>/Docs/Referenz/chatgpt-reviews/CGR-YYYY-MM-DD-<thema>/r<N>/
     ├── 01-claude-prompt.md
     ├── 02-chatgpt-response.md
     ├── 03-claude-analysis.md
     └── 04-user-decisions.md
   ```

2. **Zusätzlich: Copy-Paste-Hilfe** für den User. Damit der User den
   Prompt schnell in ChatGPT pasten kann, liefert Claude den Prompt-Text
   zusätzlich als Download-Datei:
   ```
   /mnt/user-data/outputs/chatgpt-review-prompt.md        (Initial)
   /mnt/user-data/outputs/chatgpt-review-runde-N.md       (Folgeprompt)
   ```
   Dateien via `create_file` + `present_files` als Dateikarte.

Phase 2 Stufe A: direkt im Chat + ask_user_input_v0.
Download erst in Stufe B.

## Sprache

Prompts in der Sprache des Users.

---

## VERBOTEN

- Branch automatisch annehmen ohne ask_user_input_v0
- Multiple-Choice als Prosa statt ask_user_input_v0
- Stufe A Entscheidungspunkte als Prosa statt ask_user_input_v0
- Uneinigkeit ohne ask_user_input_v0 auflösen
- Initialprompt ohne Frühphasen-Hinweis-Block erstellen (siehe Frühphasen-Prinzip in INDEX.md)
- **Review-Serie starten ohne CGR-Ordner + README.md + INDEX.md-Zeile** (Phase 4.6)
- **Runde durchlaufen ohne die 4 Dateien inkrementell abzulegen** — 01 in Phase 1, 02 vor Stufe A, 03 in Stufe A, 04 zwischen Stufe A und B
- **INDEX.md-Status nicht aktualisieren** bei neuer Runde / Serie-Abschluss
- **Alle 4 Dateien einer Runde gesammelt am Rundenende anlegen** — Archiv-Lücken bei Chat-Abbruch
- **CGR-ID aus falschem Datum verwenden** — immer das aktuelle `YYYY-MM-DD` beim Serie-Start nehmen, auch wenn die Runde später läuft
