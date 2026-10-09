# Review Runde 1 – Antwort ChatGPT (30 s nachgedacht)

Technisches Review – `projekt-anlegen` als Walking-Skeleton-Generator

## 1. Gesamturteil

Empfehlung Variante C – hybrider, deterministischer Generator mit geprüften Vorlagen und begrenzter KI-Ergänzung:
„Alles, was wiederholbar, sicherheitsrelevant oder automatisiert testbar ist, wird deterministisch erzeugt. Claude
entscheidet über die passende Architektur und ergänzt nur dort Code, wo feste Vorlagen nicht sinnvoll ausreichen.“
Der Generator erzeugt aus wenigen verständlichen Entscheidungen einen geprüften Projektstart. Die Regel „lauffähige
Minimalfassung, keine Fachlogik“ ist richtig; es fehlt die Definition von „lauffähig“.

Befund Repo (main): Fall „bestehendes Repo einrichten“ darf nicht in den Generatorpfad geraten; Architektur- und
Testlogik von code-erstellen nicht duplizieren; `docs/skill-profile-v1.md` hat Checks, Stacks, Auslieferung,
Entscheidungsorte – ein Generator-Standard darf diese Werte nicht nochmals speichern. Kein Neuentwurf nötig.

## 2. Bauweise

| Kriterium | A: Vorlagen + Skript | B: Claude nach Rezept | C: Hybrid |
|---|---|---|---|
| Wiederholbarkeit | Sehr hoch | Niedrig | Hoch |
| Automatische Tests | Sehr gut | Aufwendig | Sehr gut |
| Neue Stacks | Hoher Vorlagenaufwand | Flexibel | Kontrollierbar |
| Wartung | Steigt mit Varianten | Schwankende Qualität | Gut begrenzbar |
| Claude-Code-Eignung | Sehr gut | Sehr gut | Sehr gut |
| claude.ai ohne Shell | Eingeschränkt | Möglich | Mit Einschränkung |
| Empfehlung | Für stabile Stacks | Nicht als Standard | Bevorzugt |

A kippt durch die Zahl abhängiger Optionen (8 binäre → 256). Statt Vorlagen je Kombination: Komposition kleiner,
geprüfter Bausteine mit Voraussetzungen und Konflikten:

    generator/
      generate.py
      validate.py
      templates/ common/ python-cli/ python-service/ persistence-sqlite/ persistence-postgresql/ ci-github/
      manifests/ python-cli.json python-service.json

Eingabe z. B. `{"stack": "python-cli", "storage": "sqlite", "interface": "cli", "target": "desktop"}`; Generator prüft
erst, ob die Kombination unterstützt wird. Templates nur generisch; Projektwerte aus Antworten bzw. Skill-Profil.

Eigenes Skript (Standardbibliothek) statt copier/cookiecutter für den Anfang, bewusst begrenzt: JSON-Eingabe mit
Schema, deklarative Auswahl, einfache Platzhalter, keine Template-Sprache, keine stillen Überschreibungen, Ausgabe in
ein temporäres Verzeichnis, eindeutige Fehler. Copier neu bewerten bei Vererbung, bedingten Dateibäumen, Updates
erzeugter Projekte.

Versionen: drei Ebenen – Generator-Version, Stack-Kompatibilität (Python/HA/.NET), Abhängigkeitsversionen;
Kompatibilitätsmatrix je Stack, CI prüft regelmäßig. Werkzeuge/Tests reproduzierbar anheften, Laufzeit-Abhängigkeiten
von Bibliotheken nicht zwingend exakt. Generator aktualisiert nie bereits erzeugte Projekte; spätere Updates gehören zu
code-erstellen.

## 3. Grenze projekt-anlegen ↔ code-erstellen

„projekt-anlegen erzeugt technische Funktionsfähigkeit. code-erstellen implementiert fachliches Verhalten.“
Zulässig: startfähige Anwendung, minimale UI/CLI, Konfiguration, Logging/Fehlerbehandlung, Persistenzanbindung mit
Beispieldaten, technischer Durchlauf durch die Schichten, Tests, Build/Lint/CI. Nicht zulässig: fachliche Berechnungen,
reale Geschäftsprozesse, projektbezogene Datenmodelle, produktive externe Schreiboperationen, spezifische
Benutzerabläufe, Berechtigungslogik, fachliche Import-/Exportregeln.

Prüfbare Regel: „projekt-anlegen darf ausführbaren Anwendungscode erzeugen, soweit dieser ausschließlich den
technischen Start, die Schichtenkopplung und deren automatisierte Prüfung ermöglicht. Die Beispiel-Funktion verwendet
neutrale Testdaten und besitzt keine fachliche Bedeutung. Jede Funktion, deren erwartetes Ergebnis aus den
Anforderungen des konkreten Produkts abgeleitet werden muss, gehört zu code-erstellen.“

