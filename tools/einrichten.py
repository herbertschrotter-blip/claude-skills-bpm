#!/usr/bin/env python3
"""Richtet die Plugins des Marketplace workbench auf einem Rechner ein (nur Standardbibliothek).

Wird von tools/install.sh bzw. tools/install.ps1 aufgerufen, nachdem git, Python 3 und Claude Code geprüft sind und der
Marketplace angelegt ist. Läuft auch allein: python3 tools/einrichten.py [--modus terminal|desktop] [--host NAME] [--ja]

Schritte (jeder mit Rückfrage, außer mit --ja):
  1. Plugins passend zum Rechner: terminal → work + skill-workshop, desktop → work-hooks (nie work und work-hooks zusammen)
  2. Plugin-Optionen log_host (Rechnername im Skill-Log) und log_repo (privates Sammel-Repo, optional)
  3. ~/.claude/settings.json: autoUpdate für workbench; im Terminal auf Wunsch skillOverrides für die Skills der Plugins,
     falls dieselben Skills auch bei claude.ai hochgeladen sind (Sicherung settings.json.bak)
  4. Probe: Hook-Skripte laufen mit dem gefundenen Python
"""

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys

MARKETPLACE = "workbench"
REPO = "herbertschrotter-blip/claude-workbench"
PLUGINS = {"terminal": ["work", "skill-workshop"], "desktop": ["work-hooks"]}
MIT_HOOKS = {"work", "work-hooks"}  # nur diese haben Optionen (userConfig) und Hooks
SETTINGS = os.path.join(os.path.expanduser("~"), ".claude", "settings.json")
PROTOKOLL = os.path.join(os.path.expanduser("~"), ".claude", "workbench-einrichtung.json")
SAMMEL_KLON = os.path.join(os.path.expanduser("~"), ".claude", "skill-log-sammel")


# --- reine Funktionen (getestet in test_einrichten.py) ---------------------------------------------------------------

def with_auto_update(settings):
    """settings.json mit autoUpdate: true für den Marketplace; vorhandene Quelle bleibt."""
    markets = settings.setdefault("extraKnownMarketplaces", {})
    entry = markets.setdefault(MARKETPLACE, {})
    entry.setdefault("source", {"source": "github", "repo": REPO})
    entry["autoUpdate"] = True
    return settings


def with_overrides(settings, skills):
    """skillOverrides "anthropic-skills:<name>": "off" für jeden Skill; andere Einträge bleiben."""
    overrides = settings.setdefault("skillOverrides", {})
    for name in skills:
        overrides.setdefault("anthropic-skills:" + name, "off")
    return settings


def merge_protokoll(alt, neue, jetzt=""):
    """Protokoll fortschreiben: ein Eintrag je (was, wert). Der erste Befund bleibt – was einmal "war-da" war, wird nie
    zu "installiert" (sonst würde --entfernen etwas löschen, das schon vorher da war); "entfernt" darf ihn ersetzen."""
    eintraege = {(e["was"], e.get("wert", "")): e for e in (alt or {}).get("eintraege", [])}
    for e in neue:
        key = (e["was"], e.get("wert", ""))
        if key not in eintraege or e.get("aktion") == "entfernt" or eintraege[key].get("aktion") == "entfernt":
            eintraege[key] = dict(e, am=e.get("am") or jetzt)
    return {"version": 1, "eintraege": sorted(eintraege.values(), key=lambda e: (e["was"], e.get("wert", "")))}


def offen(protokoll, was=None):
    """Einträge, die das Skript selbst angelegt hat und die noch nicht entfernt sind."""
    return [e for e in protokoll.get("eintraege", [])
            if e.get("aktion") == "installiert" and (was is None or e["was"] == was)]


