---
name: chatgpt-review
description: >
  Erstellt Prompts und Folgeprompts für ein technisches Review-Gespräch zwischen
  Claude und ChatGPT (inkl. Runden-Folgeprompts wie "Runde 3 erstellen") und
  archiviert jede Runde im Repo (CGR-System) – projektneutral nach dem
  Review-Profil des Repos (BPM, Heidi, …). Use when users want a ChatGPT review prompt, a second opinion from ChatGPT, a
  reply prompt to ChatGPT feedback, or a structured cross-LLM critique. Do not
  trigger for normal chat handovers, prompts for the next Claude session, or
  vague replies without explicit ChatGPT review context.
---

# ChatGPT Review-Gespräch

Ermöglicht strukturiertes Review zwischen Claude und ChatGPT.
Der User kopiert Prompts zwischen beiden und entscheidet.

Was projektspezifisch ist (Ablage, Themen, Repo, Pflicht-Block, Kontextquelle), steht im
**Review-Profil** der CLAUDE.md des Repos (Abschnitt „Voraussetzung: Review-Profil“). Der Skill
läuft im Cowork-Chat (DC, Artifact) und in Claude Code (Write, Bash, SendUserFile).

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
Auswahlfrage den Typ klären: "Claude-Handover (chat-wechsel) oder
ChatGPT-Review (chatgpt-review)?"

---

## Branch-Ermittlung

Branch aus Chat-Kontext verwenden. Mit Shell (Claude Code: Bash/PowerShell, Cowork: DC):
`git branch --show-current`. Ohne Shell und unbekannt: per Auswahlfrage fragen.
NIE automatisch einen Branch annehmen.

## Voraussetzung: Review-Profil

Abschnitt `## Review-Profil` in der `CLAUDE.md` des Repos (Claude Code liest sie automatisch;
Cowork per DC). Felder:

| Feld | Bedeutung | BPM | Heidi |
|------|-----------|-----|-------|
| Review-Ablage | Ordner der CGR-Serien + `INDEX.md` | `Docs/Referenz/chatgpt-reviews/` | `docs/chatgpt-reviews/` |
| Themen | erlaubte `<thema>`-Werte (kebab-case) | skillsystem, docs-refactor, bpm-architektur, datenschutz-dbschema | heidi-v2, karte, backend, geraeteprofil |
| GitHub-Repo | Owner/Repo für den Repo-Zugriff-Block | aus INDEX.md Projekt-Metadaten | `herbertschrotter-blip/herbert-smarthome` |
| Pflicht-Block | Abschnitt, der in jedem Initialprompt steht | „Frühphase“ (keine Migration, Reset statt Backward-Compat) | „Regeln des Neubaus“: Bauplan Abschnitt 2 in Kurzform, Paritätsregel (Abweichung nur mit PD-Eintrag), Entitäts-Vertrag eingefroren, v1 nur Referenz |
| Kontextquelle | woraus „Projektkontext“ im Prompt gebaut wird | Quickloads + Invarianten (DOC-STANDARD Kap. 8) | Bauplan Abschnitt 2 (Regeln), 4 (Vertrag), 7 (Seiten), die betroffene Karte aus 8, HANDOFF 3e; max. 3–5 Blöcke |
| Reviewer-Rolle | Rolle im Prompt | „erfahrener .NET/WPF-Architekt“ | „erfahrener Frontend-Architekt für Web Components / Home Assistant“ |
| Ergebnis-Ort | wohin Entscheidungen nach Phase 3 gehen | ADR.md, BACKLOG.md | Bauplan Abschnitt 10 (Notiz, Art `Widerspruch`/`Befund`), 10a bei Abweichung, HANDOFF 3e |

**Fehlt das Profil:** BPM-Werte aus diesem Skill annehmen – nur wenn das Repo `Docs/Referenz/` hat;
sonst Auswahlfrage „Profil anlegen (Vorschlag aus dem Repo)“. Repo-Pfad: Tracker-Profil (Claude Code)
bzw. Memory `[PROJECT]` (Cowork).

