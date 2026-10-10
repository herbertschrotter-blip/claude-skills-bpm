# Grundsatz-Prüfung

Was ein erfahrener Entwickler vor der ersten Zeile Code klärt – so, dass ein Nutzer ohne Programmierkenntnisse es
beantworten kann. Nicht alles wird gefragt: Die meisten Punkte sind Standards, die der Generator fest einbaut, oder
technische Folgen, die Claude ableitet.

## Inhalt

- Drei Ebenen
- Pflichtklärungen und Fragen
- Grundentscheidungen im neuen Projekt

## Drei Ebenen

| Ebene | Inhalt | Wer |
|---|---|---|
| Standards | Grundstruktur (Fachlogik getrennt von Oberfläche und Datenzugriff), Tests, Formatierung und Lint, Einstellungen aus der Umgebung, Geheimnisse nie im Repo, Fehlerbehandlung und Protokoll, Schema-Version bei Datenhaltung | Generator bzw. Stack-Reference, ohne Frage |
| Produktentscheidungen | Zweck, Ort, erste Fassung, Datenlebensdauer, Anbindung an Vorhandenes, Veröffentlichung | Auswahlfragen |
| Dokumentiert | Architektur, Datenhaltung und Schema-Strategie, Sicherheitsannahmen, Auslieferung und Rückweg, Grenzen, offene Punkte | Grundentscheidungen des neuen Projekts |

## Pflichtklärungen und Fragen

Pflicht, wenn der Auftrag es nicht schon sagt:
- **Was soll es tun?** – Was soll am Ende passieren oder sichtbar sein?
- **Wo soll es laufen?** – Aus dem Kontext ableiten, sonst fragen.
- **Was soll die erste Fassung können?** – Die kleinste nützliche Funktion und was ausdrücklich noch nicht. Nennt
  der Auftrag viele Funktionen: Auswahlfrage, welche zuerst kommt; die übrigen werden Ausbaustufen.

Nur bei Bedarf, jeweils als Auswahlfrage mit Vorschlägen:
- Woher kommen die Daten (Gerät, Dienst, vorhandene Entitäten, Datei)? – nur, wenn mehrere Wege sinnvoll sind.
- Wer bedient es, und wo wird es angezeigt? – daraus folgt die Oberfläche.
- Muss es rechnen oder lernen, oder reicht Anzeigen und Schalten?
- **Soll es Informationen dauerhaft speichern?** Nein, nur während es läuft / ja, auf diesem Gerät / ja, mehrere Geräte
  nutzen dieselben Daten / weiß nicht – bitte vorschlagen. Daraus leitet Claude die Datenhaltung ab (z. B. „ja, auf
  diesem Gerät“ → SQLite) und erzeugt nur die benötigte; nie nach Datenbankprodukten fragen.
- Nutzen es auch andere? – nur bei Veröffentlichung; daraus folgen Sichtbarkeit und Lizenz.

Technik wird nicht abgefragt, sondern im Plan in Alltagssprache erklärt. Bei Daten gilt: Schema-Version ab Tag 1, kein
Umbau-Werkzeug auf Vorrat; ohne produktive Daten darf eine Datenbank später neu angelegt werden, mit produktiven
Daten braucht jede Schemaänderung eine ausdrückliche Entscheidung.

## Grundentscheidungen im neuen Projekt

Die Antworten landen am `Doku.Entscheidungs-Ort` des neuen Projekts (beim Generator wie auf dem Weg nach der
Stack-Reference `docs/entscheidungen.md`):
- Zweck, erste Fassung, ausdrücklich nicht
- Technik: Datenhaltung, Anbindung, Oberfläche, Auslieferung und Rückweg
- Offene Entscheidungen

Die README verweist nur darauf. code-erstellen liest die Grundentscheidungen vor der ersten fachlichen Erweiterung; sie
sind Projektkontext, keine unveränderliche Architektur.
