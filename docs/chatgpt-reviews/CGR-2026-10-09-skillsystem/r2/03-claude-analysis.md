# Runde 2 – Einschätzung Claude

## Übernehmen

- **Generator kennt keine Stack-Sonderfälle**, nur Auftrag, Bausteine, Dateien, Platzhalter, Prüfschritte; Struktur und
  Checks kommen aus dem Manifest. Damit wird HA ein weiterer Baustein.
- **JSON-Auftrag v1** wie vorgeschlagen (fünf Felder, strenge Validierung, keine Zusatzfelder, keine Befehle); Ablage,
  Owner, Policies und Checks bleiben im Skill-Profil bzw. in den Vorlagen; Zielordner als Argument mit Prüfung gegen die
  Ablage.
- **Strukturierter Renderer** für gemeinsam genutzte Dateien (pyproject.toml) statt Textfragmenten. Hinweis: Die
  Standardbibliothek liest TOML (`tomllib`), schreibt es aber nicht – der Renderer schreibt den kleinen benötigten
  Ausschnitt selbst.
- **Walking Skeleton „status“** (CLI → Service → Store → SQLite bzw. In-Memory), Starttest, echter SQLite-Integrationstest,
  Ruff für Format und Lint, Versionskatalog im Generator statt PyPI-Abfrage.
- **Zwei Phasen** Prepare und Verify & Publish, Staging im selben Dateisystem, Ziel erst nach grünen Checks sichtbar;
  GitHub-Repo und Push erst danach im bestätigungspflichtigen Ablauf.
- **Eigener Workflow** `test-project-generator.yml` für die Kombinationen; schnelle Generator-Unit-Tests zusätzlich in
  `validate-skills.yml`.
- **Neue Regel für code-erstellen** (Grundentscheidungen am `Doku.Entscheidungs-Ort` vor der ersten fachlichen
  Erweiterung lesen) – knapp, kein neues Pflichtfeld.
- **Rückfragen 1–4** (alle technisch, ohne Herbert entschieden): ci-github bei GitHub-Repos standardmäßig; kleine
  Herkunftsdatei im erzeugten Projekt (Generator-Version, Stack, Bausteine; nie aktualisiert); neue
  Abhängigkeitsversionen nur nach grünen Kombinationstests und Freigabe über skill-pflege; HA mit SQLite später über
  eigenen Adapter.

## Anpassen

- **Description-Entwurf** (927 Zeichen): verliert zwei Auslöser, die heute zünden und Eval-Fälle haben – das Klonen
  eines vorhandenen GitHub-Repos und die deutschen Sätze „neues Projekt“ / „ich will X bauen, weiß aber nicht wie“.
  Ich formuliere ihn im Refactor neu und messe mit den vorhandenen sieben plus den neuen Fällen.
- **Ordner `generator/`:** Präzedenzfall im Repo ist `skills/sitzung/scripts/`. Ich nehme `scripts/` für die Skripte
  und `templates/` daneben, damit das Muster gleich bleibt; die Lieferung bei claude.ai bleibt SKILL.md + references/
  (Generator läuft dort nicht), dafür ist ein Satz in `skill-pflege/references/delivery.md` nötig.
- **Prüfskript:** `tools/validate-skills.ps1` muss die neuen Ordner unter einem Skill dulden und die Generator-Tests
  kennen; im Umbau mitprüfen.

## Bereit zur Umsetzung

Die Reihenfolge aus Abschnitt 8 übernehme ich. Offen für Herbert ist nur, ob die Serie hier endet und der Umbau
beginnt, und wohin die Ergebnisse gehen (Umbau-Plan, ClickUp-Aufgabe).
