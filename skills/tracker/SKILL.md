---
name: tracker
description: >
  Führt konkrete ClickUp-Aktionen für BPM-Tasks und Skill-Issues aus, z.B.
  "tracker neu", "tracker issue", "tracker done", "tracker update",
  "tracker status", "tracker suche", "tracker next", "tracker split",
  "tracker relate" und "tracker field". Use when users want to anlegen,
  erstellen, eintragen, melden, dokumentieren, abschließen, aktualisieren,
  or update a ClickUp task or issue — including BPM-Tasks, Skill-Issues,
  Bug-Reports, neue Aufgaben, offene Punkte, Task-Splits, Dependencies,
  oder Status-Abfragen. Triggers also on "issue erstellen", "task anlegen",
  "ClickUp-Eintrag", "Skill-Issue melden". Do not trigger for general talk
  about priorities, brainstorming, notes without concrete tracker command,
  or code/doc work without explicit task action.
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

**In Folge-Antworten** die einen Task inhaltlich besprechen (ohne Tool-Call)
steht oben ein Referenz-Anker:
```
Betroffene Tasks in dieser Antwort: [BPM-ANCHOR-<task-id>] <name>.
```
Bei Quittung in derselben Antwort entfällt der Referenz-Anker für diesen Task
(Quittung hat Vorrang). Spec: `references/batch-protocol.md` Kapitel 2b.

Adressiert `tracker-001`, `tracker-004`, `tracker-005`.

---

## 🚨 Kernregel: Referenz-Anker in Folge-Antworten

**Bei JEDER Folge-Antwort die einen bereits existierenden Task inhaltlich
betrifft (ohne Tool-Call), MUSS oben ein Referenz-Anker stehen:**

```
Betroffene Tasks in dieser Antwort: [BPM-ANCHOR-<task-id>] <n>.
```

Mehrere Tasks kommagetrennt:
```
Betroffene Tasks in dieser Antwort: [BPM-ANCHOR-86c9feyj9] tracker-005, [BPM-ANCHOR-86c9f7awj] tracker-001.
```

**Pflicht-Trigger:**
- Commit-Vorschlag für einen Task
- Klärungsfrage zu laufendem Task-Fix
- Fehler-Diagnose während Task-Arbeit
- Status-Update / Fortschrittsbericht
- Nachträgliche Analyse oder Konzept-Änderung
- Jede Folge-Antwort in einem Thread der einen aktiven Task behandelt

