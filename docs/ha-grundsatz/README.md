# HA-Grundsatzregeln

Grundsatzregeln für alle Home-Assistant-Projekte von Herbert: wie ein Gerät, ein Modul oder ein Dashboard aufgebaut wird –
vom Konzept bis zum fertigen Dashboard. Der Skill `projekt-anlegen` nutzt sie beim Anlegen von HA-Projekten
(`skills/projekt-anlegen/references/stacks/home-assistant.md`, Profilfeld `Modul.Grundsatzregeln`); das Prüfen gegen die
Regeln macht `audit`. Ein eigener Skill `modul-bauplan` ist damit entfallen.

**Stand: 23.09.2026 – im Aufbau.** Erarbeitet im ChatGPT-Review `CGR-2026-09-23-ha-grundsatz`
(`docs/chatgpt-reviews/CGR-2026-09-23-ha-grundsatz/`). Referenzfall ist die Heidi-App (Repo `HA_Dash_DreameX60`), die danach
nach diesen Regeln neu gebaut wird – ohne Migration.

| Datei | Inhalt |
|---|---|
| `recherche-2026-09-23.md` | Recherche-Brief von Claude: offizielle HA-Vorgaben und bewährte Praxis (Stand HA 2026.9.3), mit Quellen |

Ausgangspunkt aus dem Gespräch vom 23.09.2026 (Referenzfall Heidi, `docs/ENTSCHEIDUNGEN.md` dort): Schichten Quellen → Adapter →
Module → Ergebnis-Entitäten → Oberfläche, Steuerung über HA-Automationen; Ergebnisse als Entitäten (E-134); „jetzt“ aus HA,
Verlauf aus der Datenbank (E-132); gemeinsames Haus-Modul (E-136); Ausbaustufen 0–4.

## Festgelegte Regeln

Die Regeln G-01 bis G-21 stehen bis zur Grundsatzdoku (ClickUp „HA-Grundsatz · Phase 1“) in den Entscheidungen des Reviews
(`docs/chatgpt-reviews/CGR-2026-09-23-ha-grundsatz/r*/04-user-decisions.md`). Direkt von Herbert festgelegt:

| Regel | Inhalt | Festgelegt |
|---|---|---|
| G-22 Oberfläche mit Lit | Eigene Oberflächen in Home Assistant (Karten, Panels, Dialoge) werden mit **Lit** als Web Components gebaut und zu einer ausgelieferten Datei gebündelt. Kein HTML als Text mit `innerHTML`. Die Sprache folgt dem Stack des Projekts: TypeScript (Heidi) oder JavaScript (ha-baustelle). Für Code gilt die Stack-Referenz `typescript-lit` von code-erstellen; das Code-Profil des Projekts führt sie unter `Stacks`. Bestehende Oberflächen ohne Lit werden schrittweise umgestellt, nicht nebenbei. | 07.10.2026 |
