# Smoke-Eval Methodik-Anleitung

> **Zweck:** Anleitung für Tester (Herbert + Claude) zur Durchführung von Smoke-Eval-Runs für das BPM-Skill-System. Ergänzt `evals/smoke-all-skills.md` um Test-Setup-Regeln, die in der Praxis aus Smoke-Run 2026-04-28 (Teil 33) abgeleitet wurden.
>
> **Entstehung:** ClickUp `chat-wechsel-001` — Methodik-Befund aus Smoke-Run 2026-04-28.

---

## 1. Standard-Setup

Für jeden Case der Smoke-Eval gilt:

- **Frischer Chat** in Claude.ai Web (nicht in einem bestehenden Projekt-Chat)
- **Memory aus** (oder Memory leer)
- **Skills aktiv** (alle 11 BPM-Skills installiert)
- **Eine Query pro Chat** — nicht mehrere Queries in einem Chat
- Pro Case dokumentieren:
  - Welcher Skill triggerte (Loading-Indikator)
  - Erste Aktion (Tool-Calls, ask_user_input_v0, fragt nach, schreibt direkt)
  - Status: PASS / WARN / FAIL

---

## 2. Demonstrativ-Bezug-Regel (KRITISCH)

**Befund aus Smoke-Run 2026-04-28:** Queries mit Demonstrativ-Bezug ("der/die/das + bestehend/neu/letzt") sind in leeren Sessions **nicht zuverlässig testbar**. Sie brauchen Vor-Kontext.

### Was ist ein Demonstrativ-Bezug?

Pronomen oder Artikel die auf etwas Vorheriges verweisen:

- "der **bestehende** Dialog" → welcher?
- "die **neue** Recovery-Logik" → welche?
- "die Inkonsistenz" → welche?
- "**das** ADR für die Entscheidung" → welche Entscheidung?
- "**diesen** Bug" → welchen?

### Was tut Claude in leerer Session?

Bei Demonstrativ-Bezug ohne Vor-Kontext fragt Claude **immer** zuerst nach Inhalt — was ist richtig und gewollt. Aber: das wird leicht als "Skill triggert nicht" missinterpretiert, obwohl der Skill korrekt in einer Standby-Phase wartet.

### Lösung: Vor-Konversation aufbauen

Bei Cases mit Demonstrativ-Bezug **vor** der eigentlichen Query 2-3 Vor-Nachrichten zum Etablieren des Bezugs senden.

#### Beispiel — MU-07 Setup

```
Nachricht 1: ich hab gerade den ImportPreviewDialog im PlanManager-Modul fertig
            gemacht. der zeigt eine vorschau der zu importierenden pläne.

Nachricht 2: in dem dialog ist der bestätigen-button rechts unten aber zu klein
            und das padding zwischen den listen-spalten ist zu eng.

Nachricht 3 (= MU-07-Query): kleiner UI-Fix im bestehenden Dialog
```

→ Erst nach Nachricht 3 wird der Skill korrekt getriggert. Die Demonstrativ-Verweise sind etabliert.

#### Cases mit nötigem Vor-Kontext (Liste)

Aus Smoke-Run 2026-04-28:

| Case | Query | Demonstrativ | Vor-Kontext |
|---|---|---|---|
| MU-07 | `kleiner UI-Fix im bestehenden Dialog` | "bestehenden" | Dialog erwähnen + Mängel beschreiben |
| DOC-06 | `implementiere die neue Recovery-Logik` | "neue" | Konzept skizzieren + Recovery-Idee benennen |
| AUD-07 | `fix die Inkonsistenz im DB-Schema` | "die Inkonsistenz" | Inkonsistenz konkret nennen |
| CE-07 | `schreib ein ADR für die Entscheidung` | "die Entscheidung" | Entscheidung im Vor-Kontext erwähnen |

### Wann KEIN Vor-Kontext nötig

Cases mit konkreten Substantiven oder Eigennamen funktionieren auch in leeren Sessions:

- ✅ `cc bau die neue View für ProfileWizard` (ProfileWizard ist konkret)
- ✅ `erstelle ein Mockup für den ProfileWizard` (ProfileWizard ist konkret)
- ✅ `erstelle die CommitService.cs` (.cs-Datei ist konkret)

---

## 3. chat-wechsel-Spezialfall

