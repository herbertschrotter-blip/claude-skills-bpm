# Ausgangsbefund ChatGPT – Analyse der 12 Skills (vor Runde 1)

**Quelle:** ChatGPT, eigene Analyse von `herbertschrotter-blip/claude-skills-bpm` (Branch `main`), von Herbert am 2026-09-24
in die Claude-Code-Sitzung eingefügt. Anlass der Serie CGR-2026-09-24-skillsystem. Wortlaut unverändert übernommen;
nur Überschriften, Tabellen und Dateibäume als Markdown gesetzt.

---

Ich habe herbertschrotter-blip/claude-skills-bpm auf main durchgesehen – die 12 Skills, die zentralen Repo-Regeln, die vorhandenen Evals und auch euren eingebetteten Anthropic-skill-creator als Referenz.
Das System ist konzeptionell schon weit: klare Zuständigkeiten, Profile statt vollständig hartkodierter Projektlogik, Progressive Disclosure beim tracker, Negativ-Trigger und echte Workflow-Regeln. Die größten Probleme liegen inzwischen nicht mehr in fehlenden Regeln, sondern im Gegenteil in Regelwachstum, Überschneidungen und teilweise widersprüchlichen Invarianten.

## Die wichtigsten Repo-weiten Befunde

| Priorität | Befund | Einschätzung |
|---|---|---|
| 🔴 | Repo hat 12 Skills, README.md und INDEX.md behaupten weiterhin 11 | echter Fehler / Drift |
| 🔴 | git-commit-helper pusht standardmäßig, cc-steuerung sagt ausdrücklich „User pusht immer selbst“ | echter Cross-Skill-Widerspruch |
| 🔴 | PowerShell-Commitsequenz benutzt ;, behauptet aber bei Fehlern abzubrechen | funktionaler Fehler |
| 🔴 | doc-pflege und audit beanspruchen beide read-only Doku-/Frontmatter-Validierung | Routing-Konflikt |
| 🔴 | skill-pflege verhindert strukturelle Verbesserung praktisch selbst | langfristiges Architekturproblem |
| 🟠 | Mehrere SKILL.md liegen über Anthronics empfohlenen ~500 Zeilen | Progressive Disclosure nicht konsequent |
| 🟠 | skill-neu erklärt test-prompts.md für jeden Skill zur Pflicht, vorhanden ist es nur bei 2 Skills | Repo-Regel ↔ Realität inkonsistent |
| 🟠 | Eval-Abdeckung ist für ein Routing-System zu gering | Regressionen werden schwer erkannt |
| 🟠 | Globale Toolnamen-/Auswahlfrage-Regeln widersprechen teilweise dem Ziel „umgebungsneutral“ | unnötig fragil |
| 🟡 | Projektneutralität ist eher „profilbasiert multi-project“ als wirklich neutral | Benennung/Architektur präzisieren |

Anthropics Referenz in reference/anthropic-skill-creator/SKILL.md nennt als Ideal: SKILL.md unter ungefähr 500 Zeilen, große Details in references/, Beschreibung als primären Triggermechanismus und iterative Evals. Genau dort würde ich bei eurem nächsten Refactor ansetzen.

## 1. audit

Zweck: Read-only-Prüfer, der Code, Dokumentation, Aufgabenquelle und Projektprofile gegeneinander verifiziert.
Der Grundgedanke ist sehr gut. Besonders richtig ist, dass audit keine eigene Projektwahrheit erfinden soll, sondern Prüfregeln aus Doku-/Code-Profil und Stack-Referenzen ableitet. Dadurch kann derselbe Skill BPM und Heidi prüfen.
Das Hauptproblem ist die Abgrenzung zu doc-pflege. audit sagt ausdrücklich, Frontmatter, Quickload und formale Doku zu validieren. doc-pflege Modus 6 sagt praktisch dasselbe und triggert sogar auf „prüfe frontmatter“, „quickload check“ und „prüfe die doku“. Das sind zwei Skills mit derselben Nutzerabsicht.
Ich würde die Trennung hart machen:

| Aufgabe | Zuständig |
|---|---|
| „Prüfe / analysiere / finde Inkonsistenzen“ | audit |
| „Korrigiere / aktualisiere / repariere Docs“ | doc-pflege |
| doc-pflege vor dem Schreiben intern validiert | interne Prüfung, aber kein öffentlicher Validierungsmodus |

