# Runde 3 – Einschätzung Claude

- **Description:** übernommen. Gemessen 839 Zeichen (Python `len`, wie bisher für die Grenze). Alle sieben bestehenden
  Auslöser sind enthalten (anlegen, Repo holen/klonen, unklare Idee, Profil einrichten, Abgrenzung code-erstellen,
  mockup-erstellen, skill-neu). Endgültig erst nach der Routing-Eval.
- **17 Fälle:** übernommen, inklusive des schärferen Negativfalls mit Bestandsbezug; der CSV-Fall bekommt einen Grader,
  der projekt-anlegen verlangt und code-erstellen in derselben Runde zulässt.
- **Ordner** `scripts/` + `templates/`, eigener Validator, UTF-8 ohne BOM, LF, `.projekt-anlegen.json` ohne Datum,
  begrenzter TOML-Renderer mit `tomllib`-Prüfung: übernommen.
- **Veröffentlichen:** `rename` ins nicht existierende Ziel auf demselben Dateisystem; vorher Zielordner exklusiv per
  `mkdir` als Platzhalter reservieren ist auf Windows mit `rename` nicht kombinierbar – ich teste beide Plattformen und
  dokumentiere die Grenze (nur kooperierende Instanzen geschützt) in `references/generator.md`.
- **Unterstützte Kombinationen** explizit im Manifest und nur, wenn in CI getestet: übernommen.
- Kein Widerspruch mehr. Serie aus meiner Sicht abschließbar.
