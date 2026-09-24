---
description: "Refactoring von Anwendungscode – code-erstellen soll auslösen."
tags: [baseline, routing, code-erstellen]
runs: 3
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---

Refaktoriere den PlanParser: Die drei fast gleichen Parse-Methoden sollen eine gemeinsame Hilfsmethode nutzen.
