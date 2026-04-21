# Chat-Anker-System — Konzept

**Status:** Draft v2 (Task-ID-basiert)
**Datum:** 2026-04-21
**Quelle:** Teil 23, Diskussion mit Herbert
**Betroffene Skills:** `tracker`, `chat-wechsel`, `code-erstellen`
**Betroffene Systeme:** ClickUp (3 neue Custom Fields), Memory (`[ANKER-LIVE]`)

---

## 1. Problem

Die URL-Felder `Chat erstellt` und `Chat erledigt` in ClickUp-Tasks sind aktuell schwer zuverlässig zu füllen:

- Die laufende Chat-URL ist programmatisch nicht auslesbar — User muss sie manuell einfügen
- `conversation_search` findet Themen nur fuzzy — bei mehrdeutigen Begriffen 5–10 Treffer
- Der aktuelle Chat ist in `recent_chats` meist noch nicht indexiert
- Nachträgliche Zuordnung "wo wurde X besprochen" ist mühsam

## 2. Ziel

Präzise, deterministische Rückverfolgung welche Stelle in welchem Chat zu einem Task gehört — sowohl für Claude (bei `tracker done`) als auch für Herbert (per ClickUp-Suche).

## 3. Kernidee

Claude setzt an task-würdigen Stellen im Chat-Body einen **Anker** — eine eindeutige ID mit Prefix `BPM-ANCHOR-`:

```
[BPM-ANCHOR-86c9erNEW1] — erstellt: Wetter-Modul Google-Sheets-Worker
```

Diese ID ist per `conversation_search("BPM-ANCHOR-86c9erNEW1")` exakt wiederfindbar — ein Treffer, eine URL, eine Stelle.

Als ID wird die **ClickUp-Task-ID** verwendet (z.B. `86c9erNEW1`) — sie ist ohnehin eindeutig und existiert nach Task-Erstellung.

## 4. Drei Phasen

### Phase 1 — Ausarbeitung (vor Task-Erstellung)

Wenn ein task-würdiges Thema erkannt wird, aber noch kein ClickUp-Task existiert:

```
[BPM-ANCHOR-TEMP-01JS7KABCD] — Idee: Wetter-Modul Google-Sheets-Worker
```

- **Prefix:** `TEMP-`
- **ID-Format:** 10-Zeichen-Base32-Hash (aus Timestamp + Zufall) — reicht für Session-Eindeutigkeit
- Memory wird aktualisiert (Eintrag mit Typ `offen`)

### Phase 2 — Task wird erstellt

User sagt `tracker neu: ...`. Claude-Ablauf:

1. Prüft `[ANKER-LIVE]` auf vorhandenen temp-Anker zum Thema
2. Erstellt Task in ClickUp → bekommt Task-ID (z.B. `86c9erNEW1`)
3. Schreibt neuen Anker mit Task-ID in den Chat, mit Brücke zum temp:
   ```
   [BPM-ANCHOR-86c9erNEW1] — erstellt: Wetter-Modul GS-Worker (war TEMP-01JS7KABCD)
   ```
4. Füllt Custom Fields im Task:
   - `Chat-Anker temp` = `TEMP-01JS7KABCD` (nur wenn temp existierte)
   - `Chat-Anker erstellt` = `86c9erNEW1`
5. Memory: temp-Eintrag durch Task-ID-Eintrag ersetzen

### Phase 3 — Task wird abgeschlossen

`tracker done BPM-XXX`:

1. Neuer Anker mit gleicher Task-ID, Typ `erledigt`:
   ```
   [BPM-ANCHOR-86c9erNEW1] — erledigt: Commit abc1234 Wetter-Modul
   ```
2. Custom Field `Chat-Anker erledigt` = `86c9erNEW1`
3. Memory: beide Einträge (erstellt + erledigt) entfernen

## 5. Auslöser für Anker-Erstellung

| Auslöser | Phase | Wer setzt | Typ im Memory |
|----------|-------|-----------|---------------|
| Feature-Ausarbeitung mit Task-Keywords | 1 | Skill automatisch | `offen` |
| Manuell per `anker setzen: <text>` | 1 | Skill auf Kommando | `offen` |
| `tracker neu` ausgeführt | 2 | tracker-Skill | `erstellt` |
| `tracker done` mit Commit | 3 | tracker-Skill | `erledigt` |

