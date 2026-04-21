---
name: tracker
description: >
  Führt konkrete ClickUp-Aktionen für BPM-Tasks aus, z.B. "tracker neu",
  "tracker done", "tracker update", "tracker status", "tracker suche",
  "tracker next", "tracker split", "tracker relate" und "tracker field".
  Use when users want an explicit BPM task action in ClickUp. Do not trigger
  for general talk about priorities, open points, brainstorming, notes, or
  free-form project planning without a concrete tracker command.
---

# Tracker Skill — ClickUp Offene-Punkte-Verwaltung

## Zweck

Einzige standardisierte Schreibschnittstelle für den ClickUp-Task-Tracker.
Pro Modul eine eigene Liste. Neue Module bekommen automatisch eine neue Liste.
Globale Nummerierung BPM-001, BPM-002, ... über alle Listen hinweg.

---

## 🚨 VERBINDLICHE REGEL: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0`
verwendet werden — KEINE Prosa-Fragen.**

### Diese Fragen IMMER mit ask_user_input_v0:

| Situation | Optionen |
|-----------|----------|
| `tracker neu`: Modul unbekannt | PlanManager, Settings, Infrastructure, Docs, Anderes |
| `tracker neu`: Meilenstein unbekannt | v1, v1-nice, post-v1, backlog |
| `tracker neu`: Priorität unbekannt | urgent, high, normal, low |
| `tracker neu`: Typ unbekannt | Feature, Fix, Refactor, Perf, Docs, Konzept, Meta |
| `tracker neu`: Aufwand unbekannt | S (<1h), M (1-4h), L (halber Tag), XL (>1 Tag), Später |
| `tracker done`: Mehrere Commit-Kandidaten | Hash + Message jedes Kandidaten |
| `tracker split`: Wie viele Unteraufgaben? | 2-3, 4-5, 6+, Anders |
| `tracker split`: Mockup-Aufteilung | 1 Mockup-Task, 2 Mockup-Tasks, Je eigene, Nach Art |
| `tracker relate`: Beziehungstyp | blocks, is blocked by, relates to, duplicates |
| Task-Struktur: Variante A oder B | "Variante A: ...", "Variante B: ..." |
| Tag/Status wegen Obsoleszenz | Löschen, Archivieren, Tag "obsolet", Behalten |
| Hauptaufgabe auch schliessen? | Ja, Nein |
| Aehnlicher Task gefunden (Dedup) | Trotzdem neu, Bestehenden nutzen, Abbrechen |
| Commit-Info nicht ermittelbar | Manuell eingeben, Feld leer lassen, Abbrechen |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen  
  (Beispiel: "Welche Datei ist betroffen?", "Welche Zielversion?")
- User hat gerade eine klare Präferenz signalisiert und braucht nur Bestätigung
- Es ist keine echte Entscheidung, sondern Erklärung/Kontext

### Wie ask_user_input_v0 aussieht

```
ask_user_input_v0(
  questions: [
    {
      question: "Welcher Meilenstein für BPM-XXX?",
      options: ["v1", "v1-nice", "post-v1", "backlog"]
    }
  ]
)
```

Mehrere Fragen in einem Aufruf sind erlaubt (max 3). Zu lange Options-Listen
(>4) in Multi-Aufrufe aufteilen.

### VERBOTEN

- "Welche Variante willst du? A oder B?" als Prosa
- "Soll ich X oder Y machen?" als Prosa
- "Wie viele Unteraufgaben?" als Prosa
- Eine Liste von Optionen im Chat aufzählen und dann auf Tipp-Antwort warten

---

## ClickUp-Konfiguration

Aus Memory lesen: `[CLICKUP]` Eintrag enthält Space-ID, Listen-IDs und nächste freie Nummer.

Format:
```
[CLICKUP] Space:<ID> | Listen: <Modul>:<ListID>, ... | Next:<NNN> | Letzte Sync: Teil <N>
```

---

## Custom Fields (Pflicht bei `tracker neu` und `tracker done`)

Space hat **10 Custom Fields**. Pflegen unterscheidet sich je Phase:

### Felder (Übersicht)

| Feld | ID | Typ | Phase | Inhalt |
|------|----|----|----|--------|
| **Typ** | `f7b8c62a-0783-4b6d-9a95-0ce861eae2ad` | drop_down | neu | Feature/Fix/Refactor/Perf/Docs/Konzept/Meta |
| **Aufwand** | `ecc194e5-2c67-46a7-b4d1-177ce3512c10` | drop_down | neu | S/M/L/XL |
| **Zielversion** | `1fcc0b5a-082c-4c2a-8238-f7ff31b560d4` | short_text | neu | z.B. "v0.26.0" |
| **Komponente** | `b0f37cca-c325-4ac6-9bb8-407c65e4611a` | short_text | neu | Hauptmodul/Datei |
| **Zugehörige Docs** | `421cf05a-d02a-40b9-aca7-1dc086536f36` | text | neu | Doc-Pfade, mehrzeilig |
| **Commit ID** | `a851a04d-f34a-429f-abce-bec0b0b6859f` | short_text | done | 7-char Hash |
| **Commit Text** | `cae9f6cb-e0eb-44aa-81f8-df2e1194111e` | text | done | Erste Zeile Commit-Message |
| **Erledigt** | `457bde4f-c9c1-40ab-b464-897b7f87e6bc` | date | done | YYYY-MM-DD |
| **Chat-Anker temp** | `fef35671-3752-4bf2-bcb8-f29482d3a2d7` | short_text | neu (Phase 1) | TEMP-ID aus Ausarbeitungsphase (optional) |
| **Chat-Anker erstellt** | `512b8920-e958-4e43-826e-110e3bccdfc2` | short_text | neu | ClickUp-Task-ID beim Anlegen |
| **Chat-Anker erledigt** | `0c72a2ea-630e-4320-9cdb-80a19bc5ebb6` | short_text | done | ClickUp-Task-ID beim Abschluss |