| Anfrage | Zuständigkeit |
|---|---|
| „Erstelle ein neues Python-Werkzeug“ | projekt-anlegen |
| „Erstelle eine neue HA-Integration mit SQLite-Grundgerüst“ | projekt-anlegen |
| „Die Integration soll Baustellenstunden berechnen“ | code-erstellen, nach Projektanlage |
| „Ergänze eine Exportfunktion“ | code-erstellen |
| „Richte mein bestehendes Repo für Skills ein“ | projekt-anlegen |
| „Erweitere die vorhandene Datenbank“ | code-erstellen |

Kein eigener Generator-Skill: zusätzliche Routing-Grenze ohne Nutzen; Generator ist interne Komponente
(Bedarf klären → Bestand prüfen → Architektur wählen → Generator ausführen → Ergebnis prüfen → übergeben).

## 4. Fragenkatalog

Zu viele technische Fragen. Drei Pflichtklärungen: Was soll das Projekt machen? Wo soll es laufen (aus Kontext, sonst
fragen)? Was soll die erste Version können (kleinste nützliche Funktion, Grenzen)? Weitere nur bei Bedarf:
Datenhaltung (nur ob Daten dauerhaft bleiben), Oberfläche (aus Bedienung ableiten), Datenquelle (nur bei mehreren
Möglichkeiten), Nutzung durch andere (nur bei Veröffentlichung), GitHub-Sichtbarkeit (beim Repo-Schritt).
Beispiel statt „SQLite oder PostgreSQL?“: „Soll das Programm Informationen dauerhaft speichern? A nein · B ja, auf
diesem Gerät · C ja, mehrere Geräte nutzen dieselben Daten · D weiß nicht – bitte vorschlagen“.
Fehlende Frage: bestehendes System anbinden oder ganz neu? – in die vorhandene Bestandsprüfung integrieren.
Korrektur: Zielumgebung legt die Projektart nicht fest (Dienst, Integration, Paket auf demselben Gerät); zuerst die
einfachste geeignete Art, dann die technischen Optionen.

## 5. Grundsatz-Prüfung

Als interne Prüfliste richtig, als Gespräch zu umfangreich. Drei Ebenen:

| Ebene | Inhalt | Verantwortung |
|---|---|---|
| Automatische Standards | Struktur, Tests, Logging, Konfiguration, Lint, Fehlerbehandlung, Geheimnisse | Generator |
| Echte Produktentscheidungen | Zweck, Datenlebensdauer, Anbindung, Zielumgebung, Veröffentlichung | Auswahlfragen |
| Dokumentierte Entscheidungen | Architektur, Datenmodell, Schema-Strategie, Sicherheitsannahmen, Auslieferung, Grenzen | Projektdoku |

Ergänzungen: Wiederholbarkeit (gleiche Eingabe + Version → gleicher Stand); Fehlerfall und Rückbau (erst temporär
erzeugen und prüfen, dann übernehmen; nie halbes Projekt); Betriebsfähigkeit (stackabhängiger Start- bzw.
Integrationstest, pytest allein reicht nicht). Entscheidungen in eine Datei unter docs/, Pfad über
`Doku.Entscheidungs-Ort` im Skill-Profil; README nur Einstieg mit Verweis.

## 6. Datenhaltung

Nicht sofort ein Migrationsframework, aber von Anfang an eine Strategie für Schemaänderungen.

    src/<package>/application/ domain/ infrastructure/persistence/{protocol.py, sqlite_store.py,
    postgres_store.py (nur falls gewählt), schema.py}
    tests/unit/ tests/integration/

Gemeinsame Schnittstelle nur, wenn beide Datenbanken wirklich gebraucht werden; Standard lokal SQLite; PostgreSQL bei
zentralem Mehrbenutzerzugriff, vorhandener Infrastruktur, paralleler Schreiblast. Gleiche Schnittstelle ≠ gleiche
Semantik (Transaktionen, Typen, Sperren, Dialekte).

Schema-Version von Anfang an (`schema_meta` mit `version`). Frühphase: ohne produktive Daten neu erstellen; mit
produktiven Daten ausdrückliche Migrationsentscheidung; keine automatische Löschung. Einstiegspunkt für spätere
Migrationen erzeugen.

