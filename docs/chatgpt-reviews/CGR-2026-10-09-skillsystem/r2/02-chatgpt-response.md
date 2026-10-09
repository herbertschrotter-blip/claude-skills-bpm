# Review Runde 2 – Antwort ChatGPT (23 s nachgedacht)

Technisches Review – Generator-Vertrag, Pilotimplementierung und Skill-Integration

## 1. Architekturentscheidung

Zustimmung zu Runde 1. Generator als versionierter, transaktionaler Scaffolding-Kern, über Stack-Manifeste erweitert:
„Der Generator kennt keine Python-, Home-Assistant- oder .NET-Sonderfälle. Er kennt ausschließlich validierte
Erzeugungsaufträge, Baustein-Abhängigkeiten, Dateien, Platzhalter und Prüfschritte.“ Die HA-Integration wird eine
Erweiterung des Bausteinkatalogs, keine Änderung der Generatorarchitektur.

Repo-Stand (main, INDEX.md, validate-skills.yml): Die Action prüft Skills, Python-Tests und Installationsskripte –
schnelle Qualitätsschranke, aber nicht alleiniger Ort für Generator-Integrationstests. Das Skill-Profil trennt
`Projekte.Ablage`, `Projekte.GitHub-Owner`, `Code.Stacks`, `Code.Tests`, `Code.Auslieferung`, `Doku.Entscheidungs-Ort`
– erhalten.

## 2. JSON-Erzeugungsauftrag v1

Kleines, streng validiertes JSON, kurzlebiger Ausführungsauftrag, keine zweite Projektkonfiguration.

    {
      "schema_version": 1,
      "project": {"name": "Beispiel Werkzeug", "slug": "beispiel-werkzeug", "package": "beispiel_werkzeug"},
      "template": {"id": "python-tool", "version": 1},
      "features": {"storage": "sqlite"},
      "delivery": {"github": false}
    }

| Feld | Pflicht | Herkunft |
|---|---|---|
| schema_version | Ja | Generator |
| project.name | Ja | Nutzer oder Claude aus Beschreibung |
| project.slug | Ja | Claude, deterministisch abgeleitet |
| project.package | Ja | Claude, deterministisch abgeleitet |
| template.id | Ja | Claude nach Stack-Reference |
| template.version | Ja | Manifest |
| features.storage | Ja | Nutzeranforderung, sonst none |
| delivery.github | Ja | Bestätigte Auswahl |

Erlaubt im Pilot: schema_version 1; template.id python-tool; template.version 1; features.storage none, sqlite;
delivery.github true, false. Zusätzliche Felder werden abgewiesen.

Nicht ins JSON: Ablage, GitHub-Owner, Branch-/Push-Policy, Check-Befehle – die liest der Skill aus dem Skill-Profil
bzw. sie kommen aus den Stack-Vorlagen. Zielordner als Kommandozeilenargument; das Skript prüft, ob er in der
freigegebenen Ablage liegt (das Markdown-Profil interpretiert der Skill, nicht das Skript).

Validierung: slug nur Kleinbuchstaben/Ziffern/Bindestriche, nicht am Rand; package gültiger Python-Modulname, kein
Schlüsselwort; keine Pfad-Traversal-Sequenzen; unbekannte Template-Versionen und ungültige Kombinationen vor jeder
Dateierzeugung abweisen; keine Shell-Befehle im Auftrag. Der Generator vertraut dem Auftrag nicht blind.

## 3. Bausteinarchitektur und Repo-Struktur

    skills/projekt-anlegen/
      SKILL.md
      references/ generator.md grundsatz.md github.md stacks/{python.md, home-assistant.md}
      generator/
        generate.py validate.py
        manifests/python-tool.json
        templates/{common/, python-tool/, storage-sqlite/, ci-github/}
        tests/{test_validation.py, test_generation.py, test_security.py}

Begründung: Das Plugin liefert den Skill mit; ein Zip kann den Generator ganz enthalten. Für claude.ai wird er nicht
ausgeführt; ein kleineres Zip nur mit SKILL.md und References ist möglich, sofern die Packaging-Regeln es vorsehen.

