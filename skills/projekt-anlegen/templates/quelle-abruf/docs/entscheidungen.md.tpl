# Grundentscheidungen – {{name}}

Was beim Anlegen entschieden wurde. Die Skills lesen das vor der ersten fachlichen Erweiterung (Skill-Profil →
Doku → Entscheidungs-Ort). Es ist Projektkontext, keine unveränderliche Architektur: Ändert sich etwas, wird es hier
nachgetragen.

## Zweck und Grenzen

- Zweck: (beim Anlegen ergänzt)
- Erste Fassung: (beim Anlegen ergänzt)
- Ausdrücklich nicht: (beim Anlegen ergänzt)

## Technik

- Art: eigene Integration mit Abruf (`quelle: {{quelle}}`). Sie fragt ein Gerät oder einen Dienst selbst ab, über
  einen gemeinsamen Abruf für alle Entitäten (Coordinator). Die Verbindung in
  `custom_components/{{package}}/api.py` ist ein Beispiel ohne Netz und wird durch die echte Bibliothek ersetzt.
- Ist das Gerät nicht erreichbar, scheitert die Einrichtung mit einer Meldung bzw. die Entitäten werden „nicht
  verfügbar“; Home Assistant versucht es selbst wieder.
- Fachlogik ohne Home Assistant in `custom_components/{{package}}/logik/`, mit eigenen Tests.
- Verlauf über die Aufzeichnung von Home Assistant; keine eigene Datenbank.
- GitHub mit automatischer Prüfung: `{{github}}`. Geheimnisse nie im Repo; Zugangsdaten nur im Einrichtungsdialog.
- Auslieferung: Ordner nach `custom_components/` der HA-Konfiguration kopieren, dann Neustart durch den Nutzer.

## Offene Entscheidungen

- Welche Bibliothek spricht mit dem Gerät oder Dienst?