def settings_entfernen(settings, eintraege):
    """Nimmt nur die protokollierten Einstellungen zurück; ein Override, den der Nutzer seither geändert hat, bleibt."""
    for e in eintraege:
        if e["was"] == "einstellung-autoupdate":
            entry = settings.get("extraKnownMarketplaces", {}).get(MARKETPLACE)
            if entry is not None:
                if e.get("neu_eintrag"):
                    settings["extraKnownMarketplaces"].pop(MARKETPLACE)
                    if not settings["extraKnownMarketplaces"]:
                        settings.pop("extraKnownMarketplaces")
                else:
                    entry.pop("autoUpdate", None)
        elif e["was"] == "einstellung-override":
            overrides = settings.get("skillOverrides", {})
            if overrides.get(e["wert"]) == "off":
                overrides.pop(e["wert"])
                if not overrides:
                    settings.pop("skillOverrides")
    return settings


def skills_of(marketplace, plugins):
    """Skill-Namen der Plugins aus marketplace.json (Einträge mit "skills": ["./skills/<name>", …])."""
    names = []
    for entry in marketplace.get("plugins", []):
        if entry.get("name") in plugins:
            names += [os.path.basename(p.rstrip("/")) for p in entry.get("skills", []) if isinstance(p, str)]
    return names


def plan(mode, installed):
    """(installieren, aktualisieren, entfernen) für den Modus; installed = Namen der installierten workbench-Plugins."""
    want = PLUGINS[mode]
    other = [p for p in PLUGINS["desktop" if mode == "terminal" else "terminal"] if p in installed]
    return [p for p in want if p not in installed], [p for p in want if p in installed], other


# --- Ein- und Ausgabe ------------------------------------------------------------------------------------------------

def ask(text, default, yes):
    if yes:
        return default
    hint = "J/n" if default else "j/N"
    answer = input(f"{text} [{hint}] ").strip().lower()
    return default if not answer else answer in ("j", "ja", "y", "yes")


def ask_text(text, default, yes):
    if yes:
        return default
    answer = input(f"{text} [{default}] ").strip()
    return answer or default


BALKEN = False  # --balken: Fortschritt als "##BALKEN <prozent> <text>" für install.ps1/install.sh


def balken(prozent, text):
    if BALKEN:
        print(f"##BALKEN {prozent} {text}")


def schritt(nummer, text):
    print(f"\n[{nummer}/5] {text}")


def ok(text):
    print(f"  OK  {text}")


def claude(*args, capture=True, stdin=None):
    exe = shutil.which("claude")
    if not exe:
        sys.exit("Claude Code (claude) nicht gefunden.")
    result = subprocess.run([exe, *args], capture_output=capture, text=True, input=stdin)
    if result.returncode != 0 and capture:
        print((result.stderr or result.stdout).strip())
    return result


def installed_plugins():
    out = claude("plugin", "list", "--json").stdout or "[]"
    return {p["id"].split("@")[0]: p for p in json.loads(out) if p.get("id", "").endswith("@" + MARKETPLACE)}


def marketplace_file():
    out = claude("plugin", "marketplace", "list", "--json").stdout or "[]"
    for m in json.loads(out):
        if m.get("name") == MARKETPLACE:
            path = os.path.join(m.get("installLocation", ""), ".claude-plugin", "marketplace.json")
            if os.path.exists(path):
                with open(path, encoding="utf-8") as fh:
                    return json.load(fh)
    sys.exit(f"Marketplace {MARKETPLACE} fehlt – zuerst: claude plugin marketplace add {REPO}")


def parse_settings(text):
    """(einstellungen, fehler): eine kaputte settings.json liefert einen lesbaren Fehler statt eines Tracebacks."""
    if not text.strip():
        return {}, None
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, f"Zeile {exc.lineno}, Spalte {exc.colno}: {exc.msg}"
    if not isinstance(data, dict):
        return None, "kein JSON-Objekt"
    return data, None


def load_settings():
    if not os.path.exists(SETTINGS):
        return {}, None
    with open(SETTINGS, encoding="utf-8") as fh:
        return parse_settings(fh.read())


