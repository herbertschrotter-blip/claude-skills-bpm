# ClickUp Custom Fields, Listen, IDs, Nummerierung

Universelle Referenz für `tracker neu`, `tracker done`, `tracker field`, `tracker split`.

**Konkrete BPM-Werte** (Listen-IDs, Custom-Field-IDs, Option-IDs, Modul-Kürzel, Meilenstein-Tags, Status-Werte-Matrix) liegen in `projects/<[PROJECT]>/clickup-fields.md`. Diese Datei enthält nur universelle Regeln und Muster.

---

## ClickUp-Konfiguration

Aus Memory lesen: `[PROJECT]`- und `[CLICKUP]`-Einträge. Format-Spec siehe `projects/<[PROJECT]>/memory-format.md`.

---

## Custom Fields

Custom-Field-IDs, -Typen und deren Semantik sind **projekt-spezifisch**.
Siehe `projects/<[PROJECT]>/clickup-fields.md`:

- **Abschnitt 1 — BPM-Scope / Haupt-Scope:** Fields die bei `tracker neu`
  (Neue Tasks) und `tracker done` (Abschluss) gesetzt werden — typischerweise
  Typ, Aufwand, Zielversion, Komponente, Zugehörige Docs, Commit ID, Commit Text, Erledigt, Chat-Anker erstellt/erledigt.
- **Abschnitt 2 — Issue-Scope** (falls vorhanden): Fields für Skill-Issues
  oder ähnliche Sekundär-Listen.

### Dropdown-Regel (universell)

Wenn ein Field `drop_down`-Typ hat: **Option-ID** (nicht Display-Label) als
Value setzen. Option-IDs stehen in `projects/<[PROJECT]>/clickup-fields.md`.
Bei unbekannter Option-ID: `ask_user_input_v0` mit den bekannten Options —
**nie raten**.

---

### Option-IDs pro Dropdown

Liste der Option-IDs für alle Dropdowns des Projekts:
`projects/<[PROJECT]>/clickup-fields.md`.

---

## Default bei `tracker neu`

**Pflicht ausfüllen** (wenn ermittelbar):
- Typ-Field (aus Kontext oder `ask_user_input_v0`)
- Chat-Anker-erstellt-Field (ClickUp-Task-ID, wird nach `clickup_create_task` direkt gesetzt)

**Wenn vorhanden** (aus `[ANKER-LIVE]` Memory):
- Chat-Anker-temp-Field (TEMP-ID aus Ausarbeitungsphase)

**Wenn bekannt** (sonst leer lassen):
- Aufwand, Zielversion, Komponente, Zugehörige Docs (oder äquivalente
  Projekt-Fields — siehe `projects/<[PROJECT]>/clickup-fields.md`)

---

## Default bei `tracker done`

**Pflicht ausfüllen**:
- Commit-ID-Field + Commit-Text-Field (aus DC `git log`)
- Erledigt-Field (Commit-Datum)
- Chat-Anker-erledigt-Field (ClickUp-Task-ID)

**Nachpflegen** (falls bei `tracker neu` nicht gesetzt):
- Typ, Zugehörige Docs, Komponente, Zielversion

---

## Modul-Kürzel

Die Zuordnung Modul-Name → Kürzel → Listen-ID ist **projekt-spezifisch**.
Siehe `projects/<[PROJECT]>/clickup-fields.md` Abschnitt "Modul-Kürzel".

Bei Abweichung: Memory `[CLICKUP]`-Eintrag ist Quelle, danach `projects/<[PROJECT]>/clickup-lists.md`.

### Auto-Create für neue Module

Wenn ein neues Modul auftaucht das noch keine Liste hat:

1. `ask_user_input_v0` zur Bestätigung: "Liste '<Modul>' neu anlegen?"
2. Bei Bestätigung: `clickup_create_list(name: "<Modul>", space_id: "<Space-ID-aus-Memory>")`
3. Memory-Eintrag `[CLICKUP]` aktualisieren mit neuer Listen-ID
4. Kürzel-Eintrag in `projects/<[PROJECT]>/clickup-fields.md` ergänzen
5. User informieren über neue Liste + Kürzel

---

## Globale Nummerierung (Hauptaufgaben)

**Pattern:** `<PROJEKT-PREFIX>-<NNN>` — dreistellig mit führenden Nullen,
global über alle Listen des Projekts, **nie wiederverwendet**.

