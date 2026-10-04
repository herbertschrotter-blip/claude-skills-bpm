---
name: sitzung
description: >
  Verwaltet Claude-Code-Gespräche und tmux-Fenster per Auswahlmenü, auch am Smartphone: erst Projekt wählen, dann
  dessen Gespräche; ein Gespräch im richtigen Ordner in eigenem Fenster mit Remote Control fortsetzen oder hinwechseln,
  Vorschau, Suche, Abzweigen; Fenster wechseln, umbenennen, verschieben, holen, schließen, Claude neu
  starten; nach einem Neustart die offenen Fenster wiederherstellen; alte Gespräche archivieren oder löschen. Use when
  users type "sitzung" or "sitzungen", want an old chat or session found, resumed or reopened in its folder, ask where
  their sessions went, want Remote Control back on a chat, want tmux windows listed, switched, renamed, moved or
  closed, want windows restored after a terminal or add-on restart, or want old chats cleaned up. Do not trigger for
  handover prompts or "neuer chat" with handover (chat-wechsel), creating a new project (projekt-anlegen), editing
  tmux config or key bindings, skill-log analysis (skill-auswertung), or work inside the chat's project itself.
---

# sitzung – Gespräche und Fenster per Auswahl

## Zweck

Claude Code speichert jedes Gespräch unter dem Ordner, in dem es gestartet wurde, und `claude --resume` findet nur die
des aktuellen Ordners. Fenster in tmux gehen bei einem Neustart des Terminals verloren. Dieser Skill macht beides mit
wenigen Tipps bedienbar: Projekt wählen, Gespräch wählen, fertig – das Gespräch läuft im richtigen Ordner, mit Remote
Control, in einem eigenen Fenster.

- **Abgrenzung:** Übergabe an eine neue Sitzung mit Handover-Prompt → chat-wechsel (legt dafür selbst ein Fenster an).
  Neues Projekt → projekt-anlegen. Die Arbeit im geöffneten Gespräch macht der jeweilige Fachskill dort, nicht hier.
- **Umgebung:** nur Claude Code mit Shell; Fensterfunktionen nur, wenn tmux läuft. Ohne tmux gehen Liste, Suche,
  Vorschau und Aufräumen; fortsetzen dann mit dem Befehl aus [references/umgebung.md](references/umgebung.md).
- **Keine Projektwerte nötig.** Der Skill arbeitet über alle Ordner eines Rechners; die Pfade sind die von Claude Code
  (`~/.claude/projects`, `~/.claude/sessions`). Eigene Daten (Arbeitsplatz, Archiv) liegen unter `~/.claude/sitzung/`.

## Werkzeug

Die Arbeit macht `scripts/sitzung.py` im Ordner dieses Skills (Python 3, nur Standardbibliothek). Immer mit `--json`
aufrufen und aus dem Ergebnis die Menüs bauen; die Textausgabe ist für Menschen. Alle Befehle:
[references/befehle.md](references/befehle.md). Fehlt Python, gelten die Handgriffe aus
[references/umgebung.md](references/umgebung.md).

Begriffe: **Gespräch** = gespeicherte Claude-Code-Sitzung (ID, Name, Ordner). **Fenster** = tmux-Fenster.
**Hauptsitzung** = die tmux-Sitzung, in der dieses Gespräch läuft; neue Fenster kommen dorthin, damit sie mit einem
Tipp erreichbar sind.

## Grundsätze

- **Alles per Auswahlfrage.** Der Nutzer tippt am Smartphone; jede Entscheidung ist ein Menü, Freitext nur für Namen
  und Suchbegriffe. Höchstens vier Optionen je Frage: die drei wichtigsten und „Weitere …“ zum Blättern. Label kurz
  (Name), Beschreibung mit Datum, Zustand und Thema.
- **Erst Projekt, dann Gespräch.** Projekt = Ordner, in dem Gespräche liegen.
- **Ein Gespräch läuft nie doppelt.** Läuft es schon, wird nur hingewechselt (das Skript prüft das).
- **Remote Control ist Standard** beim Öffnen; ohne nur, wenn der Nutzer es abwählt.
- **Löschen ist endgültig** und kommt nur nach eigener Auswahlfrage mit Name und Datum; sonst archivieren
  (zurückholbar).
- **Das eigene Fenster** nie schließen, verschieben oder neu starten.

## Ablauf bei „sitzung“

Direkte Wünsche überspringen die Menüs („sitzung fenster“, „sitzung wiederherstellen“, „öffne die Tickets-Sitzung von
ha-baustelle“): gleich zum passenden Abschnitt.

### 1. Lage holen

`projekte --json`, `fenster --json` und `wiederherstellen --json` (ohne Angabe: nur Kandidaten). Gibt es Kandidaten zum
Wiederherstellen und läuft außer diesem Gespräch kein Claude-Fenster, ist das ein Neustart: dann zuerst
**Wiederherstellen** anbieten.

