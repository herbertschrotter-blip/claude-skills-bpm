# ClickUp Custom Fields, Listen, IDs, Nummerierung

Referenz für `tracker neu`, `tracker done`, `tracker field`, `tracker split`.

---

## ClickUp-Konfiguration

Aus Memory lesen: `[CLICKUP]` Eintrag enthält Space-ID, Listen-IDs und nächste freie Nummer.

Format:
```
[CLICKUP] Space:<ID> | Listen: <Modul>:<ListID>, ... | Next:<NNN> | Letzte Sync: Teil <N>
```

---

## Custom Fields — Übersicht (10 Felder)

Space hat **10 Custom Fields**. Pflegen unterscheidet sich je Phase:

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

---

## Typ-Dropdown (Option-IDs)

| Option | Option-ID | Farbe |
|--------|-----------|-------|
| Feature | `5f4be01a-1b85-42ef-a987-b8ffb16ecdc1` | Grün |
| Fix | `00bb1941-b0a4-4eaf-96c9-116b2a57a8d6` | Rot |
| Refactor | `aa48cd2f-a319-4abf-b6ba-9bbe6f44e2c7` | Blau |
| Perf | `976b3664-5973-4922-8287-4a63101e0c2d` | Orange |
| Docs | `12a547b2-4ebc-4caa-8527-023c66e9f111` | Violett |
| Konzept | `1291a46f-feab-4596-8762-3872e51ee327` | Gelb |
| Meta | `d60891c6-129f-4b99-9e6f-043940541a22` | Grau |

## Aufwand-Dropdown (Option-IDs)

| Option | Option-ID | Farbe |
|--------|-----------|-------|
| S (<1h) | `805fd010-b820-46b1-acaa-8b2e047904e6` | Grün |
| M (1-4h) | `0298c9b6-9116-4c9e-bb74-d78a41bfe975` | Gelb |
| L (halber Tag) | `7646181a-b2ff-4eaa-a61b-0d378c0e91d3` | Orange |
| XL (>1 Tag) | `6b7587cc-2031-44c4-8b95-74a2d73c87a7` | Rot |

---

## Default bei `tracker neu`

**Pflicht ausfüllen** (wenn ermittelbar):
- Typ (aus Kontext oder ask_user_input_v0)
- Chat-Anker erstellt (ClickUp-Task-ID, wird nach `clickup_create_task` direkt gesetzt)

**Wenn vorhanden** (aus `[ANKER-LIVE]` Memory):
- Chat-Anker temp (TEMP-ID aus Ausarbeitungsphase)

**Wenn bekannt** (sonst leer lassen):
- Aufwand, Zielversion, Komponente, Zugehörige Docs

---

## Default bei `tracker done`

**Pflicht ausfüllen**:
- Commit ID + Commit Text (aus DC `git log`)
- Erledigt (Commit-Datum)
- Chat-Anker erledigt (ClickUp-Task-ID)

**Nachpflegen** (falls bei `tracker neu` nicht gesetzt):
- Typ, Zugehörige Docs, Komponente, Zielversion

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

**IMMER kleingeschrieben in API-Calls!** (`open` / `in progress` / `done`).
API ist case-sensitive. Grossgeschrieben kann Fehler werfen.

---

## Memory-Pflege

Nach jeder Änderung `[CLICKUP]` in Memory aktualisieren:
- Neue Liste-ID anhängen
- `Next:` erhöhen
- `Letzte Sync: Teil <N>` setzen
