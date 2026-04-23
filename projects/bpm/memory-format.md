# BPM — Memory-Eintragsformate

Dieser Ordner dokumentiert alle Memory-Einträge die zum BPM-Projekt gehören.
Zweck: Bei Memory-Cleanup, neuem Chat oder Debugging sofort klar ist welche
Einträge BPM-spezifisch sind und wie sie aufgebaut sind.

**Source of Truth:** Die tatsächlichen Memory-Einträge (via
`memory_user_edits` tool). Diese Datei ist Doku und Referenz.

---

## Übersicht aller BPM-Memory-Einträge

| Typ | Prefix | Zweck |
|---|---|---|
| Projekt-Identifier | `[PROJECT]` | Aktives Projekt + Konfigurations-Pfad |
| ClickUp-Konfiguration | `[CLICKUP]` | Space-IDs, Listen-IDs, Nummerierung |
| Skill-Issues-Konfiguration | `[CLICKUP]` (zweiter Eintrag) | Skill-Issues-Ordner-Struktur |
| Anker-Registry | `[ANKER-LIVE]` | Chat-Anker Lifecycle |

---

## 1. `[PROJECT]` — Projekt-Identifier

Identifiziert das aktive Projekt und den Config-Pfad.

### Format

```
[PROJECT] <name> | Skill-Repo-Pfad (OneDrive-relativ): <relativer-pfad> | Projekt-Config: projects/<name>/ | <Projekt-Repo>: <url> | Aktive Spaces: <Label>=<id>, ...
```

### Aktuelles Beispiel (BPM)

```
[PROJECT] bpm | Skill-Repo-Pfad (OneDrive-relativ): Dokumente\02 Arbeit\05 Vorlagen - Scripte\00_claude-skills-bpm | Projekt-Config: projects/bpm/ | BPM-Repo: github.com/herbertschrotter-blip/BauProjektManager | Aktive Spaces: BPM=901510792907, Claude-Skills=901510833068
```

### Felder

| Feld | Inhalt |
|---|---|
| `<name>` | Projekt-Kurzname, matched Ordner in `projects/` |
| `Skill-Repo-Pfad (OneDrive-relativ)` | Pfad ohne Laufwerksbuchstabe, funktioniert auf allen PCs |
| `Projekt-Config` | Relativer Pfad zu `projects/<name>/` |
| `<Projekt-Repo>` | GitHub-URL des Projekt-Repos (nicht Skill-Repo) |
| `Aktive Spaces` | ClickUp-Space-IDs für tracker-Routing |

### Regeln

- **Exakt einer** `[PROJECT]`-Eintrag pro aktivem Chat
- Bei Projekt-Wechsel: alten Eintrag ersetzen, nicht zusätzlich anlegen
- Skill-Repo-Pfad OHNE Laufwerksbuchstabe (PC-übergreifend nutzbar)

### Universal-Teil der Spec

Die Regel "Memory-Eintrag [PROJECT] <name> existiert pro aktivem Projekt" ist
universell und in `docs/project-architecture.md` des Skill-Repos dokumentiert.
Dieser Abschnitt hier dokumentiert nur das konkrete BPM-Format.

---

## 2. `[CLICKUP]` — BPM-Space-Konfiguration

Kompakte Form der Listen-Mapping-Info für den BPM-Space.

### Format

```
[CLICKUP] BPM-Space:<id> (<N> BPM-Listen) | Claude-Skills-Space:<id> (enthält CS:..<kurz-id>) | Listen: <kuerzel>:..<kurz-id>, ... | <N> CF aktiv | BPM-Next:<NNN> | Dummy: <ids-zum-loeschen>
```

### Aktuelles Beispiel

```
[CLICKUP] BPM-Space:901510792907 (17 BPM-Listen) | Claude-Skills-Space:901510833068 (enthält CS:..935159) | Listen: PM:..848097, DOC:..848102, KON:..848103, INF:..848104, REF:..848105, SET:..849234, DASH:..850042, BTB:..850044, FOTO:..850057, ZEIT:..850060, KI:..850064, OL:..850068, VORL:..850070, PK:..850071, GIS:..850073, WET:..850074, MOB:..850075 | 10 CF aktiv | BPM-Next:084 | Dummy: 86c9evb14+86c9evbtw zum Löschen
```

### Felder

| Feld | Inhalt |
|---|---|
| `BPM-Space` | Voll-ID des BPM-Space |
| `Claude-Skills-Space` | Voll-ID des Claude-Skills-Space |
| `CS:..<kurz-id>` | Kurz-ID der ClaudeSkills-Refactor-Plan-Liste |
| `Listen: <kuerzel>:..<kurz-id>` | Komma-getrennt, Kurz-ID = letzte 6 Stellen |
| `<N> CF aktiv` | Anzahl aktiver Custom Fields im Space |
| `BPM-Next:<NNN>` | Nächste freie BPM-Nummer (3-stellig) |
| `Dummy` | IDs von zum Löschen markierten Dummy-Tasks |

### Regeln

- Listen-IDs werden **nur mit Kurz-ID** gespeichert (Memory-Kompaktheit)
- Voll-ID entsteht durch Prefix `90152284` bzw. `90152285` — siehe
  `clickup-lists.md` für Vollreferenz
