# Runde 3 – Einschätzung von Claude

Stand: 29.09.2026, Claude Code auf dem Home Assistant.

## Kurzfassung

ChatGPT übernimmt alle sieben Korrekturen, sechs unverändert, eine präzisiert (`translation_key`). Die offenen Fragen aus
Runde 2 (Listen in der eigenen Oberfläche, ein Speicherort) sind beantwortet. Es gibt keine blockierende Rückfrage mehr;
das Modell ist geschlossen genug für die Grundsatzdoku und den Skill `modul-bauplan`. Ich stimme zu und empfehle, die Serie
abzuschließen.

## Zustimmung

- **Eigentümer statt Schreibweg (G-01):** „ein fachlicher Eigentümer je Wert“ mit Validierung beim Eigentümer ist die
  tragende Regel. Mehrere Bedienwege (Karte, Automation, Sprache) sind dann kein Widerspruch.
- **Schnittstelle ist kein Speicherort:** Entity, Action und WebSocket sind Zugänge; Store, Config Entry, Recorder und
  Modul-DB sind Speicher. Diese Trennung wird die Gliederung der Doku bestimmen.
- **Action oder WebSocket:** „Automatisierbarer Befehl → Action; Bearbeiten und komplexes Lesen in der eigenen Oberfläche →
  WebSocket; beides endet beim selben Eigentümer.“ Einfach genug für Herbert und eindeutig für Claude.
- **`null` erbt, `[]` ist bewusst leer:** wichtig für Planabweichungen; gehört als Beispiel in die Doku.
- **Personenauswahl dynamisch aus `person.*`,** gespeichert als Referenz, fehlende Person nicht still löschen, sondern als
  Reparatur-Hinweis melden.
- **`translation_key` als unsere Konvention,** nicht als HA-Garantie. Die Doku kennzeichnet das ausdrücklich als
  Hausregel.
- **Ein bevorzugter Bedienort je Einstellung** statt eines technischen Verbots.
- **Reihenfolge der Planung (Abschnitt 10):** Problem → Werte → Eigentümer → was HA schon hat → was übrig bleibt →
  Darstellung. Das wird der Ablauf im Modus „Planen“ von `modul-bauplan`.
- **Offene Punkte (Abschnitt 11)** gehören in die Bestandsanalyse des Roboter-Neubaus, nicht in die Grundsatzregeln –
  besonders Raum ↔ HA-Bereich nicht 1:1 annehmen.

## Anmerkungen

1. **Ausfallverhalten fehlt als Regel.** Was ein Modul tut, wenn eine Quelle `unavailable` ist oder eine Entität fehlt,
   steht nur als offener Punkt für den Roboter. Das betrifft aber jedes Modul (Haus ohne Personen, Planer ohne Roboter).
   Vorschlag **G-21 Ausfall:** „Ein Modul erkennt fehlende oder nicht verfügbare Quellen, trifft dann keine Entscheidung auf
   veralteten Daten, zeigt den Grund an (Entität bzw. Reparatur-Hinweis) und erholt sich ohne Neustart.“ Prüfbar durch einen
   Test mit abgeschalteter Quelle, gilt ab Stufe 2.
2. **Neustart bei Python-Code (G-16) und Arbeit direkt auf dem HA.** Jede Code-Änderung an einer Integration braucht einen
   Neustart, und den löst nur Herbert aus (Regel in `/config/CLAUDE.md`). Folge für den Ablauf: Änderungen sammeln, Tests
   vorher auf dem Pi, dann ein Neustart je Lieferung. Gehört in den Abschnitt „Einspielen“ der Doku bzw. `BETRIEB.md`,
   nicht in die Regel selbst.
3. **G-18 enger fassen:** „private Daten“ ausdrücklich um Koordinaten, Gerätekennungen und Personennamen ergänzen – so steht
   es schon im Rahmen der Serie.
4. **Sprache der Doku:** Die Endfassung von ChatGPT nutzt englische HA-Begriffe (Options Flow, Store, Config Entity,
   Repairs). Für Herbert braucht die Doku deutsche Begriffe mit dem HA-Fachwort in Klammern beim ersten Auftreten, und ein
   kurzes Glossar.
5. **Beispiel-`module.yaml`:** `id: planer` ist ein Arbeitsname. Der Name der Roboter-Integration wird laut E-138 erst beim
   Neubau festgelegt; im Doku-Beispiel als Platzhalter kennzeichnen.
6. **Review-Config veraltet:** Der Pflicht-Block „Rahmen“ in `.claude/skill-config/review.md` nennt noch „Entwicklung auf
   Windows 11 … Samba-Laufwerk“. Seit E-141 wird direkt auf dem HA gearbeitet; beim Abschluss nachziehen.

## Vorschlag zum Abschluss

- Serie ohne Runde 4 abschließen; G-21 als Entscheidung von Herbert aufnehmen (oder ChatGPT kurz fragen).
- Ergebnis-Ort `docs/ha-grundsatz/` wird im nächsten Schritt (Grundsatzdoku) aus Runden 1–3 geschrieben.
- Die offenen Punkte aus Abschnitt 11 als Prüfliste in DX-111 (Bestandsanalyse) übernehmen, nicht als 24 einzelne Aufgaben.
