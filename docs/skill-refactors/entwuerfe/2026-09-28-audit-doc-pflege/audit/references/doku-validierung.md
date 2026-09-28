# Doku-Validierung – Prüflisten

Prüflisten für audit, Modul 6 („Formale Doc-Prüfung nach Profil“): was bei der Doku-Validierung eines Projekts geprüft
wird. Vorrang hat `Doku.Validierungsregeln` des Skill-Profils (ohne Skill-Profil: Feld „Validierung“ des Doku-Profils);
diese Listen gelten, solange ein Projekt sie nicht dort führt.

## Heidi-Prüfliste (aus dem Doku-Profil)

Stufe A — Blocker:
- Statusliste (Bauplan Abschnitt 1) ↔ ClickUp-Status (DX-Aufgaben) ↔ Code: fertig nur, wenn Code, Tests und Commit da sind
- Jede Abweichung von v1 hat einen PD-Eintrag in 10a mit Status `freigegeben`
- Abschnitt 4 (Entitäts-Vertrag) ↔ `contract.ts`: gleiche Entitäten, gleiche Dienste
- HANDOFF Abschnitt 3e nennt den letzten abgeschlossenen Bauschritt und die aktuelle Version
- Nichts Verbotenes im Repo (Token, GPS, `.storage`, Datenbanken, Laufprotokolle)

Stufe B — Warnung:
- ⚠️ Notiz in Abschnitt 10 ohne Datum, Aufgabe, Art oder Schwere; Entscheidung Herbert fehlt bei Widerspruch/Wunsch
- ⚠️ Aufgabenkarte ohne Akzeptanz oder ohne Tests
- ⚠️ Offene Punkte (HANDOFF Abschnitt 4) ohne Gegenstück in ClickUp
- ⚠️ Plan-Doc (GERAETEPROFIL, PLANER-NACHHOLEN, UX-TRANSITIONS) ohne Stand-Datum
- ⚠️ Version in package.json, Lock und Ressourcen-`?v=` uneinheitlich

## BPM-Prüfliste: Frontmatter + Quickload

### Stufe A — Formal (Blocker)

- Frontmatter vorhanden bei Kern/, Module/, Referenz/?
- Alle Pflichtfelder?
- doc_id eindeutig?
- Enums korrekt?
- Quickload bei source_of_truth/secondary?
- Quickload Kapitel-Feld stimmt mit H2s?
- Kapitelreihenfolge nach Vorlage?
- Pflichtlesen verweist auf existierende Kapitel?
- Fachliche Invarianten max 5?

### Stufe B — Semantisch (Warnung)

- ⚠️ Quickload Kapitel stimmt nicht mit H2s
- ⚠️ historical als Primary im Router
- ⚠️ related_docs nicht existent
- ⚠️ Kapitelvorlage nicht eingehalten
- ⚠️ Fachliche Invarianten leer bei großem Modul
- ⚠️ Pflichtlesen leer bei source_of_truth Modul

## Heidi-Kurzprüfung

Karten mit allen Feldern (Voraussetzung, Ziel, Nicht ändern, Akzeptanz);
Statusliste ohne Lücken; keine Notiz ohne Datum/Art/Schwere; PD-Tabelle vollständig gefüllt.

## BPM-Kurzprüfung

### 6a. Frontmatter-Vollständigkeit
- Frontmatter vorhanden? Pflichtfelder? doc_id eindeutig?

### 6b. Quickload-Vollständigkeit
- Quickload vorhanden bei source_of_truth/secondary?
- Kapitel-Feld stimmt mit H2s?

### 6c. Cross-Checks
- INDEX referenziert nur Docs mit gültigem Frontmatter?
- source_of_truth hat Quickload?
- historical NICHT als Primary im Router?
- Keine doppelten doc_ids?
- Fachliche Invarianten nicht widersprüchlich zwischen Docs?
