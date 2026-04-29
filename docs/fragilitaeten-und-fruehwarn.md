# Fragilitäten und Frühwarn-Indikatoren

**Quelle:** CGR-2026-04-skillsystem-r6, Kapitel 4
**Stand:** 2026-04-29
**Zweck:** Konkrete Beobachtungssignale für die 4 wichtigsten Fragilitäten im
Skill-System. Jede Sektion: Indikatoren + Sofortmaßnahme + Beispiel +
Gegenbeispiel. Diese Doku wird beim Handover (`chat-wechsel` Memory-Scan
Schritt 4) gegen den laufenden Chat geprüft und bei Treffern als
Eskalationshinweis übernommen.

---

## Wozu diese Doku

Das Skill-System hat 4 wiederkehrende Fragilitäten, die in der Praxis schwer
zu erkennen sind, weil sie nicht hart fehlschlagen — sie schleichen sich ein.
Diese Liste macht sie beobachtbar:

- **Indikator** = Verhalten, das die Fragilität ankündigt
- **Sofortmaßnahme** = was Claude / Herbert in dem Moment tut
- **Beispiel / Gegenbeispiel** = konkrete Sätze oder Aktionen zur Kalibrierung

Der Anhang in [MEMORY-RUBRIKEN.md](../MEMORY-RUBRIKEN.md) verlinkt hierher
für die Memory-spezifische Fragilität (Sektion 3).

---

## 1. cc-steuerung-Pfad-/Modalitätsfragilität (Top 1)

Die häufigste Fragilität: cc-steuerung wird nicht erkannt, oder DC wird zwar
benutzt, aber mit falschen Pfaden / falscher Shell-Mechanik.

### Indikatoren

- **Codeblöcke statt Dateioperation:** Claude liefert XAML/C#/Markdown als
  Codeblock im Chat, obwohl der User „cc“ / „dc“ / „direkt auf den PC“ gesagt
  hat — keine `write_file` / `edit_block`-Calls.
- **Hartkodierte Pfade:** `D:\OneDrive\...` oder `C:\Users\herbe\...` ohne
  Auto-Discovery via `hostname` + `[System.Environment]::GetEnvironmentVariable('OneDrive','User')`.
- **`$`-Variablen in PowerShell-Command-Strings:** `$env:OneDrive`, `$path = ...`
  — werden von der äußeren Shell-Schicht zu leerem String interpoliert.
- **Fehlende Branch-/PC-Frage:** Claude beginnt mit Operationen ohne vorher
  per `ask_user_input_v0` Branch oder PC-Identität zu klären.
- **Vergessene `code-erstellen`-Pflichten:** Bei `cc + code` läuft nur die
  cc-steuerung-Modalität, aber INDEX-Routing / Quickloads / Pflichtlesen aus
  `code-erstellen` werden übersprungen.
- **Paraphrasierte Tool-Outputs:** Claude beschreibt das DC-Ergebnis statt
  den echten Output zu zitieren (Halluzinationsrisiko).

### Sofortmaßnahme

1. **Stop** — keine weitere Operation, bevor das Signal eingeordnet ist.
2. Case in `evals/smoke-all-skills.md` aufnehmen mit Datum + Trigger-Satz.
3. INDEX-Regel und betroffenes SKILL.md prüfen: Stimmen Description und Body
   noch mit dem beobachteten Verhalten überein?
4. Bei **2+ Reproduktionen** in echten Sessions: **Variante A umsetzen** —
   kurzer Modalitätsblock zusätzlich in den betroffenen Fachskills (siehe
   INDEX.md Invariante 9).

### Beispiel (Indikator-Treffer)

> User: „cc, leg die Datei `Docs/Konzepte/Wetter.md` an mit folgendem Inhalt …“
>
> Claude: „Hier ist der Inhalt für die Datei:
> ```markdown
> # Wetter-Modul
> ...
> ```
> Du kannst die Datei selbst anlegen."

→ **FAIL.** „cc“ war explizit. Korrekt wäre `write_file`-Call.

### Gegenbeispiel (sauber)

> User: „cc, leg die Datei `Docs/Konzepte/Wetter.md` an mit folgendem Inhalt …“
>
> Claude: [`ask_user_input_v0` für Branch] → [`write_file` mit echtem Pfad
> aus Auto-Discovery] → Quittung mit File-Pfad und Zeilenzahl.

---

## 2. Tracker-Anker / Task-Scope-Disziplin (Top 2)

