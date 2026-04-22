# Chat-Anker-System — Master-Spec

**Zweck:** Präzise Rückverfolgung welcher Chat welchen Task ausgelöst/abgeschlossen hat — per `conversation_search` auf eindeutige Anker-Strings. Löst die Chat-URL-Problematik (URL nicht programmatisch auslesbar, Indexierungs-Verzögerung).

**Konzept-Doc:** `docs/chat-anker-konzept.md` im Skill-Repo.

**Hinweis:** Diese Datei ist die Master-Spezifikation. `code-erstellen` (Auto-Anker) und `chat-wechsel` (Übergabe) haben eigene lokale Kopien der für sie relevanten Teile. Bei Änderungen der Spec müssen dort die Kopien mit-gepflegt werden.

---

## Anker-Format im Chat-Body

```
[BPM-ANCHOR-<id>] — <typ>: <kurzbeschreibung max 80 Zeichen>
```

- `<id>` = `TEMP-<10-char-base32>` (Phase 1, vor Task-Erstellung) **oder** ClickUp-Task-ID (Phase 2/3)
- `<typ>` = `erstellt` | `erledigt`

Beispiele:
```
[BPM-ANCHOR-TEMP-01JS7KABCD] — Idee: Wetter-Modul Google-Sheets-Worker
[BPM-ANCHOR-86c9eupfk] — erstellt: tracker-Skill Anker-Logik (war TEMP-01JS7KABCD)
[BPM-ANCHOR-86c9eupfk] — erledigt: Commit abc1234 tracker Anker-Logik
```

---

## Memory-Registry `[ANKER-LIVE]`

Live-Liste aller aktiven Anker der aktuellen Session.

**Format:**
```
[ANKER-LIVE] <id>|<typ>|<timestamp>|<kurzbeschreibung>
```

- `<id>` = TEMP-ID oder Task-ID
- `<typ>` = `offen` (temp, kein Task) | `erstellt` | `erledigt`
- `<timestamp>` = ISO `YYYY-MM-DDTHH:MM`
- `<kurzbeschreibung>` = max 60 Zeichen

**Beispiel während Session:**
```
[ANKER-LIVE] TEMP-01JS7KABCD|offen|2026-04-21T18:45|Wetter-Modul GS-Worker
[ANKER-LIVE] 86c9eupfk|erstellt|2026-04-21T19:00|tracker Anker-Logik
```

---

## Lifecycle

| Event | Aktion auf `[ANKER-LIVE]` |
|-------|---------------------------|
| `anker setzen: <text>` (Task 6.5) | Eintrag mit Typ `offen` hinzufügen |
| `tracker neu` mit vorhandenem TEMP | TEMP-Eintrag **ersetzen** durch Task-ID-Eintrag mit Typ `erstellt` |
| `tracker neu` ohne TEMP | neuer Eintrag mit Typ `erstellt` |
| `tracker done` erfolgreich | **beide Einträge** (erstellt + erledigt wenn vorhanden) entfernen |
| `chat-wechsel` (Task 6.3) | komplette Liste in Übergabeprompt kopieren, dann leeren |

---

## TEMP-ID Generierung

**Format:** `TEMP-<10 Zeichen Crockford-Base32>`

**Via DC PowerShell:**
```powershell
$ts = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$rand = Get-Random -Maximum 1024
"TEMP-" + ("{0:x}{1:x}" -f $ts, $rand).ToUpper().Substring(0, 10)
```

**Fallback (Claude selbst):** Base32-Hash aus `yyMMddHHmm` + Zufallsbuchstaben. Reicht für Session-Eindeutigkeit.

---

## Kommando `anker setzen: <text>`

**Zweck:** Manueller TEMP-Anker in der Phase 1 des Chat-Anker-Systems. Nutze dieses Kommando wenn die Auto-Keyword-Erkennung im `code-erstellen`-Skill nicht greift aber der User eine Stelle im Chat für späteres Wiederfinden markieren will.

Abgrenzung:
- **Auto-Anker** (code-erstellen): Claude setzt automatisch bei Task-Keywords
- **`anker setzen`** (manuell): User fordert explizit einen Anker

### Trigger-Phrasen

- "anker setzen: <text>"
- "setze einen anker: <text>"
- "anker für <text>"
- "merk dir diese stelle: <text>"

### Ablauf

1. **TEMP-ID generieren** (siehe Kapitel "TEMP-ID Generierung"):
   - Primär via DC PowerShell
   - Fallback: Claude erzeugt `TEMP-<yyMMddHHmm><3 Zufallsbuchstaben>`