**Task-Keywords für automatische Phase-1-Anker:**
- "das müssen wir noch bauen"
- "später implementieren"
- "ins backlog"
- "backlog-wert"
- "da brauchen wir einen task"
- "sollten wir im task tracken"

Nicht zu aggressiv — zu viele Anker verrauschen den Chat. Bei Unsicherheit: **keinen Anker setzen**, User kann manuell.

## 6. Memory-Registry `[ANKER-LIVE]`

Damit Anker innerhalb derselben Session bereits nutzbar sind (vor Indexierung durch `conversation_search`), wird pro Chat eine Live-Registry in User-Memory geführt.

### Format

```
[ANKER-LIVE] <id>|<typ>|<timestamp>|<kurzbeschreibung>
```

- `<id>` — `TEMP-<10>` oder ClickUp-Task-ID
- `<typ>` — `offen` | `erstellt` | `erledigt`
- `<timestamp>` — ISO-Format `YYYY-MM-DDTHH:MM`
- `<kurzbeschreibung>` — max 60 Zeichen

### Beispiel während Session

```
[ANKER-LIVE] TEMP-01JS7KABCD|offen|2026-04-21T18:45|Wetter-Modul GS-Worker
[ANKER-LIVE] 86c9erNEW1|erstellt|2026-04-21T19:00|ProfileManager Service
[ANKER-LIVE] 86c9erABCD|erstellt|2026-04-21T19:30|Recovery Workflow
```

## 7. Lebenszyklus in Memory

| Event | Aktion auf `[ANKER-LIVE]` |
|-------|---------------------------|
| Phase 1: neuer temp-Anker | Eintrag hinzufügen, Typ `offen` |
| Phase 2: Task aus temp erstellt | temp-Eintrag **ersetzen** durch Task-ID-Eintrag mit Typ `erstellt` |
| Phase 2: Task ohne temp erstellt (direkter `tracker neu`) | neuer Eintrag mit Typ `erstellt` |
| Phase 3: `tracker done` erfolgreich | **beide Einträge** (erstellt + erledigt wenn vorhanden) entfernen |
| `chat-wechsel` | komplette Liste in Übergabeprompt kopieren, dann leeren |
| Neuer Chat startet | Registry beginnt leer, wird aus Übergabeprompt wieder befüllt |

### Stale-Check am Chat-Start

Claude prüft am Chat-Start ob `[ANKER-LIVE]` Einträge älter als 24h enthält → Warnung an User, Frage ob Aufräumen. Fängt vergessene Einträge nach abgebrochenen Chats ab.

## 8. Übergabe bei `chat-wechsel`

Der chat-wechsel-Skill erweitert den Übergabeprompt um folgende Sektion:

```markdown
## Offene Anker aus Teil N

Folgende IDs wurden im Chat gesetzt und sind noch nicht abgeschlossen:

| ID | Typ | Thema |
|----|-----|-------|
| TEMP-01JS7KABCD | offen | Wetter-Modul GS-Worker (noch kein Task) |
| 86c9erNEW1 | erstellt | ProfileManager Service (BPM-082) |

Claude im neuen Chat: Diese Einträge in `[ANKER-LIVE]` übernehmen.
```

Der erste Claude-Response im neuen Chat extrahiert die Tabelle und füllt Memory via `memory_user_edits`.

## 9. ClickUp Custom Fields (neu)

Drei neue Felder auf Workspace-Level:

| Feld | Typ | Bedeutung |
|------|-----|-----------|
| `Chat-Anker temp` | short_text | Temp-ID aus Ausarbeitungsphase (optional, nur wenn vorhanden) |
| `Chat-Anker erstellt` | short_text | Task-ID beim Anlegen (ist identisch mit der sichtbaren ClickUp-Task-ID, aber als eigenes Filter-/Such-Feld verfügbar) |
| `Chat-Anker erledigt` | short_text | Task-ID beim Abschluss |

**Redundanz mit Task-ID ist gewollt** — die Felder dienen als Filter-/Such-Anker in ClickUp-Views und machen die Anker-Logik symmetrisch zu den bestehenden URL-Feldern.