**Gilt auch wenn der Task nicht via `tracker neu`/`tracker done` angefasst
wurde, sondern nur per `clickup_get_task` gelesen, besprochen oder per
`edit_block` umgesetzt wird** (adressiert tracker-009: "Task übernommen
ohne neu/done").

**Wann NICHT Pflicht:**
- Task-ID nur in Aufzählung erwähnt ("die 4 tracker-Issues")
- Antwort rein über Meta/Tooling (DC, git, Skill-System)
- Rückfrage ohne Task-Bezug
- Reine Begrüßung / Abschluss

**Wenn in derselben Antwort eine Pro-Task-Quittung steht** (die bereits
den Anker inline enthält), entfällt der Referenz-Anker oben für diesen
Task.

Adressiert `tracker-005`, `tracker-009`.

Details + Beispiele: `references/batch-protocol.md` Kapitel 2b.

---

## 🚨 Kernregel: Review-Workflow vor Task-Übergang

**Vor JEDEM `tracker done` / `tracker start` (neu oder Wechsel) / Fokus-Wechsel
im Dialog MUSS ein 4-Punkte-Scope-Check durchgeführt werden:**

1. **Aktueller Task** — Description ändert sich durch neue Erkenntnisse?
2. **Parent-Task** — Scope/DoD betroffen?
3. **Sibling-Subtasks** im selben Parent — betroffen?
4. **Verweisende offene Tasks** (Related/Links/Dependencies) — betroffen?

Gefundene Änderungen werden in ClickUp umgesetzt **BEVOR** der Task-Übergang
passiert. Danach ggf. neue Abarbeitungs-Reihenfolge via `ask_user_input_v0`
vorschlagen.

**Trigger:**
- Bevor `tracker done` ausgeführt wird
- Bevor `tracker start` auf neuen oder bereits gestarteten Task
- Nach expliziter User-Bestätigung `"so machen wir's"` / `"das merken wir uns so"`

**Check ENTFÄLLT bei:** reinen Pflege-Updates ohne Scope-Änderung, Zero-Change-Tasks,
explizitem User-Skip `"Scope-Check überspringen"`.

Vollständige Spec mit API-Calls und Beispiel-Ablauf: `references/review-workflow.md`.

Adressiert `tracker-006`.

---

## 🚨 Kernregel: Automatischer Nachlauf nach tracker done

**Nach jedem erfolgreichen `tracker done` MUSS Claude automatisch weiterführen —
niemals passiv auf User-Input warten.**

4 Schritte:

1. **Commit-Hash via DC holen** (`git log -1 --format='%h %s'`) — nicht vom User anfordern wenn DC verfügbar
2. **Custom Fields setzen** (Commit ID, Erledigt-Datum, Chat-Anker erledigt) — typischerweise im Haupt-Ablauf-Schritt 9 bereits erledigt
3. **Zwischenstand-Tabelle im Chat** (Task / Commit-Hash / Status / Push-Pending)
4. **Folgeoptionen via `ask_user_input_v0`** — niemals Prosa-Frage, niemals still warten

**Ausnahmen:** Zero-Change-Tasks (Schritt 1 entfällt), Batches (Schritte 3-4 nur einmal am Batch-Ende), DC nicht verfügbar (Schritt 1 entfällt → Prosa-Frage nach Hash).

Baut auf `cc-steuerung-003` auf (DC ist Default-Ausführungsmodus).

Vollständige Spec mit Beispiel-Ablauf: `references/complete-task.md` Abschnitt "Automatischer Nachlauf nach tracker done".

Adressiert `tracker-008`.

---

## 🚨 Kernregel: Projekt-Config aus `projects/<[PROJECT]>/`

**Alle projekt-spezifischen Daten (Listen-IDs, Custom-Field-IDs,
Option-IDs, Modul-Kürzel, Meilenstein-Tags, Status-Werte-Matrix) werden
zur Laufzeit aus `projects/<[PROJECT]>/` gelesen — NICHT hartkodiert
im Skill.**

### Wie Claude das aktive Projekt ermittelt

1. Memory scannen nach Eintrag `[PROJECT] <n> | ...`
2. Projekt-Config-Pfad konstruieren: `projects/<n>/`
3. Benötigte Datei lesen:
   - `projects/<[PROJECT]>/clickup-lists.md` — Listen-IDs + Scope-Routing
   - `projects/<[PROJECT]>/clickup-fields.md` — Custom-Field-IDs + Option-IDs + Modul-Kürzel + Status-Werte
   - `projects/<[PROJECT]>/memory-format.md` — Memory-Eintragsformate

### Fallback wenn `[PROJECT]`-Memory fehlt

```
1. Claude scannt Memory → kein [PROJECT]-Eintrag gefunden
2. Claude listet vorhandene Ordner in projects/
3. ask_user_input_v0: "Welches Projekt ist aktiv?"
   Optionen = gefundene Ordner-Namen
4. User wählt → Claude schlägt Memory-Eintrag vor
5. User bestätigt → Claude schreibt [PROJECT]-Eintrag via memory_user_edits
```

### Fallback wenn Projekt-Config-Datei fehlt

```
1. Claude versucht projects/<[PROJECT]>/<datei>.md zu lesen
2. Datei existiert nicht → Prosa-Info: "Datei fehlt, Skill läuft im
   Universell-Modus. Bitte Daten manuell angeben oder Datei anlegen."
3. Claude fragt nach den konkreten Daten die aktuell benötigt werden
```

### Fallback wenn `projects/`-Verzeichnis leer

```
Skill läuft im Universell-Modus. Alle konkreten Werte werden ad-hoc
vom User abgefragt. Empfehlung: Projekt-Ordner anlegen — siehe
docs/project-architecture.md.
```

### Beispiel-Muster für Skill-interne Verweise

Statt einer hartkodierten Tabelle wie früher:
```
| PlanManager | PM | 901522848097 |
| Docs | DOC | 901522848102 |
...
```

steht jetzt im Skill nur noch:
```
Modul-Kürzel und Listen-IDs siehe
`projects/<[PROJECT]>/clickup-fields.md` Abschnitt 3.
```

Universelle Regel: `docs/project-architecture.md` (im Skill-Repo-Root).

---

## Vorrang / Delegation an andere Skills

**tracker ist für explizite ClickUp-Task-Aktionen. Wenn die Hauptabsicht
Code-Arbeit, Doku oder andere inhaltliche Tätigkeit ist, NICHT hier
weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Code schreiben oder ändern (auch wenn ein Task-Bezug besteht) | **code-erstellen** |
| UI-Entwurf als HTML-Mockup | **mockup-erstellen** |
| Commit-Befehl, Commit-Message, Version-Bump | **git-commit-helper** |
| Doku schreiben, ADR, Konzept, Frontmatter-Pflege | **doc-pflege** |
| Konsistenzprüfung Code ↔ Docs | **audit** |

Nur wenn die Hauptabsicht **eine konkrete ClickUp-Task-Aktion** ist
(`tracker neu`, `tracker done`, `tracker update`, `tracker status`,
`tracker suche`, Issue anlegen, Scope-Check, Anker setzen),
bleibt tracker zuständig.

**Wichtig:** tracker wird NICHT automatisch ausgelöst durch Code-Commits
oder Doc-Änderungen. Andere Skills (code-erstellen, doc-pflege) rufen
tracker nur aktiv via `ask_user_input_v0` auf ("Passt zu BPM-XXX.
tracker done?"). Die User-Bestätigung ist Pflicht. Details siehe
Kapitel "Integration mit anderen Skills".

---

## Routing: Kommando → Reference-Datei

| Kommando | Reference |
|----------|-----------|
| `tracker neu: <Beschreibung>` | `references/create-task.md` |
| `tracker issue <skill>: <Titel>` | `references/issue-task.md` |
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
| `issue-task.md` | `tracker issue` Ablauf, Skill-Issue-Listen-Routing, Issue-ID-Nummerierung, Skill-Issues-Scope Custom Fields |
| `start-task.md` | `tracker start` Ablauf, Parent-Kaskade, implizite Trigger mit Task-ID |
| `complete-task.md` | `tracker done` Ablauf, Git-Commit-Ermittlung, Commit-Disziplin (ein Task = ein Commit), Automatischer Nachlauf (Hash holen, Zwischenstand, Folgeoptionen), Status-Werte, Beispiel-Workflow |
| `review-workflow.md` | 4-Punkte-Scope-Check vor `tracker done` / `tracker start` / Fokus-Wechsel: aktueller Task + Parent + Siblings + verweisende offene Tasks |
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

## Memory-Eskalation

Memory-Einträge (Rubriken `[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]`,
`[REVIEW-PENDING]`) werden **nie automatisch** zu ClickUp-Tasks.

Wenn Herbert einen wiederholt auftauchenden Memory-Eintrag zu einem
echten Task eskalieren will:

1. Memory-Eintrag als Kontext in Task-Description übernehmen
2. Per `tracker neu` einen ClickUp-Task anlegen (normaler Ablauf)
3. Nach User-Bestätigung: Memory-Eintrag via `memory_user_edits remove`
   entfernen — **nie stillschweigend, nie automatisch**

**Memory ≠ Tracker-Light.** Memory bleibt nur offene Merker, Fragen,
Verifikationen. Substantielle Arbeit gehört in ClickUp.

Abgrenzung:
- **Ohne User-Anweisung:** Memory bleibt Memory, auch bei wiederholtem
  Handover-Vorkommen
- **Mit User-Anweisung:** Memory → Task via `tracker neu`, dann
  Bestätigung einholen fürs Entfernen

Rubriken-Konvention: `MEMORY-RUBRIKEN.md`.

Adressiert Phase 4.4.

---

## Automationspolitik (Kurzform)

**Goldene Regel:** Explizit → direkt. Alles andere → ask_user_input_v0 (keine Prosa!).

Vollständige Tabelle in `references/anti-patterns.md`.

---

## ClickUp-Tools (Lade-Pattern)

ClickUp-Tools sind in Claude.ai **deferred-loaded** — zu Sessionbeginn nicht im Tool-Inventar, sondern müssen über `tool_search` aktiviert werden.

**Regel:** Wenn ein Tool nicht aufrufbar ist (`Tool '...' not found`), `tool_search` mit dem **EXAKTEN Tool-Namen** verwenden, nicht mit Umschreibung.

```
✅ tool_search("clickup_get_task")          # lädt das Tool
❌ tool_search("clickup task subtasks")     # liefert Müll-Treffer
```

Vollständiges Tool-Inventar + Befehl→Tool-Mapping: `references/clickup-tools.md`.

Adressiert `tracker-010`.

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
- **Referenz-Anker in Folge-Antworten weglassen** — wenn eine Antwort einen Task inhaltlich betrifft und keine Quittung enthält, MUSS oben `Betroffene Tasks in dieser Antwort: [BPM-ANCHOR-<id>] <name>.` stehen. **Gilt auch bei Tasks die nur gelesen/bearbeitet wurden, ohne `tracker neu`/`tracker done` auszulösen** (tracker-009)
- **Projekt-Daten hartkodieren** im Skill (Listen-IDs, Custom-Field-IDs, Option-IDs, Modul-Kürzel) — alles aus `projects/<[PROJECT]>/` lesen
- **Annehmen dass `[PROJECT]` immer "bpm" ist** — Memory lesen und den tatsächlichen Wert verwenden
- **Commits sammeln statt pro Task** — jeder abgeschlossene (Sub-)Task bekommt sofort einen eigenen Commit (Details: `references/complete-task.md`)
- **Review-Workflow-Check vor Task-Übergang weglassen** — 4-Punkte-Check (aktueller Task + Parent + Siblings + verweisende offene Tasks) ist Pflicht vor `tracker done`, `tracker start` und Fokus-Wechsel (Details: `references/review-workflow.md`)
- **Nach `tracker done` passiv warten statt Nachlauf ausführen** — Hash via DC holen + Zwischenstand-Tabelle + Folgeoptionen via `ask_user_input_v0` sind Pflicht (Details: `references/complete-task.md` Abschnitt "Automatischer Nachlauf")
- **Issue-IDs manuell vergeben lassen bei `tracker issue`** — Auto-Nummerierung via `clickup_filter_tasks` ist Pflicht, inkl. `include_closed: true` + Unique-Check (Details: `references/issue-task.md` Schritt 4)
- **Memory-Einträge automatisch zu Tasks eskalieren** — nur auf explizite Herbert-Anweisung `tracker neu` aus Memory ableiten, nie ungefragt. Entfernen des Memory-Eintrags erst nach Bestätigung (siehe Memory-Eskalation, Phase 4.4)
- **`tool_search` mit Umschreibung statt exaktem Tool-Namen** wenn ein ClickUp-Tool nicht geladen ist — das liefert Müll-Treffer und kostet Zeit. Bei `Tool '...' not found` IMMER mit dem exakten Tool-Namen suchen (z.B. `tool_search("clickup_get_task")`, nicht `tool_search("clickup task details")`). Tool-Inventar: `references/clickup-tools.md` (tracker-010)

**Vollständige VERBOTEN-Liste:** `references/anti-patterns.md`.
