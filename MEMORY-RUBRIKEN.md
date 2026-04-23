# Memory-Rubriken-Konvention

**Zweck:** Strukturierte Ablage offener Punkte im Claude-Memory, die nicht
ClickUp-würdig sind. Die 4 Rubriken ergänzen das ClickUp-basierte Task-System.

---

## Die 4 Rubriken

| Prefix | Bedeutung | Beispiel |
|---|---|---|
| `[VERIFY]` | Ausstehende Prüfung/Verifikation | "ADR-046 Annahme: .bpm/ funktioniert mit OneDrive Hidden+System — testen" |
| `[ARCH-OPEN]` | Offene Architektur-/Systementscheidung | "Backup-Strategie für .bpm/ vor Import: eigenes Konzept oder Skip?" |
| `[INFRA-TODO]` | Kleine Infra-/Prozessaufgabe, nicht ClickUp-würdig | "Taskkill-Alias für BPM.exe in PowerShell-Profil einbauen" |
| `[REVIEW-PENDING]` | Externe Rückmeldung/Review-Antwort steht aus | "CGR-2026-04-bpm-architektur-r3: Rundenantwort von ChatGPT ausstehend" |

---

## Format

Pro Eintrag eine Memory-Zeile:

```
[<RUBRIK>] <Kurztext>
```

Beispiele:

```
[VERIFY] ADR-046: .bpm/ Hidden+System-Attribute funktionieren in OneDrive
[ARCH-OPEN] Backup vor Import - eigenes Konzept oder Skip?
[INFRA-TODO] PowerShell: Taskkill-Alias für BPM.exe einbauen
[REVIEW-PENDING] CGR-2026-04-bpm-architektur-r3: ChatGPT-Antwort ausstehend
```

---

## Lifecycle

**Erstellen:** Claude oder User legt Eintrag an wenn ein offener Punkt
entsteht, der nicht ClickUp-würdig ist (siehe Abgrenzung unten).

**Erledigen:** NUR nach expliziter Herbert-Bestätigung. Kein stilles
Entfernen. Siehe `skill-pflege` Memory-Cleanup-Regel (Phase 4.3).

**Eskalation zu ClickUp:** Wenn derselbe Eintrag bei 3 Handovers in
Folge steht oder sich zu einer substantiellen Aufgabe entwickelt,
`tracker neu` vorschlagen. Siehe `tracker` Memory-Eskalation (Phase 4.4).

---

## Abgrenzung zu ClickUp-Tasks

| Gehört in ClickUp | Gehört in Memory-Rubrik |
|---|---|
| Substantielle Arbeit (>30min) | Kleine Prüfung, Frage, Notiz |
| Kommt in Zielversion | Nicht versionsrelevant |
| Code/Doc/Konzept-Änderung | Meta-Frage, Verifikation |
| Mehrere Schritte | Ein-Schritt-Erledigung |
| Braucht Commit | Kein Commit |

**Faustregel:** Wenn unsicher → ClickUp. Memory-Rubriken sind für
Dinge, die sonst im Chat versinken würden.

---

## Abgrenzung zu anderen Memory-Konventionen

Folgende Memory-Konventionen sind KEINE offenen Punkte und bleiben ohne Rubrik-Prefix:

- `[CLICKUP]` — dauerhafte ClickUp-Config (Listen-IDs, next-free-number)
- `[SKILL-ISSUES]` — dauerhafte Skill-Issues-Config
- `[ANKER-LIVE]` — Live-Anker-Registry (eigener Lifecycle via `tracker/references/anker-system.md`)
- `[PROJECT]` — aktives Projekt

Die 4 Rubriken gelten NUR für offene Punkte.

---

## Skill-Integration

| Skill | Rolle | Phase |
|---|---|---|
| `chat-wechsel` | Scan bei Handover, Sektion "Offene Punkte aus Memory" erzeugen | 4.1 ✅ |
| `skill-neu` | Beim Skill-Anlegen Memory-Disziplin-Abschnitt aufnehmen | 4.2 |
| `skill-pflege` | Memory-Cleanup mit Bestätigung, kein stilles Remove | 4.3 |
| `tracker` | Memory-Eskalation: wiederholte Einträge → ClickUp-Task-Vorschlag | 4.4 |

---

## Initial-Cleanup bestehender Memory-Einträge

Bestehende Memory-Einträge ohne Rubrik-Prefix sind retrofit-fähig:

1. Memory-Scan: Welche Einträge existieren aktuell?
2. Pro Eintrag: passt eine Rubrik? → retrofit mit Prefix
3. Nicht-passende Einträge: bleiben ohne Prefix
   (`[CLICKUP]`, `[SKILL-ISSUES]`, `[ANKER-LIVE]`, `[PROJECT]` etc.)

Der Retrofit passiert auf Herbert-Ansage, nicht automatisch.
