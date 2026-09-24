# Review Runde 1 – Skillsystem: Einschätzung zu deinem Befund und eigene Analyse

## Rolle
Du bist ein erfahrener Architekt für Prompts und Skills (Claude Agent Skills: Auslösen über die Description, Progressive
Disclosure, Evals) und führst ein technisches Review-Gespräch mit einem Kollegen (Claude/Anthropic).

## Gesprächsformat
Dieses Gespräch läuft über einen Vermittler (Herbert).
- Sprich direkt zu mir, NICHT zu Herbert; kein Meta-Kommentar über das Format.
- Deinen Ausgangsbefund zu den 12 Skills hast du in diesem Chat geschrieben. Archiviert ist er unter
  `docs/chatgpt-reviews/CGR-2026-09-24-skillsystem/00-ausgangsbefund-chatgpt.md`. Die Kennungen A1 … und E1 … beziehen
  sich auf diesen Prompt.
- Schreibe deine GESAMTE Antwort in Canvas, Titel „Review Runde 1“.
- Fasse am Ende zusammen: ✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen

## Repo-Zugriff
Du hast Zugriff auf die GitHub-Repos und kannst selbst Dateien lesen:
- **Skill-Repo:** `herbertschrotter-blip/claude-skills-bpm` – **Branch `main`**
- **Belege aus den Projekten (nur lesen):**
  - Heidi heute: `herbertschrotter-blip/HA_Dash_DreameX60` – Branch `main` (`CLAUDE.md`, `docs/README.md`)
  - Heidi bis 22.09.2026: `herbertschrotter-blip/herbert-smarthome` – **Branch `dreame_x60`** (`CLAUDE.md` mit den Profilen)
  - BPM: `herbertschrotter-blip/BauProjektManager` – Branch `main` (`CLAUDE.md`, `INDEX.md`, `Docs/`)
- Nutze das aktiv, um meine Aussagen zu prüfen. Bei JEDEM Dateizugriff den Branch angeben.

## Gesprächsregeln
- Ehrlich und kritisch; Probleme konkret benennen (Datei, Stelle).
- Verbesserungen konkret zeigen (Gliederung, Regeltext, kurze Beispiele) – keine ganzen Skills ausschreiben.
- Rückfragen bei fehlendem Kontext; nur zustimmen, wenn du überzeugt bist.
- Fokus: Aufbau, Auslösen und Neutralität der Skills – keine allgemeinen Exkurse.

## Neutralitäts-Checkliste (PFLICHT-Hinweis)
Maßstab für jeden Skill (Quelle: `skills/skill-neu/SKILL.md` Schritt 3a). Vorschläge dürfen sie nicht verletzen – oder
begründen, warum ein Punkt selbst geändert werden sollte.

| # | Punkt | Richtig |
|---|---|---|
| 1 | Handlung statt Werkzeug | „Auswahlfrage“, „Shell der Umgebung“ – Werkzeugnamen nicht als Vorschrift |
| 2 | Umgebungsweiche | ein Satz im Zweck (Cowork = A, Claude Code = B), danach nur die Handlung |
| 3 | Keine Projektwerte | Pfade, IDs, Präfixe, Doc-Namen, Deploy-Befehle aus dem Profil (CLAUDE.md) oder `projects/<name>/` |
| 4 | Keine Sprache im Skill | Stack-Details in `references/<gruppe>/<key>.md` |
| 5 | Beispiele gekennzeichnet | „Beispiel (BPM)“, „Heidi: …“ – als Muster erkennbar |
| 6 | Profil-Fallback | fehlt das Profil → Auswahlfrage „Profil anlegen“ / „Werte nennen“, nie raten |
| 7 | Lieferung je Umgebung | Cowork Artifact; Claude Code Datei bzw. Zip |
| 8 | description ≤ 1024 Zeichen | gemessen |
| 9 | Split-Regel (skill-pflege Regel 21) | SKILL.md = Zweck, Kernregeln, Routing, Kurz-VERBOTEN; Abläufe in `references/` |
| 10 | Memory je Umgebung | Cowork Memory-Einträge; Claude Code Memory-Ordner |

Die Punkte 2, 7 und 10 stammen aus der Zeit, als der Cowork-Chat gleichwertig war (siehe Kontext).

