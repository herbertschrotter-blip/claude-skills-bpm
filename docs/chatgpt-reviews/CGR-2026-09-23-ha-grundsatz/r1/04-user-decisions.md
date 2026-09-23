# Runde 1 – Entscheidungen von Herbert (23.09.2026)

| Frage | Entscheidung |
|---|---|
| Daten und Einstellungen: „Ein Eigentümer je Datum“ – Einstellungen als HA-Einstellungs-Entitäten bzw. Optionsdialog, eigene Datenbank nur für Fachdaten? | **ChatGPT fragen** – in Runde 2 konkret an Heidis Einstellungen durchspielen lassen |
| Eigene Integration ab Stufe 2 – und Heidi direkt so neu bauen (Neustart nach Code-Änderungen, WSL für Integrationstests)? | **Ja** |
| ChatGPTs Rückfragen: (1) Heidi nur über die Dreame-Integration, nie direkt zur Cloud; (2) Haus-Modul als eigenes Repo und eigene Integration `haus`; (3) `module.yaml` als Pflicht ab Stufe 2 | **Alle drei ja** (`module.yaml` klein: Vertrag + Eigentumsregister; Stufe 0–1 freiwillig) |

Übernommen aus der Einschätzung von Claude (ohne Gegenrede): `command_line` fragt standardmäßig alle 60 s ab; Dreame kann
`vacuum.clean_area` noch nicht, der Adapter bleibt und schaltet später um; die Karte liest den Roboter über `vacuum.*`, die
Heidi-Integration veröffentlicht nur eigene Ergebnisse; Entitäten über das Register finden; kurzer Weg für Stufe 0–1;
Modul-Steckbrief + `module.yaml`; Name `haus`; Entwicklungsumgebung als Grundsatz; Code-Änderung an einer Integration = Neustart.
