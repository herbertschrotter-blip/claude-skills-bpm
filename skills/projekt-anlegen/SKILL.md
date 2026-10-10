---
name: projekt-anlegen
description: >
  Legt neue Projekte an und richtet bestehende Repos für die Skills ein. Klärt
  Zweck, Ort und erste Fassung, prüft den Bestand und erzeugt für unterstützte
  Stacks ein lauffähiges, getestetes Grundgerüst ohne Fachlogik. Erstellt oder
  klont nach Rückfrage GitHub-Repos und richtet das Skill-Profil ein. Use when
  users want to start, scaffold, anlegen, aufsetzen or einrichten a new project,
  HA integration, card, dashboard or Python tool, say "neues Projekt" or "ich
  will X bauen, weiß aber nicht wie", want a GitHub repo created or cloned, or
  an existing repo eingerichtet for these skills (Skill-Profil, Configs). Do not
  trigger for changes in existing projects (code-erstellen), UI mockups
  (mockup-erstellen), new or changed skills (skill-neu, skill-pflege), ClickUp
  tasks (tracker), documentation only (doc-pflege), or git-only operations.
---

# projekt-anlegen – neue Projekte anlegen und einrichten

## Zweck

Ein neues Projekt beginnt oft mit einer halben Idee. Dieser Skill führt von der Idee zu einem eingerichteten Projekt:
klären, was es werden soll, prüfen, ob es das schon gibt, entscheiden, wo es lebt, ein lauffähiges Grundgerüst
erzeugen und eintragen. Danach übernehmen die Fachskills.

- **Grenzen:** Dieser Skill erzeugt technische Funktionsfähigkeit: Start, Verbindung der Schichten, Konfiguration,
  Tests und Prüfungen, gegebenenfalls eine neutrale Datenhaltung, dazu Repo, Profil und Eintrag. Fachliches Verhalten
  schreibt code-erstellen – jede Funktion, deren Ergebnis aus den Anforderungen des konkreten Projekts folgt. Enthält
  ein Auftrag beides, entsteht zuerst das Grundgerüst, dann übernimmt code-erstellen. Entwürfe macht mockup-erstellen,
  Doku pflegt doc-pflege, Aufgaben legt tracker an.
- **Bestehende Projekte** gehören nicht hierher. Wer in einem vorhandenen Projekt etwas ergänzt, braucht code-erstellen.
  Ausnahmen: ein bestehendes Repo zum ersten Mal an einen Ort holen und einrichten (klonen) und ein bestehendes Repo
  für die Skills einrichten (Abschnitt „Bestehendes Repo einrichten“).
- **Prüfen** eines Projekts gegen seine Regeln macht audit.

## Benötigte Werte

Aus dem Skill-Profil der `CLAUDE.md` des Repos, in dem die Sitzung läuft (`docs/skill-profile-v1.md` im Skill-Repo):

| Feld | Wofür | Fehlt es |
|---|---|---|
| `Projekte.Ablage` | Ordner für neue Projekt-Repos | Auswahlfrage nach Profil-Regel „Fehlende Werte“ |
| `Projekte.Übersicht` | Datei, in der Projekte eingetragen werden | `none` ist gültig; dann entfällt das Eintragen |
| `Projekte.GitHub-Owner` | Besitzer für neue GitHub-Repos | nur gefragt, wenn GitHub gewählt wird |
| `Projekte.Geschützt` | Bereiche, die Claude nicht ändert | `none` ist gültig |
| `Code.Stacks` | Stack der Umgebung, bestimmt die Reference | pro Projekt fragen |
| `Modul.Grundsatzregeln` | fachliche Regeln für Module eines Stacks | `none` ist gültig |

Das neue Projekt bekommt `Doku.Entscheidungs-Ort` in seinem eigenen Profil; dort stehen seine Grundentscheidungen
(`references/grundsatz.md`).

Fehlt das Profil ganz, schlägt der Skill eines mit Werten aus der Umgebung vor und legt es erst nach Zustimmung an. Nie
einen Pfad oder Owner raten.

## Ablauf

