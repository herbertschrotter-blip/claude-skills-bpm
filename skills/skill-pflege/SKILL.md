---
name: skill-pflege
description: >
  Ändert und erweitert bestehende BPM-Skills, ohne deren Originalinhalt
  ungewollt zu kürzen oder umzuschreiben. Use when users want to update an
  existing skill, add rules to a current SKILL.md, adjust trigger wording, or
  refine an already existing skill safely. Do not trigger for creating a brand
  new skill from scratch (use skill-neu instead), running skill evals, or
  designing a new skill system.
---

# Skill-Pflege — Sichere Änderung bestehender Skills

## Zweck

Ändert bestehende Skills ohne den Originaltext zu beschädigen. Löst das Problem dass beim Neu-Generieren eines Skills Inhalte aus dem Gedächtnis heraus weggelassen, gekürzt oder umformuliert werden können.

**Default-Philosophie:** Additiv. Der Skill wird größer, nie kleiner. Änderungen sind Präzisierungen, keine Umschreibungen.

---

## 🚨 VERBINDLICHE REGEL: ask_user_input_v0 bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS `ask_user_input_v0`
verwendet werden — KEINE Prosa-Fragen.**

### Diese Fragen IMMER mit ask_user_input_v0:

| Situation | Optionen |
|-----------|----------|
| Nächsten Skill updaten? | Ja, nächsten | Pause | Fertig | Anderer Skill |
| Löschen eines Abschnitts | Löschen, Behalten, Umformulieren, Abbrechen |
| Tippfehler im Original | Korrigieren, Als Tippfehler lassen, User entscheiden |
| Redundanz erkannt | Beide behalten, Erstes entfernen, Zweites entfernen, Abbrechen |
| Struktur-Konflikt | Alt-Struktur behalten, Neu-Struktur, Mischform |
| Skill-Version angeben? | Keine Version, v2, v3, Anders benennen |
| Welcher Skill soll geändert werden | Liste aus /mnt/skills/user/ als Optionen |

### Prosa-Fragen NUR wenn:

- Offene Frage ohne feste Optionen (z.B. "Welcher Text soll eingefügt werden?")
- User hat gerade Präferenz signalisiert
- Es ist Erklärung/Kontext

---

## 🔴 HARTE REGELN (nie brechen)

### 1. Original zeilengenau übernehmen

Nicht "sinngemäß neu schreiben". Der komplette bestehende Text bleibt erhalten wie er ist — inklusive:
- Zeichensetzung
- Absatzformatierung
- Überschriften-Hierarchie
- Listen-Einrückung
- Code-Blöcke

### 2. Nichts löschen ohne explizite Freigabe

Auch scheinbar redundante Stellen nicht entfernen. Redundanz kann Absicht sein — z.B. eine Regel die oben und unten erwähnt wird um sie in beiden Kontexten präsent zu haben.

Wenn Löschung nötig scheint: `ask_user_input_v0`:
```
Frage: "Abschnitt X wirkt redundant zu Y. Was tun?"
Optionen: "Beide behalten", "X löschen", "Y löschen", "Abbrechen"
```

### 3. Nichts kürzen ohne Freigabe

Keine Zusammenfassung von längeren Erklärungen zu Einzeilern. Wenn der Skill 3 Sätze zu einem Thema hatte, bleiben es 3 Sätze.

### 4. Nichts umformulieren ohne Freigabe

Auch wenn eine Formulierung "besser" erscheint — nicht ändern. Der User hat bewusst seine Wortwahl gewählt.

**Ausnahme:** Echter Tippfehler (z.B. `ask_user_input` ohne `v0`-Suffix). Dann per `ask_user_input_v0` nachfragen ob korrigiert werden soll.

### 5. Struktur/Reihenfolge nicht ändern

Wenn Kapitel 3 vor Kapitel 4 stand, bleibt das so. Auch wenn "Kapitel 4 wäre logischer zuerst" gedacht wird.

---

## 🟡 WICHTIG (beachten)

### 6. Frontmatter nicht anfassen

Der YAML-Block oben (`name`, `description`) bleibt 1:1 erhalten. Nur auf explizite Anweisung ändern.

### 7. Versions-Info im Frontmatter ist optional

Wenn der User nicht ausdrücklich sagt "nenn es v2", dann keine Versions-Suffixe irgendwohin pflanzen. Der Skill heißt `tracker`, nicht `tracker v4.1` — das v4.1 ist nur Chat-Kommunikation.

### 8. Neue Abschnitte am Anfang oder Ende einfügen

