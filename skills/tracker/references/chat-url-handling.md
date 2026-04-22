# Chat-URL-Ermittlung (zentrale Hilfsmethode)

Referenz für tracker-Operationen die Chat-URLs in Custom Fields setzen.

---

## Grundsatz

**Chat erstellt** = Chat, wo das Feature **inhaltlich ausgearbeitet** wurde (Konzept-Chat, Backlog-Aufnahme, Implementierungsplanung).

**Chat erledigt** = Chat, wo der **Code-Commit** gemacht wurde.

Beides ist NICHT zwangsläufig der Chat wo der ClickUp-Task angelegt oder geschlossen wird.

---

## Aktuellen Chat ermitteln

Der **gerade laufende Chat** ist meist nicht zuverlässig per `recent_chats` abrufbar (Indexierungs-Verzögerung). Strategie:

1. **Primary:** User fragt am Chat-Start einmalig (oder proaktiv):
   ```
   "Ich brauche die URL dieses Chats — kopier sie mir bitte aus der Browser-Adressleiste."
   ```
   Die URL wird für diese Session gemerkt und bei jedem tracker-Call verwendet.

2. **Secondary:** `recent_chats(n: 1, sort_order: "desc")` aufrufen — wenn der oberste Eintrag inhaltlich zum aktuellen Chat passt, verwenden. Sonst User fragen.

3. **Bei `chat-wechsel`-Skill:** Die aktuelle URL wird in den Übergabe-Prompt geschrieben, damit sie im nächsten Chat verfügbar ist.

---

## Chat für einen Commit finden

Gegeben: Commit-Hash + Commit-Datum/-Zeit (aus `git log`).

Ablauf:
```
1. Datum-Zeitpunkt des Commits notieren (ISO-Zeitstempel)
2. recent_chats(after: commit_time - 4h, before: commit_time + 4h, n: 10, sort_order: "asc")
3. Durch Ergebnisse gehen und prüfen ob der Chat inhaltlich zum Commit passt
   (Feature-Name, Dateinamen, Diskussionsthema im Chat-Content)
4. Besten Match auswählen
5. Bei Unsicherheit: ask_user_input_v0 mit Kandidaten als Optionen
```

---

## Chat wo Feature ausgearbeitet wurde

Gegeben: Feature-Name oder Task-Beschreibung.

Ablauf:
```
1. conversation_search(query: "<feature-name> <kernkonzept>", max_results: 10)
2. Sortieren nach updated_at aufsteigend (ältester zuerst)
3. Durchgehen und den Chat finden wo das Feature zum ersten Mal KONKRET geplant/ausgearbeitet wurde
   - Nicht nur erwähnt, sondern als Implementierungsschritt, ADR, Backlog-Eintrag, Konzept-Diskussion
4. Bei mehreren Kandidaten: ask_user_input_v0 mit Chat-Titeln als Optionen
```

---

## Fallback

Wenn der Chat nicht ermittelbar ist: `ask_user_input_v0`
Optionen: Manuell URL eingeben, Feld leer lassen, Abbrechen

---

## Chat-Start: Automatischer Kontext

Bei `[CLICKUP]` in Memory → kompakte Zusammenfassung:
```
📋 ClickUp: 12 offene V1-Tasks, 4 davon high
   Höchste Prio: BPM-001 | PM | DB-Anbindung Orchestrator [high] [v1] [M]
```

**Zusätzlich:** Proaktiv nach aktueller Chat-URL fragen (Prosa, weil offene Frage):
```
"Falls du mit tracker arbeiten willst — kopier mir bitte einmal die URL
dieses Chats aus der Adressleiste. Sonst kann ich Chat erstellt/erledigt
nicht automatisch füllen."
```

Wenn User ignoriert: Nicht nerven, aber bei erstem tracker-Call fragen.

