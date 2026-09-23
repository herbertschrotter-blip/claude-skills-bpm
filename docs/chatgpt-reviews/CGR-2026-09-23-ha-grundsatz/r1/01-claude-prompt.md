# Review Runde 1 – HA-Grundsatzregeln und Skill „modul-bauplan“

## Rolle
Du bist ein erfahrener Home-Assistant-Architekt (Core- und eigene Integrationen, eigene Karten und Panels, HACS) und
Architekt für modulare Systeme. Du führst ein technisches Review-Gespräch mit einem Kollegen (Claude/Anthropic).

## Gesprächsformat
Dieses Gespräch läuft über einen Vermittler (Herbert).
- Sprich direkt zu deinem Kollegen, NICHT zu Herbert
- Kein Meta-Kommentar über das Format
- **Runde 1 ist eine Deep-Research-Runde:** Recherchiere gründlich im Netz und in den beiden Repos und liefere einen
  Bericht mit dem Titel „Review Runde 1“. Ab Runde 2 antwortest du im Canvas (Titel „Review Runde N“).
- Belege Aussagen über Home Assistant mit Quellen (Link, möglichst offizielle Doku, Stand 2026) und kennzeichne eigene
  Einschätzungen als solche.
- Fasse am Ende zusammen: ✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen

## Repo-Zugriff
Du hast Zugriff auf zwei GitHub-Repos und kannst selbst Dateien lesen:
- **Skill-Repo:** `herbertschrotter-blip/claude-skills-bpm` – **Branch `main`** (Grundsatzregeln entstehen unter
  `docs/ha-grundsatz/`, der Skill unter `skills/modul-bauplan/`; Aufbau der Skills: `README.md`, `INDEX.md`,
  `docs/project-architecture.md`, `skills/skill-neu/SKILL.md`)
- **Referenzfall Heidi:** `herbertschrotter-blip/HA_Dash_DreameX60` – **Branch `main`** (Stand `16f6588`)
- Nutze das aktiv, um Aussagen zu prüfen und Originaldateien zu lesen. Bei JEDEM Dateizugriff den Branch `main` angeben.

## Gesprächsregeln
- Ehrlich und kritisch; Probleme konkret benennen (Datei, Stelle)
- Verbesserungen konkret zeigen (Struktur, Pseudocode, kurze Beispiele nur wo nötig)
- Rückfragen bei fehlendem Kontext
- Fokus: Grundsatzregeln für Herberts Home-Assistant-Projekte und der Ablauf des Skills vom Konzept bis zum fertigen
  Dashboard – keine allgemeinen Exkurse

## Rahmen (PFLICHT-Hinweis)

- Herbert ist Home-Assistant-Einsteiger; gebaut wird mit Claude Code. Regeln müssen für ihn verständlich und für
  Claude eindeutig prüfbar sein.
- Ergebnis: (1) eine Doku „HA-Grundsatzregeln“ (Skill-Repo, docs/ha-grundsatz/), (2) der Skill „modul-bauplan“, der
  vom Konzept bis zum fertigen Dashboard führt und die Reihenfolge vorschlägt (Modi: Planen, Prüfen, Nachschlagen).
- Skills sind projektneutral: Projektwerte (Pfade, Präfixe, IDs) stehen in einem Profil der CLAUDE.md des jeweiligen
  Repos; Plattform-Spezifisches (Home Assistant) in einer eigenen Referenzdatei des Skills.
- Bestehende Apps (Referenzfall Heidi) werden nach den Grundsatzregeln von Grund auf neu gebaut – ohne Migration:
  kein Übergangscode, keine Rückwärtskompatibilität. Ihr heutiger Stand ist Referenzfall und Lernquelle.
- Umgebung: Home Assistant OS auf Raspberry Pi 5, HA 2026.9; Entwicklung auf Windows 11 mit Claude Code, Konfiguration
  über ein Samba-Laufwerk, Einspielen per Skript.
- Keine externen Ressourcen in Karten; nichts Geheimes ins Repo (Tokens, Koordinaten, Gerätekennungen).
- Sprache: Deutsch.

## Projektkontext (Referenzfall Heidi, Repo `HA_Dash_DreameX60`)

### docs/ARCHITEKTUR.md (source_of_truth)
- Vier Teile: Roboter (Dreame X60) → Dreame-Integration (HACS) → Backend (YAML-Paket `ha/packages/heidi.yaml` mit Helfern,
  Vorlagen-Sensoren, `shell_command` und `command_line`; `automations.yaml`, `scripts.yaml`; Python-Skripte in `ha/prognose/`)
  → eigene Lit-Karte `card/` (ein Panel mit Seiten, gebaut zu einer Datei).
