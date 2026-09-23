# Runde 1 – Einschätzung von Claude (23.09.2026)

ChatGPT hat gründlich gearbeitet; die drei Hauptkorrekturen überzeugen mich. Zwei Aussagen habe ich nachgeprüft (Quellen unten).

## Übernehmen (Einigkeit)

1. **„Ein Eigentümer je Datum“ statt „eine Datenbank für alles“.** Die Motivation von E-128 (keine doppelten Wahrheiten) bleibt,
   die Lösung wird HA-typisch: Einstellungen als Einstellungs-Entitäten (`number`/`select`/`switch`/`time`, `EntityCategory.CONFIG`),
   Optionsdialog oder Einrichtungsdialog; Entitätsverlauf im Recorder; kleiner interner Zustand im `Store`; die eigene SQLite-
   Datenbank nur für Fachdaten (Pläne, Läufe, Lernwerte, Aufträge, Diagnose-Ereignisse); große Daten über WebSocket.
2. **Heidi-Neubau direkt als eigene Integration** (`custom_components/heidi`) – eine „Helfer“-Integration über der
   Dreame-Integration. Die reinen Rechenmodule wandern unverändert in `domain/`; Shell-, base64- und JSON-Brücken entfallen.
3. **Native HA-Fähigkeit zuerst, Adapter nur für Lücken.** Belegt: HA 2026.3 hat `vacuum.clean_area` eingeführt (Segmente →
   HA-Bereiche, Reparatur-Hinweis bei geänderter Karte), zunächst für Matter, Ecovacs und Roborock.
4. **Haus-Modul in drei Ebenen:** Fakten (Personen, Kalender, Zeitpläne) → Haus-Schluss (jemand da, Ruhezeit, Arbeitszeit) →
   Geräte-Regel (Heidi, Mäher, Lüftung entscheiden selbst). Das Haus-Modul besitzt nur die mittlere Ebene.
5. **Module sprechen nur über öffentliche HA-Schnittstellen:** Entitäten, Aktionen, Ereignisse, WebSocket – nie fremde
   Datenbanken, Dateien oder Python-Importe.
6. **Skill-Ablauf:** Vertrag vor Mockup; Phasen 0–10 mit Ergebnis je Phase; „Prüfen“ gegen nummerierte Regeln mit Schwere;
   „Nachschlagen“ kurz mit Regel und Quelle.
7. **Diagnose, Reparatur-Hinweise und Backup-Haken** für größere Integrationen; keine privaten Daten unter `/local`.
8. **Die fünf Ideen**, besonders Architektur-Drift-Tests (haben wir mit `geheimnisse.test.ts` schon im Kleinen), Schattenbetrieb
   (hat Heidi schon) und der maschinenlesbare Modulvertrag.

## Korrekturen und Ergänzungen von meiner Seite

1. **`command_line` fragt standardmäßig alle 60 s ab, nicht 30 s** – so steht es in der offiziellen Doku; der Brief war richtig.
   Am Urteil ändert das nichts.
2. **Dreame kann `vacuum.clean_area` (noch) nicht:** Der Wunsch dazu (Tasshack/dreame-vacuum #1498, März 2026) ist geschlossen,
   eine Umsetzung ist nicht zu sehen. Außerdem kennt `clean_area` keine Werte je Raum (Saugstufe, Wasser, Wiederholungen). Heidi
   braucht den Dreame-Adapter also weiter – er soll so gebaut sein, dass Raumreinigung auf `clean_area` umschaltet, sobald die
   Integration es kann.
3. **„Die Karte versteht Heidi, nicht Dreame“ – mit Grenze:** Die Heidi-Integration darf den Zustand des Roboters nicht noch
   einmal veröffentlichen (sonst zwei Wahrheiten). Die Karte liest den Roboter über die Standard-Entität `vacuum.*` und die
   Standard-Aktionen, dazu die Heidi-Entitäten für Ergebnisse und Einstellungen; nur Dreame-Eigenheiten (Werte je Raum,
   CleanGenius, Karte) gehen über den Adapter der Integration.
4. **Entitäten finden statt IDs zusammensetzen:** Wenn IDs nicht der Vertrag sind, sucht die Karte ihre Entitäten über das
   Entitäts-Register (Integration + `translation_key`) und das Gerät. Das gehört als Regel in den Frontend-Teil.
5. **Der Ablauf muss mit der Ausbaustufe wachsen:** Für Stufe 0–1 (Poolsensor, einfache Automationen) sind zehn Phasen mit fünf
   Dokumenten zu viel. Vorschlag: ein kurzer Weg (Auftrag → Bestand → Vertrag → Bau → Abnahme) und der volle Weg ab Stufe 2.
6. **Weniger Dokumente je Modul:** statt `problem.md`, `bestand.md`, `datenvertrag.md`, `contract.md` und `module.yaml` ein
   **Modul-Steckbrief** (eine Markdown-Datei mit festen Abschnitten) plus `module.yaml` (Vertrag und Eigentumsregister in einem).
7. **Namen:** Das Haus-Modul heißt `haus`, nicht `hausregeln` – „Hausregeln“ war im Heidi-Konzept die Heidi-Seite (Geräte-Regel).
8. **Entwicklungsumgebung als eigener Grundsatz:** Rechenmodule und Karte testen unter Windows; Integrationstests brauchen WSL
   (einmal einrichten, braucht Administratorrechte und einen Neustart). Bis dahin: Integrationsschicht dünn halten.
9. **Einspielen ändert sich:** Nach einer Code-Änderung an einer Integration muss HA neu starten (heute reicht bei Python ein
   neuer Aufruf, E-117 „neu laden statt neu starten“). Regel: Code-Änderung = Neustart, geplant, wenn kein Gerät läuft;
   Optionsänderungen = Neuladen des Eintrags.

## Zu ChatGPTs drei Rückfragen
1. Heidi nur über die Dreame-Integration, nie direkt zur Dreame-Cloud – **ja**.
2. Haus-Modul als eigenes Repo und eigene Integration `haus`, andere Module lesen nur seine Entitäten – **ja**.
3. `module.yaml` als Pflicht – **ja ab Stufe 2**, für Stufe 0–1 freiwillig; klein halten (Vertrag + Eigentumsregister).

## Quellen der Nachprüfung
- [HA 2026.3 Release „A clean sweep“](https://www.home-assistant.io/blog/2026/03/04/release-20263/)
- [Aktion vacuum.clean_area](https://www.home-assistant.io/actions/vacuum.clean_area/)
- [Tasshack/dreame-vacuum #1498](https://github.com/Tasshack/dreame-vacuum/issues/1498)
- [command_line (scan_interval 60 s, command_timeout 15 s)](https://www.home-assistant.io/integrations/command_line/)