### 2. Projekt wählen (Auswahlfrage)

Die drei zuletzt aktiven Projekte (Label: Ordnername; Beschreibung: „N Gespräche · zuletzt <Datum> · M laufen“) und
„Weitere …“. „Weitere …“ zeigt die nächsten Projekte und die Werkzeuge: **Fenster**, **Wiederherstellen**, **Suchen**,
**Aufräumen**.

### 3. Gespräch wählen (Auswahlfrage)

`liste --ordner <ordner> --json`. Die drei neuesten Gespräche (Label: Name; Beschreibung: „<Datum> · ruht/wartet/arbeitet
· <Kontext>k · <Thema>“) und „Weitere …“ (ältere Gespräche, dann „Neues Gespräch hier“). Ein laufendes Gespräch nennt sein Fenster.

### 4. Aktion wählen (Auswahlfrage)

- **Öffnen (Recommended)** – `oeffnen <id>`: neues Fenster im Ordner des Gesprächs, Name = Gesprächsname,
  `claude --resume <id> --remote-control "<name>"`, Ansicht wechselt dorthin. Läuft es schon: nur hinwechseln.
- **Vorschau** – `vorschau <id>`: die letzten Nachrichten in drei bis fünf Zeilen zusammenfassen, dann die Frage erneut.
- **Abzweigen** – `oeffnen <id> --abzweigen --name "<name> (Kopie)"`: Kopie fortsetzen, das Original bleibt.
- **Mehr …** – Umbenennen (Name als Freitext; läuft das Gespräch, dort `/rename` nutzen), Archivieren, Löschen.

Nach dem Öffnen melden: Fenster (Sitzung:Nummer, Name), Ordner, Remote Control an, wie man zurückkommt
(Fensterleiste antippen oder `Strg+b w`). Dieses Fenster bleibt offen.

### Fenster

`fenster --json` zeigt alle Fenster aller tmux-Sitzungen mit Ordner, Gespräch und Zustand (arbeitet, wartet, Shell).
Fenster wählen (Auswahlfrage, Fenster der Hauptsitzung zuerst), dann Aktion:
- **Wechseln**, **Umbenennen** (Freitext), **Verschieben** (Zielstelle als Auswahl), **Neu starten** (Claude im Fenster
  neu, Gespräch bleibt – bei hängendem Claude), **Schließen** (Rückfrage; arbeitet Claude dort gerade, erst warten).
- Fenster in **anderen tmux-Sitzungen** sieht man am Smartphone schlecht, weil das Terminal sich nur an die
  Hauptsitzung hängt: **In Hauptsitzung holen** anbieten (`holen`, ohne Angabe alle).

### Wiederherstellen

Kandidaten sind die gemerkten Fenster (`merken`) und die Gespräche, die beim letzten Beenden noch offen waren (Claude
hinterlässt dann einen verwaisten Eintrag). Auswahlfrage mit Mehrfachauswahl, zuletzt aktive zuerst, dazu „Alle“.
Dann `wiederherstellen <id> …` bzw. `--alle`. Danach `merken`, damit der neue Stand gilt. Nach jedem Öffnen,
Schließen oder Holen von Fenstern ebenfalls `merken`.

### Suchen

Suchbegriff als Freitext, `suche "<text>" --json`. Die drei Gespräche mit den meisten Treffern als Auswahl
(Beschreibung: Ordner, Datum, eine Fundstelle), dann weiter mit Aktion wählen.

### Aufräumen

- **Kaum genutzte Gespräche** – `leer --json`: Fehlstarts und reine Startbefehle. Mehrfachauswahl → `archivieren`.
- **Archiv ansehen** – `archiv --json`: Zurückholen (`zurueckholen`) oder endgültig löschen.
- **Endgültig löschen** – nur aus dem Archiv heraus anbieten, eigene Auswahlfrage „<Name> vom <Datum> endgültig
  löschen?“ (Ja / Nein), dann `loeschen <id> --ja`.

## VERBOTEN

- ein Gespräch ein zweites Mal starten, während es schon läuft
- löschen ohne eigene Bestätigung mit Name und Datum, oder ein laufendes Gespräch archivieren oder löschen
- das eigene Fenster schließen, verschieben oder neu starten; ein Fenster schließen, in dem Claude gerade arbeitet,
  ohne Rückfrage
- in einem anderen Fenster Eingaben absenden oder dort weiterarbeiten
- Gesprächsdateien von Hand ändern; nur über das Skript
- Prosa-Fragen, wo ein Menü möglich ist

## VERWEIS

- Skript-Befehle: [references/befehle.md](references/befehle.md)
- tmux, Terminal-Add-on, Handgriffe ohne Skript: [references/umgebung.md](references/umgebung.md)
- Übergabe mit neuem Fenster → chat-wechsel (`skills/chat-wechsel/references/neues-fenster.md`)
