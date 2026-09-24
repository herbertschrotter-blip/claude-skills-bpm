# Review Runde 2 – Skillsystem: Abgleich mit den offiziellen Leitfäden, Skill-Profil v1, skill-pflege, Eval

## Gesprächsformat
- Sprich direkt zu mir, NICHT zu Herbert; kein Meta-Kommentar.
- Schreibe deine GESAMTE Antwort in Canvas, Titel „Review Runde 2“.
- Diese Runde liefert Entwürfe, nach denen gebaut werden kann. cc-steuerung als Cowork-Adapter, die Liste der Phase 1
  und der neue INDEX folgen in Runde 3. Wo du etwas nicht belegen kannst, kennzeichne es als Annahme.
- Fasse am Ende zusammen: ✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen

## Repo-Zugriff
Du hast Zugriff auf die GitHub-Repos und kannst selbst Dateien lesen:
- **Skill-Repo:** `herbertschrotter-blip/claude-skills-bpm` – **Branch `main`** (Runde 1 vollständig archiviert unter
  `docs/chatgpt-reviews/CGR-2026-09-24-skillsystem/r1/`, meine Einschätzung in `03-claude-analysis.md`)
- **Heidi heute:** `herbertschrotter-blip/HA_Dash_DreameX60` – Branch `main` (`CLAUDE.md`, `docs/README.md`, `docs/STATUS.md`)
- **Heidi bis 22.09.2026:** `herbertschrotter-blip/herbert-smarthome` – Branch `dreame_x60` (`CLAUDE.md` mit den alten
  Profilen – nur als Material, nicht als Vorlage)
- **BPM:** `herbertschrotter-blip/BauProjektManager` – Branch `main` (`CLAUDE.md`, `INDEX.md`)
- Nutze das aktiv. Bei JEDEM Dateizugriff den Branch angeben.

## Herberts Entscheidungen (24.09.2026)
1. **Profil:** ein Block `## Skill-Profil` mit Version in der CLAUDE.md jedes Repos (BPM, HA_Dash_DreameX60, Skill-Repo).
2. **cc-steuerung:** bleibt als **kleiner Cowork-Adapter** (rund 100 Zeilen). Er löst nur im Cowork-Chat bei
   ausdrücklichem Desktop-Commander-Wunsch aus; „Claude Code“ ist kein Auslöser mehr.
3. **Verteilung:** bleibt beim **Upload über claude.ai** – kein Laden aus `~/.claude/skills/`. Folgen: Two-Place-Pflege
   und Lieferung als Datei/Zip bleiben, die description bleibt auf 1024 Zeichen begrenzt, und die hochgeladenen Skills
   erscheinen weiter auch in Claude Code – **auch der Cowork-Adapter**. Seine Description muss Claude Code also
   ausdrücklich ausschließen, und das gehört als Fall in die Evals.
4. **Keine Schlussrunde:** Die offiziellen Leitfäden für Skills fließen als zweiter Maßstab neben der
   Neutralitäts-Checkliste ein, dazu Herberts Frage nach einem Skill-Analyse-Skill (beides unten).
5. Aus Runde 1: Herbert arbeitet am Repo fast nur in Claude Code.

## Einigkeit aus Runde 1 (Kurzform)
- Phasen 0–7: Entscheidungen → Blocker und Wahrheitsquellen → Profile → Eval-Baseline → skill-pflege neu → Querschnitt →
  Skills einzeln verkleinern → Routing-Gesamttest.
- Grenzen: audit = systemweite Konsistenz (nur prüfen); doc-pflege = Doku ändern (Modus 3/4 und Modus 6 als öffentliche
  Modi entfallen); modul-bauplan = fachlicher Lebenszyklus eines HA-Moduls; „Bauplan“ und andere Projektbegriffe raus aus
  generischen Descriptions.
- Querschnitt in drei Ebenen: globale CLAUDE.md sehr klein, Projekt-CLAUDE.md mit Skill-Profil, im Skill ein Satz;
  Regel 19 neu als „Self-contained contract, not duplicated implementation“; Fragen nur bei tatsächlich offener
  Entscheidung.
- skill-pflege mit zwei Modi (Safe Patch, Refactor mit Regel-Inventar KEEP/MOVE/MERGE/REWRITE/DROP).
- Eine Eval-Quelle, dieselben Fälle vor und nach jedem Umbau, Freigabe-Tor.
- Push-Prüfung in chatgpt-review bleibt; die Push-Berechtigung gehört ins Profil. ticket bleibt, wie er ist.