Damit könnte doc-pflege Modus 6 stark verkleinert und als interne Post-Write-Validation behandelt werden.
Weitere Verbesserung: Die BPM- und Heidi-Prüfkataloge gehören zunehmend in Projektprofile oder references/, nicht in den Kernskill. Sonst wird audit bei Projekt 3, 4 und 5 wieder wachsen.
Fazit: Inhaltlich stark, Routinggrenze korrigieren.

## 2. cc-steuerung

Zweck: Modalität – wie eine Fachaufgabe direkt auf Herberts Rechner ausgeführt wird.
Die Trennung WAS = Fachskill / WIE = cc-steuerung ist eine der besten Architekturentscheidungen im Repo.
Es gibt aber einen wichtigen Trigger-Widerspruch. Das Frontmatter sagt sinngemäß: nicht triggern ohne explizite CC/DC-Absicht. Im Body steht dagegen:
Nach Konzeptfreigabe wie „mach“, „ok“, „passt“ wird DC automatisch Default.

Das sind zwei unterschiedliche Triggerregeln. Ein Skill wird hauptsächlich über seine Description ausgewählt; der Body kann einen Skill, der gar nicht geladen wurde, nicht nachträglich aktivieren.
Ihr müsst euch entscheiden. Für euren Workflow scheint die Body-Regel gewollt zu sein. Dann müsste die Description ungefähr ausdrücken:
Use when direct execution on the user's PC is requested or when an already discussed implementation is approved for execution and Desktop Commander is available.

Außerdem ist die Regel „User pusht immer selbst“ wichtig – und wird momentan von git-commit-helper verletzt.
Die vielen konkreten Toolnamen (ask_user_input_v0, Desktop Commander, ToolSearch etc.) machen den Skill zusätzlich empfindlich gegenüber Plattformänderungen. Das operative Mapping darf gern in einer Reference stehen, während SKILL.md eher semantisch beschreibt: „verwende das Auswahlwerkzeug der aktuellen Umgebung“.
Fazit: Sehr gutes Konzept, Description muss an tatsächliches Verhalten angepasst werden.

## 3. chat-wechsel

Mit 571 Zeilen ist dieser Skill bereits größer als Anthronics Idealbereich.
Sein ursprünglicher Job wäre klar: den Zustand einer Sitzung so aufbereiten, dass die nächste Sitzung ohne Informationsverlust weiterarbeiten kann.
Inzwischen macht er aber sehr viel mehr: ClickUp lesen, erledigte Tasks erkennen, neue Tasks erkennen, Taskstatus ändern, Memory scannen, Memory-Einträge verwalten, Chat-Anker behandeln, Links prüfen, teilweise doc-pflege Modus 8 anstoßen und dann den Handover-Prompt bauen.
Das erzeugt eine problematische Eigenschaft: Ein scheinbar harmloser Wunsch wie „machen wir in einem neuen Chat weiter“ kann einen ganzen Session-Abschlussprozess mit externen Änderungen auslösen.
Besser wäre:
chat-wechsel/SKILL.md = Orchestrator + Handover-Schema.
Die detaillierten Mechaniken gehören etwa nach:

```
references/
  clickup-handover.md
  memory-handover.md
  anker-handover.md
  link-check.md
  claude-code-session-close.md
```

Dabei würde ich ClickUp-Mutationen vollständig an tracker delegieren. chat-wechsel stellt nur fest: „Diese 2 Tasks scheinen erledigt“. Der Tracker entscheidet und führt aus.
Fazit: Funktioniert wahrscheinlich gut, ist aber zu einem Session-Management-Monolithen geworden.

## 4. chatgpt-review

Auch dieser Skill liegt mit etwa 548 Zeilen oberhalb des sinnvollen Kernumfangs.
Die eigentliche Fähigkeit ist hervorragend definiert: strukturierte Cross-LLM-Reviewgespräche mit sauberem Projektkontext und iterativen Runden. Das passt zu eurer Arbeitsweise sehr gut.
Was unnötig viel Raum frisst, ist das komplette CGR-Archivsystem einschließlich Serien-ID, Checkpoints, Runde starten, abschließen, retroaktive Nutzung usw. Das ist klassische Progressive-Disclosure-Information.
Ich würde den Kern auf vier Dinge reduzieren:
Trigger → Kontext laden → Reviewprompt erstellen → Antwort in nächste Runde überführen.
CGR-Archivierung dann in references/cgr-lifecycle.md.
Die Pflicht zur Push-Prüfung vor jedem Prompt ist außerdem nur dann nötig, wenn ChatGPT tatsächlich über GitHub den aktuellen Stand sehen soll. Für rein textbasiertes Review sollte sie nicht pauschal gelten.
Positiv: chatgpt-review ist vom chat-wechsel semantisch sauber getrennt.
Fazit: Inhalt gut, starkes Split-Potenzial.

