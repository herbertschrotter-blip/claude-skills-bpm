---
name: chat-wechsel
description: >
  Erstellt die Übergabe an die nächste Claude-Sitzung: einen vollständigen
  Handover-Prompt mit Stand, Erledigtem, offenen Punkten, nächsten Schritten,
  Entscheidungen und Regeln (aus den Profilen); in Claude Code zusätzlich vorher
  den Sitzungsabschluss im Repo (doc-pflege Modus 8). Use when users want to continue in a new chat or session, ask for
  a session handover, a continuation prompt, or a next-chat summary. Do not trigger for ChatGPT review prompts,
  generic prompt requests, or casual goodbyes like "tschüss" or "gute Nacht".
---

# Chat-Wechsel Skill

## Zweck

Übergabe, wenn eine Sitzung endet und in der nächsten weitergearbeitet wird. Zwei Wege, ein Ziel:

- **Cowork-Chat:** Ein Handover-Prompt im Chat (PROMPT-STRUKTUR: `references/prompt-struktur.md`). Der Chat hat kein
  Repo-Gedächtnis, also trägt der Prompt den Stand.
- **Claude Code:** Erst **doc-pflege Modus 8 (Sitzungsabschluss)** – Statusliste/Aufgabenquelle, Befunde,
  Stand-Abschnitt, offene Punkte, Commit + Push nach der Push-Policy –, dann **derselbe vollständige Handover-Prompt** nach
  PROMPT-STRUKTUR (Herbert, 16.09.2026: „der war in BPM immer viel umfangreicher“). Der Prompt darf den
  Repo-Stand zusammenfassen, verweist aber für Details auf HANDOFF/Bauplan statt sie zu kopieren. Der
  Startprompt des Doku-Profils (Heidi: Bauplan Abschnitt 0) steht als Einstiegszeile **im** Prompt.
  Eine Kurzform (nur Startprompt) gibt es nur, wenn der User sie ausdrücklich verlangt („kurzer Prompt“).

Projektwerte (Präfix, Listen, Commit-Format, Doc-Namen, Testbefehl) kommen aus den Profilen der CLAUDE.md
(Commit-, Tracker-, Code-, Doku-Profil); ohne Profil gilt der BPM-Weg (Memory `[CLICKUP]`, INDEX.md).

---

## Vorrang / Delegation an andere Skills

**chat-wechsel erzeugt den Handover-Prompt für die NÄCHSTE Claude-Session.
Wenn die Hauptabsicht ein ChatGPT-Review-Prompt oder ein anderer
Prompt-Typ ist, NICHT hier weiterarbeiten, sondern delegieren.**

| Hauptabsicht | Zuständiger Skill |
|--------------|-------------------|
| Prompt für ChatGPT-Review (zweite Meinung, Cross-LLM-Kritik) | **chatgpt-review** |
| Code schreiben | **code-erstellen** |
| ClickUp-Task-Aktion | **tracker** |
| Doc schreiben | **doc-pflege** |

Nur wenn die Hauptabsicht **ein Handover-Prompt für den nächsten Claude-Chat** ist
("neuer chat", "nächster chat", "übergabe", "session beenden"), bleibt
chat-wechsel zuständig.

**Wichtig:** Beide Skills können im selben Chat nacheinander laufen
(erst ChatGPT-Review abschließen, dann Claude-Handover). Sie triggern
aber nicht gemeinsam auf einen Satz — der User-Intent entscheidet,
welcher zuerst dran ist.

---

## Grundsätze

- **Fragen nur bei offener Entscheidung** – wenn nach Auftrag, Skill-Profil, Regel und Kontext wirklich etwas offen
  ist –, dann als Auswahlfrage mit dem Frage-Werkzeug der Umgebung. Typische Stellen:

  | Situation | Optionen |
  |-----------|----------|
  | Link-Prüfung findet tote Verweise | "Korrigieren", "Mit Warnung übernehmen", "Weglassen" |
  | Claude Code: uncommittete Änderungen beim Abschluss | "Jetzt committen (Modus 8)", "Als offen vermerken", "Abbrechen" |
  | Batch-Abschluss: erledigte Tasks | "Alle als Done markieren", "Einzeln wählen", "Keine" |
  | Batch-Abschluss: erledigte Tasks einzeln wählen | multi_select mit allen Task-Namen |
  | Batch-Anlage: neue Tasks aus Chat | "Alle anlegen", "Einzeln wählen", "Keine" |
  | Batch-Anlage: neue Tasks einzeln wählen | multi_select mit allen erkannten Problemen |
  | ClickUp nicht erreichbar | "Trotzdem Prompt erstellen", "Retry", "Abbrechen" |
  | Version-Angabe unklar | Aktuelle Versionen als Optionen |
  | Kein Commit-Stand erkennbar | "Version vom User eingeben", "Ohne Version", "Abbrechen" |

  Prosa nur bei einer offenen Frage ohne feste Optionen (Beispiel: "Welche Version ist aktuell?" ohne Kandidaten), wenn
  der Nutzer gerade eine klare Präferenz signalisiert hat, oder bei Erklärung/Kontext ohne echte Entscheidung.
