---
description: "Bauplan-Check nur lesend – audit soll auslösen, doc-pflege nicht."
tags: [baseline, routing, critical, audit, doc-pflege]
runs: 3
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---

Mach einen Bauplan-Check: Stimmen Statusliste und Entitäts-Vertrag noch mit dem Code überein? Nur prüfen.
