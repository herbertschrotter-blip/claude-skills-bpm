#!/bin/sh
# Einrichtung des Marketplace workbench auf Linux/macOS (auch Home-Assistant-Add-on).
#
#   sh tools/install.sh [--modus terminal|desktop] [--host NAME] [--log-repo owner/name] [--ja] [--ohne-overrides]
#   sh tools/install.sh --entfernen
#   Tests: WORKBENCH_REPO=<lokaler Ordner> HOME=<leerer Ordner> sh tools/install.sh --ja --ohne-login ...
#   curl -fsSL https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/tools/install.sh | sh
#
# Ablauf wie tools/install.ps1: Bestandsaufnahme -> alle Fragen auf einmal -> installieren (Claude-Installer parallel
# zu den Paketen) -> Marketplace -> einrichten.py (Plugins, Optionen, autoUpdate, skillOverrides, Probe) -> Anmeldung.
# Protokoll fuer --entfernen: ~/.claude/workbench-einrichtung.json. Fehlerquellen: docs/installation.md.

REPO="${WORKBENCH_REPO:-herbertschrotter-blip/claude-workbench}"  # WORKBENCH_REPO: anderes Repo oder lokaler Ordner (Tests)
MARKETPLACE="workbench"
SAMMEL_NAME="skill-log"  # Sammel-Repo für das Skill-Log: eines je GitHub-Konto, <konto>/skill-log
JA=""; MODUS=""; HOST=""; LOGREPO="-"; OHNE_OVERRIDES=""; ENTFERNEN=""; OHNE_LOGIN=""
while [ $# -gt 0 ]; do
    case "$1" in
        --ja) JA=1 ;;
        --modus) shift; MODUS="$1" ;;
        --host) shift; HOST="$1" ;;
        --log-repo) shift; LOGREPO="$1" ;;
        --ohne-overrides) OHNE_OVERRIDES=1 ;;
        --entfernen) ENTFERNEN=1 ;;
        --ohne-login) OHNE_LOGIN=1 ;;
    esac
    shift
done
TTY=/dev/tty; ( : < /dev/tty ) 2>/dev/null || TTY=/dev/null  # ohne Terminal: Vorschläge nehmen
[ "$TTY" = /dev/null ] && JA=1
TMP="${TMPDIR:-/tmp}/workbench-einrichtung.$$"
mkdir -p "$TMP"
trap 'fest_aus; rm -rf "$TMP"' EXIT
LOCALBIN="$HOME/.local/bin"
PROTOKOLL="$HOME/.claude/workbench-einrichtung.json"
ZUSATZ="$TMP/zusatz.json"
printf '[' > "$ZUSATZ"