### Typ-Dropdown (Option-IDs)

| Option | Option-ID | Farbe |
|--------|-----------|-------|
| Feature | `5f4be01a-1b85-42ef-a987-b8ffb16ecdc1` | Grün |
| Fix | `00bb1941-b0a4-4eaf-96c9-116b2a57a8d6` | Rot |
| Refactor | `aa48cd2f-a319-4abf-b6ba-9bbe6f44e2c7` | Blau |
| Perf | `976b3664-5973-4922-8287-4a63101e0c2d` | Orange |
| Docs | `12a547b2-4ebc-4caa-8527-023c66e9f111` | Violett |
| Konzept | `1291a46f-feab-4596-8762-3872e51ee327` | Gelb |
| Meta | `d60891c6-129f-4b99-9e6f-043940541a22` | Grau |

### Aufwand-Dropdown (Option-IDs)

| Option | Option-ID | Farbe |
|--------|-----------|-------|
| S (<1h) | `805fd010-b820-46b1-acaa-8b2e047904e6` | Grün |
| M (1-4h) | `0298c9b6-9116-4c9e-bb74-d78a41bfe975` | Gelb |
| L (halber Tag) | `7646181a-b2ff-4eaa-a61b-0d378c0e91d3` | Orange |
| XL (>1 Tag) | `6b7587cc-2031-44c4-8b95-74a2d73c87a7` | Rot |

### Default bei `tracker neu`

**Pflicht ausfüllen** (wenn ermittelbar):
- Typ (aus Kontext oder ask_user_input_v0)
- Chat-Anker erstellt (ClickUp-Task-ID, wird nach `clickup_create_task` direkt gesetzt)

**Wenn vorhanden** (aus `[ANKER-LIVE]` Memory):
- Chat-Anker temp (TEMP-ID aus Ausarbeitungsphase)

**Wenn bekannt** (sonst leer lassen):
- Aufwand, Zielversion, Komponente, Zugehörige Docs

### Default bei `tracker done`

**Pflicht ausfüllen**:
- Commit ID + Commit Text (aus DC `git log`)
- Erledigt (Commit-Datum)
- Chat-Anker erledigt (ClickUp-Task-ID)

**Nachpflegen** (falls bei `tracker neu` nicht gesetzt):
- Typ, Zugehörige Docs, Komponente, Zielversion

---

## Chat-Anker-System

**Zweck:** Präzise Rückverfolgung welcher Chat welchen Task ausgelöst/abgeschlossen hat — per `conversation_search` auf eindeutige Anker-Strings. Löst die Chat-URL-Problematik (URL nicht programmatisch auslesbar, Indexierungs-Verzögerung).

**Konzept-Doc:** `docs/chat-anker-konzept.md` im Skill-Repo.

### Anker-Format im Chat-Body

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

### Memory-Registry `[ANKER-LIVE]`

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

### Lifecycle

| Event | Aktion auf `[ANKER-LIVE]` |
|-------|---------------------------|
| `anker setzen: <text>` (Task 6.5) | Eintrag mit Typ `offen` hinzufügen |
| `tracker neu` mit vorhandenem TEMP | TEMP-Eintrag **ersetzen** durch Task-ID-Eintrag mit Typ `erstellt` |
| `tracker neu` ohne TEMP | neuer Eintrag mit Typ `erstellt` |
| `tracker done` erfolgreich | **beide Einträge** (erstellt + erledigt wenn vorhanden) entfernen |
| `chat-wechsel` (Task 6.3) | komplette Liste in Übergabeprompt kopieren, dann leeren |

### TEMP-ID Generierung

**Format:** `TEMP-<10 Zeichen Crockford-Base32>`

**Via DC PowerShell:**
```powershell
$ts = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$rand = Get-Random -Maximum 1024
"TEMP-" + ("{0:x}{1:x}" -f $ts, $rand).ToUpper().Substring(0, 10)
```

**Fallback (Claude selbst):** Base32-Hash aus `yyMMddHHmm` + Zufallsbuchstaben. Reicht für Session-Eindeutigkeit.

---

## Modul-Kürzel (verbindlich)

| Modul | Kürzel | Liste-ID |
|-------|--------|----------|
| PlanManager | PM | 901522848097 |
| Docs | DOC | 901522848102 |
| Konzept | KON | 901522848103 |
| Infrastructure | INF | 901522848104 |
| Refactoring | REF | 901522848105 |
| Settings | SET | 901522849234 |
| Dashboard | DASH | 901522850042 |
| Bautagebuch | BTB | 901522850044 |
| Foto | FOTO | 901522850057 |
| Zeiterfassung | ZEIT | 901522850060 |
| KI-Assistent | KI | 901522850064 |
| Outlook | OL | 901522850068 |
| Vorlagen | VORL | 901522850070 |
| Plankopf | PK | 901522850071 |
| GIS | GIS | 901522850073 |
| Wetter | WET | 901522850074 |
| Mobile | MOB | 901522850075 |
| App | APP | (Auto-Create) |
| Domain | DOM | (Auto-Create) |
| Theme | THM | (Auto-Create) |

Bei Abweichung: Memory `[CLICKUP]` ist Quelle.

### Auto-Create für neue Module

1. "Liste '<Modul>' wird erstellt."
2. `clickup_create_list(name: "<Modul>", space_id: "<Space-ID>")`
3. Memory aktualisieren
4. Kürzel-Tabelle im Skill manuell ergänzen (nächste Version)

---

## Globale Nummerierung

