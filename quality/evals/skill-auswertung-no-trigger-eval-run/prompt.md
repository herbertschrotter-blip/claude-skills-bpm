---
description: "Künstliche Eval-Läufe – skill-auswertung darf nicht auslösen."
tags: [routing, skill-auswertung, skill-neu, skill-pflege]
runs: 3
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---

Lass die Routing-Tests mit claude plugin eval für den tracker-Skill laufen, drei Durchläufe je Fall.
