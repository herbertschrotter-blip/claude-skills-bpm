# Windows: Netzlaufwerk zu Home Assistant

Wenn die Sitzung unter Windows läuft und ein Home-Assistant-Projekt angelegt wird, liegt die Ablage auf dem Rechner
mit Home Assistant (z. B. ein Raspberry Pi). Erreichbar ist sie über die Samba-Freigabe des
Konfigurationsordners als Netzlaufwerk. Diese Reference sagt, wie Claude das Laufwerk findet, mit dem Nutzer
einrichtet und sich für spätere Sitzungen auf diesem Rechner merkt.

Einfacher und vollständiger ist eine Sitzung direkt auf dem HA-Rechner (dort laufen alle Prüfungen, auch die
HA-Tests). Deshalb steht diese Möglichkeit zuerst in der Auswahlfrage; das Netzlaufwerk ist der Weg, wenn am
Windows-Rechner gearbeitet werden soll.

## Merker dieses Rechners

In der persönlichen `CLAUDE.md` des Rechners (`~/.claude/CLAUDE.md`, gilt für alle Sitzungen dort), Abschnitt
`## Rechner`, eine Zeile:

```
- Netzlaufwerk Home Assistant: H: = \\<host>\config (Samba); Ablage HA-Projekte: H:\projekte
```

Buchstabe, Host und Ablage sind Beispielwerte; es zählt, was beim Einrichten tatsächlich verbunden wurde. Die Ablage
ist `Projekte.Ablage` aus dem Skill-Profil des HA-Konfigurationsordners, auf das Laufwerk übertragen.

## Ablauf

1. **Merker lesen.** Steht er da: prüfen, ob `<Laufwerk>:\configuration.yaml` erreichbar ist. Ja → weiter mit
   Schritt 5. Nein (Laufwerk getrennt, Rechner aus) → dem Nutzer sagen und Schritt 3c anbieten.
2. **Ohne Merker suchen.** `net use` bzw. `Get-PSDrive -PSProvider FileSystem`: Gibt es ein Laufwerk, in dessen Wurzel
   `configuration.yaml` liegt? Ja → per Auswahlfrage bestätigen lassen, dann Schritt 4.
3. **Einrichten mit dem Nutzer**, jeder Schritt mit Auswahlfrage:
   1. Erreichbarkeit: `Test-NetConnection <host> -Port 445` (Host aus dem Kontext, sonst fragen; Standardname von
      Home Assistant OS ist `homeassistant`). Scheitert das, läuft die Freigabe nicht: Der Nutzer installiert bzw.
      startet in Home Assistant das Add-on „Samba share“ und setzt dort Benutzer und Passwort.
   2. Freien Laufwerksbuchstaben vorschlagen (`H:`, sonst den nächsten freien).
   3. Verbinden macht der Nutzer selbst, weil Windows nach dem Passwort fragt: in einem eigenen PowerShell-Fenster ohne
      Administratorrechte (dort sieht auch Claude Code das Laufwerk)
      `net use H: \\<host>\config /user:<samba-benutzer> /persistent:yes`, oder im Explorer „Netzlaufwerk verbinden“
      mit „Verbindung bei Anmeldung wiederherstellen“.
   4. Prüfen: `H:\configuration.yaml` ist sichtbar.
4. **Merker schreiben**, nach Rückfrage: die Zeile oben in `~/.claude/CLAUDE.md`, Abschnitt `## Rechner` (anlegen,
   falls er fehlt; vorhandener Text bleibt).
5. **Anlegen** mit der Ablage auf dem Laufwerk (`--ablage H:\projekte`). Der Generator legt den Zwischenordner dort an
   und verschiebt erst nach grüner Prüfung. Prüfschritte nur für Linux (die HA-Tests) laufen unter Windows nicht: das
   in der Zusammenfassung als eigenen Satz sagen und den Testbefehl aus der `CLAUDE.md` des neuen Projekts für eine
   Sitzung auf dem HA-Rechner nennen. „Lädt im Test-HA“ erst melden, wenn er dort grün gelaufen ist.

## Nie

- Passwort oder Samba-Benutzerdaten lesen, speichern, in einen Befehl oder in den Merker schreiben
- Das Samba-Add-on oder seine Einstellungen selbst ändern
- Ein Laufwerk ohne `configuration.yaml` als Ablage nehmen oder einen Laufwerksbuchstaben raten