## Neu: die offiziellen Leitfäden als zweiter Maßstab
Quellen:
- Anthropic, „Skill authoring best practices“ (von mir vollständig gelesen):
  https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Agent Skills, Übersicht: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Claude Code, Skills: https://code.claude.com/docs/en/skills
- Engineering-Blog „Equipping agents for the real world with Agent Skills“:
  https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Beispiel-Skills: https://github.com/anthropics/skills

Kernregeln des Leitfadens und unser Stand (von mir gemessen):

| Regel des Leitfadens | Unser Stand |
|---|---|
| Knapp schreiben: „Claude is already very smart“ – nur, was Claude nicht schon weiß | skill-neu erklärt über rund 100 Zeilen Anthropics eigene Skill-Mechanik (Progressive Disclosure, Auslöse-Mechanik, Schreibstil). Der Leitfaden sagt ausdrücklich, dafür brauche es keinen eigenen „writing skills“-Skill. |
| SKILL.md-Körper unter 500 Zeilen | 6 von 12 darüber: skill-pflege 627, mockup-erstellen 595, chat-wechsel 570, chatgpt-review 547, skill-neu 533, code-erstellen 523 |
| References nur eine Ebene tief; Dateien über 100 Zeilen mit Inhaltsverzeichnis | tracker: 11 References über 100 Zeilen, keine mit Inhaltsverzeichnis; Verweise quer zwischen References und anderen Skills (E9) |
| Keine zeitabhängigen Angaben (Altes höchstens in einen Abschnitt „alte Muster“) | Historienmarken im Regeltext, vor allem skill-pflege (22 Zeilen: Issue-IDs wie „skill-pflege-006“, „seit 16.09.2026“, „Teil 31 / v0.17.11“), tracker (11), cc-steuerung und skill-neu (je 7) |
| Einheitliche Begriffe | gemischt, z. B. „Auswahlfrage“ neben `ask_user_input_v0`, „Task“ neben „Aufgabe“, „Profil“ neben „Projektprofil“ und „Projekt-Config“ |
| Freiheitsgrad passend zur Fragilität | zu prüfen: Wo schreiben wir fest vor, wo Urteil besser wäre (Doku schreiben, Mockup), und wo fehlt feste Führung (Commit-Folge, Ticket-Status)? |
| Description in dritter Person, „was + wann“, Schlüsselwörter, höchstens 1024 Zeichen | erfüllt (alle 12 unter 1024) |
| MCP-Werkzeuge voll qualifiziert nennen (`Server:tool`) | Spannung zur Neutralitäts-Checkliste Punkt 1 („Handlung statt Werkzeug“) |
| Evaluationen zuerst, mindestens drei je Skill, mit allen genutzten Modellen testen; „Claude A“ schreibt, „Claude B“ testet in echter Arbeit | Seit April kein Lauf (A8). Der Leitfaden sagt „currently no built-in way to run these evaluations“ – Claude Code hat dafür inzwischen aber `claude plugin eval` (unten). |
| Einheitliches Namensmuster in der Sammlung | gemischt (deutsch/englisch, `-erstellen`/`-pflege`/`-helper`); Umbenennen wäre teuer (Auslöser, Querverweise, Upload) |

### Offizielle Werkzeuge zum Prüfen von Skills (belegt)
- **`skill-creator`** (Anthropic, in Herberts Claude Code installiert): Skills anlegen und verbessern, Evals laufen
  lassen, Benchmarks mit Streuung, Descriptions auf zuverlässiges Auslösen optimieren; eigenes Format `evals/evals.json`.
  Doku: https://code.claude.com/docs/en/skills (Abschnitt „Run evals with skill-creator“).
- **`claude plugin eval`** (Claude Code): https://code.claude.com/docs/en/plugin-evals
  - Ein Fall ist ein Prompt plus Prüfer. Der Prüfer `tool_used` mit `tool: Skill` und
    `input_match: '"skill"\s*:\s*"(?:[\w-]+:)?<skill-name>"'` prüft, ob genau dieser Skill ausgelöst wurde – das ist ein
    offizieller Weg, das Auslösen zwischen Skills zu messen.
  - Jeder Fall läuft standardmäßig dreimal, jeweils in einer frischen, abgeschotteten Sitzung „with only your plugin
    loaded“. Auf Wunsch zusätzlich ohne Plugin als Vergleich; `--ablation none` spart diesen zweiten Durchgang.
  - Weiter: `--json`, HTML-Bericht, `--max-cost-usd`, `claude plugin eval init` schlägt Fälle vor. Jeder Lauf ist ein
    echter Modellaufruf auf Herberts Konto.
  - Voraussetzung ist ein Plugin mit `.claude-plugin/plugin.json`; ein bloßer Skills-Ordner ist kein Plugin. Idee: Das
    Skill-Repo bekommt ein Manifest nur für die Tests, die Verteilung über claude.ai bleibt unverändert.
  - Offen: Werden in der abgeschotteten Sitzung auch die Konto-Skills und Anthropic-Skills geladen? Wenn nicht, lassen
    sich Konfliktpaare wie skill-creator ↔ skill-neu dort nicht messen.

