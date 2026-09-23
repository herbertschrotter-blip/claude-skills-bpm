# CGR-2026-09-23-ha-grundsatz — Grundsatzregeln für Home-Assistant-Projekte und Skill „modul-bauplan“

**Thema:** `ha-grundsatz` – Grundsatzregeln (Doku `docs/ha-grundsatz/`) und der Skill `modul-bauplan`, der vom Konzept bis zum
fertigen Dashboard führt; Referenzfall Heidi (`herbertschrotter-blip/HA_Dash_DreameX60`), die danach neu gebaut wird
**Zeitraum:** 2026-09-23
**Branch:** `main` (beide Repos)
**Status:** Runde 2 offen

---

## Runden-Übersicht

### Runde 1 — Deep Research: Praxis, Bewertung Heidi, Kritik am Konzept
- **Artefakte:** [r1/](./r1/)
- **Fokus:** Recherche zur gängigen und bewährten Praxis (offiziell und Community), Bewertung des Referenzfalls Heidi,
  Kritik an Schichten, Regeln, Ausbaustufen, Haus-Modul und Adapter, Antworten auf die offenen Grundsatzfragen, Vorschlag für
  Grundsatzregeln und Skill-Ablauf
- **Kernergebnis:** Eigenes Modul mit Logik ab Stufe 2 = eigene Integration, Heidi wird direkt als `custom_components/heidi`
  neu gebaut (nur über die Dreame-Integration); native HA-Fähigkeit vor Adapter (Dreame-Adapter bleibt, weil `clean_area`
  fehlt); Haus-Modul `haus` als eigenes Repo und eigene Integration (nur „Haus-Schluss“); Module sprechen nur über öffentliche
  HA-Schnittstellen; `module.yaml` Pflicht ab Stufe 2; kurzer Weg für Stufe 0–1. Offen: das Einstellungsmodell
  („ein Eigentümer je Datum“) → Runde 2.

### Runde 2 — Einstellungsmodell konkret, Grundsatzregeln Version 2, kurzer und voller Weg
- **Artefakte:** [r2/](./r2/)
- **Fokus:** Heidis Einstellungen durchgespielt (Ort je Einstellung, eigene Automatik je Plan, Speichern und Prüfen,
  Nachteile, Einstellungen des Haus-Moduls); Grundsatzregeln G-01 … G-16 in Version 2; kurzer Weg (Stufe 0–1) und voller Weg
  (ab Stufe 2); Vorlage Modul-Steckbrief und `module.yaml` Schema v1
- **Kernergebnis:** –
