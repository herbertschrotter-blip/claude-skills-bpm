---
name: ticket
description: >
  Bearbeitet Fehler-Tickets eines Projekts (z.B. Heidi-Tickets HT-0007 aus dem Diagnose-Protokoll) einzeln und
  immer im selben Ablauf: Ticket holen, Befund erklären, mit dem User klären ob es ein echter Fehler ist, Ursache
  finden, Aufgabe im Tracker anlegen, Fix mit Test, einspielen, Ticket auf gelöst setzen – jeder Schritt mit
  Bestätigung, nichts automatisch. Use when users say "ticket HT-0007", "ticket liste", "offene tickets", "nimm
  das nächste ticket", "ticket verwerfen", "ticket notiz", "ticket schließen", or want to work through a
  reported bug or an automatically detected Auffälligkeit from the project's ticket system. Do not trigger for
  ClickUp-Aufgaben ohne Ticket (tracker), allgemeine Bugfixes ohne Ticketnummer (code-erstellen), Skill-Issues
  (tracker issue), Support-Tickets anderer Systeme, or general talk about errors without a ticket command.
---

# ticket — Fehler-Tickets einzeln und immer gleich bearbeiten

## Zweck

Ein Projekt sammelt Fehler als **Tickets**: Meldungen des Users („Fehler melden“) und Auffälligkeiten, die eine
Auswertung selbst findet. Dieser Skill sorgt dafür, dass jedes Ticket **gleich** bearbeitet wird – ein Ticket zur Zeit,
gemeinsam mit dem User, jeder Übergang mit Bestätigung. Er ist die Klammer um die Nachbarskills: **tracker** (Aufgabe),
**code-erstellen** (Fix + Test + Auslieferung), **git-commit-helper** (Commit), **doc-pflege** (Befund in die Doku).

Wo die Tickets liegen, wie sie heißen und wie man sie liest und ändert, steht im **Ticket-Profil** des Projekts –
nicht hier. Beispiele in diesem Skill zeigen das Projekt Heidi (`HT-NNNN`); sie sind Muster, keine Vorgabe.

**Umgebung:** Der Skill braucht eine Shell mit Zugriff auf das Ticket-System des Projekts. Das ist in der Regel
**Claude Code**. Im Cowork-Chat funktioniert er nur, wenn dort eine Shell verfügbar ist (Desktop Commander); sonst
liefert er die Befehle, und der User führt sie aus und fügt die Ausgabe ein.

---

## 🚨 Kernregeln

1. **Ein Ticket zur Zeit.** Kein zweites Ticket beginnen, bevor das erste `gelöst`, `verworfen` oder ausdrücklich
   zurückgestellt ist. Warum: Tickets teilen sich oft eine Ursache; wer springt, behebt Symptome.
