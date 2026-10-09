# Review Runde 3 – Antwort ChatGPT (25 s nachgedacht)

Abschlussreview vor der Implementierung – Description, Routing, Verteilung und Plattformdetails

## 1. Description

Einwand berechtigt: der Entwurf aus Runde 2 berücksichtigte Klonen und deutsche Umgangssprache zu wenig; der
Gegenentwurf (1018 Zeichen) nutzt fast die ganze Länge. Gekürzte Fassung:

> Legt neue Projekte an und richtet bestehende Repos für die Skills ein. Klärt Zweck, Ort und erste Fassung, prüft den
> Bestand und erzeugt für unterstützte Stacks ein lauffähiges, getestetes Grundgerüst ohne Fachlogik. Erstellt oder
> klont nach Rückfrage GitHub-Repos und richtet das Skill-Profil ein. Use when users want to start, scaffold, anlegen,
> aufsetzen or einrichten a new project, HA integration, card, dashboard or Python tool, say "neues Projekt" or "ich
> will X bauen, weiß aber nicht wie", want a GitHub repo created or cloned, or an existing repo eingerichtet for these
> skills (Skill-Profil, Configs). Do not trigger for changes in existing projects (code-erstellen), UI mockups
> (mockup-erstellen), new or changed skills (skill-neu, skill-pflege), ClickUp tasks (tracker), documentation only
> (doc-pflege), or git-only operations.

Zeichenzahl maschinell messen (nachgemessen von Claude: 839).

| Inhalt | Entscheidung | Begründung |
|---|---|---|
| „trägt in die Übersicht ein“ | Streichen | interner Ablauf |
| konkrete Grunddateien | Streichen | gehören in SKILL.md |
| ausführliche Stack-Beispiele | Kürzen | HA und Python reichen |
| GitHub erstellen/klonen | Behalten | bestehende Routing-Fälle |
| „neues Projekt“ | Behalten | zentraler deutscher Auslöser |
| „weiß aber nicht wie“ | Behalten | unklare Projektidee |
| bestehendes Repo einrichten | Behalten | eigener Anwendungsfall |
| Negativabgrenzungen | Behalten | verhindern Konflikte |

## 2. Routing-Evals: 17 Fälle

Positiv: `projekt-anlegen-new-simple` „neues Projekt: Bewässerungssteuerung“; `projekt-anlegen-python-repo` „mach mir
ein Repo für ein kleines Python-Tool, das CSVs zusammenführt“ (darf auslösen, obwohl eine Fachfunktion genannt ist –
erst Gerüst, dann code-erstellen; im Grader berücksichtigen); `projekt-anlegen-ha-card` „ich will eine eigene Karte für
meinen Pool bauen“; `projekt-anlegen-ha-integration-en` „set up a new Home Assistant integration for my heat pump“;
`projekt-anlegen-python-sqlite` „leg ein Python-Werkzeug mit Datenbank an, das meine Stromzähler speichert“.

Negativ: `projekt-anlegen-no-clickup` „leg in ClickUp ein neues Projekt an“ (tracker); `projekt-anlegen-no-readme`
„schreib die README für das neue Projekt“ (doc-pflege); `projekt-anlegen-no-session` „öffne mein Projekt ha-baustelle“
(sitzung); `projekt-anlegen-no-commit` „commit und push das neue Repo“ (git-commit-helper);
`projekt-anlegen-no-feature` – stärker mit Bestandsbezug: „In meiner bestehenden Integration fehlt noch die Berechnung
der Baustellenstunden. Bau die ein.“ (code-erstellen).

Die sieben vorhandenen `prompt.md` unverändert lassen und nach der Description-Änderung erneut laufen lassen.
Abnahme: kritische Fälle 3/3, normale ≥ 2/3, kein bisher bestandener Negativfall kippt.

## 3. Ordnerstruktur

Claudes Vorschlag übernehmen (passt zu `skills/sitzung/scripts/`):

    skills/projekt-anlegen/
      SKILL.md
      references/ generator.md grundsatz.md stacks/{python.md, home-assistant.md}
      scripts/ generate.py validate.py tests/{test_generate.py, test_manifest.py, test_security.py}
      templates/ versions.json manifests/{python-tool.json, components/} common/ python-tool/ storage-sqlite/ ci-github/

`references/` beschreibt das Verhalten, `scripts/` implementiert den Generator, `templates/` enthält die Bausteine.

Lieferung claude.ai: nur SKILL.md + references/. Regel in delivery.md präzisieren: „Ausführbare Skripte und
Projektvorlagen, die ausschließlich für Claude Code vorgesehen sind, werden nicht in das claude.ai-Upload-ZIP
aufgenommen. Die References beschreiben in claude.ai den Planungsablauf ohne Ausführung. Ein nicht ausführbarer
Generator darf nicht als erfolgreich ausgeführt dargestellt werden.“ Der Skill darf bei claude.ai fehlende Vorlagen
nicht improvisiert ersetzen.

