---
name: chat-wechsel
description: >
  Erstellt einen Übergabe-Prompt für den nächsten Chat. Triggert bei
  "neuer chat", "nächster chat", "session beenden", "chat wechsel",
  "weiter im nächsten chat", "mach mir den prompt", "übergabe".
  NICHT bei "pause", "tschüss", "gute nacht".
---

# Chat-Wechsel Skill

## Zweck

Übergabe-Prompt wenn Session endet und im nächsten Chat weitergearbeitet wird.

---

## 🚨 VERBINDLICHE REGEL: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0`
verwendet werden — KEINE Prosa-Fragen.**

### Diese Fragen IMMER mit ask_user_input_v0:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung | Alle Branch-Namen aus `git branch -a` als Optionen |
| Batch-Abschluss: erledigte Tasks | "Alle als Done markieren", "Einzeln wählen", "Keine" |
| Batch-Abschluss: erledigte Tasks einzeln wählen | multi_select mit allen Task-Namen |
| Batch-Anlage: neue Tasks aus Chat | "Alle anlegen", "Einzeln wählen", "Keine" |
| Batch-Anlage: neue Tasks einzeln wählen | multi_select mit allen erkannten Problemen |
| ClickUp nicht erreichbar | "Trotzdem Prompt erstellen", "Retry", "Abbrechen" |
| Version-Angabe unklar | Aktuelle Versionen als Optionen |
| Kein Commit-Stand erkennbar | "Version vom User eingeben", "Ohne Version", "Abbrechen" |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen  
  (Beispiel: "Welche Version ist aktuell?" ohne Kandidaten)
- User hat gerade eine klare Präferenz signalisiert
- Es ist Erklärung/Kontext, keine echte Entscheidung

### Wie ask_user_input_v0 aussieht

```
ask_user_input_v0(
  questions: [
    {
      question: "Welcher Branch ist aktiv?",
      options: ["main", "feature/planmanager-v1", "feature/settings-tabs"]
    }
  ]
)
```

Multi-Select für Listen-Auswahl:
```
ask_user_input_v0(
  questions: [
    {
      question: "Welche Tasks als Done markieren?",
      type: "multi_select",
      options: ["BPM-001 | PM | DB-Anbindung", "BPM-007 | SET | CS8629 Fix", "BPM-012 | SET | Token-Migration"]
    }
  ]
)
```

### VERBOTEN

- "→ Alle als Done markieren? (ja / nein / einzeln wählen)" als Prosa
- "→ Diese Tasks anlegen? (ja / nein / einzeln wählen)" als Prosa
- Branch-Liste im Chat aufzählen und auf getippte Antwort warten
- Eine Optionen-Aufzählung im Chat ohne ask_user_input_v0

---

## Branch-Ermittlung (PFLICHT)

1. Prüfe ob Branch bereits in dieser Session bekannt ist → verwenden
2. Wenn nicht bekannt: Alle Branches via GitHub API oder `git branch -a` via DC auflisten
3. **Per `ask_user_input_v0`** den aktiven Branch wählen lassen (Optionen = Branch-Namen)
4. Gewählten Branch für die gesamte Session merken
5. NIE automatisch einen Branch annehmen (weder `main` noch einen anderen)
6. Den ermittelten Branch im Übergabe-Prompt unter `**Branch:**` eintragen

---

## TRIGGER

Ja: "neuer chat", "nächster chat", "session beenden", "chat wechsel",
"weiter im nächsten chat", "mach mir den prompt", "übergabe"

Nein: "pause", "tschüss", "gute nacht"

---

## ClickUp-Integration (vor Übergabeprompt)

### Schritt 1: Offene Tasks laden

1. `[CLICKUP]` Eintrag aus Memory lesen → Space-ID
2. `clickup_filter_tasks(space_ids: ["<Space-ID>"], statuses: ["open", "in progress"])`
3. Tasks nach Listen gruppieren

### Schritt 2: Chat-Verlauf scannen

Chat scannen auf:
- Tasks die bearbeitet aber nicht als Done markiert wurden
- Neue Probleme die aufgetaucht aber nicht erfasst sind
- NUR nach klaren Mustern: `TODO:`, `offen:`, `neuer punkt:`, `neue aufgabe:`,
  `später:`, klare Problemformulierungen mit Handlungsbezug
- NICHT jede Erwähnung eines Problems als neuen Task interpretieren

### Schritt 3: Batch-Abschluss (ask_user_input_v0!)

Strukturierte Übersicht im Chat zeigen:

```
### ClickUp Tracker — Batch-Abschluss

**Im Chat erledigt — als Done markieren?**
- BPM-003 | DB-Anbindung Orchestrator
- BPM-007 | CS8629 Warning behoben
- BPM-012 | Token-Migration

**Im Chat neu erkannt — Task anlegen?**
- PlanManager — <neues Problem aus diesem Chat>
- Docs — <neuer Doc-Punkt>

**Weiterhin offen laut ClickUp:**
PlanManager (4):
- [high] [V1] BPM-004 | 5998er Statikplaene Erkennung
- [normal] [V1] BPM-008 | Mockup ManuellSortieren
...
Docs (1):
- [normal] [V1-Nice] BPM-015 | ADR-050 schreiben
```