- `BPM-Next` wird nach jedem `tracker neu` um 1 erhöht
- Lücken werden nie gefüllt — nur `Next` zählt weiter

---

## 3. `[CLICKUP]` — Skill-Issues-Ordner

Zweiter `[CLICKUP]`-Eintrag speziell für den Skill-Issues-Ordner und seine
11 Listen.

### Format

```
[CLICKUP] Ordner 'Skill Issues' (<ordner-id>) im Space Claude-Skills (<space-id>) mit <N> Issue-Listen: <skill1> <listen-id1>, <skill2> ..<kurz-id>, ... | CF: Issue-ID (<cf-id>), Typ (<cf-id>), Commit-Hash (<cf-id>), Beobachtungs-Chat (<cf-id>), Chat-Anker erstellt/erledigt (<cf-id>/<cf-id>).
```

### Aktuelles Beispiel

```
[CLICKUP] Ordner 'Skill Issues' (901515724728) im Space Claude-Skills (901510833068) mit 11 Issue-Listen: audit 901522952203, cc-steuerung ..208, chat-wechsel ..212, chatgpt-review ..221, code-erstellen ..225, doc-pflege ..230, git-commit-helper ..231, mockup-erstellen ..236, skill-neu ..243, skill-pflege ..246, tracker ..249. CF: Typ (5b45b13a), Commit-Hash (8e8879f7), Beobachtungs-Chat (eb1f6eb6), Chat-Anker erstellt/erledigt (identisch zu BPM).
```

### Felder

| Feld | Inhalt |
|---|---|
| `Ordner 'Skill Issues'` | Ordner-ID im Claude-Skills-Space |
| `<N> Issue-Listen` | Aktuelle Anzahl Listen (wächst bei neuen Skills) |
| `<skill> <listen-id>` | Erste Liste Voll-ID, Rest Kurz-ID |
| `CF: ...` | Custom-Field-Namen + IDs (Ordner-weit) |

### Zweck

Erster `[CLICKUP]`-Eintrag (Abschnitt 2) fokussiert auf Task-Routing.
Dieser Eintrag hält die **Issue-Spezifika** getrennt weil sie andere
Custom Fields und andere Status-Werte haben (`complete` statt `done`).

---

## 4. `[ANKER-LIVE]` — Chat-Anker-Registry

Laufende Registry aller aktiven Chat-Anker. Details siehe universelle Spec
in `skills/tracker/references/anker-system.md`.

### Format

```
[ANKER-LIVE] <task-id>|<typ>|<timestamp>|<kurzbeschreibung>
```

### Beispiel

```
[ANKER-LIVE] 86c9fj88e|erstellt|2026-04-23T08:30:00Z|7.1 Ordnerstruktur + Docs
```

### Felder

| Feld | Inhalt |
|---|---|
| `<task-id>` | ClickUp-Task-ID (9-stellig hex) |
| `<typ>` | `erstellt` oder `erledigt` |
| `<timestamp>` | ISO 8601 UTC |
| `<kurzbeschreibung>` | Knappe Beschreibung für Chat-Scan |

### Lifecycle

Details in `skills/tracker/references/anker-system.md`:

- Anker wird bei `tracker neu` als `erstellt` eingetragen
- Bei `tracker done` wird er als `erledigt` ersetzt
- Anker älter als 24h werden beim Chat-Start geprüft (Stale-Check)
- Bei Rollover: Anker wandert mit in den neuen Chat

### Warum hier dokumentiert

Der **Format-Teil** ist universell (anker-system.md). Der **Scope** ist aber
projekt-spezifisch: Anker werden nur für Tasks im aktiven Projekt-Space
gesetzt. Bei mehreren Projekten: pro Projekt eigene Anker-Registry.

---

## Nicht-projekt-spezifische Memory-Einträge

Diese Einträge im Memory gehören **nicht** zu BPM sondern sind
projekt-unabhängige Regeln und werden hier zur Abgrenzung gelistet:

- Allgemeine Skill-Update-Regeln (z.B. Artifact-Name `SKILL.md`)
- ChatGPT-Modell-Hinweise
- UI-Design-Patterns die skill-übergreifend gelten
- DC-PowerShell-Workarounds

Diese bleiben beim Projekt-Wechsel bestehen. Nur Einträge die im
[PROJECT]/[CLICKUP]/[ANKER-LIVE]-Schema laufen werden beim Wechsel
ersetzt.

---

## Memory-Cleanup beim Projekt-Wechsel

Wenn BPM durch ein anderes Projekt ersetzt wird:

1. `[PROJECT] bpm | ...` → `[PROJECT] <neu> | ...`
2. `[CLICKUP] BPM-Space:... | ...` → ersetzen oder löschen
3. `[CLICKUP] Ordner 'Skill Issues' ... | ...` → bleibt (ist Claude-Skills-
   übergreifend, nicht BPM-spezifisch)
4. `[ANKER-LIVE] <task>|...` → alle mit BPM-Task-IDs löschen

Für automatisiertes Cleanup siehe `skill-pflege`-Skill.