has() { command -v "$1" >/dev/null 2>&1; }
# Fortschritt oben fest: Zeile 1 Gesamt, Zeile 2 laufende Aufgabe; darunter scrollt die Ausgabe (Rollbereich ab Zeile 4)
PCT=0; TEXT=""; TPCT=0; TTEXT=""; FEST=""
leiste() {  # leiste PROZENT BREITE
    voll=$(($1 * $2 / 100)); out=""; i=0
    while [ $i -lt "$2" ]; do if [ $i -lt $voll ]; then out="$out█"; else out="$out░"; fi; i=$((i + 1)); done
    printf '%s' "$out"
}
zeichnen() {
    [ -n "$FEST" ] || return 0
    printf '\0337\033[1;1H\033[2K  %s %3d%%  %.50s\033[2;1H\033[2K' "$(leiste "$PCT" 30)" "$PCT" "$TEXT"
    [ -n "$TTEXT" ] && printf '      %s %3d%%  %.46s' "$(leiste "$TPCT" 24)" "$TPCT" "$TTEXT"
    printf '\0338'
}
fest_an() {
    [ -t 1 ] || return 0
    rows=$(stty size < "$TTY" 2>/dev/null | cut -d' ' -f1)
    [ -n "$rows" ] && [ "$rows" -gt 10 ] || return 0
    printf '\033[H\033[2J\033[4;%sr\033[4;1H' "$rows"
    FEST=1; zeichnen
}
fest_aus() { [ -n "$FEST" ] && printf '\0337\033[r\0338'; FEST=""; }
balken() { [ "$1" -gt "$PCT" ] && PCT=$1; [ -n "$2" ] && TEXT=$2; zeichnen; }
teil() { TPCT=$1; TTEXT=$2; zeichnen; }   # teil PROZENT TEXT; teil 0 "" blendet aus
meldung() { printf '%s\n' "$1"; }
ok() { meldung "  OK  $1"; }
hinweis() { meldung "  !   $1"; }
fehler() { meldung "  X   $1"; }
frage() {  # frage "Text" [j|n] -> 0 bei ja
    vorschlag=${2:-j}
    if [ -n "$JA" ]; then [ "$vorschlag" = j ]; return; fi
    if [ "$vorschlag" = j ]; then printf '  %s [J/n] ' "$1"; else printf '  %s [j/N] ' "$1"; fi
    read -r antwort < "$TTY" || antwort=""
    [ -z "$antwort" ] && { [ "$vorschlag" = j ]; return; }
    case "$antwort" in j|J|ja|Ja|y|Y|yes) return 0 ;; *) return 1 ;; esac
}
eingabe() {  # eingabe "Text" VORSCHLAG -> Ergebnis in $ANTWORT
    ANTWORT=$2
    [ -n "$JA" ] && return
    printf '  %s [%s] ' "$1" "$2"
    read -r a <"$TTY" && [ -n "$a" ] && ANTWORT=$a
}
protokoll() { # protokoll WAS WERT AKTION
    [ "$(cat "$ZUSATZ")" = "[" ] || printf ',' >> "$ZUSATZ"
    printf '{"was":"%s","wert":"%s","aktion":"%s"}' "$1" "$2" "$3" >> "$ZUSATZ"
}
paket() {  # paket NAME – mit dem Paketmanager des Systems
    sudo=""
    [ "$(id -u)" != "0" ] && has sudo && sudo="sudo"
    if has apk; then $sudo apk add --no-cache "$1"
    elif has apt-get; then $sudo apt-get update -qq && $sudo apt-get install -y "$1"
    elif has dnf; then $sudo dnf install -y "$1"
    elif has pacman; then $sudo pacman -S --noconfirm "$1"
    elif has brew; then brew install "$1"
    else return 1
    fi
}
python3_ok() { has python3 && python3 -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>/dev/null; }
profil_datei() { case "$(basename "${SHELL:-sh}")" in zsh) echo "$HOME/.zprofile" ;; *) echo "$HOME/.profile" ;; esac; }
pfad_dauerhaft() {  # ~/.local/bin dauerhaft in die Profil-Datei, sofort in die laufende Sitzung
    datei=$(profil_datei)
    if ! grep -qs 'workbench: ~/.local/bin' "$datei"; then
        printf '\nexport PATH="$HOME/.local/bin:$PATH"  # workbench: ~/.local/bin (tools/install.sh)\n' >> "$datei"
        ok "PATH ergänzt in $datei (neue Shells sehen es)"
        protokoll pfad "$datei" installiert
    fi
    case ":$PATH:" in *":$LOCALBIN:"*) ;; *) PATH="$LOCALBIN:$PATH"; export PATH ;; esac
}
eingeloggt() { claude auth status 2>/dev/null | python3 -I -c 'import json,sys; sys.exit(0 if json.load(sys.stdin).get("loggedIn") else 1)' 2>/dev/null; }
marketplace_ort() {
    claude plugin marketplace list --json 2>/dev/null | python3 -I -c '
import json, sys
print(next((m["installLocation"] for m in json.load(sys.stdin) if m["name"] == sys.argv[1]), ""))' "$MARKETPLACE" 2>/dev/null
}
git_leise() { GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never git "$@" 2>/dev/null; }  # nur gespeicherte Zugangsdaten
github_konto() {  # GitHub-Konto des Nutzers: gh, sonst die gespeicherten git-Zugangsdaten
    if has gh; then k=$(gh api user --jq .login 2>/dev/null) && [ -n "$k" ] && { printf '%s' "$k"; return; }; fi
    printf 'protocol=https\nhost=github.com\n\n' | git_leise credential fill | sed -n 's/^username=//p' | head -1
}
frueher_log_repo() {  # schon gesetzte Option log_repo von work oder work-hooks
    for id in "work@$MARKETPLACE" "work-hooks@$MARKETPLACE"; do
        r=$(claude plugin configure "$id" --json 2>/dev/null | python3 -I -c '
import json, sys
try: print(json.load(sys.stdin).get("inputs", {}).get("log_repo") or "")
except Exception: pass' 2>/dev/null)
        [ -n "$r" ] && { printf '%s' "$r"; return; }
    done
}

# --- Entfernen --------------------------------------------------------------------------------------------------------
if [ -n "$ENTFERNEN" ]; then
    printf '\n=== workbench entfernen (nur, was die Einrichtung selbst angelegt hat) ===\n'
    [ -f "$PROTOKOLL" ] || { echo "Kein Protokoll ($PROTOKOLL) - nichts zu tun. Von Hand: docs/installation.md, Abschnitt Entfernen."; exit 0; }
    [ -x "$LOCALBIN/claude" ] && PATH="$LOCALBIN:$PATH"
    ORT=$(has claude && python3_ok && marketplace_ort)
    if [ -n "$ORT" ] && [ -f "$ORT/tools/einrichten.py" ]; then
        cp "$ORT/tools/einrichten.py" "$TMP/einrichten.py"  # Kopie: einrichten.py entfernt den Marketplace-Ordner selbst
        python3 -I "$TMP/einrichten.py" --entfernen ${JA:+--ja} <"$TTY"
    else
        echo "  python3, claude oder der Marketplace fehlt - Plugins und Einstellungen bitte von Hand prüfen."
    fi
    python3 -I - "$PROTOKOLL" <<'PY' > "$TMP/rest.txt"
import json, sys
for e in json.load(open(sys.argv[1], encoding="utf-8-sig")).get("eintraege", []):
    if e.get("aktion") == "installiert" and e["was"] in ("pfad", "claude", "git", "python"):
        print(e["was"], e.get("wert", ""))
PY
    printf '\n[Entfernen] System\n'
    : > "$TMP/weg.txt"
    while read -r was wert; do
        case "$was" in
            pfad) if frage "PATH-Zeile aus $wert entfernen?" j; then sed -i.bak '/workbench: ~\/.local\/bin/d' "$wert" && echo "  OK  entfernt" && echo "$was $wert" >> "$TMP/weg.txt"; fi ;;
            claude) if frage "Claude Code entfernen (~/.claude mit Gesprächen und Skill-Log bleibt)?" n; then
                        rm -f "$LOCALBIN/claude"; rm -rf "$HOME/.local/share/claude"; echo "  OK  entfernt"; echo "$was $wert" >> "$TMP/weg.txt"; fi ;;
            git|python) echo "  $was wurde über den Paketmanager installiert - bei Bedarf von Hand entfernen." ;;
        esac
    done < "$TMP/rest.txt"
    # Protokoll fortschreiben; löschen nur, wenn nichts mehr offen ist
    python3 -I - "$PROTOKOLL" "$TMP/weg.txt" <<'PY'