Der `chat-wechsel`-Skill hat eine **eigene** Test-Setup-Falle: Er erstellt einen Handover-Prompt für die nächste Session — basierend auf der **aktuellen** Session.

In einer leeren Session existiert kein "aktuell zu übergebender Inhalt", also reagiert Claude mit einer normalen Begrüßung statt einen Handover zu bauen. Das ist **korrektes Skill-Verhalten**, kein Bug.

### Realistisches Test-Setup für chat-wechsel

Vor `neuer chat` / `chat-wechsel` zuerst eine Mini-Konversation aufbauen:

```
Nachricht 1: ich arbeite gerade am PlanManager. die Settings-View ist fast fertig,
            morgen will ich noch das Wizard-Modal fertigmachen.

Nachricht 2: bin müde, mach Schluss für heute.

Nachricht 3 (= chat-wechsel-Query): neuer chat
```

→ Jetzt hat chat-wechsel echten Kontext (PlanManager-Settings-View, Wizard-Modal-Plan, Sessions-Ende).

---

## 4. Testen vs. Skill-Bug — Diagnose-Checkliste

Wenn ein Smoke-Test als FAIL klassifiziert wird, folgende Fragen durchgehen:

1. **Ist die Query selbsterklärend?** (kein Demonstrativ-Bezug, konkrete Substantive)
   - Ja → echter FAIL möglich
   - Nein → Re-Test mit Vor-Kontext nötig

2. **Reagiert Claude mit "Welche/r/s X meinst du?"**
   - Ja → wahrscheinlich Demonstrativ-Bezug ohne Kontext, KEIN Skill-Bug
   - Nein → Skill triggert wirklich nicht

3. **Wird der Skill in der Antwort wenigstens benannt?** ("Das ist ein Trigger für X")
   - Ja → Skill ist aktiv, nur Workflow blockiert auf Eingabe
   - Nein → Skill triggert nicht

4. **Hat der Loading-Indikator den Skill geladen?** ("X Skill lesen")
   - Ja → triggert, FAIL ist Workflow-Issue
   - Nein → echter Trigger-FAIL

→ Erst wenn 1, 2 und 4 negativ sind, ist es ein echter Skill-Bug. Sonst ist es ein Test-Setup-Problem.

---

## 5. Snapshot-Format

Pro Run eine eigene Snapshot-Datei unter `evals/runs/smoke-<YYYY-MM-DD>-<modus>.md`:

- Header: model, tester, mode, repo-ref, Quelle
- Pro Block eine Tabelle: ID, Query, ERW-Skills, TAT-Skills, Aktion, Status, Notiz
- Summary-Tabelle pro Skill (PASS/WARN/FAIL)
- Failures-Tabelle mit Diagnose und Action
- Hauptbefunde

Beispiel: `evals/runs/smoke-2026-04-28-real.md`

---

## 6. Re-Test nach Skill-Refactor

Nach jedem Description-Refactor:

1. Repo-Update via DC + Artifact für Two-Place-Sync
2. Push + Skill speichern in Claude.ai
3. **Frischer Chat** für Re-Test der ehemaligen FAILs
4. Wenn FAIL → PASS: Issue auf complete + Hash + Anker
5. Wenn FAIL bleibt FAIL: weitere Description-Iteration nötig

⚠️ **Wichtig:** Skill-Updates wirken erst in **neu gestarteten Sessions**. Bestehende Chats nutzen die alte Skill-Version.

---

## 7. Bias-Hinweis: Selbst-Simulation ist nicht Re-Test

Eine "Selbst-Simulation" durch dieselbe Claude-Instanz, die das Skill-System aus dem System-Prompt kennt, hat **kognitiven Bias**. Sie unterschätzt FAILs.

Konkret aus Teil 33: Selbst-Sim hatte 4 falsche PASS-Vorhersagen, die im echten Run als FAIL durchschlugen (CE-02, CE-07, DOC-06, SN-07).

→ **Selbst-Sim ist nur eine Vorprüfung des Katalogs**, kein Ersatz für echte Runs in frischen Sessions.

---

## Verweise

- `evals/smoke-all-skills.md` — Hauptkatalog Smoke-Cases
- `evals/runs/smoke-2026-04-28-real.md` — Beispiel-Snapshot mit Befunden
- ClickUp `chat-wechsel-001` (`86c9hyt0c`) — Issue-Quelle dieser Anleitung
