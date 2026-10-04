#!/usr/bin/env python3
"""sitzung – Claude-Code-Gespräche und tmux-Fenster auflisten, öffnen, verwalten.

Liest die Gespräche aus ~/.claude/projects/*/<id>.jsonl und die laufenden Sitzungen aus ~/.claude/sessions/<pid>.json.
Steuert tmux über die Kommandozeile. Nur Standardbibliothek. Jede Ausgabe gibt es mit --json auch maschinenlesbar.

Aufruf: python3 sitzung.py <befehl> [argumente] [--json]
Befehle: liste, fenster, oeffnen, neu, wechseln, fenster-umbenennen, verschieben, holen, schliessen, neustart,
         umbenennen, suche, vorschau, merken, wiederherstellen, archivieren, zurueckholen, archiv, loeschen, leer
"""
import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime

HOME = os.path.expanduser("~")
CLAUDE = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(HOME, ".claude")
PROJECTS = os.path.join(CLAUDE, "projects")
SESSIONS = os.path.join(CLAUDE, "sessions")
EIGEN = os.path.join(CLAUDE, "sitzung")
ARCHIV = os.path.join(EIGEN, "archiv")
ARBEITSPLATZ = os.path.join(EIGEN, "arbeitsplatz.json")


class Fehler(Exception):
    pass


# ---------- Hilfen ----------

def sh(*args, check=True):
    r = subprocess.run(list(args), capture_output=True, text=True)
    if check and r.returncode != 0:
        raise Fehler("%s: %s" % (" ".join(args[:2]), (r.stderr or r.stdout).strip()))
    return r.stdout


def tmux_da():
    return shutil.which("tmux") is not None and subprocess.run(
        ["tmux", "ls"], capture_output=True).returncode == 0


def hauptsitzung(wunsch=None):
    """Ziel-Sitzung: ausdrücklich gewünscht, sonst die des eigenen Fensters, sonst die erste."""
    if wunsch:
        return wunsch
    if os.environ.get("TMUX"):
        name = sh("tmux", "display-message", "-p", "#S", check=False).strip()
        if name:
            return name
    if not tmux_da():
        raise Fehler("tmux läuft nicht")
    return sh("tmux", "list-sessions", "-F", "#S").split("\n")[0].strip()


def zeit(ts):
    if not ts:
        return ""
    try:
        if isinstance(ts, (int, float)):
            d = datetime.fromtimestamp(ts / 1000 if ts > 1e11 else ts)
        else:
            d = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()
        return d.strftime("%d.%m. %H:%M")
    except Exception:
        return str(ts)[:16]


def kurz(text, n=70):
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def text_aus(msg):
    c = (msg or {}).get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
    return ""


def echte_eingabe(d):
    if d.get("type") != "user" or d.get("isMeta") or d.get("isSidechain"):
        return ""
    t = text_aus(d.get("message")).strip()
    if not t or t.startswith("<") or t.startswith("This session is being continued"):
        return ""
    return t


# ---------- laufende Sitzungen ----------

def lebt(pid, start):
    try:
        with open("/proc/%d/stat" % int(pid)) as f:
            felder = f.read().rsplit(")", 1)[1].split()
        return not start or felder[19] == str(start)
    except Exception:
        return False


def registrierte():
    """Einträge aus ~/.claude/sessions: laufend und verwaist (Prozess weg, z. B. nach einem Neustart)."""
    out = []
    if not os.path.isdir(SESSIONS):
        return out
    for n in os.listdir(SESSIONS):
        if not n.endswith(".json"):
            continue
        try:
            d = json.load(open(os.path.join(SESSIONS, n)))
        except Exception:
            continue
        d["laeuft"] = lebt(d.get("pid", 0), d.get("procStart"))
        out.append(d)
    return out


