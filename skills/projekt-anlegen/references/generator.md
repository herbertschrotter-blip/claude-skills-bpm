# Generator

Erzeugt für unterstützte Projektarten ein lauffähiges, geprüftes Grundgerüst (Walking Skeleton): alle Schichten
verbunden, eine technische Beispiel-Funktion läuft durch, Formatierung, Lint, Tests und Start sind grün. Fachlogik
enthält es nicht.

## Inhalt

- Wer was macht
- Unterstützte Kombinationen
- Aufruf
- Erzeugungsauftrag
- Ablauf
- Ergebnis und Fehler
- Ohne ausführbare Umgebung
- Pflege der Vorlagen

## Wer was macht

- **Der Skill** stellt die Fragen, liest das Skill-Profil (Ablage, Owner, Geschützt), zeigt den Plan, baut den
  Erzeugungsauftrag, ergänzt danach Zweck und Grenzen in den Grundentscheidungen, macht Commit, GitHub und Push und
  übergibt.
- **Der Generator** (`scripts/generate.py`) bekommt nur den geprüften Auftrag und die Ablage. Er erzeugt Dateien
  lokal, prüft sie und stellt das Projekt an seinen Platz. Er fragt nichts, liest kein Profil, ruft kein Netz außer der
  Installation der Prüfwerkzeuge auf und fasst ein bestehendes Ziel oder ein früher erzeugtes Projekt nie an.
- Was ein Projekt enthält, steht in den Manifesten unter `templates/manifests/` (Projektart, Bausteine mit
  Voraussetzungen und Konflikten, Prüfschritte); der Generator selbst kennt keine Stack-Sonderfälle.

## Unterstützte Kombinationen

Nur was im Manifest freigegeben und in der CI des Generators geprüft ist:

| Projektart (`template.id`) | Version | `features` | Bausteine |
|---|---|---|---|
| `python-tool` – Python-Werkzeug mit Befehlszeile | 1 | `storage`: `none` | common, python-tool, storage-memory |
| `python-tool` | 1 | `storage`: `sqlite` | common, python-tool, storage-sqlite |
| `ha-integration` – eigene Home-Assistant-Integration | 1 | `quelle`: `aufsatz` | common, ha-integration, quelle-aufsatz |
| `ha-integration` | 1 | `quelle`: `abruf` | common, ha-integration, quelle-abruf |

Bei `delivery.github: true` kommt `ci-github-python` bzw. `ci-github-ha` dazu (automatische Prüfung bei jedem
Push). Alles andere geht den Weg nach der Stack-Reference; nie eine Kombination improvisieren.

Bei `ha-integration` entscheidet die Quelle: `aufsatz`, wenn die Integration die Entitäten einer vorhandenen
Integration nutzt (das Gerät ist schon in Home Assistant); `abruf`, wenn sie selbst ein Gerät oder einen Dienst
abfragt. `package` ist zugleich die Domain und darf nicht wie eine vorhandene Integration heißen. Die Tests gegen
Home Assistant brauchen `uv` und Python 3.14 und laufen nur unter Linux; unter Windows meldet der Generator sie als
übersprungen. Läuft die Sitzung unter Windows, zuerst per Auswahlfrage: auf dem HA-Rechner anlegen (empfohlen) / über
das Netzlaufwerk anlegen (`references/windows-netzlaufwerk.md`) / abbrechen.

## Aufruf

```
python3 <skill>/scripts/generate.py --auftrag <datei.json> --ablage <Projekte.Ablage>
```

`<skill>` ist der Ordner dieses Skills; den Auftrag schreibt Claude in den Scratchpad, nie ins Projekt. Unter Windows
heißt der Interpreter je nach Installation `python`. Die Prüfung installiert die Werkzeuge in eine eigene Umgebung im
Zwischenordner; das braucht Netz und auf einem Raspberry Pi etwa eine halbe Minute (HA-Integration: knapp eine
Minute).

## Erzeugungsauftrag

```json
{
  "schema_version": 1,
  "project": {"name": "Stromzähler Übersicht", "slug": "stromzaehler", "package": "stromzaehler"},
  "template": {"id": "python-tool", "version": 1},
  "features": {"storage": "sqlite"},
  "delivery": {"github": true}
}
```

(Beispielwerte.) Streng geprüft, zusätzliche Felder sind ein Fehler:
- `name`: Anzeigename, höchstens 80 Zeichen, Umlaute erlaubt, keine `/ \ .. {{ }} ` ` $( "`.
- `slug`: Ordnername, Kleinbuchstaben, Ziffern, einzelne Bindestriche, höchstens 40 Zeichen.
- `package`: Python-Name, Kleinbuchstaben, Ziffern, `_`, höchstens 40 Zeichen, kein Schlüsselwort und kein Modul der
  Standardbibliothek. Claude leitet `slug` und `package` aus dem Namen ab (`Stromzähler` → `stromzaehler`).
