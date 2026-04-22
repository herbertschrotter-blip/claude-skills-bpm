# Test-Prompts für skill-neu

Vorlage und gleichzeitig Live-Test-Set für `skill-neu` selbst (Meta-Test: triggert der Skill-Erstellungs-Skill bei den richtigen Sätzen?).

---

## Should trigger (Trigger-Cases)

1. "Bau mir einen neuen Skill für das Wetter-Modul."
2. "Ich brauch einen Skill der Konzept-Docs nach DOC-STANDARD anlegt — kannst du den von Grund auf entwerfen?"
3. "Lass uns einen neuen Skill von null aufbauen, der mir bei der Foto-Modul-Planung hilft."
4. "Entwirf eine SKILL.md für ein neues Use-Case: automatisches Diary-Backup. Inkl. Description-Schema und Test-Prompts."
5. "Ich will einen Skill der bei meinen Bautagebuch-Einträgen triggert — wie geh ich das systematisch an?"

---

## Should NOT trigger (Catch-all-Tests)

1. "Pass die Description vom tracker-Skill an, dass er mehr triggert."
   → sollte `skill-pflege` triggern, nicht `skill-neu` (bestehender Skill)

2. "Lauf doch mal die Evals für den tracker-Skill durch."
   → automatisierte Eval-Runner gibts nicht in claude.ai → kein skill-neu-Trigger

3. "Welche Skills hab ich überhaupt?"
   → reine Inspektions-Frage, kein Skill-Erstellungs-Workflow

4. "Erstell mir eine neue Konzept-Doc für das Wetter-Modul."
   → Doc-Pflege, nicht Skill-Erstellung → sollte `doc-pflege` triggern

5. "Mach den tracker-Skill kürzer, der ist zu lang."
   → Änderung an existierendem Skill → `skill-pflege`

---

## Edge Cases (optional)

1. "Wir brauchen einen Skill für Wetter, oder besser eine Konzept-Doc — was meinst du?"
   → mehrdeutig: skill-neu sollte triggern und im Capture-Intent klären, ob wirklich ein Skill oder doch eine Doc gemeint ist

2. "Refactoring-Skill: nimm den skill-neu als Vorlage und mach was Eigenes draus."
   → grenzwertig: technisch Neu-Erstellung, aber stark abgeleitet von Bestand → skill-neu OK, im Interview klären

---

## Test-Log

| Datum | Prompt-ID | Erwartung | Ergebnis | Bemerkung |
|-------|-----------|-----------|----------|-----------|
| TBD | trigger-1 | trigger | – | initialer Live-Test offen |
| TBD | trigger-2 | trigger | – | – |
| TBD | trigger-3 | trigger | – | – |
| TBD | trigger-4 | trigger | – | – |
| TBD | trigger-5 | trigger | – | – |
| TBD | not-trigger-1 | NICHT trigger (skill-pflege) | – | – |
| TBD | not-trigger-2 | NICHT trigger | – | – |
| TBD | not-trigger-3 | NICHT trigger | – | – |
| TBD | not-trigger-4 | NICHT trigger (doc-pflege) | – | – |
| TBD | not-trigger-5 | NICHT trigger (skill-pflege) | – | – |

**Test-Vorgehen:** Im neuen Chat (sonst hat aktueller Chat den Skill schon im Speicher) jeden Prompt 3× senden, Ergebnis eintragen.

**Trigger-Rate-Schwelle:** ≥80% bei "should trigger"-Prompts, 0% bei "should NOT trigger"-Prompts. Bei Abweichung Description nachschärfen (siehe SKILL.md Schritt 9).
