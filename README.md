# claude-workbench

Skills für Claude Code (auf Deutsch) und zwei Helfer im Hintergrund: das **Skill-Log**, das mitschreibt, welcher Skill
wann gezündet hat, und den **Skill-Wächter**, der darauf achtet, dass Claude für Code, Doku und Mockups den passenden
Skill lädt. Alles kommt als Plugin über den Marketplace `workbench`.

## Schnellstart

### 1. Was du brauchst

| Was | Wofür | Fehlt es? |
|---|---|---|
| **Claude Code**, angemeldet | darin laufen die Skills | Das Skript bietet den offiziellen Installer an und meldet am Ende an (`claude auth login`, Browser) |
| **git** | Claude Code holt den Marketplace als Git-Repo | Das Skript installiert es auf Wunsch |
| **Python 3** (ab 3.8) | Skill-Log und Wächter sind Python-Skripte | Das Skript installiert es auf Wunsch (Windows: aus dem Microsoft Store, damit `python3` funktioniert) |
| ClickUp-Konnektor (optional) | nur für den Skill tracker | bei claude.ai unter Konnektoren |

### 2. Installieren – ein Befehl

**Windows** (PowerShell):

```powershell
irm https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.ps1 | iex
```

**Linux, macOS, Home-Assistant-Add-on:**

```sh
curl -fsSL https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.sh | sh
```

Das Skript prüft zuerst ohne Netz, was schon da ist, und stellt dann **alle Fragen auf einmal**:

1. **Was fehlt, installieren?** (git, Python, Claude Code – nur, was wirklich fehlt; Updates für git werden angeboten)
2. **Desktop-App oder Terminal?** In der Claude-Desktop-App kommen nur die Helfer (`work-hooks`), die Skills holt die
   App von claude.ai. Im Terminal kommen Skills und Helfer (`work`, dazu `skill-workshop`).
3. **Rechnername** – Vorschlag ist der Windows-Computername bzw. der schon eingerichtete Name (z. B. `surface`).
4. **Sammel-Repo** (optional, privat) und ob dieselben Skills auch bei claude.ai hochgeladen sind.

Danach läuft alles ohne Rückfrage durch, mit einem Fortschrittsbalken. Zum Schluss meldet es sich bei Claude an, falls
nötig (Browser) – die Anmeldung der Desktop-App zählt dafür nicht. Dann **Claude Code neu starten** – fertig.
Was das Skript installiert, steht im Protokoll `~/.claude/workbench-einrichtung.json`; ein erneuter Start setzt fort.
Updates, Entfernen und was bei Problemen hilft: [`docs/installation.md`](./docs/installation.md).

### 3. Im Alltag

| Du willst … | So geht's |
|---|---|
| Updates | kommen von selbst beim Start von Claude Code (das Skript schaltet Auto-Update ein) |
| sofort aktualisieren | `claude plugin marketplace update workbench`, dann `claude plugin update work@workbench`, dann Claude neu starten |
| Einstellungen ändern (Rechnername, Sammel-Repo, Log oder Wächter aus) | in Claude Code `/plugin configure work@workbench` (bzw. `work-hooks@workbench`) – oder das Skript noch einmal laufen lassen |
| prüfen, was installiert ist | `claude plugin list` |
| Statistik sehen (auch Arbeitszeit je Projekt) | in Claude Code `/statistik` (oder `/statistik ha-baustelle`, `/statistik 2026-10-01`): Dashboard mit Zündungen je Skill und Projekt, Verlauf und Blockaden des Wächters |
| reparieren oder neuen Rechner einrichten | das Installationsskript einfach noch einmal laufen lassen |
| entfernen | Installationsskript mit `-Entfernen` bzw. `--entfernen` (nimmt nur zurück, was es selbst angelegt hat) – siehe [`docs/installation.md`](./docs/installation.md) |

**Gut zu wissen**

- Der Wächter **blockiert** Änderungen an Code, Doku und Mockups sowie Commits, solange der zuständige Skill nicht
  geladen ist. Nach einem Commit, einem Aufgabenstart oder einer neuen Aufgabennummer gilt ein früher geladener Skill
  als verbraucht. Claude lädt ihn dann selbst nach und macht weiter. Stört eine Regel, sag es Claude; die Regeln werden mit
  skill-auswertung nachgeschärft.
- **Nie `work` und `work-hooks` zusammen** installieren – sonst läuft jeder Helfer doppelt. Das Skript achtet darauf.
- Das Skill-Log liegt auf deinem Rechner (`~/.claude/skill-log/`). Nur wenn du ein privates Sammel-Repo angibst,
  gleicht jeder Rechner es dorthin ab (enthält Prompt-Texte – andere Nutzer sehen es nie).
- Damit die Skills in einem Projekt richtig arbeiten, braucht die `CLAUDE.md` des Projekts ein Skill-Profil. Fehlt es,
  fragen die Skills nach; „richte die Skills hier ein“ legt es an (Skill projekt-anlegen).

## Über dieses Repo

Claude-Skills von Herbert Schrotter für Claude Code, als Plugin-Marketplace `workbench`. Entstanden im Projekt
BauProjektManager (BPM), heute für C#-, TypeScript-, Python- und Home-Assistant-Projekte im Einsatz.