## 5. code-erstellen

Das ist zurecht euer Master-Orchestrator. Das Modell „Projektprofil + Stackreference + Impact Check + Tests + Auslieferung“ ist solide.
Mit etwa 524 Zeilen ist auch er über die sinnvolle Kernlänge hinausgewachsen, obwohl ihr bei den Stackdetails bereits vorbildlich references/stacks/ verwendet.
Ich würde noch mehr auslagern. Insbesondere Auto-Anker, ausführliche Cowork-/DC-Ausgabevarianten und projektbezogene Spezialfälle müssen nicht ständig im Kontext stehen.
Ein wichtiger Architekturpunkt: code-erstellen sollte Code bauen, nicht sämtliche nachgelagerten Lebenszyklusaufgaben selbst übernehmen. Commit, Dokumentation und Tracker sind gute Hooks, aber sollten als Ergebniszustand ausgegeben werden:
Code fertig → Tests grün → Doc-Hints X → Commit-Vorschlag Y → Task Z könnte abgeschlossen werden.

Dann nur bei Nutzerabsicht wirklich delegieren.
Dadurch wird der Orchestrator weniger „magisch“.
Fazit: Einer der stärksten Skills; Kern entschlacken.

## 6. doc-pflege

Mit 467 Zeilen formal noch innerhalb der Anthropic-Empfehlung, inhaltlich aber bereits sehr breit.
Acht Modi sind viel. Besonders Modus 6 — Validierung kollidiert direkt mit audit.
Auch Modus 8 — Sitzungsabschluss ist eigentlich Workflow-Orchestrierung und überschneidet sich mit chat-wechsel. Das kann funktionieren, solange klar ist:
doc-pflege persistiert den Dokumentationsstand.
chat-wechsel erzeugt die Übergabe.

Diese Trennung sollte noch deutlicher werden.
Bei Modus 7 ist die harte Regel „beim Refactoring darf nichts gelöscht oder gekürzt werden“ zu absolut. Bei Dokumentationsrefactoring gehört Redundanz entfernen, veraltete Inhalte ersetzen und Aussagen konsolidieren gerade zur Arbeit. Was ihr wirklich schützen wollt, ist fachlicher Informationsverlust.
Die bessere Invariante wäre:
Keine fachlich relevante Information darf ohne explizite Entscheidung verloren gehen.

Das erlaubt echte Verbesserung, ohne Inhalt versehentlich zu zerstören.
Fazit: Gute Profilarchitektur; Validierung an audit abgeben und „kein Löschen“ semantischer formulieren.

## 7. git-commit-helper

Hier habe ich zwei echte Bugs gefunden.
Erstens sagt cc-steuerung:
User pusht immer selbst.

git-commit-helper liefert standardmäßig:
git add ... ; git commit ... ; git push origin ... ; git log ...
Das widerspricht sich unmittelbar.
Zweitens schreibt der Skill für PowerShell:
cmd1 ; cmd2 ; cmd3
und behauptet später, die Sequenz würde bei einem Fehler abbrechen.
Das tut ; nicht. Der Folgebefehl wird ausgeführt, auch wenn der vorherige externe Prozess einen Fehlercode liefert. Bei Bash ist && korrekt; bei PowerShell muss das ebenfalls explizit abgesichert werden.
Ich würde ohnehin Commit und Push trennen:
git add ...
git commit ...
git log ...
Push ausschließlich dann, wenn der User ausdrücklich „commit und push“ sagt oder das Projektprofil Push-Automatik verlangt.
Außerdem sollte ein Commit-Helper nicht bei jedem Commit zwangsläufig Version und Dokumentation verändern. Ein kleiner Docs-, Test- oder Chore-Commit benötigt nicht automatisch einen neuen Produktrelease. Die Versionsstrategie sollte vollständig aus dem Commit-Profil kommen und auch „kein Versionsbump“ erlauben.
Fazit: Dieser Skill braucht kurzfristig einen Fix.