`BPM-<NNN>` — global über alle Listen, nie wiederverwendet.
Nächste freie Nummer im Memory: `Next:<NNN>`.
Nach jedem `tracker neu`: Next +1.

### Unteraufgaben-Nummerierung

**Unteraufgaben bekommen KEINE eigene BPM-Nummer**, aber eine **Positionsnummer** im Titel.

Format: `<Parent-NNN>.<Sub-NN> — <Kurzbeschreibung>`

Beispiele:
- `016.01 — GetPendingImports() Detail-Infos`
- `016.02 — Recovery-Entscheidungsmatrix`
- `079.01 — Mockup 1/2 Tab-Navigation Design`

**Regeln:**
- Sub-NN fortlaufend 01, 02, 03... pro Parent (2-stellig mit führender Null)
- Bei 100+ Unteraufgaben (unwahrscheinlich): 3-stellig (.001, .002)
- Parent-NNN wird mit führenden Nullen auf 3-stellig gepaddet (007, 016, 079)
- Bei Löschen einer Unteraufgabe: Nummer NICHT nachnummerieren (Lücke bleibt)
- Bei Nachtrag: nächste freie Sub-Nummer verwenden

---

## Titel-Format

### Hauptaufgaben
```
BPM-<NNN> | <KÜRZEL> | <Kurzbeschreibung>
```

Beispiel: `BPM-016 | PM | Recovery nach Crash`

### Unteraufgaben
```
<Parent-NNN>.<Sub-NN> — <Kurzbeschreibung>
```

Beispiel: `016.01 — GetPendingImports() Detail-Infos`

Kein BPM-Prefix, kein Kürzel. Zuordnung über Parent-Task + Nummerierung.

---

## Meilensteine (fix, als ClickUp-Tags)

| Tag | Bedeutung |
|-----|-----------|
| `v1` | Muss für PlanManager V1 fertig sein |
| `v1-nice` | Wäre gut für V1, blockiert aber nicht |
| `post-v1` | Nach V1 Release |
| `server` | Erst wenn Server-Modus gebaut wird |
| `backlog` | Irgendwann, kein Zeitdruck |

Tags kleingeschrieben in ClickUp. Nur an Hauptaufgaben, nicht an Unteraufgaben.

---

## Unteraufgaben

### Wann Unteraufgaben erstellen?

| Situation | Unteraufgaben? |
|-----------|---------------|
| Task ist in 1 Chat erledigt | Nein |
| Task hat 3+ klar trennbare Schritte | Ja |
| Task läuft über 3+ Chats | Ja |
| Modul-Platzhalter ("Dashboard implementieren") | Ja, wenn Modul gestartet wird |

### Wann KEINE Unteraufgaben?

- Task ist trivial (1-2 Stunden Arbeit)
- Schritte sind nicht klar trennbar
- Nur der Vollständigkeit halber

### Unteraufgaben erstellen

Via `clickup_create_task` mit `parent` Parameter:

```
clickup_create_task(
  list_id: "<gleiche Liste wie Parent>",
  name: "<Parent-NNN>.<Sub-NN> — <Beschreibung>",
  parent: "<Parent-Task-ID>",
  priority: "<von Parent erben oder eigene>",
  custom_fields: [
    {"id": "<Typ-ID>", "value": "<Typ-Option-ID>"},
    // Aufwand/Komponente je nach Bedarf
  ]
)
```

Custom Fields bei Unteraufgaben sind optional, aber Typ + Aufwand werden
empfohlen wenn bekannt.

### Hauptaufgabe automatisch Done?

Wenn alle Unteraufgaben Done → mit `ask_user_input_v0` fragen:
"Alle Unteraufgaben von BPM-XXX erledigt. Hauptaufgabe auch schließen?"
Optionen: Ja / Nein

NICHT automatisch schließen.

---

## Relationships (ClickUp-Dependencies)

Task-Beziehungen werden über ClickUp's eigene **Dependency-Funktion** gepflegt,
NICHT als Custom Field oder Freitext in der Description.

### Beziehungstypen

| Typ | Bedeutung | In ClickUp |
|-----|-----------|------------|
| **blocks** | Task A muss fertig sein bevor Task B starten kann | "blocking" |
| **is blocked by** | Umkehrung von blocks | "waiting on" |
| **relates to** | Lose inhaltliche Verbindung | "linked task" |
| **duplicates** | A ist Duplikat von B | "duplicate" |

### Einsatz

- BPM-007 `blocks` BPM-XX → BPM-XX kann nicht beginnen
- BPM-079 `is blocked by` BPM-079.01 → Mockup muss vor Umsetzung fertig sein
- BPM-004 `relates to` BPM-005 → Thematisch verwandt
- BPM-050 `duplicates` BPM-048 → BPM-050 zum Schließen

### API-Aufruf

Per `clickup_add_task_dependency`:
```
clickup_add_task_dependency(
  task_id: "<Task A>",
  depends_on: "<Task B>"  // Task A is_blocked_by Task B
  // oder
  dependency_of: "<Task B>"  // Task A blocks Task B
)
```

### Kommando

`tracker relate: BPM-X blocks BPM-Y`
`tracker relate: BPM-X relates BPM-Y`

Bei unklarer Richtung: `ask_user_input_v0` mit den 4 Beziehungstypen.

---

## Notizen vs. Tasks

| Trigger | Aktion |
|---------|--------|
| "neue aufgabe", "neuer punkt", "tracker neu" | → Task in ClickUp |
| "merk dir", "remember" | → Memory (KEIN ClickUp) |
| "notiz", "nicht vergessen" | → `ask_user_input_v0`: Task, Notiz, Beides |

---

## Description-Template (Default bei tracker neu)

Neue Tasks bekommen automatisch dieses Markdown-Template als Description:

