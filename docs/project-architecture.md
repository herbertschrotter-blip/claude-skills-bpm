# Projekt-Architektur des Skill-Repos

**Zweck:** Trennung von universellen Skills und projekt-spezifischer Config.
Erlaubt dass Skills wiederverwendbar bleiben, während konkrete Daten
(ClickUp-IDs, Modul-Kürzel, Repo-Pfade) pro Projekt isoliert sind.

---

## Problem

Skills wie `tracker`, `code-erstellen`, `doc-pflege` enthalten in ihrer
Ursprungsform sowohl:

- **Universelle Regeln** (z.B. "Pro-Task-Quittung nach jedem Tool-Call",
  "em-dash in Custom-Field-Values vermeiden")
- **Projekt-spezifische Daten** (z.B. ClickUp-Listen-IDs, BPM-Modul-Kürzel,
  konkrete Custom-Field-IDs)

Das macht die Skills nicht wiederverwendbar für mehrere Projekte. Ein zweites
Projekt müsste die Skills komplett forken und Daten überall ersetzen.

---

## Lösung: Ordnerstruktur

```
claude-skills-bpm/
├── skills/              ← universelle Skills (wiederverwendbar)
│   └── <skill-name>/
│       ├── SKILL.md
│       └── references/
├── projects/            ← projekt-spezifische Configs
│   └── <projekt-name>/  ← z.B. "bpm"
│       ├── README.md
│       ├── clickup-lists.md
│       ├── clickup-fields.md
│       └── memory-format.md
└── docs/
    └── project-architecture.md   ← diese Datei
```

### Was gehört wohin

| Ort | Inhalt |
|---|---|
| `skills/<skill>/` | Regeln, Abläufe, Formate, universelle Trigger-Phrasen, universelle VERBOTEN-Listen |
| `projects/<projekt>/` | Listen-IDs, Custom-Field-IDs, Option-IDs, Modul-Kürzel, Repo-Pfade, Projekt-spezifische Konventionen |

### Entscheidungsregel

Wenn eine Information **beim Wechsel zu einem neuen Projekt neu definiert
werden müsste** → projekt-spezifisch → `projects/<projekt>/`.

Wenn sie **für jedes Projekt gleich sinnvoll** ist → universell → `skills/`.

---

## Memory-Mechanismus

Skills erfahren das aktive Projekt über einen Memory-Eintrag:

```
[PROJECT] <projekt-name> | Skill-Repo-Pfad: ... | Projekt-Config: projects/<name>/ | <Weitere projekt-spezifische Info>
```

Beispiel BPM:
```
[PROJECT] bpm | Skill-Repo-Pfad (OneDrive-relativ): Dokumente\02 Arbeit\05 Vorlagen - Scripte\00_claude-skills-bpm | Projekt-Config: projects/bpm/ | BPM-Repo: github.com/herbertschrotter-blip/BauProjektManager | Aktive Spaces: BPM=901510792907, Claude-Skills=901510833068
```

Skills lesen diesen Eintrag und wissen wo die Projekt-Config liegt.

### Wenn kein `[PROJECT]`-Eintrag existiert

Skill fragt `ask_user_input_v0`: "Welches Projekt ist aktiv?" — mit Liste der
vorhandenen Ordner in `projects/`. Bei leerem `projects/`-Verzeichnis:
Skill läuft im Universell-Modus (Platzhalter für Daten) und bittet User um
Angabe der konkreten IDs.

### Projekt-Wechsel

Mehrere Projekte parallel: Memory-Edit auf `[PROJECT]` ändern. Die Skills
wechseln automatisch, weil sie den Eintrag lesen.

**Empfehlung:** Pro Chat-Session genau ein `[PROJECT]`-Eintrag aktiv. Bei
Wechsel mitten in der Session explizit ankündigen und Memory anpassen.

---

## Skills mit projekt-spezifischen Anteilen

Stand heute (Skill-Repo v0.12.0, vor v0.13.0-Refactor):

| Skill | Projekt-spezifisch? | Status |
|---|---|---|
| tracker | Ja (Listen, Kürzel, IDs) | Refactor in v0.13.0 |
| code-erstellen | Ja (Architektur, Pfade) | Später |
| doc-pflege | Ja (INDEX-Routing, Docs-Struktur) | Später |
| git-commit-helper | Ja (Repo-Pfade, Versionsregeln) | Später |
| chatgpt-review | Ja (CGR-Pfad, Themen-Enum) | Später |
| mockup-erstellen | Ja (Design-Tokens, UI-Guidelines) | Später |
| chat-wechsel | Teilweise (Memory-Formate projekt-spezifisch) | Später |
| audit | Teilweise (INDEX-Check projekt-spezifisch) | Später |
| cc-steuerung | Minimal (OneDrive-Pfade) | Später |
| skill-pflege | Nein | — |
| skill-neu | Nein | — |

Nur `tracker` wird in v0.13.0 bereinigt. Die anderen folgen in eigenen
Releases.

---

## Wie ein neues Projekt angelegt wird

1. Neuen Ordner `projects/<projekt-name>/` anlegen
2. `README.md` mit Projekt-Beschreibung
3. Datendateien nach Bedarf: `clickup-lists.md`, `clickup-fields.md`,
   `memory-format.md`, weitere je nach Skills die genutzt werden
4. Memory-Eintrag `[PROJECT] <projekt-name> | ...` setzen
5. Skills lesen ab jetzt die neue Config