## 8. mockup-erstellen

Mit etwa 596 Zeilen klar zu groß.
Die Fähigkeit selbst ist gut: HTML-Mockup vor großer UI-Implementierung, vorhandenes Design laden, Tokens verwenden, mehrere Ansichten, danach Abnahme.
Sehr viel BPM-spezifische Sitemap- und NN-Namenslogik steckt allerdings direkt im Kernskill. Genau das sollte ein Mockup-Profil oder eine Reference übernehmen.
Eine saubere Struktur wäre beispielsweise:

```
SKILL.md
references/
  html-guidelines.md
  sitemap-workflow.md
  responsive-review.md
  bpm-mockups.md
  heidi-bento.md
```

Zusätzlich fehlt mir ein expliziter visueller Qualitäts-Loop. Ein UI-Mockup sollte nicht nur technisch erzeugt werden, sondern gegen Kriterien bewertet werden: Desktop/390 px, Overflow, Bedienbarkeit, Hierarchie, Kontrast, Touch-Ziele, reale Zustände.
Gerade für diesen subjektiven Skill passt Anthronics Empfehlung sehr gut: qualitative Evaluation statt ausschließlich formaler Checks.
Fazit: Gute Funktion, aber einer der besten Kandidaten für Progressive Disclosure.

## 9. skill-neu

Dieser Skill ist erstaunlich nah an der eingebetteten Anthropic-Referenz: Intent erfassen, Trigger bestimmen, Negativgrenzen, Testprompts, Live-Test, iterativ nachschärfen.
Ein paar Dinge würde ich dennoch ändern.
Mit etwa 534 Zeilen verletzt er selbst seine eigene Regel, ab ungefähr 300 Zeilen über references/ nachzudenken.
Noch auffälliger: Er definiert test-prompts.md als Pflicht für alle Skills des Repos. Im aktuellen Tree besitzen diese Datei nur:
skill-neu/test-prompts.md und ticket/test-prompts.md.
Das ist entweder ein Repo-Fehler oder die Regel ist falsch. Ich würde eher eine einzige Eval-Quelle definieren. Momentan habt ihr zwei Systeme:
skills/<skill>/test-prompts.md
und
evals/<skill>.md.
Das sollte konsolidiert werden.
Anthronics aktuelle Referenz geht außerdem weiter: mit Skill vs. Baseline testen, Ergebnisse quantitativ/qualitativ vergleichen und iterieren. Euer Skill ist dagegen noch stärker manuell ausgerichtet. Für kritische Skills wäre genau dieser Benchmark-Loop sinnvoll.
Fazit: Sehr guter Meta-Skill, aber Eval-Architektur vereinheitlichen.

## 10. skill-pflege

Das ist für mich aktuell der größte strukturelle Schwachpunkt im System.
Mit ungefähr 628 Zeilen ist er der längste Skill. Gleichzeitig schreibt er sich selbst Regeln vor wie:
nichts löschen
nichts kürzen
nichts umformulieren
Struktur/Reihenfolge nicht ändern
Frontmatter nicht anfassen

Damit wird jeder Skill langfristig zwangsläufig größer.
Das erklärt wahrscheinlich einen Teil dessen, was man heute im Repo sieht: Regeln werden additiv ergänzt, Ausnahmen kommen als „zweite Ausnahme seit v0.24“ dazu, neue Abschnitte werden angehängt – aber alte Regeln können kaum sauber konsolidiert werden.
Das widerspricht dem Zweck von „Pflege“.
Es gibt sogar einen internen Spannungsbogen: Die Description sagt, skill-pflege sei auch für „refining descriptions“ und „restructuring existing SKILL.md content“ zuständig, während die harten Regeln Frontmatter und Struktur zunächst verbieten.
Ich würde zwei Modi einführen:

| Modus | Verhalten |
|---|---|
| Safe Patch | minimale additive Änderung, bestehende Struktur schützen |
| Refactor | Redundanz beseitigen, umformulieren, verschieben, löschen – mit Diff und semantischem Vollständigkeitscheck |

Entscheidend ist nicht, dass jeder alte Satz erhalten bleibt. Entscheidend ist, dass jede beabsichtigte Regel und Funktion erhalten oder bewusst geändert wird.
Damit könnte dieser Skill anschließend auch die anderen Skills gesundschrumpfen.
Fazit: Höchste Refactor-Priorität.

