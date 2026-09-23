# Review Runde 2 – Einstellungsmodell konkret, Regeln Version 2, kurzer Weg

Canvas-Titel: **„Review Runde 2“**. Schreibe deine gesamte Antwort in den Canvas und schließe mit
✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen.

## Repo-Zugriff
Du hast Zugriff auf zwei GitHub-Repos und kannst selbst Dateien lesen:
- **Skill-Repo:** `herbertschrotter-blip/claude-skills-bpm` – **Branch `main`** (Runde 1 vollständig unter
  `docs/chatgpt-reviews/CGR-2026-09-23-ha-grundsatz/r1/`: deine Antwort, meine Einschätzung, Herberts Entscheidungen)
- **Referenzfall Heidi:** `herbertschrotter-blip/HA_Dash_DreameX60` – **Branch `main`**
- Nutze das aktiv, um Aussagen zu verifizieren, Querverweise zu prüfen und Originaldateien zu lesen, wenn der Kontext im
  Prompt nicht reicht.
- Bei JEDEM Dateizugriff den Branch `main` angeben.

## Stand nach Runde 1

**Einig und entschieden (Herbert):**
- Eigenes Modul mit Logik ab Stufe 2 = **eigene Integration**; der Heidi-Neubau entsteht direkt als `custom_components/heidi`
  (Helfer-Integration über der Dreame-Integration).
- Heidi spricht **nur über die Dreame-Integration**, nie direkt mit der Dreame-Cloud.
- Das **Haus-Modul** wird ein eigenes Repo und eine eigene Integration **`haus`** (nur die mittlere Ebene „Haus-Schluss“:
  jemand da, Ruhezeit, Arbeitszeit); Geräte-Regeln bleiben bei den Geräten.
- **`module.yaml` ist Pflicht ab Stufe 2**, klein gehalten (Vertrag + Eigentumsregister); für Stufe 0–1 freiwillig.
- Übernommen: native HA-Fähigkeit vor Adapter; Module sprechen nur über öffentliche HA-Schnittstellen (Entitäten, Aktionen,
  Ereignisse, WebSocket); Vertrag vor Mockup; Diagnose, Reparatur-Hinweise und Backup-Haken; nichts Privates unter `/local`;
  Schattenbetrieb, Ereignis-Wiedergabe und Architektur-Drift-Tests.

**Meine Korrekturen und Ergänzungen zu deiner Runde 1** (bitte kurz: einverstanden oder nicht, mit Grund):
1. `command_line` fragt laut offizieller Doku standardmäßig alle **60 s** ab (nicht 30 s); `command_timeout` 15 s.
2. Die Dreame-Integration (Tasshack) unterstützt `vacuum.clean_area` **nicht** (Wunsch #1498 geschlossen, keine Umsetzung
   sichtbar), und `clean_area` kennt keine Werte je Raum (Saugstufe, Wasser, Wiederholungen). Der Dreame-Adapter bleibt also,
   gebaut zum Umschalten auf `clean_area`, sobald die Integration es kann.
3. Die Heidi-Integration veröffentlicht den Zustand des Roboters **nicht** noch einmal (sonst zwei Wahrheiten). Die Karte liest
   den Roboter über die Standard-Entität `vacuum.*` und die Standard-Aktionen, dazu die Heidi-Entitäten; nur Dreame-Eigenheiten
   (Werte je Raum, CleanGenius, Karte) laufen über den Adapter.
4. Da Entitäts-IDs nicht der Vertrag sind, **findet die Karte ihre Entitäten über das Entitäts-Register** (Integration +
   `translation_key`) und das Gerät – nicht durch Zusammensetzen von IDs.
5. **Kurzer Weg für Stufe 0–1** (z. B. Poolsensor, einfache Automationen): Auftrag → Bestand → Vertrag → Bau → Abnahme;
   der volle Ablauf mit zehn Phasen erst ab Stufe 2.
6. **Weniger Dokumente je Modul:** ein Modul-Steckbrief (eine Datei mit festen Abschnitten) plus `module.yaml`, statt fünf
   Einzeldokumenten.
7. **Entwicklungsumgebung als Grundsatz:** Rechenmodule (`domain/`) und Karte unter Windows testen; Integrationstests unter
   WSL (einmalig einrichten); bis dahin die Integrationsschicht dünn halten.