Dieses Repo enthält 15 Skills samt Evals, Prüfskript, Refactor-Dokumentation und Memory-Konventionen, dazu zwei Hooks
(Skill-Log und Skill-Wächter). Die Skills sind projektneutral: Projektwerte (Pfade, Präfixe, IDs, Befehle) kommen aus
dem Skill-Profil in der `CLAUDE.md` des jeweiligen Repos und dessen Configs unter `.claude/skill-config/`. Sie sind auf
eine bestimmte Arbeitsweise zugeschnitten (Deutsch, ClickUp, Commit-Format `[vX.Y.Z] Modul, Typ: Kurztitel`, Kapitel 10);
wer sie nutzen will, ist willkommen. Für generische Skills siehe z.B.
[obra/superpowers](https://github.com/obra/superpowers) oder
[alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills).

> **Umbau läuft (seit 24.09.2026):** [`docs/skillsystem-umbau.md`](./docs/skillsystem-umbau.md) – Skill-Profil v1,
> Qualitätsregeln, Prüfskript und Routing-Tests; Ergebnis der Review-Serie `CGR-2026-09-24-skillsystem`.

> **Verbindliche Regelquelle:** [INDEX.md](./INDEX.md) definiert Routing und globale Invarianten.
> Dieses README ist Onboarding-Kontext und wiederholt keine operativen Regeln.

---

## Installation im Detail

**Voraussetzungen:** Claude Code; git; Python 3 (Befehl `python3`) für die Hooks; für den Skill tracker ein
ClickUp-Konnektor (MCP). Die Skills sprechen Deutsch.

**Am einfachsten: Installationsskript.** Bestandsaufnahme ohne Netz, dann alle Fragen auf einmal, danach läuft es
unbeaufsichtigt: Fehlendes installieren (git und Python mit winget bzw. Paketmanager, Claude Code mit dem offiziellen
Installer, parallel), `~/.local/bin` dauerhaft in den PATH, Marketplace, Plugins passend zum Rechner, Optionen
`log_host` und `log_repo`, `autoUpdate`, auf Wunsch `skillOverrides`, Probe der Hooks, unter Windows optional eine
wöchentliche Aufgabe für git-Updates, zum Schluss die Anmeldung. Ein erneuter Lauf setzt fort bzw. aktualisiert.
Ablauf, Protokoll, Entfernen und Fehlerquellen: [`docs/installation.md`](./docs/installation.md).

Windows (PowerShell):

```powershell
irm https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.ps1 | iex
```

Linux, macOS, Home-Assistant-Add-on (mit Optionen nach `sh -s --`):

```sh
curl -fsSL https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.sh | sh -s -- --host laptop
```

Optionen: `--modus terminal|desktop`, `--host <name>`, `--log-repo <owner/name>`, `--ja` (alle Vorschläge annehmen),
`--ohne-overrides`, `--ohne-login`, `--entfernen`; unter Windows `-Modus`, `-RechnerName`, `-LogRepo`, `-Ja`,
`-OhneOverrides`, `-OhneLogin`, `-Entfernen` (mit `powershell -File tools\install.ps1 …` aus einem Klon, oder
`& ([scriptblock]::Create((irm …/install.ps1))) -Entfernen`).
Die Logik steht in [`tools/einrichten.py`](./tools/einrichten.py).

**Von Hand** (in Claude Code; in der Shell gehen dieselben Befehle als `claude plugin …`):

```
/plugin marketplace add herbertschrotter-blip/claude-workbench
/plugin install work@workbench
/plugin install skill-workshop@workbench      # nur wer selbst an Skills arbeitet
```

| Plugin | Inhalt | Wann |
|---|---|---|
| `work` | 11 Skills für die Projektarbeit (Code, Mockups, Doku, Tickets, Tracker, Commits, Übergaben, Sitzungen, Reviews) + Hooks Skill-Log und Skill-Wächter | Standard |
| `skill-workshop` | skill-neu, skill-pflege, skill-auswertung | zusätzlich, für die Arbeit an Skills |
| `work-hooks` | nur Skill-Log und Skill-Wächter, ohne Skills | wenn die Skills schon anders geladen werden (z. B. Upload bei claude.ai). **Nie zusammen mit `work`** – sonst läuft jeder Hook doppelt |

Die Hooks kommen mit dem Plugin; von Hand eingerichtet wird nichts außer den Einstellungen unten.

**Updates:** Die Plugins haben keine feste Version, jeder Commit ist ein Update. Auto-Update ist bei fremden Marketplaces
ab Werk **aus**. Einschalten über `/plugin` → Marketplaces → `workbench` → Auto-Update, oder in
`~/.claude/settings.json`:

```json
"extraKnownMarketplaces": {
  "workbench": {
    "source": { "source": "github", "repo": "herbertschrotter-blip/claude-workbench" },
    "autoUpdate": true
  }
}
```

Auto-Update greift beim Start einer Sitzung. Von Hand – zuerst den Marketplace, sonst sieht Claude Code keine neue
Version:

```
claude plugin marketplace update workbench
claude plugin update work@workbench
claude plugin update skill-workshop@workbench
```

Danach Claude neu starten (mit tmux und dem Skill sitzung: `sitzung.py neustart <fenster>` je Fenster). Stand prüfen:
`claude plugin list` (Version = Git-Commit). Entfernen: mit dem Installationsskript (`-Entfernen`/`--entfernen`), von
Hand nur ohne Protokoll – siehe [`docs/installation.md`](./docs/installation.md).

**Einstellungen** sind Plugin-Optionen: Claude Code fragt sie beim Aktivieren ab, ändern über `/config` oder
`/plugin configure work@workbench`, bei der Installation direkt mit `--config log_host=laptop`. Alternativ als Variable
im Block `env` der `~/.claude/settings.json`; die Variable hat Vorrang.

| Option | Variable | Wirkung |
|---|---|---|
| `log_host` | `SKILL_LOG_HOST` | Name des Rechners im Skill-Log (sonst der Hostname) |
| `log_dir` | `SKILL_LOG_DIR` | Ablage des Skill-Logs (Standard `~/.claude/skill-log/`) |
| `skill_log` | `SKILL_LOG=aus` | Skill-Log an/aus |
| `skill_guard` | `SKILL_GUARD=aus` | Skill-Wächter an/aus |
| `guard_rules` | `SKILL_GUARD_RULES` | eigene Regeldatei statt `plugins/work-hooks/hooks/regeln.json` |
| `log_repo` | `SKILL_LOG_REPO` | privates GitHub-Repo `owner/name`, in das jeder Rechner sein Skill-Log beim Sitzungsstart abgleicht (enthält Prompt-Texte – nur privat). Leer = kein Abgleich. `/statistik` und die Auswertung zeigen dann alle Rechner |

**Dieselben Skills auch bei claude.ai hochgeladen?** Dann wären sie im Terminal doppelt da (`anthropic-skills:<name>`
und `work:<name>`). Im Terminal die claude.ai-Fassung je Skill abschalten, in `~/.claude/settings.json`:

```json
"skillOverrides": {
  "anthropic-skills:audit": "off", "anthropic-skills:chat-wechsel": "off", "anthropic-skills:chatgpt-review": "off",
  "anthropic-skills:code-erstellen": "off", "anthropic-skills:doc-pflege": "off", "anthropic-skills:git-commit-helper": "off",
  "anthropic-skills:mockup-erstellen": "off", "anthropic-skills:projekt-anlegen": "off", "anthropic-skills:sitzung": "off",
  "anthropic-skills:ticket": "off", "anthropic-skills:tracker": "off", "anthropic-skills:skill-neu": "off",
  "anthropic-skills:skill-pflege": "off", "anthropic-skills:skill-auswertung": "off"
}
```

Die Claude-Desktop-App beachtet `skillOverrides` nicht. Dort `work-hooks` statt `work` und `skill-workshop`
installieren; die Skills kommen dann aus claude.ai.

| Rechner | Plugins | dazu |
|---|---|---|
| Terminal (z. B. Home-Assistant-Add-on) | `work`, `skill-workshop` | `log_host`, optional `log_repo`, `autoUpdate`, `skillOverrides` (falls bei claude.ai hochgeladen) |
| Claude-Desktop-App | `work-hooks` | `log_host`, optional `log_repo`, `autoUpdate`; Desktop-App nach der Einrichtung neu starten (PATH, `python3`) |

**Skill-Wächter:** Er blockiert ab Werk Änderungen an Code, Doku und Mockups, neue Docs ohne doc-pflege und Commits
ohne git-commit-helper (bzw. ticket oder einen Skill, der selbst committet), solange der zuständige Skill nicht geladen
ist; Claude lädt ihn dann nach. Bei ClickUp-Aktionen ohne tracker warnt er. Ein geladener Skill verfällt nach einem
Commit, einem Aufgabenstart oder einer neuen Aufgabennummer. Regeln, Grenzen und Format:
[`docs/skill-guard-v1.md`](./docs/skill-guard-v1.md). Das Skill-Log hält Prompts und Skill-Zündungen fest, lokal auf dem
Rechner und optional im privaten Sammel-Repo ([`docs/skill-log-v1.md`](./docs/skill-log-v1.md)).

**Projekt einrichten:** Die Skills lesen ihre Werte aus dem Block `## Skill-Profil` der `CLAUDE.md` im Projekt-Repo
(Schema: [`docs/skill-profile-v1.md`](./docs/skill-profile-v1.md)). Ein Profil ist nicht Pflicht: Fehlt ein Wert, fragt
der Skill nur nach diesem Wert und schlägt vor, ihn ins Profil zu schreiben. Ein vollständiges Beispiel ist die
[`CLAUDE.md`](./CLAUDE.md) dieses Repos, Configs liegen unter [`.claude/skill-config/`](./.claude/skill-config/).

---

## Source-of-Truth-Hierarchie

| Quelle | Zuständigkeit |
|---|---|
| [`INDEX.md`](./INDEX.md) | Verbindliche Routing- und Invarianten-Regeln |
| `skills/<skill>/SKILL.md` | Operative skill-spezifische Regeln |
| [`docs/skill-quality.md`](./docs/skill-quality.md) | Verbindliche Qualitätsregeln für Skills (Aufbau, Inhalt, Neutralität, Prüfung) |
| [`docs/skill-profile-v1.md`](./docs/skill-profile-v1.md) | Spezifikation des Skill-Profils in der `CLAUDE.md` eines Repos |
| [`MEMORY-RUBRIKEN.md`](./MEMORY-RUBRIKEN.md) | Verbindliche Memory-Rubrik-Konvention |
| [`evals/README.md`](./evals/README.md) | Eval-Methodik und Scoring (manuelle Evals) |
| `README.md` (diese Datei) | Onboarding und Architektur-Überblick |

---

## Zweck dieses Repos

| Zweck | Beschreibung |
|---|---|
| **Versionshistorie** | Jede Skill-Änderung ist ein Git-Commit. Volle Nachvollziehbarkeit von v0.1.0 bis aktuell. Format-Details siehe [`INDEX.md`](./INDEX.md). |
| **Cross-Review** | ChatGPT kann Skills und Review-Runden direkt aus dem Repo lesen. CGR-System archiviert jede Review-Runde in 4 Dateien. |
| **Backup** | Skills gehen nicht verloren wenn der Claude-Projekt-Speicher reset wird. |
| **Portabilität** | Universelle Skills + projektspezifische Werte sind getrennt (`skills/` vs Skill-Profil in der CLAUDE.md des Projekts). Neue Projekte nutzen dasselbe Skill-System, indem sie ihr Profil anlegen ([`docs/skill-profile-v1.md`](./docs/skill-profile-v1.md)). |
| **Meta-Werkzeug** | Die Skills reflektieren über sich selbst: `skill-neu` erstellt neue Skills, `skill-pflege` ändert bestehende, `quality/evals/` misst das Routing-Verhalten, das Skill-Log mit `skill-auswertung` zeigt, wie die Skills im Alltag greifen. |

---

## Verzeichnisstruktur (Überblick)

```
claude-workbench/
├── README.md              ← Dieses File (Onboarding)
├── INDEX.md               ← Verbindliches Routing + globale Invarianten
├── CHANGELOG.md           ← Versionsverlauf
├── CLAUDE.md              ← Skill-Profil dieses Repos (Commit, Checks, Push)
├── LICENSE                ← MIT
├── MEMORY-RUBRIKEN.md     ← Konvention für 4 Memory-Rubriken
├── .claude/skill-config/  ← Configs der Skills für dieses Repo (tracker, review, skill-log)
├── .github/workflows/     ← validate-skills.yml – Prüfskript nach jedem Push
├── .claude-plugin/        ← marketplace.json: Marketplace workbench (Plugins work, skill-workshop)
├── docs/                  ← Konzepte, Regeln, Reviews, Umbau-Plan
├── plugins/               ← Plugin work-hooks (Skill-Log, Skill-Wächter); work ruft dieselben Skripte auf
├── evals/                 ← Manuelle Skill-Routing-Evals (bis v0.20)
├── quality/               ← Eval-Plugin: evals/ (Testfälle für claude plugin eval), skills → ../skills
├── reference/             ← Externe Referenz-Artefakte
├── skills/                ← 15 Skills, je ein Ordner mit SKILL.md
└── tools/                 ← Installation (install.sh/.ps1, einrichten.py), Prüfskript, Auswertung des Skill-Logs
```

Die folgenden Kapitel erklären jeden dieser Ordner und die darin liegenden Dateien.

---

## Kapitel 1 — Die 15 Skills im Überblick

Die Skills sind in drei konzeptionelle Gruppen einteilbar: **Fachskills**, **Meta-Skills** und **Modalitäts-Skills**.

> **Verbindliche Trigger:** [`INDEX.md`](./INDEX.md).
> **Operative Regeln je Skill:** `skills/<skill>/SKILL.md`.
> Dieses Kapitel zeigt nur Zweck und grobe Trigger-Beispiele.

### Fachskills (beantworten "WAS wird gemacht")

| Skill | Aufgabe | Trigger-Beispiele |
|---|---|---|
| **code-erstellen** | Master-Orchestrator für Code-Änderungen (Code-Profil in der CLAUDE.md des Projekts). | "implementiere das Feature", "erstelle DocumentTypeRecognizer.cs", "baue Recovery-Logik ein" |
| **mockup-erstellen** | HTML-UI-Mockups nach Mockup-Profil. | "Mockup für ProfileWizard", "Screen-Design", "UI-Mockup" |
| **doc-pflege** | Erstellt und pflegt Projektdokumentation nach Doku-Profil (BPM: DOC-STANDARD.md). | "pflege die docs", "schreib ein ADR", "neues Konzept für X" |
| **projekt-anlegen** | Neue Projekte anlegen und einrichten: klären, Plan zeigen, Ordner, Git, Skill-Profil, GitHub nach Rückfrage. | "neues Projekt", "ich will X bauen, weiß aber nicht wie", "Repo holen und einrichten" |
| **ticket** | Fehler-Tickets eines Projekts einzeln und immer im selben Ablauf bearbeiten (acht Schritte). | "ticket liste", "ticket HT-0007", "nimm das nächste ticket" |
| **chatgpt-review** | Strukturierte Cross-LLM-Review-Prompts zwischen Claude und ChatGPT. | "besprich das mit ChatGPT", "zweite Meinung", "Folgeprompt für Runde 3" |
| **audit** | Strikt read-only Konsistenzprüfung zwischen Code, Docs, Frontmatter und Quickload. | "audit", "prüfe alles", "konsistenzcheck" |
| **tracker** | Standardisierte Schreibschnittstelle zum ClickUp-Task-System. | "tracker neu: PM — Regex-Bug", "tracker done BPM-042", "tracker suche Regex" |
| **git-commit-helper** | Fertige Git-Commit-Befehle im Format `[vX.Y.Z] Modul, Typ: Kurztitel` (Commit-Profil). | "commit bitte", "commit-message", "PATCH oder MINOR?" |
| **chat-wechsel** | Handover-Prompt für die nächste Claude-Session. | "neuer chat", "nächster chat", "übergabe" |
| **sitzung** | Claude-Code-Gespräche und tmux-Fenster per Auswahlmenü: Projekt → Gespräch → im richtigen Ordner mit Remote Control fortsetzen; Fenster verwalten, nach Neustart wiederherstellen, aufräumen (Skript `scripts/sitzung.py`). | "sitzung", "alte Sitzung öffnen", "Fenster wiederherstellen" |

### Meta-Skills (ändern andere Skills)

| Skill | Aufgabe |
|---|---|
| **skill-neu** | Erstellt neue Skills von Grund auf (projektneutral). |
| **skill-pflege** | Ändert bestehende Skills: Safe Patch oder Refactor mit Regel-Inventar. |
| **skill-auswertung** | Wertet das Skill-Log aus: Zündungen, Fehlausfälle, Konflikte im Alltag; gibt Befunde an Evals, tracker oder skill-pflege weiter. |

### Modalitäts-Skill (beantwortet "WIE wird ausgeführt")

| Skill | Aufgabe |
|---|---|
| **cc-steuerung** | Regelt im Cowork-Chat, wie Claude über Desktop Commander (DC) direkt auf dem PC arbeitet (Dateien, Shell, Arbeitsverzeichnis). Läuft parallel zu Fachskills; in Claude Code nie. |

---

## Kapitel 2 — `skills/` — Die Skill-Dateien

### Struktur pro Skill

```
skills/<skill-name>/
├── SKILL.md              ← Die Skill-Definition (Frontmatter + Body)
└── references/           ← (optional) Progressive Disclosure Details
    ├── <aspekt-1>.md
    └── ...
```

Die Testsätze eines Skills liegen nicht mehr im Skill-Ordner, sondern als Eval-Fälle zentral unter `quality/evals/`
(Kapitel 3); `test-prompts.md` ist eine Altlast (noch bei ticket, entfällt in Umbau-Phase 7).

### Aufbau einer `SKILL.md`

Jede Skill-Datei beginnt mit einem YAML-Frontmatter:

```yaml
---
name: <skill-name>
description: >
  <Zweck-Satz>. Use when <positive Trigger>. Do not trigger for <Ausschlüsse>.
---
```

Der Body enthält je nach Skill: Zweck, Vorrang/Delegation, Kernregeln, Ablauf, Reference-Tabelle (bei Progressive Disclosure), VERBOTEN-Liste.

> **Operative Regelquelle:** Frontmatter-Schema und Body-Struktur sind in [`INDEX.md`](./INDEX.md) und den jeweiligen Skill-Dateien definiert.

### Progressive Disclosure — am Beispiel `tracker`

Der `tracker`-Skill nutzt Progressive Disclosure: Die `SKILL.md` enthält nur Kernregeln und Routing-Tabelle, Details liegen in 14 `references/`-Dateien (anker-system, anti-patterns, batch-protocol, chat-url-handling, clickup-fields, clickup-tools, complete-task, create-task, issue-task, review-workflow, search-and-status, split-and-relations, start-task, update-task). Auch `code-erstellen` hat `references/` (`stacks/`: csharp-wpf, home-assistant-yaml, python, typescript-lit).

> **Operative Regelquelle:** [`skills/tracker/SKILL.md`](./skills/tracker/SKILL.md).

### Two-Place-Pflege

Skills werden an zwei Orten gepflegt: `claude-workbench/skills/<n>/SKILL.md` (Repo) und `/mnt/skills/user/<n>/SKILL.md` (Claude.ai).

> **Operative Regelquelle:** [`skills/skill-pflege/references/delivery.md`](./skills/skill-pflege/references/delivery.md) und [`INDEX.md`](./INDEX.md).

---

## Kapitel 3 — `evals/` — Skill-Routing-Evaluation

Das Eval-System misst, ob ein Skill bei den richtigen Queries triggert und bei den falschen nicht.

### Dateien

| Datei | Inhalt |
|---|---|
| `README.md` | Workflow, Kategorien, Scoring-Schema |
| `_template.md` | Vorlage für neue Skill-Evals |
| `git-commit-helper.md` | Query-Katalog + Run-Log |
| `chatgpt-review.md` | dto. |
| `tracker.md` | dto. |
| `code-erstellen.md` | dto. |
| `phase-5-abschluss-report.md` | Aggregierter Gesamt-Report der Phase-5-Abschluss-Eval |
| `smoke-all-skills.md` | Smoke-Test-Katalog für die 11 Skills bis v0.20 (88 Fälle; ticket fehlt) |
| `methodik-anleitung.md` | Test-Setup-Regeln für Smoke-Läufe (aus dem Lauf vom 28.04.2026) |
| `runs/smoke-2026-04-28-real.md` | Snapshot des manuellen Smoke-Laufs (30 Fälle) |

4 Skills haben detaillierte Evals — die kritischsten aus Phase 1a des Refactors. Die übrigen 8 Skills sind nur im Smoke-Katalog (ticket gar nicht) und werden bedarfsbasiert nachgezogen.

### Neu: automatische Routing-Tests (`quality/evals/`)

Seit Umbau Phase 1 (24.09.2026) gibt es Testfälle für `claude plugin eval` (Manifest `quality/.claude-plugin/plugin.json`,
nur für Tests). 87 Fälle, davon 32 kritisch und 9 aus echten Prompts des Skill-Logs (Tag `real`); Tabelle aller Fälle in
[`quality/README.md`](./quality/README.md). Aufruf und Schwellen: Skill-Profil in [`CLAUDE.md`](./CLAUDE.md) und [`docs/skillsystem-umbau.md`](./docs/skillsystem-umbau.md).
Die mechanische Prüfung aller Skills macht [`tools/validate-skills.ps1`](./tools/validate-skills.ps1), auf Rechnern ohne
PowerShell (HA) nach jedem Push per GitHub Actions.

### Neu: Skill-Log aus dem Alltag (Plugin `work`, Auswertung `tools/skill-log/`)

Hooks in Claude Code schreiben auf jedem Rechner mit, welche Prompts eingegeben wurden und welche Skills darauf
gezündet haben. `skill_log_report.py` zeigt Zündungen je Skill, Runden mit mehreren Skills und Prompts ohne Skill –
Rohstoff für neue Fälle in `quality/evals/`. Ausgewertet wird mit dem Skill skill-auswertung (Config
`.claude/skill-config/skill-log.md`). Format und Einrichtung: [`docs/skill-log-v1.md`](./docs/skill-log-v1.md).

### Neu: Skill-Wächter (Plugin `work`)

Skills zünden auf den Prompt; bei „weiter“ zündet nichts, obwohl Claude danach Code oder Doku ändert. Der Wächter
prüft deshalb an der Aktion (Hooks `PreToolUse`/`PostToolUse`), ob der zuständige Skill geladen ist: blocken oder
warnen nach `plugins/work-hooks/hooks/regeln.json`. Die Regeln lernen über skill-auswertung aus dem Skill-Log. Format und
Einrichtung: [`docs/skill-guard-v1.md`](./docs/skill-guard-v1.md).

### Eval-Methodik

Pro Skill ein Query-Katalog mit Einträgen in 4 Kategorien (`should_trigger`, `should_not_trigger`, `other_skill`, `ambiguous`). Queries sind als `[golden]` (echte BPM-Chat-Formulierung) oder `[synthetic]` (konstruierte Variante) markiert.

> **Operative Regelquelle:** [`evals/README.md`](./evals/README.md).
> Dieses Kapitel zeigt nur die Ordnerstruktur.

### Phase-5-Abschluss-Report

Der Report in `phase-5-abschluss-report.md` aggregiert die 4 Eval-Durchläufe. Gesamtergebnis Phase 5: Blind-Modus 73/76, Vollmodus 75/76.

---

## Kapitel 4 — Projektwerte

Die Skills sind projekt-agnostisch. Projektwerte (Pfade, Präfixe, ClickUp-IDs, Befehle) stehen nicht in diesem Repo,
sondern im Projekt-Repo: im Block `## Skill-Profil` der `CLAUDE.md`, große Strukturen unter `.claude/skill-config/`
(z. B. `tracker.md`). Der frühere Ordner `projects/<projekt>/` ist seit 07.10.2026 aufgelöst; seine Werte liegen in den
Projekt-Repos.

| Ort | Beispiele |
|---|---|
| `skills/<skill>/` | Universelle Kernregeln, Ablauf-Schritte, Trigger-Phrasen, VERBOTEN-Listen |
| Skill-Profil und `.claude/skill-config/` im Projekt-Repo | ClickUp-IDs, Custom-Field-IDs, Modul-Kürzel, Repo-Pfade, projekt-spezifische Konventionen |

> **Operative Regelquelle:** [`docs/skill-profile-v1.md`](./docs/skill-profile-v1.md) (Skill-Profil v1: welche Werte wohin gehören und wie ein Skill sie findet).

---

## Kapitel 5 — `docs/` — Konzepte, Regeln, Reviews

| Datei | Inhalt |
|---|---|
| `chat-anker-konzept.md` | Draft v2 des Chat-Anker-Systems |
| `chatgpt-reviews/` | CGR-Archiv dieses Repos (Serien `CGR-2026-09-23-ha-grundsatz`, `CGR-2026-09-24-skillsystem`) mit `INDEX.md` |
| `fragilitaeten-und-fruehwarn.md` | 4 Fragilitäten mit Frühwarn-Indikatoren (INDEX-Invariante 10) |
| `ha-grundsatz/` | HA-Grundsatzregeln für Home-Assistant-Projekte (im Aufbau, genutzt von `projekt-anlegen`; G-22 Oberfläche mit Lit) |
| `skill-guard-v1.md` | Skill-Wächter: Hooks, die an der Aktion prüfen, ob der zuständige Skill geladen ist; lernbare Regeln |
| `skill-log-v1.md` | Format, Einrichtung und Auswertung des Skill-Logs |
| `skill-profile-v1.md` | Spezifikation Skill-Profil v1 (Abschnitt `## Skill-Profil` in der CLAUDE.md, Configs unter `.claude/skill-config/`) |
| `skill-quality.md` | Verbindliche Qualitätsregeln für Skills |
| `skill-refactor-phases.md` | Arbeitsnahe Referenz der 5 Refactor-Phasen (April 2026) |
| `skill-refactors/` | Regel-Inventare der Skill-Refactors (`<Datum>-<skill>.md`, skill-pflege Modus Refactor) |
| `skillsystem-umbau.md` | Umbau-Plan Phasen 1–7 (seit 24.09.2026) |

---

## Kapitel 6 — `reference/` — Externe Referenz-Artefakte

Enthält Artefakte **anderer Projekte oder Quellen**, die als Referenz dienen. Wird **nicht modifiziert**.

| Verzeichnis | Inhalt |
|---|---|
| `reference/anthropic-skill-creator/` | Anthropic's offizieller `skill-creator` als Vergleichsobjekt |

---

## Kapitel 7 — Top-Level-Dokumente

### `INDEX.md` — Routing und globale Invarianten

Die **verbindliche Regelquelle** des Skill-Systems. Enthält Skill-Übersicht, Trigger-Matrix, Skill-Hierarchie und gemeinsame Invarianten über alle Skills.

### `CHANGELOG.md` — Versionsverlauf

Umgekehrt chronologisch, pro Versionstag ein Eintrag mit 2-4 Zeilen Beschreibung. Seit 24.09.2026 gibt es eine neue
Nummer nur bei Skill-Änderungen (Versionsregel oben in der Datei).

### `CLAUDE.md` — Skill-Profil dieses Repos

Regeln für die Arbeit in diesem Repo mit Claude Code: Commit-Format und Module, Prüfungen vor dem Commit
(`skill-validation`, `routing-eval`), Versionsquelle, Push nach jedem Commit, Verweise auf die Configs unter
`.claude/skill-config/`.

### `MEMORY-RUBRIKEN.md` — Memory-Konvention

Definiert die 4 Rubriken-Prefixe für Memory-Einträge: `[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]`, `[REVIEW-PENDING]`.

> **Operative Regelquelle:** [`MEMORY-RUBRIKEN.md`](./MEMORY-RUBRIKEN.md).
> README enthält nur eine Kurzbeschreibung.

---

## Kapitel 8 — Refactor-Historie

Das Skill-System wurde zwischen v0.1.0 (2026-04-21) und v0.17.7 (2026-04-24) in 5 Phasen systematisch refactored. Die Phasen-Nummerierung stammt aus dem ChatGPT-Review Runde 4 (`CGR-2026-04-skillsystem-r4`).

| Phase | Inhalt |
|---|---|
| **Phase 1** | Sofort-Fixes — Trigger-Bereinigung an 4 kritischen Skills |
| **Phase 1a** | Eval-Baseline — Verzeichnis, Query-Dateien pro Skill, Baseline-Scores im Blind-Modus |
| **Phase 2** | Description-Schema-Refactor — alle 9 Skills auf einheitliches Schema |
| **Phase 3** | Body-Refactor + Progressive Disclosure — Delegations-Blöcke, `tracker` mit references/, neuer `skill-neu` |
| **Phase 4** | Memory-Integration + CGR-System — 4 Memory-Rubriken, Cross-Review-Archivierung |
| **Phase 5** | Konfliktpaare + Abschluss-Eval — symmetrische Delegations-Tabellen für 7 Konfliktpaare |

> **Detail-Quelle:** [`CHANGELOG.md`](./CHANGELOG.md) für Versionseinträge, [`docs/skill-refactor-phases.md`](./docs/skill-refactor-phases.md) für die arbeitsnahe Phasen-Referenz.

---

## Kapitel 9 — Workflow-Konventionen

Workflow-Konventionen (Branch-Ermittlung, `ask_user_input_v0`-Disziplin, Two-Place-Pflege, Commit-Format, Frühphasen-Prinzip, Skill-Änderungen ohne stillen Regelverlust, DC-Pfade, Chat-Anker) sind in den verbindlichen Regelquellen definiert — nicht in dieser README.

> **Verbindliche Regelquelle:** [`INDEX.md`](./INDEX.md) für globale Invarianten.
> **Operative Skill-Regeln:** jeweilige `skills/<skill>/SKILL.md`.
> **Memory-Konvention:** [`MEMORY-RUBRIKEN.md`](./MEMORY-RUBRIKEN.md).

---

## Kapitel 10 — Abgrenzung zu öffentlichen Skill-Repos

Bis v0.23 waren diese Skills **BPM-spezifisch** (BPM-Docs, ClickUp-IDs, Commit-Format, Herberts 3-PC-Setup,
CGR-Archiv im BPM-Repo). Seit v0.24 (16.09.2026) sind sie projektneutral; sie bleiben aber auf Herberts Arbeitsweise
zugeschnitten:

- Workflow-Regeln (Commit-Format `[vX.Y.Z] Modul, Typ: Kurztitel`, Ein-Task-Ein-Commit, Pro-Task-Quittung)
- ClickUp als Aufgaben-System (Werte je Projekt aus der Tracker-Config des Projekt-Repos)
- Herberts Rechner (Büro-PC auf D:, Surface auf C:, Standrechner) und der Home Assistant (Raspberry Pi), auf dem
  Claude Code als Hauptumgebung läuft
- CGR-Archivierung der ChatGPT-Reviews im jeweiligen Repo

Für **generische** Skills (TDD, Debugging, Refactoring, allgemeine Code-Patterns) empfehlen sich öffentliche Repos:

- [obra/superpowers](https://github.com/obra/superpowers) — Workflow-Skills
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) — 235+ Engineering- und Marketing-Skills
- [anthropic/skill-creator](https://docs.claude.com/) — Anthropic-Referenz (eingebettet in `reference/anthropic-skill-creator/`)

---

## Kapitel 11 — Weiterarbeit und Wartung

### Skills ändern

Über den `skill-pflege`-Skill – Safe Patch für gezielte Änderungen oder Refactor mit Regel-Inventar unter `docs/skill-refactors/`; danach Prüfskript, Routing-Eval und Lieferung zum Upload bei claude.ai (Two-Place-Pflege).

> **Operative Regelquelle:** [`skills/skill-pflege/SKILL.md`](./skills/skill-pflege/SKILL.md).

### Neuen Skill anlegen

Über den `skill-neu`-Skill — Absicht klären, Kollisionsprüfung, Description, Neutralität, mindestens drei Eval-Fälle unter `quality/evals/`, Prüfskript und Routing-Eval, dann Commit und Lieferung zum Upload bei claude.ai.

> **Operative Regelquelle:** [`skills/skill-neu/SKILL.md`](./skills/skill-neu/SKILL.md).

### Prüfen und Eval-Runs

Vor jedem Commit an Skills: `pwsh -NoProfile -File tools/validate-skills.ps1` (mechanische Prüfung); auf dem HA ohne
PowerShell läuft sie nach jedem Push per GitHub Actions (`gh run list`). Nach Änderungen an
einer description und vor dem Hochladen: die betroffenen Fälle mit `claude plugin eval` (Befehl im Skill-Profil der
[`CLAUDE.md`](./CLAUDE.md)). Die manuellen Evals unter `evals/` bleiben als Archiv.

> **Operative Regelquelle:** [`docs/skill-quality.md`](./docs/skill-quality.md) und [`docs/skillsystem-umbau.md`](./docs/skillsystem-umbau.md); für die manuellen Evals [`evals/README.md`](./evals/README.md).

### Memory pflegen

Die 4 Rubriken werden automatisch beim Handover gescannt. Einträge werden nie stillschweigend entfernt.

> **Operative Regelquelle:** [`MEMORY-RUBRIKEN.md`](./MEMORY-RUBRIKEN.md).

### Projekt-Config erweitern

Wenn weitere Skills projekt-spezifische Daten brauchen: nach Skill-Profil v1 als Feld im `## Skill-Profil` der
CLAUDE.md des Projekts oder als Config unter `.claude/skill-config/`.

> **Operative Regelquelle:** [`docs/skill-profile-v1.md`](./docs/skill-profile-v1.md).

---

## Kapitel 12 — Schnellreferenz: Datei-Inventar

```
claude-workbench/
├── README.md                              ← dieses File (Onboarding)
├── INDEX.md                               ← Routing + globale Invarianten (verbindlich)
├── CHANGELOG.md                           ← Versionseinträge
├── CLAUDE.md                              ← Skill-Profil dieses Repos
├── LICENSE                                ← MIT (reference/ unter Apache-2.0)
├── MEMORY-RUBRIKEN.md                     ← Memory-Konvention (4 Rubriken)
├── .gitignore
│
├── .claude/skill-config/
│   ├── review.md                          ← Config für chatgpt-review
│   ├── skill-log.md                       ← Config für skill-auswertung (Log-Ordner, ausgewertet bis)
│   └── tracker.md                         ← Config für tracker (Space Claude Skills Entwicklung)
│
├── .github/workflows/
│   └── validate-skills.yml                ← Prüfskript nach jedem Push
│
├── .claude-plugin/
│   └── marketplace.json                   ← Marketplace workbench: Plugins work und skill-workshop (strict: false,
│                                            Skills aus skills/, Hooks direkt im Eintrag)
│
├── docs/
│   ├── chat-anker-konzept.md
│   ├── chatgpt-reviews/                   ← CGR-Archiv + INDEX.md
│   ├── fragilitaeten-und-fruehwarn.md
│   ├── installation.md                    ← Installation: Ablauf, Updates, Entfernen, Fehlerquellen
│   ├── ha-grundsatz/
│   ├── skill-guard-v1.md                  ← Skill-Wächter
│   ├── skill-log-v1.md                    ← Skill-Log
│   ├── skill-profile-v1.md
│   ├── skill-quality.md
│   ├── skill-refactor-phases.md
│   ├── skill-refactors/                   ← Regel-Inventare der Refactors
│   └── skillsystem-umbau.md
│
├── evals/
│   ├── README.md                          ← Eval-Methodik + Scoring
│   ├── _template.md
│   ├── git-commit-helper.md
│   ├── chatgpt-review.md
│   ├── tracker.md
│   ├── code-erstellen.md
│   ├── methodik-anleitung.md
│   ├── phase-5-abschluss-report.md
│   ├── smoke-all-skills.md
│   └── runs/
│
├── plugins/
│   └── work-hooks/                        ← Plugin nur mit Hooks: .claude-plugin/plugin.json; hooks/: hooks.json,
│                                            skill_log.py, skill_guard.py, regeln.json, Test des Wächters
│
├── quality/                               ← für claude plugin eval selbst ein Plugin
│   ├── .claude-plugin/plugin.json         ← Eval-Manifest (experimental.evals: evals)
│   ├── skills → ../skills                 ← Symlink, damit die Evals die Skills laden
│   ├── README.md                          ← Regeln und Tabelle aller Fälle
│   └── evals/                             ← 87 Fälle (prompt.md + graders/), 9 aus echten Prompts
│
├── reference/
│   └── anthropic-skill-creator/
│
├── skills/
│   ├── audit/SKILL.md
│   ├── cc-steuerung/
│   │   ├── SKILL.md
│   │   └── references/desktop-commander.md
│   ├── chat-wechsel/                      ← SKILL.md + references/ (prompt-struktur, tracker-abgleich, cowork, neues-fenster)
│   ├── chatgpt-review/SKILL.md
│   ├── code-erstellen/
│   │   ├── SKILL.md
│   │   └── references/stacks/
│   ├── doc-pflege/SKILL.md
│   ├── git-commit-helper/SKILL.md
│   ├── mockup-erstellen/SKILL.md
│   ├── projekt-anlegen/                   ← SKILL.md + references/ (github, stacks/home-assistant)
│   ├── sitzung/                           ← SKILL.md + references/ (befehle, umgebung) + scripts/sitzung.py
│   ├── skill-auswertung/SKILL.md
│   ├── skill-neu/                         ← SKILL.md + references/ (cowork)
│   ├── skill-pflege/                      ← SKILL.md + references/ (rule-inventory, delivery)
│   ├── ticket/                            ← SKILL.md + test-prompts.md
│   └── tracker/
│       ├── SKILL.md
│       ├── references/
│       └── references.zip                 ← entfällt in Umbau Phase 7
│
└── tools/
    ├── install.sh, install.ps1            ← Installation: Voraussetzungen, Marketplace, dann einrichten.py
    ├── einrichten.py, test_einrichten.py  ← Plugins, Optionen, autoUpdate, skillOverrides, Probe der Hooks
    ├── commands/statistik.md              ← Befehl /statistik des Plugins work
    ├── skill-log/                         ← skill_log_report.py (Bericht), dashboard.py (Dashboard), Tests
    └── validate-skills.ps1                ← Prüfskript (PowerShell 7)
```

---

## Lizenz

MIT, siehe [LICENSE](./LICENSE) (© 2026 Herbert Schrotter). Ausgenommen ist das Anthropic-Referenzmaterial unter
`reference/anthropic-skill-creator/`: Es steht unter Apache-2.0 (dortige `LICENSE.txt`).
