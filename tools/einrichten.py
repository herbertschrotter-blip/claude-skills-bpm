#!/usr/bin/env python3
"""Richtet die Plugins des Marketplace workbench auf einem Rechner ein (nur Standardbibliothek).

Wird von tools/install.sh bzw. tools/install.ps1 aufgerufen, nachdem git, Python 3 und Claude Code geprüft sind und der
Marketplace angelegt ist. Läuft auch allein: python3 tools/einrichten.py [--modus terminal|desktop] [--host NAME] [--ja]

Schritte (jeder mit Rückfrage, außer mit --ja):
  1. Plugins passend zum Rechner: terminal → work + skill-workshop, desktop → work-hooks (nie work und work-hooks zusammen)
  2. Plugin-Option log_host (Rechnername im Skill-Log)
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
SETTINGS = os.path.join(os.path.expanduser("~"), ".claude", "settings.json")


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


def load_settings():
    if not os.path.exists(SETTINGS):
        return {}
    with open(SETTINGS, encoding="utf-8") as fh:
        return json.load(fh)


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


def main():
    sys.stdout.reconfigure(line_buffering=True)  # Überschriften vor der Ausgabe von claude, auch umgeleitet
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--modus", choices=sorted(PLUGINS), help="terminal (work + skill-workshop) oder desktop (work-hooks)")
    parser.add_argument("--host", help="Rechnername im Skill-Log (Plugin-Option log_host)")
    parser.add_argument("--ja", action="store_true", help="alle Rückfragen mit dem Vorschlag beantworten")
    parser.add_argument("--ohne-overrides", action="store_true", help="keine skillOverrides setzen")
    parser.add_argument("--schritt", type=int, default=3, help=argparse.SUPPRESS)
    args = parser.parse_args()
    yes = args.ja
    nummer = args.schritt

    schritt(nummer, "Plugins")
    mode = args.modus
    if not mode:
        desktop = ask("Läuft Claude hier in der Claude-Desktop-App (Skills kommen aus claude.ai)?", False, yes)
        mode = "desktop" if desktop else "terminal"
    host = args.host or ask_text("Rechnername im Skill-Log", socket.gethostname().split(".")[0], yes)
    print(f"  Modus {mode}: {', '.join(PLUGINS[mode])} - Rechner {host}")

    installed = installed_plugins()
    install, update, remove = plan(mode, installed)
    for name in remove:
        if ask(f"{name} ist installiert und verträgt sich nicht mit {', '.join(PLUGINS[mode])}. Entfernen?", True, yes):
            claude("plugin", "uninstall", f"{name}@{MARKETPLACE}", capture=False)
    for name in install:
        if name == "skill-workshop" and not ask("skill-workshop (Arbeit an Skills) mit installieren?", True, yes):
            continue
        claude("plugin", "install", f"{name}@{MARKETPLACE}", "--config", f"log_host={host}", capture=False)
    for name in update:
        claude("plugin", "update", f"{name}@{MARKETPLACE}", capture=False)
        claude("plugin", "configure", f"{name}@{MARKETPLACE}", "--values-stdin", stdin=json.dumps({"log_host": host}))
    plugins = sorted(installed_plugins())
    ok("installiert: " + (", ".join(plugins) or "keine"))

    schritt(nummer + 1, "Einstellungen (~/.claude/settings.json)")

    settings = load_settings()
    before = json.dumps(settings, sort_keys=True)
    with_auto_update(settings)
    if mode == "terminal" and not args.ohne_overrides:
        if ask("Sind dieselben Skills auch bei claude.ai hochgeladen (dann skillOverrides gegen doppelte Skills)?", False, yes):
            with_overrides(settings, skills_of(marketplace_file(), PLUGINS["terminal"]))
    if json.dumps(settings, sort_keys=True) != before:
        if ask(f"{SETTINGS} anpassen (autoUpdate{', skillOverrides' if 'skillOverrides' in settings else ''})?", True, yes):
            save_settings(settings)
            ok(f"gespeichert, Sicherung: {SETTINGS}.bak")
    else:
        ok("schon richtig")
    auto = load_settings().get("extraKnownMarketplaces", {}).get(MARKETPLACE, {}).get("autoUpdate")
    overrides = sum(1 for k in load_settings().get("skillOverrides", {}) if k.startswith("anthropic-skills:"))

    schritt(nummer + 2, "Probe der Hooks")
    passt = probe(installed_plugins())

    print("\nZusammenfassung")
    print(f"  Rechner        {host}")
    print(f"  Plugins        {', '.join(plugins) or 'keine'}")
    print(f"  Auto-Update    {'an' if auto else 'aus'}")
    print(f"  skillOverrides {overrides}")
    print(f"  Hooks          {'laufen' if passt else 'FEHLER - siehe oben'}")
    return 0 if passt else 1


if __name__ == "__main__":
    sys.exit(main())
