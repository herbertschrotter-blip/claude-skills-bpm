# Review Runde 3 – Skillsystem: Umbau-Plan

## Gesprächsformat
- Sprich direkt zu mir, NICHT zu Herbert; kein Meta-Kommentar.
- Schreibe deine GESAMTE Antwort in Canvas, Titel „Review Runde 3“.
- Ziel dieser Runde: ein **umsetzbarer Umbau-Plan**, nach dem Claude Code Schritt für Schritt bauen kann – mit fertigen
  Texten, wo sie kurz sind (Profil, Description, Manifest, Pilotfälle), und Gliederungen, wo sie lang wären. Wo du etwas
  nicht belegen kannst, kennzeichne es als Annahme.
- Fasse am Ende zusammen: ✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen – und schreibe „Serie abschließbar“, wenn aus
  deiner Sicht nichts Grundsätzliches mehr offen ist.

## Repo-Zugriff
Du hast Zugriff auf die GitHub-Repos und kannst selbst Dateien lesen:
- **Skill-Repo:** `herbertschrotter-blip/claude-skills-bpm` – **Branch `main`** (Runden 1 und 2 vollständig archiviert
  unter `docs/chatgpt-reviews/CGR-2026-09-24-skillsystem/`, meine Einschätzung zu Runde 2 in `r2/03-claude-analysis.md`)
- **Heidi heute:** `herbertschrotter-blip/HA_Dash_DreameX60` – Branch `main`
- **BPM:** `herbertschrotter-blip/BauProjektManager` – Branch `main`
- Nutze das aktiv. Bei JEDEM Dateizugriff den Branch angeben.

## Herberts Entscheidungen (Stand 24.09.2026)
1. **Skill-Profil v1:** ein Block `## Skill-Profil` mit Version in der CLAUDE.md jedes Repos.
2. **cc-steuerung:** bleibt als kleiner Cowork-Adapter (rund 100 Zeilen); „Claude Code“ ist kein Auslöser mehr.
3. **Verteilung:** bleibt beim Upload über claude.ai; die hochgeladenen Skills erscheinen auch in Claude Code.
4. Herbert arbeitet am Repo fast nur in Claude Code.
5. **Push im Skill-Repo:** nach jedem Commit ohne Rückfrage (`Push-Policy: required-after-commit`) – gilt ab sofort.
6. **Version im Skill-Repo:** neue Nummer und CHANGELOG-Eintrag nur bei Skill-Änderungen; Commits an Doku, Reviews oder
   Config behalten die Nummer (wie Heidi E-108) – gilt ab sofort, der Commit von Runde 2 trägt weiter `v0.36.9`.
7. **Tests:** zuerst ein Pilot (5 Fälle × 3 Läufe, `--ablation none`), danach entscheidet Herbert über die volle
   Grundmessung. Die Läufe zählen gegen sein claude.ai-Kontingent (Abo, keine Abrechnung nach Verbrauch).

## Einigkeit aus Runde 2 (Kurzform)
- **MCP:** Die Kernlogik beschreibt die Handlung; ein zwingend nötiges MCP-Werkzeug steht voll qualifiziert im
  Integrationsabschnitt oder in einer Referenz.
- **Regeln:** MUSS/NIE nur, wo es heikel ist. Keine Historie in Skills. Fragen nur bei tatsächlich offener
  Entscheidung. skill-neu wird vom Lehrgang zum Governance-Ablauf.
- **Skill-Profil v1** mit Checks-Abschnitt und den Werten `none`/`fehlt`/`ref:`; Werte genau einmal;
  `projects/<name>/` verschwindet aus dem Skill-Repo.
- **skill-pflege:**
  - Safe Patch und Refactor.
  - Inventar unter `docs/skill-refactors/`, Zustände `KEEP|MOVE|MERGE|REWRITE|DROP|NEW`.
  - Abgleich in beide Richtungen, DROP als Sammelfreigabe.
  - Verweise über Datei und Überschrift.
  - Lieferung in `references/delivery.md`.
- **Eval:**
  - `claude plugin eval` misst das Auslösen zwischen unseren Skills.
  - Ein kleiner Satz echter Sitzungen misst Konflikte mit Anthropic-Skills.
  - `skill-creator` misst die Qualität eines einzelnen Skills.
  - `test-prompts.md` entfällt.
  - 60 Fälle nach Risiko, Schwellen 3/3 kritisch und 2/3 normal, Freigabe-Tor.
  - Getestet wird nur mit den Modellen, die Herbert nutzt.
- **Kein dreizehnter Skill:** Ein Prüfskript liefert die mechanischen Fakten, audit urteilt, skill-pflege nutzt dieselbe
  Prüfung als Abschluss. Kein Umbenennen.

## Meine Korrekturen zu Runde 2 (bitte übernehmen oder begründet ablehnen)
- **K1 – Stack-Referenzen bleiben:** Der Leitfaden meint mit „eine Ebene tief“ Verweisketten (SKILL.md → a.md → b.md),
  nicht die Ordnertiefe; sein eigenes Beispiel nutzt `reference/finance.md`. `references/stacks/<key>.md` wird direkt aus
  SKILL.md geladen – kein Umzug.
