# Stack Home Assistant

Arten, Orte und Grunddateien für neue Home-Assistant-Projekte. Die fachlichen Grundsatzregeln (Schichten, Entitäten,
Ausbaustufen) kommen aus `Modul.Grundsatzregeln` im Skill-Profil; im Skill-Repo liegen sie unter `docs/ha-grundsatz/`.
Pfade sind relativ zum Konfigurationsordner von Home Assistant (`/config`).

## Inhalt

- Zuerst: gibt es das schon?
- Arten und Orte
- Grunddateien je Art
- Geschützte Bereiche
- .gitignore für den Konfigurationsordner
- Neu laden oder neu starten
- Stolperfallen

## Zuerst: gibt es das schon?

Vor jedem eigenen Projekt kurz prüfen, ob eine eingebaute Integration, ein Helfer oder eine verbreitete HACS-Lösung den
Zweck schon erfüllt. Ist das so, dem Nutzer das als erste Option der Auswahlfrage anbieten: Einrichten ist dann kein
Projekt, sondern eine Installation.

## Arten und Orte

Reihenfolge von einfach nach aufwendig. Die einfachste Art, die den Zweck erfüllt, gewinnt.

| Art | Wofür | Ort | Eigenes Repo |
|---|---|---|---|
| Paket | Automationen, Skripte, Template-Sensoren und Helfer zu einem Thema | `packages/<thema>.yaml` | nein |
| Blueprint | dieselbe Automation mehrfach mit anderen Geräten | `blueprints/automation/<name>.yaml` | nein |
| YAML-Dashboard | eine eigene Seite aus vorhandenen Karten | `dashboards/<name>.yaml` | nein |
| Python-Werkzeug | Rechnen oder Auswerten außerhalb von HA, aufgerufen über `shell_command` | `<name>/` mit Modulen und `tests/` | nein, außer es wächst |
| Eigene Karte | Anzeige, die keine vorhandene Karte kann | Repo in der Ablage, ausgeliefert nach `www/<name>.js` | ja |
| Eigene Integration | neue Geräte oder Dienste, Entitäten mit eigener Logik | Repo in der Ablage, ausgeliefert nach `custom_components/<domain>/` | ja |

Beispiel (Projekt): Fensterüberwachung mit Reedkontakten → Paket `packages/fenster.yaml` mit Gruppe, Template-Sensor
„Fenster offen“ und Automation; bei Bedarf dazu ein YAML-Dashboard. Keine Integration nötig.

Faustregeln aus den HA-Vorgaben (Details in `docs/ha-grundsatz/`):
- Verhalten gehört in Automationen und Skripte, abgeleitete Werte in Template-Entitäten, Geräte- und Dienstlogik in
  eine Integration.
- Ein Dashboard zeigt nur an. Aktionen gehen über Dienste zurück.
- Fachlogik eines Python-Werkzeugs frei von HA-Code halten; so bleibt sie testbar und später in eine Integration
  übertragbar.

## Grunddateien je Art

- **Paket:** eine YAML-Datei mit Kommentarkopf (Zweck, beteiligte Entitäten). Voraussetzung ist ein Eintrag
  `homeassistant: packages: !include_dir_named packages` in `configuration.yaml`; fehlt er, gehört das zur
  Registrierung mit eigener Rückfrage.
- **Blueprint:** YAML mit `blueprint:`-Kopf (`name`, `domain`, `input`).
- **YAML-Dashboard:** `dashboards/<name>.yaml` mit einer Ansicht und einer Platzhalterkarte. Registrierung unter
  `lovelace: dashboards:` in `configuration.yaml` (Schlüssel mit Bindestrich, `mode: yaml`, `title`, `icon`,
  `show_in_sidebar`, `filename`).
- **Python-Werkzeug:** Ordner mit Einstiegsmodul, `tests/` und kurzer README; Aufruf über `shell_command` im Paket
  des Themas.