## 4. Prüfung von Templates

`validate-skills.ps1` bleibt für die Skill-Qualitätsregeln; `scripts/validate.py` prüft den Katalog: Manifeste gültig,
referenzierte Templates vorhanden, keine unbekannten Platzhalter, keine unaufgelösten nach Generierung, kein
Pfad-Traversal, keine doppelten Zieldateien, keine nicht unterstützten Kombinationen, keine Projektwerte, keine
Zugangsdaten, einheitliche Kodierung. UTF-8 ohne BOM statt ASCII-Pflicht. Projektneutralität: verbotene Muster
mechanisch prüfen, Platzhalter-Allowlist, Review neuer Templates über skill-pflege; keine absoluten Pfade,
Benutzerkonten, Repo-Namen in Vorlagen.

## 5. Herkunftsdatei

`.projekt-anlegen.json` ohne Datum (Git kennt den Zeitpunkt, Zeitstempel stört die Reproduzierbarkeit):

    {"schema_version": 1, "generator": {"name": "projekt-anlegen", "version": "1.0.0"},
     "template": {"id": "python-tool", "version": 1}, "components": ["common", "python-tool", "storage-sqlite"]}

Nur Herkunft, keine Konfiguration, kein Update-Mechanismus. Test: identischer Auftrag → identische Datei.

## 6. TOML-Renderer

Korrektur zu Runde 2: kein allgemeiner Renderer. Eine zentrale `pyproject.toml`-Vorlage mit definierten optionalen
Abschnitten; Bausteine liefern strukturierte Werte (Abhängigkeiten aus `versions.json`); der Renderer schreibt nur
bekannte Felder in fester Reihenfolge mit korrektem String-Escaping und validiert danach mit `tomllib.load`. Keine
Vorlage je Kombination (wächst mit HA, PostgreSQL). Kein allgemeiner TOML-Writer; bei beliebigen Strukturen eine
Bibliothek bewerten.

## 7. Plattformen

| Thema | Empfehlung |
|---|---|
| Pfade | pathlib.Path |
| Zeilenenden | einheitlich LF |
| Kodierung | UTF-8 ohne BOM |
| Platzhalter | streng validierte Namen, keine Ausdrücke |
| Shell | keine Befehle aus Eingaben |
| Prozesse | subprocess.run([...], shell=False) |
| Temporäre Dateien | Staging unter dem Ziel-Elternverzeichnis |
| Überschreiben | vorhandene Ziele abweisen |
| Symlinks | keine aus Templates übernehmen |
| Berechtigungen | keine Unix-Modi unter Windows annehmen |

`os.replace()` ist kein universeller atomarer Verzeichnis-Publish; `staging.rename(target)` bei gleichem Dateisystem,
nicht existierendem Ziel, abgeschlossenen Prüfungen, auf der Zielplattform getestet. `exists()` vor `rename()` ist
keine exklusive Reservierung; atomare Zielreservierung oder getestete No-Replace-Strategie; ein Lock schützt nur
kooperierende Instanzen – dokumentieren. Unterprozesse mit `sys.executable`, Projektchecks mit dem Interpreter der
virtuellen Umgebung. Abnahme auch auf Windows und Linux, nicht nur Ubuntu-CI.

## 8. Vor dem Bau festlegen

Kein Architekturblocker. In `references/generator.md` ausdrücklich: Grenze Generator (validierter Auftrag → lokale
Dateien) vs. Orchestrator/Skill (Fragen, Profil, GitHub, Commit, Push, Übergabe). Unterstützte Kombinationen explizit
deklarieren; eine Kombination gilt erst als unterstützt, wenn sie im Manifest freigegeben und in CI getestet ist.

## 9. Abschluss

✅ Einigkeit: Description gekürzt ohne Verlust deutscher Auslöser und Klonen; 7 + 10 Routing-Fälle; `scripts/` und
`templates/`; claude.ai nur SKILL.md und References; Generator nur in Claude Code; `.projekt-anlegen.json`; begrenzter
TOML-Renderer mit `tomllib`-Prüfung; Python 3.12 Linux und Windows; Generierung und Veröffentlichung getrennt;
bestehende Projekte nie überschreiben oder aktualisieren.

⚠️ Widerspruch: Description aus Runde 2 war zu stark gekürzt (Einwand berechtigt); keine ASCII-Pflicht, UTF-8 ohne BOM;
kein allgemeiner TOML-Renderer; `rename()` allein ist keine plattformübergreifende Transaktion; eigener Validator statt
Ausbau des Skill-Prüfskripts.

❓ Rückfragen: keine blockierenden. Vor Freigabe Zeichenzahl maschinell messen und die sieben vorhandenen Prompts gegen
die neue Description laufen lassen. Serie abschließbar.
