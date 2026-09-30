# Neues Fenster für die nächste Sitzung (Claude Code mit tmux)

Gilt nur in **Claude Code**, wenn die Sitzung in **tmux** läuft (z. B. das Claude-Terminal-Add-on auf Home Assistant).
Nach dem Handover-Prompt richtet Claude die nächste Sitzung gleich ein: neues tmux-Fenster im Projekt-Repo, Claude
mit Remote Control, der Prompt liegt eingefügt im Eingabefeld – abgeschickt wird er vom Nutzer.

## Ablauf

1. **Umgebung prüfen** (Tatsachen aus der Shell, keine Fragen):
   - läuft tmux? `tmux ls` bzw. `$TMUX`. Kein tmux → nur den Prompt ausgeben und einen Satz dazu, dass ein neues
     Fenster mit tmux ginge; hier aufhören.
   - Projekt-Repo: `git rev-parse --show-toplevel` im Arbeitsordner der Sitzung. Läuft die Sitzung außerhalb des Repos
     (z. B. im Config-Ordner), das Repo aus dem Chat nehmen, in dem gearbeitet wurde; unklar → Auswahlfrage mit den
     Kandidaten.
   - tmux-Sitzung des Projekts: `tmux list-windows -a -F '#{session_name}:#{window_index} #{window_name} #{pane_current_path}'`.
     Hat der Nutzer je Projekt eine eigene Sitzung (Name passt zum Projekt oder ein Fenster liegt im Repo), diese
     nehmen; sonst die Sitzung, in der Claude gerade läuft. Mehrere Kandidaten → Auswahlfrage.
2. **Rückfrage** (Auswahlfrage): „Neues Fenster einrichten (Recommended)“ / „Nur Prompt“. Die Optionen nennen den
   geplanten Fensternamen und die Sitzung.
3. **Fenster anlegen:** Name `<Projekt> Teil <N+1>` (N+1 wie im Prompt-Titel), Arbeitsordner = Repo:
   `tmux new-window -d -t "<Sitzung>" -n "<Name>" -c "<Repo>" 'claude --remote-control "<Name>"'`.
   Warten, bis Claude bereit ist (`tmux capture-pane -p -t "<Sitzung>:<Name>"` zeigt den Kopf von Claude Code und
   „remote-control is active“); höchstens etwa 30 s, sonst melden und den Prompt nur ausgeben.
4. **Prompt einfügen:** den fertigen Prompt als Datei in den Scratchpad schreiben, dann
   `tmux load-buffer -b uebergabe <datei>` und `tmux paste-buffer -p -d -b uebergabe -t "<Sitzung>:<Name>"`
   (`-p` = Bracketed Paste: der Text landet als ein Block im Eingabefeld, Zeilenumbrüche schicken nichts ab).
   Prüfen, dass er angekommen ist (Anzeige „[Pasted text …]“). **Nicht absenden** – der Nutzer prüft und drückt Enter.
5. **Melden:** Fenstername und Sitzung, der Remote-Control-Link aus der Anzeige, wie man hinkommt
   (`Strg+b`, dann `s` für Sitzungen bzw. `w` für Fenster) und der Hinweis, das alte Fenster zu beenden, sobald die neue
   Sitzung läuft (`/exit`, dann `exit`) – sonst arbeiten zwei Sitzungen am selben Repo. Den Prompt zusätzlich im Chat
   als Markdown-Codeblock ausgeben.

## Regeln

- Das alte Fenster nie selbst schließen und den Prompt nie selbst absenden.
- Keine Pfade raten: Repo und Sitzung kommen aus der Shell oder aus einer Auswahlfrage.
- Remote Control ist Standard (`claude --remote-control "<Name>"`); lehnt der Nutzer es ab, `claude -n "<Name>"`.
