# Test-Prompts für ticket

## Should trigger (Trigger-Cases)
1. (Claude Code) „ticket HT-0001“
2. (Claude Code) „ticket liste – welche Tickets sind offen, und welches sollten wir zuerst angehen?“
3. (Claude Code) „Nimm das nächste Ticket aus dem Diagnose-Protokoll und geh es mit mir durch.“
4. (Claude Code) „ticket verwerfen HT-0002, das war nur ein Test von mir“
5. (Cowork) „Ich habe in der Karte einen Fehler gemeldet, das Ticket heißt HT-0008 – bearbeite das bitte mit mir.“
6. (Claude Code) „HT-0004 ist behoben, ticket schließen“

## Should NOT trigger (Catch-all-Tests)
1. „tracker neu: Seite Dev bekommt eine Tagesauswahl“ → tracker
2. „Der Akku-Wert in der Karte ist falsch, bau das bitte um“ (keine Ticketnummer, kein Ticket-Befehl) → code-erstellen
3. „tracker issue tracker: create-task.md hat den falschen Inhalt“ → tracker (Skill-Issue)
4. „Ich habe beim Energieversorger ein Support-Ticket offen, formuliere mir eine Nachfrage“ → kein Skill
5. „Warum zeigt Heidi manchmal Bereit, obwohl sie fährt?“ (allgemeine Frage ohne Ticket) → normale Antwort, höchstens Hinweis auf „Fehler melden“

## Edge Cases
1. „ticket HT-0001 und HT-0004 zusammen erledigen“ → triggert, aber Regel „ein Ticket zur Zeit“: Auswahlfrage, welches zuerst
2. „ticket HT-0099“ (gibt es nicht) → triggert, meldet den Fehler des Ticket-Systems, bietet `ticket liste` an
3. Repo ohne Ticket-Profil: „ticket liste“ → Auswahlfrage Profil anlegen / Befehle nennen / Abbrechen

## Test-Log
| Datum | Umgebung (Cowork/Claude Code) | Prompt-ID | Erwartung | Ergebnis | Bemerkung |
|-------|-------------------------------|-----------|-----------|----------|-----------|
| 2026-09-18 | Claude Code | – | – | – | Skill angelegt; Ablauf vorab von Hand an HT-0004 durchgespielt (Ursache in der Auswertung, Fix 94be28f, Status gelöst) – Live-Trigger-Tests in neuer Sitzung offen |
