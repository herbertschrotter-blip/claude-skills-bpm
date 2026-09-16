# Stack: python — Python-Skripte neben HA (Prognose, Laufprotokoll) und allgemein

Stack-Referenz für `code-erstellen`. Wird geladen, wenn das Code-Profil des Projekts
`Stacks: python` enthält. Projektspezifisches (Pfade, Aufruf über `shell_command`, Datenorte)
steht im Code-Profil, nicht hier.

---

## Schichten und Kopplungsregeln

- Reine Funktionen für Fachlogik (parsen, schätzen, aufteilen); I/O (Dateien, HA-API) in
  dünnen Wrappern am Rand.
- Wenn dieselbe Fachlogik auch in einem anderen Stack existiert (z.B. TypeScript-Karte),
  gelten **gemeinsame Vektoren** (JSON) als Vertrag: beide Seiten testen gegen dieselben Dateien.
- Skripte, die HA aufruft (`shell_command`, `command_line`), geben JSON aus und schreiben
  nur in die dafür vorgesehenen Dateien; Laufprotokolle werden nie gelöscht.
- Keine Abhängigkeiten außer Standardbibliothek, wenn das Skript auf dem HA-Host läuft.

## Modus-Eskalation (Beispiele)

| Standard | Deep |
|----------|------|
| neue Funktion, neues Attribut in der JSON-Ausgabe | neues Ausgabeformat (Vertrag mit Sensor/Karte) |
| Parameter aus HA-Helfern lesen | neuer Datenfluss (neue Datei, neue Quelle) |
| Randfall in bestehender Logik | Verhalten, das die Karte anders rechnet (Vektoren ändern) |

## Impact-Check-Zeilen (Stack-Lesart)

- Fachlogik / gemeinsame Vektoren betroffen?
- JSON-Ausgabe (Attribute, die Sensor oder Karte lesen)
- Datenorte / Laufprotokoll
- Aufruf aus HA (`shell_command`, Rechte, Python-Version auf dem Host)
- Datenschutz (Anwesenheitsdaten, GPS)

## Blocking: was zuerst

| Betroffen | Zuerst |
|-----------|--------|
| Ausgabeformat | Sensor-Definition im HA-Paket + Vertrag |
| gemeinsame Logik | Vektor-Dateien + Gegenstück im anderen Stack |

## Tests

- `pytest` in `<pfad>/tests/`, Testdaten = die gemeinsamen Vektor-JSONs; Abweichungen zum
  anderen Stack als `xfail` mit Begründung, nicht stillschweigend anpassen
- Befehl aus dem Profil (z.B. `python -m pytest tests/`); wenn auf dem PC kein Python ist:
  auf dem Host ausführen oder als Aufgabe für den User markieren – nicht ungetestet committen
- Exit-Code 0 vor Commit

## Typische Fehler

- Fachlogik „neu erfinden“ statt portieren (Vektoren brechen)
- Ausgabe-Attribut umbenannt, Sensor/Karte nicht nachgezogen
- Datei mit personenbezogenen Daten ins Repo
- Rundungs-/Zeitzonenunterschiede zwischen Python und TypeScript nicht in Vektoren festgehalten