def pane_zu_fenster():
    """%pane -> {sitzung, index, name, pfad}"""
    if not tmux_da():
        return {}
    out = {}
    fmt = "#{pane_id}\t#{session_name}\t#{window_index}\t#{window_name}\t#{pane_current_path}\t#{window_id}"
    for z in sh("tmux", "list-panes", "-a", "-F", fmt, check=False).splitlines():
        p = z.split("\t")
        if len(p) == 6:
            out[p[0]] = {"sitzung": p[1], "index": int(p[2]), "fenster": p[3], "pfad": p[4], "window_id": p[5]}
    return out


def laufende():
    """sessionId -> Eintrag mit Fenster (nur lebende Prozesse)."""
    panes = pane_zu_fenster()
    out = {}
    for d in registrierte():
        if not d["laeuft"]:
            continue
        pane = (d.get("tmux") or "").rsplit(".", 1)[-1]
        d["ort"] = panes.get(pane)
        out[d.get("sessionId")] = d
    return out


# ---------- Gespräche ----------

def dateien(wurzel=PROJECTS):
    if not os.path.isdir(wurzel):
        return []
    out = []
    for ordner in os.listdir(wurzel):
        p = os.path.join(wurzel, ordner)
        if os.path.isdir(p):
            out += [os.path.join(p, f) for f in os.listdir(p) if f.endswith(".jsonl")]
    return out