2. **Nichts automatisch.** Jeder Statuswechsel und jeder Schritt mit Wirkung (Aufgabe anlegen, Code ändern, einspielen,
   Ticket lösen/verwerfen) braucht vorher eine **Auswahlfrage**. Auswahlfrage = Frage-Werkzeug der Umgebung mit
   anklickbaren Optionen (Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion`). Keine Prosa-Fragen bei festen Optionen.
3. **Das Ticket ist die Quelle.** Immer zuerst das Ticket mit den gesicherten Beweisen holen (Befehl aus dem Profil) –
   nie aus dem Gedächtnis oder aus der Liste heraus arbeiten. Die Beweise sind beim Anlegen gesichert worden, weil
   die Protokolle später gelöscht werden.
4. **Einziger Schreibweg.** Tickets nur über die Befehle des Profils ändern, nie die Ticket-Datei direkt bearbeiten.
5. **Aufgaben nur über tracker, Code nur über code-erstellen.** Dieser Skill legt selbst keine Aufgaben an und
   schreibt selbst keinen Code; er ruft die Nachbarskills auf und hält das Ticket aktuell.
6. **Schließen macht der User.** `gelöst` setzt Claude nach dem Einspielen; `geschlossen` erst, wenn der User
   geprüft und bestätigt hat.
7. **Einfach erklären.** Der Befund wird in zwei bis vier Sätzen ohne Fachwörter erklärt, bevor irgendetwas passiert.

---

## Voraussetzung: Ticket-Profil

Abschnitt `## Ticket-Profil` in der `CLAUDE.md` des Repos (Claude Code liest sie automatisch). Felder:

| Feld | Bedeutung | Beispiel (Heidi) |
|------|-----------|------------------|
| Präfix | Nummernschema der Tickets | `HT-NNNN` |
| Befehle | Liste, Ticket als Text, Status, Notiz, Verwerfen, Auswertung anstoßen | `.\tools\ticket.ps1 liste [alle]` · `zeige <nr>` · `status <nr> <status> [-Dx -Commit -Version]` · `notiz <nr> "<text>"` · `verwerfen <nr> "<grund>"` · `auswertung` |
| Status | Werte und Reihenfolge | `neu → angenommen → in_arbeit → geloest → geschlossen`, daneben `verworfen` |
| Pflichtangaben | was ein Status braucht | angenommen → Aufgaben-Nummer · geloest → Commit (+ Version) · verworfen → Grund |
| Aufgaben | wie das Ticket zur Tracker-Aufgabe wird | tracker neu, Titel „`<Präfix-Nr>`: `<Kurztitel>`“, Ticket-Text in die Beschreibung |
| Beweise nachlesen | Rohdaten rund um das Ticket | `node tools\diag.js --tag <Tag> --von <HH:MM> --bis <HH:MM> --debug` |
| Regeln | wo die Regeln der Auswertung stehen | `ha/prognose/diag_regeln.py`, Bauplan Karte F.2 |
| Doku | wo Befund und Entscheidung landen | Bauplan Abschnitt 10 |

**Fehlt das Profil:** Auswahlfrage „Profil jetzt anlegen (ich schlage Werte aus dem Repo vor)“ / „Ohne Profil, ich
nenne die Befehle“ / „Abbrechen“. Nie raten, nie die Heidi-Werte für ein anderes Projekt annehmen.

---

## Kommandos

| Kommando | Was passiert |
|----------|--------------|
| `ticket liste` / „offene tickets“ | Liste holen (Profil-Befehl), als kurze Tabelle zeigen: Nummer, Status, Anzahl, Titel. Danach Auswahlfrage „Welches Ticket?“ (höchstens 4 Optionen: die wichtigsten offenen + „Keines“) |
| `ticket <Nr>` / „nimm das nächste ticket“ | **Ablauf** unten, Schritt 1–8. „Das nächste“ = ältestes offenes Ticket mit der höchsten Schwere; vor dem Start bestätigen lassen |
| `ticket notiz <Nr> <Text>` | Notiz anhängen (Profil-Befehl), Quittung |
| `ticket verwerfen <Nr>` | Grund erfragen, wenn keiner genannt ist (Freitext), dann verwerfen, Quittung |
| `ticket schließen <Nr>` | Nur wenn Status `geloest`: Auswahlfrage „Hast du geprüft, dass es behoben ist?“ → `geschlossen` |
| `ticket auswertung` | Auswertung sofort anstoßen (Profil-Befehl), Ergebnis in einem Satz |

Quittung nach jeder Änderung: `🎫 <Nr> — <alter Status> → <neuer Status> — <Kurztitel>`.

---

## ABLAUF für `ticket <Nr>` (immer diese acht Schritte)

### Schritt 1 — Ticket holen und einfach erklären
Ticket als Text holen (Profil-Befehl „zeige“). Dann in zwei bis vier Sätzen sagen: **Was ist passiert? Woran sieht
man es? Wie oft? Seit wann?** Bei Meldungen des Users: seinen Text wörtlich zitieren. Keine Lösung vorschlagen, bevor
Schritt 2 geklärt ist. Ist das Ticket schon `in_arbeit` oder `geloest`: den Stand nennen und bei diesem Schritt weitermachen.

### Schritt 2 — Echter Fehler? (Auswahlfrage)
Optionen: „Ja, echter Fehler – weiter“ · „Kein Fehler – verwerfen“ · „Unklar – erst Beweise ansehen“ · „Später“.
- **Verwerfen:** Grund in einem Satz (vom User oder vorgeschlagen und bestätigt) → Profil-Befehl → Ende.
- **Unklar:** Beweise nachlesen (Profil „Beweise nachlesen“), Ergebnis erklären, Frage noch einmal stellen.
- Liegt die Ursache erkennbar **in der Auswertung selbst** (Regel schlägt falsch an), ist das ein echter Fehler –
  der Fix gehört dann in die Regel, nicht in das geprüfte Programm.

### Schritt 3 — Ursache suchen
„Wo suchen“ aus dem Ticket als Startpunkt nehmen, Code und Doku lesen, Hypothese bilden und **belegen** (Stelle im
Code, Zeile im Protokoll, Rohmeldung). Ergebnis: Ursache in einfachen Worten + betroffene Dateien + Vorschlag für
den Fix + grober Aufwand. Bei mehreren Wegen: Auswahlfrage mit Empfehlung. Findet sich keine Ursache: Notiz ans Ticket
(was geprüft wurde), Auswahlfrage „Weiter suchen / Zurückstellen / Verwerfen“.

### Schritt 4 — Aufgabe anlegen (tracker)
Auswahlfrage „Aufgabe für `<Nr>` anlegen?“ → **tracker neu** nach dem Schema des Projekts (Profil „Aufgaben“; der
Ticket-Text kommt in die Beschreibung, Akzeptanz = „Ticket tritt nicht mehr auf“ + der neue Test). Danach Ticket auf
`angenommen` mit der Aufgaben-Nummer, dann **tracker start** und Ticket auf `in_arbeit`. Kleine Fixes ohne eigene Aufgabe
nur, wenn der User das per Auswahlfrage so entscheidet („Ohne Aufgabe, direkt beheben“) – dann bleibt das Ticket ohne
Aufgaben-Nummer und geht direkt auf `in_arbeit`, falls das Profil das erlaubt.

### Schritt 5 — Fix mit Test (code-erstellen)
An **code-erstellen** übergeben: Pflicht-Docs, Impact Check, Fix, und **ein Test, der ohne den Fix rot wäre**
(der Fall aus dem Ticket). Bei größeren Änderungen an der Oberfläche gilt die Mockup-Pflicht des Projekts.

### Schritt 6 — Einspielen
Tests grün → Commit (git-commit-helper-Format, Ticketnummer im Kurztitel) → Auslieferung nach dem Code-Profil.
Vor dem Einspielen Auswahlfrage, wenn es den Betrieb stört (Neustart, laufender Auftrag).

### Schritt 7 — Ticket lösen
Ticket auf `geloest` mit Commit und Version (Profil-Befehl), Notiz mit Ursache und Fix in zwei Sätzen, **tracker done**
für die Aufgabe, Befund in die Doku (Profil „Doku“, über doc-pflege bzw. die Doku-Checkliste des Commit-Profils).
Dann dem User sagen, **woran er prüfen kann**, dass es behoben ist.

### Schritt 8 — Prüfung durch den User
Auswahlfrage „Behoben?“: „Ja – schließen“ → `geschlossen` · „Nein – tritt wieder auf“ → zurück auf `in_arbeit`, Schritt 3 ·
„Prüfe ich später“ → bleibt `geloest`. Tritt ein gelöstes Ticket später wieder auf, öffnet das Ticket-System es selbst neu –
dann beginnt der Ablauf bei Schritt 1 mit dem Hinweis „wieder aufgetreten“.

Zum Schluss Auswahlfrage „Nächstes Ticket / Liste zeigen / Schluss für heute“.

---

## VERBOTEN

- Mehrere Tickets gleichzeitig bearbeiten oder „gleich mit erledigen“
- Status ändern, Aufgabe anlegen, Code ändern oder einspielen **ohne** vorherige Auswahlfrage
- Ein Ticket aus der Liste heraus bearbeiten, ohne es mit den Beweisen geholt zu haben
- Die Ticket-Datei direkt bearbeiten (nur Befehle des Profils)
- Aufgaben direkt im Tracker-System anlegen (nur über tracker) oder Code ohne code-erstellen ändern
- `geschlossen` setzen, ohne dass der User geprüft hat
- Einen Fix ohne Test, der den Fall aus dem Ticket abdeckt
- Tickets verwerfen ohne Grund, oder weil die Ursache unbequem ist
- Profilwerte eines Projekts (Präfix, Befehle, Pfade) für ein anderes annehmen
- Fachwörter ohne Erklärung in Schritt 1 und 3
- Prosa-Fragen bei festen Entscheidungsoptionen

---

## VERWEIS

- **tracker** – Aufgabe anlegen, starten, abschließen (einzige Schreibschnittstelle zum Tracker)
- **code-erstellen** – Fix, Test, Auslieferung nach dem Code-Profil
- **git-commit-helper** – Commit-Format; Ticketnummer gehört in den Kurztitel
- **doc-pflege** – Befund und Entscheidung in die Projekt-Doku
- **chat-wechsel** – offene Tickets gehören in die Übergabe (Liste der offenen Tickets mit Status)
