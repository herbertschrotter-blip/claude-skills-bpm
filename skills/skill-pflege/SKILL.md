---
name: skill-pflege
description: >
  Ändert und erweitert bestehende Skills im Skills-Repo (claude-skills-bpm),
  ohne deren Originalinhalt ungewollt zu kürzen oder umzuschreiben – aus dem
  Cowork-Chat wie aus Claude Code. Use when users want to ändern,
  erweitern, ergänzen, einbauen, einfügen, schärfen, refactoren,
  aktualisieren, anpassen, präzisieren, korrigieren, or update an existing
  skill — including adding new rules, adjusting trigger wording, refining
  descriptions, fixing typos, updating references, or restructuring
  existing SKILL.md content. Do not trigger for creating a brand new skill
  from scratch (use skill-neu instead), running skill evals, designing a
  new skill system, or changing skills in unrelated repos.
---

# Skill-Pflege — Sichere Änderung bestehender Skills

## Zweck

Ändert bestehende Skills ohne den Originaltext zu beschädigen. Löst das Problem dass beim Neu-Generieren eines Skills Inhalte aus dem Gedächtnis heraus weggelassen, gekürzt oder umformuliert werden können.

**Default-Philosophie:** Additiv. Der Skill wird größer, nie kleiner. Änderungen sind Präzisierungen, keine Umschreibungen.

**Zwei Umgebungen, ein Ablauf.** Im **Cowork-Chat** liest Claude mit `view`, schreibt per DC und liefert
ein Artifact (Regeln 13–14b). In **Claude Code** liest Claude die Datei mit dem Read-Werkzeug, ändert
sie mit Edit/Write direkt im Skills-Repo (Pfad aus dem Tracker-Profil der CLAUDE.md, OneDrive-relativ)
und liefert die fertige Datei per `SendUserFile` – Herbert lädt sie bei claude.ai hoch. Wo unten
„Artifact“ steht, gilt in Claude Code „Datei per SendUserFile“. Wo „DC“ steht, gilt „Werkzeug der
Umgebung“.

---

## 🚨 VERBINDLICHE REGEL: Auswahlfrage bei Entscheidungen

**Bei JEDER Entscheidungsfrage mit festen Optionen MUSS eine Auswahlfrage
gestellt werden — KEINE Prosa-Fragen.** Auswahlfrage = Frage-Werkzeug der Umgebung
mit anklickbaren Optionen (Cowork `ask_user_input_v0`, Claude Code `AskUserQuestion`).

### Diese Fragen IMMER als Auswahlfrage:

| Situation | Optionen |
|-----------|----------|
| Nächsten Skill updaten? | Ja, nächsten | Pause | Fertig | Anderer Skill |
| Löschen eines Abschnitts | Löschen, Behalten, Umformulieren, Abbrechen |
| Tippfehler im Original | Korrigieren, Als Tippfehler lassen, User entscheiden |
| Redundanz erkannt | Beide behalten, Erstes entfernen, Zweites entfernen, Abbrechen |
| Struktur-Konflikt | Alt-Struktur behalten, Neu-Struktur, Mischform |
| Skill-Version angeben? | Keine Version, v2, v3, Anders benennen |
| Welcher Skill soll geändert werden | Liste der Ordner in `skills/` des Repos (Cowork alternativ /mnt/skills/user/) |
| Split-Prüfung schlägt an (Regel 21) | Aufteilen in references, So lassen, Später |
| description über 1024 Zeichen | Kürzen (Vorschlag zeigen), Anders kürzen, Abbrechen |

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

Wenn Löschung nötig scheint: Auswahlfrage:
```
Frage: "Abschnitt X wirkt redundant zu Y. Was tun?"
Optionen: "Beide behalten", "X löschen", "Y löschen", "Abbrechen"
```

### 3. Nichts kürzen ohne Freigabe

Keine Zusammenfassung von längeren Erklärungen zu Einzeilern. Wenn der Skill 3 Sätze zu einem Thema hatte, bleiben es 3 Sätze.

### 4. Nichts umformulieren ohne Freigabe

Auch wenn eine Formulierung "besser" erscheint — nicht ändern. Der User hat bewusst seine Wortwahl gewählt.