def lies(pfad, voll=False):
    g = {"id": os.path.basename(pfad)[:-6], "datei": pfad, "name": "", "titel": "", "ordner": "", "erste": "",
         "letzte": "", "beginn": "", "ende": "", "eingaben": 0, "nachrichten": 0, "kontext": 0,
         "groesse": os.path.getsize(pfad)}
    verlauf = []
    with open(pfad, errors="ignore") as f:
        for z in f:
            try:
                d = json.loads(z)
            except Exception:
                continue
            t = d.get("type")
            if t == "custom-title":
                g["name"] = d.get("customTitle", "")
            elif t == "agent-name" and not g["name"]:
                g["name"] = d.get("agentName", "")
            elif t == "ai-title":
                g["titel"] = d.get("aiTitle") or d.get("title") or g["titel"]
            ts = d.get("timestamp")
            if ts:
                g["beginn"] = g["beginn"] or ts
                g["ende"] = ts
            if d.get("cwd") and not g["ordner"]:
                g["ordner"] = d["cwd"]
            if t in ("user", "assistant") and not d.get("isSidechain"):
                g["nachrichten"] += 1
            if t == "assistant" and not d.get("isSidechain"):
                u = (d.get("message") or {}).get("usage") or {}
                k = sum(u.get(x) or 0 for x in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
                if k:
                    g["kontext"] = k
            e = echte_eingabe(d)
            if e:
                g["eingaben"] += 1
                g["erste"] = g["erste"] or e
                g["letzte"] = e
            if voll and t in ("user", "assistant") and not d.get("isSidechain"):
                txt = e if t == "user" else text_aus(d.get("message"))
                if txt.strip():
                    verlauf.append({"wer": "du" if t == "user" else "claude", "zeit": ts, "text": txt})
    if not g["ordner"]:
        g["ordner"] = "?"
    if voll:
        g["verlauf"] = verlauf
    return g


def alle(wurzel=PROJECTS):
    lauf = laufende()
    out = []
    for p in dateien(wurzel):
        g = lies(p)
        r = lauf.get(g["id"])
        if r:
            g["zustand"] = {"busy": "arbeitet", "idle": "wartet"}.get(r.get("status"), r.get("status") or "läuft")
            g["fenster"] = r.get("ort")
            g["name"] = r.get("name") if r.get("nameSource") == "user" else (g["name"] or "")
        else:
            g["zustand"] = "ruht"
        out.append(g)
    out.sort(key=lambda g: g["ende"] or "", reverse=True)
    return out


def finde(teil, wurzel=PROJECTS):
    teil = teil.strip().lower()
    treffer = [p for p in dateien(wurzel) if os.path.basename(p).lower().startswith(teil)]
    if not treffer:
        treffer = [p for p in dateien(wurzel) if (lies(p)["name"] or "").lower() == teil]
    if not treffer:
        raise Fehler("kein Gespräch zu „%s“" % teil)
    if len(treffer) > 1:
        raise Fehler("„%s“ ist nicht eindeutig: %s" % (teil, ", ".join(os.path.basename(t)[:8] for t in treffer)))
    return treffer[0]


def anzeigename(g):
    return g["name"] or kurz(g["titel"], 40) or os.path.basename(g["ordner"].rstrip("/")) or g["id"][:8]


# ---------- Fenster ----------

def fenster_liste():
    if not tmux_da():
        raise Fehler("tmux läuft nicht")
    lauf = {}
    for sid, d in laufende().items():
        if d.get("ort"):
            lauf[d["ort"]["window_id"]] = d
    fmt = "#{session_name}\t#{window_index}\t#{window_name}\t#{pane_current_path}\t#{pane_current_command}\t" \
          "#{window_active}\t#{window_id}"
    out = []
    for z in sh("tmux", "list-windows", "-a", "-F", fmt).splitlines():
        p = z.split("\t")
        if len(p) != 7:
            continue
        d = lauf.get(p[6])
        out.append({"sitzung": p[0], "index": int(p[1]), "name": p[2], "pfad": p[3], "befehl": p[4],
                    "aktiv": p[5] == "1", "window_id": p[6],
                    "gespraech": d.get("sessionId") if d else "",
                    "gespraech_name": (d.get("name") if d else ""),
                    "zustand": ({"busy": "arbeitet", "idle": "wartet"}.get(d.get("status"), "läuft") if d else
                                ("Shell" if p[4] in ("bash", "sh", "zsh", "ash") else p[4]))})
    return out


def ziel(angabe, sitzung=None):
    """Fenster über 'Sitzung:Index', Index (in der Hauptsitzung) oder Namen finden."""
    fl = fenster_liste()
    if ":" in angabe:
        s, i = angabe.rsplit(":", 1)
        t = [f for f in fl if f["sitzung"] == s and (str(f["index"]) == i or f["name"] == i)]
    elif angabe.isdigit():
        s = hauptsitzung(sitzung)
        t = [f for f in fl if f["sitzung"] == s and f["index"] == int(angabe)]
    else:
        t = [f for f in fl if f["name"] == angabe] or [f for f in fl if f["name"].lower() == angabe.lower()]
    if not t:
        raise Fehler("kein Fenster „%s“" % angabe)
    if len(t) > 1:
        raise Fehler("„%s“ ist nicht eindeutig: %s" % (angabe, ", ".join("%s:%d" % (f["sitzung"], f["index"]) for f in t)))
    return t[0]


def hinwechseln(window_id):
    sh("tmux", "select-window", "-t", window_id)
    sess = sh("tmux", "display-message", "-p", "-t", window_id, "#S").strip()
    if os.environ.get("TMUX"):
        sh("tmux", "switch-client", "-t", sess, check=False)


def claude_befehl(gid=None, name="", fork=False, fernsteuerung=True):
    teile = ["claude"]
    if gid:
        teile += ["--resume", gid]
        if fork:
            teile.append("--fork-session")
    if fernsteuerung:
        teile += ["--remote-control", name]
    elif name:
        teile += ["-n", name]
    return " ".join(shlex.quote(t) for t in teile)


def warten_bereit(window_id, sekunden=30):
    ende = time.time() + sekunden
    while time.time() < ende:
        bild = sh("tmux", "capture-pane", "-p", "-t", window_id, check=False)
        if re.search(r"remote.control|Claude Code|╭|>\s*$", bild, re.I):
            return True
        time.sleep(1)
    return False


def oeffne(gid_teil, name=None, sitzung=None, fork=False, fernsteuerung=True, still=False):
    g = lies(finde(gid_teil))
    r = laufende().get(g["id"])
    if r and not fork:
        if r.get("ort"):
            if not still:
                hinwechseln(r["ort"]["window_id"])
            return {"aktion": "gewechselt", "gespraech": g["id"], "fenster": r["ort"]}
        raise Fehler("Gespräch läuft schon außerhalb von tmux (PID %s); nicht doppelt öffnen" % r.get("pid"))
    if not os.path.isdir(g["ordner"]):
        raise Fehler("Ordner %s gibt es nicht mehr" % g["ordner"])
    name = name or anzeigename(g)
    s = hauptsitzung(sitzung)
    wid = sh("tmux", "new-window", "-d", "-P", "-F", "#{window_id}", "-t", s + ":", "-n", name, "-c", g["ordner"],
             claude_befehl(g["id"], name, fork, fernsteuerung)).strip()
    sh("tmux", "set-window-option", "-t", wid, "automatic-rename", "off", check=False)
    bereit = warten_bereit(wid)
    if not still:
        hinwechseln(wid)
    idx = sh("tmux", "display-message", "-p", "-t", wid, "#{window_index}").strip()
    return {"aktion": "abgezweigt" if fork else "geöffnet", "gespraech": g["id"], "ordner": g["ordner"],
            "fenster": {"sitzung": s, "index": int(idx), "fenster": name, "window_id": wid}, "bereit": bereit,
            "fernsteuerung": fernsteuerung}


# ---------- Befehle ----------

def b_liste(a):
    gs = alle()
    if a.ordner:
        o = a.ordner.rstrip("/")
        gs = [g for g in gs if g["ordner"].rstrip("/") == o or os.path.basename(g["ordner"].rstrip("/")) == o]
    if not a.alle:
        gs = gs[: a.n]
    return gs


def b_projekte(a):
    """Ordner, in denen Gespräche liegen: Anzahl, zuletzt aktiv, wie viele gerade laufen."""
    proj = {}
    for g in alle():
        p = proj.setdefault(g["ordner"], {"ordner": g["ordner"], "name": os.path.basename(g["ordner"].rstrip("/")) or "/",
                                          "gespraeche": 0, "laufen": 0, "ende": ""})
        p["gespraeche"] += 1
        p["laufen"] += g["zustand"] != "ruht"
        p["ende"] = max(p["ende"], g["ende"] or "")
    return sorted(proj.values(), key=lambda p: p["ende"], reverse=True)


def b_fenster(a):
    return fenster_liste()


def b_oeffnen(a):
    return oeffne(a.gespraech, a.name, a.sitzung, a.abzweigen, not a.ohne_fernsteuerung)


def b_neu(a):
    ordner = os.path.abspath(a.ordner)
    if not os.path.isdir(ordner):
        raise Fehler("Ordner %s gibt es nicht" % ordner)
    name = a.name or os.path.basename(ordner.rstrip("/"))
    s = hauptsitzung(a.sitzung)
    wid = sh("tmux", "new-window", "-d", "-P", "-F", "#{window_id}", "-t", s + ":", "-n", name, "-c", ordner,
             claude_befehl(None, name, False, not a.ohne_fernsteuerung)).strip()
    sh("tmux", "set-window-option", "-t", wid, "automatic-rename", "off", check=False)
    bereit = warten_bereit(wid)
    hinwechseln(wid)
    return {"aktion": "neu", "ordner": ordner, "fenster": {"sitzung": s, "fenster": name, "window_id": wid},
            "bereit": bereit}


def b_wechseln(a):
    f = ziel(a.fenster, a.sitzung)
    hinwechseln(f["window_id"])
    return {"aktion": "gewechselt", "fenster": f}


def b_fenster_umbenennen(a):
    f = ziel(a.fenster, a.sitzung)
    sh("tmux", "rename-window", "-t", f["window_id"], a.name)
    sh("tmux", "set-window-option", "-t", f["window_id"], "automatic-rename", "off", check=False)
    return {"aktion": "umbenannt", "alt": f["name"], "neu": a.name}


def b_verschieben(a):
    """Fenster an eine andere Stelle der Leiste: tauscht mit dem Fenster an der Zielstelle oder rückt dorthin."""
    f = ziel(a.fenster, a.sitzung)
    belegt = [x for x in fenster_liste() if x["sitzung"] == f["sitzung"] and x["index"] == a.stelle]
    if belegt:
        sh("tmux", "swap-window", "-d", "-s", f["window_id"], "-t", belegt[0]["window_id"])
    else:
        sh("tmux", "move-window", "-s", f["window_id"], "-t", "%s:%d" % (f["sitzung"], a.stelle))
    return {"aktion": "verschoben", "fenster": f["name"], "stelle": a.stelle}


def b_holen(a):
    """Fenster aus einer anderen tmux-Sitzung in die Hauptsitzung holen (dort sieht man es am Handy)."""
    s = hauptsitzung(a.sitzung)
    geholt = []
    quellen = [ziel(a.fenster)] if a.fenster else [f for f in fenster_liste() if f["sitzung"] != s]
    eigen = sh("tmux", "display-message", "-p", "#{window_id}", check=False).strip() if os.environ.get("TMUX") else ""
    for f in quellen:
        if f["sitzung"] == s or f["window_id"] == eigen:
            continue
        sh("tmux", "move-window", "-s", f["window_id"], "-t", s + ":")
        geholt.append("%s:%d %s" % (f["sitzung"], f["index"], f["name"]))
    return {"aktion": "geholt", "nach": s, "fenster": geholt}


def b_schliessen(a):
    f = ziel(a.fenster, a.sitzung)
    if f["zustand"] == "arbeitet" and not a.erzwingen:
        raise Fehler("In „%s“ arbeitet Claude gerade; erst warten oder --erzwingen" % f["name"])
    if f["aktiv"] and os.environ.get("TMUX") and f["window_id"] == sh(
            "tmux", "display-message", "-p", "#{window_id}").strip() and not a.erzwingen:
        raise Fehler("Das ist das eigene Fenster; nicht von hier aus schließen")
    sh("tmux", "kill-window", "-t", f["window_id"])
    if f["gespraech"]:
        time.sleep(1)
        vergessen([f["gespraech"]])
    return {"aktion": "geschlossen", "fenster": f["name"], "gespraech": f["gespraech"]}


def b_neustart(a):
    f = ziel(a.fenster, a.sitzung)
    if not f["gespraech"]:
        raise Fehler("In „%s“ läuft kein Claude-Gespräch" % f["name"])
    if f["zustand"] == "arbeitet" and not a.erzwingen:
        raise Fehler("In „%s“ arbeitet Claude gerade; erst warten oder --erzwingen" % f["name"])
    g = lies(finde(f["gespraech"]))
    sh("tmux", "respawn-window", "-k", "-t", f["window_id"], "-c", g["ordner"],
       claude_befehl(g["id"], f["name"], False, not a.ohne_fernsteuerung))
    return {"aktion": "neu gestartet", "fenster": f["name"], "gespraech": g["id"], "bereit": warten_bereit(f["window_id"])}


def b_umbenennen(a):
    pfad = finde(a.gespraech)
    gid = os.path.basename(pfad)[:-6]
    if gid in laufende():
        raise Fehler("Das Gespräch läuft gerade; dort mit /rename %s umbenennen" % a.name)
    with open(pfad, "a") as f:
        f.write(json.dumps({"type": "custom-title", "customTitle": a.name, "sessionId": gid}, ensure_ascii=False) + "\n")
        f.write(json.dumps({"type": "agent-name", "agentName": a.name, "sessionId": gid}, ensure_ascii=False) + "\n")
    return {"aktion": "umbenannt", "gespraech": gid, "name": a.name}


def b_suche(a):
    muster = re.compile(re.escape(a.text), re.I)
    out = []
    for p in dateien():
        g = lies(p, voll=True)
        hits = []
        for v in g.pop("verlauf"):
            m = muster.search(v["text"])
            if m:
                s = max(0, m.start() - 40)
                hits.append({"wer": v["wer"], "zeit": v["zeit"], "stelle": kurz(v["text"][s:s + 140], 140)})
        if hits:
            g["treffer"] = len(hits)
            g["beispiele"] = hits[:3]
            out.append(g)
    out.sort(key=lambda g: (g["treffer"], g["ende"]), reverse=True)
    return out[: a.n]


def b_vorschau(a):
    g = lies(finde(a.gespraech), voll=True)
    v = g.pop("verlauf")
    g["verlauf"] = [{"wer": x["wer"], "zeit": x["zeit"], "text": kurz(x["text"], 300)} for x in v[-a.n:]]
    return g


def b_merken(a):
    fl = [f for f in fenster_liste() if f["gespraech"]]
    stand = {"gemerkt": datetime.now().astimezone().isoformat(timespec="seconds"),
             "fenster": [{"sitzung": f["sitzung"], "index": f["index"], "name": f["name"], "gespraech": f["gespraech"],
                          "ordner": f["pfad"]} for f in fl]}
    os.makedirs(EIGEN, exist_ok=True)
    json.dump(stand, open(ARBEITSPLATZ, "w"), ensure_ascii=False, indent=1)
    return stand


def kandidaten():
    """Was wiederhergestellt werden kann: gemerkter Arbeitsplatz und verwaiste Einträge (Prozess weg)."""
    lauf = laufende()
    out = {}
    if os.path.exists(ARBEITSPLATZ):
        for f in json.load(open(ARBEITSPLATZ)).get("fenster", []):
            out[f["gespraech"]] = {"gespraech": f["gespraech"], "name": f["name"], "ordner": f["ordner"],
                                   "quelle": "gemerkt"}
    for d in registrierte():
        sid = d.get("sessionId")
        if d["laeuft"] or not sid or sid in out:
            continue
        out[sid] = {"gespraech": sid, "name": d.get("name") if d.get("nameSource") == "user" else "",
                    "ordner": d.get("cwd"), "quelle": "beim Beenden offen", "seit": zeit(d.get("updatedAt"))}
    erg = []
    for sid, k in out.items():
        if sid in lauf:
            continue
        try:
            g = lies(finde(sid))
        except Fehler:
            continue
        k["name"] = k["name"] or anzeigename(g)
        k["ende"] = g["ende"]
        erg.append(k)
    erg.sort(key=lambda k: k.get("ende") or "", reverse=True)
    return erg


def vergessen(ids):
    """Verwaiste Einträge aus ~/.claude/sessions entfernen, damit sie nicht mehr als „beim Beenden offen“ gelten."""
    for d in registrierte():
        if not d["laeuft"] and d.get("sessionId") in set(ids):
            try:
                os.remove(os.path.join(SESSIONS, "%s.json" % d["pid"]))
            except OSError:
                pass


def b_wiederherstellen(a):
    ks = kandidaten()
    if not a.ids and not a.alle:
        return {"kandidaten": ks}
    wahl = ks if a.alle else [k for k in ks if any(k["gespraech"].startswith(i) for i in a.ids)]
    erg = []
    for k in wahl:
        try:
            erg.append(oeffne(k["gespraech"], k["name"], a.sitzung, still=True))
        except Fehler as e:
            erg.append({"aktion": "fehler", "gespraech": k["gespraech"], "grund": str(e)})
    vergessen([k["gespraech"] for k in wahl])
    return {"wiederhergestellt": erg}


def verschiebe(gid, von, nach):
    for p in dateien(von):
        if os.path.basename(p)[:-6] == gid:
            rel = os.path.relpath(os.path.dirname(p), von)
            os.makedirs(os.path.join(nach, rel), exist_ok=True)
            shutil.move(p, os.path.join(nach, rel, gid + ".jsonl"))
            ordner = os.path.join(os.path.dirname(p), gid)
            if os.path.isdir(ordner):
                shutil.move(ordner, os.path.join(nach, rel, gid))
            return os.path.join(rel, gid)
    raise Fehler("Gespräch %s nicht gefunden" % gid)


def b_archivieren(a):
    out = []
    for teil in a.gespraeche:
        gid = os.path.basename(finde(teil))[:-6]
        if gid in laufende():
            raise Fehler("Gespräch %s läuft gerade; erst das Fenster schließen" % gid[:8])
        out.append(verschiebe(gid, PROJECTS, ARCHIV))
    return {"aktion": "archiviert", "gespraeche": out}


def b_zurueckholen(a):
    out = []
    for teil in a.gespraeche:
        gid = os.path.basename(finde(teil, ARCHIV))[:-6]
        out.append(verschiebe(gid, ARCHIV, PROJECTS))
    return {"aktion": "zurückgeholt", "gespraeche": out}


def b_archiv(a):
    return sorted((lies(p) for p in dateien(ARCHIV)), key=lambda g: g["ende"] or "", reverse=True)


def b_loeschen(a):
    if not a.ja:
        raise Fehler("Löschen ist endgültig; nur mit --ja")
    out = []
    for teil in a.gespraeche:
        for wurzel in (ARCHIV, PROJECTS):
            try:
                p = finde(teil, wurzel)
            except Fehler:
                continue
            gid = os.path.basename(p)[:-6]
            if gid in laufende():
                raise Fehler("Gespräch %s läuft gerade" % gid[:8])
            os.remove(p)
            ordner = os.path.join(os.path.dirname(p), gid)
            if os.path.isdir(ordner):
                shutil.rmtree(ordner)
            out.append(gid)
            break
        else:
            raise Fehler("kein Gespräch zu „%s“" % teil)
    return {"aktion": "gelöscht", "gespraeche": out}


def b_leer(a):
    """Kandidaten zum Aufräumen: ruhen, höchstens eine echte Eingabe und kaum Antworten (Fehlstarts, Startbefehle)."""
    return [g for g in alle() if g["zustand"] == "ruht" and g["eingaben"] <= a.hoechstens and g["nachrichten"] <= 6]


# ---------- Ausgabe ----------

def zeile_g(g):
    ort = ""
    if g.get("fenster"):
        ort = " [%s:%s]" % (g["fenster"]["sitzung"], g["fenster"]["index"])
    return "%s  %-9s %-28s %-34s %s %5s%s\n          %s" % (
        g["id"][:8], g.get("zustand", ""), kurz(anzeigename(g), 28), kurz(g["ordner"], 34), zeit(g["ende"]),
        "%dk" % (g.get("kontext", 0) // 1000), ort,
        kurz(g["titel"] or g["erste"], 100))


def ausgabe(befehl, erg):
    if befehl in ("liste", "archiv", "leer", "suche"):
        if not erg:
            print("(nichts)")
        for g in erg:
            print(zeile_g(g))
            for b in g.get("beispiele", []):
                print("          · %s: %s" % (b["wer"], b["stelle"]))
    elif befehl == "projekte":
        for p in erg:
            print("%-22s %3d Gespräche  %s läuft  zuletzt %s  %s" % (kurz(p["name"], 22), p["gespraeche"], p["laufen"],
                                                                   zeit(p["ende"]), p["ordner"]))
    elif befehl == "fenster":
        for f in erg:
            print("%s%s:%d  %-28s %-9s %s%s" % ("*" if f["aktiv"] else " ", f["sitzung"], f["index"], kurz(f["name"], 28),
                                                f["zustand"], f["pfad"],
                                                ("  (%s)" % f["gespraech"][:8]) if f["gespraech"] else ""))
    elif befehl == "vorschau":
        print(zeile_g(erg))
        for v in erg["verlauf"]:
            print("\n[%s %s] %s" % (v["wer"], zeit(v["zeit"]), v["text"]))
    else:
        print(json.dumps(erg, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(prog="sitzung")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="befehl", required=True)

    def neu(name, fn, hilfe):
        p = sub.add_parser(name, help=hilfe)
        p.set_defaults(fn=fn)
        p.add_argument("--json", action="store_true", default=argparse.SUPPRESS)
        return p

    neu("projekte", b_projekte, "Ordner mit Gesprächen, zuletzt aktiv zuerst")
    p = neu("liste", b_liste, "Gespräche, neueste zuerst"); p.add_argument("--n", type=int, default=15)
    p.add_argument("--ordner", help="nur Gespräche dieses Ordners (Pfad oder Ordnername)")
    p.add_argument("--alle", action="store_true")
    neu("fenster", b_fenster, "tmux-Fenster mit Gespräch und Zustand")
    p = neu("oeffnen", b_oeffnen, "Gespräch im eigenen Fenster fortsetzen oder hinwechseln")
    p.add_argument("gespraech"); p.add_argument("--name"); p.add_argument("--sitzung")
    p.add_argument("--abzweigen", action="store_true"); p.add_argument("--ohne-fernsteuerung", action="store_true")
    p = neu("neu", b_neu, "neues Fenster mit neuem Gespräch in einem Ordner")
    p.add_argument("ordner"); p.add_argument("--name"); p.add_argument("--sitzung")
    p.add_argument("--ohne-fernsteuerung", action="store_true")
    for name, fn in (("wechseln", b_wechseln),):
        p = neu(name, fn, "zu einem Fenster wechseln"); p.add_argument("fenster"); p.add_argument("--sitzung")
    p = neu("fenster-umbenennen", b_fenster_umbenennen, "Fenster umbenennen")
    p.add_argument("fenster"); p.add_argument("name"); p.add_argument("--sitzung")
    p = neu("verschieben", b_verschieben, "Fenster an eine andere Stelle der Leiste")
    p.add_argument("fenster"); p.add_argument("stelle", type=int); p.add_argument("--sitzung")
    p = neu("holen", b_holen, "Fenster anderer tmux-Sitzungen in die Hauptsitzung holen")
    p.add_argument("fenster", nargs="?"); p.add_argument("--sitzung")
    p = neu("schliessen", b_schliessen, "Fenster schließen")
    p.add_argument("fenster"); p.add_argument("--sitzung"); p.add_argument("--erzwingen", action="store_true")
    p = neu("neustart", b_neustart, "Claude in einem Fenster neu starten, Gespräch bleibt")
    p.add_argument("fenster"); p.add_argument("--sitzung"); p.add_argument("--erzwingen", action="store_true")
    p.add_argument("--ohne-fernsteuerung", action="store_true")
    p = neu("umbenennen", b_umbenennen, "ruhendes Gespräch umbenennen")
    p.add_argument("gespraech"); p.add_argument("name")
    p = neu("suche", b_suche, "Volltext über alle Gespräche"); p.add_argument("text")
    p.add_argument("--n", type=int, default=10)
    p = neu("vorschau", b_vorschau, "letzte Nachrichten eines Gesprächs"); p.add_argument("gespraech")
    p.add_argument("--n", type=int, default=6)
    neu("merken", b_merken, "offene Fenster mit Gesprächen merken")
    p = neu("wiederherstellen", b_wiederherstellen, "ohne Angabe: Kandidaten zeigen; mit IDs oder --alle: öffnen")
    p.add_argument("ids", nargs="*"); p.add_argument("--alle", action="store_true"); p.add_argument("--sitzung")
    p = neu("archivieren", b_archivieren, "Gespräche ins Archiv"); p.add_argument("gespraeche", nargs="+")
    p = neu("zurueckholen", b_zurueckholen, "Gespräche aus dem Archiv"); p.add_argument("gespraeche", nargs="+")
    neu("archiv", b_archiv, "archivierte Gespräche")
    p = neu("loeschen", b_loeschen, "Gespräche endgültig löschen"); p.add_argument("gespraeche", nargs="+")
    p.add_argument("--ja", action="store_true")
    p = neu("leer", b_leer, "ruhende Gespräche mit kaum Eingaben")
    p.add_argument("--hoechstens", type=int, default=1)

    a = ap.parse_args()
    try:
        erg = a.fn(a)
    except Fehler as e:
        if a.json:
            print(json.dumps({"fehler": str(e)}, ensure_ascii=False))
        else:
            print("Fehler: %s" % e, file=sys.stderr)
        sys.exit(1)
    if a.json:
        print(json.dumps(erg, ensure_ascii=False, indent=1, default=str))
    else:
        ausgabe(a.befehl, erg)


if __name__ == "__main__":
    main()