- `template`, `features`: aus der Tabelle oben; die Wahl leitet Claude aus den Grundentscheidungen ab.
- `delivery.github`: die bestätigte Auswahl.

Ablage, GitHub-Owner, Branch- und Push-Policy und Prüfbefehle stehen nie im Auftrag.

## Ablauf

1. Auftrag prüfen, Ziel `<Ablage>/<slug>` darf nicht existieren und muss in der Ablage liegen.
2. Bausteine auflösen und zweimal in einen Zwischenordner der Ablage erzeugen (gleiches Dateisystem).
3. Eine Fassung prüfen: Umgebung einrichten, Formatierung, Lint, Tests (parallel), Start.
4. Nur bei Grün die saubere Fassung (ohne Umgebung und Caches) an ihren Platz verschieben. Der Zwischenordner
   verschwindet in jedem Fall.

Gleicher Auftrag ergibt gleiche Dateien. Im Projekt liegt `.projekt-anlegen.json` mit Generator-Version, Projektart und
Bausteinen – nur Herkunft, keine Konfiguration und keine Update-Funktion.

Grenze: Zwischen der letzten Prüfung, ob das Ziel frei ist, und dem Verschieben schützt nichts vor einem fremden
Prozess, der denselben Ordner anlegt. Für einen Nutzer an einer Ablage genügt das.

## Ergebnis und Fehler

Ausgabe ist JSON: `ok`, `phase` (auftrag, erzeugen, pruefen, veroeffentlichen, fertig), `ziel`, `dateien`,
`pruefungen` (je Schritt `name`, `dauer`, `ok`, bei Fehler `ausgabe` mit den letzten Zeilen, bei einem Schritt nur
für eine andere Plattform `uebersprungen`) und `fehler`. Übersprungene Schritte stehen in der Tabelle als
„übersprungen“, mit Grund, und in der Zusammenfassung als eigener Satz (z. B. „Die HA-Tests sind nicht gelaufen“).

- `ok: true` → Tabelle Prüfung / Dauer / Ergebnis zeigen, weiter mit Grundentscheidungen, Commit, GitHub, Eintrag.
- `ok: false` → es wurde nichts angelegt. Phase, Schritt und Ursache in einem Satz nennen; bei `auftrag` den Auftrag
  korrigieren, bei `pruefen` mit Werkzeugen oder Netz liegt die Ursache meist in der Umgebung (Ausgabe lesen, nicht
  raten). Nie den Generator mit abgeschalteter Prüfung wiederholen, um ein Projekt trotzdem anzulegen.

## Ohne ausführbare Umgebung

Wo keine Shell da ist (claude.ai im Browser oder in der App), entsteht nur der Plan mit Grundentscheidungen und
Auftrag. Erzeugt wird später in Claude Code. Nie Dateien aus dem Gedächtnis nachbauen und nie eine Erzeugung
behaupten.

## Pflege der Vorlagen

- Vorlagen liegen unter `templates/<baustein>/`, UTF-8 ohne BOM, Zeilenenden LF, Platzhalter nur aus der festen Liste
  (`{{name}}`, `{{slug}}`, `{{package}}`, `{{package_upper}}`, `{{github}}`, `{{v_<paket>}}`) und den Features der
  Projektarten (`{{storage}}`, `{{quelle}}`). Zeilen mit `{{package}}` oder `{{name}}` so schreiben, dass Ruff sie
  bei jeder erlaubten Länge gleich formatiert; `scripts/validate.py --erzeugen` prüft das nicht für jede Länge.
- Prüfschritte stehen im Manifest der Projektart; ein Schritt mit `plattform` (z. B. `["linux"]`) läuft nur dort.
- Versionen der Werkzeuge stehen nur in `templates/versions.json`; neue Versionen erst nach grüner CI des Generators
  übernehmen.
- Vor jedem Commit: `python3 scripts/validate.py` (Katalog) und die Tests unter `scripts/tests/`; jede Kombination echt
  prüft `scripts/validate.py --erzeugen <ordner>` bzw. der Workflow `test-project-generator.yml` auf Linux und Windows.
- Eine neue Projektart oder Kombination gilt erst als unterstützt, wenn sie im Manifest freigegeben, in der Tabelle
  oben eingetragen und in der CI grün ist.
