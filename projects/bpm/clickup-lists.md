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

**Umgezogen** in die Config des Skill-Repos: `.claude/skill-config/tracker.md` (Liste ClaudeSkills, Ordner „Skill Issues“
mit den Issue-Listen, Felder, Status, Nummernschema). Diese Datei behält nur den BPM-Space und zieht in Umbau Phase 2 ins
BPM-Repo (`docs/skillsystem-umbau.md`).

---

## Scope-Erkennung (Routing-Logik)

Bei jedem `tracker`-Kommando Ziel-Scope aus der Syntax ableiten:

| Kommando-Syntax | Ziel-Scope | Ziel-Liste |
|---|---|---|
| `tracker neu: <Modul-Kürzel> — ...` | **BPM** | Space 1, passende Modul-Liste |
| `tracker neu: <ClaudeSkills-Phase-Titel>` | **ClaudeSkills** | siehe `.claude/skill-config/tracker.md` im Skill-Repo |
| `tracker issue <skill-name>: ...` | **Skill-Issues** | siehe `.claude/skill-config/tracker.md` im Skill-Repo |

Gültige Skill-Namen für `tracker issue` und ihre Listen: `.claude/skill-config/tracker.md` im Skill-Repo.

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

---

## Präfix (Nummern und Anker)

**Task-Präfix:** `BPM` → Titel `BPM-NNN | <KÜRZEL> | <Kurztitel>`
**Anker-Präfix:** `BPM-ANCHOR` → `[BPM-ANCHOR-<task-id>]`
Der Präfix wird pro Projekt festgelegt; andere Projekte haben einen eigenen (Heidi: `DX`).
**Workspace-ID:** `90152410319` (aus references/clickup-tools.md hierher verschoben, 16.09.2026)
