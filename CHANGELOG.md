# CHANGELOG

Alle relevanten Änderungen an den Skills werden hier dokumentiert.

Format: Umgekehrte Chronologie (neueste zuerst).

## 2026-04-21 - Initial Commit

Erste Version des Repos mit allen 10 bestehenden Skills aus dem Claude-Projekt.

### Enthalten
- audit (193 Zeilen)
- cc-steuerung (271 Zeilen)
- chat-wechsel (307 Zeilen)
- chatgpt-review (238 Zeilen) - Frühphasen-Hinweis-Block integriert
- code-erstellen (326 Zeilen) - Frühphasen-Prinzip + Migrations-Blocking
- doc-pflege (321 Zeilen) - Frühphasen-Regel für Schema-/DB-Doku
- git-commit-helper (105 Zeilen)
- mockup-erstellen (235 Zeilen)
- skill-pflege (299 Zeilen)
- tracker (911 Zeilen)

### Entscheidungen
- Separate Repo statt Unterordner im BPM-Repo (bessere Trennung, eigene Historie)
- Struktur folgt Anthropic-Standard (`skills/<n>/SKILL.md`)
- Sync: Skills werden in zwei Orten gepflegt (`/mnt/skills/user/` + `claude-skills-bpm/skills/`)