- **Branch** nach der Branch-Policy im Skill-Profil der `CLAUDE.md`: `current` → der aktuelle Branch aus der Shell
  (`git branch --show-current`); `fixed:<branch>` → der aktuelle muss dieser sein, sonst Auswahlfrage (wechseln /
  abbrechen). Ohne Shell gilt bei `fixed:<branch>` dieser Branch, bei `current` eine Auswahlfrage. Ohne Skill-Profil: ein in dieser Sitzung schon bekannter Branch; sonst mit Shell
  `git branch --show-current` – Tatsache, keine Frage; ohne Shell die Branches über die GitHub API auflisten und per
  Auswahlfrage wählen lassen (Optionen = Branch-Namen). NIE automatisch einen Branch annehmen (weder `main` noch einen
  anderen). Den Branch für die ganze Sitzung merken und im Übergabe-Prompt unter `**Branch:**` eintragen.
- **Push** im Sitzungsabschluss (Claude Code) nach der Push-Policy des Skill-Profils:
  - `user-only`: kein Push; der Nutzer pusht selbst
  - `allowed`: Push nur, wenn der Nutzer es ausdrücklich will
  - `required-after-commit`: Push direkt nach dem Commit des Sitzungsabschlusses
  - `required-at-session-end`: alle Commits der Sitzung pushen, bevor der Handover-Prompt ausgegeben wird

  Ohne Push-Policy (kein Skill-Profil): Commit + Push im Sitzungsabschluss.

  Bleiben Commits ungepusht (`user-only`, `allowed`), nennt der Übergabe-Prompt sie unter „Sonstige offene Punkte“
  (Hash und Titel, „Push durch den Nutzer“).

---

## TRIGGER

Ja: "neuer chat", "nächster chat", "session beenden", "chat wechsel",
"weiter im nächsten chat", "mach mir den prompt", "übergabe", "neue sitzung",
"sitzung abschließen und übergabe"

Nein: "pause", "tschüss", "gute nacht"

---

## Fall → Reference

| Fall | Reference |
|------|-----------|
| Handover-Prompt aufbauen (beide Umgebungen) | [references/prompt-struktur.md](references/prompt-struktur.md) |
| ClickUp-Abgleich vor dem Übergabeprompt: offene Tasks, Chat-Scan, Batch-Abschluss, ClickUp nicht erreichbar | [references/tracker-abgleich.md](references/tracker-abgleich.md) |
| Cowork-Chat: Memory-Scan, Chat-Anker-Übergabe, Chat-URL im Übergabe-Prompt | [references/cowork.md](references/cowork.md) |
| Claude Code in tmux: neues Fenster für die nächste Sitzung | [references/neues-fenster.md](references/neues-fenster.md) |

---

## Memory-Scan (PFLICHT bei Handover)

**Zweck:** Offene Merker, Verifikationen und Architektur-Fragen aus Memory in den Handover-Prompt übernehmen, damit sie nicht zwischen Chats verloren gehen.

**Claude Code:** Das Memory ist ein Ordner mit Dateien (Typen `user`/`feedback`/`project`/`reference`) und
bleibt über Sitzungen erhalten – es muss **nicht** in den Prompt kopiert werden. Stattdessen: offene Punkte,
die nur im Chat entstanden sind, gehören in den Doc-Ort des Doku-Profils (Heidi: HANDOFF Abschnitt 4 /
Bauplan Abschnitt 10), erledigte Merker werden mit Herberts Bestätigung als Datei entfernt. Die Schritte für den
Cowork-Chat stehen in [references/cowork.md](references/cowork.md), Abschnitt „Memory-Scan (PFLICHT bei Handover)“.

---

## ABLAUF IN CLAUDE CODE (Sitzungsabschluss + vollständiger Prompt)

1. **doc-pflege Modus 8 (Sitzungsabschluss)** ausführen: Statusliste/Aufgabenquelle ↔ Tracker, Befunde und
   Entscheidungen, Stand-Abschnitt (Heidi: HANDOFF 3e), offene Punkte als Checkliste (HANDOFF 4), Doku-Checkliste
   des Commit-Profils, Commit + Push nach der Push-Policy (Grundsätze). Uncommittete Änderungen → Auswahlfrage.