Die zweithäufigste Fragilität: ClickUp-Tasks werden modifiziert, ohne dass
das Anker-System / Pro-Task-Quittungen / Scope-Disziplin sauber durchgezogen
sind.

### Indikatoren

- **Fehlender `[BPM-ANCHOR-…]`:** Task wird `created` / `updated` / `done`
  markiert, aber kein Anker im Chat-Body und/oder Custom Fields.
- **`tracker done` ohne Commit-Hash:** Task auf Done gesetzt, aber Custom
  Field „Commit ID“ leer oder mit Platzhalter befüllt.
- **Fehlende Pro-Task-Quittung:** Nach `create`/`status-change` gibt es keine
  Zeile `✅ <ID> — [BPM-ANCHOR-…] — <typ>: <kurz>` im selben Antwort-Block.
- **Multi-Task-Commit:** Ein Commit schließt 2+ unabhängige ClickUp-Tasks
  („Ein Commit = eine logische Änderung“ verletzt).
- **Fehlender Scope-Check:** Bei `tracker update` werden Felder geändert, die
  nicht zur ursprünglichen Task-Beschreibung gehören (Scope Creep).
- **„Machen wir später" nur im Chat:** Im Chat-Verlauf wird ein neuer Punkt
  als TODO benannt, aber nie als ClickUp-Task / Memory-Eintrag fixiert.

### Sofortmaßnahme

1. **Pause** — keine weitere Tracker-Aktion, bevor reconciliiert ist.
2. Anker und Status reconciliieren:
   - `clickup_get_task` für betroffene Task(s) abrufen
   - Custom Field „Chat-Anker erstellt“ / „Chat-Anker erledigt“ prüfen
   - Bei Lücke: Anker im Chat-Body **nachträglich** einfügen + Custom Field
     setzen (mit Hinweis „nachgetragen“)
3. Fehlende Commit-Hashes nachreichen via `github:list_commits`.
4. Bei „machen wir später"-Punkten: per `ask_user_input_v0` entscheiden lassen
   (ClickUp-Task / Memory-Eintrag / verwerfen).

### Beispiel (Indikator-Treffer)

> User: „Task 86c9xxx ist erledigt, mach done."
>
> Claude: [`clickup_update_task` mit `status: done`] → „Task ist done."
>
> ❌ kein Anker im Body, kein Commit-Hash, keine Pro-Task-Quittung

→ **FAIL.** Korrekter Output: Anker-Zeile + Commit-Hash + ✅-Quittung im
selben Antwort-Block.

### Gegenbeispiel (sauber)

> User: „Task 86c9xxx ist erledigt, mach done."
>
> Claude: [Commit-Hash via GitHub MCP holen] → [`clickup_update_task` mit
> status, Anker, Commit-ID, Erledigt-Datum, Zielversion] →
>
> ```
> ✅ 86c9xxx — [BPM-ANCHOR-86c9xxx] — erledigt: <Kurztitel>
> Commit: <hash>, v0.21.0
> ```

---

## 3. Memory-Schatten-Backlog

Memory-Rubriken werden statt zu einem Kurzzeit-Notizblock zu einem zweiten,
inoffiziellen Backlog. Die Folge: Punkte werden nicht erledigt, nicht
eskaliert, nicht entfernt — sie bleiben einfach.

### Indikatoren

- **5+ offene `[VERIFY]` / `[INFRA-TODO]`** nach einem Handover.
- **Wiederkehrende Punkte:** Derselbe Memory-Eintrag taucht in 3 oder mehr
  Handovers in Folge auf.
- **Erledigte Punkte werden referenziert:** Claude bringt einen Memory-Punkt
  in die Antwort ein, der laut Chat-Verlauf längst abgeschlossen ist.
- **Unklare Formulierung:** Eintrag ist nicht entscheidbar — niemand kann
  beim Lesen sagen, was er bedeutet oder wann er erledigt wäre.

### Sofortmaßnahme

Pro Indikator unterschiedlich (siehe auch
[MEMORY-RUBRIKEN.md](../MEMORY-RUBRIKEN.md) Anhang):

| Indikator | Reaktion |
|---|---|
| 5+ offen | Memory-Hygiene-Prompt: Welche erledigt, welche eskaliert, welche bleiben? |
| 3-Handovers-Wiederkehr | `tracker neu` vorschlagen — Eintrag ist substantieller als gedacht |
| Erledigte Referenz | Memory-Cleanup mit Bestätigung — Eintrag entfernen |
| Unklare Formulierung | Reformulierung verlangen oder löschen — keine Müllhalde |

