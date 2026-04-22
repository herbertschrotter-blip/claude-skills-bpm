---
name: tracker
description: >
  Führt konkrete ClickUp-Aktionen für BPM-Tasks aus, z.B. "tracker neu",
  "tracker done", "tracker update", "tracker status", "tracker suche",
  "tracker next", "tracker split", "tracker relate" und "tracker field".
  Use when users want an explicit BPM task action in ClickUp. Do not trigger
  for general talk about priorities, open points, brainstorming, notes, or
  free-form project planning without a concrete tracker command.
---

# Tracker Skill — ClickUp Offene-Punkte-Verwaltung

## Zweck

Einzige standardisierte Schreibschnittstelle für den ClickUp-Task-Tracker.
Pro Modul eine eigene Liste. Neue Module bekommen automatisch eine neue Liste.
Globale Nummerierung BPM-001, BPM-002, ... über alle Listen hinweg.

Die operativen Details sind in `references/` ausgelagert. Diese Hauptdatei
ist nur der Routing-Einstieg — je nach Kommando die passende Referenz laden.

---

## 🚨 Kernregel: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0`
verwendet werden — KEINE Prosa-Fragen.**

Mehrere Fragen in einem Aufruf sind erlaubt (max 3). Zu lange Options-Listen
(>4) in Multi-Aufrufe aufteilen.

VERBOTEN:
- "Welche Variante willst du? A oder B?" als Prosa
- "Soll ich X oder Y machen?" als Prosa
- Eine Liste von Optionen im Chat aufzählen und dann auf Tipp-Antwort warten

Prosa-Fragen NUR wenn:
- Offene Frage ohne feste Optionen (z.B. "Welche Datei ist betroffen?")
- User hat gerade eine klare Präferenz signalisiert
- Freitext-Input nötig

---

## 🚨 Kernregel: Pro-Task-Quittung (Format-Zwang)

Nach **jedem** `clickup_create_task` oder status-änderndem `clickup_update_task`
MUSS im selben Antwort-Block eine Quittungszeile stehen:

```
✅ <BPM-ID oder Issue-ID> — [BPM-ANCHOR-<task-id>] — <typ>: <kurz>
```

Die Quittung ist Bestätigung + Body-Anker + Audit-Spur in einem Format.
Keine Quittung am Ende gesammelt. Keine Tabellen statt Quittungen.

**Zusätzlich im selben Tool-Call-Block:** Custom Field `Chat-Anker erstellt`
(`512b8920-...`) bzw. `Chat-Anker erledigt` (`0c72a2ea-...`) setzen — nicht
später nachtragen.

Bei ≥2 Task-Operationen in derselben Antwort greift das **Batch-Protokoll**:
Batch-Ansage vor Beginn, Pro-Task-Zyklus, Batch-Audit am Ende.
Vollständige Spec: `references/batch-protocol.md`.

Adressiert `tracker-001` + `tracker-004`.

---

## Routing: Kommando → Reference-Datei

| Kommando | Reference |
|----------|-----------|
| `tracker neu: <Beschreibung>` | `references/create-task.md` |
| `tracker start: <BPM-NNN>` | `references/start-task.md` |
| `tracker done: <BPM-NNN>` | `references/complete-task.md` |
| `tracker update: <BPM-NNN> → <Änderung>` | `references/update-task.md` |
| `tracker field: <BPM-NNN> <Feld> <Wert>` | `references/update-task.md` |
| `tracker status` | `references/search-and-status.md` |
| `tracker next` | `references/search-and-status.md` |
| `tracker suche: <Stichwort>` | `references/search-and-status.md` |
| `tracker listen` | `references/search-and-status.md` |
| `tracker split: <BPM-NNN>` | `references/split-and-relations.md` |
| `tracker relate: <A> <Bez> <B>` | `references/split-and-relations.md` |
| `anker setzen: <text>` | `references/anker-system.md` |
| ≥2 Task-Operationen in einer Antwort | `references/batch-protocol.md` |

---

## Querverweis: was steht in welcher Reference