- Karte: Schichten `contract.ts` → `device.ts`/`profile.ts` → Selektoren → Komponenten; Schreiben nur über `DxApi`;
  nichts fest verdrahten (Gerät, Räume, Optionen kommen vom Gerät); Unit- und Playwright-Tests; Einspielen mit
  Prüfsummen (`tools/deploy.ps1`).

### docs/DATEN.md (source_of_truth)
- Heute verteilte Daten (CSV/JSON-Dateien, HA-Helfer); Zielbild eine SQLite-Datenbank `heidi.db` mit „eine Quelle je Wert“.
  Schritt 1 ist gebaut: ein Python-Modul öffnet die Datenbank, alle Dateien liegen als Spiegel darin, Sicherung um 02:50,
  Ansehen über HA (Abschnitt 8). Sieben Einstellungen liegen doppelt (Abschnitt 4.2).

### docs/HAUSREGELN.md (Entwurf, pausiert)
- Bestandsaufnahme zu Ruhezeiten („Nicht stören“), Anwesenheit, Arbeitszeit und Heimkehr mit 13 Widersprüchen
  (Abschnitt 3.8) – typisch für gewachsene Logik; Zielbild mit Ergebnis-Entitäten; wird mit dem Haus-Modul neu geschnitten.

### docs/ENTSCHEIDUNGEN.md
- Grundsätze E-01 bis E-26 (nichts fest verdrahten, Geräteprofil, eine API-Schicht, Selektoren …), E-128 (eine Datenbank),
  E-132 („jetzt“ aus der HA-Entität, Verlauf aus der Datenbank), E-134 (Ergebnisse als Entitäten), E-136 (gemeinsames
  Haus-Modul).

### Recherche von Claude (Skill-Repo `docs/ha-grundsatz/recherche-2026-09-23.md`)
- Offizielle HA-Vorgaben und bewährte Praxis, Stand HA 2026.9.3, mit Quellen: Rollen (Integration/Entitäten/Dienste/
  Automationen/Dashboard), Integration Quality Scale (54 Regeln), Bausteine eigener Integrationen, Grenzen von
  `shell_command`/`command_line`, Karten-APIs 2026. **Bitte prüfen, ergänzen, korrigieren.**

## Das Konzept (Entwurf aus dem Gespräch Herbert/Claude am 23.09.2026)

### Ziel
Grundsatzregeln für alle Home-Assistant-Projekte von Herbert und ein Skill, der sie anwendet. Projekte heute und geplant:
Heidi (Saugroboter, Neubau), Netzdiagnose (FRITZ!Box, Speedtest; eigenes Repo), Poolsensor iCO, Mähroboter Mammotion Luba,
ein eigener Lüftungsrechner und weitere. Viele haben eigene Logik und sollen untereinander Daten liefern und auswerten.

### Schichten
```
Quellen                      Adapter                    Module (Fachlogik)       Ausgabe                        Oberfläche / Wirkung
Gerät über Integration ──►   Geräte-Schnittstelle   ──► rechnen, entscheiden ──► Ergebnis-Entitäten (E-134) ──► Karten, Dashboards, Automationen
HA-Entitäten („jetzt“)       je Hersteller              (reine Funktionen)       Dienste als Schreibwege
eigene Datenbank ◄────────────────────────────────────  schreiben nur ihre       Entscheidung ──► HA-Automation/Skript ──► Gerät
(Verlauf, Einstellungen,                                eigenen Tabellen
 eigener Zustand)
Rückweg: Oberfläche ──► API-Schicht ──► Dienst/Skript ──► Modul (Einstellung) oder Gerät (Befehl)
```

### Regeln (Entwurf)
1. **Eine Quelle je Wert:** „jetzt“ aus der HA-Entität; Verlauf, Einstellungen und eigener Zustand aus der Datenbank; keine Kopien.
2. **Module rechnen, die Oberfläche zeigt nur an** – keine Nachrechnung in der Karte.
3. **Ergebnisse als eigene Entitäten** – nichts doppelt (was HA weiß, bleibt dort), keine Einstellungen als Ergebnis.
4. **Datenaustausch zwischen Modulen nur über Entitäten**, nie direkt.
5. **Steuerung:** Module entscheiden, HA-Automationen und Skripte führen aus; die Oberfläche schreibt nur über eine API-Schicht.
6. **Fähigkeiten statt Modelle**; nichts fest verdrahten, was Gerät oder HA liefern.
7. **Adapter je Hersteller** für alles, was HA nicht vereinheitlicht (Raumreinigung, Werte je Raum, Karte …).
8. **Gemeinsames „Haus“-Modul** für Anwesenheit, Ruhezeiten und Arbeitszeit; alle Geräte nutzen es.
9. **Ausbaustufen – so niedrig wie möglich beginnen:** 0 nur HA · 1 Logik in HA (Vorlagen, Automationen, Blueprints) ·
   2 eigenes Modul · 3 eigene Oberfläche · 4 Adapter für mehrere Hersteller.