**Ausnahme:** Echter Tippfehler (z.B. `ask_user_input` ohne `v0`-Suffix). Dann per Auswahlfrage nachfragen ob korrigiert werden soll.

**Zweite Ausnahme (seit v0.24, Herbert 16.09.2026):** Beim **Neutralisieren** eines Skills
(Werkzeugnamen → Handlung, Projektwerte → Profil/Config) dürfen die betroffenen Sätze umgebaut
werden – „nur die wesentlichen Teile umbauen, Rest bleibt Original“. Der Diff-Report zeigt jede
Stelle.

### 5. Struktur/Reihenfolge nicht ändern

Wenn Kapitel 3 vor Kapitel 4 stand, bleibt das so. Auch wenn "Kapitel 4 wäre logischer zuerst" gedacht wird.

---

## 🟡 WICHTIG (beachten)

### 6. Frontmatter nicht anfassen

Der YAML-Block oben (`name`, `description`) bleibt 1:1 erhalten. Nur auf explizite Anweisung ändern.

**Wenn die description geändert wird: maximal 1024 Zeichen** (Zeilen des `description: >`-Blocks
getrimmt und mit Leerzeichen verbunden). claude.ai lehnt den Upload sonst ab („field 'description'
in SKILL.md must be at most 1024 characters“, passiert am 16.09.2026 bei code-erstellen). Vor jeder
Lieferung messen; über dem Limit → Auswahlfrage mit Kürzungsvorschlag.

### 7. Versions-Info im Frontmatter ist optional

Wenn der User nicht ausdrücklich sagt "nenn es v2", dann keine Versions-Suffixe irgendwohin pflanzen. Der Skill heißt `tracker`, nicht `tracker v4.1` — das v4.1 ist nur Chat-Kommunikation.

### 8. Neue Abschnitte am Anfang oder Ende einfügen

Nicht mittendrin neue Sections reinquetschen:
- Neue globale Regeln (wie 🚨-Box) direkt nach dem Zweck-Abschnitt
- Neue VERBOTEN-Punkte ans Ende der bestehenden VERBOTEN-Liste
- Neue Beispiele im jeweiligen Kontext-Abschnitt

### 9. Inline-Änderungen nur punktuell

Wenn im Original "User fragen" steht und es zu "per Auswahlfrage fragen" geändert wird, dann nur diese eine Zeile. Nicht den ganzen umgebenden Absatz umschreiben.

### 10. Diff-Report nach jedem Update

Bevor User "Skill speichern" klickt, zeigen:
- Was unverändert blieb (Kurzform: "20 Abschnitte unverändert")
- Was neu hinzugekommen ist (exakter Text)
- Was inline geändert wurde (vorher/nachher)
- Was gelöscht wurde (hoffentlich nichts — wenn doch, mit Begründung)
- Länge der description (Zeichen, muss < 1024 sein)
- Dateiliste der Lieferung (nur SKILL.md, oder Zip mit SKILL.md + references/…)
- CHANGELOG-Version und Commit-Hash

---

## 🟢 PROZESS-REGELN

### 11. Immer Original lesen VOR Änderung

Nie aus dem Gedächtnis oder aus einer Zusammenfassung arbeiten. Den aktuellen Skill-Inhalt
als ersten Schritt komplett lesen – **aus dem Repo**, nicht aus der geladenen Skill-Kopie
(die kann älter sein).

```
Cowork:      view /mnt/skills/user/<skill-name>/SKILL.md   (oder DC read_file auf das Repo)
Claude Code: Read <skills-repo>/skills/<skill-name>/SKILL.md  (+ references/*.md, wenn vorhanden)
```

### 12. Two-Place-Pflege (Repo + Artifact)

Jede Skill-Änderung lebt an zwei Orten:

1. **Repo** (versioniert): `claude-skills-bpm/skills/<name>/SKILL.md` — Cowork via DC `edit_block` oder `write_file`, Claude Code via Edit/Write (oder ein Patch-Skript bei vielen Stellen)
2. **Lieferung an den User**: Cowork ein Artifact mit dem vollständigen neuen Inhalt („Skill speichern“-Button); Claude Code die Datei per `SendUserFile` (Herbert lädt sie bei claude.ai unter Skills hoch)