Dann **zwei `ask_user_input_v0` Aufrufe**:

**Erster Aufruf — Done-Markierungen:**
```
ask_user_input_v0(
  questions: [{
    question: "Welche Tasks als Done markieren?",
    type: "multi_select",
    options: [
      "BPM-003 | DB-Anbindung Orchestrator",
      "BPM-007 | CS8629 Warning behoben",
      "BPM-012 | Token-Migration",
      "Keine"
    ]
  }]
)
```

**Zweiter Aufruf — Neue Tasks:**
```
ask_user_input_v0(
  questions: [{
    question: "Welche neuen Tasks anlegen?",
    type: "multi_select",
    options: [
      "PlanManager — <neues Problem>",
      "Docs — <neuer Doc-Punkt>",
      "Keine"
    ]
  }]
)
```

### Schritt 4: Nach Bestätigung ausführen

- Done-Tasks: `tracker done` pro ausgewähltem Task (mit Commit-Kommentar)
- Neue Tasks: `tracker neu` pro ausgewähltem Task (Fragemodus per ask_user_input_v0 im tracker-Skill)
- Memory `[CLICKUP]` Eintrag aktualisieren: `Letzte Sync: Teil <N>`

### ClickUp nicht erreichbar?

Per `ask_user_input_v0`:
```
Frage: "ClickUp nicht erreichbar. Wie weiter?"
Optionen: "Trotzdem Prompt erstellen", "Retry", "Abbrechen"
```

Bei "Trotzdem Prompt erstellen": Hinweis in Prompt einfügen, Übergabe aus Chat-Verlauf.

---

## Chat-Anker-Übergabe

**Zweck:** Die Live-Registry `[ANKER-LIVE]` (aus dem Chat-Anker-System, siehe tracker-Skill) muss beim Chat-Wechsel in den neuen Chat transportiert werden, weil Memory pro Session gilt.

### Schritt 1: `[ANKER-LIVE]` aus Memory lesen

```
memory_user_edits(command: "view")
→ alle Zeilen mit Prefix "[ANKER-LIVE]" herausfiltern
```

### Schritt 2: Einträge klassifizieren

- Typ `offen` → TEMP-Anker ohne Task (Phase 1 Ausarbeitung)
- Typ `erstellt` → Task existiert, aber noch nicht erledigt
- Typ `erledigt` → sollte eigentlich nicht auftauchen (wird bei `tracker done` entfernt)

Alle Einträge werden in den Übergabeprompt übernommen — im neuen Chat stellt Claude sie wieder her.

### Schritt 3: Sektion "Offene Anker" in Übergabeprompt

```markdown
## Offene Anker aus Teil N

Folgende IDs wurden im Chat gesetzt und sind noch nicht abgeschlossen:

| ID | Typ | Thema |
|----|-----|-------|
| TEMP-01JS7KABCD | offen | Wetter-Modul GS-Worker (noch kein Task) |
| 86c9eupfk | erstellt | tracker-Skill Anker-Logik (BPM-XXX) |

Claude im neuen Chat: Diese Einträge in `[ANKER-LIVE]` übernehmen via
`memory_user_edits` (add pro Zeile).
```

### Schritt 4: Nach Prompt-Erstellung — Memory leeren

Alle `[ANKER-LIVE]`-Einträge des alten Chats aus Memory entfernen:

```
memory_user_edits(command: "remove", line_number: <N>)
```

Pro Eintrag einen Remove-Call. Die Daten reisen per Übergabeprompt — nicht per Memory — in den neuen Chat.

### Keine Anker vorhanden?

Sektion komplett weglassen. Nicht als leere Tabelle in den Prompt schreiben.

---

## PROMPT-STRUKTUR