Test-Isolation – Fehler im bisherigen Ansatz: Datenbankname aus `worker_id` isoliert Worker, nicht Tests desselben
Workers, und parallele CI-Läufe mit gleichen Worker-Namen können kollidieren. SQLite: `tmp_path` je Test. PostgreSQL:
eindeutige Kennung je Lauf und Worker (ggf. je Test), Fixtures legen an und räumen zuverlässig ab. Invariante: Kein
Test beeinflusst einen anderen, unabhängig von Worker-Zahl, Reihenfolge, Wiederholung. `-n auto` auf kleinen Maschinen
prüfen (Speicher, Startkosten); Obergrenze in die Stack-Reference, nicht in den Skill.

## 7. Stack-Reihenfolge und Abnahme

| Phase | Stack | Ziel |
|---|---|---|
| 1 | Python CLI ohne Datenbank | Generator, Tests, Lint, Startfähigkeit |
| 2 | Python CLI mit SQLite | Persistenz, Schema-Version, Test-Isolation |
| 3 | Python-Dienst | Lebenszyklus, Konfiguration, Fehlerbehandlung |
| 4 | Python mit PostgreSQL | Datenbankadapter, Integrationstests |
| 5 | HA-Integration | HA-Lebenszyklus, Manifest, Konfiguration |
| 6 | TypeScript/Lit-Karte | Frontend-Build, Test, Auslieferung |
| 7 | C#/.NET/WPF | Desktop-Architektur und Tests |

Abnahme in fünf Ebenen: (1) Generator-Vertrag – gültige Eingaben erzeugen ein Projekt, ungültige verständliche Fehler,
nichts wird überschrieben; (2) Projektqualität – Build, Lint, Unit-Tests, Starttest je Projekttyp; (3)
Kombinationsprüfung – jede unterstützte Kombination erzeugt und geprüft, nicht unterstützte vorher abgewiesen; (4)
Routing-Eval – kritische Fälle 3/3, übrige ≥ 2/3, kein Negativfall kippt; (5) Praxistest – Idee, wenige Fragen,
startbares Projekt mit grünen Checks und verständlicher Übergabe. Leitfrage: Lässt sich das Projekt starten, prüfen und
mit code-erstellen erweitern?

## 8. Verteilung Plugin und claude.ai

Claude Code: voller Generator mit Skript, Checks, Anlage. claude.ai: Skill und References bleiben nutzbar; ohne
Ausführungsumgebung Architektur und Projektplan, keine behauptete Generierung. Keine zwei Generator-Implementierungen.
Volle Generierung in claude.ai wäre ein eigenes Abnahmekriterium. Description (1020) neu und kürzer formulieren;
SKILL.md < 500 Zeilen; Stack-Abläufe in references/stacks; Inhaltsverzeichnis ab 100 Zeilen; keine
Querschnittsregeln kopieren; Regel-Inventar für den Refactor.

## 9. Nächster Schritt

Pilot Python-Werkzeug mit optionaler SQLite-Datenhaltung: Eingabeschema, geprüfte CLI-Vorlage, SQLite-Baustein, Tests,
Lint, Startprüfung, Skill-Profil und Grundentscheidungen generieren, Routing-Evals und Praxistest. Weitere Stacks erst
nach Pilotabnahme.

## 10. Zusammenfassung

✅ Einigkeit: Walking Skeleton richtig; Projektanlage und Fachimplementierung getrennt; Projektwerte aus Skill-Profil
und bestätigten Eingaben; getestete Vorlagen statt improvisiertem Code; Generator berücksichtigt Tests, Konfiguration,
Datenisolation, Auslieferung; stackweiser Ausbau mit Abnahme; projekt-anlegen bleibt Einstieg.

⚠️ Widerspruch: C mit deterministischem Kern statt A; weniger Fragen, Technik automatisch vorschlagen; nur die
benötigte Datenbank erzeugen; Schema-Strategie ja, Migrationsframework nicht immer; `-n auto` auf dem Pi prüfen;
gleiche Ausführung in Claude Code und claude.ai nicht nachgewiesen.

❓ Rückfragen: (1) „Lauffähig“ bei HA-Integration – isolierter Kern mit Manifest und Config-Flow oder in HA geladen
und eingerichtet (Empfehlung: Letzteres, mit automatisiertem HA-Integrationstest)? (2) Auch Projekte ohne eigenes
Repo (HA-Paket im Konfigurations-Repo) – ja, aber getrennt vom Generator für eigenständige Anwendungen? (3) Wie
verbindlich ist volle Ausführung in claude.ai? (4) Generator-Vertrag als JSON-Datei akzeptabel (kurzlebiger,
validierter Erzeugungsauftrag, kein Ersatz für das Skill-Profil)?

Vorschlag Runde 2: diese vier Entscheidungen klären, dann Pilotvertrag, Template-Komposition und die Änderungen an
projekt-anlegen, code-erstellen und INDEX.md festlegen.
