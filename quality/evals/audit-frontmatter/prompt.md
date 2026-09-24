---
description: "Frontmatter-Prüfung nur lesend – audit soll auslösen, doc-pflege nicht (beide Descriptions nennen Frontmatter)."
tags: [baseline, routing, critical, audit, doc-pflege]
runs: 3
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---

Validiere bitte Frontmatter und Quickloads aller Docs. Nur lesen und die Befunde auflisten, nichts korrigieren.