import json, os, sys
path, weg = sys.argv[1], {tuple(l.split(" ", 1)) for l in open(sys.argv[2]).read().splitlines() if l}
data = json.load(open(path, encoding="utf-8-sig"))
for e in data.get("eintraege", []):
    if (e["was"], e.get("wert", "")) in weg:
        e["aktion"] = "entfernt"
rest = [e for e in data["eintraege"] if e.get("aktion") == "installiert" and e["was"] not in ("git", "python")]
if rest:
    json.dump(data, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("  !   Noch offen (abgelehnt oder gescheitert): " + ", ".join(f'{e["was"]} {e.get("wert", "")}' for e in rest))
    print("      Das Protokoll bleibt; ein erneutes --entfernen macht weiter.")
else:
    os.remove(path)
    print("  OK  Alles zurückgenommen, Protokoll gelöscht. Das Skill-Log (~/.claude/skill-log) bleibt.")
PY
    exit 0
fi

# --- 1. Bestandsaufnahme ----------------------------------------------------------------------------------------------
fest_an
printf '\n=== Einrichtung workbench (Skills, Skill-Log, Skill-Wächter) ===\n'
balken 1 "Bestandsaufnahme"
if [ -x "$LOCALBIN/claude" ] && ! has claude; then pfad_dauerhaft; fi
HAT_GIT=""; HAT_PY=""; HAT_CLAUDE=""; ANGEMELDET=""; MP_DA=""
has git && HAT_GIT=1 && ok "git: $(git --version | sed 's/git version //')" && protokoll git git war-da
python3_ok && HAT_PY=1 && ok "Python: $(python3 --version)" && protokoll python python3 war-da
if has claude; then
    HAT_CLAUDE=1; protokoll claude claude war-da
    [ -n "$HAT_PY" ] && eingeloggt && ANGEMELDET=1
    [ -n "$HAT_PY" ] && [ -n "$(marketplace_ort)" ] && MP_DA=1
    ok "Claude Code: $(claude --version 2>/dev/null | head -1)$([ -n "$ANGEMELDET" ] && echo ', angemeldet' || echo ', nicht angemeldet')"
fi
if [ -n "$MP_DA" ]; then protokoll marketplace "$MARKETPLACE" war-da; else protokoll marketplace "$MARKETPLACE" installiert; fi
# Marketplace sofort im Hintergrund auffrischen
[ -n "$MP_DA" ] && { claude plugin marketplace update "$MARKETPLACE" > "$TMP/mp.txt" 2>&1 & }
balken 5 "Bestandsaufnahme fertig"

# --- 2. Alle Fragen auf einmal ----------------------------------------------------------------------------------------
meldung ""
meldung "  Bitte einmal alles beantworten - danach läuft die Einrichtung ohne weitere Fragen."
WOLL_GIT=""; WOLL_PY=""; WOLL_CLAUDE=""
if [ -z "$HAT_GIT" ]; then frage "git fehlt. Installieren?" && WOLL_GIT=1 || { fehler "Ohne git geht es nicht."; exit 1; }; fi
if [ -z "$HAT_PY" ]; then frage "Python 3 (ab 3.8) fehlt. Installieren?" && WOLL_PY=1 || { fehler "Ohne python3 laufen die Hooks nicht."; exit 1; }; fi
if [ -z "$HAT_CLAUDE" ]; then frage "Claude Code fehlt. Mit dem offiziellen Installer installieren?" && WOLL_CLAUDE=1 || { fehler "Ohne Claude Code geht es nicht."; exit 1; }; fi
if [ -z "$MODUS" ]; then
    if frage "Läuft Claude hier in der Claude-Desktop-App (Skills kommen aus claude.ai)?" n; then MODUS=desktop; else MODUS=terminal; fi
fi
if [ -z "$HOST" ]; then eingabe "Rechnername im Skill-Log (Enter = Vorschlag)" "$(hostname 2>/dev/null | cut -d. -f1 | tr 'A-Z' 'a-z')"; HOST=$ANTWORT; fi
if [ "$LOGREPO" = "-" ]; then
    # Ein Sammel-Repo je GitHub-Konto, auf allen Rechnern dasselbe: schon gesetzte Option, lokaler Klon, sonst
    # <konto>/skill-log, wenn es das Repo gibt; fehlt es, mit gh anlegen
    balken 9 "Suche Sammel-Repo"
    VORSCHLAG=""; KONTO=""; LOGREPO=""
    FRAGE_REPO="Sammel-Repo für das Skill-Log (eines je GitHub-Konto, auf allen Rechnern gleich; - = keins)"
    [ -n "$HAT_CLAUDE" ] && [ -n "$HAT_PY" ] && VORSCHLAG=$(frueher_log_repo)
    if [ -z "$VORSCHLAG" ] && [ -n "$HAT_GIT" ] && [ -d "$HOME/.claude/skill-log-sammel/.git" ]; then
        VORSCHLAG=$(git_leise -C "$HOME/.claude/skill-log-sammel" remote get-url origin | sed -n 's#.*github\.com[/:]\([^/]*/[^/]*\)$#\1#p' | sed 's/\.git$//')
    fi
    if [ -z "$VORSCHLAG" ] && [ -n "$HAT_GIT" ]; then
        KONTO=$(github_konto)
        [ -n "$KONTO" ] && git_leise ls-remote "https://github.com/$KONTO/$SAMMEL_NAME.git" HEAD >/dev/null && VORSCHLAG="$KONTO/$SAMMEL_NAME"
    fi
    if [ -n "$VORSCHLAG" ]; then
        eingabe "$FRAGE_REPO" "$VORSCHLAG"; LOGREPO=$ANTWORT
    elif [ -n "$KONTO" ] && has gh; then
        if frage "Kein Sammel-Repo $KONTO/$SAMMEL_NAME gefunden. Jetzt als privates Repo anlegen (Skill-Log aller Rechner, enthält Prompt-Texte)?" n; then
            if gh repo create "$KONTO/$SAMMEL_NAME" --private --add-readme --description "Skill-Log aller Rechner (claude-workbench)" > "$TMP/gh.txt" 2>&1; then
                ok "Sammel-Repo $KONTO/$SAMMEL_NAME angelegt (privat)"; LOGREPO="$KONTO/$SAMMEL_NAME"
            else hinweis "Sammel-Repo nicht angelegt: $(tail -1 "$TMP/gh.txt")"; fi
        fi
    else
        [ -n "$KONTO" ] && hinweis "Kein Sammel-Repo $KONTO/$SAMMEL_NAME gefunden. Anlegen auf github.com: privat, mit README; dann hier eintragen."
        eingabe "$FRAGE_REPO" ""; LOGREPO=$ANTWORT
    fi
    [ "$LOGREPO" = "-" ] && LOGREPO=""
fi
OVERRIDES="--ohne-overrides"
if [ "$MODUS" = terminal ] && [ -z "$OHNE_OVERRIDES" ] && frage "Sind dieselben Skills auch bei claude.ai hochgeladen (doppelte ausblenden)?" n; then OVERRIDES="--mit-overrides"; fi

# --- 3. Installieren (Claude-Installer parallel zu den Paketen) -------------------------------------------------------
meldung ""
balken 10 "Installieren"
if [ -n "$WOLL_CLAUDE" ]; then (curl -fsSL https://claude.ai/install.sh | bash > "$TMP/claude.txt" 2>&1; echo $? > "$TMP/claude.rc") & fi
if [ -n "$WOLL_GIT" ]; then
    balken 15 "git wird installiert"; teil 10 "git"
    if paket git > "$TMP/git.txt" 2>&1; then ok "git installiert"; protokoll git git installiert; else fehler "git-Installation gescheitert: $(tail -1 "$TMP/git.txt")"; exit 1; fi
fi
if [ -n "$WOLL_PY" ]; then
    teil 0 ""; balken 25 "Python wird installiert"; teil 10 "Python"
    if paket python3 > "$TMP/py.txt" 2>&1 && python3_ok; then ok "Python: $(python3 --version)"; protokoll python python3 installiert
    else fehler "Python-Installation gescheitert: $(tail -1 "$TMP/py.txt")"; exit 1; fi
fi
if [ -n "$WOLL_CLAUDE" ]; then
    teil 0 ""; balken 35 "Claude Code wird installiert"; teil 30 "Claude Code (offizieller Installer)"
    wait
    [ -x "$LOCALBIN/claude" ] && pfad_dauerhaft
    if has claude; then ok "Claude Code: $(claude --version 2>/dev/null | head -1)"; protokoll claude claude installiert
    else fehler "Claude Code nicht installiert: $(tail -2 "$TMP/claude.txt" | tr '\n' ' ')"; exit 1; fi
fi

# --- 4. Marketplace ---------------------------------------------------------------------------------------------------
teil 0 ""; balken 50 "Marketplace $MARKETPLACE"
wait
[ -z "$MP_DA" ] && claude plugin marketplace add "$REPO" > "$TMP/mp.txt" 2>&1
ORT=$(marketplace_ort)
if [ -z "$ORT" ]; then fehler "Marketplace nicht eingerichtet: $(tail -2 "$TMP/mp.txt" | tr '\n' ' ')"; exit 1; fi
ok "Marketplace $MARKETPLACE"
printf ']' >> "$ZUSATZ"

# --- 5. Plugins, Einstellungen, Probe (einrichten.py meldet ##BALKEN-Zeilen) ------------------------------------------
python3 -I "$ORT/tools/einrichten.py" --ja --balken --modus "$MODUS" --host "$HOST" --log-repo "$LOGREPO" $OVERRIDES \
    --protokoll-zusatz "$ZUSATZ" </dev/null > "$TMP/einrichten.txt" 2>&1 &
PID=$!; GELESEN=0
while kill -0 $PID 2>/dev/null || [ "$GELESEN" -lt "$(wc -l < "$TMP/einrichten.txt")" ]; do
    ANZ=$(wc -l < "$TMP/einrichten.txt")
    while [ "$GELESEN" -lt "$ANZ" ]; do
        GELESEN=$((GELESEN + 1))
        z=$(sed -n "${GELESEN}p" "$TMP/einrichten.txt")
        case "$z" in
            "##BALKEN "*) p=$(echo "$z" | cut -d' ' -f2); balken $((55 + p * 35 / 100)) "Plugins und Einstellungen"; teil "$p" "$(echo "$z" | cut -d' ' -f3-)" ;;
            "") ;;
            *) meldung "$z" ;;
        esac
    done
    kill -0 $PID 2>/dev/null && sleep 0.3
done
wait $PID; RC=$?

# --- 6. Anmeldung (claude plugin ... läuft auch ohne; deshalb erst am Ende) -------------------------------------------
teil 0 ""; balken 92 "Anmeldung"
if [ -n "$OHNE_LOGIN" ]; then
    eingeloggt && ANGEMELDET=1
elif [ -z "$ANGEMELDET" ] && ! eingeloggt; then
    meldung ""
    meldung "  Claude Code ist noch nicht angemeldet - gleich startet die Anmeldung im Browser."
    fest_aus
    claude auth login <"$TTY"
    eingeloggt && ANGEMELDET=1 && ok "Claude Code angemeldet"
else
    ANGEMELDET=1
fi
balken 100 "Fertig"
fest_aus
printf '\n'
if [ "$RC" -eq 0 ] && [ -n "$ANGEMELDET" ]; then
    printf '=== FERTIG – Claude Code neu starten ===\n'
elif [ "$RC" -eq 0 ]; then
    printf '=== FERTIG bis auf die Anmeldung – claude auth login, dann Claude Code neu starten ===\n'
else
    printf '=== NICHT FERTIG – siehe die Meldung oben; ein erneuter Start setzt fort ===\n'
    exit 1
fi
