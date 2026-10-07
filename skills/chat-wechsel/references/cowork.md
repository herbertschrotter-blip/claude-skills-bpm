# Cowork-Chat – Memory-Scan, Chat-Anker, Chat-URL

Gilt nur im Cowork-Chat. Einstieg und Reihenfolge: `SKILL.md`, Abschnitt „Ablauf im Cowork-Chat“.

## Inhalt

- Memory-Scan (PFLICHT bei Handover): Memory lesen, Rubriken, NICHT übernehmen, Eskalations-Hinweis mit
  Fragilitäten-Check, Prüfung vor Prompt-Abschluss, Sektion im Handover-Prompt
- Chat-Anker-Übergabe (nur Cowork): `[ANKER-LIVE]` lesen, klassifizieren, in den Prompt übernehmen, Memory leeren
- Chat-URL in Übergabe-Prompt (nur Cowork)

## Memory-Scan (PFLICHT bei Handover)

Schritte für den Cowork-Chat; Zweck und der Teil für Claude Code: `SKILL.md`, Abschnitt „Memory-Scan (PFLICHT bei
Handover)“.

### Schritt 1: Memory lesen (Cowork)

```
memory_user_edits(command: "view")
```

### Schritt 2: Nach 4 Rubriken filtern

Nur Einträge mit diesen Prefixen berücksichtigen:

- `[VERIFY]` — ausstehende Prüfung / Verifikation
- `[ARCH-OPEN]` — offene Architektur- oder Systementscheidung
- `[INFRA-TODO]` — kleine Infrastruktur-/Prozessaufgabe, nicht ClickUp-würdig
- `[REVIEW-PENDING]` — externe Rückmeldung oder Review-Antwort steht noch aus

### Schritt 3: NICHT übernehmen

Folgende Memory-Einträge gehören NICHT in den Handover:

- `[CLICKUP]`-Einträge (sind Projekt-Konvention, bleiben dauerhaft)
- `[SKILL-ISSUES]`-Einträge (Skill-Konvention, bleiben dauerhaft)
- `[ANKER-LIVE]`-Einträge (werden separat in Chat-Anker-Übergabe behandelt)
- Dauerhafte Konventions-Einträge ohne Rubrik-Prefix

### Schritt 4: Eskalations-Hinweis

Für jeden `[VERIFY]`- oder `[INFRA-TODO]`-Eintrag prüfen:

- Ist der Eintrag in 3 aufeinanderfolgenden Handovern aufgetaucht?
- Wenn ja: im Handover-Prompt kennzeichnen mit:
  > "Dieser Punkt war jetzt in 3 Übergaben offen. Prüfen, ob ClickUp-Task sinnvoll ist."

**Zusätzlich Fragilitäten-Check** (siehe
[docs/fragilitaeten-und-fruehwarn.md](../../../docs/fragilitaeten-und-fruehwarn.md)):

Vier Fragilitäten mit dokumentierten Indikatoren werden gegen den
Chat-Verlauf geprüft. Bei Treffern wird eine Eskalationsempfehlung in den
Übergabeprompt aufgenommen:

| Fragilität | Hauptsignal |
|---|---|
| 1. cc-steuerung-Pfad-/Modalitätsfragilität | Codeblöcke statt Dateioperation, hartkodierte Pfade, `$`-Variablen |
| 2. Tracker-Anker / Task-Scope-Disziplin | Fehlender `[<PRÄFIX>-ANCHOR-…]`, `tracker done` ohne Hash, Multi-Task-Commit |
| 3. Memory-Schatten-Backlog | 5+ offene `[VERIFY]`/`[INFRA-TODO]`, 3-Handovers-Wiederkehr |
| 4. Frühphasen-Verstoss | Migration-/Legacy-Vorschläge, Backward-Compat-Logik ohne Auftrag |

Volldoku inklusive Sofortmaßnahmen und Beispielen:
[docs/fragilitaeten-und-fruehwarn.md](../../../docs/fragilitaeten-und-fruehwarn.md).

### Schritt 5: Vor Prompt-Abschluss prüfen

Vor dem Finalisieren des Prompts:

1. Einträge durchgehen: Wurde in diesem Chat einer erledigt?
2. Wenn ja: Herbert fragen (per Auswahlfrage):
   > "Folgende Memory-Punkte wurden in diesem Chat bearbeitet. Entfernen?"
3. Bei Bestätigung: `memory_user_edits(command: "remove")` pro Eintrag
4. **Nie stillschweigend entfernen**

### Schritt 6: Sektion in Handover-Prompt erzeugen

Gemeinsamer Block (NICHT pro Rubrik eigener H2-Block):

```markdown
## Offene Punkte aus Memory

### VERIFY
- [Eintragstext]

### ARCH-OPEN
- [Eintragstext]

### INFRA-TODO
- [Eintragstext]

### REVIEW-PENDING
- [Eintragstext]
```

**Leere Rubriken weglassen** — nicht als leere H3-Header einfügen.

Wenn KEINE Rubrik Einträge hat: komplette Sektion `## Offene Punkte aus Memory` weglassen.

---

## Chat-Anker-Übergabe (nur Cowork)

**Zweck:** Die Live-Registry `[ANKER-LIVE]` (aus dem Chat-Anker-System, siehe tracker-Skill) muss beim Chat-Wechsel in den neuen Chat transportiert werden, weil Memory pro Session gilt. Anker-Präfix = Projekt-Präfix (Tracker-Config). In Claude Code gibt es keine Anker-Registry – Abschnitt entfällt.

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
| 86c9eupfk | erstellt | tracker-Skill Anker-Logik (<PRÄFIX>-NNN) |

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

## Chat-URL in Übergabe-Prompt (nur Cowork)

Die URL des aktuellen Chats (der gerade endet) wird in den Übergabe-Prompt unter `**Chat-URL Teil [N]:**` geschrieben, damit sie im nächsten Chat für Nachpflege (z.B. tracker done bei retrospektiven Tasks) verfügbar ist.

Ermittlung der aktuellen Chat-URL:

1. Wenn User die URL am Chat-Start oder während der Session gepostet hat → verwenden
2. Sonst: `recent_chats(n: 1, sort_order: "desc")` aufrufen
   - Oberster Treffer sollte dieser Chat sein (wenn indexiert)
   - Prüfen ob der Inhalt passt (Chat-Titel, letzte Nachrichten)
3. Wenn keine URL ermittelbar: Feld im Prompt leer lassen + Hinweis

**Nicht raten.** Lieber Feld leer als falsche URL.