```markdown
## Problem
<Was ist kaputt / was fehlt / was muss besser werden?>

## Lösungsansatz
<Wie lösen wir das konkret? Falls noch unklar: "Offen">

## Acceptance Criteria
- [ ] <Kriterium 1>
- [ ] <Kriterium 2>

## Definition of Done
- [ ] Code implementiert
- [ ] Manuell getestet
- [ ] Dokumentation aktualisiert
- [ ] Commit gemacht

## Abhängigkeiten / Related
<Falls ClickUp-Dependencies gesetzt: hier noch mal Freitext-Notizen>
<Oder Verweise auf Docs: Docs/Kern/DB-SCHEMA.md>

## Technische Notizen
<Beliebige weitere Infos, Code-Snippets, Links, Hintergrund>
```

**Regeln:**
- Für **Meta-Tasks** (ClickUp-Pflege, Skill-Updates) das Template **verkürzen**:
  nur Problem + Lösungsansatz
- Für **Mockup-Tasks**: AC ersetzen durch konkrete Screen-Bereiche
- Für **Konzept-Tasks**: DoD nur "Konzept-Doc geschrieben + in INDEX verlinkt"
- Template auch bei `tracker done` prüfen: DoD-Checkliste abhaken

### Bei Unteraufgaben

Unteraufgaben bekommen ein **verkürztes Template**:

```markdown
## Aufgabe
<Was genau in diesem Schritt?>

## Definition of Done
- [ ] <konkret>
```

Kein Problem/Lösungsansatz (das steht im Parent).

---

## Kommandos

### `tracker neu: <Beschreibung>`

#### Schnellmodus
"neue aufgabe: PM — Index-Erkennung spinnt, v1, high, Fix, M"
→ Direkt anlegen.

#### Fragemodus (Infos fehlen)
Per `ask_user_input_v0` (nicht Prosa!):
```
Frage 1 — Modul: PlanManager, Settings, Infrastructure, Docs, Anderes
Frage 2 — Meilenstein: v1, v1-nice, post-v1, backlog
Frage 3 — Priorität: urgent, high, normal, low
```

Nach Basics fragen per `ask_user_input_v0`:
```
Frage 1 — Typ: Feature, Fix, Refactor, Perf, Docs, Konzept, Meta
Frage 2 — Aufwand: S (<1h), M (1-4h), L (halber Tag), XL (>1 Tag), Später
Frage 3 — Zielversion?: Aktuelle (v0.25.x), Nächste Minor, v1.0, Später
```

Offensichtliches aus Kontext überspringen. Max 3 Fragen pro Aufruf.

**Prosa-Fragen für Freitext:**
- "Welche Komponente/Datei ist betroffen?" (falls Code-Bezug)
- "Welche Docs sind relevant?" (falls Doc-Bezug)

#### Ablauf
1. BPM-<Next> aus Memory
2. Kürzel + Liste-ID aus Tabelle
3. Dedup: `clickup_search` → wenn Treffer, mit `ask_user_input_v0` fragen: Trotzdem neu, Bestehenden nutzen, Abbrechen
4. **Description**: Template aus Kapitel "Description-Template" generieren
5. **TEMP-Anker aus `[ANKER-LIVE]` prüfen** (siehe Kapitel "Chat-Anker-System"):
   - `[ANKER-LIVE]` aus Memory lesen
   - Gibt es einen Eintrag mit Typ `offen` zum Thema dieses Tasks? → TEMP-ID merken
   - Sonst: kein TEMP (Phase 2 ohne vorherige Phase 1)
6. `clickup_create_task(list_id, name, priority, tags, markdown_description)` → Task-ID erhalten
7. **Anker-Text in Chat schreiben** (direkt nach `clickup_create_task`):
   ```
   [BPM-ANCHOR-<task-id>] — erstellt: <kurzbeschreibung> (war TEMP-<id>)
   ```
   (Brücke `(war TEMP-...)` nur wenn TEMP existierte)
8. **Custom Fields nachträglich setzen** via `clickup_update_task`:
   ```
   custom_fields = [
     {"id": "<Typ-ID>", "value": "<Typ-Option-ID>"},
     {"id": "<Aufwand-ID>", "value": "<Aufwand-Option-ID>"},
     {"id": "<Zielversion-ID>", "value": "v0.26.0"},
     {"id": "<Komponente-ID>", "value": "DocumentTypeRecognizer.cs"},
     {"id": "<Zugehörige Docs-ID>", "value": "Docs/Kern/DB-SCHEMA.md"},
     {"id": "512b8920-e958-4e43-826e-110e3bccdfc2", "value": "<task-id>"},
     // Falls TEMP existierte:
     {"id": "fef35671-3752-4bf2-bcb8-f29482d3a2d7", "value": "TEMP-<id>"}
   ]
   ```
9. **Memory `[ANKER-LIVE]` aktualisieren**:
   - Falls TEMP existierte: Eintrag **ersetzen** (TEMP-... → Task-ID-Eintrag mit Typ `erstellt`)
   - Sonst: neuen Eintrag hinzufügen mit Typ `erstellt`
10. Memory: Next +1
11. Bestätigung an User inkl. Task-ID als Anker-Referenz

---

### `tracker done: <Stichwort oder BPM-NNN>`

#### Ablauf