2. **ClickUp-Abgleich** nach [references/tracker-abgleich.md](references/tracker-abgleich.md) (Batch-Abschluss über tracker),
   **Memory**: erledigte Merker mit Bestätigung entfernen.
3. **Link-Prüfung** auf den Stand-Abschnitt und den Startprompt.
4. **Handover-Prompt nach PROMPT-STRUKTUR ausgeben** ([references/prompt-struktur.md](references/prompt-struktur.md);
   vollständig, als Markdown-Codeblock). Erste Zeile darin ist
   der Startprompt des Doku-Profils, z.B.:

```
> Lies CLAUDE.md, docs/HANDOFF.md (Abschnitt 3e + 4) und docs/dreame_x60/BAUPLAN.md. Nimm die nächste offene
> Aufgabe aus der Statusliste (Abschnitt 1): <DX-NNN | Kürzel | Schritt>. Prüfe Voraussetzungen, lies ihre Karte
> in Abschnitt 8 und arbeite nur diese Aufgabe ab (Skills: tracker start, code-erstellen nach Code-Profil).
> Regeln: Abschnitt 2. Widerspruch Code ↔ Bauplan → Befund in Abschnitt 10, Aufgabe blockiert, stoppen.
```

   Quelle des Musters: Feld „Startprompt“ im Doku-Profil (Heidi: Bauplan Abschnitt 0). Danach folgen die
   Abschnitte der PROMPT-STRUKTUR: Aktueller Stand, Erledigt in dieser Sitzung, Offene Punkte (ClickUp nach
   Status, Chat, Sonstiges), Nächste Schritte, Aktive Entscheidungen, Kontext/Warnungen, Regeln aus den Profilen.
   Memory-Sektion: in Claude Code die relevanten Memory-Dateien nennen (Titel), nicht kopieren.
5. **Neues Fenster** (nur wenn die Sitzung in tmux läuft): Umgebung prüfen, per Auswahlfrage anbieten, dann ein
   tmux-Fenster im Projekt-Repo mit `claude --remote-control` anlegen und den Prompt dort einfügen, nicht absenden.
   Ablauf: [references/neues-fenster.md](references/neues-fenster.md).
6. Fertig. Kurzform (nur Startprompt) nur auf ausdrücklichen Wunsch.

---

## Ablauf im Cowork-Chat

Der Chat hat kein Repo-Gedächtnis, der Handover-Prompt trägt den Stand. Die Einzelheiten stehen in den References:

1. **ClickUp-Abgleich** vor dem Übergabeprompt: [references/tracker-abgleich.md](references/tracker-abgleich.md).
2. **Memory-Scan** nach den Rubriken, erledigte Merker nur mit Bestätigung entfernen:
   [references/cowork.md](references/cowork.md), Abschnitt „Memory-Scan (PFLICHT bei Handover)“.
3. **Chat-Anker-Übergabe:** `[ANKER-LIVE]` in den Prompt übernehmen, nach der Prompt-Erstellung aus dem Memory leeren:
   [references/cowork.md](references/cowork.md), Abschnitt „Chat-Anker-Übergabe (nur Cowork)“.
4. **Chat-URL** des endenden Chats ermitteln: [references/cowork.md](references/cowork.md), Abschnitt „Chat-URL in
   Übergabe-Prompt (nur Cowork)“.
5. **Link-Prüfung** (unten).
6. **Handover-Prompt** nach [references/prompt-struktur.md](references/prompt-struktur.md) als Markdown-Codeblock direkt
   im Chat ausgeben.

---

## Link-Prüfung (PFLICHT vor der Ausgabe)

Jeder Verweis im Prompt muss stimmen, sonst startet die nächste Sitzung mit falschen Annahmen
(Beispiel: `heidi-panel-v2.js`, das seit dem Umbau `dreame_x60.js` heißt).

1. **Dateien und Pfade:** jede genannte Datei existiert (Claude Code: Glob; Cowork: DC `list_directory`)
2. **Abschnitte:** genannte Kapitel/Abschnitte existieren in der Datei (Grep auf die Überschrift)
3. **Task-IDs:** jede `<PRÄFIX>-NNN` existiert im Tracker mit dem genannten Status (tracker read-only, `clickup_get_task`)
4. **Versionen:** Version im Prompt = Versionsquelle des Commit-Profils (Heidi: package.json)
5. Tote Verweise → Auswahlfrage „Korrigieren / Mit Warnung übernehmen / Weglassen“; nie stumm übernehmen