### Beispiel (Indikator-Treffer)

> Memory enthält:
> - `[INFRA-TODO] BPM-Build prüfen`
> - `[INFRA-TODO] BPM-Build prüfen`
> - `[INFRA-TODO] Build pruefen`
>
> Drei fast-gleiche Einträge, alle vage formuliert, niemand weiß was geprüft
> werden soll.

→ **FAIL.** Korrekter Umgang: Beim Handover per `ask_user_input_v0` fragen,
ob ClickUp-Task daraus wird oder Eintrag entfernt wird, und neue
Formulierung verlangen.

### Gegenbeispiel (sauber)

> Memory enthält:
> - `[VERIFY] PlanManager-Tab-Wechsel friert ein bei großem Plan-Volumen — Repro pending`
>
> Konkret formuliert, mit Repro-Bedingung, klar entscheidbar wann erledigt.

---

## 4. Frühphasen-Verstoss

BPM ist in Frühphase (kein produktiver Live-Datenbestand außerhalb von
Herberts eigenem Test-Setup). Das Frühphasen-Prinzip lautet: **„Datei löschen,
neu anlegen lassen"** statt **Migration / Backward-Compat / Upgrade-Pfad**.
Verstöße produzieren unnötige Komplexität und führen zu Code, der den
Hauptpfad verwässert.

### Indikatoren

- **Migrations-/Legacy-Vorschläge:** Claude schlägt bei Schema-/Config-/DB-
  Änderungen einen Migrationspfad vor („alte Versionen einlesen und
  konvertieren", „v1-Schema und v2-Schema parallel unterstützen").
- **Backward-Compatibility-Logik:** Code akzeptiert mehrere Schemaformen,
  Parser entscheiden zur Laufzeit über Format. Ohne expliziten User-Auftrag.
- **Upgrade-Pfade ohne Auftrag:** Eine `MigrationService` / `LegacyAdapter`-
  Klasse taucht im Code auf, obwohl der Auftrag nur „Schema X ändern" lautete.
- **Datenübernahme statt „löschen + neu anlegen":** Bei DB-Schema-Änderung
  wird existierende `bpm.db` mit `ALTER TABLE` migriert statt gelöscht.

### Sofortmaßnahme

1. **Stop** — Vorschlag verwerfen, bevor er in Code landet.
2. Den User explizit fragen via `ask_user_input_v0`:
   - „Datei/DB löschen + neu anlegen lassen" (Default in Frühphase)
   - „Migration schreiben" (nur mit explizitem Auftrag)
   - „Anders — bitte erklären"
3. Frühphasen-Prinzip ist Invariante 4 in INDEX.md — bei wiederholten
   Verstößen Description / Body der betroffenen Skills schärfen.

### Beispiel (Indikator-Treffer)

> User: „Ändere `BpmManifest.cs` so, dass das Feld `ProjectId` jetzt ULID
> statt GUID ist."
>
> Claude: „Ich baue eine `BpmManifestMigrator.cs`-Klasse, die alte Manifeste
> mit GUID einliest und beim Laden in ULID konvertiert. So bleibt
> Backward-Compat erhalten …"

→ **FAIL.** Frühphase. Korrekt: Bestehende `.bpm-manifest`-Dateien werden
gelöscht, neue Projekte erzeugen die Datei mit ULID.

### Gegenbeispiel (sauber)

> User: „Ändere `BpmManifest.cs` so, dass das Feld `ProjectId` jetzt ULID
> statt GUID ist."
>
> Claude: „Frühphase — ich ändere das Schema direkt auf ULID. Bestehende
> `.bpm-manifest`-Dateien sind vor dem Update zu löschen (Hinweis im
> Commit-Body). Migration nur falls explizit gewünscht?"
> [`ask_user_input_v0`: löschen+neu / Migration / anders]

---

## Querverweise

- **INDEX.md** Sektion 10 verweist auf diese Doku
- **MEMORY-RUBRIKEN.md** Anhang verweist für Sektion 3 hierher
- **chat-wechsel/SKILL.md** Memory-Scan Schritt 4 prüft die Indikatoren
  beim Handover
- **CGR-Quelle:** `Docs/Referenz/chatgpt-reviews/CGR-2026-04-skillsystem/r6-chatgpt-response.md`
  Kapitel 4 (im BPM-Repo)
