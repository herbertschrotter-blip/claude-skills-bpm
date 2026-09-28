# GitHub für projekt-anlegen

Wie ein Projekt auf GitHub kommt oder von dort geholt wird. Werte (Owner, Push-Policy) kommen aus dem Skill-Profil.

## Anmeldung prüfen

- `gh auth status` zeigt, ob die GitHub-CLI angemeldet ist. Ohne `gh`: `git ls-remote <url>` zeigt, ob ein Repo
  erreichbar ist.
- Fehlt die Anmeldung, erklärt Claude den Weg (`gh auth login` im Terminal des Nutzers oder ein Token mit minimalen
  Rechten) und wartet. Claude fragt nie nach dem Token im Chat und schreibt ihn nie in eine Datei, einen Befehl oder
  eine Remote-URL.
- Öffentliche Repos lassen sich ohne Anmeldung klonen. Fragt `git clone` nach Benutzername und Passwort, ist das Repo
  privat: abbrechen und die Anmeldung klären.

## Neues Repo erstellen

Nur nach Auswahlfrage (erstellen / später / nie). Sichtbarkeit privat, außer der Nutzer wählt öffentlich.

```bash
gh repo create <owner>/<name> --private --source . --remote origin
git push -u origin <branch>
```

- `<owner>` aus `Projekte.GitHub-Owner`; fehlt er, danach fragen.
- Gibt es den Namen schon: nicht überschreiben, sondern Auswahlfrage (anderer Name / vorhandenes Repo klonen /
  abbrechen).
- Ohne `gh`: Der Nutzer legt das leere Repo auf github.com an, Claude setzt danach `git remote add origin <url>` und
  pusht nach der Push-Policy.
- Soll das Projekt über HACS oder einen ähnlichen Katalog verteilt werden, braucht es später echte Releases; das
  gehört nicht zum Anlegen, nur der Hinweis in der Zusammenfassung.

## Bestehendes Repo klonen

```bash
git clone https://github.com/<owner>/<name>.git <Projekte.Ablage>/<name>
```

- Vorher prüfen, ob der Zielordner leer ist oder fehlt. Existiert er mit Inhalt: nicht überschreiben, Auswahlfrage.
- Nach dem Klonen die `CLAUDE.md` des Repos lesen. Hat sie ein Skill-Profil, gilt es; fehlen Felder, nach der
  Profil-Regel „Fehlende Werte“ vorgehen.
- Wird das Repo schon an einem anderen Ort bearbeitet (anderer PC), die Quelle der Wahrheit klären (SKILL.md,
  Schritt 3), bevor jemand darin ändert.