Jeder Übergang zum nächsten Schritt läuft über eine Auswahlfrage. Was der Auftrag schon beantwortet, wird nicht noch
einmal gefragt.

### 1. Klären, was es werden soll

Pflicht sind drei Klärungen: Was soll es tun? Wo soll es laufen? Was soll die erste Fassung können (und was
ausdrücklich nicht)? Was der Auftrag schon sagt, wird nicht gefragt. Was Claude selbst nachsehen kann (vorhandene
Integrationen, Geräte, Entitäten, Dateien), sieht es nach, statt zu fragen. Technische Entscheidungen (Datenbank,
Oberfläche, Bausteine) leitet Claude daraus ab und erklärt sie im Plan, statt sie abzufragen. Fragen in Alltagssprache
und weitere Fragen nur bei Bedarf: `references/grundsatz.md`.

Für „Was soll es tun?“: Auswahlfrage mit den Arten, die der Stack kennt (Liste in der Stack-Reference), dazu immer
„weiß ich noch nicht“; dann die Idee in wenigen Fragen schärfen (`references/grundsatz.md`).

Daraus einen Vorschlag für die Art ableiten und kurz begründen. Die Stack-Reference sagt, welche Art für welchen Zweck
die einfachste ist; die einfachste passende Art gewinnt. Ist nur das Aussehen offen, mockup-erstellen anbieten, bevor
etwas angelegt wird.

### 2. Bestand prüfen

- In der Übersicht und in der Ablage nach ähnlichen Namen und Zwecken suchen.
- Nennt der Nutzer ein vorhandenes Repo oder gibt es eines auf GitHub: klonen statt neu anlegen (`references/github.md`).
- Gibt es das Projekt schon an diesem Ort: nicht anlegen, sondern auf code-erstellen verweisen.
- Soll ein vorhandenes System angebunden werden (Gerät, Dienst, Datenbank), gehört das in die Grundentscheidungen.

### 3. Ort und Quelle der Wahrheit festlegen

- **Eigenes Repo** in `Projekte.Ablage/<name>`, wenn das Projekt eigenen Code, eigene Versionen oder eine eigene
  Veröffentlichung hat (z. B. eine Integration oder eine Karte, die über HACS verteilt wird).
- **Ordner im aktuellen Repo**, wenn es nur Konfiguration ist, die zur Umgebung gehört (z. B. ein Paket mit
  Automationen). Welche Art wohin gehört, steht in der Stack-Reference.
- **Genau eine Quelle der Wahrheit.** Liegt dasselbe Projekt schon woanders (anderer PC, GitHub), wird festgelegt, wo
  gearbeitet wird und wie der Stand an die anderen Orte kommt (Pull, Push, Auslieferung). Zwei Orte, an denen parallel
  geändert wird, sind der häufigste Grund für verlorene Arbeit.
- **Auslieferung:** Wenn das Projekt woanders läuft, als es entwickelt wird, wird der Weg dorthin festgelegt und später
  als `Code.Auslieferung` ins Profil des Projekts geschrieben.
- Nichts in `Projekte.Geschützt` anlegen oder ändern.

### 4. Plan zeigen

Kurz und vollständig: Name, Art, Ort, Ordnerbaum mit Dateien, Git ja/nein, GitHub ja/nein (Sichtbarkeit), die Werte für
das Skill-Profil des neuen Projekts, Einträge an anderen Stellen (Übersicht, Registrierung in der Umgebung). Dazu die
Grundentscheidungen und die abgeleitete Technik in Alltagssprache (z. B. „Daten bleiben auf diesem Gerät, in einer
kleinen Datenbankdatei“) und welche Prüfungen vor dem Anlegen laufen. Der Plan ist für den Nutzer geschrieben: die
Grundentscheidungen zuerst, Erklärungen im Ordnerbaum ohne Fachbegriffe (keine Manifest-Felder, Paket- oder
Werkzeugnamen); die stehen danach im Projekt. Auswahlfrage: anlegen / anpassen / abbrechen.

### 5. Erzeugen

