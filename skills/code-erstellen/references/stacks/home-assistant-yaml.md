# Stack: home-assistant-yaml — Home Assistant Pakete, Automationen, Skripte, Dashboards

Stack-Referenz für `code-erstellen`. Wird geladen, wenn das Code-Profil des Projekts
`Stacks: home-assistant-yaml` enthält. Projektspezifisches (Host, Laufwerk, Deploy-Skript,
Token-Variable) steht im Code-Profil bzw. der CLAUDE.md, nicht hier.

---

## Schichten und Kopplungsregeln

- **Quelle der Wahrheit** ist das Repo (`ha/`), nie der Config-Ordner auf dem Host. Änderung im
  Repo → deployen → prüfen.
- **Pakete** (`packages/*.yaml`): Helfer (`input_*`), Template-Sensoren, `command_line`,
  `shell_command`. Ein Paket je Thema; neue Helfer-Domäne braucht Neustart.
- **Automationen/Skripte** (`automations.yaml`, `scripts.yaml`): Fachlogik dort, Entscheidungs-
  werte aus Sensor-Attributen lesen, nicht doppelt rechnen.
- **Dashboards** (`dashboards/*.yaml`, `configuration.yaml`): Views `type: panel`, Ressourcen
  über die Lovelace-Ressourcen-API mit `?v=` versionieren.
- **Vertrag:** Jede Entität, die eine Karte liest oder schreibt, steht in der Vertrags-Doku des
  Projekts. Umbenennung = Breaking Change für die Karte.
- Entitäts-IDs mit Umlaut: HA macht ö→o, ü→u (`_storen`, nicht `_stoeren`); echte ID vor dem
  Referenzieren per API prüfen.
- Nie ins Repo: `.storage/`, `secrets.yaml`, Datenbanken, Laufprotokolle, Abzüge mit Tokens/GPS.

## Modus-Eskalation (Beispiele)

| Standard | Deep |
|----------|------|
| neue Bedingung/Aktion in bestehender Automation | neue Helfer-Domäne (Neustart), neues Paket |
| neues Attribut an bestehendem Template-Sensor | neue Entität, die die Karte liest/schreibt (Vertrag) |
| neuer `shell_command`/`command_line` | Integration/HACS betroffen, Kartenbild/Datenkarte |
| Dashboard-View ändern | configuration.yaml, Ressourcen, Personen/Zonen |

## Impact-Check-Zeilen (Stack-Lesart)

- Paket / Helfer (neue Domäne? Neustart nötig?)
- Automationen / Skripte (Trigger, Bedingungen, Trace prüfbar?)
- Vertrag: liest/schreibt eine Karte diese Entität?
- Dashboard / Ressource / Version
- Integration (HACS, Beta-Stand, Entitätsnamen der Integration)
- Datenschutz: Token, GPS, Abzüge

## Blocking: was zuerst

| Betroffen | Zuerst |
|-----------|--------|
| neue Entität für die Karte | Vertrags-Doku + `contract.ts` des Karten-Stacks |
| Entität mit unbekannter ID | `ha.ps1 get states/<id>` (echte ID) |
| Automation | bestehenden Trace / Ist-Verhalten lesen |

## Prüfen und Ausliefern (Befehle aus dem Profil)

1. Kopieren mit dem Deploy-Skript des Projekts (UTF-8 ohne BOM)
2. `config/core/check_config` über die REST-API → muss `valid` sein
3. Ohne Neustart: `automation/reload`, `template/reload`, `shell_command/reload`,
   `command_line/reload`, `input_*/reload`; Neustart nur für neue Helfer-Domänen oder
   `configuration.yaml`
4. Ergebnis prüfen: `states/<entity>` (Zustand, Attribute), Automations-Trace, Dashboard Strg+F5

## Tests

- Kein Unit-Framework; Prüfung = `check_config` + Zustände/Attribute nach Reload + Trace
- Karten-E2E gegen Fixtures (`states-*.json`) müssen nach Entitätsänderungen erneuert werden
  (Dump-Skript, dann Fixture-Prüfung gegen den Vertrag)

## Typische Fehler

- Direkt auf dem Host editieren statt im Repo
- Template mit `states.x` ohne `| default` → `unavailable` bricht Automation
- Reload statt Neustart bei neuer Helfer-Domäne
- Ressourcen-`?v=` nicht erhöht → Browser zeigt alte Karte
- Token oder Anmeldedaten in Datei/Commit/Chat
