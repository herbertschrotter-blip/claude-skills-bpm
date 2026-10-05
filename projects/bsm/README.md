# Projekt-Config `bsm` — BSM Baustrommanager (Integration `baustelle`, Repo ha-baustelle)

Projekt-spezifische Daten für den Skill `tracker`. Universelle Regeln stehen in `skills/*/SKILL.md`; hier liegt nur,
was für dieses Projekt anders ist.

| Datei | Inhalt |
|---|---|
| `clickup-lists.md` | Space, Liste, Status-Werte, Nummernschema `BSM-NNN | KÜRZEL | Titel`, Etappen-Tags, Anker |
| `clickup-fields.md` | Custom Fields der Liste mit IDs und Option-IDs |
| `memory-format.md` | Wie Claude das aktive Projekt erkennt (Claude Code: CLAUDE.md-Abschnitt `## Tracker-Profil`) |

**Projekt-Repo:** https://github.com/herbertschrotter-blip/ha-baustelle (lokal auf dem HA-Pi unter
`/config/projekte/ha-baustelle`, Branch `main`).

**Wahrheit für die Reihenfolge:** `docs/fahrplan.md` im Projekt-Repo (Etappen A–H, je Schritt eine BSM-Aufgabe).
ClickUp ist die Sicht zum Abhaken; Fahrplan und Baupläne (`docs/bauplan-datenbank.md`, `docs/bauplan-0.7.md`)
bleiben führend.

**Tickets** aus dem Melden-Knopf der Seite (`FE-/WU-/AN-NNNN`) laufen **nicht** über ClickUp, sondern über den Skill
`ticket` und `tools/ticket.py` (Ticket-Profil in der CLAUDE.md des Projekt-Repos).
