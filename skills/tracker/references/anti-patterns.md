# Anti-Patterns + Automationspolitik + Integration

Kollektion aller Regeln die verhindern sollen dass tracker-Operationen schiefgehen.

---

## Automationspolitik

| Situation | Verhalten |
|-----------|-----------|
| "tracker neu: ..." | Schnellmodus oder Fragemodus (ask_user_input_v0!) + Chat erstellt + Custom Fields |
| "tracker start: ..." | Status auf `in progress` + Parent-Check + Pro-Task-Quittung |
| "starte BPM-NNN" / "fangen wir mit BPM-NNN an" | ask_user_input_v0: Beide / Nur Subtask / Nein |
| "los geht's" / "fangen wir an" OHNE Task-ID | Ignorieren (kein impliziter Start) |
| User bestätigt vorgeschlagenen Task-Fokus ("ok", "mach", "weiter") | `tracker start` vor inhaltlicher Arbeit |
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

### Commit-Disziplin (tracker-007)

- **Sammeln von mehreren Subtasks auf einen Commit** ohne dokumentierte Ausnahme — jeder abgeschlossene (Sub-)Task bekommt sofort einen eigenen Commit
- **Commit aufschieben bis zum Session-Ende** — Commit direkt nach Task-Abschluss, nicht sammeln
- **Zero-Change-Tasks mit leerem `Commit ID`-Feld unkommentiert lassen** — Quittung MUSS `(Zero-Change)` enthalten damit das leere Feld nachvollziehbar ist
- **Versionierung ignorieren** — PATCH für kleine Refactors, MINOR für Features/Phasen, MAJOR für Breaking Changes
- **WANN vs. WIE vermischen** — `tracker` steuert WANN committet wird, `git-commit-helper` formatiert WIE; Commit-Disziplin gehört NICHT in `git-commit-helper`

### Review-Workflow (tracker-006)

- **Scope-Check vor Task-Übergang weglassen** — Pflicht vor jedem `tracker done`, `tracker start` (neu oder Wechsel), Fokus-Entscheidung im Dialog, oder nach User-Bestätigung "so machen wir's"
- **Nur Punkt 1 prüfen und Punkte 2-4 überspringen** — alle 4 Punkte (aktueller Task, Parent, Siblings, verweisende offene Tasks) sind Pflicht wenn Trigger greift
- **Task auf done setzen während verweisende offene Tasks den Scope ändern würden** — erst Scope der verweisenden Tasks klären
- **Start auf neuen Task ohne Check auf Auswirkungen auf bereits laufende Tasks** — Task-Wechsel triggert denselben 4-Punkte-Check
- **User-Bestätigung "so machen wir's" annehmen ohne Parent/Siblings zu prüfen** — Bestätigungen von Regeln/Entscheidungen sind starke Trigger für den Check
- **Gefundene Änderungen nur mündlich notieren, nicht in ClickUp eintragen** — Descriptions/neue Subtasks MÜSSEN in ClickUp persistiert werden
- **Check nach dem Task-Übergang nachholen** — muss VORHER passieren, nach dem Übergang ist zu spät

### Automatischer Nachlauf nach tracker done (tracker-008)

- **Nach `tracker done` passiv auf User-Input warten** ohne `ask_user_input_v0` mit Folgeoptionen
- **Commit-Hash vom User anfordern** wenn DC verfügbar ist — Hash selbst via `git log -1 --format='%h %s'` holen
- **Zwischenstand-Tabelle nach Task-Abschluss weglassen** — Übersicht über erledigte Items und Push-Pending ist Pflicht
- **Folgeoptionen als Prosa-Frage statt `ask_user_input_v0`** — "Was willst du als nächstes?" im Fließtext ist VERBOTEN, nur Button-Optionen
- **Folgeoptionen bereits nach dem ersten Task eines Batches zeigen** — erst nach dem letzten Task des Batches
- **Nachlauf komplett überspringen** weil "der User weiß ja eh was er will" — die Regel ist verbindlich auch wenn User aktiv ist
- **Zero-Change-Tasks als Grund für komplettes Überspringen nehmen** — nur Schritt 1 (Hash holen) entfällt, Schritte 2-4 bleiben

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

### Start-spezifisch (tracker-002)

- **Inhaltliche Arbeit beginnen BEVOR `tracker start` ausgeführt wurde** — Task muss vorher auf `in progress`
- **Impliziter Start-Trigger OHNE Task-ID im Satz** — "los geht's" / "fangen wir an" ohne BPM-Nummer triggert NICHT
- **User-Zustimmung zu Task-Fokus ignorieren** — nach "ok" / "mach" / "weiter" auf einen vorgeschlagenen Task MUSS `tracker start` vor der Arbeit
- **Parent überschreiben wenn er schon `in progress` oder `done` ist** — nur `to do`/`open`-Parents werden auf `in progress` gesetzt
- **Task-ID raten** wenn User Kurzform ohne eindeutige Zuordnung nutzt — stattdessen `ask_user_input_v0`
- **Status-Wert raten** bei Listen-Typen — Fallback-Reihenfolge einhalten, bei Scheitern `ask_user_input_v0`

### Referenz-Anker in Folge-Antworten (tracker-005)

- **Referenz-Anker weglassen** in Folge-Antworten die einen Task inhaltlich betreffen (Commit-Vorschlag, Klärung, Fehler-Fix, Fortschritt)
- **Referenz-Anker unten** statt oben in der Antwort — erschwert Suche und Überblick
- **Referenz-Anker und Quittung für denselben Task doppelt** zeigen — Quittung enthält den Anker bereits inline
- **Referenz-Anker für rein beiläufige Erwähnung** setzen — "die 4 tracker-Issues" in einer Aufzählung braucht keinen Anker
- **Task inhaltlich diskutieren ohne Anker** — Thread verliert sonst die Audit-Spur für spätere `conversation_search`

### Projekt-Config (Projekt-Architektur, v0.13.0)

Skills lesen projekt-spezifische Daten aus `projects/<[PROJECT]>/`.
VERBOTEN ist jede Form von Hartkodierung oder Fallback-Weglassung:

- **Konkrete Listen-IDs / Custom-Field-IDs / Option-IDs** im Skill selbst führen — alles aus `projects/<[PROJECT]>/clickup-fields.md` und `projects/<[PROJECT]>/clickup-lists.md` lesen
- **Modul-Kürzel raten** wenn `[PROJECT]`-Memory fehlt — stattdessen `ask_user_input_v0` mit den vorhandenen Ordnern in `projects/`
- **Projekt-Config-Dateipfade raten** — Muster ist immer `projects/<[PROJECT]>/<datei>.md`, niemals davon abweichen
- **Fallback-Frage weglassen** wenn Memory fehlt — Skill MUSS aktiv nach dem aktiven Projekt fragen, nicht still rumraten
- **Annehmen dass `[PROJECT]` immer "bpm" ist** — Memory lesen und den tatsächlichen Wert verwenden
- **`projects/<[PROJECT]>/`-Dateien ohne Lesen verwenden** — zuerst prüfen dass die Datei existiert, dann ihren Inhalt laden, erst dann verwenden
- **BPM-Spezifika (PlanManager, PM, v1, 901522…) inline im Skill einbauen** statt sie als Beispiele mit Kontext zu markieren — wenn Beispiele, dann explizit als "Beispiel (BPM-Projekt)"
- **Status-Werte `done` oder `complete` hartkodieren** statt aus `projects/<[PROJECT]>/clickup-fields.md` Status-Werte-Matrix zu lesen
