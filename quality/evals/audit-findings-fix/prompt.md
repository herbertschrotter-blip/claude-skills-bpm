---
description: "Audit-Befunde beheben – doc-pflege soll auslösen, audit nicht."
tags: [baseline, routing, critical, audit, doc-pflege]
runs: 3
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---

Das Audit hat ergeben, dass die Kapitel 3 und 5 der Architektur-Doku noch den alten Import-Ablauf beschreiben. Bring die
beiden Kapitel auf den neuen Stand.