| Baustein | Wesentliche Dateien |
|---|---|
| common | README, CHANGELOG, CLAUDE.md, .gitignore, Entscheidungsdokument |
| python-tool | pyproject.toml, src/<package>/, CLI, Anwendungsschicht, Unit-Tests |
| storage-sqlite | SQLite-Adapter, Schema v1, Fixtures, Integrationstests |
| ci-github | .github/workflows/ci.yml (nur bei bestätigter GitHub-Nutzung) |

Manifest-Beispiel:

    {
      "id": "python-tool", "version": 1, "requires": ["common"], "conflicts": [],
      "features": {"storage": {"none": [], "sqlite": ["storage-sqlite"]}},
      "files": [
        {"source": "python-tool/pyproject.toml.tpl", "target": "pyproject.toml"},
        {"source": "python-tool/main.py.tpl", "target": "src/{{package}}/__main__.py"}
      ]
    }

Kompositionskern: Abhängigkeiten transitiv auflösen, Zyklen erkennen, Konflikte vorher prüfen, Dateikollisionen
erkennen statt überschreiben, Platzhalter vollständig auflösen, nur ins temporäre Projektverzeichnis schreiben.
Stolperstein: Brauchen zwei Bausteine dieselbe Datei (z. B. pyproject.toml), nicht Textfragmente mischen – gemeinsame
Konfigurationsdateien erzeugt ein einziger Renderer aus strukturierten, deklarativen Beiträgen der Bausteine. Sonst
wird der Generator zur selbstgebauten Template-Sprache.

## 4. Walking Skeleton Python-Werkzeug

Technischer Durchlauf: Statusfunktion liest einen technischen Statusdatensatz und gibt ihn über die CLI als JSON aus.
CLI → Application Service → Storage Protocol → SQLite Adapter → Tabelle system_status; ohne SQLite ein In-Memory-Adapter
mit demselben Vertrag.

    from dataclasses import dataclass
    from typing import Protocol

    @dataclass(frozen=True)
    class SystemStatus:
        state: str

    class StatusStore(Protocol):
        def read_status(self) -> SystemStatus: ...

    class StatusService:
        def __init__(self, store: StatusStore):
            self.store = store
        def execute(self) -> dict[str, str]:
            status = self.store.read_status()
            return {"status": status.state}

Starttest: `python -m beispiel_werkzeug status` → `{"status": "ready"}`. Tests: Exit-Code 0, gültiges JSON, Status
ready, SQLite-Variante liest wirklich aus der Datenbank, zweiter Start mit derselben DB funktioniert, fehlerhafte
Konfiguration → verständliche Meldung und Exit ≠ 0. Ein CLI-Test mit gemocktem Speicher genügt nicht; SQLite braucht
einen Integrationstest mit echter temporärer Datenbank.

Format und Lint mit Ruff: `python -m ruff format --check .`, `python -m ruff check .`, `python -m pytest -n auto`.
Ruff, pytest, pytest-xdist mit geprüften Versionen; nicht bei jedem Start aus PyPI abfragen, sondern ein zentraler,
regelmäßig aktualisierter Versionskatalog des Generators – reproduzierbar je Generator-Version.

## 5. Generatorprüfung und GitHub Actions

`validate-skills.yml` bleibt (Struktur, Description-Längen, References, Regeln, Python-Unit-Tests,
Installationsskripte); die schnellen Generator-Unit-Tests können dort mitlaufen. Neuer Workflow
`.github/workflows/test-project-generator.yml`: Generator-Unit-Tests, alle unterstützten Kombinationen ermitteln, je
Kombination erzeugen, Abhängigkeiten installieren, Format/Lint, Unit- und Integrationstests, Starttest, Sicherheits- und
Negativfälle.

| Projekt | Speicher | Erwartung |
|---|---|---|
| Python-Werkzeug | keiner | CLI, Tests, Lint, Start grün |
| Python-Werkzeug | SQLite | zusätzlich Schema v1 und Persistenztest grün |