- **Unterstützte Kombination** (Liste in `references/generator.md`): Claude baut den Erzeugungsauftrag, der Generator
  erzeugt das Grundgerüst in einen Zwischenordner, prüft es (Werkzeuge einrichten, Formatierung, Lint, Tests, Start)
  und stellt es erst bei Grün an seinen Platz. Bei Rot entsteht nichts; Claude meldet den Schritt und die Ursache.
  Ergebnis als Tabelle Prüfung / Dauer / Ergebnis. Ablauf, Aufruf und Grenzen: `references/generator.md`.
- **Sonst** Ordner und Grunddateien nach der Stack-Reference. Nur das Gerüst: lauffähige Minimalfassung, keine
  Fachlogik.
- **Testgerüst parallel-fähig**, wenn der Stack einen Testläufer mit Parallelbetrieb hat (Stack-Reference): Die Zahl
  der Worker misst der Testläufer zur Laufzeit, nie fest eintragen. Kein Test beeinflusst einen anderen (eigener
  temporärer Ordner bzw. eigene Datenbank je Test, bei einer Server-Datenbank Kennung je Lauf und Worker). Versionen der Testwerkzeuge angeheftet. Der Testbefehl kommt mit
  Pfad-Mustern unter `### Checks` ins Skill-Profil und unter `Pre-Commit-Checks`. Der Generator baut das selbst ein.
- Zur Info Kerne und Speicher der Maschine einmal nennen (z. B. `nproc`, `free -h`); nichts davon ins Profil.
- Bei eigenem Repo: `git init`, `.gitignore` nach Stack, `README.md`, `CHANGELOG.md`, `CLAUDE.md` mit Skill-Profil
  (Grundfelder, Commit, Code, Doku; unbekannte Werte als `fehlt`, bewusst leere als `none`). Beim Generator liefert
  das der Baustein; Claude ergänzt danach Zweck und Grenzen in den Grundentscheidungen. Ohne Generator legt Claude
  die Grundentscheidungen selbst in `docs/entscheidungen.md` an und trägt sie als `Doku.Entscheidungs-Ort` ein, nie
  `none`.
- Erster Commit im Format von git-commit-helper, erst wenn die Prüfungen grün sind. Pushen nur nach der Push-Policy
  des neuen Profils.
- GitHub nur nach Auswahlfrage: erstellen (privat als Standard) / später / nie, erst nach dem lokalen Anlegen. Ablauf in
  `references/github.md`; bei GitHub nimmt der Generator die automatische Prüfung (CI) mit auf.
- Registrierung in der Umgebung (z. B. ein Dashboard in einer zentralen Konfigurationsdatei): nur, wenn die Datei nicht
  geschützt ist, und immer mit eigener Rückfrage, weil sie den laufenden Betrieb betrifft.
- Keine Geheimnisse in Dateien. Zugangsdaten gehören in den dafür vorgesehenen Ort des Stacks, nie ins Repo.

### 6. Eintragen und übergeben

- Das Projekt mit einer Zeile in `Projekte.Übersicht` eintragen: Name, Art, Ort, Quelle der Wahrheit, Repo.
- Zusammenfassung: was angelegt wurde, Ergebnis der Prüfungen, was noch `fehlt` im Profil, was der Nutzer selbst tun
  muss (z. B. Neustart).
- Nächsten Schritt per Auswahlfrage anbieten: Entwurf (mockup-erstellen) / erste Funktion (code-erstellen) / Aufgaben
  anlegen (tracker) / fertig.

## Bestehendes Repo einrichten

Für ein Repo, das es schon gibt und in dem die Skills arbeiten sollen, dessen `CLAUDE.md` aber kein oder nur ein
unvollständiges `## Skill-Profil` hat („richte die Skills hier ein“, „leg das Skill-Profil an“). Kein Gerüst, keine
Grunddateien, kein GitHub – nur Profil und Configs. Jeder Schritt läuft wie oben über eine Auswahlfrage.

1. **Repo lesen:** `CLAUDE.md`, `README.md`, Build- und Testdateien (z. B. `package.json`, `*.csproj`, `pyproject.toml`,
   `Makefile`), Versionsquelle (`CHANGELOG.md`, Manifest), Branches, Stil der letzten Commits, `docs/`.