- Projekt-Prefix (z.B. `BPM-`) aus `projects/<[PROJECT]>/clickup-fields.md`
- Nächste freie Nummer im Memory: `<Prefix>Next:<NNN>`
- Nach jedem `tracker neu`: Next +1

### Unteraufgaben-Nummerierung

**Unteraufgaben bekommen KEINE eigene Haupt-Nummer**, sondern eine
**Positionsnummer** im Titel.

Pattern: `<Parent-NNN>.<Sub-NN> — <Kurzbeschreibung>`

Beispiele:
- `016.01 — GetPendingImports() Detail-Infos`
- `016.02 — Recovery-Entscheidungsmatrix`
- `079.01 — Mockup 1/2 Tab-Navigation Design`

**Regeln:**
- Sub-NN fortlaufend 01, 02, 03... pro Parent (2-stellig mit führender Null)
- Bei 100+ Unteraufgaben (unwahrscheinlich): 3-stellig (.001, .002)
- Parent-NNN mit führenden Nullen auf 3-stellig gepaddet (007, 016, 079)
- Bei Löschen einer Unteraufgabe: Nummer NICHT nachnummerieren (Lücke bleibt)
- Bei Nachtrag: nächste freie Sub-Nummer verwenden

---

## Titel-Format

### Hauptaufgaben

```
<PROJEKT-PREFIX>-<NNN> | <KÜRZEL> | <Kurzbeschreibung>
```

Beispiel (BPM): `BPM-016 | PM | Recovery nach Crash`

### Unteraufgaben

```
<Parent-NNN>.<Sub-NN> — <Kurzbeschreibung>
```

Beispiel: `016.01 — GetPendingImports() Detail-Infos`

Kein Prefix, kein Kürzel. Zuordnung über Parent-Task + Nummerierung.

### Issue-Tasks (Skill-Issues-Scope oder vergleichbar)

```
<issue-scope-name>-<NNN>: <Kurzbeschreibung>
```

Beispiel: `tracker-005: Anker-Persistenz in Folge-Antworten`

Issue-ID zusätzlich im passenden Custom Field speichern — siehe
`projects/<[PROJECT]>/clickup-fields.md`.

---

## Meilenstein-Tags

Tag-Namen + Bedeutung sind **projekt-spezifisch**:
`projects/<[PROJECT]>/clickup-fields.md` Abschnitt "Meilenstein-Tags".

Universelle Regeln:
- Tags **kleingeschrieben** in ClickUp
- Nur an **Hauptaufgaben**, nicht an Unteraufgaben
- Bei unbekanntem Tag: `ask_user_input_v0` mit den definierten Tags

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

Allgemeines Konzept (universell):

| Semantik | Übliche Werte |
|----------|---------------|
| noch nicht angefangen | `open` oder `to do` |
| wird bearbeitet | `in progress` |
| erledigt und committet | `done` oder `complete` |

**IMMER kleingeschrieben in API-Calls!** ClickUp-API ist case-sensitive.
Grossgeschrieben wirft `"Status does not exist"`-Fehler.

### Status-Werte pro Listen-Typ

Nicht alle ClickUp-Listen nutzen die gleichen Status-Werte. Die
**konkrete Matrix** pro Listen-Typ steht in
`projects/<[PROJECT]>/clickup-fields.md` Abschnitt "Status-Werte pro Listen-Typ".

### Fallback-Reihenfolge bei Status-Änderung

1. Zuerst den listen-typischen Wert versuchen (aus `projects/<[PROJECT]>/clickup-fields.md`)
2. Bei Fehler `"Status does not exist"`: Alternative aus derselben Zeile probieren
3. Wenn beide scheitern: `ask_user_input_v0` mit den bekannten Werten

Für `in progress` ist der Wert listen-übergreifend gleich.

---

## Memory-Pflege

Nach jeder relevanten Änderung den entsprechenden Memory-Eintrag
aktualisieren:

- Neue Liste-ID → `[CLICKUP]`-Eintrag erweitern
- Next-Nummer → `<Prefix>Next:` erhöhen
- Letzte Sync-Markierung (z.B. `Letzte Sync: Teil <N>`) setzen

Eintragsformate pro Projekt: `projects/<[PROJECT]>/memory-format.md`.
