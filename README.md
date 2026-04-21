# claude-skills-bpm

Claude-Skills für das BauProjektManager (BPM) Projekt von Herbert Schrotter.

Diese Skills sind **projektspezifisch für BPM** optimiert — sie kennen die BPM-Docs, -Konventionen, ClickUp-IDs und Workflow-Regeln. Sie sind **nicht** als allgemeine Community-Skills gedacht (dafür siehe z.B. [obra/superpowers](https://github.com/obra/superpowers) oder [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)).

## Zweck dieses Repos

1. **Versionshistorie** — Jede Skill-Änderung ist ein Git-Commit mit Kontext
2. **Cross-Review** — ChatGPT kann Skills direkt aus dem Repo lesen
3. **Backup** — Skills gehen nicht verloren wenn Claude-Projekt-Speicher reset
4. **Portabilität** — Skills können später für andere Projekte adaptiert werden

## Struktur

```
claude-skills-bpm/
├── README.md           ← Dieses File
├── INDEX.md            ← Skill-Übersicht + Trigger-Matrix
├── CHANGELOG.md        ← Skill-Versionsverlauf
└── skills/
    ├── audit/SKILL.md
    ├── cc-steuerung/SKILL.md
    ├── chat-wechsel/SKILL.md
    ├── chatgpt-review/SKILL.md
    ├── code-erstellen/SKILL.md
    ├── doc-pflege/SKILL.md
    ├── git-commit-helper/SKILL.md
    ├── mockup-erstellen/SKILL.md
    ├── skill-pflege/SKILL.md
    └── tracker/SKILL.md
```