**Reihenfolge:** Erst Repo (inkl. CHANGELOG/INDEX/Commit, Regel 12a), dann Lieferung.

### 12a. CHANGELOG, INDEX und Commit gehören zu jeder Skill-Änderung

Vor der Lieferung, nach dem Repo-Edit:
1. `CHANGELOG.md` im Repo-Root: neuer Eintrag `## [vX.Y.Z] — <Datum>` mit Skill, Typ und
   Kurzbeschreibung (Version nach git-commit-helper: MINOR bei neuer Fähigkeit, PATCH bei Fix/Chore)
2. `INDEX.md`: Zeile des Skills anpassen, wenn sich Zuständigkeit oder Trigger geändert haben
3. Commit `[vX.Y.Z] <skill>, <Typ>: <Kurztitel>` und Push (Branch `main` des Skills-Repos)
Ohne diese drei Schritte ist die Änderung nicht fertig – auch nicht nach dem Upload.

**KEINE Download-Datei mehr** in `/mnt/user-data/outputs/SKILL.md`. Kein `present_files` für Skill-Updates. Der Artifact ersetzt beide Schritte.

### 13. Dateiname immer exakt `SKILL.md`

Damit der "Skill speichern"-Button im UI erscheint. Kein `SKILL-<name>.md` oder `skill.md` oder sonst was.

**Skills mit `references/`:** Lieferung als **Zip** mit `SKILL.md` und dem Ordner `references/`
(Struktur wie im Repo). Herbert legt den Skill bei claude.ai aus der Zip neu an bzw. ersetzt alle
Dateien; bei claude.ai muss danach unter „Inhalte“ die Dateizahl stimmen (SKILL.md + alle references).
Nur SKILL.md geändert und keine references vorhanden → einzelne Datei reicht.

### 13a. 🔴 Artifact-Dateiname (KRITISCH, skill-pflege-004)

Der Artifact-Dateiname MUSS **exakt** `SKILL.md` sein. Sonst erscheint der "Skill speichern"-Button in Claude.ai nicht und Herbert muss den Inhalt manuell copy-pasten.

**RICHTIG:**
```
create_file(path="/home/claude/SKILL.md", ...)
```

**FALSCH (kein "Skill speichern"-Button):**
```
create_file(path="/home/claude/chat-wechsel-SKILL.md", ...)
create_file(path="/home/claude/SKILL-chat-wechsel.md", ...)
create_file(path="/home/claude/chat-wechsel.md", ...)
create_file(path="/home/claude/skill.md", ...)   ← klein, auch falsch
```

**Grund:** Die Claude.ai-UI erkennt nur exakt `SKILL.md` (Groß-Klein-Schreibung!) als ersetzbare Skill-Datei.

**Hinweis (skill-pflege-006):** Der korrekte Dateiname ist notwendig, aber allein nicht ausreichend. `create_file` schreibt nur in die Container-Sandbox. Damit die Dateikarte mit "Skill speichern"-Button erscheint, muss **direkt anschliessend** `present_files` auf denselben Pfad aufgerufen werden. Siehe Regel 14 und 14b.

### 13b. 🚨 Ein Skill-Artifact pro Antwort (KRITISCH, skill-pflege-007)

**Pro Antwort darf maximal EIN Skill-Artifact erstellt werden.**

**Grund:** Der Pfad `/home/claude/SKILL.md` ist ein einzelner Container-Slot. Jede neue `create_file`-Operation mit diesem Pfad **überschreibt** den vorigen Inhalt. Wenn Claude in einer Antwort zwei Artifacts erstellt, zeigen beide Dateikarten im Chat denselben (zweiten) Inhalt — der User klickt zweimal "Skill speichern" und speichert **denselben Skill zweimal**, während der erste Skill nicht aktualisiert wird.

**Ablauf bei Mehrfach-Updates:**

1. DC-Edits für ALLE betroffenen Skills in einer Antwort sind OK (Repo-Seite, weil Skills dort eigene Pfade haben)
2. Artifacts werden SEQUENTIELL über mehrere Antworten hinweg erzeugt
3. Nach jedem Artifact: User-Bestätigung ("gespeichert" / "ok") abwarten
4. Erst dann nächstes Artifact erstellen

