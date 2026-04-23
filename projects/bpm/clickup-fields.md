# BPM — ClickUp Custom Fields, Modul-Kürzel, Meilensteine

Referenz für alle BPM-spezifischen ClickUp-Daten. Universelle
tracker-Regeln stehen in `skills/tracker/references/clickup-fields.md`
(Verweise auf diese Datei hier).

**Source of Truth:** ClickUp-Workspace direkt. Diese Datei ist Doku.

---

## Scope-Abgrenzung

Es gibt **zwei verschiedene Field-Scopes** in diesem Projekt:

| Scope | Gilt für | Anzahl Fields | Dokumentiert in |
|---|---|---|---|
| **BPM-Scope** | BPM-Listen (PM, DOC, …) + ClaudeSkills-Liste | 10 Custom Fields | Abschnitt 1 unten |
| **Skill-Issues-Scope** | Alle 11 Listen im Ordner "Skill Issues" | 6 Custom Fields | Abschnitt 2 unten |

Bei jedem `tracker`-Kommando: Scope aus Ziel-Liste ableiten
(siehe `clickup-lists.md`).

---

## 1. BPM-Scope — 10 Custom Fields

Gilt für alle 17 BPM-Listen + die ClaudeSkills-Refactor-Plan-Liste.

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
| **Chat-Anker temp** | `fef35671-3752-4bf2-bcb8-f29482d3a2d7` | short_text | neu | TEMP-ID aus Ausarbeitungsphase |
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

---

## 2. Skill-Issues-Scope — 6 Custom Fields

Gilt für alle 11 Listen im Ordner "Skill Issues" (Ordner-ID `901515724728`).

| Feld | ID | Typ | Inhalt |
|------|----|----|----|
| **Issue-ID** | `e286a04a-d79b-481a-8ee4-9c9401a87bfc` | short_text | `<skill>-NNN` (z.B. `tracker-005`) |
| **Typ** | `5b45b13a-a866-4a5a-83e2-eea2ea1128b8` | drop_down | Bug/Trigger-Fehler/Doku-Fehler/Verbesserung/Refactor-Idee |
| **Commit-Hash** | `8e8879f7-5741-4af9-9a4a-708eff59ca87` | short_text | Git-Hash nach Fix |
| **Beobachtungs-Chat** | `eb1f6eb6-8fcf-4b73-b7aa-ffd81f2db0fe` | short_text | Chat in dem Issue erkannt wurde |
| **Chat-Anker erstellt** | `512b8920-e958-4e43-826e-110e3bccdfc2` | short_text | Identisch zu BPM-Scope |
| **Chat-Anker erledigt** | `0c72a2ea-630e-4320-9cdb-80a19bc5ebb6` | short_text | Identisch zu BPM-Scope |

### Skill-Issues-Typ-Dropdown (Option-IDs)

| Option | Option-ID |
|--------|-----------|
| Bug | `2519a0e3-5ef4-4913-96b9-6a297343326d` |
| Trigger-Fehler | `9e98787e-8956-4212-86ed-789276f4aa3e` |
| Doku-Fehler | `d1116505-fd85-4283-bab8-9e657e6ea833` |
| Verbesserung | `6fcb6a19-d22e-4a36-b3f2-047523e41ad6` |
| Refactor-Idee | `3dfdb7a5-39b1-433d-b550-dc05a371de47` |

---

## 3. Modul-Kürzel (BPM-Listen)

Hauptaufgaben-Titel-Prefix und Listen-Zuordnung:

| Modul | Kürzel | Listen-ID |
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

---

## 4. BPM-Nummerierung

**Format:** `BPM-<NNN>` — 3-stellig mit führenden Nullen, global über alle
BPM-Listen, nie wiederverwendet.

**Nächste freie Nummer:** Im Memory als `BPM-Next:<NNN>`. Nach jedem
`tracker neu`: Next +1.

**Titel-Format für Hauptaufgaben:**
```
BPM-<NNN> | <KÜRZEL> | <Kurzbeschreibung>
```

Beispiel: `BPM-016 | PM | Recovery nach Crash`

**Titel-Format für Unteraufgaben:** `<Parent-NNN>.<Sub-NN> — <Kurzbeschr.>`

Beispiel: `016.01 — GetPendingImports() Detail-Infos`

(Universelle Sub-Nummerierungs-Regel: siehe `skills/tracker/references/clickup-fields.md`.)

---

## 5. Skill-Issue-Nummerierung

**Format:** `<skill-name>-NNN` — 3-stellig, pro Skill eigener Zähler ab 001.

**Titel-Format:** `<skill>-NNN: <Kurzbeschreibung>`

Beispiel: `tracker-005: Anker-Persistenz in Folge-Antworten`

Issue-ID wird **zusätzlich** im Custom Field `Issue-ID` (`e286a04a-…`)
gespeichert. Lücken werden nicht gefüllt.

---

## 6. Meilenstein-Tags (BPM-Scope)

ClickUp-Tags für BPM-Hauptaufgaben:

| Tag | Bedeutung |
|-----|-----------|
| `v1` | Muss für PlanManager V1 fertig sein |
| `v1-nice` | Wäre gut für V1, blockiert aber nicht |
| `post-v1` | Nach V1 Release |
| `server` | Erst wenn Server-Modus gebaut wird |
| `backlog` | Irgendwann, kein Zeitdruck |

Tags kleingeschrieben. Nur an Hauptaufgaben, nicht an Unteraufgaben.

---

## 7. Status-Werte pro Listen-Typ

| Listen-Typ | "offen" | "in Arbeit" | "erledigt" |
|---|---|---|---|
| BPM-Listen (PM, DOC, SET, etc.) | `open` | `in progress` | `done` |
| ClaudeSkills-Liste (Refactor-Plan) | `open` | `in progress` | `done` |
| Skill-Issue-Listen (tracker, cc-steuerung, …) | `to do` | `in progress` | `complete` |

**Alle Werte kleingeschrieben** — ClickUp-API ist case-sensitive.

Universelle Regel für Fallback-Reihenfolge bei unklarem Status-Wert:
siehe `skills/tracker/references/clickup-fields.md`.