Nicht mittendrin neue Sections reinquetschen:
- Neue globale Regeln (wie 🚨-Box) direkt nach dem Zweck-Abschnitt
- Neue VERBOTEN-Punkte ans Ende der bestehenden VERBOTEN-Liste
- Neue Beispiele im jeweiligen Kontext-Abschnitt

### 9. Inline-Änderungen nur punktuell

Wenn im Original "User fragen" steht und es zu "per ask_user_input_v0 fragen" geändert wird, dann nur diese eine Zeile. Nicht den ganzen umgebenden Absatz umschreiben.

### 10. Diff-Report nach jedem Update

Bevor User "Skill speichern" klickt, zeigen:
- Was unverändert blieb (Kurzform: "20 Abschnitte unverändert")
- Was neu hinzugekommen ist (exakter Text)
- Was inline geändert wurde (vorher/nachher)
- Was gelöscht wurde (hoffentlich nichts — wenn doch, mit Begründung)

---

## 🟢 PROZESS-REGELN

### 11. Immer Original lesen VOR Änderung

Nie aus dem Gedächtnis oder aus einer Zusammenfassung arbeiten. `view` auf den aktuellen Skill-Inhalt als ersten Schritt.

```
view /mnt/skills/user/<skill-name>/SKILL.md
```

### 12. Two-Place-Pflege (Repo + Artifact)

Jede Skill-Änderung lebt an zwei Orten:

1. **Repo** (versioniert): `claude-skills-bpm/skills/<name>/SKILL.md` — via DC `edit_block` oder `write_file` direkt editieren
2. **Artifact im Chat**: Claude liefert ein Artifact mit dem vollständigen neuen Inhalt. Der User klickt darauf den "Skill speichern"-Button in Claude.ai.

**Reihenfolge:** Erst Repo, dann Artifact.

**KEINE Download-Datei mehr** in `/mnt/user-data/outputs/SKILL.md`. Kein `present_files` für Skill-Updates. Der Artifact ersetzt beide Schritte.

### 13. Dateiname immer exakt `SKILL.md`

Damit der "Skill speichern"-Button im UI erscheint. Kein `SKILL-<name>.md` oder `skill.md` oder sonst was.

### 14. Artifact mit vollständigem Skill-Inhalt

Das Artifact enthält die komplette neue SKILL.md (nicht nur den Diff). Der User klickt "Skill speichern" → Claude.ai ersetzt den aktiven Skill.

### 15. Nach Speicher-Bestätigung erst weiter

Nicht gleich mehrere Skills hintereinander aktualisieren. Jeder einzelne wird gespeichert, dann weiter.

### 16. Immer Skill für Skill

Bei Batch-Updates mehrerer Skills NIEMALS mehrere auf einmal erstellen. Strikt:
1. Einen Skill ändern (Repo via DC + Artifact im Chat)
2. User speichert via "Skill speichern"-Button
3. **`ask_user_input_v0`** fragen ob der nächste drankommt:
   ```
   Frage: "Nächsten Skill updaten?"
   Optionen: "Ja, nächster: <Name>", "Pause", "Anderer Skill", "Fertig für heute"
   ```
4. Erst nach Bestätigung → nächster Skill

---

## ⚪ WENN DOCH MAL GELÖSCHT WERDEN MUSS

### 17. Explizite Freigabe per `ask_user_input_v0`

```
Frage: "Abschnitt X ist klar veraltet wegen Y. Was tun?"
Optionen: 
  "Abschnitt löschen"
  "Als 'deprecated' markieren"
  "Umformulieren angleichen"
  "Abbrechen"
```

### 18. Nie stillschweigend löschen

Auch Duplikate nicht. Wenn zwei Stellen dasselbe sagen → nachfragen.

---

## 🔵 WEITERE ÜBERLEGUNGEN

### 19. Eigenständig bleiben

Nicht zwischen Skills querverweisen ("siehe tracker v4.1") als Ersatz für Inhalte. Jeder Skill bleibt vollständig lesbar. Querverweise nur als Zusatzinfo.

### 20. Ausnahme für Tippfehler

Wenn im Original ein echter Tippfehler steht (z.B. `ask_user_input` ohne `v0`-Suffix, veraltete Syntax), per `ask_user_input_v0`:

```
Frage: "Im Original steht X, ist das ein Tippfehler?"
Optionen: "Ja, korrigieren zu Y", "Nein, so lassen", "User entscheidet später"
```

---

## ABLAUF (Standard)

### Schritt 1 — Skill identifizieren

