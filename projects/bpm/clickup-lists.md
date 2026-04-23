# BPM — ClickUp Listen-Mapping

Vollständige Übersicht aller ClickUp-Listen für das BPM-Projekt und deren
IDs für das Routing in `tracker neu`, `tracker issue`, `tracker done` etc.

**Quelle of Truth:** Memory `[CLICKUP]`-Einträge. Diese Datei ist Doku und
Fallback wenn Memory nicht verfügbar ist.

---

## Space 1 — BPM (BauProjektManager)

**Space-ID:** `901510792907`

17 BPM-Listen (eine pro Modul):

| Modul | Kürzel | Listen-ID |
|-------|--------|-----------|
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

**Custom-Field-Scope:** 10 BPM-Fields — Typ, Aufwand, Zielversion,
Komponente, Zugehörige Docs, Commit ID, Commit Text, Erledigt,
Chat-Anker temp, Chat-Anker erstellt/erledigt. IDs und Option-IDs in
`clickup-fields.md`.

**Status-Werte:** `open` / `in progress` / `done`

**Nummerierung:** Global `BPM-<NNN>`, dreistellig, nie wiederverwendet.
Nächste freie Nummer im Memory: `Next:<NNN>`.

---

## Space 2 — Claude Skills Entwicklung

**Space-ID:** `901510833068`

### 2a. Liste direkt im Space: ClaudeSkills (Refactor-Plan)

**Listen-ID:** `901522935159`

**Zweck:** Refactor-Plan-Tasks (Phasen 1-7), Meta-Tasks zum Skill-System.

**Custom-Field-Scope:** 10 Fields (identisch zu BPM). Feld-IDs siehe
`clickup-fields.md`.

**Status-Werte:** `open` / `in progress` / `done`

### 2b. Ordner "Skill Issues" mit 11 Issue-Listen

**Ordner-ID:** `901515724728`

Eine Liste pro Skill, für Issue-Tracking (Bugs, Trigger-Fehler, Doku-Fehler,
Verbesserungs-Ideen, Refactor-Ideen).

| Skill | Listen-ID |
|-------|-----------|
| audit | 901522952203 |
| cc-steuerung | 901522952208 |
| chat-wechsel | 901522952212 |
| chatgpt-review | 901522952221 |
| code-erstellen | 901522952225 |
| doc-pflege | 901522952230 |
| git-commit-helper | 901522952231 |
| mockup-erstellen | 901522952236 |
| skill-neu | 901522952243 |
| skill-pflege | 901522952246 |
| tracker | 901522952249 |

**Custom-Field-Scope:** 6 Skill-Issue-Fields — Issue-ID, Typ, Commit-Hash,
Beobachtungs-Chat, Chat-Anker erstellt/erledigt. IDs in `clickup-fields.md`.

**Status-Werte:** `to do` / `in progress` / `complete`
⚠️ **Unterschied zu BPM/ClaudeSkills!** Skill-Issues-Listen nutzen
`complete`, nicht `done`.

**Nummerierung:** Pro Skill `<skill-name>-NNN`, dreistellig, ab 001 pro
Skill. Lücken werden bewusst nicht gefüllt (wegen Chat-Anker-Referenzen).
Höchste vergebene Nummer ermitteln über Scan aller Tasks der Liste
(Custom Field `Issue-ID`). Siehe tracker-003 für Auto-Nummerierung.

---

## Scope-Erkennung (Routing-Logik)

Bei jedem `tracker`-Kommando Ziel-Scope aus der Syntax ableiten:

| Kommando-Syntax | Ziel-Scope | Ziel-Liste |
|---|---|---|
| `tracker neu: <Modul-Kürzel> — ...` | **BPM** | Space 1, passende Modul-Liste |
| `tracker neu: <ClaudeSkills-Phase-Titel>` | **ClaudeSkills** | Space 2, Liste 901522935159 |
| `tracker issue <skill-name>: ...` | **Skill-Issues** | Space 2, passende Skill-Issues-Liste |

### Gültige Skill-Namen für `tracker issue`

Eindeutige Werte für `<skill-name>`:

- `audit`
- `cc-steuerung`
- `chat-wechsel`
- `chatgpt-review`
- `code-erstellen`
- `doc-pflege`
- `git-commit-helper`
- `mockup-erstellen`
- `skill-neu`
- `skill-pflege`
- `tracker`

Bei unbekanntem Skill-Namen: `ask_user_input_v0` mit diesen 11 Werten als
Optionen. **Nie raten.**

### Gültige Modul-Kürzel für `tracker neu`

Siehe Tabelle in Space 1. Kürzel (PM, DOC, INF, …) sind in Großbuchstaben.
Bei unbekanntem Kürzel: `ask_user_input_v0` mit Liste.

---

## Memory-Quelle

Die kompakten Formen stehen im Memory:

```
[CLICKUP] BPM-Space:901510792907 (17 BPM-Listen) | Claude-Skills-Space:901510833068 (enthält CS:..935159) | Listen: PM:..848097, ... | 10 CF aktiv | BPM-Next:<NNN>
```

```
[CLICKUP] Ordner 'Skill Issues' (901515724728) im Space Claude-Skills (901510833068) mit 11 Issue-Listen: audit 901522952203, cc-steuerung ..208, ...
```

Bei Konflikt zwischen Memory und dieser Datei: **Memory ist Source of Truth**,
diese Datei ist Fallback und ausführlichere Dokumentation.

---

## Verbotene Aktionen

- Listen-IDs raten wenn Skill-Name nicht in Tabelle — `ask_user_input_v0`
- Task in falscher Liste anlegen weil Scope nicht geprüft wurde
- Custom Fields aus falschem Scope setzen (z.B. Skill-Issue-Task mit
  BPM-Fields oder umgekehrt)
- Status-Wert raten — **immer listen-typisch** (BPM/ClaudeSkills: `done`,
  Skill-Issues: `complete`)
- Skill-Issue-Nummerierung neu starten oder Lücken füllen — Lücken sind
  absichtlich wegen Chat-Anker-Referenzen