**Ausnahme:** Keine. Auch bei "trivialen" Mehrfach-Updates (z.B. Description-Schärfung in 2 Skills, Refactor mit 3 Skills) gilt die Regel strikt.

**Konkretes Beispiel (Teil 31 / v0.17.11):**

Description-Schärfung von `git-commit-helper` + `chatgpt-review` in einer Antwort → zweite `create_file` überschrieb erste → beide Dateikarten zeigten chatgpt-review-Inhalt. Der git-commit-helper-Skill wurde erst in einer Folge-Antwort korrekt als Artifact bereitgestellt.

### Mehrere Skills in einer Session

- Pro Skill einen **eigenen Antwort-Block**
- Pro Antwort-Block nur **EIN** Artifact namens `SKILL.md`
- Kontext-Trennung durch Antwort-Text ("Jetzt Skill X updaten..."), **nicht** durch Dateinamen-Variation

### 14. Artifact mit vollständigem Skill-Inhalt

Das Artifact enthält die komplette neue SKILL.md (nicht nur den Diff). Der User klickt "Skill speichern" → Claude.ai ersetzt den aktiven Skill.

**Tool-Call-Paar (KRITISCH, skill-pflege-006):**

`create_file` allein erzeugt KEIN UI-Widget — weder in Claude Desktop noch in Claude.ai Web. Die Datei landet nur in der Container-Sandbox. Damit die Dateikarte mit "Skill speichern"-Button rendert, müssen ZWEI Tool-Calls direkt hintereinander kommen:

1. `create_file path="/home/claude/SKILL.md" file_text=<komplette Datei>`
2. `present_files filepaths=["/home/claude/SKILL.md"]`

`present_files` kopiert die Datei automatisch nach `/mnt/user-data/outputs/SKILL.md` und rendert die UI-Komponente. Weil der Dateiname exakt `SKILL.md` ist, erscheint der "Skill speichern"-Button.

### 14a. 🔴 Artifact-Separation (skill-pflege-003)

**Nach Artifact-Erstellung KEIN `ask_user_input_v0` im selben Antwort-Block.**

Claude.ai-UI verdrängt das Artifact, wenn direkt danach ein `ask_user_input_v0`-Dialog erscheint. Der User sieht das Artifact nur kurz, dann deckt der Input-Dialog es ab — Herbert kann nicht in Ruhe auf "Skill speichern" klicken.

**Richtiger Ablauf:**

Antwort N (Artifact-Block):
1. DC schreibt Datei aufs Laufwerk
2. DC-Verifikation (Zeilenzahl, Diff-Stat)
3. Artifact mit vollständiger SKILL.md (`create_file /home/claude/SKILL.md`)
4. Kurzer Status-Text ("Zum Copy-Paste ins Claude.ai-Projekt via Skill speichern-Button")
5. **Antwort abschließen** — KEIN `ask_user_input_v0` hier

Antwort N+1 (nach User-Bestätigung "gespeichert"):
- Erst jetzt `ask_user_input_v0` für nächste Schritte (z.B. "Nächsten Skill updaten?")

**Gilt für:** jede Kombination aus Artifact + Folgefrage. Nicht nur bei SKILL.md-Artifacts, sondern bei allen Artifacts, bei denen der User noch eine Aktion (Kopieren, Speichern, Ansehen) ausführen muss.

### 14b. 🔴 Artifact-Pflicht nach Skill-Commit (KRITISCH, skill-pflege-005)

Nach JEDEM Skill-Commit (PATCH/MINOR auf einen beliebigen Skill) MUSS Claude
in derselben oder direkt folgenden Antwort ein Artifact mit der kompletten
neuen SKILL.md erzeugen.

**Ohne Artifact bleibt der aktive Skill in Claude.ai unverändert.** Herbert
arbeitet weiter mit der alten Version, obwohl das Repo längst aktualisiert ist.

**Pflicht-Trigger (Artifact MUSS erzeugt werden):**

- `tracker done` auf einen Skill-Task (Skill-Issues-Listen-Scope)
- Direkter `edit_block` oder `write_file` auf `skills/*/SKILL.md`
- Git-Commit mit Format `[vX.Y.Z] <skill>, <Typ>: ...`

