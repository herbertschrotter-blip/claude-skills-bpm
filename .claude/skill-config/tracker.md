# Tracker-Konfiguration – Skill-Repo

Für den Skill tracker (Skill-Profil → Tracker): der ClickUp-Space „Claude Skills Entwicklung“ mit der Liste
ClaudeSkills und den Skill-Issue-Listen. Die Werte standen bis 24.09.2026 in `projects/bpm/clickup-lists.md` und
`clickup-fields.md` und stehen jetzt nur hier.

## Inhalt

- Provider
- Nummernschema und nächste freie Nummer
- Listen und Routing
- Statusmodell
- Felder und Option-IDs
- Titel- und Beschreibungsformat
- Quittungsformat
- Sonderfälle

## Provider

ClickUp · Workspace `90152410319` · Space „Claude Skills Entwicklung“ `901510833068`

## Nummernschema und nächste freie Nummer

| Liste | Schema | Nächste freie Nummer |
|---|---|---|
| ClaudeSkills | keine Nummern; Name `📦 <Vorhaben> · Phase <N> — <Kurztitel>` bzw. `P<N> — <Kurztitel>` | – |
| Skill-Issues | `<skill>-NNN: <Kurztitel>`, dreistellig, eigener Zähler je Skill ab 001, Lücken nicht füllen; die Issue-ID steht zusätzlich im Feld `Issue-ID` | höchste vergebene Nummer der Liste (auch geschlossene Aufgaben) + 1 |

## Listen und Routing

| Zweck | Liste | ID |
|---|---|---|
| Umbau-, Plan- und Meta-Aufgaben zum Skillsystem | ClaudeSkills (direkt im Space) | `901522935159` |
| Issues je Skill (Bug, Auslöse-Fehler, Doku-Fehler, Verbesserung, Refactor-Idee) | Ordner „Skill Issues“ | `901515724728` |

Skill-Issue-Listen:

| Skill | Liste |
|---|---|
| audit | `901522952203` |
| cc-steuerung | `901522952208` |
| chat-wechsel | `901522952212` |
| chatgpt-review | `901522952221` |
| code-erstellen | `901522952225` |
| doc-pflege | `901522952230` |
| git-commit-helper | `901522952231` |
| mockup-erstellen | `901522952236` |
| skill-neu | `901522952243` |
| skill-pflege | `901522952246` |
| tracker | `901522952249` |
| ticket | fehlt – Liste im Ordner „Skill Issues“ anlegen, bevor das erste ticket-Issue entsteht |

Routing: `tracker issue <skill>: …` → Liste des Skills; alles zum Umbau und zum Skillsystem als Ganzes → ClaudeSkills.
Unbekannter Skill-Name → Auswahlfrage mit den Namen oben, nie raten.

## Statusmodell

| Liste | offen | in Arbeit | erledigt |
|---|---|---|---|
| ClaudeSkills | `open` | `in progress` | `done` |
| Skill-Issues | `to do` | `in progress` | `complete` |

Status immer kleingeschrieben.

## Felder und Option-IDs

### ClaudeSkills – 10 Felder (dieselben IDs wie im BPM-Space)

| Feld | ID | Typ | Wann |
|---|---|---|---|
| Typ | `f7b8c62a-0783-4b6d-9a95-0ce861eae2ad` | Dropdown | neu |
| Aufwand | `ecc194e5-2c67-46a7-b4d1-177ce3512c10` | Dropdown | neu |
| Zielversion | `1fcc0b5a-082c-4c2a-8238-f7ff31b560d4` | Kurztext | neu |
| Komponente | `b0f37cca-c325-4ac6-9bb8-407c65e4611a` | Kurztext | neu |
| Zugehörige Docs | `421cf05a-d02a-40b9-aca7-1dc086536f36` | Text | neu |
| Commit ID | `a851a04d-f34a-429f-abce-bec0b0b6859f` | Kurztext | erledigt |
| Commit Text | `cae9f6cb-e0eb-44aa-81f8-df2e1194111e` | Text | erledigt |
| Erledigt | `457bde4f-c9c1-40ab-b464-897b7f87e6bc` | Datum | erledigt |
| Chat-Anker temp | `fef35671-3752-4bf2-bcb8-f29482d3a2d7` | Kurztext | neu |
| Chat-Anker erstellt | `512b8920-e958-4e43-826e-110e3bccdfc2` | Kurztext | neu |
| Chat-Anker erledigt | `0c72a2ea-630e-4320-9cdb-80a19bc5ebb6` | Kurztext | erledigt |