### Herberts Frage: Braucht es einen Skill-Analyse-Skill?
Unter Herberts zwölf Skills fehlt einer, der die eigenen Skills prüft. Die Analyse dieser Serie lief von Hand: Zeilen,
Historienmarken, tote Verweise, Werkzeugnamen, Projektwerte, Description-Länge, Leitfaden- und Neutralitäts-Checkliste.
Mein Vorschlag ist **kein dreizehnter Skill**, denn das wäre mehr Konkurrenz beim Auslösen (E5). Stattdessen:
- Das Skill-Repo bekommt ein eigenes Skill-Profil. Als Validierungsquelle nennt es beide Checklisten und ein kleines
  Prüfskript für das Mechanische.
- audit führt diese Prüfung aus, wie bei jedem anderen Projekt.
- skill-pflege nutzt dieselbe Prüfung nach jeder Änderung.
- `skill-creator` und `claude plugin eval` messen das Auslösen.

## Meine Schärfungen zu deiner Runde 1 (bitte in den Ergebnissen berücksichtigen oder begründet ablehnen)
- **S1 – v0.36.0:** Der Beleg liegt in Git, nicht im CHANGELOG: Die Commits `4c498ce` (ticket, Feature) und `3a34d48`
  (tracker, Docs) tragen beide `[v0.36.0]`.
- **S2 – Werte genau einmal:** Werte (Versionsquelle, Push-Policy, Testbefehl, Standard-Branch …) stehen nur im
  Skill-Profil; Prosa-Abschnitte der CLAUDE.md verweisen darauf oder entfallen. Nur lange Regelwerke (Validierung,
  Architekturregeln) verlinkt das Profil. Sonst bleibt die doppelte Wahrheit (heute Heidis Abschnitt „Commits“).
- **S3 – Regel-Inventar prüfbar:** Regeln mechanisch vorsammeln (Marker MUSS/NIE/IMMER/Pflicht, VERBOTEN-Listen, Tabellen
  „IMMER als Auswahlfrage“); Abgleich in beide Richtungen (auch neue Regeln im neuen Text stehen im Inventar); DROP als
  Sammelfreigabe über die Tabelle statt einer Frage je Regel; das Inventar als Datei mit dem Commit ablegen.
- **S4 – Eval automatisch:** 60 Fälle × 3 Wiederholungen von Hand sind zu viel. Also automatisch – bevorzugt mit
  `claude plugin eval` (oben), sonst mit einem Skript. Schwellen statt 100 %: kritische Fälle 3/3, sonst mindestens 2/3.
  Fälle nach Risiko verteilen: mehr für Auffang-Skills (code-erstellen, doc-pflege, audit, mockup-erstellen), weniger für
  Befehls-Skills (ticket, tracker, chatgpt-review).
- **S5 – Descriptions erst nach der Baseline ändern** (auch „Bauplan“ raus).
- **S6 – chat-wechsel:** Den vollständigen Handover-Prompt auch in Claude Code hat Herbert am 16.09. entschieden (v0.35.4,
  „Kurzform nur auf Wunsch“) – bitte nicht wieder aufmachen.
- **S7 – Tracker-Config:** `projects/<name>/` im Skill-Repo ist ein zweiter Ort für Projektwerte und bei Heidi schon
  abgedriftet. Vorschlag: ins Projekt-Repo, das Skill-Profil verweist darauf. (Mit dem Upload über claude.ai sieht der
  Cowork-Chat das Projekt-Repo nur über GitHub – prüfe, ob das den Vorschlag kippt.)
- **S8 – Abgrenzung zu `module.yaml`:** Die Serie CGR-2026-09-23-ha-grundsatz legt `module.yaml` v1 und einen
  Modul-Steckbrief fest (Skill-Repo `docs/chatgpt-reviews/CGR-2026-09-23-ha-grundsatz/`). Das Skill-Profil beschreibt die
  Arbeit im Repo (Commit, Tests, Doku, Tracker), `module.yaml` das Modul fachlich. Keine Felder doppelt; das Profil darf
  auf `module.yaml` verweisen.