GitHub-CI ist Auslieferungsoption, keine fachliche Kombination; das erzeugte Workflow-Dokument trotzdem prüfen.
Negativtests: Ziel existiert, unbekannter Baustein, fehlende Abhängigkeit, Zyklus, Konflikt, zwei Bausteine schreiben
dieselbe Datei, ungültiger Name, Pfad-Traversal, fehlender Platzhalter, Fehler beim Erzeugen, Fehler bei der
Projektprüfung. Ein Projekt mit roten Tests wird nicht als angelegt gemeldet.

Zwei Phasen: Prepare (Auftrag validieren → Bausteine auflösen → Dateien in Staging → Struktur prüfen); Verify & Publish
(Tests, Lint, Starttest → bei Erfolg Ziel übernehmen, bei Fehler Staging entfernen). Staging auf demselben Dateisystem
wie das Ziel (möglichst atomare Übernahme), vor dem Verschieben erneut prüfen, ob das Ziel existiert. GitHub-Repo und
Push sind externe Seiteneffekte – erst nach erfolgreicher lokaler Anlage im bestehenden GitHub-Ablauf.

## 6. Änderungen an projekt-anlegen

| Abschnitt | Inhalt |
|---|---|
| Zweck und Grenzen | Neues Projekt, Walking Skeleton, kein Fachcode |
| Benötigte Werte | Skill-Profil der aufrufenden Umgebung |
| Ablauf | Klären → Bestand → Plan → Erzeugen → Prüfen → Übergeben |
| Bestehendes Repo einrichten | Bestehenden Ablauf unverändert erhalten |
| Unterstützte Stacks | Direkte Links zu Stack-References |
| Generator | Verweis auf references/generator.md |
| Verboten | Sicherheits- und Datenverlustregeln |
| Verweise | Andere Skills und Regelquellen |

In References: Generatorvertrag und Ablauf → references/generator.md; Grundsatz-Prüfung → references/grundsatz.md;
Python → references/stacks/python.md; HA → references/stacks/home-assistant.md; GitHub → references/github.md.

Description-Vorschlag: „Legt neue Projekte an und richtet bestehende Repositories für die Skills ein. Klärt Zweck,
Zielumgebung und kleinste nützliche Fassung, prüft vorhandene Projekte und erzeugt für unterstützte Stacks ein
lauffähiges technisches Grundgerüst mit Konfiguration, Tests, Startprüfung und Skill-Profil. Verwendet geprüfte
Vorlagen und einen deterministischen Generator, ohne Fachlogik zu implementieren. Richtet bei bestehenden Repositories
ausschließlich Skill-Profil und Configs ein. Use when users want to start, create, scaffold, anlegen, aufsetzen or
einrichten a new project, tool, integration, card or repository, or prepare an existing repository for these skills.
Do not trigger for feature implementation or changes in existing projects (code-erstellen), UI mockups
(mockup-erstellen), skill creation or maintenance (skill-neu, skill-pflege), documentation-only tasks (doc-pflege), or
git-only operations (git-commit-helper).“

INDEX-Konfliktpaar projekt-anlegen ↔ code-erstellen: „Neues Projekt oder erstmalige Skill-Einrichtung eines
bestehenden Repos → projekt-anlegen. Ein neues Projekt erhält ausschließlich technische Startfähigkeit: lauffähige
Einstiegspunkte, Schichtenkopplung, Konfiguration, Tests und gegebenenfalls neutrale Persistenz. Fachliches Verhalten
und jede Erweiterung oder Änderung eines bestehenden Projekts → code-erstellen. Enthält ein Auftrag beides, legt
projekt-anlegen zuerst das technische Grundgerüst an und übergibt danach an code-erstellen.“

code-erstellen: kein zweiter Architekturvertrag. Neue Regel: „Bei Projekten mit `Doku.Entscheidungs-Ort` liest
code-erstellen die dort dokumentierten Grundentscheidungen vor der ersten fachlichen Erweiterung. Diese Entscheidungen
gelten als Projektkontext, nicht als unveränderliche Architektur. Änderungen werden nach den bestehenden
Dokumentationsregeln behandelt.“ Inhalt dort: Zweck, kleinste Fassung, Nicht-Ziele, Architektur, Datenhaltung,
Schema-Strategie, Konfiguration, Auslieferung, offene technische Entscheidungen.

