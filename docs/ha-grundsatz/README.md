# HA-Grundsatzregeln

Grundsatzregeln für alle Home-Assistant-Projekte von Herbert: wie ein Gerät, ein Modul oder ein Dashboard aufgebaut wird –
vom Konzept bis zum fertigen Dashboard. Daraus entsteht der Skill `modul-bauplan` (Modi: Planen, Prüfen, Nachschlagen).

**Stand: 23.09.2026 – im Aufbau.** Erarbeitet im ChatGPT-Review `CGR-2026-09-23-ha-grundsatz`
(`docs/chatgpt-reviews/CGR-2026-09-23-ha-grundsatz/`). Referenzfall ist die Heidi-App (Repo `HA_Dash_DreameX60`), die danach
nach diesen Regeln neu gebaut wird – ohne Migration.

| Datei | Inhalt |
|---|---|
| `recherche-2026-09-23.md` | Recherche-Brief von Claude: offizielle HA-Vorgaben und bewährte Praxis (Stand HA 2026.9.3), mit Quellen |

Ausgangspunkt aus dem Gespräch vom 23.09.2026 (Referenzfall Heidi, `docs/ENTSCHEIDUNGEN.md` dort): Schichten Quellen → Adapter →
Module → Ergebnis-Entitäten → Oberfläche, Steuerung über HA-Automationen; Ergebnisse als Entitäten (E-134); „jetzt“ aus HA,
Verlauf aus der Datenbank (E-132); gemeinsames Haus-Modul (E-136); Ausbaustufen 0–4.