## Projektkontext

### Arbeitsweise (Herbert, 24.09.2026)
- Mit den Skills am Repo arbeitet Herbert **fast nur noch in Claude Code** (Desktop-App, Windows 11, PowerShell 7). Der
  Cowork-Chat (claude.ai mit Desktop Commander, Artifacts, Memory-Einträgen) spielt für Repo-Arbeit kaum noch eine Rolle.
- Die Skills werden bei claude.ai hochgeladen und kommen darüber auch in Claude Code an. Dort sind neben Herberts 12
  Skills weitere aktiv – von Anthropic (`skill-creator`, `docs`, `consolidate-memory` …) und von Claude Code selbst
  (`code-review`, `simplify` …).
- Projekte: BPM (C#/WPF); Heidi (Home Assistant) – wird nach den Grundsatzregeln aus CGR-2026-09-23-ha-grundsatz neu
  gebaut, dazu entsteht der Skill `modul-bauplan` (Modi Planen, Prüfen, Nachschlagen); weitere HA-Projekte geplant.

### INDEX.md (laut README verbindliche Regelquelle)
- Routing-Tabelle, Hierarchie, 8 Konfliktpaare – **audit ↔ doc-pflege fehlt**.
- Invarianten 1–10 von April 2026: Acht von zehn passen nicht mehr zum heutigen Text der Skills – u. a. Nr. 1
  (`ask_user_input_v0`), 2 (Branch immer per Auswahlfrage), 5 („nie gelöscht oder gekürzt“), 6 (Quittung mit
  `[BPM-ANCHOR-…]`), 8 (Two-Place mit Artifact-Pflicht), 9 (cc-steuerung liefert das WIE). Gegen Nr. 3 (keine
  `$`-Variablen) verstoßen zwei Stellen. INDEX und README nennen die Skills außerdem „bewusst projektspezifisch“.

### docs/project-architecture.md
- Beschreibt Projektwerte in `projects/<name>/` plus Memory-Eintrag `[PROJECT]`, Statustabelle „Stand v0.12.0“. Die
  Profile in der CLAUDE.md der Projekte (v0.24–v0.36, 16.–18.09.2026) kommen nur in einer Tabellenzeile vor. Eine
  aktuelle Beschreibung des Profil-Vertrags gibt es im Repo nicht.

### Profile heute (Belege)
- **BPM** (`CLAUDE.md`, main): kein Profil-Abschnitt; Git-Regel „NIE git push ausführen — Herbert pusht selbst“.
- **Heidi bis 22.09.** (`herbert-smarthome`, Branch `dreame_x60`): sieben Profile – Commit, Tracker, Ticket, Code, Doku,
  Mockup, Review (rund 10 KB der 15-KB-Datei).
- **Heidi seit 22./23.09.** (`HA_Dash_DreameX60`, main): **kein Profil-Abschnitt**. Dieselben Fakten stehen als Prosa
  („Commits“, „Aufgaben und Tickets“, „Arbeitsweise“: „Am Ende einer Sitzung: docs/STATUS.md nachziehen, committen,
  hochladen“). Die Doku ist neu aufgebaut (`docs/STATUS.md`, `ENTSCHEIDUNGEN.md` mit E-NNN, `AUDIT.md`; kein
  `BAUPLAN.md`, kein `HANDOFF.md` mehr). Doku-Regel dort: „Keine Geschichte, nur der heutige Stand. Was nicht mehr
  gilt, wird gelöscht.“ E-108: Commits nur an Doku oder Werkzeugen behalten die Versionsnummer.
- **Skill-Repo** (`CLAUDE.md`): nur das Review-Profil.

## Das Konzept: meine Einschätzung

### Teil A – Deine Befunde, von mir geprüft
Urteil: ✅ bestätigt · ◐ teilweise · ✗ Widerspruch

| # | Dein Befund | Urteil | Beleg und Ergänzung |
|---|---|---|---|
| A1 | README/INDEX nennen 11 statt 12 Skills | ✅ größer | INDEX Z. 3 „11 Skills“, die Tabelle hat 12. README (Stand 25.04.) kennt ticket gar nicht; im Inventar (Kap. 12) fehlen `docs/chatgpt-reviews/`, `docs/ha-grundsatz/`, `projects/heidi/`; `evals/smoke-all-skills.md` steht in Kap. 3 als „geplant“ und existiert. INDEX Z. 19 nennt „8 Modi“ für doc-pflege (es sind 9). Dazu die veralteten Invarianten und `project-architecture.md` (Kontext; 7 von 11 Tabellenzeilen überholt). Die ganze Regelschicht über den Skills ist veraltet, nicht nur eine Zahl. |
| A2 | Push: git-commit-helper ↔ cc-steuerung | ✅ breiter | Sechs Skills lassen Claude pushen: git-commit-helper (Z. 178/186), doc-pflege Modus 8 (Z. 422), chat-wechsel (über Modus 8), chatgpt-review („Claude Code pusht selbst“, Z. 287), skill-neu (Z. 354), skill-pflege (Regel 12a, Schritt 5a). cc-steuerung verbietet es an vier Stellen (Z. 136, 370, 387, 415). Die Projekte sind selbst uneins: BPM „nie pushen“, Heidi „committen, hochladen“, im Skill-Repo pusht Claude. → Push ist ein **Feld im Commit-Profil**, keine Regel in einem Skill. Zusätzlich schließt git-commit-helper „git push“ in der Description aus und pusht in jeder Sequenz. |
| A3 | PowerShell-Sequenz mit `;` | ✅ | Z. 175–178 gegen Z. 203. Einfachster Fix: Herbert nutzt PowerShell 7 (Heidi: `deploy.ps1` nur mit pwsh), dort gibt es `&&` und `\|\|` (seit 7.0); nur Windows PowerShell 5.1 braucht eine Exit-Code-Prüfung. Praktisch wiegt es wenig, seit Claude Code die Befehle selbst ausführt und das Ergebnis sieht – die Copy-Paste-Sequenz stammt aus dem Cowork-Betrieb. |
| A4 | audit ↔ doc-pflege | ✅ plus | Beide Descriptions nennen Frontmatter-/Quickload-Validierung und den Bauplan; audit Modul 6 verweist für die Regeln sogar auf doc-pflege Modus 6. Die Heidi-Prüflisten gab es dreimal (audit, doc-pflege, altes Doku-Profil). Deine Trennung „prüfen = audit, ändern = doc-pflege“ trage ich mit – aber die **Prüfregeln** gehören in keinen der beiden Skills, sondern ins Projekt (Profil, Doc-Standard). Sonst verschieben wir nur die Kopie. |
| A5 | skill-pflege verhindert Konsolidierung | ✅ mit Bedingung | „Default-Philosophie: Additiv. Der Skill wird größer, nie kleiner“ (Z. 22), harte Regeln 1–6. Aber die Regel schützt vor einem echten Fehlerbild: Beim Neu-Schreiben fallen Inhalte still heraus. Ein Refactor-Modus ohne prüfbares Gegenmittel wäre ein Rückschritt (Aufgabe 4). Symptom des reinen Anbauens: skill-pflege widerspricht sich selbst – Z. 173 „Kein `present_files` für Skill-Updates“ gegen Regel 14 (Z. 234–241) „`create_file` + `present_files`, KRITISCH“; die neue Regel kam dazu, die alte blieb stehen. Zweite Wachstumsquelle ist Regel 19 „Eigenständig bleiben“ (E2). |
| A6 | SKILL.md über ~500 Zeilen | ✅ andere Metrik | Wichtiger als die Dateigröße ist, was bei einer Aufgabe gleichzeitig geladen ist: Code mit Commit und Task zieht code-erstellen (523) + Stack-Referenz + tracker (460) + git-commit-helper (273), oft doc-pflege (466) – rund 1.700 Zeilen Regeln auf einmal. |
| A7 | test-prompts.md Pflicht, nur 2 vorhanden | ✅ | skill-neu Z. 365; zwei Eval-Systeme nebeneinander. |
| A8 | Eval-Abdeckung zu gering | ✅ schärfer | Einziger Lauf: `evals/runs/smoke-2026-04-28-real.md` (30 der 86 Smoke-Fälle; ticket hat 0 Fälle). Seitdem haben sich 10 der 11 damaligen Descriptions geändert (Neutralisierung v0.24–v0.36, 16.–18.09.) – alles ungemessen. Die Test-Logs in beiden `test-prompts.md` sind leer bzw. „offen“. |
| A9 | Werkzeugnamen/Auswahlfrage fragil | ◐ | Einmal „Cowork X, Claude Code Y“ zu nennen ist gewollt und hilft Claude. Das Problem sind die Kopie des Blocks in 11 Skills (E2) und seine absolute Form (E6). |
| A10 | „profilbasiert multi-project“ 🟡 | ✗ Einstufung | Für mich 🔴: kein Namensproblem, sondern ein Vertrag ohne Abnehmer (E1). |
| A11 | cc-steuerung: Description ↔ Body | ◐ | Der Befund stimmt, deinen Fix halte ich für falsch: „ok“, „passt“, „mach“ sind die häufigsten Wörter jedes Chats (git-commit-helper schließt sie ausdrücklich aus); in der immer geladenen Description würden sie ständig auslösen. Seit „fast nur Claude Code“ stellt sich die Frage anders: Dort braucht es cc-steuerung nicht, und der Skill schadet sogar (E3). |
| A12 | chat-wechsel als Monolith | ◐ | ClickUp-Änderungen laufen schon über tracker und nur nach Auswahlfrage (Schritt 3–4, VERBOTEN). Das Problem ist die Länge des Pflichtablaufs (ClickUp laden, Chat scannen, zwei Mehrfachauswahlen, Memory-Scan, Anker, Link-Prüfung, Modus 8 mit Commit und Push) – und dass rund ein Drittel nur im Cowork-Chat gilt (Memory-Rubriken, `[ANKER-LIVE]`, Chat-URL). |
| A13 | chatgpt-review: Push-Prüfung nicht pauschal | ✗ | Der Block „Repo-Zugriff“ steht in jedem Prompt, also braucht jeder Prompt den Push-Stand. Die Prüfung ist ein Befehl und fragt nur, wenn etwas ungepusht ist. Behalten. CGR-Ablauf in eine Referenz: ✅. |
| A14 | code-erstellen „weniger magisch“ | ◐ | Die Kette ist Herberts Wunsch und größtenteils bestätigungspflichtig (Task-Zuordnung per Auswahlfrage). Das Gewicht liegt woanders: 138 von 523 Zeilen sind Querschnittsblöcke, dazu rund 60 Zeilen Auto-Anker (nur Cowork) und die BPM-Ladereihenfolge im Kern. |
| A15 | doc-pflege Modus 7 „nichts kürzen“ zu absolut | ✅ | Deine Invariante passt. Heidis eigene Doku-Regel geht schon weiter („Was nicht mehr gilt, wird gelöscht“). |
| A16 | doc-pflege Modus 8 ↔ chat-wechsel | ◐ | Die Trennung steht im Text („liefert zu“). Neu: Heidi regelt den Sitzungsabschluss inzwischen in der eigenen CLAUDE.md. |
| A17 | Versionssprung nicht bei jedem Commit | ✅ | Herbert hat das für Heidi schon entschieden (E-108). Der Skill erlaubt es nur über die Bump-Regel des Profils – und das fehlt (E1). |
| A18 | mockup: Qualitätsschleife fehlt | ◐ | In Claude Code gibt es sie zum Teil (Schritt 3 Browser-Vorschau, Screenshot, 390 px; 3b Token-Abgleich; 3c Ansichten). Es fehlen Kriterien (Überlauf, Touch-Ziele, Kontrast, Zustände). BPM-Sitemap und NN-Schema in eine Referenz: ✅. |
| A19 | skill-neu: Benchmark gegen Baseline | ✅ plus | skill-neu verbietet ausdrücklich, die Eval-Skripte zu nennen (VERBOTEN Z. 509: „nicht in claude.ai verfügbar“). In Claude Code sind sie nutzbar: skill-creator ist installiert, die Skripte liegen auch in `reference/anthropic-skill-creator/scripts/`. |
| A20 | ticket: Aufgabe optional, fixed → verification → resolved | ✗ | Beides ist da. Schritt 4 erlaubt „Ohne Aufgabe, direkt beheben“ (Auswahlfrage, falls das Profil es erlaubt). `geloest` = behoben, `geschlossen` erst nach Herberts Prüfung (Kernregel 6, Schritt 8) – genau fixed → verification → resolved. Höchstens der Name „gelöst“ ist missverständlich. |
| A21 | tracker: Interaction Tax, `references.zip` | ✅ plus | `references.zip` ist nicht nur potenziell veraltet: Sie ist getrackt, entspricht dem Stand v0.25.0, und 12 von 14 Dateien weichen heute ab (`skills/ticket.zip` liegt zusätzlich ungetrackt im Ordner). Dazu: Das Anker-System dient der Suche in claude.ai-Chats (`conversation_search`, anker-system.md Z. 3). code-erstellen sagt „In Claude Code gibt es keine Chat-Suche – kein Anker“ (Z. 178); tracker verlangt Anker in jeder Quittung und einen Referenz-Anker in jeder Folgeantwort aber unabhängig von der Umgebung, sobald das Projekt Anker führt (Heidi: ja). |

### Teil B – Eigene Befunde (in deinem Befund nicht enthalten)

**E1 🔴 Der Profil-Vertrag hat keinen Abnehmer.** Die Neutralisierung vom 16.–18.09. hat alle Projektwerte in sieben
Profile der Projekt-CLAUDE.md verlagert. Heute hat kein Projekt diese Profile (Kontext „Profile heute“). Folgen:
(a) Alle Skills laufen dauerhaft im Ersatzweg – bei BPM der „BPM-Weg“ mit festen BPM-Werten im Skill, bei Heidi die
Frage „Profil anlegen?“ oder stilles Zusammensuchen aus der Prosa. (b) Die Heidi-Beispiele im Kern von sieben Skills
beschreiben eine Struktur, die es nicht mehr gibt: Bauplan-Abschnitte 1/2/4/7/8/10/10a, HANDOFF 3e/4/5, PD-Register,
`dreame_x60/card`, `dreame_x60/mockups/bento.html`, Pflicht-Branch `dreame_x60`, Repo `herbert-smarthome` (chatgpt-review).
Rund 170 Skill-Zeilen tragen Heidi-Begriffe, rund 210 BPM-Begriffe; doc-pflege allein rund 90. (c) Auch der
„BPM-Weg“ zeigt auf Dinge, die es auf BPM `main` nicht gibt: `Docs/Referenz/DOC-STANDARD.md`,
`Docs/Referenz/chatgpt-reviews/`, `Docs/Mockups/` und im BPM-INDEX die Kapitel „Projekt-Phase (VERBINDLICH)“ (daran
hängt die Frühphasen-Regel von doc-pflege und chatgpt-review) und „PCs und Arbeitsverzeichnisse“ (anderer Branch?
bitte prüfen). (d) Die Projekt-Config im Skill-Repo widerspricht sich ebenfalls: `projects/heidi/`
nennt eine Liste (es sind drei), „keine Chat-Anker“ (die Anker-Felder gibt es), 10 statt 11 Felder und noch
`herbert-smarthome`. Lehre: Konkrete Projektbeispiele im Skill veralten mit jedem Projektumbau, und ein Vertrag, den
nichts prüft, bricht still.

**E2 🔴 Querschnittsregeln in elf Kopien.** Die Blöcke Auswahlfrage, Branch-Ermittlung, Arbeitsverzeichnis und
Vorrang/Delegation machen rund 690 der ~5.500 Zeilen aus (code-erstellen 138 von 523, chat-wechsel 95 von 570). ticket,
dein Vorbild, braucht dafür einen Satz. Ursache: skill-pflege Regel 19 („jeder Skill bleibt vollständig lesbar,
Querverweise nur als Zusatz“) plus Regeln 2/3 (nie kürzen). Kopien driften: code-erstellen Z. 154 zeigt einen
PowerShell-Befehl mit `$pc = hostname; …` – genau das Muster, das cc-steuerung 5a und INDEX-Invariante 3 verbieten;
anker-system.md Z. 7 sagt selbst, dass code-erstellen und chat-wechsel „lokale Kopien“ haben, die „mit-gepflegt werden
müssen“. Weil claude.ai jeden Skill einzeln hochlädt, gibt es keinen gemeinsamen Ordner. Der richtige Ort für
Querschnittsregeln ist der immer geladene Kontext (in Claude Code die CLAUDE.md); im Skill bleibt ein Satz.

**E3 🔴 cc-steuerung ist der einzige nicht neutralisierte Skill – und in Claude Code schädlich.** Stand April (nicht Teil
der Neutralisierung): wörtlich `ask_user_input_v0` (11×), `bash_tool` (6×), Desktop-Commander-Werkzeugnamen (9×),
`tool_search`, `github:get_file_contents`; Pfadermittlung über OneDrive + Suffix aus dem INDEX-Abschnitt „PCs und
Arbeitsverzeichnisse“, den es weder im Skill-Repo (laut Git-Historie nie) noch im BPM-INDEX gibt – und Heidi liegt gar
nicht in OneDrive (`C:\Users\herbe\source\HA_Dash_DreameX60`). Die Description löst auch auf „Claude Code“ aus; in
einer Claude-Code-Sitzung schreibt der Skill dann Desktop Commander, 25–30-Zeilen-Blöcke beim Schreiben und „nie push“
vor. Vier Skills verweisen auf „cc-steuerung Kapitel 4“. Mit „fast nur Claude Code“
spricht viel dafür, cc-steuerung stillzulegen oder auf einen kurzen Cowork-Adapter zu reduzieren.

**E4 🟠 Unerreichbare Teile.** doc-pflege Modus 3 und 4 plus Kapitel „Advisory-Checkliste“ (rund 60 Zeilen): Die
Description schließt „automatic post-change advisory checks“ aus, und code-erstellen Schritt 9 erzeugt die
Doku-Hinweise selbst – doc-pflege wird dafür nie geladen. Der Text beschreibt das Verhalten anderer Skills.

**E5 🟠 Die echte Konkurrenz fehlt in Konfliktpaaren und Evals.** In Claude Code konkurriert `skill-creator` („create
new skills, modify and improve existing skills, … optimize a skill's description“) direkt mit skill-neu und
skill-pflege; `code-review` grenzt an audit. skill-neu prüft nur Namens-, nicht Auslöse-Kollisionen mit
Anthropic-Skills. Das Messwerkzeug dafür wäre vorhanden (A19).

**E6 🟠 Die Fragepflicht erzeugt Fragekaskaden.** „Bei JEDER Entscheidungsfrage mit festen Optionen MUSS eine
Auswahlfrage gestellt werden“ heißt wörtlich: fragen, auch wenn die Antwort feststeht (chatgpt-review: „Thema der
Serie?“ auch bei eindeutigem Thema; tracker: Folgeoptionen nach jedem `done`; skill-pflege: „Nächsten Skill?“ nach jedem
Skill). Vorschlag: „Nur fragen, wenn die Antwort nicht aus Kontext, Profil oder einem klaren Standard folgt – sonst den
Standard nennen und handeln. Wenn gefragt wird, dann als Auswahlfrage.“ Das deckt sich mit der Leitlinie von Claude Code
für sein Frage-Werkzeug.

**E7 🟠 „Bauplan“ wird zum Auslöse-Konflikt.** audit („a Bauplan check“) und doc-pflege („Bauplan-Statuslisten“)
tragen Heidis alten Doc-Namen in der immer geladenen Description. Gleichzeitig entsteht `modul-bauplan` mit dem Modus
„Prüfen“ (Entwurf oder Code gegen Regeln) – fachlich audit-Gebiet. Die Grenze audit ↔ modul-bauplan muss vor dem neuen
Skill feststehen, und Projektbegriffe gehören aus den Descriptions.

**E8 🟡 Das Skill-Repo nutzt die eigenen Profile nicht.** Kein Commit-, Doku- oder Tracker-Profil in seiner CLAUDE.md,
obwohl jede Skill-Änderung CHANGELOG, INDEX, Commit und Push verlangt (skill-pflege 12a). Der CHANGELOG endet bei
v0.36.0; zehn Versionen fehlen (v0.35.2–v0.35.4, v0.36.1–v0.36.7), darunter mit v0.35.4 eine Verhaltensänderung an
chat-wechsel. v0.36.0 wurde zweimal vergeben. Für Commits an Projekt-Config oder Review-Archiv ist unklar, ob ein
Eintrag nötig ist – weil die Regel dafür fehlt.

**E9 🟠 Querverweise: tot, im Kreis, einseitig, über Nummern.**
- Tot: Die vier Verweise auf „cc-steuerung Kapitel 4“ (audit, code-erstellen, doc-pflege, mockup-erstellen) enden
  beim fehlenden PC-Abschnitt (E3); doc-pflege Z. 252 `references/projekt-init.md` (Ordner fehlt); code-erstellen
  Z. 184 „tracker-Skill Kapitel Chat-Anker-System“ (steht nur in `references/anker-system.md`).
- Im Kreis: BPM in Claude Code – chat-wechsel (Z. 20) ruft erst doc-pflege Modus 8, dessen BPM-Sitzungsabschluss
  (Z. 114) „Handover via chat-wechsel“ ist.
- Einseitig: ticket (Z. 157) „offene Tickets gehören in die Übergabe“ – chat-wechsel kennt keine Tickets; INDEX verweist
  beim Paar ticket ↔ tracker/code-erstellen auf Delegationsabschnitte, von denen keiner ticket erwähnt; tracker nennt
  `clickup-tools.md` nicht in der Routing-Tabelle (verlangt von skill-pflege Regel 21); `tracker/references/` enthält
  noch 7× `ask_user_input_v0`, obwohl CHANGELOG v0.26.0 meldet, es sei „in allen references“ ersetzt.
- Über Nummern: „cc-steuerung Kapitel 4“, „doc-pflege Modus 6/8“, „skill-pflege Regel 14a/21“, „skill-neu Schritt 3a“ …
  Jeder Umbau verschiebt Nummern – ein Grund für skill-pflege Regel 5 („Struktur nicht ändern“). Ein Refactor-Modus
  braucht deshalb eine Querverweis-Prüfung.

**E10 🟡 Zwei Lieferwege für einen Nutzer.** Die Skills kommen über den claude.ai-Upload in Claude Code an; daran hängen
Two-Place-Pflege, Zip-Lieferung, Artifact-Regeln 13–14b und „Skill für Skill“ – rund 150 Zeilen in skill-pflege und
skill-neu. Wenn Claude Code die Hauptumgebung ist, wäre zu prüfen, ob die Skills dort direkt aus dem Repo geladen werden
(persönliche Skills unter `~/.claude/skills/`, z. B. als Verknüpfung auf den OneDrive-Ordner) – dann ist der Commit die
Auslieferung. Haken: doppelte Skills, solange die hochgeladenen Kopien aktiv sind; der Cowork-Chat bekäme keine
Updates mehr.

### Teil C – Warum das System wächst
1. **Schutz auf Textebene statt auf Regelebene** (skill-pflege 1–6, doc-pflege 7b): Erlaubt ist nur Anbauen.
2. **Eigenständigkeit ohne gemeinsamen Ort** (Regel 19, Einzel-Upload): Jede Querschnittsregel wird kopiert, Kopien
   driften.
3. **Zwei Umgebungen im Kern:** Fast jede Handlung steht zweimal da, obwohl eine davon kaum noch genutzt wird.
4. **Projekte im Skill statt im Projekt:** Beispiele und Ersatzwege tragen BPM- und Heidi-Werte; der Profil-Vertrag,
   der das ablösen sollte, wird nicht geprüft und ist beim Umzug verloren gegangen.
5. **Keine Messung:** Seit April kein Eval-Lauf. Regeln entstehen aus Einzelfällen („Session Teil 28“,
   „skill-pflege-006“) statt aus Messwerten, und niemand merkt, wenn eine Kürzung schadet.

### Teil D – Zielbild und Reihenfolge (mein Vorschlag)

| Schicht | Inhalt | Ort |
|---|---|---|
| Grundregeln | Auswahlfrage-Stil (E6), Branch aus der Shell, Repo-Wurzel, Sprache, nichts Geheimes | immer geladen: `~/.claude/CLAUDE.md` oder Projekt-CLAUDE.md; Cowork: Einstellungen |
| Projektfakten | was die Skills brauchen: Commit (Module, Versionsquelle, Bump-Regel, Push), Tests, Auslieferung, Aufgabenquelle, Doku-Orte, Tracker, Review | CLAUDE.md des Projekts – ein Block, prüfbar |
| Skill-Kern | Zweck, Grenzen, Ablauf, Kurz-VERBOTEN; 100–300 Zeilen, Orchestrator bis 450 | SKILL.md |
| Details | Teilabläufe, Umgebungsadapter (`references/cowork.md`), Stack-Referenzen | `references/` |
| Messung | eine Eval-Quelle je Skill plus Konfliktpaare inkl. Anthropic-Skills; Lauf vor und nach jedem Umbau | `evals/` |

Reihenfolge:
0. Herbert entscheidet: Form des Profil-Vertrags; cc-steuerung stilllegen oder als Cowork-Adapter; Skills in Claude
   Code direkt aus dem Repo laden (ja/nein).
1. Sofort-Fixes: Push als Profilfeld; PowerShell 7 `&&`; `$`-Befehl in code-erstellen; INDEX und README (12 Skills,
   Invarianten, Inventar); Zip-Dateien; veraltete Heidi- und BPM-Werte (`herbert-smarthome`, Bauplan, HANDOFF,
   DOC-STANDARD-Pfad) raus.
2. Profile für Heidi, BPM und das Skill-Repo wieder herstellen – sonst läuft jeder weitere Umbau im Ersatzweg.
3. Eval-Baseline für das Auslösen – vor dem Kürzen, sonst ist eine Verschlechterung nicht messbar.
4. skill-pflege neu: Refactor-Modus mit Regel-Inventar und Querverweis-Prüfung; Regel 19 neu.
5. Querschnittsregeln in den immer geladenen Kontext; Cowork-Teile in Adapter; Anker nur noch im Cowork-Chat.
6. Kerne verkleinern, Skill für Skill, jeweils mit Eval-Lauf.

Unterschied zu deiner Reihenfolge: Profile (2) und Messung (3) kommen vor den großen Umbauten; einige Widersprüche aus
deinem Schritt 1 lösen sich erst mit den Profilen (Push, Versionssprung).

## Aufgabe
1. **Teil A prüfen:** Wo liege ich falsch? Besonders A11 (cc-steuerung), A13 (Push-Prüfung), A20 (ticket).
2. **Teil B prüfen:** E1–E10 im Repo gegenlesen (Datei, Stelle), bestätigen oder widerlegen. Was fehlt noch?
3. **Profil-Vertrag (E1):** strikt (feste Abschnitte `## X-Profil`, prüfbar), tolerant (Fakten in beliebiger Form in
   der CLAUDE.md) oder ein einziger Block `## Skill-Profil` für alle Skills? Empfehlung mit Begründung, Feldliste,
   Verhalten bei fehlenden Werten – und wer prüft, dass der Block vollständig und aktuell ist.
4. **skill-pflege neu (A5):** konkreter Entwurf „Safe Patch“ / „Refactor“. Wie sieht ein prüfbares Regel-Inventar aus
   (Format vorher/nachher; je Regel: behalten, verschoben nach, zusammengeführt mit, bewusst gestrichen mit Freigabe)?
   Was bleibt von den harten Regeln 1–6 und von Regel 19?
5. **Querschnittsregeln (E2, E6):** Wohin genau, und was bleibt als Satz im Skill? Wie bleibt ein Skill robust, wenn
   dieser Kontext fehlt (z. B. im Cowork-Chat)?
6. **Eval-Plan (A8, E5):** die kleinste sinnvolle Baseline – welche Fälle und Konfliktpaare (inkl. skill-creator ↔
   skill-neu/skill-pflege, code-review ↔ audit, modul-bauplan ↔ audit), eine Quelle statt zwei, Einsatz der
   skill-creator-Werkzeuge in Claude Code.
7. **Schnitt der vier größten Skills:** skill-pflege, mockup-erstellen, chat-wechsel, code-erstellen – je eine
   Gliederung Kern ↔ `references/` ↔ streichen (nur Überschriften, kein Volltext).
8. **Reihenfolge (Teil D):** Widersprich, wo sie falsch ist.

Schließe mit einer priorisierten Liste der 10 wichtigsten Maßnahmen und der Zusammenfassung
✅ Einigkeit | ⚠️ Widerspruch | ❓ Rückfragen.
