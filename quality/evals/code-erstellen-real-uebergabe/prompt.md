---
description: "Echter Fehlausfall aus dem Skill-Log: eingefügte Übergabe mit Arbeitsauftrag – code-erstellen soll auslösen, chat-wechsel nicht."
tags: [routing, real, code-erstellen, chat-wechsel]
runs: 3
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---

# Baustrom-Integration Teil 3

Weiterführung aus Teil 2. Stand: Version 0.8.40 läuft, alle Tests grün.

## Offene Punkte
1. Berechtigungen: Auf der Seite dürfen nur Admins Einstellungen ändern; die Prüfung kommt in die Websocket-Befehle der Integration und als Sperre in die Oberfläche.
2. Ticket WU-0018: Das Thermostat sitzt nicht mittig.

Nimm dir die Punkte der Reihe nach vor und fang mit Punkt 1 an.