2. **Kurzbeschreibung** aus `<text>` ableiten (max 60 Zeichen, keine Zeilenumbrüche)
3. **Anker-Zeile im Chat schreiben**:
   ```
   [BPM-ANCHOR-TEMP-<id>] — Idee: <kurzbeschreibung>
   ```
4. **Memory aktualisieren**:
   ```
   memory_user_edits(
     command: "add",
     control: "[ANKER-LIVE] TEMP-<id>|offen|<ISO-timestamp>|<kurzbeschreibung>"
   )
   ```
5. **Bestätigung an User**:
   ```
   ✅ Anker gesetzt: TEMP-<id>
      Thema: <kurzbeschreibung>
      Wird bei `tracker neu` mit Task-ID verknüpft oder bei `chat-wechsel` in Übergabeprompt übernommen.
   ```

### Wann KEIN manueller Anker?

- Beschreibung unter 10 Zeichen (zu vage)
- Mehr als 10 Einträge bereits in `[ANKER-LIVE]` (erst aufräumen per `tracker neu` oder `tracker done`)
- Nahezu identischer Anker existiert bereits in `[ANKER-LIVE]` (Duplikat-Check)

Bei Duplikat: Hinweis auf bestehenden Anker statt neuen zu setzen.

### Beispiel

```
User: anker setzen: Wetter-Modul Google-Sheets Polling-Intervall diskutiert

Claude:
  1. TEMP-ID: TEMP-01JS9ABCDE
  2. [BPM-ANCHOR-TEMP-01JS9ABCDE] — Idee: Wetter-Modul GS Polling-Intervall
  3. memory_user_edits(add, "[ANKER-LIVE] TEMP-01JS9ABCDE|offen|2026-04-21T23:15|Wetter-Modul GS Polling-Intervall")
  4. ✅ Anker gesetzt: TEMP-01JS9ABCDE
     Thema: Wetter-Modul GS Polling-Intervall
     Wird bei `tracker neu` mit Task-ID verknüpft oder bei `chat-wechsel` in Übergabeprompt übernommen.
```

---

## Stale-Check (am Chat-Start)

Am Chat-Start (nach dem Laden des Memory) prüfen ob es veraltete Anker gibt.

**Veraltet** = älter als 24 Stunden, berechnet aus dem `<timestamp>`-Feld jedes `[ANKER-LIVE]`-Eintrags.

### Ablauf

1. **Alle `[ANKER-LIVE]`-Einträge parsen**: 
   - Format: `[ANKER-LIVE] <id>|<typ>|<timestamp>|<kurzbeschreibung>`
   - Timestamp ist ISO `YYYY-MM-DDTHH:MM`
2. **Aktuelle Zeit ermitteln** (ISO via `[DateTimeOffset]::UtcNow` oder Claude-intern)
3. **Differenz berechnen** — wenn älter als 24h → stale
4. **Stale-Liste anzeigen** (nur wenn ≥1 stale):
   ```
   ⚠️ Veraltete Anker in [ANKER-LIVE] (älter als 24h):

   | ID | Alter | Thema |
   |----|-------|-------|
   | TEMP-01JS7KABCD | 3 Tage | Wetter-Modul GS-Worker |
   | 86c9eupfk | 26 Std | tracker-Skill Anker-Logik |
   ```

5. **Per `ask_user_input_v0`** fragen was damit passieren soll:
   ```
   Frage: "Was mit den veralteten Ankern tun?"
   Optionen:
   - "Alle verwerfen (Memory bereinigen)"
   - "Einzeln entscheiden"
   - "Behalten (nur Hinweis)"
   ```
6. **Bei "Alle verwerfen":** Alle stale Einträge via `memory_user_edits(remove, <line>)` entfernen
7. **Bei "Einzeln entscheiden":** Pro stale Eintrag `ask_user_input_v0` mit Optionen:
   - "Verwerfen"
   - "`tracker neu` — Task daraus machen"
   - "Behalten"
8. **Bei "Behalten":** Nichts tun, nur im Chat notiert

### Keine stale Anker vorhanden?

Ausgabe unterdrücken. Kein "Alles OK"-Hinweis — der Chat-Start soll nicht überladen werden.

### Edge Cases

- **Timestamp unparseable** → Eintrag als stale behandeln, im Hinweis markieren ("unbekanntes Alter")
- **Mehr als 10 stale Einträge** → nur die 10 ältesten anzeigen, Gesamtzahl erwähnen
- **Memory nicht lesbar** → Check überspringen (still)