---

## REGELN

1. Automatisch sammeln — nicht nachfragen was rein soll
2. Chat-Nummer korrekt — N+1
3. Nichts vergessen — inkl. pending Frontmatter, neue Invarianten
4. Kompakt aber vollständig
5. Kopierfähig als Markdown-Codeblock
6. Version prüfen
7. Keine Datei — direkt im Chat; Claude Code: zusätzlich vorher Stand ins Repo (Modus 8)
8. Pending Quickload-Änderungen explizit nennen
9. **ClickUp-Abgleich VOR Übergabeprompt** — offene Tasks laden + Chat scannen
10. **Batch-Abschluss per Auswahlfrage** (nicht Prosa-Liste)
11. **Keine automatischen ClickUp-Mutationen ohne Auswahlfrage-Bestätigung**
12. **Nächste Schritte basierend auf V1 + Priority ableiten**
13. **Sonstige offene Punkte** (Pending Commits, Frontmatter, Invarianten) ZUSÄTZLICH zu ClickUp auflisten
14. **Aktuelle Chat-URL** in Übergabe-Prompt einfügen (für Nachpflege)
15. **`[ANKER-LIVE]` aus Memory in Übergabeprompt kopieren** und danach aus Memory leeren — Anker reisen per Prompt, nicht per Memory
16. **Memory-Scan nach 4 Rubriken** (`[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]`, `[REVIEW-PENDING]`) durchführen und als Sektion `## Offene Punkte aus Memory` in Prompt einfügen
17. **Memory-Cleanup nur mit Bestätigung** — bei Einträgen die in diesem Chat bearbeitet wurden per Auswahlfrage fragen, nie stillschweigend entfernen
18. **Link-Prüfung vor der Ausgabe** — Dateien, Abschnitte, Task-IDs, Version (Abschnitt „Link-Prüfung“)
19. **Regeln-Block aus den Profilen** erzeugen, nicht aus einer festen Liste
20. **Claude Code: erst doc-pflege Modus 8, dann vollständiger Handover-Prompt** — Kurzform nur auf Wunsch; Details verweisen auf HANDOFF/Bauplan statt sie zu kopieren

---

## VERBOTEN

- Nachfragen was rein soll (Prosa)
- Offene Punkte vergessen
- Als Datei liefern
- Ohne Version/Chat-Nummer
- Nummern verwechseln
- Pending Frontmatter/Invarianten vergessen
- Branch automatisch annehmen – ohne Branch-Policy, Shell oder Auswahlfrage
- **Prosa-Fragen bei festen Entscheidungsoptionen** — IMMER Auswahlfrage (Branch-Auswahl, Batch-Abschluss, "ja/nein/einzeln wählen")
- **Tasks automatisch in ClickUp erstellen/schließen ohne Auswahlfrage-Bestätigung**
- **ClickUp-Schreiboperationen direkt ausführen (→ tracker-Skill nutzen)**
- **Pending Commits/Doc-Updates/Frontmatter-Updates vergessen nur weil ClickUp da ist**
- Chat-URLs raten oder erfinden — bei Unsicherheit Feld leer lassen
- **`[ANKER-LIVE]`-Einträge im alten Chat-Memory belassen nach Übergabe** — müssen geleert werden
- **Anker-Sektion im Prompt als leere Tabelle einfügen wenn keine Anker vorhanden** — dann Sektion komplett weglassen
- **`[CLICKUP]`- oder `[SKILL-ISSUES]`-Memories in Handover-Prompt übernehmen** — das sind dauerhafte Konventionen, nicht offene Punkte
- **Rubriken `[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]`, `[REVIEW-PENDING]` als leere H3-Blöcke einfügen** wenn Rubrik keine Einträge hat
- **Memory-Einträge stillschweigend entfernen nach Abschluss** — Herbert muss explizit bestätigen
- **Prompt mit toten Verweisen ausgeben** (umbenannte Dateien, fehlende Abschnitte, falsche Task-IDs oder Version)
- **BPM-Regeln oder BPM-NNN in den Prompt eines anderen Projekts schreiben** — Regeln und Präfix aus den Profilen
- **In Claude Code den Stand nur in den Prompt schreiben statt ins Repo** (HANDOFF/Bauplan) — Modus 8 kommt immer zuerst
- **In Claude Code ungefragt nur den kurzen Startprompt liefern** — der User erwartet den vollständigen Handover-Prompt
- **Sitzung mit uncommitteten Änderungen übergeben** ohne Auswahlfrage
- **Den Prompt im neuen Fenster selbst absenden oder das alte Fenster schließen** — beides entscheidet der User
