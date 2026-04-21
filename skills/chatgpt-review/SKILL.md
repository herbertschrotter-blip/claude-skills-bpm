---
name: chatgpt-review
description: >
  Erstellt Prompts für ein Review-Gespräch zwischen Claude und ChatGPT.
  Verwende diesen Skill immer wenn der User sagt: "besprich das mit ChatGPT",
  "ChatGPT Review", "frag ChatGPT", "zweite Meinung von ChatGPT",
  "Cross-Review", "Prompt für ChatGPT", "weiter mit ChatGPT",
  "antworte darauf" (im Kontext eines laufenden ChatGPT-Reviews).
  Nutzt Quickloads verwandter Docs als Kontext im Initialprompt.
---

# ChatGPT Review-Gespräch

Ermöglicht strukturiertes Review zwischen Claude und ChatGPT.
Der User kopiert Prompts zwischen beiden und entscheidet.

## Branch-Ermittlung

Branch aus Chat-Kontext verwenden.
Wenn Branch in dieser Session noch nicht bekannt: Per ask_user_input_v0 fragen.
NIE automatisch einen Branch annehmen.

## 🚨 VERBINDLICHE REGEL: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0`
verwendet werden — KEINE Prosa-Fragen.**

### Diese Fragen IMMER mit ask_user_input_v0:

| Situation | Optionen |
|-----------|----------|
| Branch-Ermittlung (unbekannt) | Branch-Namen aus `git branch -a` |
| Phase 2 Stufe A: Entscheidungspunkte | je nach Review-Thema + immer "ChatGPT fragen" |
| Bei Uneinigkeit Claude/ChatGPT | Claude zustimmen, ChatGPT zustimmen, Mittelweg, Abbrechen |
| Review-Phase wechseln | In Phase 2, In Phase 3, Weiter in aktueller Phase |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen
- User hat Präferenz signalisiert
- Freitext-Input nötig

## Vor dem Start: ChatGPT-Modell

Falls der User schon gesagt hat welches Modell: nicht nochmal fragen.

## ChatGPTs Repo-Zugriff (PFLICHT in jedem Prompt)

ChatGPT hat die Möglichkeit selbst Dateien aus dem GitHub-Repo zu lesen.
**In JEDEM Prompt** (Initial, Folgeprompt, Audit) muss folgender Block enthalten sein:

```
## Repo-Zugriff

Du hast Zugriff auf das GitHub-Repo und kannst selbst Dateien lesen:
- **Repo:** [Owner/Repo aus INDEX.md]
- **Branch: `[aktueller Branch]`** — IMMER diesen Branch verwenden, NICHT `main`!
- Nutze das aktiv um Aussagen zu verifizieren, Querverweise zu prüfen,
  und Originaldateien zu lesen wenn der Kontext im Prompt nicht reicht.
- Bei JEDEM Dateizugriff den Branch `[aktueller Branch]` angeben!
```

**Regeln:**
- Branch NICHT hardcoden — immer den in dieser Session ermittelten Branch verwenden
- Owner/Repo aus INDEX.md Projekt-Metadaten lesen
- Wenn der Branch noch nicht gepusht ist: User darauf hinweisen dass
  ChatGPT die neuen Dateien nicht sehen kann

## Doc-Laderegel

Beim Erstellen des Initialprompts die verbindliche Ladereihenfolge
(DOC-STANDARD.md Kapitel 8) nutzen:

1. INDEX.md → Welche Docs sind für das Review-Thema relevant?
2. Quickloads der relevanten Docs lesen
3. Fachliche Invarianten sammeln
4. Relevante Quickloads + Invarianten als Kontext in den Prompt packen

So weiß ChatGPT z.B. "SQLite ist SoR" oder "alles über
IExternalCommunicationService" ohne dass der User es manuell einfügt.

**Format im Prompt:**

```
## Projektkontext (aus Quickloads)

### [Doc-Name] (source_of_truth)
- Zweck: [aus Quickload]
- Fachliche Invarianten:
  - [aus Quickload]

### [Doc-Name] (secondary)
- Zweck: [aus Quickload]
```

Nur Quickloads einfügen die relevant sind — nicht alle Docs.
Max 3-5 Quickloads im Prompt, sonst wird er zu lang.

## Frühphasen-Hinweis (PFLICHT in jedem Initialprompt)

INDEX.md hat das Kapitel "Projekt-Phase (VERBINDLICH)". Solange dieses Kapitel
besteht, MUSS jeder Initialprompt einen Frühphasen-Block enthalten, damit
ChatGPT keine Migrations-/Backward-Compatibility-Vorschläge macht die wir
ausdrücklich nicht wollen.