## 11. ticket

Mit 158 Zeilen ist das fast ein Musterbeispiel dafür, wie kompakt ein spezialisierter Skill sein kann.
Der Skill hat eine konkrete Domäne, klaren Trigger und einen nachvollziehbaren Acht-Schritte-Workflow. Er delegiert Ursache/Fix an code-erstellen und Taskverwaltung an tracker.
Das ist genau die richtige Art von Orchestrierung.
Ein Punkt: Nicht jeder reale Fehler muss zwangsläufig einen neuen Tracker-Task benötigen. Wenn das Ticket bereits die Source of Truth ist, erzeugt ihr möglicherweise doppelte Verwaltung. Das sollte das Ticket-Profil festlegen können:
Tracker-Aufgabe erforderlich: ja/nein/nur bei angenommen

Außerdem ist bei Schritt 8 interessant, ob „gelöst“ erst nach User-Verifikation oder bereits nach Einspielen gesetzt wird. Momentan kommt Ticket lösen vor User-Prüfung. Semantisch wäre oft besser:
fixed → verification → resolved.
Fazit: Einer der saubersten Skills im Repo.

## 12. tracker

Der tracker zeigt am besten, wie Progressive Disclosure bei euch funktionieren kann.
461 Zeilen sind zwar immer noch recht viel, aber die eigentlichen Kommandoworkflows sind bereits in 13 Reference-Dateien ausgelagert. Das ist die richtige Richtung.
Einige Kernregeln sind allerdings überreguliert. Beispielsweise zwingt der Skill bei sehr vielen Folgeantworten Task-Anker, Zwischenstandstabellen, Review-Workflow-Checks und automatischen Nachlauf auf. Jede einzelne Regel kann sinnvoll sein; gemeinsam entsteht aber ein hoher Interaction Tax.
Ein Tracker-Skill sollte hauptsächlich zuverlässig sein:
richtiger Task → richtige Änderung → eindeutige Bestätigung.
Alles Weitere sollte nach Risiko gestaffelt werden.
Außerdem liegt im Repo sowohl
tracker/references/
als auch
tracker/references.zip.
Wenn das ZIP nicht ausdrücklich als Distributionsartefakt benötigt wird, würde ich es entfernen. Es ist eine zweite, potenziell veraltende Kopie derselben Inhalte.
Der Tool-Ladeabschnitt ist ebenfalls sehr plattformspezifisch. Solche Details gehören eher in eine Tool-Adapter-Reference als in den fachlichen Kern.
Fazit: Architektonisch der beste große Skill; Kernregeln noch reduzieren.

## Was ich am System grundsätzlich ändern würde

Der nächste Refactor sollte nicht noch mehr Regeln hinzufügen. Er sollte konsolidieren.
Ich würde in dieser Reihenfolge vorgehen:
1. Echte Widersprüche beheben: 12 statt 11 Skills, Commit/Push, PowerShell-Fehlerabbruch, audit ↔ doc-pflege.
2. skill-pflege neu konzipieren, damit kontrolliertes Löschen, Umstrukturieren und Zusammenfassen möglich wird.
3. SKILL.md-Kerne verkleinern: insbesondere chat-wechsel, chatgpt-review, mockup-erstellen, skill-neu, skill-pflege, danach code-erstellen.
4. Eval-System vereinheitlichen: nicht gleichzeitig halb gepflegte test-prompts.md und evals/*.md.
5. Jeden der 12 Skills mit echten Positiv-/Negativ-/Konfliktfällen testen.
6. Tool-/Umgebungsdetails aus Fachskills in Adapter-/Reference-Dateien verschieben.

Mein Zielbild wäre: Ein normaler Fachskill hat ungefähr 100–300 Zeilen, ein komplexer Orchestrator vielleicht 300–450, und alles Ablauf- oder projektspezifische darunter liegt in references/. Genau dadurch wird Claude weniger Regeln gleichzeitig jonglieren müssen und die Wahrscheinlichkeit steigen, dass die wirklich wichtigen Regeln zuverlässig befolgt werden.
Der wichtigste Einzelpunkt ist dabei skill-pflege: Solange „nichts löschen/kürzen/umformulieren/verschieben“ die Grundphilosophie bleibt, wird das Repo mit jeder Verbesserung zwangsläufig komplizierter statt einfacher.
Ich habe dabei nichts im Repo verändert.
