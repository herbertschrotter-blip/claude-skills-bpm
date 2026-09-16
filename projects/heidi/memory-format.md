# Heidi — Projektkennung und Memory

Der Skill `tracker` braucht zu Beginn nur eines: den Namen des aktiven Projekts, um
`projects/<name>/` zu lesen. Wo der Name steht, hängt von der Umgebung ab.

---

## Claude Code (Standard für dieses Projekt)

Kein Memory-Eintrag. Die Kennung steht in der `CLAUDE.md` des Projekt-Repos:

```
## Tracker-Profil
- Projekt: heidi
- Skill-Repo (OneDrive-relativ): Dokumente\02 Arbeit\05 Vorlagen - Scripte\00_claude-skills-bpm
- Projekt-Config: projects/heidi/
- ClickUp: Space Smart Home 1200660000001609, Liste dreame_x60 – Bauplan 1200660000004100
- Nummernschema: DX-NNN | KÜRZEL | Titel, Next: DX-063
```

Claude Code liest die CLAUDE.md automatisch beim Start; damit ist das Projekt bekannt, ohne
dass etwas gesucht oder gefragt werden muss.

---

## Cowork-Chat (claude.ai)

Wie bei BPM ein Memory-Eintrag `[PROJECT]`:

```
[PROJECT] heidi | Skill-Repo-Pfad (OneDrive-relativ): Dokumente\02 Arbeit\05 Vorlagen - Scripte\00_claude-skills-bpm | Projekt-Config: projects/heidi/ | Repo: https://github.com/herbertschrotter-blip/herbert-smarthome | Aktive Spaces: SmartHome=1200660000001609
```

Kein `[CLICKUP]`-Eintrag nötig (eine Liste, keine Nummernvergabe), kein `[ANKER-LIVE]`
(keine Chat-Anker in diesem Projekt).

---

## Rubriken

Die Memory-Rubriken `[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]`, `[REVIEW-PENDING]` gelten
unverändert (siehe `MEMORY-RUBRIKEN.md` im Skill-Repo). In Claude Code entsprechen sie
Einträgen im Projekt-Gedächtnis; offene Punkte des Baus stehen zusätzlich in
`docs/HANDOFF.md` und im Bauplan Abschnitt 10.