2. **Bereiche wählen:** Auswahlfrage mit Mehrfachauswahl, welche Skills dort arbeiten sollen (Code, Doku, Commits,
   Tracker, Tickets, Mockups, Reviews). Die Pflichtfelder je Skill stehen in `docs/skill-profile-v1.md`.
3. **Vorschlag zeigen:** das Skill-Profil v1 für die gewählten Bereiche mit den erkannten Werten und ihrer Herkunft
   (Datei); Unbekanntes als `fehlt`, bewusst Leeres als `none`. Dazu die Configs unter `.claude/skill-config/`, die die
   Bereiche brauchen (z. B. `tracker.md` mit Listen, Status und Feldern aus dem Tracker gelesen), in der Gliederung aus
   `docs/skill-profile-v1.md`. Auswahlfrage: anlegen / anpassen / abbrechen.
4. **Anlegen:** Den Profil-Block an die `CLAUDE.md` anhängen; vorhandener Text bleibt. Steht ein Wert schon als Prosa
   oder in einem älteren Profil-Abschnitt, die Stelle nennen und per Auswahlfrage klären, ob sie auf das Profil verweist
   oder bleibt (Werte genau einmal). Commit im Format des neuen Profils, Push nach seiner Push-Policy.
5. **Übergeben:** Zusammenfassung, welche Felder noch `fehlt` sind und welcher Skill sie braucht; zur Info Kerne und
   Speicher der Maschine; nächsten Schritt wie oben anbieten.

## Stacks

Die Arten, Orte, Grunddateien und `.gitignore` eines Stacks stehen in `references/stacks/<key>.md`; der Schlüssel kommt
aus `Code.Stacks`. Geladen wird nur die genannte Datei. Welche Arten der Generator schon erzeugt, steht in
`references/generator.md`.

- Home Assistant: `references/stacks/home-assistant.md`
- Python: `references/stacks/python.md`

Gibt es für einen Stack keine Reference, fragt der Skill nach Art und Grunddateien und legt nur das an, was der Nutzer
bestätigt. Keine Vorlagen erfinden. Eine Kombination, die der Generator nicht kennt, wird nicht improvisiert: dann gilt
der Weg nach der Stack-Reference.

## VERBOTEN

- Anlegen ohne gezeigten und bestätigten Plan
- Ein Projekt ein zweites Mal anlegen, wenn es das schon gibt
- Dateien in `Projekte.Geschützt` anlegen, ändern oder löschen
- Ein GitHub-Repo erstellen oder pushen ohne Auswahlfrage bzw. gegen die Push-Policy
- Tokens, Passwörter oder andere Geheimnisse in Dateien, Befehlen oder Commits
- Einen Pfad, Owner oder Stack raten
- Fachlogik schreiben – das Gerüst endet mit technischer Funktionsfähigkeit; Fachliches macht code-erstellen
- Beim Einrichten eines bestehenden Repos vorhandenen Text der `CLAUDE.md` überschreiben oder still entfernen
- Ein Projekt mit roter Prüfung als angelegt melden oder den Generator in ein vorhandenes Ziel schreiben lassen
- Ohne ausführbare Umgebung (z. B. bei claude.ai) eine Erzeugung behaupten – dort entsteht nur der Plan
- Ein neues Projekt ohne Grundentscheidungen anlegen (`Doku.Entscheidungs-Ort` leer oder `none`)

## VERWEIS

- Generator (Aufruf, Erzeugungsauftrag, unterstützte Kombinationen, Prüfung): `references/generator.md`
- Grundsatz-Prüfung und Fragen in Alltagssprache: `references/grundsatz.md`
- GitHub (erstellen, klonen, Anmeldung): `references/github.md`
- Stack Home Assistant: `references/stacks/home-assistant.md`
- Stack Python: `references/stacks/python.md`
- Skill-Profil und fehlende Werte: `docs/skill-profile-v1.md` im Skill-Repo
- Commit-Format: git-commit-helper. Code: code-erstellen. Entwürfe: mockup-erstellen. Aufgaben: tracker.
- Im Cowork-Chat laufen Datei- und Shell-Aktionen über cc-steuerung; der Ablauf bleibt gleich.