1. **Task finden** via `clickup_search` (falls BPM-NNN nicht explizit)
2. **Mehrere Treffer** → mit `ask_user_input_v0` User wählen lassen
3. **Commit-Infos ermitteln** (Pflicht):
   - Wenn Task Code-Bezug hat (SET/PM/INF/APP/DOM/THM):
     - Claude fragt User: "Welche Datei(en) sind betroffen?" (Prosa, offene Frage!)
     - Per DC: `git log -1 --format="%h|%ad|%s" --date=short -- <Datei>`
     - Oder: `git log --all --diff-filter=A --format="%h %ad %s" --date=short -- <Datei>` (erste Erwähnung)
     - Oder: `git log --grep="vX.Y.Z" --format="%h %ad %s" --date=short` (Version bekannt)
   - Wenn Task reiner Doc-Bezug (DOC/KON):
     - Gleicher Weg, aber auf Docs/ Pfade
   - Wenn Task keinen Code-Bezug hat (z.B. Meta-Task):
     - Commit ID + Commit Text leer lassen
     - Erledigt-Datum = heute (YYYY-MM-DD)
4. **Bei mehreren Commits:** `ask_user_input_v0` mit allen Kandidaten (Hash + erste Zeile)
5. **Anker-Text in Chat schreiben** (direkt vor `clickup_update_task`):
   ```
   [BPM-ANCHOR-<task-id>] — erledigt: Commit <hash> <kurzbeschreibung>
   ```
6. **Nachpflege-Felder prüfen** (falls bei `tracker neu` nicht gesetzt):
   - Typ, Aufwand, Zielversion, Komponente, Zugehörige Docs
   - Falls alle leer: `ask_user_input_v0` mit fehlenden Feldern
7. **Custom Fields vorbereiten**:
   ```
   custom_fields = [
     {"id": "a851a04d-f34a-429f-abce-bec0b0b6859f", "value": "<7-char-hash>"},
     {"id": "cae9f6cb-e0eb-44aa-81f8-df2e1194111e", "value": "<erste Zeile der Commit-Message>"},
     {"id": "457bde4f-c9c1-40ab-b464-897b7f87e6bc", "value": "<YYYY-MM-DD>"},
     {"id": "0c72a2ea-630e-4320-9cdb-80a19bc5ebb6", "value": "<task-id>"},
     // + Nachpflege-Felder falls gesetzt
   ]
   ```
8. **Einziger API-Call**:
   ```
   clickup_update_task(
     task_id: "<TaskID>",
     status: "done",     ← KLEINGESCHRIEBEN (case-sensitive)
     custom_fields: custom_fields
   )
   ```
9. **Memory `[ANKER-LIVE]` aufräumen**:
   - Eintrag mit Task-ID und Typ `erstellt` entfernen
   - Falls temporär ein Typ `erledigt` gesetzt wurde: auch entfernen
   - Nach diesem Schritt existiert im Memory nichts mehr zu diesem Task
10. **Bestätigung** an User:
    ```
    ✅ BPM-XXX auf Done gesetzt
       Commit: <hash> — <Erste Zeile der Message>
       Erledigt: <YYYY-MM-DD>
       Anker: [BPM-ANCHOR-<task-id>] (erstellt + erledigt)
    ```

#### Status-Werte IMMER kleingeschrieben

- `open` (nicht Open)
- `in progress` (nicht In Progress)
- `done` (nicht Done)

API ist case-sensitive. Grossgeschrieben kann Fehler werfen.

#### DC nicht verfügbar?

1. User nach Commit-Hash fragen (Prosa, offene Frage)
2. User nach Commit-Message fragen (Prosa)
3. Erledigt-Datum = heute
4. Chat-URLs: aktueller Chat als Fallback für beide Felder

#### Keine Commit-Info ermittelbar?

Per `ask_user_input_v0`: Manuell eingeben, Feld leer lassen, Abbrechen.

---

### `tracker split: <BPM-NNN>`

Hauptaufgabe in Unteraufgaben aufteilen.

1. Task laden: `clickup_get_task(task_id, subtasks: true)`
2. Claude analysiert den Task und schlägt Unteraufgaben vor
3. Per `ask_user_input_v0` bestätigen lassen:
   - "Diese X Unteraufgaben anlegen?" → Ja / Anders aufteilen / Abbrechen
4. Wenn "Anders aufteilen": weitere `ask_user_input_v0` Fragen zur Struktur
5. **Bestehende Sub-Nummern ermitteln** (Lücken beachten)
6. Pro Unteraufgabe:
   ```
   clickup_create_task(
     parent: "<task_id>",
     name: "<Parent-NNN>.<Sub-NN> — <Beschreibung>",
     markdown_description: "<verkürztes Template>",
     custom_fields: [Typ + ggf. Aufwand]
   )
   ```
7. Hauptaufgabe auf "in progress" setzen

---

### `tracker relate: <BPM-A> <Beziehung> <BPM-B>`

Task-Beziehung setzen.

1. Beide Tasks laden via `clickup_search` oder direkte ID
2. Beziehungstyp prüfen:
   - Wenn unklar: `ask_user_input_v0` mit blocks/is blocked by/relates to/duplicates
3. `clickup_add_task_dependency` aufrufen mit korrekter Richtung
4. Bestätigung: "✅ BPM-A blocks BPM-B"

---

### `tracker field: <BPM-NNN> <Feld> <Wert>`

Einzelnes Custom Field gezielt updaten ohne Task sonst anzupacken.

Beispiele:
- `tracker field: BPM-007 Zielversion v0.26.0`
- `tracker field: BPM-016 Aufwand L`
- `tracker field: BPM-079 Komponente SettingsView.xaml`

Bei Dropdown-Feldern (Typ, Aufwand): Option-ID aus dem Skill-Kapitel nehmen.

---

### `anker setzen: <text>`

**Zweck:** Manueller TEMP-Anker in der Phase 1 des Chat-Anker-Systems. Nutze dieses Kommando wenn die Auto-Keyword-Erkennung im `code-erstellen`-Skill nicht greift aber der User eine Stelle im Chat für späteres Wiederfinden markieren will.

