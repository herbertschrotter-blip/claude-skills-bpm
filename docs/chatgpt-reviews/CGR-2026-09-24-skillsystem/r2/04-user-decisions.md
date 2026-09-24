# Entscheidungen Herbert – Runde 2 (24.09.2026)

| Frage | Antwort | Folge |
|---|---|---|
| Push im Skill-Repo | **Nach jedem Commit** (Empfehlung) | Claude pusht im Skill-Repo nach jedem Commit ohne Rückfrage (`Push-Policy: required-after-commit`). Gilt ab sofort. Ausgeliefert werden die Skills dadurch nicht – das bleibt der Upload bei claude.ai. |
| Versionsnummer und CHANGELOG im Skill-Repo | **Nur Skill-Änderungen** (Empfehlung) | Neue Nummer und CHANGELOG-Eintrag nur, wenn sich ein Skill ändert; Commits an Doku, Reviews oder Config behalten die Nummer (wie Heidi E-108). Gilt ab sofort: Der Commit dieser Runde trägt weiter `v0.36.9`. |
| Automatische Tests der Skills | **Pilot, dann entscheiden** (Empfehlung) | Erst 5 Fälle mit je 3 Läufen (15 kurze Sitzungen, `--ablation none`); danach entscheidet Herbert über die volle Grundmessung mit 60 Fällen |

## Nachfrage von Herbert

„Was für eine Kostenabgabe?“ – Antwort: keine Abgabe. Jeder Lauf von `claude plugin eval` ist eine echte Claude-Sitzung
und zählt laut Doku gegen das Nutzungskontingent des Abos; eine Rechnung nach Verbrauch entsteht nur mit einem
API-Schlüssel. Die Dollarbeträge der Doku sind Schätzungen nach Listenpreis; `--max-cost-usd` begrenzt diese Schätzung,
nicht das Kontingent.

## Weiter

Runde 3: umsetzbarer Umbau-Plan – ChatGPTs acht offene Punkte, Claudes Korrekturen K1–K9, das vollständige Skill-Profil
des Skill-Repos mit den Werten oben, Eval-Pilot als Dateien.
