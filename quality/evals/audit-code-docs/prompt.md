---
description: "Doku gegen Code prüfen, nur lesen – audit soll auslösen, doc-pflege und code-erstellen nicht."
tags: [baseline, routing, critical, audit, code-erstellen, doc-pflege]
runs: 3
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---

Prüf bitte, ob die Doku zum Import-Modul noch zum Code passt. Nur prüfen, nichts ändern – ich will eine Liste der Abweichungen.