## 10. Integration mit bestehenden Feldern

Die URL-Felder `Chat erstellt` und `Chat erledigt` bleiben bestehen — werden aber jetzt via Anker-Rückwärtssuche gefüllt:

```
conversation_search("BPM-ANCHOR-86c9erNEW1")
→ <chat url='https://claude.ai/chat/abc-...'>
→ URL extrahieren
→ Custom Field "Chat erstellt" setzen
```

Für Live-Session (vor Indexierung): Chat-URL aus `[ANKER-LIVE]`-Kontext wenn verfügbar, sonst User-Fallback wie bisher.

## 11. Temp-ID Generierung

**Format:** `TEMP-<10 Zeichen Crockford-Base32>`

**Generierung via DC (PowerShell):**
```powershell
$ts = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$rand = [int](Get-Random -Maximum 1024)
$combined = "{0:x}{1:x}" -f $ts, $rand
# dann auf 10 Zeichen Crockford-Base32 mappen
```

**Fallback (Claude selbst):** Einfacher Base32-Hash aus `DateTimeOffset.UtcNow.ToString("yyMMddHHmm") + zufällig`. Reicht für Session-Eindeutigkeit.

Eindeutigkeit ist **pro Session** nötig, nicht global — 10 Zeichen mehr als genug.

## 12. Anti-Patterns

- **Anker rückwirkend einfügen:** Geht nicht (Edits ändern Index-Content nicht zuverlässig). Anker immer beim Auslöser setzen, nicht nachträglich.
- **Zu viele Anker:** Pro Chat realistisch 3–10. Bei 20+ wird der Chat verrauscht. Bei Unsicherheit keinen setzen.
- **Anker ohne Kurzbeschreibung:** Debug-Hölle. Kurzbeschreibung ist Pflicht.
- **Temp-ID und Task-ID im selben Chat für dasselbe Thema:** Erlaubt (Phase 1 → Phase 2). Wichtig: Die Brücke `(war TEMP-...)` im Task-ID-Anker-Text.
- **Memory-Registry nicht aufräumen:** Führt zu Drift. Stale-Check am Chat-Start abfängt.
- **Eigene ULIDs bauen für Tasks die schon existieren:** ClickUp-Task-ID ist die kanonische Referenz. Nur für Phase 1 (vor Task) nötig.

## 13. Offene Fragen / Later

- **Verhalten bei Fork:** Wenn ein Chat geforked wird — beide Forks haben dieselben Anker. Zeigt auf gleiche inhaltliche Stelle, ist also korrekt. Aber Memory-Drift möglich (welcher Fork ist "der echte"?). Für V1 ignoriert.
- **Anker für ChatGPT-Review-Prompts:** Könnte sinnvoll sein — der Review-Prompt verweist auf konkrete Anker-Stellen. Erst nach V1-Stabilisierung prüfen.
- **Historische Tasks (vor Anker-System):** 78 bestehende Tasks haben keine Anker. Migration nicht nötig — Custom Fields bleiben leer, URL-Felder bestehen wie bisher.

## 14. Implementierungs-Reihenfolge

1. 3 Custom Fields in ClickUp anlegen (Workspace-Level)
2. `tracker`-Skill erweitern: Phase 2 + 3 Anker-Logik, Memory-Pflege
3. `chat-wechsel`-Skill erweitern: Anker-Übergabe-Sektion
4. `code-erstellen`-Skill erweitern: Phase 1 Auto-Anker bei Task-Keywords
5. Neues Kommando: `anker setzen: <text>` (manuell)
6. Stale-Check am Chat-Start in allen Skill-Triggern
7. PoC-Test: im nächsten Chat prüfen ob Anker via `conversation_search` findbar

## 15. Erfolgskriterien

- Nach `tracker done` ist `Chat-Anker erstellt` und `Chat-Anker erledigt` gesetzt (in ≥ 95% der Fälle)
- Bei `tracker done` im selben Chat wo `tracker neu` war: kein User-Eingriff für Chat-URLs nötig
- Bei `tracker done` 1-2 Chats später: Anker-Suche findet den Ursprungs-Chat zuverlässig
- `[ANKER-LIVE]` bleibt konsistent — keine verwaisten Einträge nach 1 Woche