## 🚨 VERBINDLICHE REGEL: Auswahlfrage bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS eine Auswahlfrage
gestellt werden — KEINE Prosa-Fragen.** Auswahlfrage = Frage-Werkzeug der Umgebung
mit anklickbaren Optionen (Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion`).

### Diese Fragen IMMER als Auswahlfrage:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (nur wenn die Shell ihn nicht liefert) | Branch-Namen aus `git branch -a` |
| Ungepushte Commits vor einem Prompt mit Repo-Zugriff | Jetzt pushen, Im Prompt vermerken, Abbrechen |
| Phase 3: Ergebnisse übernehmen | Entscheidungen an Ergebnis-Ort, Offene Punkte als Tasks (tracker), Beides, Nur Zusammenfassung |
| Rundenstand aus Archiv widerspricht Chat | Archiv gilt (r<N>), Chat gilt, Abbrechen |
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

Jede Review-Runde wird im Repo unter der **Review-Ablage des Profils** archiviert
(BPM: `Docs/Referenz/chatgpt-reviews/`; Heidi: `docs/chatgpt-reviews/`). Schreiben: Cowork via DC,
Claude Code via Write/Bash – die Struktur ist dieselbe. Die Archivierung läuft **inkrementell** — pro Runde 4 Dateien,
angelegt in der jeweiligen Gesprächsphase.

### ID-Schema

```
CGR-<YYYY-MM-DD>-<thema>-r<runde>
```

- `YYYY-MM-DD` = Vollständiges Startdatum der Serie (Tag der ersten Runde)
- `<thema>` = kebab-case aus Themen-Enum
- `r<runde>` = Rundennummer (r1, r2, r3, ...)

### Themen-Enum (aus dem Review-Profil)

Beispiel BPM:
- `skillsystem` — Skill-System-Architektur, Trigger, Description-Schema
- `docs-refactor` — Dokumentationsstruktur, Frontmatter, INDEX, Quickloads
- `bpm-architektur` — BPM-Code-Architektur (SQLite, Domain, Infra)
- `datenschutz-dbschema` — DSGVO, DB-Schema, Whitelist

Beispiel Heidi: `heidi-v2` (Neubau der Karte), `karte`, `backend`, `geraeteprofil`.

- **Neues Thema** — Auswahlfrage mit Option "neues Thema", dann
  Namensvorschlag per Prosa-Frage, danach Themenliste im Review-Profil **und** in der
  `INDEX.md` der Review-Ablage erweitern

### Ablagestruktur pro Serie

```
<Repo>/<Review-Ablage>/
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
<Repo>/<Review-Ablage>/INDEX.md
```

Pro Serie eine Zeile in der Tabelle "Aktueller Stand". Bei neuer Runde:
Status-Update. Bei Serie-Abschluss: Kernergebnis eintragen.

### Serie starten (vor Phase 1)

Wenn der User eine neue Review-Serie startet, VOR Phase 1 Initialprompt:

1. **Thema ermitteln** via Auswahlfrage (Optionen = Themen aus dem Review-Profil + "neues Thema"):
   ```
   Frage: "Thema der Review-Serie?"
   Optionen (Beispiel BPM): "skillsystem", "docs-refactor", "bpm-architektur",
             "datenschutz-dbschema", "neues Thema"
   ```
   Bei "neues Thema": Prosa-Frage nach Kurzname (kebab-case).

2. **CGR-ID festziehen:** `CGR-<aktuelles-YYYY-MM-DD>-<thema>`
   (aktuelles Datum nehmen, nicht fragen)

3. **Repo-Pfad ermitteln:**
   - Claude Code: Repo-Wurzel der Sitzung (`git rev-parse --show-toplevel`)
   - Cowork: Memory `[PROJECT]`-Eintrag (enthält Repo-Pfad); falls nicht vorhanden: Prosa-Frage

4. **Ordner anlegen** (Cowork DC `create_directory`, Claude Code Bash `mkdir -p`):
   ```
   <Repo>/<Review-Ablage>/CGR-YYYY-MM-DD-<thema>/
   ```

5. **README.md Stub** (Cowork DC, Claude Code Write):
   ```markdown
   # CGR-YYYY-MM-DD-<thema> — <Serie-Titel>

   **Thema:** <Beschreibung>
   **Zeitraum:** <YYYY-MM-DD>
   **Branch:** <Branch>
   **Ursprungs-Chat:** <optional, nur Cowork>
   **Status:** Runde 1 offen

   ---

   ## Runden-Übersicht

   ### Runde 1 — <Titel>
   - **Artefakte:** [r1/](./r1/)
   - **Fokus:** ...
   - **Kernergebnis:** ...
   ```

6. **INDEX.md erweitern** (Cowork DC `edit_block`, Claude Code Edit):
   ```
   <Repo>/<Review-Ablage>/INDEX.md → neue Zeile in Tabelle "Aktueller Stand"
   ```

### Rundenstand aus dem Archiv (Pflicht vor jeder Runde)

Rundennummer und Status werden **aus dem Archiv gelesen, nicht aus dem Chat gezählt**:

1. `README.md` der Serie lesen (Status-Zeile, Runden-Übersicht)
2. Vorhandene `r<N>/`-Ordner listen (Claude Code: Glob; Cowork: DC `list_directory`) und je Ordner prüfen,
   welche der vier Dateien existieren
3. Daraus folgt: letzte Runde = höchstes N; ist `r<N>/04-user-decisions.md` vorhanden → nächste Runde ist N+1;
   fehlt in r<N> eine Datei → diese Runde ist offen, dort weitermachen
4. Widerspricht der Chat dem Archiv (z.B. „Runde 3 erstellen“, aber r3 existiert schon mit 01) →
   Auswahlfrage „Archiv gilt / Chat gilt / Abbrechen“

### Runde starten (innerhalb laufender Serie)

Wenn innerhalb einer bestehenden Serie eine neue Runde beginnt:

1. **r<N>/-Ordner anlegen** (Cowork DC `create_directory`, Claude Code Bash `mkdir -p`):
   ```
   <Repo>/<Review-Ablage>/CGR-YYYY-MM-DD-<thema>/r<N>/
   ```

2. **4 Platzhalter-Dateien** erst bei Befüllung anlegen — nicht vorab
   alle 4 leer anlegen. Lifecycle siehe unten.

### Lifecycle pro Runde (4 Datei-Checkpoints)

| Phase | Aktion | Datei |
|-------|--------|-------|
| Phase 1 Initialprompt erstellt | `01-claude-prompt.md` schreiben (DC / Write) | r<N>/01-claude-prompt.md |
| User pastet ChatGPT-Antwort | `02-chatgpt-response.md` schreiben (DC / Write) | r<N>/02-chatgpt-response.md |
| Phase 2 Stufe A Claude-Analyse | `03-claude-analysis.md` schreiben (DC / Write) | r<N>/03-claude-analysis.md |
| User-Entscheidungen nach Stufe A | `04-user-decisions.md` schreiben (DC / Write) | r<N>/04-user-decisions.md |

**Regel:** Jede Datei wird direkt in der zugehörigen Gesprächsphase
angelegt — nicht gesammelt am Rundenende. So bleibt das Archiv auch bei
Chat-Abbruch lückenlos.

### Serie abschließen

Wenn User signalisiert "Serie fertig" / "keine weitere Runde":

1. **README.md finalisieren:**
   - Kernergebnisse pro Runde
   - Links zu resultierenden ADRs / Bauplan-Notizen / Commits
   - Status: "Abgeschlossen"
2. **INDEX.md Status-Update:** Status-Spalte auf "Abgeschlossen",
   Kernergebnis-Spalte befüllen.
3. **Ergebnisse übernehmen** (Auswahlfrage, siehe Phase 3): Entscheidungen an den Ergebnis-Ort des Profils,
   offene Punkte als Tasks über den tracker-Skill (Präfix des Projekts).
4. Commit der Archivdateien: `[vX.Y.Z] <Doku-Modul>, Docs: CGR-<id> Runde <N> / Abschluss`
   (Claude Code committet selbst; Cowork liefert den Befehl)

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
- **Repo:** [Owner/Repo aus dem Review-Profil; BPM: INDEX.md Projekt-Metadaten]
- **Branch: `[aktueller Branch]`** — IMMER diesen Branch verwenden, NICHT `main`!
- Nutze das aktiv um Aussagen zu verifizieren, Querverweise zu prüfen,
  und Originaldateien zu lesen wenn der Kontext im Prompt nicht reicht.
- Bei JEDEM Dateizugriff den Branch `[aktueller Branch]` angeben!
```

**Regeln:**
- Branch NICHT hardcoden — immer den in dieser Session ermittelten Branch verwenden
- Owner/Repo aus dem Review-Profil (BPM: INDEX.md Projekt-Metadaten)
- **Push-Prüfung (Pflicht vor jedem Prompt mit Repo-Zugriff):** mit Shell
  `git fetch --quiet && git log origin/<branch>..HEAD --oneline` – gibt es Commits, sieht ChatGPT alte
  Dateien. Dann Auswahlfrage: „Jetzt pushen“ (Claude Code pusht selbst; Cowork liefert den Befehl) /
  „Im Prompt vermerken“ (Block ergänzen: „Stand auf GitHub ist <hash>, neuere Änderungen stehen unten im
  Prompt“) / „Abbrechen“. Ohne Shell: User fragen, ob gepusht ist.
- Uncommittete Änderungen an Dateien, die im Prompt genannt werden, ebenfalls nennen (`git status --short`)

## Doc-Laderegel (Kontextquelle aus dem Review-Profil)

Beim Erstellen des Initialprompts den Projektkontext aus der **Kontextquelle des Profils** bauen:

BPM (DOC-STANDARD.md Kapitel 8):
1. INDEX.md → Welche Docs sind für das Review-Thema relevant?
2. Quickloads der relevanten Docs lesen
3. Fachliche Invarianten sammeln
4. Relevante Quickloads + Invarianten als Kontext in den Prompt packen

Heidi:
1. Bauplan Abschnitt 2 (Regeln) → Kurzform der Regeln, die das Thema berühren
2. Abschnitt 4 (Entitäts-Vertrag) → nur die betroffenen Entitäten/Dienste
3. Die betroffene Aufgabenkarte aus Abschnitt 8 (Ziel, Nicht ändern, Akzeptanz) und Abschnitt 7 (Seite)
4. HANDOFF 3e → Stand, Version, Stolpersteine; Abschnitt 10/10a → bekannte Befunde und Abweichungen

So weiß ChatGPT z.B. "SQLite ist SoR" (BPM) oder "Schreiben nach HA nur über DxApi, Vertrag eingefroren"
(Heidi) ohne dass der User es manuell einfügt.

**Format im Prompt:**

```
## Projektkontext (aus der Kontextquelle des Profils; BPM: Quickloads)

### [Doc-Name] (source_of_truth)
- Zweck: [aus Quickload]
- Fachliche Invarianten:
  - [aus Quickload]

### [Doc-Name] (secondary)
- Zweck: [aus Quickload]
```

Nur Blöcke einfügen die relevant sind — nicht alle Docs.
Max 3-5 Blöcke im Prompt, sonst wird er zu lang.

## Pflicht-Block des Projekts (PFLICHT in jedem Initialprompt)

Jedes Projekt hat Regeln, die ChatGPT kennen muss, damit es keine Vorschläge macht, die wir
ausdrücklich nicht wollen. Welcher Block das ist, steht im Review-Profil („Pflicht-Block“).

**Heidi – „Regeln des Neubaus“:**

```
## Regeln des Neubaus (PFLICHT-Hinweis)

- v1 (heidi/archiv/heidi-panel.js) ist nur Referenz für Verhalten und Vektoren; v2 wird portiert, nicht neu erfunden.
- Der Entitäts-Vertrag (Bauplan Abschnitt 4) ist eingefroren; neue Entitäten nur mit Vertragsänderung.
- Jede gewollte Abweichung vom v1-Verhalten braucht einen PD-Eintrag (Abschnitt 10a) mit Freigabe durch Herbert.
- Schreiben nach HA nur über die API-Klasse; Komponenten lesen nur Views aus Selektoren; nichts fest verdrahten,
  was Roboter oder HA liefern.
- Keine externen Ressourcen (Fonts, CDN); Tests (npm test) grün vor jedem Commit.

Quelle: docs/dreame_x60/BAUPLAN.md Abschnitt 2.
```

**BPM – „Frühphase“:** INDEX.md hat das Kapitel "Projekt-Phase (VERBINDLICH)". Solange dieses Kapitel
besteht, MUSS jeder Initialprompt einen Frühphasen-Block enthalten, damit
ChatGPT keine Migrations-/Backward-Compatibility-Vorschläge macht die wir
ausdrücklich nicht wollen.

**Block der eingefügt werden muss (BPM):**

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

**Regel (beide Projekte):**
- Der Block kommt als eigener Abschnitt in den Initialprompt, **vor** "Projektkontext"
- Bei Folgeprompts (Runde 2, 3, ...) nicht nochmal einfügen — einmal pro Review reicht
- Wenn der User eine Regel bewusst aussetzt (z.B. Migration will), Block anpassen und im Prompt erwähnen warum

---

## Gesprächsphasen

### Phase 1: Initialprompt

```
## Rolle
Du bist ein erfahrener [Reviewer-Rolle aus dem Review-Profil] und führst ein technisches
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

## <Pflicht-Block des Projekts>
[Block aus "Pflicht-Block des Projekts" oben einfügen – BPM Frühphase, Heidi Regeln des Neubaus]

## Projektkontext
[Blöcke aus der Kontextquelle des Profils hier einfügen]

## Das Konzept
[Vollständiges Konzept/Code/Architektur]

## Aufgabe
[Spezifische Prüfpunkte]
```

**Wichtig:**
- ALLEN Kontext aus dem Chat sammeln
- Code vollständig, nicht gekürzt
- Kontextquelle des Profils als Projektkontext einbauen (BPM: Quickloads; Heidi: Bauplan-Abschnitte)
- Fachliche Invarianten / Regeln explizit aufführen
- Repo-Zugriff Block mit aktuellem Branch IMMER einfügen – nach Push-Prüfung

**Archivierung (CGR-System):**
- Vor dem Erstellen: Rundenstand aus dem Archiv lesen; sicherstellen dass `CGR-YYYY-MM-DD-<thema>/r<N>/` existiert
  (anlegen wenn neu)
- Nach dem Erstellen: Prompt-Text 1:1 als `r<N>/01-claude-prompt.md` ablegen
- Bei Runde 1: zusätzlich Serie-Stub anlegen (siehe "Serie starten")

### Phase 2: Antwort/Reaktion

#### Stufe A — Einschätzung + Auswahlfrage

**Vor Stufe A: ChatGPT-Antwort archivieren.**
User hat die Antwort in den Chat gepastet (oder als Datei geschickt). Vor der Einschätzung:
- ChatGPT-Antwort 1:1 als `r<N>/02-chatgpt-response.md` ablegen

**Dann Stufe A:**

1. Eigene Einschätzung zusammenfassen
2. Einschätzung zusätzlich als `r<N>/03-claude-analysis.md` ablegen
3. Auswahlfrage mit Entscheidungspunkten (max 3 Fragen)
4. Immer Option "ChatGPT fragen" anbieten

#### Stufe B — Folgeprompt (nach User-Antwort)

**Vor Stufe B: User-Entscheidungen archivieren.**
- User-Antworten auf die Stufe-A-Fragen als `r<N>/04-user-decisions.md`
  ablegen

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

**Ergebnisse zurück ins Repo (Auswahlfrage, nie automatisch):**
- „Entscheidungen an Ergebnis-Ort“ → jede getroffene Entscheidung als Eintrag am Ergebnis-Ort des Profils
  (Heidi: Bauplan Abschnitt 10 als Notiz `[Datum] [Aufgabe] Widerspruch/Befund · Schwere: … Entscheidung Herbert: …`,
  Abweichung vom v1-Verhalten zusätzlich als PD-Eintrag 10a; BPM: ADR.md). Schreiben tut doc-pflege (Modus 7a/2),
  dieser Skill liefert die fertigen Einträge.
- „Offene Punkte als Tasks“ → `tracker neu` je Punkt im Schema des Projekts (`<PRÄFIX>-NNN | KÜRZEL | …`),
  mit Verweis auf `CGR-<id> r<N>` in der Beschreibung
- „Beides“ / „Nur Zusammenfassung“
Verweise in beide Richtungen: README der Serie nennt die Bauplan-Notizen/ADRs und Task-IDs; Notiz/ADR nennt die CGR-ID.

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
- Bei Uneinigkeit: User per Auswahlfrage entscheiden lassen

---

## Formatierung

**Zwei Ablage-Orte für Prompts:**

1. **Primär: Repo-Archiv** (CGR-System, Review-Ablage des Profils):
   ```
   <Repo>/<Review-Ablage>/CGR-YYYY-MM-DD-<thema>/r<N>/
     ├── 01-claude-prompt.md
     ├── 02-chatgpt-response.md
     ├── 03-claude-analysis.md
     └── 04-user-decisions.md
   ```

2. **Zusätzlich: Copy-Paste-Hilfe** für den User. Damit der User den
   Prompt schnell in ChatGPT pasten kann, liefert Claude den Prompt-Text
   zusätzlich als Datei:
   - **Cowork:** `/mnt/user-data/outputs/chatgpt-review-prompt.md` (Initial) bzw.
     `chatgpt-review-runde-N.md` (Folgeprompt) via `create_file` + `present_files` als Dateikarte
   - **Claude Code:** die Archivdatei `r<N>/01-claude-prompt.md` per `SendUserFile` (attach) –
     dieselbe Datei, kein zweiter Ort

Phase 2 Stufe A: direkt im Chat + Auswahlfrage.
Datei erst in Stufe B.

## Sprache

Prompts in der Sprache des Users.

---

## VERBOTEN

- Branch automatisch annehmen (Shell fragen oder Auswahlfrage)
- Multiple-Choice als Prosa statt Auswahlfrage
- Stufe A Entscheidungspunkte als Prosa statt Auswahlfrage
- Uneinigkeit ohne Auswahlfrage auflösen
- Initialprompt ohne den Pflicht-Block des Projekts erstellen (BPM Frühphase, Heidi Regeln des Neubaus)
- **Prompt mit Repo-Zugriff-Block ohne Push-Prüfung** – ChatGPT liest sonst alte Dateien
- **Rundennummer aus dem Chat raten** statt aus README/r<N>-Ordnern zu lesen
- **Phase 3 ohne Auswahlfrage „Ergebnisse übernehmen“ beenden** – Entscheidungen bleiben sonst nur im Chat
- **BPM-Ablage, -Themen oder -Frühphase für ein anderes Projekt annehmen** – alles aus dem Review-Profil
- **Review-Serie starten ohne CGR-Ordner + README.md + INDEX.md-Zeile** (Phase 4.6)
- **Runde durchlaufen ohne die 4 Dateien inkrementell abzulegen** — 01 in Phase 1, 02 vor Stufe A, 03 in Stufe A, 04 zwischen Stufe A und B
- **INDEX.md-Status nicht aktualisieren** bei neuer Runde / Serie-Abschluss
- **Alle 4 Dateien einer Runde gesammelt am Rundenende anlegen** — Archiv-Lücken bei Chat-Abbruch
- **CGR-ID aus falschem Datum verwenden** — immer das aktuelle `YYYY-MM-DD` beim Serie-Start nehmen, auch wenn die Runde später läuft