| Reference | Inhalt |
|-----------|--------|
| `clickup-fields.md` | 10 Custom Fields mit IDs + Option-IDs, Modul-Kürzel, Listen-IDs, BPM-Nummerierung, Titel-Format, Meilensteine, Priority, Status, Memory-Pflege |
| `anker-system.md` | Chat-Anker Master-Spec: Format, `[ANKER-LIVE]` Registry, Lifecycle, TEMP-ID-Generierung, `anker setzen`, Stale-Check |
| `batch-protocol.md` | Pro-Task-Quittung + Batch-Ansage + Batch-Audit + Subtask/Parent-Regeln. Gilt immer wenn ≥2 Task-Operationen in einer Antwort |
| `chat-url-handling.md` | Chat erstellt/erledigt ermitteln, Chat-Start Kontext, recent_chats/conversation_search |
| `create-task.md` | `tracker neu` Ablauf, Description-Template, Beispiel-Workflow |
| `start-task.md` | `tracker start` Ablauf, Parent-Kaskade, implizite Trigger mit Task-ID, Status-Werte pro Listen-Typ |
| `complete-task.md` | `tracker done` Ablauf, Git-Commit-Ermittlung, Status-Werte, Beispiel-Workflow |
| `update-task.md` | `tracker update` + `tracker field` |
| `search-and-status.md` | `tracker status`, `next`, `suche`, `listen` |
| `split-and-relations.md` | Unteraufgaben-Regeln, `tracker split`, `tracker relate`, Dependency-Typen |
| `anti-patterns.md` | Automationspolitik, Integration mit anderen Skills, VERBOTEN-Liste |

---

## ClickUp-Konfiguration (aus Memory)

Aus Memory lesen: `[CLICKUP]` Eintrag enthält Space-ID, Listen-IDs und nächste freie Nummer.

Format:
```
[CLICKUP] Space:<ID> | Listen: <Modul>:<ListID>, ... | Next:<NNN> | Letzte Sync: Teil <N>
```

Details zu Listen-IDs + Modul-Kürzeln in `references/clickup-fields.md`.

---

## Chat-Start: Automatischer Kontext

Bei `[CLICKUP]` in Memory → kompakte Zusammenfassung:
```
📋 ClickUp: 12 offene V1-Tasks, 4 davon high
   Höchste Prio: BPM-001 | PM | DB-Anbindung Orchestrator [high] [v1] [M]
```

**Zusätzlich:** Proaktiv nach aktueller Chat-URL fragen (Prosa, weil offene Frage).
Wenn User ignoriert: Nicht nerven, aber bei erstem tracker-Call fragen.

**Stale-Check für `[ANKER-LIVE]`:** Einmal am Chat-Start prüfen ob Anker älter als 24h sind.
Details in `references/anker-system.md`.

---

## Notizen vs. Tasks (Trigger-Disambiguierung)

| Trigger | Aktion |
|---------|--------|
| "neue aufgabe", "neuer punkt", "tracker neu" | → Task in ClickUp |
| "merk dir", "remember" | → Memory (KEIN ClickUp) |
| "notiz", "nicht vergessen" | → `ask_user_input_v0`: Task, Notiz, Beides |

---

## Automationspolitik (Kurzform)

**Goldene Regel:** Explizit → direkt. Alles andere → ask_user_input_v0 (keine Prosa!).

Vollständige Tabelle in `references/anti-patterns.md`.

---

## Integration mit anderen Skills

- **code-erstellen** nach Commit: `ask_user_input_v0` "Passt zu BPM-XXX. `tracker done`?"
- **chat-wechsel** am Ende: Batch-Abschluss + Chat-URL in Übergabeprompt
- **doc-pflege** nach Doc-Update: `ask_user_input_v0` "Doc-Task BPM-XXX erledigt?"

Details in `references/anti-patterns.md`.

---

## Kern-VERBOTEN (Kurzliste)

- Tasks automatisch erstellen aus freiem Chattext
- Tasks automatisch auf Done setzen ohne Trigger
- Titel ohne BPM-Nummer oder Kürzel (Hauptaufgaben)
- BPM-Nummern an Unteraufgaben vergeben
- **Prosa-Fragen bei festen Entscheidungsoptionen** — IMMER ask_user_input_v0
- Status mit Grossbuchstaben setzen — IMMER klein (`open`/`in progress`/`done`)
- Custom Field Option-IDs raten — immer aus `references/clickup-fields.md` kopieren
- Chat-URLs raten oder erfinden — bei Unsicherheit ask_user_input_v0 oder leer lassen
- **Pro-Task-Quittung weglassen** nach `create`/`update` — Format-Zwang ist Pflicht
- **Custom Fields (Chat-Anker) erst am Ende eines Batches sammeln** — pro Task setzen
- **em-dash `—` in Custom-Field-Values** verwenden (nur ASCII `-`, em-dash löst ClickUp-Fehler aus)
- **Batch-Audit weglassen** (`N/N Body-Anker ✅ | N/N Custom Fields ✅`)
- **Impliziter Start-Trigger OHNE Task-ID** im Satz — "los geht's" / "fangen wir an" ohne BPM-Nummer triggert NICHT
- **Inhaltliche Arbeit starten BEVOR `tracker start` ausgeführt wurde** — Task muss vorher auf `in progress`

**Vollständige VERBOTEN-Liste:** `references/anti-patterns.md`.
