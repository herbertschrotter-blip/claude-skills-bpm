#!/bin/sh
# Einrichtung des Marketplace workbench auf Linux/macOS (auch Home-Assistant-Add-on).
# Prüft git, Python 3 und Claude Code, installiert Fehlendes nach Rückfrage, legt den Marketplace an bzw. aktualisiert
# ihn und übergibt dann an tools/einrichten.py (Plugins, Optionen, autoUpdate, skillOverrides, Probe der Hooks).
#
#   sh tools/install.sh [--modus terminal|desktop] [--host NAME] [--ja] [--ohne-overrides]
#   curl -fsSL https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.sh | sh -s -- --host laptop
set -e

REPO="herbertschrotter-blip/claude-workbench"
MARKETPLACE="workbench"
JA=""
for arg in "$@"; do [ "$arg" = "--ja" ] && JA=1; done

has() { command -v "$1" >/dev/null 2>&1; }
schritt() { printf '\n%s\n' "$1"; }
ok() { printf '  OK  %s\n' "$1"; }

frage() {  # frage "Text" → 0 bei ja (Vorschlag: ja)
    [ -n "$JA" ] && return 0
    printf '%s [J/n] ' "$1"
    read -r antwort </dev/tty || antwort=""
    case "$antwort" in n|N|nein|Nein) return 1 ;; *) return 0 ;; esac
}

paket() {  # paket <apk/apt-Name> – installiert mit dem Paketmanager des Systems
    sudo=""
    [ "$(id -u)" != "0" ] && has sudo && sudo="sudo"
    if has apk; then $sudo apk add --no-cache "$1"
    elif has apt-get; then $sudo apt-get update -qq && $sudo apt-get install -y "$1"
    elif has dnf; then $sudo dnf install -y "$1"
    elif has pacman; then $sudo pacman -S --noconfirm "$1"
    elif has brew; then brew install "$1"
    else echo "Kein bekannter Paketmanager – bitte $1 von Hand installieren."; return 1
    fi
}

printf '\n=== Einrichtung workbench (Skills, Skill-Log, Skill-Wächter) ===\n'
schritt "[1/5] Voraussetzungen"
if has git; then ok "git: $(git --version)"
elif frage "git fehlt. Installieren?"; then paket git
else echo "Ohne git geht es nicht (der Marketplace ist ein Git-Repo)."; exit 1
fi

if has python3 && python3 -c 'import sys; sys.exit(sys.version_info < (3, 8))'; then
    ok "Python: $(python3 --version)"
elif frage "Python 3 (ab 3.8) fehlt. Installieren?"; then paket python3
else echo "Ohne Python 3 laufen Skill-Log und Skill-Wächter nicht."; exit 1
fi

if has claude; then ok "Claude Code: $(claude --version 2>/dev/null | head -1)"
elif frage "Claude Code fehlt. Mit dem offiziellen Installer installieren (curl -fsSL https://claude.ai/install.sh | bash)?"; then
    curl -fsSL https://claude.ai/install.sh | bash
    PATH="$HOME/.local/bin:$PATH"
    has claude || { echo "claude noch nicht im PATH – neue Shell öffnen und dieses Skript erneut starten."; exit 1; }
    echo "Anmelden: claude starten und /login ausführen, danach dieses Skript erneut starten."
else echo "Ohne Claude Code geht es nicht."; exit 1
fi

schritt "[2/5] Marketplace $MARKETPLACE"
if claude plugin marketplace list --json 2>/dev/null | grep -q "\"name\": *\"$MARKETPLACE\""; then
    claude plugin marketplace update "$MARKETPLACE"
else
    claude plugin marketplace add "$REPO"
fi

ORT=$(claude plugin marketplace list --json | python3 -I -c '
import json, sys
print(next(m["installLocation"] for m in json.load(sys.stdin) if m["name"] == sys.argv[1]))' "$MARKETPLACE")

ok "Marketplace $MARKETPLACE in $ORT"

if python3 -I "$ORT/tools/einrichten.py" --schritt 3 "$@" </dev/tty; then
    printf '\n=== FERTIG – Claude Code jetzt neu starten ===\n'
else
    printf '\n=== NICHT FERTIG – siehe die Meldung oben ===\n'
    exit 1
fi