Abgrenzung:
- **Auto-Anker** (code-erstellen): Claude setzt automatisch bei Task-Keywords
- **`anker setzen`** (manuell): User fordert explizit einen Anker

#### Trigger-Phrasen

- "anker setzen: <text>"
- "setze einen anker: <text>"
- "anker für <text>"
- "merk dir diese stelle: <text>"

#### Ablauf

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

#### Wann KEIN manueller Anker?

- Beschreibung unter 10 Zeichen (zu vage)
- Mehr als 10 Einträge bereits in `[ANKER-LIVE]` (erst aufräumen per `tracker neu` oder `tracker done`)
- Nahezu identischer Anker existiert bereits in `[ANKER-LIVE]` (Duplikat-Check)

Bei Duplikat: Hinweis auf bestehenden Anker statt neuen zu setzen.

#### Beispiel

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

### `tracker status`

1. `clickup_filter_tasks(space_ids, statuses: ["open", "in progress"])`
2. Gruppiert nach Liste:
```
**PlanManager** (6 offen)
- [high] [v1] [M] BPM-001 | PM | DB-Anbindung Orchestrator
  └─ (3 Unteraufgaben, 1 erledigt)
- [normal] [v1] [L] BPM-002 | PM | 5998er Statikplaene
```

Anzeige kann Typ und Aufwand als weitere Kurz-Indikatoren enthalten.

---

### `tracker next`

1. Offene Tasks laden
2. `v1` + urgent/high zuerst
3. Aufwand berücksichtigen: "heute nur S-Tasks" per User-Wunsch möglich
4. Abhängigkeiten prüfen (blocked_by!)
5. Vorschlag: "Nächster Schritt: BPM-001 | PM | ..."
6. Per `ask_user_input_v0`: "Diesen Task angehen?" → Ja / Nächsten vorschlagen / Eigener Task-Name

---

### `tracker update: <BPM-NNN> → <Änderung>`

Task aktualisieren (Priority, Meilenstein, Description, Status, Custom Fields).
Bei ambiger Änderung: `ask_user_input_v0` mit Optionen.

---

### `tracker suche: <Stichwort>`

Tasks durchsuchen mit Liste/Kürzel/Status/Priority/Tag/Typ/Aufwand.

---

### `tracker listen`

Alle Listen im Space mit Task-Anzahl.

---

## Chat-URL-Ermittlung (zentrale Hilfsmethode)

### Grundsatz

**Chat erstellt** = Chat, wo das Feature **inhaltlich ausgearbeitet** wurde (Konzept-Chat, Backlog-Aufnahme, Implementierungsplanung).

**Chat erledigt** = Chat, wo der **Code-Commit** gemacht wurde.

Beides ist NICHT zwangsläufig der Chat wo der ClickUp-Task angelegt oder geschlossen wird.

### Aktuellen Chat ermitteln

Der **gerade laufende Chat** ist meist nicht zuverlässig per `recent_chats` abrufbar (Indexierungs-Verzögerung). Strategie:

1. **Primary:** User fragt am Chat-Start einmalig (oder proaktiv):
   ```
   "Ich brauche die URL dieses Chats — kopier sie mir bitte aus der Browser-Adressleiste."
   ```
   Die URL wird für diese Session gemerkt und bei jedem tracker-Call verwendet.

2. **Secondary:** `recent_chats(n: 1, sort_order: "desc")` aufrufen — wenn der oberste Eintrag inhaltlich zum aktuellen Chat passt, verwenden. Sonst User fragen.

3. **Bei `chat-wechsel`-Skill:** Die aktuelle URL wird in den Übergabe-Prompt geschrieben, damit sie im nächsten Chat verfügbar ist.

### Chat für einen Commit finden

Gegeben: Commit-Hash + Commit-Datum/-Zeit (aus `git log`).

Ablauf:
```
1. Datum-Zeitpunkt des Commits notieren (ISO-Zeitstempel)
2. recent_chats(after: commit_time - 4h, before: commit_time + 4h, n: 10, sort_order: "asc")
3. Durch Ergebnisse gehen und prüfen ob der Chat inhaltlich zum Commit passt
   (Feature-Name, Dateinamen, Diskussionsthema im Chat-Content)
4. Besten Match auswählen
5. Bei Unsicherheit: ask_user_input_v0 mit Kandidaten als Optionen
```

### Chat wo Feature ausgearbeitet wurde

Gegeben: Feature-Name oder Task-Beschreibung.

Ablauf:
```
1. conversation_search(query: "<feature-name> <kernkonzept>", max_results: 10)
2. Sortieren nach updated_at aufsteigend (ältester zuerst)
3. Durchgehen und den Chat finden wo das Feature zum ersten Mal KONKRET geplant/ausgearbeitet wurde
   - Nicht nur erwähnt, sondern als Implementierungsschritt, ADR, Backlog-Eintrag, Konzept-Diskussion
4. Bei mehreren Kandidaten: ask_user_input_v0 mit Chat-Titeln als Optionen
```

### Fallback

Wenn der Chat nicht ermittelbar ist: `ask_user_input_v0`
Optionen: Manuell URL eingeben, Feld leer lassen, Abbrechen

---

## Chat-Start: Automatischer Kontext

Bei `[CLICKUP]` in Memory → kompakte Zusammenfassung:
```
📋 ClickUp: 12 offene V1-Tasks, 4 davon high
   Höchste Prio: BPM-001 | PM | DB-Anbindung Orchestrator [high] [v1] [M]
```

**Zusätzlich:** Proaktiv nach aktueller Chat-URL fragen (Prosa, weil offene Frage):
```
"Falls du mit tracker arbeiten willst — kopier mir bitte einmal die URL
dieses Chats aus der Adressleiste. Sonst kann ich Chat erstellt/erledigt
nicht automatisch füllen."
```