- **Eigene Karte** (Repo): Quellcode mit Build (Lit üblich), `README.md`, `CHANGELOG.md`, `hacs.json` (Pflichtfeld
  `name`), `.gitignore` für Node. Die gebaute Datei wird nach `www/<name>.js` ausgeliefert und unter den
  Dashboard-Ressourcen als `/local/<name>.js` eingetragen.
- **Eigene Integration** (Repo): `custom_components/<domain>/` mit `__init__.py`, `manifest.json` (`domain`, `name`,
  `version`, `documentation`, `codeowners`, `iot_class`, `config_flow`, `requirements`), `const.py`,
  `translations/de.json` und `en.json`; dazu `hacs.json`, `README.md`, `CHANGELOG.md`, `tests/`. Vorlage ist das
  verbreitete `integration_blueprint`. Ausgeliefert wird der Ordner nach `custom_components/<domain>/`.

## Geschützte Bereiche

Typische Werte für `Projekte.Geschützt`, wenn die Sitzung im Konfigurationsordner läuft:
- `custom_components/**` außer den selbst ausgelieferten Integrationen – verwaltet HACS, Änderungen gehen beim Update
  verloren
- `www/community/**` – verwaltet HACS
- `.storage/**` – interner Zustand von HA, enthält Zugangsdaten
- `automations.yaml`, `scripts.yaml`, `scenes.yaml` – schreibt der Editor der Oberfläche; neue Themen kommen in Pakete

Nicht geschützt, aber nur mit eigener Rückfrage: `configuration.yaml` (Registrierung von Paketen und Dashboards) und
`secrets.yaml` (Claude trägt dort nur Platzhalter-Schlüssel ein, die Werte setzt der Nutzer).

## .gitignore für den Konfigurationsordner

Wird der Konfigurationsordner selbst ein Git-Repo, gehören diese Einträge in seine `.gitignore`:

```gitignore
secrets.yaml
.storage/
.cloud/
deps/
tts/
backups/
*.db
*.db-shm
*.db-wal
*.log
*.log.*
*.fault
.HA_VERSION
.ha_run.lock
__pycache__/
*.bak
www/community/
custom_components/
```

Eigene Datenbanken und Daten von Python-Werkzeugen (`*.db`, Messdaten) bleiben ebenfalls draußen. Wer selbst
ausgelieferte Integrationen im Repo des Konfigurationsordners führen will, nimmt sie mit `!custom_components/<domain>/`
wieder auf; die Quelle der Wahrheit bleibt trotzdem ihr eigenes Repo.

## Neu laden oder neu starten

| Änderung | Wirksam durch |
|---|---|
| Automation, Skript, Szene, Template-Entität im Paket | Entwicklerwerkzeuge → YAML → passende Konfiguration neu laden |
| neues Paket oder neuer Eintrag in `configuration.yaml` | Konfiguration prüfen, dann Neustart |
| YAML-Dashboard | Seite im Browser neu laden; neues Dashboard braucht einen Neustart |
| Karte unter `www/` | Browser neu laden, notfalls Cache leeren; der Ordner `www/` selbst braucht beim ersten Anlegen einen Neustart |
| Integration | immer Neustart |

Vor jedem Neustart die Konfiguration prüfen (`ha core check` in der Shell der App oder Entwicklerwerkzeuge → YAML →
Konfiguration prüfen). Den Neustart löst der Nutzer aus oder bestätigt ihn ausdrücklich.

## Stolperfallen

- Alles unter `www/` ist über `/local/` ohne Anmeldung abrufbar. Keine Zugangsdaten und keine privaten Daten dort.
- `shell_command` wird nach 60 Sekunden hart beendet.
- Die alte Schreibweise `platform: template` ist entfernt; Template-Entitäten unter `template:` anlegen.
- Karten nutzen keine eingebauten `ha-*`-Bausteine, Farben kommen aus dem Theme mit Ersatzwert.
- Tests für Integrationen (`pytest-homeassistant-custom-component`) laufen nicht direkt unter Windows.
