---
description: "Allgemeines Code-Review ohne Doku-Bezug – audit darf nicht auslösen."
tags: [baseline, routing, audit]
runs: 3
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---

Schau dir diese Funktion an und sag mir, ob sie einen Fehler hat:

```python
def teile(a, b):
    return a / b
```