**Ausnahmen (keine Lieferung nötig):**

- Zero-Change-Commits auf Skills (reine Pfad-Anpassungen ohne Inhaltsänderung)

**Keine Ausnahme mehr (seit 16.09.2026):** Commits, die nur `references/`-Dateien ändern.
Der Skill wird bei claude.ai als Ganzes (SKILL.md + references) gehalten, also braucht jede
references-Änderung eine neue Zip-Lieferung.

**Workflow-Reihenfolge (verbindlich):**

1. Repo-Edit (Cowork DC `edit_block` / `write_file`; Claude Code Edit/Write)
2. CHANGELOG/INDEX, Git-Commit, Push (Regel 12a); description-Länge messen (Regel 6)
3. Lieferung: Cowork Artifact als Tool-Call-Paar (create_file + present_files, siehe Regel 14);
   Claude Code `SendUserFile` mit SKILL.md bzw. Zip (Regel 13)
   im selben oder direkt folgenden Antwort-Block
4. Antwort abschliessen (keine Auswahlfrage, siehe 14a)

**Bei mehreren Skill-Commits in einer Session:**

- Pro geändertem Skill EIN Artifact
- In SEPARATEN Antwort-Blöcken (nicht zwei Artifacts in einer Antwort)
- User bestätigt "gespeichert" zwischen den Skills (siehe Regel 15 + 16)

### 15. Nach Speicher-Bestätigung erst weiter

Nicht gleich mehrere Skills hintereinander aktualisieren. Jeder einzelne wird gespeichert, dann weiter.

### 16. Immer Skill für Skill

Bei Batch-Updates mehrerer Skills NIEMALS mehrere auf einmal erstellen. Strikt:
1. Einen Skill ändern (Repo + Lieferung, siehe Regel 12)
2. User speichert („Skill speichern“-Button bzw. Upload bei claude.ai) und sagt „gespeichert“
3. **Auswahlfrage** ob der nächste drankommt:
   ```
   Frage: "Nächsten Skill updaten?"
   Optionen: "Ja, nächster: <Name>", "Pause", "Anderer Skill", "Fertig für heute"
   ```
4. Erst nach Bestätigung → nächster Skill

---

## ⚪ WENN DOCH MAL GELÖSCHT WERDEN MUSS

### 17. Explizite Freigabe per Auswahlfrage

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

Wenn im Original ein echter Tippfehler steht (z.B. `ask_user_input` ohne `v0`-Suffix, veraltete Syntax), per Auswahlfrage:

```
Frage: "Im Original steht X, ist das ein Tippfehler?"
Optionen: "Ja, korrigieren zu Y", "Nein, so lassen", "User entscheidet später"
```

---

### 21. Split-Prüfung: wann gehören Teile in `references/`?

Bei jeder Änderung an einem Skill kurz prüfen, ob er zu groß oder zu gemischt geworden ist
(Herbert, 16.09.2026 – Vorbild: tracker mit 14 references, code-erstellen mit `references/stacks/`).
Ein Split ist sinnvoll, wenn **mindestens zwei** Punkte zutreffen:

- SKILL.md über ~300 Zeilen oder mehr als ~8 Hauptabschnitte
- Ein Abschnitt gilt nur für **ein Kommando**, **eine Umgebung** (Cowork/Claude Code) oder
  **einen Stack/eine Sprache** – der Rest des Skills braucht ihn nicht
- Projekt- oder Werkzeugwerte im Skill (IDs, Pfade, Listen) → gehören in `projects/<name>/` oder
  eine Referenz, nicht in die SKILL.md
- Dieselbe Struktur wiederholt sich mehrfach (je Stack, je Kommando) → eine Datei je Ausprägung
- Der Skill wird bei jeder Erweiterung an derselben Stelle länger (Beispielsammlungen, Fehlerlisten)

**Muster:** SKILL.md = Zweck, Kernregeln, Routing-Tabelle „Kommando/Fall → Referenz“, Kurz-VERBOTEN.
`references/<thema>.md` = der operative Ablauf; `references/<gruppe>/<key>.md` bei Ausprägungen
(z.B. `stacks/typescript-lit.md`). Jede Referenz wird in der Routing-Tabelle genannt, sonst wird
sie nicht geladen.