## Aufgabe
1. **Abgleich mit dem Leitfaden**
   - Tabelle: 12 Skills × Checkliste „Checklist for effective Skills“ am Ende des Leitfadens (Core quality und Testing;
     die Code-Punkte nur, wo ein Skill Skripte nutzt), je Zelle ✅/⚠️/❌, je Skill die zwei wichtigsten Folgen.
   - Wo widersprechen sich Leitfaden und unsere Regeln (Neutralitäts-Checkliste, INDEX-Invarianten, skill-neu,
     skill-pflege) – z. B. MCP-Werkzeugnamen, harte Pflicht-Formulierungen, Historienmarken, Fragepflicht? Wie lösen wir
     das jeweils auf?
   - Was aus dem Leitfaden übernehmen wir als feste Regel in skill-neu und skill-pflege, und was wird dort überflüssig,
     weil Claude es ohnehin weiß?
2. **Skill-Profil v1 – Endfassung**
   - Schema als Markdown-Block: Feldname, erlaubte Werte oder Form, Pflicht/optional, Bedeutung. Regeln: Version, Werte
     genau einmal, Regelwerke per Verweis, Verhalten bei fehlendem Feld (feldweise Auswahlfrage).
   - Tabelle **Pflichtfelder je Skill** (alle 12 plus `modul-bauplan`).
   - **Drei ausgefüllte Beispiele:** HA_Dash_DreameX60 (nur Werte, die in der heutigen `CLAUDE.md` belegt sind; Lücken
     als „fehlt“ markieren), BPM (aus `CLAUDE.md` und `INDEX.md`), Skill-Repo. Dazu je Repo: welche Prosa-Abschnitte der
     CLAUDE.md danach entfallen oder nur noch verweisen (S2).
3. **skill-pflege – Spezifikation:** Ablauf Safe Patch und Refactor; Datei-Format des Regel-Inventars (Ort, Spalten,
   Zustände), mechanisches Sammeln und Abgleich in beide Richtungen (S3), Sammelfreigabe, Querverweis-Prüfung mit stabilen
   Namen statt Nummern, die Leitfaden-Checkliste als Teil der Prüfung; was aus den Regeln 1–6, 19 und 21 wird; die
   Lieferregeln (Two-Place bleibt) als Referenz.
4. **Eval:** Taugt `claude plugin eval` (mit einem Manifest nur für Tests) als unser Werkzeug, und was ergänzen
   `skill-creator` oder ein eigenes Skript?
   - Format der Fälle: Fall-Ordner von `plugin eval` statt eigener `cases.json`? Wie verhält sich das zur
     Eval-Struktur des Leitfadens (`skills`, `query`, `files`, `expected_behavior`), die eher die Ergebnisqualität misst?
   - Aufteilung der 60 Fälle nach Risiko (S4), Schwellen und Freigabe-Tor.
   - Kosten eines vollen Laufs grob schätzen und begrenzen (`--max-cost-usd`, `--ablation none`, kleines `max_turns`).
   - Wie messen wir die Konfliktpaare mit Anthropic-Skills, falls die abgeschottete Sitzung sie nicht lädt?
   - Pflichtfälle u. a.: skill-creator ↔ skill-neu/skill-pflege, code-review ↔ audit, modul-bauplan ↔ audit,
     audit ↔ doc-pflege, cc-steuerung darf in Claude Code nicht auslösen.
   - Nenne nur Optionen, die du belegen kannst; sonst als Annahme markieren.
5. **Skill-Analyse (Herberts Frage):** Trägt mein Vorschlag (Prüfung über audit mit dem Skill-Profil des Skill-Repos,
   dieselbe Prüfung als Abschluss in skill-pflege, Messen mit `skill-creator` und `plugin eval`), oder ist ein eigener
   Skill oder ein Modus „Prüfen“ in skill-pflege besser? Liste, was ein Prüfskript mechanisch abdecken kann und was ein
   Urteil braucht.

**Vorschau Runde 3:** cc-steuerung als Cowork-Adapter (Description, Kern, References, was in vier Skills wegfällt),
endgültige Liste der Phase 1 je Datei, INDEX neu mit dem Verbleib der Invarianten 1–10.

Schließe mit ✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen und nenne, was aus deiner Sicht für Runde 3 offen bleibt.