10. **Arbeitsweise:** Tests grün vor jedem Commit, Doku im selben Commit, Entscheidungen als nummerierte Einträge,
    große Oberflächen zuerst als Mockup.

### Offene Grundsatzfragen
- Eigene Integration (`custom_components`) oder YAML + Python über `shell_command`/`command_line` (heute bei Heidi) – ab welcher
  Stufe? Folgen: Neustart nach Code-Änderungen, Tests nur unter WSL, dafür keine 60-s-Grenze und kein Prozessstart je Aufruf.
- Einstellungen: eigene Datenbank mit Katalog (Heidi) oder Einstellungs-Entitäten (`EntityCategory.CONFIG`) oder Optionsdialog?
- Datenhaltung: eigene SQLite-Datenbank je Projekt, HA-Recorder/Store oder zusätzlich InfluxDB für Auswertungen über Geräte?
- Oberfläche: eine Karte als „App“ (Panel mit Seiten, wie Heidi), Dashboards aus Standard-Karten oder Dashboard-Strategie?
- Wo liegt ein geteiltes Modul (Haus-Modul), wie wird es versioniert und eingespielt?
- Wie sieht eine Geräte-Schnittstelle konkret aus? Wie lösen andere das (z. B. Plattform-Vorlagen der
  `xiaomi-vacuum-map-card`, Stand der Vereinheitlichung der Raumreinigung in HA)?

### Skill-Ablauf „modul-bauplan“ (erste Skizze)
- **Planen:** 0 Idee und Ausbaustufe → 1 Bestandsaufnahme (Gerät, Integration, Entitäten) → 2 Konzept (Quellen, Module,
  Datenmodell, Ergebnis-Entitäten, Schreibwege) → 3 Mockup → 4 Adapter/Integration → 5 Module mit Tests → 6 Entitäten und
  Dienste → 7 Oberfläche/Dashboard → 8 Automationen → 9 Doku, Einspielen, Abnahme.
- **Prüfen:** Entwurf oder Code gegen die Regeln, Befunde mit Schwere.
- **Nachschlagen:** „Wie macht man X richtig?“ mit Verweis auf die Regel.

### Referenzfall Heidi – bekannte Schwächen
Einstellungen doppelt (Helfer und `planer.json`), laufender Zustand an drei Stellen, Reste der ersten Version, 60-s-Grenze,
Sensoren im Abfragetakt, Argumente als base64, Gerätename in Vorlagen fest verdrahtet, 13 Widersprüche bei Ruhe und
Anwesenheit (`docs/DATEN.md` 4, `docs/HAUSREGELN.md` 3.8, `docs/AUDIT.md`).

## Aufgabe (Deep Research)
1. **Recherche:** Was ist 2026 gängige und bewährte Praxis für Home-Assistant-Projekte mit eigener Logik – vom Konzept bis
   zum Dashboard? Offizielle Vorgaben (developers.home-assistant.io, Integration Quality Scale, Frontend-Doku, Architektur-ADRs),
   Community-Leitfäden (Forum, Blogs, der Community-Skill „home-assistant-best-practices“ von homeassistant-ai,
   „awesome-home-assistant“) und gut gebaute Beispielprojekte (Integrationen, die Entitäten zu fremden Geräten liefern;
   Karten mit Plattform-Adaptern). Prüfe und ergänze den Recherche-Brief.
2. **Bewertung des Referenzfalls Heidi:** Was ist gut, was ist schlechter als gängige Praxis, was fehlt? Priorisiert, mit
   Dateien. Keine Kleinigkeiten – es geht um den Neubau.
3. **Kritik am Konzept:** Schichten, Regeln 1–10, Ausbaustufen, Haus-Modul, Adapter. Was fehlt, was ist überflüssig, was
   widerspricht der HA-Praxis?
4. **Antworten auf die offenen Grundsatzfragen** mit Empfehlung und Begründung – einfach und mit Claude Code gut wartbar.
5. **Vorschlag „Grundsatzregeln“ – wie, wo, was:** Gliederung einer Doku mit konkreten Regeln: Projekt- und Repo-Struktur,
   Namensschema (Entitäten, Dienste, Dateien), Vorlage eines Moduls, Daten und Einstellungen, Oberfläche, Tests, Doku,
   Einspielen, Versionen, Arbeitsablauf.
6. **Vorschlag Skill-Ablauf „modul-bauplan“:** Phasen mit Ergebnis je Phase, Prüfliste, Entscheidungspunkte, Reihenfolge;
   wie „Prüfen“ und „Nachschlagen“ arbeiten.
7. **„Genial“:** 3–5 Ideen über die gängige Praxis hinaus, die sich für Herbert lohnen.

Schließe mit einer priorisierten Liste der 10 wichtigsten Empfehlungen und der Zusammenfassung
✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen.