**Ablauf:** Befund kurz nennen (was, warum, wohin) → Auswahlfrage „Aufteilen in references“ /
„So lassen“ / „Später (Skill-Issue)“ → beim Aufteilen: Text **verschieben, nicht neu schreiben**
(Regel 1 gilt weiter), Routing-Tabelle ergänzen, Lieferung als Zip (Regel 13). Nie ohne Freigabe
splitten.

---

## ABLAUF (Standard)

### Schritt 1 — Skill identifizieren

Wenn nicht klar welcher Skill: Auswahlfrage mit der Ordnerliste aus `skills/` des Repos
(Cowork alternativ `/mnt/skills/user/`).

### Schritt 2 — Original laden

```
Cowork:      view /mnt/skills/user/<name>/SKILL.md
Claude Code: Read <skills-repo>/skills/<name>/SKILL.md (+ references/)
```

Komplett lesen. Nicht scrollen, nicht abkürzen. Dabei die Split-Prüfung (Regel 21) mitlaufen lassen.

### Schritt 3 — Änderungs-Plan ausarbeiten

Konkret schreiben:
- Welche Abschnitte bleiben unverändert? (Liste der H2-Überschriften)
- Was wird neu hinzugefügt? (exakter Text)
- Was wird inline geändert? (vorher/nachher Paare)
- Was wird gelöscht? (hoffentlich leer)

### Schritt 4 — User-Freigabe für den Plan

Nur wenn Änderungen größer sind als 1-2 Zeilen:

```
Auswahlfrage:
Frage: "Plan für <skill-name> Update. OK so?"
Optionen: "Ja, umsetzen", "Anders machen", "Abbrechen"
```

### Schritt 5 — Repo-Datei editieren

Änderungen direkt ins Repo schreiben:

```
Cowork:      DC edit_block <repo-pfad>/skills/<name>/SKILL.md  (old_string → new_string)
             komplette Neu-Schreibe: DC write_file mit mode: "rewrite"
Claude Code: Edit (old_string → new_string) bzw. Write; bei vielen Stellen ein Patch-Skript
             im Scratchpad, das jede Ersetzung prüft (Fehler, wenn der Originaltext fehlt)
```

Immer absolute Pfade. Danach description-Länge messen (Regel 6).

### Schritt 5a — CHANGELOG, INDEX, Commit, Push (Regel 12a)

`[vX.Y.Z] <skill>, <Typ>: <Kurztitel>` – Version laut git-commit-helper; CHANGELOG-Eintrag mit
denselben Worten; INDEX-Zeile nur bei geänderter Zuständigkeit.

### Schritt 6 — Lieferung mit vollständigem neuen Inhalt

**Claude Code:** `SendUserFile` mit der SKILL.md aus dem Repo – bei Skills mit `references/` eine
Zip (SKILL.md + references/), gebaut aus dem Repo-Stand nach dem Commit. Caption: Skill, Version,
was geändert ist, „bei claude.ai speichern/hochladen“. Keine Auswahlfrage im selben Block (14a).

**Cowork:** Claude erstellt ein Artifact als Tool-Call-Paar:

```
Schritt A (Container-Schreibvorgang):
create_file
  path: /home/claude/SKILL.md
  file_text: <komplette neue Skill-Datei>

Schritt B (UI-Rendering):
present_files
  filepaths: ["/home/claude/SKILL.md"]
```

**Dateiname exakt `SKILL.md`** (keine Prefixes/Suffixes — siehe Regel 13).

Ohne den `present_files`-Aufruf sieht der User NICHTS in der UI. Siehe
Regel 14 und skill-pflege-006.

Der User sieht die Dateikarte in Claude.ai und klickt "Skill speichern".

### Schritt 7 — Diff-Report im Chat

Kompakt zeigen was sich geändert hat (siehe Regel 10).

### Schritt 8 — Auf User-Speicher-Bestätigung warten

Nicht weiter bis User "gespeichert" oder "ok" oder ähnliches bestätigt.

### Schritt 9 — Wenn Batch: Auswahlfrage für nächsten Skill