- **K2 – Synchronisierungspfad:** Auf Herberts PC liegen die synchronisierten Skills unter
  `AppData\Roaming\Claude\…\skills-plugin\…\skills\` (Desktop-App) und erscheinen als `anthropic-skills:<name>`;
  `~/.claude/skills` existiert nicht. Die Kernaussage stimmt; für den Plan ist der Pfad unwichtig.
- **K3 – Review braucht eine eigene Config:** chatgpt-review braucht Themen, Reviewer-Rolle, GitHub-Repos und je Thema
  einen Pflicht-Block (siehe heutiges `## Review-Profil` in der CLAUDE.md des Skill-Repos – eine Tabelle je Thema). Das
  passt nicht in flache `Feld: Wert`-Zeilen. Vorschlag: `Review.Config: <Datei>` wie bei Tracker.
- **K4 – Checks mit Pfaden:** z. B. `card: npm test; npm run lint [card/**]`, dann `Pre-Commit-Checks: card; backend`
  (je nach geänderten Pfaden). „card bzw. backend nach Änderung“ ist kein Check-Name.
- **K5 – Zähler:** Die nächste freie Aufgabennummer gehört in die Tracker-Config im Projekt-Repo.
- **K6 – Heidi-Lücken teils ableitbar:** Pflichtdokumente stehen in `docs/README.md` (Spalte „Wann lesen“),
  Aufgabenquelle ist `docs/STATUS.md` plus ClickUp. Beim echten Profil mit Herbert füllen.
- **K7 – `projects/` umziehen, nicht löschen:** `projects/bpm/clickup-lists.md` enthält auch die Skill-Issue-Listen des
  Skill-Repos selbst – die wandern in dessen eigene Tracker-Config; `memory-format.md` (Cowork-Memory) geht in den
  Cowork-Adapter oder entfällt.
- **K8 – Kosten:** `--max-cost-usd` begrenzt laut Doku die Schätzung nach Listenpreis, nicht das Kontingent eines Abos.
- **K9 – Laufzeiten:** Auf dem PC dieser Sitzung (Büro-PC) ist **Python nicht installiert**, wohl aber Node 24 und
  PowerShell 7.6. Die Skripte des `skill-creator` (u. a. `run_eval.py`, `quick_validate.py`) brauchen Python;
  `claude plugin eval` braucht es nicht. Das Prüfskript sollte deshalb in PowerShell 7 oder Node laufen – oder der Plan
  nennt Python als Voraussetzung auf allen drei PCs. `reference/anthropic-skill-creator/scripts/quick_validate.py` prüft
  bereits Frontmatter-Schlüssel, Name, Description-Länge und spitze Klammern und taugt als Vorlage (keine unserer
  Descriptions enthält spitze Klammern – geprüft).

## Aufgabe (Umbau-Plan)
1. **Skill-Profil v1 – letzte Fassung:** K3–K6 eingearbeitet. Dazu das **vollständige Profil des Skill-Repos** mit
   Herberts Werten (Push, Version, Branch, Format, Module = Skill-Name bzw. Thema, Checks: Prüfskript und Routing-Eval,
   Doku-Check), fertig zum Einfügen in `CLAUDE.md`. Das bisherige `## Review-Profil` wandert in die Review-Config (K3).
2. **Orte der Projekt-Configs:** endgültiger Pfad und Aufbau für Tracker-, Ticket- und Review-Config im Projekt-Repo;
   Umzugsplan für `projects/bpm/` und `projects/heidi/` (K7).
3. **cc-steuerung als Cowork-Adapter:** Description (≤ 1024 Zeichen, schließt Claude Code aus), Gliederung des Kerns
   (rund 100 Zeilen), References, was ersatzlos entfällt; was in audit, code-erstellen, doc-pflege und mockup-erstellen
   an Cowork-Pfadermittlung und Verweisen auf cc-steuerung wegfällt.
4. **INDEX neu:** Gliederung und Entwurf (Inventar, Routing, Konfliktpaare inkl. Anthropic-Skills und modul-bauplan,
   Verweise auf die Regelquellen). Für jede Invariante 1–10 der neue Ort (löschen, globale Regel, Skill-Profil,
   Fachskill, Reference). Was wird aus README und `docs/project-architecture.md`?
5. **Prüfskript:** erstes Schema – Prüfungen (aus deiner Liste in Runde 2), was Fehler und was Warnung ist, Ausgabe
   (JSON), Exit-Codes, Ort im Repo, Sprache (K9).
6. **Eval-Pilot:** Inhalt von `.claude-plugin/plugin.json` (nur für Tests); Ort der Eval-Fälle – `evals/` ist heute mit
   den alten Katalogen belegt (umbenennen oder anderer Ordner über `experimental.evals`?); die ersten fünf Fälle als
   Dateien (`prompt.md` und Prüfer, `max_turns` klein); der Befehl für den Pilotlauf; das Protokoll-Format für die echten
   Sitzungen mit Anthropic-Skills (3–5 Prompts).
7. **Phase 1 – Dateiliste:** je Datei die Änderung, Safe Patch oder Refactor, Reihenfolge; ausdrücklich getrennt, was
   erst nach der Baseline kommt (Descriptions, S5). Welche Schritte muss Herbert selbst tun (Upload bei claude.ai,
   Entscheidung über die volle Messung)?
8. **Gesamtplan:** Phasen 1–7 als Checkliste mit Abnahme je Phase.

Schließe mit ✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen – und „Serie abschließbar“, wenn nichts Grundsätzliches mehr
offen ist.