8. **Einspielen:** Code-Änderung an einer Integration = HA-Neustart, geplant, wenn kein Gerät läuft; Änderung von Optionen =
   Neuladen des Eintrags.

## Offene Frage von Herbert: das Einstellungsmodell („ein Eigentümer je Datum“)

Herbert möchte deine Empfehlung erst konkret sehen, bevor er entscheidet. Bitte spiele sie an Heidis echten Einstellungen durch
(Quellen: `docs/DATEN.md` 4.2 und 5.3, `docs/HAUSREGELN.md` 4.3, `docs/BACKEND.md` 5, `ha/packages/heidi.yaml`,
`ha/prognose/planer.py` `AUTOMATIK_STANDARD`/`normalisiere_automatik`):

- Automatik: an/aus, Mindest-Akku (10–80 % in 5er-Schritten, E-127), Schwelle „wenig Zeit“, Schnellprogramm (an/aus, Saugstufe,
  Wiederholungen), Leise-Profil, Reaktion bei Anwesenheit (warten/leise/trotzdem), gewählte Personen, Arbeitszeit (Tage, von–bis),
  bei Heimkehr (Station/pausieren/weiter), Fortsetzen nach Pause (Minuten), übliche Rückkehr.
- **Je Plan** kann dieselbe Automatik eigen gesetzt werden („übernimmt die globale oder hat eine eigene, gleich aufgebaute“, E-135).
- Prognose: Personen, Intervall, Auflösung, Lernwochen, Halbwertszeit, Mindesttage.
- Anzeige: Dunkelmodus, Kartendarstellung, Raumnamen (Original/Deutsch).
- Lernen: „Lernen ab“ (Neustart des Lernens).

Bitte liefere:
1. **Eine Tabelle:** Einstellung → Ort (Einrichtungsdialog / Optionsdialog / Einstellungs-Entität / Fachdaten in der Datenbank /
   Haus-Modul / gar nicht mehr nötig) → Begründung. Mit Entitäts-Art und Beispiel-`translation_key`.
2. **Eigene Automatik je Plan:** Wie modelliert man sie, ohne dass derselbe Wert doppelt entsteht? (Mein Vorschlag: Der globale
   Wert ist eine Einstellungs-Entität; die Abweichung eines Plans gehört zum Plan-Objekt in der Datenbank und speichert nur, was
   abweicht. Stimmt das mit der HA-Praxis überein?)
3. **Speichern und Prüfen** von Einstellungs-Entitäten in einer eigenen Integration (`RestoreEntity` oder `Store`, min/max/step),
   wie eine eigene Karte sie ändert (Standard-Aktionen wie `number.set_value` oder eigene Aktionen) und wie die Karte Bereiche
   und Optionen ohne feste Werte anzeigt.
4. **Die Nachteile ehrlich:** viele Entitäten (bei Heidi rund 30), Übersetzungsaufwand, Aufzeichnung im Recorder, Unordnung in
   der Geräteansicht – und wie man sie klein hält (z. B. `entity_registry_enabled_default`, Optionsdialog für Seltenes).
5. **Haus-Modul:** Wo liegen seine Einstellungen (z. B. gewählte Personen, Ruhezeiten, Arbeitszeit), wie wählt ein Geräte-Modul
   „welche Personen zählen für mich“, ohne Personen fest einzutragen?

## Dazu für den Leitfaden
6. **Grundsatzregeln Version 2:** deine Liste G-01 … G-16 mit den Korrekturen oben eingearbeitet (knapp, je Regel ein Satz
   „Regel“ und ein Satz „prüfbar durch“).
7. **Kurzer Weg (Stufe 0–1) und voller Weg (ab Stufe 2):** Phasen mit Ergebnis je Phase, so knapp, dass ein Einsteiger sie
   versteht.
8. **Vorlage Modul-Steckbrief** (Abschnitte) und **`module.yaml` Schema v1** (klein, mit Eigentumsregister), gefüllt am Beispiel
   Heidi (nur die wichtigsten Einträge).

Bitte kompakt bleiben: Tabellen und Stichpunkte, Code nur für das Schema.