```
Frage: "Nächsten Skill updaten?"
Optionen: "Ja, nächster: <Name>", "Pause", "Anderer Skill", "Fertig für heute"
```

---

## BEISPIEL-WORKFLOW (Cowork-Chat; in Claude Code: Read/Edit statt view/DC, SendUserFile statt create_file)

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

## AUTO-ISSUE-ERKENNUNG (skill-pflege-002)

Wenn Claude beim Arbeiten mit einem Skill **proaktiv** einen der folgenden
Fälle erkennt, MUSS er den User informieren und ein Issue vorschlagen:

### Trigger für Auto-Issue-Erkennung

- **Skill-Regel widerspricht expliziter User-Anweisung im aktuellen Chat**
  (z.B. User sagt "mach X direkt in der Datei", Skill-Regel sagt "SUCHE/ERSETZE verwenden")
- **Zwei Skills haben widersprüchliche Anweisungen zum gleichen Thema**
- **Referenzen im Skill auf nicht-existente Dateien/Pfade** (tote Links)
- **Veraltete Pfade oder IDs im Skill** (z.B. Listen-IDs die sich geändert haben)
- **Werkzeug- oder Projektbindung** (nur Cowork-Werkzeuge genannt, BPM-Werte hart im Skill) → Neutralisieren vorschlagen
- **Split-Kandidat** (Regel 21 trifft zu)
- **Trigger greift in Near-Miss-Phrasen versehentlich** (Over-triggering)
- **Trigger greift NICHT wo er sollte** (Under-triggering)

### Ablauf bei Trigger-Erkennung

1. **User kurz informieren** (Prosa, offene Info):
   ```
   Hinweis: Beim Arbeiten mit Skill <X> ist mir aufgefallen, dass
   <Regel Y> widerspricht <expliziter User-Anweisung Z / anderer Regel>.
   ```

2. **Auswahlfrage** mit Issue-Vorschlag:
   ```
   Frage: "Issue in <skill>-Issues-Liste anlegen?"
   Optionen:
     - "Ja, <skill>-NNN anlegen"
     - "Später selbst"
     - "Kein Issue nötig"
   ```

3. Bei Zustimmung: `tracker issue <skill>: <kurztitel>`
   (Issue-ID wird automatisch via `tracker-003` ermittelt)

### Was NICHT auslöst

- Minimale Inkonsistenzen (Tippfehler, Kommas)
- Stilistische Unterschiede zwischen Skills
- Regeln die User selbst im aktuellen Chat gerade ändert (dann ist das keine Issue, sondern aktive Pflege)
- Fehlende Features die der User nie angefragt hat

### Abgrenzung

- **Auto-Issue-Erkennung ≠ Auto-Issue-Anlage**: Claude informiert + schlägt vor, User entscheidet. Nie ungefragt anlegen.
- **Auto-Issue-Erkennung ≠ Review-Workflow** (tracker-006): Review prüft Task-Scope vor Übergängen, Auto-Erkennung prüft Skill-Qualität während der Arbeit.

---

## MEMORY-CLEANUP (nach Abschluss)

Memory-Einträge werden **nie stillschweigend entfernt**. Auch wenn ein
Change eindeutig einen Memory-Eintrag erledigt, läuft das Cleanup über
eine explizite Bestätigungs-Sequenz.

### 3-Schritt-Sequenz

Wenn ein Skill-Change einen bestehenden Memory-Eintrag (Rubriken
`[VERIFY]`, `[ARCH-OPEN]`, `[INFRA-TODO]`, `[REVIEW-PENDING]`) erledigt:

1. **Herbert hinweisen** — kurze Prosa-Zeile im Chat, welcher
   Memory-Eintrag durch den Change potentiell erledigt ist
2. **Bestätigung einholen** — Auswahlfrage:
   ```
   Frage: "Memory-Eintrag <Kurztext> jetzt entfernen?"
   Optionen: "Ja, entfernen", "Behalten", "Später entscheiden"
   ```
3. **Bei Bestätigung:** Cowork `memory_user_edits(command: "remove", line_number: <n>)`;
   Claude Code: Memory-Datei im Memory-Ordner löschen und die Zeile in `MEMORY.md` entfernen

