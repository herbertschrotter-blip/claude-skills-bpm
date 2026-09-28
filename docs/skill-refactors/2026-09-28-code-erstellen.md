# Regel-Inventar – code-erstellen (Abschnitt Arbeitsverzeichnis) – 2026-09-28

Teil-Refactor von code-erstellen in Umbau-Phase 5, Punkt „Cowork-Pfadermittlung aus audit, code-erstellen, doc-pflege und
mockup-erstellen entfernen“ (`docs/skillsystem-umbau.md`). Umfang nur der Abschnitt „Arbeitsverzeichnis“; der ganze Skill
bekommt in Phase 6 ein eigenes Inventar. Die Pfadermittlung für den Cowork-Chat steht seit v0.38.1 in cc-steuerung
(`docs/skill-refactors/2026-09-28-cc-steuerung.md`); hier war sie kopiert. Nach dem Refactor-Ablauf von skill-pflege
(`skills/skill-pflege/references/rule-inventory.md`), Regeln nach Urteil gesammelt (Abschnitt von 30 Zeilen).

- Skill: code-erstellen
- Stand vorher: 8a3e1f8 (SKILL.md, 523 Zeilen; Abschnitt Z. 141–170)
- Quellen: SKILL.md#Arbeitsverzeichnis (PFLICHT bei Dateizugriff)

## Zielstruktur

| Datei | Abschnitte |
|---|---|
| `SKILL.md` | unverändert bis auf „Arbeitsverzeichnis“: Claude Code · Cowork-Chat (Verweis) · keine hartkodierten Pfade |

Abkürzungen im Neu-Ort: `S` = `SKILL.md#Arbeitsverzeichnis (PFLICHT bei Dateizugriff)`; `CC` =
`skills/cc-steuerung/SKILL.md`; `CCD` = `skills/cc-steuerung/references/desktop-commander.md`.

## Inventar

| ID | Alt-Ort | Regelkern | Zustand | Neu-Ort | Bezug | Freigabe | Prüfung |
|---|---|---|---|---|---|---|---|
| R001 | SKILL.md#Arbeitsverzeichnis (Z. 143–145) | Claude Code: Repo-Wurzel der Sitzung (`git rev-parse --show-toplevel`); bei Worktrees der Worktree, nie das Haupt-Checkout | KEEP | S | | | ✅ |
| R002 | SKILL.md#Arbeitsverzeichnis (Z. 145) | Der Rest des Abschnitts betrifft nur den Cowork-Chat | REWRITE | S | entfällt als Satz, weil nur noch eine Cowork-Zeile folgt; die Zeile ist mit „Cowork-Chat“ gekennzeichnet | | ✅ sinngemäß |
| R003 | SKILL.md#Arbeitsverzeichnis (Z. 147–148) | Cowork: bei DC-Operationen Arbeitsverzeichnis nach cc-steuerung Kapitel 4 ermitteln | REWRITE | S | Verweis über die Überschrift „Arbeitsverzeichnis“ statt „Kapitel 4“ | | ✅ sinngemäß |
| R004 | SKILL.md#Ablauf (Z. 150–155) | Pfad-Ermittlung beim ersten DC-Aufruf: `hostname` und OneDrive-Pfad per PowerShell | MERGE | CC#Arbeitsverzeichnis | cc-steuerung R043; der kopierte Befehl nutzte `$pc`-Variablen, die cc-steuerung verbietet | | ✅ sinngemäß |
| R005 | SKILL.md#Ablauf (Z. 157–159) | PC in der INDEX.md-Tabelle suchen; gefunden → OneDrive-Pfad + Suffix, sonst Self-Registration | MERGE | CC#Arbeitsverzeichnis | cc-steuerung R046, R047 | | ✅ sinngemäß |
| R006 | SKILL.md#Ablauf (Z. 161–164) | Pfad mit `Test-Path` prüfen | MERGE | CC#Arbeitsverzeichnis | cc-steuerung R048 | | ✅ sinngemäß |
| R007 | SKILL.md#Ablauf (Z. 166) | Arbeitsverzeichnis für die Sitzung merken | MERGE | CC#Arbeitsverzeichnis | cc-steuerung R054 | | ✅ sinngemäß |
| R008 | SKILL.md#Ablauf (Z. 168–169) | `$env:OneDrive` geht über DC nicht; immer `GetEnvironmentVariable('OneDrive','User')` | MERGE | CCD#PowerShell ohne `$`-Variablen | cc-steuerung R067 | | ✅ sinngemäß |
| R009 | SKILL.md#Ablauf (Z. 170) | Keine hartkodierten absoluten Pfade, in keiner Umgebung | KEEP | S | | | ✅ |

## DROP-Gruppen

Keine. Alle entfernten Zeilen gehen in cc-steuerung auf (MERGE).

## Verweise von außen

| Stelle | Verweis | Behandlung |
|---|---|---|
| `docs/skill-refactors/2026-09-28-cc-steuerung.md`, Verweise von außen | „cc-steuerung Kapitel 4“, „Self-Registration (cc-steuerung 4.3)“ in code-erstellen | mit diesem Commit erledigt |

## Prüfung

- **Freigabe:** Zielstruktur von Herbert am 28.09.2026 freigegeben (Auswahlfrage vor dem Schreiben); keine DROP-Zeile.
- **Alt→Neu:** 9 IDs mit Zustand (KEEP 2, REWRITE 2, MERGE 5); jeder Neu-Ort gelesen, in code-erstellen und cc-steuerung.
- **Neu→Alt:** Der neue Abschnitt hat drei Aussagen, zugeordnet zu R001, R003 und R009; keine neue Regel.
- **Größe:** SKILL.md 523 → 504 Zeilen. Prüfskript 0 Fehler, Warnungen des Skills unverändert 7.
- **Routing-Eval:** wird nach dem Commit eingetragen.