Typ: Feature `5f4be01a-1b85-42ef-a987-b8ffb16ecdc1` · Fix `00bb1941-b0a4-4eaf-96c9-116b2a57a8d6` · Refactor
`aa48cd2f-a319-4abf-b6ba-9bbe6f44e2c7` · Perf `976b3664-5973-4922-8287-4a63101e0c2d` · Docs
`12a547b2-4ebc-4caa-8527-023c66e9f111` · Konzept `1291a46f-feab-4596-8762-3872e51ee327` · Meta
`d60891c6-129f-4b99-9e6f-043940541a22`

Aufwand: S (<1h) `805fd010-b820-46b1-acaa-8b2e047904e6` · M (1-4h) `0298c9b6-9116-4c9e-bb74-d78a41bfe975` · L (halber
Tag) `7646181a-b2ff-4eaa-a61b-0d378c0e91d3` · XL (>1 Tag) `6b7587cc-2031-44c4-8b95-74a2d73c87a7`

### Skill-Issues – 6 Felder

| Feld | ID | Typ |
|---|---|---|
| Issue-ID | `e286a04a-d79b-481a-8ee4-9c9401a87bfc` | Kurztext (`<skill>-NNN`) |
| Typ | `5b45b13a-a866-4a5a-83e2-eea2ea1128b8` | Dropdown |
| Commit-Hash | `8e8879f7-5741-4af9-9a4a-708eff59ca87` | Kurztext |
| Beobachtungs-Chat | `eb1f6eb6-8fcf-4b73-b7aa-ffd81f2db0fe` | Kurztext |
| Chat-Anker erstellt | `512b8920-e958-4e43-826e-110e3bccdfc2` | Kurztext |
| Chat-Anker erledigt | `0c72a2ea-630e-4320-9cdb-80a19bc5ebb6` | Kurztext |

Typ: Bug `2519a0e3-5ef4-4913-96b9-6a297343326d` · Trigger-Fehler `9e98787e-8956-4212-86ed-789276f4aa3e` · Doku-Fehler
`d1116505-fd85-4283-bab8-9e657e6ea833` · Verbesserung `6fcb6a19-d22e-4a36-b3f2-047523e41ad6` · Refactor-Idee
`3dfdb7a5-39b1-433d-b550-dc05a371de47`

## Titel- und Beschreibungsformat

- ClaudeSkills: Beschreibung nach dem Template des Skills tracker; für Umbau- und Meta-Aufgaben kurz: Problem,
  Lösungsansatz (Checkliste), Abnahme, Bezug.
- Skill-Issues: Ablauf und Beschreibung nach tracker `references/issue-task.md`.

## Quittungsformat

`✅ <Name oder Issue-ID> — [BPM-ANCHOR-<task-id>] — <aktion>: <kurz>`

Der Anker-Präfix ist in diesem Space historisch `BPM-ANCHOR`. Die Felder „Chat-Anker erstellt“ und „Chat-Anker erledigt“
bekommen denselben Text mit ASCII-Bindestrich statt Gedankenstrich.

## Sonderfälle

- Kein Gedankenstrich `—` in Feldwerten (ClickUp lehnt sonst ab).
- Option-IDs nie raten; bei unbekanntem Wert Auswahlfrage mit den Optionen oben.
