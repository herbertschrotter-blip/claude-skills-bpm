# BPM — Projekt-spezifische Config

Dieser Ordner enthält alle BPM-spezifischen Daten für das Skill-System.

**Projekt:** BauProjektManager (BPM) — WPF Desktop-Anwendung für
Bau-Projektmanagement, .NET 10, SQLite, offline-first.

**BPM-Repo:** `github.com/herbertschrotter-blip/BauProjektManager`

**Memory-Eintrag:** `[PROJECT] bpm | ...` (Source of Truth für aktives Projekt)

---

## Dateien

| Datei | Inhalt |
|---|---|
| `clickup-lists.md` | Listen-IDs beider Spaces (BPM + Claude Skills Entwicklung), Scope-Erkennungs-Regeln |
| `clickup-fields.md` | BPM-Custom-Field-IDs, Dropdown-Option-IDs, Modul-Kürzel-Tabelle, Status-Werte pro Listen-Typ |
| `memory-format.md` | Alle BPM-Memory-Eintragsformate: `[PROJECT]`, `[CLICKUP]`, `[ANKER-LIVE]` |

---

## Wer liest diesen Ordner

Primär der `tracker`-Skill. Wenn weitere Skills (code-erstellen, doc-pflege,
git-commit-helper etc.) auf die neue Struktur umgezogen werden, kommen sie
hier dazu.

---

## Allgemeine Projekt-Architektur

Siehe `docs/project-architecture.md` im Skill-Repo.
