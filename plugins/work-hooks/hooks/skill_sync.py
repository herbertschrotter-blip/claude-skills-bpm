#!/usr/bin/env python3
"""Abgleich des Skill-Logs mit einem privaten Sammel-Repo (docs/skill-log-v1.md, Abschnitt „Sammel-Repo“).

Hook für SessionStart: startet den Abgleich als Hintergrundprozess und endet sofort – die Sitzung wartet nie. Der
Hintergrundprozess klont das Repo beim ersten Mal nach ~/.claude/skill-log-sammel, holt den Stand der anderen Rechner
(pull --rebase), kopiert die eigenen Monatsdateien nach logs/<rechner>/, committet und pusht. Jeder Fehler bleibt
still (Netz, Zugang); das Ergebnis steht in ~/.claude/skill-log/sammel-status.json.

Einstellungen – Umgebungsvariable oder Plugin-Option (/plugin configure); die Umgebungsvariable gewinnt:
  SKILL_LOG_REPO / log_repo   GitHub-Repo owner/name (privat!); leer = kein Abgleich
  SKILL_LOG_HOST / log_host   Name des Rechners (Unterordner in logs/), sonst Hostname
  SKILL_LOG_DIR  / log_dir    lokales Skill-Log (Standard: ~/.claude/skill-log)
"""

import datetime
import glob
import json
import os
import re
import shutil
import socket
import subprocess
import sys

MONTH_FILE = re.compile(r"^\d{4}-\d{2}\.jsonl$")
REPO_NAME = re.compile(r"^[\w.-]+/[\w.-]+$")
HOME = os.path.expanduser("~")
CLONE = os.path.join(HOME, ".claude", "skill-log-sammel")


def setting(env, option):
    """Wert aus der Umgebungsvariable, sonst aus der Plugin-Option (userConfig → CLAUDE_PLUGIN_OPTION_<KEY>)."""
    return os.environ.get(env) or os.environ.get("CLAUDE_PLUGIN_OPTION_" + option) or ""


def host_name():
    name = setting("SKILL_LOG_HOST", "LOG_HOST") or socket.gethostname()
    return re.sub(r"[^\w.-]", "_", name) or "rechner"


def git(*args, cwd=CLONE, timeout=60):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=timeout,
                          env=dict(os.environ, GIT_TERMINAL_PROMPT="0"))


def copy_own(source, target):
    """Eigene Monatsdateien ins Repo kopieren; liefert die Zahl der geänderten Dateien."""
    os.makedirs(target, exist_ok=True)
    changed = 0
    for path in glob.glob(os.path.join(source, "*.jsonl")):
        name = os.path.basename(path)
        if not MONTH_FILE.match(name):
            continue
        dest = os.path.join(target, name)
        if os.path.exists(dest) and os.path.getsize(dest) == os.path.getsize(path):
            continue
        shutil.copyfile(path, dest)
        changed += 1
    return changed


def run(repo):
    status = {"ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "repo": repo}
    source = setting("SKILL_LOG_DIR", "LOG_DIR") or os.path.join(HOME, ".claude", "skill-log")
    lock = os.path.join(source, "sammel.lock")
    os.makedirs(source, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
    except FileExistsError:
        # Sperre älter als 10 Minuten: liegengeblieben, übernehmen
        if datetime.datetime.now().timestamp() - os.path.getmtime(lock) < 600:
            return
    try:
        if not os.path.isdir(os.path.join(CLONE, ".git")):
            result = git("clone", "-q", f"https://github.com/{repo}.git", CLONE, cwd=HOME, timeout=120)
            if result.returncode != 0:
                status["fehler"] = "clone: " + result.stderr.strip()[-300:]
                return
        git("pull", "-q", "--rebase")
        host = host_name()
        status["rechner"] = host
        status["dateien"] = copy_own(source, os.path.join(CLONE, "logs", host))
        git("add", "-A", "logs")
        if git("diff", "--cached", "--quiet").returncode != 0:
            git("-c", "user.name=skill-log", "-c", "user.email=skill-log@localhost",
                "commit", "-q", "-m", f"Skill-Log {host} {status['ts']}")
            push = git("push", "-q")
            if push.returncode != 0:
                git("pull", "-q", "--rebase")
                push = git("push", "-q")
            status["push"] = "ok" if push.returncode == 0 else "fehler: " + push.stderr.strip()[-300:]
        else:
            status["push"] = "nichts Neues"
    except Exception as exc:  # noqa: BLE001 – ein Abgleich darf nie stören
        status["fehler"] = repr(exc)[-300:]
    finally:
        try:
            with open(os.path.join(source, "sammel-status.json"), "w", encoding="utf-8") as fh:
                json.dump(status, fh, ensure_ascii=False, indent=1)
            os.remove(lock)
        except OSError:
            pass


def main():
    try:
        sys.stdin.read()
    except Exception:  # noqa: BLE001
        pass
    repo = setting("SKILL_LOG_REPO", "LOG_REPO").strip()
    if not repo or not REPO_NAME.match(repo) or not shutil.which("git"):
        return 0
    if "--jetzt" in sys.argv:
        run(repo)
        return 0
    try:
        kwargs = {"stdin": subprocess.DEVNULL, "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL,
                  "env": dict(os.environ, SKILL_LOG_REPO=repo)}
        if os.name == "nt":
            kwargs["creationflags"] = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        else:
            kwargs["start_new_session"] = True
        subprocess.Popen([sys.executable, os.path.abspath(__file__), "--jetzt"], **kwargs)
    except Exception:  # noqa: BLE001 – der Hook endet immer mit 0
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