def protokoll_laden():
    try:
        with open(PROTOKOLL, encoding="utf-8-sig") as fh:  # Windows PowerShell 5.1 schreibt UTF-8 mit BOM
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {"version": 1, "eintraege": []}


def protokoll_schreiben(neue):
    import datetime
    jetzt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    data = merge_protokoll(protokoll_laden(), neue, jetzt)
    os.makedirs(os.path.dirname(PROTOKOLL), exist_ok=True)
    with open(PROTOKOLL, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def save_settings(settings):
    os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
    if os.path.exists(SETTINGS):
        shutil.copyfile(SETTINGS, SETTINGS + ".bak")
    with open(SETTINGS, "w", encoding="utf-8") as fh:
        json.dump(settings, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def probe(installed):
    """Startet die Hook-Skripte mit abgeschaltetem Log/Wächter: Exit 0 heißt, Python und Skripte passen."""
    python3 = shutil.which("python3")
    if not python3:
        print("  python3 nicht gefunden – die Hooks rufen python3 auf (unter Windows: Python aus dem Microsoft Store"
              " oder App-Ausführungsalias python3 einschalten)")
        return False
    alles_ok = True
    for name, info in installed.items():
        if name not in MIT_HOOKS:
            continue
        base = info.get("installPath", "")
        hooks = os.path.join(base, "hooks") if name == "work-hooks" else os.path.join(base, "plugins", "work-hooks", "hooks")
        for script, env in (("skill_log.py", "SKILL_LOG"), ("skill_guard.py", "SKILL_GUARD")):
            path = os.path.join(hooks, script)
            if not os.path.exists(path):
                continue
            result = subprocess.run([python3, path], input="{}", text=True, capture_output=True,
                                    env=dict(os.environ, **{env: "aus"}))
            print(f"  {'OK    ' if result.returncode == 0 else 'FEHLER'}  {name}: {script}"
                  + ("" if result.returncode == 0 else f" (Exit {result.returncode}) {result.stderr.strip()[:200]}"))
            alles_ok = alles_ok and result.returncode == 0
    return alles_ok


def entfernen(yes):
    """Nimmt zurück, was laut Protokoll vom Skript stammt: Plugins, Marketplace, Einstellungen, auf Wunsch der Klon des
    Sammel-Repos. Programme, PATH und geplante Aufgabe erledigen install.ps1/install.sh (sie lesen dasselbe Protokoll)."""
    protokoll = protokoll_laden()
    neue = []
    plugins = offen(protokoll, "plugin")
    print("\n[Entfernen] Plugins und Marketplace")
    for e in plugins:
        if ask(f"Plugin {e['wert']} entfernen?", True, yes):
            claude("plugin", "uninstall", f"{e['wert']}@{MARKETPLACE}", capture=False)
            neue.append({"was": "plugin", "wert": e["wert"], "aktion": "entfernt"})
    for e in offen(protokoll, "marketplace"):
        if ask(f"Marketplace {e['wert']} entfernen?", True, yes):
            claude("plugin", "marketplace", "remove", e["wert"], capture=False)
            neue.append({"was": "marketplace", "wert": e["wert"], "aktion": "entfernt"})
    print("\n[Entfernen] Einstellungen")
    eintr = offen(protokoll, "einstellung-autoupdate") + offen(protokoll, "einstellung-override")
    settings, fehler = load_settings()
    if fehler:
        print(f"  FEHLER  {SETTINGS} ist kein gültiges JSON ({fehler}) – Einstellungen bitte von Hand zurücknehmen.")
    elif eintr and ask(f"autoUpdate und {len(offen(protokoll, 'einstellung-override'))} skillOverrides aus {SETTINGS} "
                       "zurücknehmen?", True, yes):
        save_settings(settings_entfernen(settings, eintr))
        neue += [dict(e, aktion="entfernt") for e in eintr]
        ok(f"zurückgenommen, Sicherung: {SETTINGS}.bak")
    if os.path.isdir(SAMMEL_KLON) and ask(f"Lokalen Klon des Sammel-Repos {SAMMEL_KLON} löschen (das Repo auf GitHub "
                                          "bleibt)?", False, yes):
        shutil.rmtree(SAMMEL_KLON, ignore_errors=True)
        ok("Klon gelöscht")
    protokoll_schreiben(neue)
    print("  Das Skill-Log (~/.claude/skill-log) bleibt erhalten.")
    return 0


def main():
    global BALKEN
    sys.stdout.reconfigure(line_buffering=True)  # Überschriften vor der Ausgabe von claude, auch umgeleitet
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--modus", choices=sorted(PLUGINS), help="terminal (work + skill-workshop) oder desktop (work-hooks)")
    parser.add_argument("--host", help="Rechnername im Skill-Log (Plugin-Option log_host)")
    parser.add_argument("--log-repo", help="privates Sammel-Repo owner/name für das Skill-Log (Plugin-Option log_repo)")
    parser.add_argument("--ja", action="store_true", help="alle Rückfragen mit dem Vorschlag beantworten")
    parser.add_argument("--mit-overrides", action="store_true", help="skillOverrides setzen, ohne zu fragen")
    parser.add_argument("--ohne-overrides", action="store_true", help="keine skillOverrides setzen")
    parser.add_argument("--balken", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--protokoll-zusatz", help=argparse.SUPPRESS)  # JSON-Datei mit Einträgen von install.ps1/.sh
    parser.add_argument("--entfernen", action="store_true", help="zurücknehmen, was laut Protokoll vom Skript stammt")
    parser.add_argument("--schritt", type=int, default=3, help=argparse.SUPPRESS)
    args = parser.parse_args()
    BALKEN = args.balken
    yes = args.ja
    nummer = args.schritt
    if args.entfernen:
        return entfernen(yes)
    neue = []
    if args.protokoll_zusatz:
        try:
            with open(args.protokoll_zusatz, encoding="utf-8-sig") as fh:
                zusatz = json.load(fh)
            neue += zusatz if isinstance(zusatz, list) else [zusatz]
        except (OSError, json.JSONDecodeError) as exc:
            print(f"  Hinweis: Protokoll-Zusatz nicht lesbar ({exc})")

    schritt(nummer, "Plugins")
    balken(0, "Plugins")
    mode = args.modus
    if not mode:
        desktop = ask("Läuft Claude hier in der Claude-Desktop-App (Skills kommen aus claude.ai)?", False, yes)
        mode = "desktop" if desktop else "terminal"
    host = args.host or ask_text("Rechnername im Skill-Log", socket.gethostname().split(".")[0], yes)
    repo = args.log_repo if args.log_repo is not None else ask_text(
        "Privates Sammel-Repo für das Skill-Log (owner/name, leer = keins)", "", yes)
    options = {"log_host": host, "log_repo": repo}
    print(f"  Modus {mode}: {', '.join(PLUGINS[mode])} - Rechner {host}")

    installed = installed_plugins()  # einmal lesen, danach im Speicher nachführen (jeder claude-Aufruf kostet Startzeit)
    install, update, remove = plan(mode, installed)
    schritte = max(1, len(install) + len(update) + len(remove))
    getan = 0
    for name in remove:
        if ask(f"{name} ist installiert und verträgt sich nicht mit {', '.join(PLUGINS[mode])}. Entfernen?", True, yes):
            balken(int(60 * getan / schritte), f"{name} entfernen")
            claude("plugin", "uninstall", f"{name}@{MARKETPLACE}", capture=False)
            neue.append({"was": "plugin", "wert": name, "aktion": "entfernt"})
        getan += 1
    for name in install:
        getan += 1
        if name == "skill-workshop" and not ask("skill-workshop (Arbeit an Skills) mit installieren?", True, yes):
            continue
        balken(int(60 * (getan - 1) / schritte), f"{name} installieren")
        config = ["--config", f"log_host={host}", *(["--config", f"log_repo={repo}"] if repo else [])] if name in MIT_HOOKS else []
        claude("plugin", "install", f"{name}@{MARKETPLACE}", *config, capture=False)
        neue.append({"was": "plugin", "wert": name, "aktion": "installiert"})
    for name in update:
        getan += 1
        balken(int(60 * (getan - 1) / schritte), f"{name} aktualisieren")
        claude("plugin", "update", f"{name}@{MARKETPLACE}", capture=False)
        if name in MIT_HOOKS:
            claude("plugin", "configure", f"{name}@{MARKETPLACE}", "--values-stdin", stdin=json.dumps(options))
        neue.append({"was": "plugin", "wert": name, "aktion": "war-da"})
    installed = installed_plugins()  # zweiter und letzter Aufruf: installPath für die Probe
    plugins = sorted(installed)
    ok("installiert: " + (", ".join(plugins) or "keine"))

    schritt(nummer + 1, "Einstellungen (~/.claude/settings.json)")
    balken(65, "Einstellungen")
    settings, fehler = load_settings()
    auto, overrides = None, 0
    if fehler:
        print(f"  FEHLER  {SETTINGS} ist kein gültiges JSON ({fehler}).")
        print("          Nichts geändert. Datei reparieren (oder die Sicherung settings.json.bak zurückholen) und erneut starten.")
    else:
        before = json.dumps(settings, sort_keys=True)
        alt_entry = settings.get("extraKnownMarketplaces", {}).get(MARKETPLACE)
        alt_overrides = set(settings.get("skillOverrides", {}))
        if not (alt_entry or {}).get("autoUpdate"):
            neue.append({"was": "einstellung-autoupdate", "wert": MARKETPLACE, "aktion": "installiert",
                         "neu_eintrag": alt_entry is None})
        with_auto_update(settings)
        if mode == "terminal" and not args.ohne_overrides:
            if args.mit_overrides or ask(
                    "Sind dieselben Skills auch bei claude.ai hochgeladen (dann skillOverrides gegen doppelte Skills)?", False, yes):
                with_overrides(settings, skills_of(marketplace_file(), PLUGINS["terminal"]))
                neue += [{"was": "einstellung-override", "wert": k, "aktion": "installiert"}
                         for k in settings["skillOverrides"] if k not in alt_overrides]
        if json.dumps(settings, sort_keys=True) != before:
            if ask(f"{SETTINGS} anpassen (autoUpdate{', skillOverrides' if 'skillOverrides' in settings else ''})?", True, yes):
                save_settings(settings)
                ok(f"gespeichert, Sicherung: {SETTINGS}.bak")
        else:
            ok("schon richtig")
        auto = settings.get("extraKnownMarketplaces", {}).get(MARKETPLACE, {}).get("autoUpdate")
        overrides = sum(1 for k in settings.get("skillOverrides", {}) if k.startswith("anthropic-skills:"))

    protokoll_schreiben(neue)

    schritt(nummer + 2, "Probe der Hooks")
    balken(85, "Probe der Hooks")
    passt = probe(installed)
    balken(100, "Plugins fertig")

    print("\nZusammenfassung")
    print(f"  Rechner        {host}")
    print(f"  Sammel-Repo    {repo or 'keins'}")
    print(f"  Plugins        {', '.join(plugins) or 'keine'}")
    print(f"  Auto-Update    {'an' if auto else ('?' if fehler else 'aus')}")
    print(f"  skillOverrides {overrides}")
    print(f"  Hooks          {'laufen' if passt else 'FEHLER - siehe oben'}")
    return 0 if passt and not fehler else 1


if __name__ == "__main__":
    sys.exit(main())
