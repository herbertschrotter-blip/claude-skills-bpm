# INDEX — Skill-Übersicht

Verzeichnis der 14 Skills im Repo `claude-skills-bpm`: wofür jeder zuständig ist, wann er auslöst und wie Konflikte
zwischen Skills entschieden werden. Die Regeln selbst stehen in den Skills und in den Dokumenten unten – dieser Index
wiederholt sie nicht.

- Qualitätsregeln für alle Skills: [docs/skill-quality.md](./docs/skill-quality.md)
- Projektwerte (Skill-Profil der `CLAUDE.md`, Configs unter `.claude/skill-config/`):
  [docs/skill-profile-v1.md](./docs/skill-profile-v1.md)
- Laufender Umbau: [docs/skillsystem-umbau.md](./docs/skillsystem-umbau.md) · Einstieg: [README.md](./README.md) ·
  Versionen: [CHANGELOG.md](./CHANGELOG.md)

---

## Skills

| Skill | Zuständig für | Löst aus bei |
|-------|---------------|--------------|
| **audit** | Konsistenz zwischen Code und Doku prüfen, read-only; Befunde → tracker oder Fix-Skill | "audit", "prüfe alles", "konsistenzcheck", "passt die Doku noch zum Code" |
| **cc-steuerung** | Desktop Commander im Cowork-Chat (Modalität, WIE statt WAS); nie in Claude Code | im Cowork-Chat: "cc mach", "dc lies", "direkt auf den PC" |
| **chat-wechsel** | Übergabe an die nächste Sitzung (Handover-Prompt; in Claude Code vorher Sitzungsabschluss über doc-pflege) | "neuer chat", "übergabe", "chat wechsel" |
| **chatgpt-review** | Review-Prompts für ChatGPT, Runden und Archiv (CGR) nach der Review-Config des Repos | "besprich mit ChatGPT", "zweite Meinung", "Runde N" |
| **code-erstellen** | Code planen und ändern nach dem Profil des Repos (Pflichtkontext, Aufgabenquelle, Stack-Referenzen, Tests, Auslieferung) | jede Anfrage, die Code-Erstellung oder -Änderung meint |
| **doc-pflege** | Projektdoku anlegen, pflegen, validieren; Sitzungsabschluss | "pflege docs", "schreib ADR", "neues Konzept", "Sitzung abschließen" |
| **git-commit-helper** | Commit-Befehle und -Messages im Format `[vX.Y.Z] Modul, Typ: Kurztitel`, Version-Bump | "commit", "git commit", "PATCH oder MINOR?" |
| **mockup-erstellen** | HTML-Mockups nach dem Mockup-Profil, Token-Abgleich, Abnahme festhalten | "Mockup für", "Screen-Design", "UI-Mockup" |
| **projekt-anlegen** | Neue Projekte anlegen und einrichten, nach Stack; Übergabe an mockup-erstellen, code-erstellen oder tracker | "neues Projekt", "leg mir ein Projekt an", "ich will X bauen, weiß aber nicht wie", "Repo holen und einrichten" |
| **skill-neu** | Neue Skills für dieses Repo anlegen (Absicht, Kollisionsprüfung, Neutralität, Eval-Fälle) | "neuer Skill für X", "erstelle einen Skill" |
| **skill-pflege** | Bestehende Skills ändern: Safe Patch oder Refactor mit Regel-Inventar; Lieferung | "Skill updaten", "Skill ändern", "Skill erweitern" |
| **skill-auswertung** | Skill-Log auswerten (Zündungen im Alltag), Modi Schnellblick/Standard/Tiefenanalyse; Befunde → Eval-Fälle, tracker, skill-pflege | "skills auswerten", "skill-log auswerten", "wie zünden die Skills" |
| **ticket** | Fehler-Tickets eines Projekts einzeln, immer im selben Ablauf, jeder Schritt mit Auswahlfrage | "ticket HT-0007", "ticket liste", "nimm das nächste ticket" |
| **tracker** | Einzige Schreibschnittstelle für ClickUp-Aufgaben und Skill-Issues | "tracker neu", "tracker done", "tracker issue", "tracker suche" |

Was jeder Skill ausdrücklich **nicht** übernimmt, steht in seiner Description („Do not trigger for …“) und in seinem
Abschnitt „Vorrang / Delegation“.

### Arten

- **Orchestrator:** code-erstellen (ruft mockup-erstellen, git-commit-helper, doc-pflege, tracker, audit auf)
- **Ändern Dinge:** skill-neu, skill-pflege (Skills), doc-pflege (Doku), projekt-anlegen (neue Projekte)
- **Abläufe:** chat-wechsel, chatgpt-review, audit, ticket, skill-auswertung
- **Schnittstellen:** tracker (ClickUp), git-commit-helper (Git), mockup-erstellen (HTML-Mockups)
- **Modalität:** cc-steuerung (läuft parallel zum Fachskill, nur im Cowork-Chat)

---

## Konfliktpaare