```
# [Projektname] Teil [N+1]

Weiterführung aus **[Projektname] Teil [N]**.

---

## Aktueller Stand
- **App-Version:** [Version]
- **Letzter Commit:** [Hash + Message]
- **Branch:** [Branch]
- **Chat-URL Teil [N]:** [aktuelle Chat-URL falls bekannt]

## Erledigt in Teil [N]
- [Erledigte Punkte/Commits]

## Offene Punkte (aus ClickUp + Chat)

### ClickUp offen (nach Liste gruppiert):
PlanManager:
- [Priority] [Meilenstein] BPM-NNN | Beschreibung
Docs:
- [Priority] [Meilenstein] BPM-NNN | Beschreibung
(nur Listen mit offenen Tasks auflisten)

### Offene Anker aus Teil [N] (aus [ANKER-LIVE]):
| ID | Typ | Thema |
|----|-----|-------|
| TEMP-xxx | offen | Thema (noch kein Task) |
| 86c9xxx | erstellt | Thema (BPM-NNN) |
(nur wenn Einträge vorhanden — sonst Sektion weglassen)

### Im Chat neu erkannt (noch nicht in ClickUp):
- Modul — Beschreibung

### Im Chat erledigt (noch nicht in ClickUp markiert):
- BPM-NNN | Beschreibung

### Sonstige offene Punkte (nicht in ClickUp):
- [Pending Commits]
- [Pending Doc-Updates]
- [Pending Frontmatter/Quickload-Updates]
- [Neue Fachliche Invarianten die noch eingetragen werden müssen]

## Nächste Schritte (geplant)
- [Prioritäten — basierend auf V1 + high/urgent zuerst]

## Aktive Entscheidungen
- [Architektur-Entscheidungen]
- [Offene Fragen]

## Kontext
- [Wichtige Erkenntnisse]
- [Warnungen]
- [Docs die gelesen werden sollten]
- [Docs deren Quickload/Invarianten veraltet sein könnten]

## Regeln (Erinnerung)
- User committet und pusht selbst
- Ein Schritt pro Antwort
- Nachfragen wenn Kontext fehlt → ask_user_input_v0 bei festen Optionen
- Commit-Format: [vX.Y.Z] Modul, Typ: Kurztitel
- Docs: Quickload-First-Pass → Pflichtlesen → Langform bei Bedarf
- DOC-STANDARD.md definiert Frontmatter + Kapitelvorlagen
- ClickUp Space "BPM Entwicklung" ist Source of Truth für Tasks
- tracker-Skill ist einzige Schreibschnittstelle zu ClickUp
- Task-Nummern: BPM-NNN (global fortlaufend)
```

---

## Chat-URL in Übergabe-Prompt

Die URL des aktuellen Chats (der gerade endet) wird in den Übergabe-Prompt unter `**Chat-URL Teil [N]:**` geschrieben, damit sie im nächsten Chat für Nachpflege (z.B. tracker done bei retrospektiven Tasks) verfügbar ist.

Ermittlung der aktuellen Chat-URL:

1. Wenn User die URL am Chat-Start oder während der Session gepostet hat → verwenden
2. Sonst: `recent_chats(n: 1, sort_order: "desc")` aufrufen
   - Oberster Treffer sollte dieser Chat sein (wenn indexiert)
   - Prüfen ob der Inhalt passt (Chat-Titel, letzte Nachrichten)
3. Wenn keine URL ermittelbar: Feld im Prompt leer lassen + Hinweis

**Nicht raten.** Lieber Feld leer als falsche URL.

---

## REGELN

1. Automatisch sammeln — nicht nachfragen was rein soll
2. Chat-Nummer korrekt — N+1
3. Nichts vergessen — inkl. pending Frontmatter, neue Invarianten
4. Kompakt aber vollständig
5. Kopierfähig als Markdown-Codeblock
6. Version prüfen
7. Keine Datei — direkt im Chat
8. Pending Quickload-Änderungen explizit nennen
9. **ClickUp-Abgleich VOR Übergabeprompt** — offene Tasks laden + Chat scannen
10. **Batch-Abschluss per `ask_user_input_v0`** (nicht Prosa-Liste)
11. **Keine automatischen ClickUp-Mutationen ohne ask_user_input_v0 Bestätigung**
12. **Nächste Schritte basierend auf V1 + Priority ableiten**
13. **Sonstige offene Punkte** (Pending Commits, Frontmatter, Invarianten) ZUSÄTZLICH zu ClickUp auflisten
14. **Aktuelle Chat-URL** in Übergabe-Prompt einfügen (für Nachpflege)
15. **`[ANKER-LIVE]` aus Memory in Übergabeprompt kopieren** und danach aus Memory leeren — Anker reisen per Prompt, nicht per Memory

---

## VERBOTEN

- Nachfragen was rein soll (Prosa)
- Offene Punkte vergessen
- Als Datei liefern
- Ohne Version/Chat-Nummer
- Nummern verwechseln
- Pending Frontmatter/Invarianten vergessen
- Branch automatisch annehmen ohne User-Auswahl
- **Branch-Auswahl als Prosa** — IMMER ask_user_input_v0
- **Batch-Abschluss als Prosa** — IMMER ask_user_input_v0
- **Tasks automatisch in ClickUp erstellen/schließen ohne ask_user_input_v0 Bestätigung**
- **ClickUp-Schreiboperationen direkt ausführen (→ tracker-Skill nutzen)**
- **Pending Commits/Doc-Updates/Frontmatter-Updates vergessen nur weil ClickUp da ist**
- **"ja/nein/einzeln wählen" Fragen als Text statt ask_user_input_v0**
- Chat-URLs raten oder erfinden — bei Unsicherheit Feld leer lassen
- **`[ANKER-LIVE]`-Einträge im alten Chat-Memory belassen nach Übergabe** — müssen geleert werden
- **Anker-Sektion im Prompt als leere Tabelle einfügen wenn keine Anker vorhanden** — dann Sektion komplett weglassen