Wenn User ignoriert: Nicht nerven, aber bei erstem tracker-Call fragen.

### Stale-Check für `[ANKER-LIVE]`

Am Chat-Start (nach dem Laden des Memory) prüfen ob es veraltete Anker gibt.

**Veraltet** = älter als 24 Stunden, berechnet aus dem `<timestamp>`-Feld jedes `[ANKER-LIVE]`-Eintrags.

#### Ablauf

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

#### Keine stale Anker vorhanden?

Ausgabe unterdrücken. Kein "Alles OK"-Hinweis — der Chat-Start soll nicht überladen werden.

#### Edge Cases

- **Timestamp unparseable** → Eintrag als stale behandeln, im Hinweis markieren ("unbekanntes Alter")
- **Mehr als 10 stale Einträge** → nur die 10 ältesten anzeigen, Gesamtzahl erwähnen
- **Memory nicht lesbar** → Check überspringen (still)

---

## Priority-Regeln

| Priority | Bedeutung |
|----------|-----------|
| urgent | Blockiert nächsten Arbeitsschritt sofort |
| high | Wichtig für laufendes Ziel |
| normal | Reguläre Arbeit |
| low | Später / Cleanup |

---

## Status-Modell

| Status | Bedeutung |
|--------|-----------|
| open | Noch nicht angefangen |
| in progress | Wird bearbeitet (Mehr-Chat-Arbeit) |
| done | Erledigt und committet |

**IMMER kleingeschrieben in API-Calls!**

---

## Memory-Pflege

Nach jeder Änderung `[CLICKUP]` in Memory aktualisieren:
- Neue Liste-ID anhängen
- `Next:` erhöhen
- `Letzte Sync: Teil <N>` setzen

---

## Automationspolitik

| Situation | Verhalten |
|-----------|-----------|
| "tracker neu: ..." | Schnellmodus oder Fragemodus (ask_user_input_v0!) + Chat erstellt + Custom Fields |
| "tracker done: ..." | Commit-Info ermitteln + 10 Custom Fields + Status setzen |
| "tracker split: ..." | Vorschlag + ask_user_input_v0 zur Bestätigung + NN.NN-Nummerierung |
| "tracker relate: ..." | Dependency setzen via ClickUp API |
| "tracker field: ..." | Einzelnes Feld gezielt aktualisieren |
| "anker setzen: ..." | Manuellen TEMP-Anker setzen + Memory-Eintrag |
| code-erstellen nach Commit | NUR vorschlagen (per ask_user_input_v0) |
| chat-wechsel am Ende | Batch-Vorschlag + Chat-URL in Prompt einbetten |
| Alle Unteraufgaben done | ask_user_input_v0: Parent auch schliessen? |
| "notiz" / "nicht vergessen" | ask_user_input_v0: Task, Notiz, Beides |
| "merk dir" / "remember" | → Memory, NICHT ClickUp |

**Goldene Regel:** Explizit → direkt. Alles andere → ask_user_input_v0 (keine Prosa!).

---

## Integration mit anderen Skills

### code-erstellen
Nach Commit: `ask_user_input_v0`: "Passt zu BPM-XXX. `tracker done`?" → Ja / Nein / Anderer Task
Wenn ja → Commit-Hash direkt aus der Session (schon bekannt) + Custom Fields befüllen + aktuellen Chat als "Chat erledigt".

### chat-wechsel
Am Chat-Ende: Batch-Abschluss + Übergabe.
Schreibt die aktuelle Chat-URL in den Übergabe-Prompt, damit im nächsten Chat sofort verfügbar.

### doc-pflege
Nach Doc-Update: `ask_user_input_v0`: "Doc-Task BPM-XXX erledigt. `tracker done`?" → Ja / Nein
Gleiches 10-Fields-Schema wie bei Code-Tasks.

---

## Git-Commit-Ermittlung (Detailhilfe)

### Szenario A: Commit wurde gerade in dieser Session gemacht
Der Hash ist Claude aus dem `git commit` Output bereits bekannt → direkt verwenden.
Chat erledigt = aktueller Chat.

### Szenario B: Task ist früher erledigt worden (Nachtrag)
Per DC:
```powershell
cd "<Repo-Pfad>"
# Suche nach erster Datei-Erstellung
git log --all --diff-filter=A --format="%h|%ad|%s" --date=short -- "<Pfad/zur/Datei.cs>"

# Oder: Suche nach bestimmter Version
git log --all --format="%h|%ad|%s" --date=short --grep="vX.Y.Z"

# Oder: Suche nach Stichwort
git log --all --format="%h|%ad|%s" --date=short --grep="<Stichwort>"

# Oder: Genauer Zeitpunkt (für Chat-Matching)
git log --all --format="%h|%aI|%s" -- "<Datei>"
```
Der Pipe-Separator `|` erleichtert das Parsen: `<hash>|<datum>|<message>`.

### Szenario C: Mehrere relevante Commits
`ask_user_input_v0` mit allen Kandidaten als Optionen (Hash + erste Zeile Message).
In der Regel: Erster Commit der die Funktionalität eingeführt hat (diff-filter=A).

### Datumsformat
- DC liefert: `YYYY-MM-DD` (mit `--date=short`) oder ISO (`%aI`)
- ClickUp erwartet: `YYYY-MM-DD` (direkt)
- Für Chat-Suche: ISO-Zeitstempel mit Stunde/Minute (für recent_chats Zeitfilter)

---

## Beispiel-Workflow: tracker neu mit allen Feldern