### Wichtig

- **Cleanup ist KEIN eigener Trigger** — läuft nur als Nachgang einer
  anderen Skill-Pflege-Aktion
- **Nie stillschweigend entfernen** — auch wenn der Change offensichtlich
  den Eintrag obsolet macht, immer erst Bestätigung einholen
- Gilt nur für die 4 Memory-Rubriken. `[CLICKUP]`, `[SKILL-ISSUES]`,
  `[ANKER-LIVE]`, `[PROJECT]` sind dauerhafte Konventionen und werden
  durch eigene Lifecycle-Regeln gepflegt.

### Abgrenzung

- **MEMORY-CLEANUP** (hier) = Memory-Einträge entfernen nach Skill-Änderung
- **Regel 17/18** (oben in HARTE REGELN) = Skill-Inhalte selbst löschen
  (Abschnitte, Duplikate im SKILL.md) — anderes Thema

Vollständige Memory-Rubriken-Konvention: `MEMORY-RUBRIKEN.md`.

Adressiert Phase 4.3.

---

## VERBOTEN

- Skills aus dem Gedächtnis neu schreiben (immer Original laden)
- Mehrere Skills parallel in einer Antwort erstellen
- **Zwei oder mehr Skill-Artifacts in einer Antwort erstellen** — das zweite `create_file /home/claude/SKILL.md` überschreibt das erste. Beide Dateikarten zeigen dann denselben Inhalt. Ein Artifact pro Antwort, User-Bestätigung abwarten, dann nächstes (skill-pflege-007, siehe Regel 13b)
- Originalinhalte still entfernen, kürzen, zusammenfassen
- Stilistische "Verbesserungen" am Original ohne Freigabe
- Umformulieren bestehender Formulierungen ohne Freigabe
- Frontmatter ändern ohne explizite Anweisung
- Versions-Suffixe in den Skill-Dateinamen einfügen (immer `SKILL.md`)
- Zwischen mehreren Skills ohne Auswahlfrage-Bestätigung wechseln
- Diff-Report weglassen bei nicht-trivialen Änderungen
- **Prosa-Fragen bei festen Entscheidungsoptionen** — IMMER Auswahlfrage
- **Auswahlfrage direkt nach Artifact/Lieferung im selben Antwort-Block** — verdrängt das Artifact in der UI (skill-pflege-003)
- **Skill-Commit ohne Lieferung an den User** (Artifact bzw. SendUserFile) — aktive Claude.ai-Skills bleiben sonst beim alten Stand (skill-pflege-005)
- **Skill mit references nur als SKILL.md liefern** — Zip mit SKILL.md + references/, sonst fehlen bei claude.ai die Abläufe
- **description über 1024 Zeichen liefern** — Upload wird abgelehnt; vorher messen und kürzen
- **Skill ohne CHANGELOG-Eintrag und Commit liefern** — Repo und Upload laufen sonst auseinander (Regel 12a)
- **Splitten ohne Freigabe** oder beim Splitten Text neu formulieren — verschieben, Routing-Tabelle ergänzen, Auswahlfrage vorher (Regel 21)
- **`create_file` für Skill-Artifacts ohne direkt folgenden `present_files`-Aufruf** — die Datei landet nur in der Container-Sandbox, keine Dateikarte, kein "Skill speichern"-Button (skill-pflege-006)
- **Memory-Einträge stillschweigend entfernen** — auch nach offensichtlicher Erledigung: erst Hinweis an Herbert, dann Bestätigung per Auswahlfrage, dann entfernen (Cowork `memory_user_edits remove`, Claude Code Memory-Datei + Indexzeile) (siehe MEMORY-CLEANUP, Phase 4.3)


---

## VERWEIS

**Komplett neuen Skill anlegen? → `skill-neu`**

`skill-neu` ist der Schwester-Skill für Neu-Erstellung. Er hat eigene Struktur (Capture-Intent-Interview, Description-Schema, Test-Prompt-Setup). `skill-pflege` macht ausschließlich Änderungen an bestehenden Skills.

Faustregel:
- Existiert die SKILL.md schon? → `skill-pflege` (hier)
- Datei wird ganz neu angelegt? → `skill-neu`