## 7. HA-Integration als zweiter Stack

7.1 Keine feste Struktur wie `src/<package>/` im Generator; HA braucht `custom_components/<domain>/{__init__.py,
manifest.json, config_flow.py, const.py, coordinator.py}` und `tests/{conftest.py, test_config_flow.py,
test_setup.py}` – kommt aus dem HA-Manifest.
7.2 Manifest definiert deklarative Prüfungen (`"checks": ["format", "lint", "unit", "integration", "startup"]`); die
Befehle gehören zum Stack. Nie Befehle aus dem Auftrag übernehmen – nur geprüfte, im Katalog definierte Checks.
7.3 HA-Testumgebung: pytest-homeassistant-custom-component, HA-kompatible Versionen, Test-HA-Konfiguration, Tests für
Setup, Config-Flow, fehlende/ungültige Konfiguration; keine produktiven Geräte oder Zugangsdaten. HA-Version und
Testpaket gemeinsam pflegen. Der Test muss den echten Setup-Pfad ausführen, nicht nur Importe.
7.4 Beispielintegration: lokale Demo mit einem technischen Statussensor (`ready`), keine externe API, Config-Flow
akzeptiert leere Konfiguration; Setup-Test prüft, dass sie lädt und der Status verfügbar ist.
7.5 Eine HA-Integration nicht in die Schichten des Python-Werkzeugs zwingen – das Framework ist wiederverwendbar,
nicht jede Projektarchitektur.

## 8. Umsetzungsreihenfolge

1. Regel-Inventar und Refactor-Zweig. 2. Generatorvertrag und Validierung (Schema, Werte, Pfadprüfung, Negativtests;
noch keine Vorlagen). 3. Bausteinauflösung (Manifeste, Abhängigkeiten, Konflikte, Zyklen, Kollisionen). 4.
Python-Pilot (ohne Speicher, mit SQLite; Starttest, Checks). 5. Transaktionale Generierung (Staging, Verifikation,
Veröffentlichung, Rückbau). 6. Skill-Integration (projekt-anlegen, code-erstellen, References, Description, INDEX). 7.
Qualitätsabnahme (Generator-CI, Routing-Evals, Skill-Validierung, Praxistest). Danach HA-Integration.

## 9. Zusammenfassung

✅ Einigkeit: Hybridgenerator mit deterministischem Kern; JSON-Auftrag v1; Vorlagen und Generator unter
skills/projekt-anlegen/generator/; Standardbibliothek; Pilot Python-CLI mit optional SQLite; technischer
Statusdurchlauf; keine Fachlogik; erzeugte Projekte nie nachträglich ändern; HA-Integration als nächster Stack;
`pytest -n auto` bleibt (gemessen); Generator-Unit-Tests und Integrationstests getrennt; Skill-Profil bleibt Quelle der
Projektwerte.

⚠️ Widerspruch: (1) Gemeinsame Konfigurationsdateien nicht durch Text-Patches – ein strukturierter Renderer. (2) „Tests
grün“ reicht nicht – Starttest, bei HA echter Setup-Test. (3) Generator erstellt keine GitHub-Repos – lokal erzeugen
und prüfen; GitHub und Push im bestätigungspflichtigen Skill-Ablauf. (4) Python-Struktur nicht im Generator
festschreiben – aus dem Stack-Manifest.

❓ Rückfragen: (1) ci-github bei jedem neuen GitHub-Repo standardmäßig? Empfehlung ja, lokal entfällt er. (2) Kleine,
unveränderliche Herkunftsinformation (Generator-Version, Stack, Bausteine) im erzeugten Projekt? Empfehlung ja, keine
Updatefunktion. (3) Neue Abhängigkeitsversionen: manuelle Freigabe nach automatisierten Kompatibilitätstests. (4)
HA-Integration später mit optionalem SQLite: gemeinsamen Persistenzvertrag wiederverwenden, HA-Lebenszyklus und
Threading in eigenem Adapter.

Fazit: Der Python-Pilot kann auf dieser Grundlage implementiert werden; die vier offenen Punkte blockieren den Beginn
nicht.
