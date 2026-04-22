# Anti-Patterns + Automationspolitik + Integration

Kollektion aller Regeln die verhindern sollen dass tracker-Operationen schiefgehen.

---

## Automationspolitik

| Situation | Verhalten |
|-----------|-----------|
| "tracker neu: ..." | Schnellmodus oder Fragemodus (ask_user_input_v0!) + Chat erstellt + Custom Fields |
| "tracker done: ..." | Commit-Info ermitteln + 10 Custom Fields + Status setzen |
| "tracker split: ..." | Vorschlag + ask_user_input_v0 zur Bestätigung + NN.NN-Nummerierung |
| "tracker relate: ..." | Dependency setzen via ClickUp API |
| "tracker field: ..." | Einzelnes Feld gezielt aktualisieren |
| "anker setzen: ..." | Manuellen TEMP-Anker setzen + Memory-Eintrag |
| code-erstellen nach Commit | NUR vorschlagen (per ask_user_input_v0) |
| chat-wechsel am Ende | Batch-Vorschlag + Chat-URL in Prompt einbetten |
| Alle Unteraufgaben done | ask_user_input_v0: Parent auch schliessen? |
| "notiz" / "nicht vergessen" | ask_user_input_v0: Task, Notiz, Beides |
| "merk dir" / "remember" | → Memory, NICHT ClickUp |

**Goldene Regel:** Explizit → direkt. Alles andere → ask_user_input_v0 (keine Prosa!).

---

## Notizen vs. Tasks

| Trigger | Aktion |
|---------|--------|
| "neue aufgabe", "neuer punkt", "tracker neu" | → Task in ClickUp |
| "merk dir", "remember" | → Memory (KEIN ClickUp) |
| "notiz", "nicht vergessen" | → `ask_user_input_v0`: Task, Notiz, Beides |

---

## Integration mit anderen Skills

### code-erstellen
Nach Commit: `ask_user_input_v0`: "Passt zu BPM-XXX. `tracker done`?" → Ja / Nein / Anderer Task
Wenn ja → Commit-Hash direkt aus der Session (schon bekannt) + Custom Fields befüllen + aktuellen Chat als "Chat erledigt".

### chat-wechsel
Am Chat-Ende: Batch-Abschluss + Übergabe.
Schreibt die aktuelle Chat-URL in den Übergabe-Prompt, damit im nächsten Chat sofort verfügbar.

### doc-pflege
Nach Doc-Update: `ask_user_input_v0`: "Doc-Task BPM-XXX erledigt. `tracker done`?" → Ja / Nein
Gleiches 10-Fields-Schema wie bei Code-Tasks.

---

## VERBOTEN

- Tasks automatisch erstellen aus freiem Chattext
- Tasks automatisch auf Done setzen ohne Trigger
- ClickUp-Calls in anderen Skills duplizieren
- Titel ohne BPM-Nummer oder Kürzel (Hauptaufgaben)
- BPM-Nummern an Unteraufgaben vergeben
- Unteraufgaben ohne NN.NN-Nummerierung im Titel
- Sub-Nummern nachnummerieren wenn Lücken entstehen
- Tasks ohne Dedup-Prüfung erstellen
- Meilensteine dynamisch erstellen
- Nummern wiederverwenden
- Hauptaufgabe automatisch schließen wenn Unteraufgaben done
- **`tracker done` ohne Versuch, Custom Fields zu befüllen** (mindestens Erledigt-Datum + Chat erledigt)
- **`tracker neu` ohne Chat erstellt URL** (außer User verweigert)
- **`tracker neu` ohne Typ** (außer Typ ist partout nicht ermittelbar)
- Chat-URLs raten oder erfinden — bei Unsicherheit ask_user_input_v0 oder leer lassen
- **Prosa-Fragen bei festen Entscheidungsoptionen** — IMMER ask_user_input_v0 verwenden
- Status mit Grossbuchstaben setzen (`Done`, `Open`, `In Progress`) — IMMER klein
- Relationships als Freitext statt ClickUp-Dependency nutzen
- Custom Field Option-IDs raten — immer aus dem Skill-Kapitel kopieren
- Description ohne Template bei Standard-Tasks (Meta-Tasks dürfen verkürzen)
- **Stale-Check-Ergebnis automatisch aus Memory entfernen** ohne `ask_user_input_v0` Bestätigung
- **Stale-Check bei jedem Chat-Turn wiederholen** — nur einmal beim Chat-Start ausführen

### Batch-spezifisch (≥2 Task-Operationen in einer Antwort)

Vollständige Spec: `batch-protocol.md`. Kurzliste:

- **Pro-Task-Quittung weglassen** nach `create`/`update` — Format-Zwang ist Pflicht (tracker-004)
- **Custom Fields (Chat-Anker) erst am Ende eines Batches sammeln** — pro Task setzen (tracker-001)
- **Tabelle statt einzelner Quittungszeilen** bei mehreren Tasks
- **Parent-Anker nutzen um Subtask-Anker zu sparen** — jeder Subtask hat eigene Task-ID und braucht eigene Quittung
- **Batch-Audit weglassen** (`N/N Body-Anker ✅ | N/N Custom Fields ✅`)
- **Batch-Ansage weglassen** (`📦 Batch: N Tasks (create/update/done)`) vor Beginn
- **em-dash `—` in Custom-Field-Values** (nur ASCII `-` — em-dash löst ClickUp-API-Fehler aus)
- **"wie gehabt" / "analog für die anderen" / "..."** statt jeder Quittung im Klartext
- **Mehrere Tool-Calls hintereinander ohne zwischendurch Quittungen** — Quittung direkt nach jedem Call
- **Parent als Container-Task ohne eigenen Anker** abschließen — auch Kaskaden-Abschlüsse brauchen eigene Quittung