| Paar | Entscheidung |
|---|---|
| code-erstellen ↔ mockup-erstellen | Code → code-erstellen; HTML-Mockup → mockup-erstellen |
| code-erstellen ↔ git-commit-helper | Code-Änderung samt Commit-Vorschlag → code-erstellen; ausdrücklicher Commit-Wunsch → git-commit-helper |
| code-erstellen ↔ doc-pflege | Doku-Hinweise aus code-erstellen lösen doc-pflege nicht aus; ausdrücklicher Doku-Auftrag → doc-pflege |
| code-erstellen ↔ tracker | Code, auch mit Aufgabenbezug → code-erstellen; ausdrücklicher Tracker-Befehl → tracker |
| ticket ↔ tracker / code-erstellen | Ticketnummer oder Ticket-Befehl → ticket (ruft tracker und code-erstellen selbst auf); Aufgabe ohne Ticket → tracker; Bugfix ohne Ticket → code-erstellen |
| audit ↔ code-erstellen | read-only Prüfung → audit; Fixes → code-erstellen (nach Auswahlfrage) |
| chat-wechsel ↔ chatgpt-review | Übergabe an Claude → chat-wechsel; Review-Prompt für ChatGPT → chatgpt-review; unklar → Auswahlfrage |
| projekt-anlegen ↔ code-erstellen | neues Projekt anlegen oder Repo holen und einrichten → projekt-anlegen; Änderung in einem bestehenden Projekt → code-erstellen |
| projekt-anlegen ↔ mockup-erstellen | neues Projekt aufsetzen, auch bei offener Art → projekt-anlegen (bietet mockup-erstellen an); nur Aussehen entwerfen → mockup-erstellen |
| projekt-anlegen ↔ skill-neu | neues Projekt → projekt-anlegen; neuer Skill → skill-neu |
| skill-neu ↔ skill-pflege | Die SKILL.md gibt es schon → skill-pflege; ganz neuer Skill → skill-neu |
| skill-auswertung ↔ skill-pflege | Log auswerten, Befunde finden → skill-auswertung; Skill-Text ändern, auch nach einem Befund → skill-pflege |
| cc-steuerung ↔ Fachskills | cc-steuerung ist Modalität (WIE), der Fachskill bleibt für das WAS zuständig; beide dürfen gleichzeitig aktiv sein |

Konflikte mit Skills von Anthropic, die `plugin eval` nicht lädt, prüfen echte Sitzungen
([quality/real-environment/README.md](./quality/real-environment/README.md)):

| Paar | Entscheidung |
|---|---|
| skill-neu, skill-pflege ↔ skill-creator | Skills dieses Repos anlegen oder ändern → skill-neu bzw. skill-pflege |
| skill-auswertung ↔ skill-creator | Zündungen aus dem echten Alltag (Skill-Log) → skill-auswertung; künstliche Testläufe und Benchmarks eines Skills → skill-creator |
| audit ↔ code-review | Doku gegen Code prüfen → audit; Code-Review eines Diffs → code-review |
| cc-steuerung ↔ Claude Code | In Claude Code löst cc-steuerung nie aus |

---

## Wo die gemeinsamen Regeln stehen

| Thema | Regelquelle |
|---|---|
| Fragen nur bei offener Entscheidung, als Auswahlfrage | [docs/skill-quality.md](./docs/skill-quality.md), Zusammenspiel; je Skill der Abschnitt „Grundsätze“ |
| Branch, Push, Version, Checks, Projektwerte | Skill-Profil der `CLAUDE.md` ([docs/skill-profile-v1.md](./docs/skill-profile-v1.md)); ohne Profil der Rückfall im jeweiligen Skill |
| Aufbau, Neutralität, Beschreibung eines Skills | [docs/skill-quality.md](./docs/skill-quality.md) |
| Skills ändern ohne stillen Regelverlust | [skills/skill-pflege/SKILL.md](./skills/skill-pflege/SKILL.md) (Safe Patch, Refactor mit Regel-Inventar unter `docs/skill-refactors/`) |
| Lieferung an claude.ai (Repo und Upload) | [skills/skill-pflege/references/delivery.md](./skills/skill-pflege/references/delivery.md) |
| Desktop Commander, Arbeitsverzeichnis, PowerShell im Cowork-Chat | [skills/cc-steuerung/SKILL.md](./skills/cc-steuerung/SKILL.md) und `references/desktop-commander.md` |
| Quittung und Batch-Protokoll bei ClickUp-Aufgaben | [skills/tracker/SKILL.md](./skills/tracker/SKILL.md) und `references/batch-protocol.md` |
| Memory-Rubriken (Cowork) | [MEMORY-RUBRIKEN.md](./MEMORY-RUBRIKEN.md); chat-wechsel übernimmt sie in den Übergabe-Prompt |
| Fragilitäten und Frühwarn-Indikatoren | [docs/fragilitaeten-und-fruehwarn.md](./docs/fragilitaeten-und-fruehwarn.md); chat-wechsel prüft sie bei der Übergabe |
| Projektregeln (z. B. Frühphase ohne Migration) | Doku des Projekts; die Skills lesen sie über das Skill-Profil |
| Messung: Routing-Eval, echte Sitzungen, Grundmessung | [quality/README.md](./quality/README.md), [quality/baseline/grundmessung-2026-09.md](./quality/baseline/grundmessung-2026-09.md) |

---

## Projektwerte

Die Skills sind projektneutral. Werte eines Projekts – Pfade, IDs, Präfixe, Befehle, Branch, Push – stehen im Block
`## Skill-Profil` der `CLAUDE.md` des jeweiligen Repos, große Strukturen unter `.claude/skill-config/`. Fehlt ein Wert,
fragt der Skill nur nach diesem Wert; ein ganzes Profil legt er nur mit Zustimmung an
([docs/skill-profile-v1.md](./docs/skill-profile-v1.md), „Fehlende Werte“).

Bis zum Ende des Umbaus lesen einzelne Skills noch ältere Quellen: die früheren Profil-Abschnitte der `CLAUDE.md`
(Tracker-, Code-, Doku-, Mockup-, Review-Profil) und `projects/<name>/` (tracker). Die Werte des Space „Claude Skills
Entwicklung“ stehen in `.claude/skill-config/tracker.md`.

---

## Andere Skill-Sammlungen

- [obra/superpowers](https://github.com/obra/superpowers) — Workflow-Skills
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) — Engineering- und Marketing-Skills
- Anthropic skill-creator — Referenz, eingebettet unter `reference/anthropic-skill-creator/`
