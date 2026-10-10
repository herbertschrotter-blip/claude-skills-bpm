# Grundentscheidungen – {{name}}

Was beim Anlegen entschieden wurde. Die Skills lesen das vor der ersten fachlichen Erweiterung (Skill-Profil →
Doku → Entscheidungs-Ort). Es ist Projektkontext, keine unveränderliche Architektur: Ändert sich etwas, wird es hier
nachgetragen.

## Zweck und Grenzen

- Zweck: (beim Anlegen ergänzt)
- Erste Fassung: (beim Anlegen ergänzt)
- Ausdrücklich nicht: (beim Anlegen ergänzt)

## Technik

- Art: eigene Integration als Aufsatz (`quelle: {{quelle}}`). Sie spricht nicht selbst mit einem Gerät, sondern
  nutzt die Entität einer vorhandenen Integration, die im Einrichtungsdialog gewählt wird, und reagiert auf deren
  Änderungen. Ihre Entitäten hängen am Gerät dieser Entität.
- Fehlt die Quelle oder ist sie nicht verfügbar, zeigt der Status „Quelle fehlt“; gerechnet wird dann nicht.
- Fachlogik ohne Home Assistant in `custom_components/{{package}}/logik/`, mit eigenen Tests.
- Verlauf über die Aufzeichnung von Home Assistant; keine eigene Datenbank.
- GitHub mit automatischer Prüfung: `{{github}}`. Geheimnisse nie im Repo.
- Auslieferung: Ordner nach `custom_components/` der HA-Konfiguration kopieren, dann Neustart durch den Nutzer.

## Offene Entscheidungen

- (keine)
