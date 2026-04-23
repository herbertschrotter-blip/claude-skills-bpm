# tracker neu — Task anlegen

Vollständiger Ablauf, Description-Template und Beispiel-Workflow für `tracker neu`.

**Abgrenzung:** Diese Datei behandelt den Standard-Fall `tracker neu` für
Haupttasks im Projekt-Scope (z.B. BPM-Listen, ClaudeSkills-Liste).
Für **Skill-Issues** (`tracker-NNN`, `cc-steuerung-NNN`, etc.) gilt das
Kommando `tracker issue <skill>: <titel>` und die separate Spec in
`references/issue-task.md` — mit eigenem Field-Scope und eigener
Nummerierungslogik.

---

## Kommando

`tracker neu: <Beschreibung>`

### Schnellmodus
"neue aufgabe: PM — Index-Erkennung spinnt, v1, high, Fix, M"
→ Direkt anlegen.

### Fragemodus (Infos fehlen)

Per `ask_user_input_v0` (nicht Prosa!). Gültige Werte für Modul-Auswahl
und Meilensteine stehen in `projects/<[PROJECT]>/clickup-fields.md`
(Modul-Kürzel-Tabelle + Meilenstein-Tags). Konkrete Zielversion-Optionen
ergeben sich aus Memory `[CLICKUP]` und dem aktuellen Release-Stand.

Beispiel (BPM-Projekt):
```
Frage 1 — Modul: PlanManager, Settings, Infrastructure, Docs, Anderes
Frage 2 — Meilenstein: v1, v1-nice, post-v1, backlog
Frage 3 — Priorität: urgent, high, normal, low
```

Nach Basics fragen per `ask_user_input_v0`:
```
Frage 1 — Typ: Feature, Fix, Refactor, Perf, Docs, Konzept, Meta
Frage 2 — Aufwand: S (<1h), M (1-4h), L (halber Tag), XL (>1 Tag), Später
Frage 3 — Zielversion: Aktuelle, Nächste Minor, später
```

Die konkreten Typ/Aufwand-Options sind projekt-spezifisch — siehe
`projects/<[PROJECT]>/clickup-fields.md`.

Offensichtliches aus Kontext überspringen. Max 3 Fragen pro Aufruf.

**Prosa-Fragen für Freitext:**
- "Welche Komponente/Datei ist betroffen?" (falls Code-Bezug)
- "Welche Docs sind relevant?" (falls Doc-Bezug)

---

## Ablauf

1. Nächste freie Haupt-Nummer aus Memory `[CLICKUP]` (z.B. `BPM-<Next>`) — Prefix aus `projects/<[PROJECT]>/clickup-fields.md`
2. Kürzel + Liste-ID aus `projects/<[PROJECT]>/clickup-fields.md` (Modul-Kürzel-Tabelle) bzw. `projects/<[PROJECT]>/clickup-lists.md`
3. Dedup: `clickup_search` → wenn Treffer, mit `ask_user_input_v0` fragen: Trotzdem neu, Bestehenden nutzen, Abbrechen
4. **Description**: Template aus Abschnitt "Description-Template" unten generieren
5. **TEMP-Anker aus `[ANKER-LIVE]` prüfen** (siehe `anker-system.md`):
   - `[ANKER-LIVE]` aus Memory lesen
   - Gibt es einen Eintrag mit Typ `offen` zum Thema dieses Tasks? → TEMP-ID merken
   - Sonst: kein TEMP (Phase 2 ohne vorherige Phase 1)
6. `clickup_create_task(list_id, name, priority, tags, markdown_description)` → Task-ID erhalten
7. **Pro-Task-Quittung im Chat schreiben** (direkt nach `clickup_create_task`):
   ```
   ✅ <BPM-ID oder Issue-ID> — [BPM-ANCHOR-<task-id>] — erstellt: <kurzbeschreibung>
   ```
   Die Quittung ist Bestätigung + Body-Anker + Audit-Zeile in einem Format.
   Bei TEMP-Brücke: ` (war TEMP-<id>)` anhängen.
   **Bei ≥2 Tasks in einer Antwort:** Vollständiges Batch-Protokoll greift — siehe `references/batch-protocol.md` (Batch-Ansage, Pro-Task-Zyklus, Batch-Audit).