```
User: tracker neu: PM — neue Regex-Erkennung in DocumentTypeRecognizer, v1, high

Claude intern:
  1. BPM-<Next> aus Memory: BPM-082
  2. Kürzel PM → Liste 901522848097
  3. Dedup: clickup_search "Regex DocumentTypeRecognizer" → kein Treffer
  4. ask_user_input_v0:
     Frage 1 — Typ: Feature, Fix, Refactor, Perf, Docs, Konzept, Meta
     Frage 2 — Aufwand: S, M, L, XL, Später
     User antwortet: Feature, M
  5. Prosa-Frage: "Welche Komponente?"
     User: "DocumentTypeRecognizer.cs"
  6. Prosa-Frage: "Zielversion?"
     User: "v0.26.0"
  7. Description-Template generieren
  8. Chat erstellt = aktueller Chat (URL aus Session-Memory)
  9. custom_fields = [Typ=Feature, Aufwand=M, Zielversion=v0.26.0, 
                      Komponente=DocumentTypeRecognizer.cs, Chat erstellt=<url>]
  10. clickup_create_task(...)
  11. Memory: Next 082 → 083
  12. Bestätigung: "✅ BPM-082 angelegt — PM | Neue Regex-Erkennung [v1, high, Feature, M]"
```

---

## Beispiel-Workflow: tracker done mit vollständiger Chat-Ermittlung

```
User: tracker done BPM-007

Claude intern:
  1. clickup_get_task("86c9cg8u5") → BPM-007 PlanTyp-Erkennung
  2. Prosa-Frage: "Welche Datei(en) sind betroffen?"
     User: "DocumentTypeRecognizer.cs"
  3. DC: git log --all --diff-filter=A --format="%h|%aI|%s" -- "src/.../DocumentTypeRecognizer.cs"
     → "cb46a48|2026-04-15T11:34:52+02:00|[v0.25.5] PlanManager, Feature: PatternTemplates..."
  4. Nur 1 Kandidat → direkt verwenden
  5. Chat erledigt:
     → recent_chats(after: "2026-04-15T07:34", before: "2026-04-15T15:34", n: 5, sort_order: "asc")
     → Treffer: Teil 17 (015353fe-...)
  6. Chat erstellt (nicht gesetzt):
     → conversation_search("Plantyp-Erkennung DocumentTypeRecognizer prefix contains")
     → Teil 10 (d546b50b-...) als ältester konkreter Treffer
  7. Nachpflege: Typ fehlt noch
     → ask_user_input_v0: Typ → Feature
  8. clickup_update_task(
       status: "done",
       custom_fields: [
         {id: "<Typ-ID>", value: "<Feature-Option-ID>"},
         {id: "<Commit ID-ID>", value: "cb46a48"},
         {id: "<Commit Text-ID>", value: "[v0.25.5] PlanManager, Feature: ..."},
         {id: "<Erledigt-ID>", value: "2026-04-15"},
         {id: "<Chat erstellt-ID>", value: "https://claude.ai/chat/d546b50b-..."},
         {id: "<Chat erledigt-ID>", value: "https://claude.ai/chat/015353fe-..."}
       ]
     )
  9. Bestätigung: "✅ BPM-007 Done. Commit cb46a48 (Teil 17), Ausarbeitung Teil 10, Typ Feature."
```

---

## Beispiel-Workflow: tracker split mit ask_user_input_v0

```
User: tracker split BPM-016

Claude intern:
  1. Task laden, analysieren
  2. Bestehende Sub-Nummern prüfen (z.B. schon 01-05 vergeben → neue ab 06)
  3. Struktur-Vorschlag mit N Unteraufgaben erarbeiten
  4. ask_user_input_v0:
     Frage 1: "5 neue Unteraufgaben anlegen oder anders aufteilen?"
     Optionen: "5 anlegen", "6 (mit Tests)", "3 (kompakt)", "Abbrechen"
  5. Wenn User "5 anlegen" → loslegen
  6. Pro Unteraufgabe: 
     name: "016.<NN> — <Beschreibung>"
     parent: "<task_id>"
     markdown_description: verkürztes Template
  7. Parent auf "in progress" setzen
```

---

## VERBOTEN

- Tasks automatisch erstellen aus freiem Chattext
- Tasks automatisch auf Done setzen ohne Trigger
- ClickUp-Calls in anderen Skills duplizieren
- Titel ohne BPM-Nummer oder Kürzel (Hauptaufgaben)
- BPM-Nummern an Unteraufgaben vergeben
- Unteraufgaben ohne NN.NN-Nummerierung im Titel
- Sub-Nummern nachnummerieren wenn Lücken entstehen
- Tasks ohne Dedup-Prüfung erstellen
- Meilensteine dynamisch erstellen
- Nummern wiederverwenden
- Hauptaufgabe automatisch schließen wenn Unteraufgaben done
- **`tracker done` ohne Versuch, Custom Fields zu befüllen** (mindestens Erledigt-Datum + Chat erledigt)
- **`tracker neu` ohne Chat erstellt URL** (außer User verweigert)
- **`tracker neu` ohne Typ** (außer Typ ist partout nicht ermittelbar)
- Chat-URLs raten oder erfinden — bei Unsicherheit ask_user_input_v0 oder leer lassen
- **Prosa-Fragen bei festen Entscheidungsoptionen** — IMMER ask_user_input_v0 verwenden
- Status mit Grossbuchstaben setzen (`Done`, `Open`, `In Progress`) — IMMER klein
- Relationships als Freitext statt ClickUp-Dependency nutzen
- Custom Field Option-IDs raten — immer aus dem Skill-Kapitel kopieren
- Description ohne Template bei Standard-Tasks (Meta-Tasks dürfen verkürzen)
- **Stale-Check-Ergebnis automatisch aus Memory entfernen** ohne `ask_user_input_v0` Bestätigung
- **Stale-Check bei jedem Chat-Turn wiederholen** — nur einmal beim Chat-Start ausführen
