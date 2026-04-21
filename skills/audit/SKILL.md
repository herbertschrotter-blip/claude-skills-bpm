---
name: audit
description: >
  Prüft Konsistenz zwischen BPM-Code, INDEX-Routing, Frontmatter, Quickloads
  und Projektdokumentation. Use when users want a consistency audit, a
  documentation-vs-code check, a Frontmatter or Quickload validation, or a
  systematic read-only review of project rules. Do not trigger for code
  implementation, build debugging, or general code review without doc/context
  comparison.
---

# Audit-Skill — Projekt-Konsistenz-Prüfung

## Zweck

Prüft ob Code, Docs, Frontmatter und Quickload konsistent sind.

## 🚨 VERBINDLICHE REGEL: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0`
verwendet werden — KEINE Prosa-Fragen.**

### Diese Fragen IMMER mit ask_user_input_v0:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (unbekannt) | Branch-Namen aus `git branch -a` |
| Modus-Auswahl (A oder B) | Vollaudit, Teilaudit, Abbrechen |
| Teilaudit: welches Modul | Modul-Namen aus INDEX.md |
| Vollaudit-Warnung vor Start | Starten, Als Teilaudit starten, Abbrechen |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen
- User hat Präferenz signalisiert

## Branch-Ermittlung

Branch aus Chat-Kontext verwenden.
Wenn Branch in dieser Session noch nicht bekannt: Per ask_user_input_v0 fragen.
NIE automatisch einen Branch annehmen.

## Arbeitsverzeichnis (PFLICHT bei DC-Zugriff)

Bei DC-Operationen: Arbeitsverzeichnis nach **cc-steuerung Kapitel 4** ermitteln.

---

## Doc-Laderegel

Liest Docs nach DOC-STANDARD.md Kapitel 8:
1. INDEX.md → Routing
2. Frontmatter + Quickload → Filter
3. Fachliche Invarianten → Prüfen
4. Langform nur bei Bedarf

---

## 2 Modi

### Modus A — Vollaudit
Alle 6 Module. Token-intensiv — vor Start per ask_user_input_v0 bestätigen lassen.

### Modus B — Teilaudit
Nur relevantes Modul.

---

## Ablauf

### Schritt 1: INDEX.md laden
### Schritt 2: Prüfmodule

---

### Modul 1 — INDEX-Selbst-Check

- Routing-Einträge → Docs existieren?
- Code Entry Points → Dateien existieren?
- Referenzimplementierungen → existieren?
- Routing-Format korrekt (Primary/Secondary/Reference)?
- historical Docs als Primary? → ❌

---

### Modul 2 — Kern-Docs vs. Code

#### 2a. DB-Schema-Check
#### 2b. DSGVO-Check
#### 2c. Architektur-Check
#### 2d. UI-Konsistenz-Check

---

### Modul 3 — Code vs. Docs (Rückwärts)

#### 3a. Interface-Implementierung
#### 3b. DI-Registrierung
#### 3c. Dependencies
#### 3d. Code Entry Points

---

### Modul 4 — Referenz-Docs

#### 4a. ADR-Status
#### 4b. CHANGELOG-Vollständigkeit
#### 4c. BACKLOG-Aktualität

---

### Modul 5 — Modul-Docs

- Module/ vs. Konzepte/ Zuordnung
- INDEX Routing vollständig?

---

### Modul 6 — Frontmatter + Quickload + Kapitelstruktur

Für die detaillierten Prüfregeln siehe **doc-pflege Modus 6**
(Stufe A: Formal/Blocker, Stufe B: Semantisch/Warnung).

Kurzprüfung hier:

#### 6a. Frontmatter-Vollständigkeit
- Frontmatter vorhanden? Pflichtfelder? doc_id eindeutig?

#### 6b. Quickload-Vollständigkeit
- Quickload vorhanden bei source_of_truth/secondary?
- Kapitel-Feld stimmt mit H2s?

#### 6c. Cross-Checks
- INDEX referenziert nur Docs mit gültigem Frontmatter?
- source_of_truth hat Quickload?
- historical NICHT als Primary im Router?
- Keine doppelten doc_ids?
- Fachliche Invarianten nicht widersprüchlich zwischen Docs?

---

## Report-Format

```
🔍 Audit-Report [Projekt] ([Datum])
═══════════════════════════════════

📊 Zusammenfassung: X ✅ | Y ⚠️ | Z ❌

─── Modul 1–5 ───

──────────────────────────────────
Modul 6 — Frontmatter + Quickload
──────────────────────────────────
❌ [Doc]: [Problem]
⚠️ [Doc]: [Warnung]
✅ [Doc]: OK

═══════════════════════════════════
📝 Empfohlene Aktionen:
═══════════════════════════════════
1. ❌ [Aktion]
2. ⚠️ [Aktion]
```

---

## Ampel

| ✅ | Konsistent | — |
| ⚠️ | Inkonsistenz | Sollte korrigiert werden |
| ❌ | Fehler | Muss korrigiert werden |

---

## Tool-Strategie

- Frontmatter/Quickload: Nur erste 30 Zeilen jeder Doc
- Existenz: list_directory
- Content: start_search
- Teilaudit: max 10 Tool-Calls
- Vollaudit: max 35 Tool-Calls

---

## VERBOTEN

- Dateien ändern (read-only)
- Annahmen ohne Dateien
- False Positives als Fehler
- Vollaudit ohne ask_user_input_v0-Vorwarnung
- Quickload-Laderegel ignorieren
- Modus-Auswahl als Prosa — IMMER ask_user_input_v0
- Modul-Auswahl für Teilaudit als Prosa — IMMER ask_user_input_v0
- Branch automatisch annehmen ohne ask_user_input_v0