8. **Custom Fields nachträglich setzen** via `clickup_update_task`. Beispiel-Struktur:
   ```
   custom_fields = [
     {"id": "<Typ-Field-ID>",         "value": "<Typ-Option-ID>"},
     {"id": "<Aufwand-Field-ID>",     "value": "<Aufwand-Option-ID>"},
     {"id": "<Zielversion-Field-ID>", "value": "<Version>"},
     {"id": "<Komponente-Field-ID>",  "value": "<Datei/Modul>"},
     {"id": "<Docs-Field-ID>",        "value": "<Doc-Pfad>"},
     {"id": "<Chat-Anker-erstellt-ID>", "value": "[BPM-ANCHOR-<task-id>] ..."},
     // Falls TEMP existierte:
     {"id": "<Chat-Anker-temp-ID>",   "value": "TEMP-<id>"}
   ]
   ```
   Konkrete Field-IDs und Option-IDs: `projects/<[PROJECT]>/clickup-fields.md`.
9. **Memory `[ANKER-LIVE]` aktualisieren**:
   - Falls TEMP existierte: Eintrag **ersetzen** (TEMP-... → Task-ID-Eintrag mit Typ `erstellt`)
   - Sonst: neuen Eintrag hinzufügen mit Typ `erstellt`
10. Memory: Next +1
11. Bestätigung an User inkl. Task-ID als Anker-Referenz

---

## Description-Template (Default bei tracker neu)

Neue Tasks bekommen automatisch dieses Markdown-Template als Description:

```markdown
## Problem
<Was ist kaputt / was fehlt / was muss besser werden?>

## Lösungsansatz
<Wie lösen wir das konkret? Falls noch unklar: "Offen">

## Acceptance Criteria
- [ ] <Kriterium 1>
- [ ] <Kriterium 2>

## Definition of Done
- [ ] Code implementiert
- [ ] Manuell getestet
- [ ] Dokumentation aktualisiert
- [ ] Commit gemacht

## Abhängigkeiten / Related
<Falls ClickUp-Dependencies gesetzt: hier noch mal Freitext-Notizen>
<Oder Verweise auf Docs: Docs/Kern/DB-SCHEMA.md>

## Technische Notizen
<Beliebige weitere Infos, Code-Snippets, Links, Hintergrund>
```

**Regeln:**
- Für **Meta-Tasks** (ClickUp-Pflege, Skill-Updates) das Template **verkürzen**:
  nur Problem + Lösungsansatz
- Für **Mockup-Tasks**: AC ersetzen durch konkrete Screen-Bereiche
- Für **Konzept-Tasks**: DoD nur "Konzept-Doc geschrieben + in INDEX verlinkt"
- Template auch bei `tracker done` prüfen: DoD-Checkliste abhaken

### Bei Unteraufgaben

Unteraufgaben bekommen ein **verkürztes Template**:

```markdown
## Aufgabe
<Was genau in diesem Schritt?>

## Definition of Done
- [ ] <konkret>
```

Kein Problem/Lösungsansatz (das steht im Parent).

---

## Beispiel-Workflow (BPM-Projekt, `tracker neu` mit allen Feldern)

Dieser Beispiel-Ablauf zeigt einen konkreten `tracker neu`-Durchlauf für BPM.
Feld-IDs und Option-IDs stehen in `projects/bpm/clickup-fields.md`.

```
User: tracker neu: PM — neue Regex-Erkennung in DocumentTypeRecognizer, v1, high

Claude intern:
  1. BPM-<Next> aus Memory: BPM-082
  2. Kürzel PM → Liste-ID aus projects/bpm/clickup-fields.md (PlanManager-Zeile)
  3. Dedup: clickup_search "Regex DocumentTypeRecognizer" → kein Treffer
  4. ask_user_input_v0:
     Frage 1 — Typ: Feature, Fix, Refactor, Perf, Docs, Konzept, Meta
     Frage 2 — Aufwand: S, M, L, XL, Später
     User antwortet: Feature, M
  5. Prosa-Frage: "Welche Komponente?"
     User: "DocumentTypeRecognizer.cs"
  6. Prosa-Frage: "Zielversion?"
     User: "v0.26.0"
  7. Description-Template generieren
  8. Chat erstellt = aktueller Chat (URL aus Session-Memory)
  9. custom_fields = [Typ=Feature, Aufwand=M, Zielversion=v0.26.0, 
                      Komponente=DocumentTypeRecognizer.cs, Chat erstellt=<url>]
  10. clickup_create_task(...) → Task-ID 86c9xyz12 erhalten
  11. Pro-Task-Quittung im Chat:
      ✅ BPM-082 — [BPM-ANCHOR-86c9xyz12] — erstellt: Neue Regex-Erkennung DocumentTypeRecognizer
  12. clickup_update_task(task_id="86c9xyz12", custom_fields=[{Chat-Anker erstellt: "[BPM-ANCHOR-86c9xyz12] - erstellt: Neue Regex-Erkennung"}])
  13. Memory: Next 082 → 083
```