**Block der eingefügt werden muss:**

```
## Frühphase (PFLICHT-Hinweis)

BPM ist in früher Entwicklung ohne Produktivdaten.

Konsequenzen für deine Architektur-Vorschläge:
- KEINE Migrations-Logik vorschlagen
- KEINE Backward-Compatibility-Patterns
- KEINE Legacy-Tolerance in Parsern/Loadern/Deserializern
- Bei Schema-/Config-/DB-Änderungen: stattdessen "Datei löschen, neu anlegen lassen"
  als gewollter Standardweg

Ausnahme: Nur wenn explizit "Migration bauen" im Prompt steht.

Quelle: INDEX.md Kapitel "Projekt-Phase".
```

**Regel:**
- Der Block kommt als eigener Abschnitt in den Initialprompt, **vor** "Projektkontext"
- Bei Folgeprompts (Runde 2, 3, ...) nicht nochmal einfügen — einmal pro Review reicht
- Wenn der User explizit Migration will, Block weglassen und im Prompt erwähnen warum

---

## Gesprächsphasen

### Phase 1: Initialprompt

```
## Rolle
Du bist ein erfahrener [Rolle] und führst ein technisches
Review-Gespräch mit einem Kollegen (Claude/Anthropic).

## Gesprächsformat
Dieses Gespräch läuft über einen Vermittler (den User).
- Sprich direkt zu deinem Kollegen, NICHT zum User
- Kein Meta-Kommentar über das Format
- Schreibe deine GESAMTE Antwort in Canvas
- CANVAS-TITEL: "Review Runde X"
- Fasse am Ende JEDER Antwort zusammen:
  ✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen

## Repo-Zugriff
[Block von oben einfügen mit aktuellem Branch]

## Gesprächsregeln
- Ehrlich und kritisch
- Probleme konkret benennen
- Verbesserungen mit Code/Pseudocode zeigen
- Rückfragen bei fehlendem Kontext
- Fokus halten, keine allgemeinen Exkurse
- Kompakt, Code nur wenn nötig
[FALLS FOKUS:] - Fokus: [Thema]

## Frühphase (PFLICHT-Hinweis)
[Block aus "Frühphasen-Hinweis" oben einfügen]

## Projektkontext (aus Quickloads)
[Relevante Quickloads + Invarianten hier einfügen]

## Das Konzept
[Vollständiges Konzept/Code/Architektur]

## Aufgabe
[Spezifische Prüfpunkte]
```

**Wichtig:**
- ALLEN Kontext aus dem Chat sammeln
- Code vollständig, nicht gekürzt
- Quickloads verwandter Docs als Projektkontext einbauen
- Fachliche Invarianten explizit aufführen
- Repo-Zugriff Block mit aktuellem Branch IMMER einfügen

### Phase 2: Antwort/Reaktion

#### Stufe A — Einschätzung + ask_user_input_v0

1. Eigene Einschätzung zusammenfassen
2. `ask_user_input_v0` mit Entscheidungspunkten (max 3 Fragen)
3. Immer Option "ChatGPT fragen" anbieten

#### Stufe B — Folgeprompt (nach User-Antwort)

- Basierend auf User-Entscheidungen
- Canvas-Rundennummer korrekt mitzählen
- Repo-Zugriff Block mit aktuellem Branch IMMER einfügen
- ✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen

### Phase 3: Abschluss

- Konsens
- Meinungsverschiedenheiten
- Offene Punkte
- Nächste Schritte
- Optional: überarbeitetes Konzept

---

## Grundhaltung

Gleichwertiger Gesprächspartner:
- Nur zustimmen wenn überzeugt
- Aktiv widersprechen wenn nötig
- Eigene Vorschläge einbringen
- Bei Uneinigkeit: User per ask_user_input_v0 entscheiden lassen

---

## Formatierung

Prompts als Download (.md) unter `/mnt/user-data/outputs/`:
- `chatgpt-review-prompt.md`
- `chatgpt-review-runde-N.md`

Phase 2 Stufe A: direkt im Chat + ask_user_input_v0.
Download erst in Stufe B.

## Sprache

Prompts in der Sprache des Users.

---

## VERBOTEN

- Branch automatisch annehmen ohne ask_user_input_v0
- Multiple-Choice als Prosa statt ask_user_input_v0
- Stufe A Entscheidungspunkte als Prosa statt ask_user_input_v0
- Uneinigkeit ohne ask_user_input_v0 auflösen
- Initialprompt ohne Frühphasen-Hinweis-Block erstellen (siehe Frühphasen-Prinzip in INDEX.md)