Wenn nicht klar welcher Skill: `ask_user_input_v0` mit Liste aus `/mnt/skills/user/`.

### Schritt 2 — Original laden

```
view /mnt/skills/user/<name>/SKILL.md
```

Komplett lesen. Nicht scrollen, nicht abkürzen.

### Schritt 3 — Änderungs-Plan ausarbeiten

Konkret schreiben:
- Welche Abschnitte bleiben unverändert? (Liste der H2-Überschriften)
- Was wird neu hinzugefügt? (exakter Text)
- Was wird inline geändert? (vorher/nachher Paare)
- Was wird gelöscht? (hoffentlich leer)

### Schritt 4 — User-Freigabe für den Plan

Nur wenn Änderungen größer sind als 1-2 Zeilen:

```
ask_user_input_v0:
Frage: "Plan für <skill-name> Update. OK so?"
Optionen: "Ja, umsetzen", "Anders machen", "Abbrechen"
```

### Schritt 5 — Repo-Datei via DC editieren

Änderungen direkt ins Repo schreiben:

```
DC edit_block <repo-pfad>/skills/<name>/SKILL.md
  old_string: <zu ersetzender Block>
  new_string: <neuer Block>
```

Für komplette Neu-Schreibe: `DC write_file` mit `mode: "rewrite"`.
Immer absolute Pfade.

### Schritt 6 — Artifact mit vollständigem neuen Inhalt

Claude erstellt ein Artifact mit der kompletten neuen SKILL.md:

```
create_file
  path: /home/claude/SKILL.md
  content: <komplette neue Skill-Datei>
```

**Dateiname exakt `SKILL.md`** (keine Prefixes/Suffixes — siehe Regel 13).

Der User sieht den Artifact-Block in Claude.ai und klickt "Skill speichern".

### Schritt 7 — Diff-Report im Chat

Kompakt zeigen was sich geändert hat (siehe Regel 10).

### Schritt 8 — Auf User-Speicher-Bestätigung warten

Nicht weiter bis User "gespeichert" oder "ok" oder ähnliches bestätigt.

### Schritt 9 — Wenn Batch: ask_user_input_v0 für nächsten Skill

```
Frage: "Nächsten Skill updaten?"
Optionen: "Ja, nächster: <Name>", "Pause", "Anderer Skill", "Fertig für heute"
```

---

## BEISPIEL-WORKFLOW

```
User: "Update alle 6 Skills auf ask_user_input_v0 Regel"

Claude:
  1. ask_user_input_v0: "Welcher Skill zuerst?"
     Optionen: "audit", "cc-steuerung", "chatgpt-review", "Alle in Reihenfolge"
  2. User: "Alle in Reihenfolge"
  3. Claude: 
     - view /mnt/skills/user/audit/SKILL.md
     - Plan schreiben
     - ask_user_input_v0 mit Plan
     - DC edit_block auf <repo>/skills/audit/SKILL.md
     - create_file Artifact /home/claude/SKILL.md
     - Diff-Report
  4. WARTEN auf "gespeichert"
  5. ask_user_input_v0: "Nächster Skill cc-steuerung?"
     Optionen: "Ja", "Pause", "Andere Reihenfolge", "Fertig"
  6. ... Zyklus wiederholt sich
```

---

## VERBOTEN

- Skills aus dem Gedächtnis neu schreiben (immer Original laden)
- Mehrere Skills parallel in einer Antwort erstellen
- Originalinhalte still entfernen, kürzen, zusammenfassen
- Stilistische "Verbesserungen" am Original ohne Freigabe
- Umformulieren bestehender Formulierungen ohne Freigabe
- Frontmatter ändern ohne explizite Anweisung
- Versions-Suffixe in den Skill-Dateinamen einfügen (immer `SKILL.md`)
- Zwischen mehreren Skills ohne ask_user_input_v0 Bestätigung wechseln
- Diff-Report weglassen bei nicht-trivialen Änderungen
- **Prosa-Fragen bei festen Entscheidungsoptionen** — IMMER ask_user_input_v0


---

## VERWEIS

**Komplett neuen Skill anlegen? → `skill-neu`**

`skill-neu` ist der Schwester-Skill für Neu-Erstellung. Er hat eigene Struktur (Capture-Intent-Interview, BPM-Description-Schema, Test-Prompt-Setup). `skill-pflege` macht ausschließlich Änderungen an bestehenden Skills.

Faustregel:
- Existiert die SKILL.md schon? → `skill-pflege` (hier)
- Datei wird ganz neu angelegt? → `skill-neu`
