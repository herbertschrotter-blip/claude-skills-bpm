#!/usr/bin/env python3
"""Dashboard des Skill-Logs als eigenständige HTML-Seite (nur Standardbibliothek, keine externen Skripte).

Nutzt dieselbe Auswertung wie skill_log_report.py: Zündungen je Skill, Projekte, Prompts und Zündungen je Tag,
Blockaden des Skill-Wächters je Regel. Prompt-Texte stehen nicht in der Seite – nur Zahlen. Aufruf auch über den
Befehl /statistik des Plugins work.

  python3 tools/skill-log/dashboard.py [log-ordner …] [--since JJJJ-MM-TT] [--projekt NAME] [--out datei.html]
"""

import argparse
import collections
import datetime
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skill_log_report as r  # noqa: E402

# Testprojekte der Plugin-Umstellung (07./08.10.2026) – zählen nicht
TEST_PROJECTS = {"plugtest", "mptest-proj", "guard-test", "proj", "home", "t-deny", "t-base", "t-over", "t-plug"}
# Umbenannte Projekte zusammenführen (alter Name → neuer)
RENAMED = {"claude-skills-bpm": "claude-workbench"}


def collect(rounds, entries=()):
    prompts = [x for x in rounds if x["art"] == "prompt"]
    fired = collections.Counter()
    for x in prompts:
        for s in x["skills"]:
            fired[r.short(s["skill"])] += 1
    days = collections.OrderedDict()
    for x in prompts:
        day = x["ts"][:10]
        d = days.setdefault(day, {"prompts": 0, "zuendungen": 0})
        d["prompts"] += 1
        d["zuendungen"] += len(x["skills"])
    guard = collections.Counter(g["regel"] for x in rounds for g in x.get("guard", []) if g["entscheidung"] == "geblockt")
    hosts = sorted({x.get("host") or "?" for x in rounds})
    projects = collections.defaultdict(lambda: {"prompts": 0, "zuendungen": 0, "blockaden": 0, "skills": collections.Counter()})
    for x in rounds:
        p = projects[x.get("project") or "?"]
        p["blockaden"] += sum(1 for g in x.get("guard", []) if g["entscheidung"] == "geblockt")
        if x["art"] == "prompt":
            p["prompts"] += 1
            p["zuendungen"] += len(x["skills"])
            p["skills"].update(r.short(s["skill"]) for s in x["skills"])
    projects = sorted(projects.items(), key=lambda kv: -kv[1]["prompts"])
    zeit_projekt = r.arbeitszeit(entries)
    zeit_tag = r.arbeitszeit(entries, key=lambda e: e["ts"][:10])
    zeit_rechner = r.arbeitszeit(entries, key=lambda e: e.get("host") or "?")
    gesamt = r.arbeitszeit(entries, key=lambda e: "alle").get("alle", {"aktiv": 0, "claude": 0})
    for day, d in days.items():
        d["aktiv"] = zeit_tag.get(day, {}).get("aktiv", 0)
    # Feste Farbe je Projekt: die 4 mit der meisten aktiven Zeit, Rest „Andere“ (Farbe folgt dem Projekt, nicht dem Rang)
    top = [name for name, _ in sorted(zeit_projekt.items(), key=lambda kv: -kv[1]["aktiv"])][:4]
    bucket = lambda p: p if p in top else "Andere"  # noqa: E731
    reihen = top + ["Andere"]
    zeit_tag_projekt = r.arbeitszeit(entries, key=lambda e: (e["ts"][:10], bucket(e.get("project") or "?")))
    prompts_tag_projekt, skill_projekt = collections.Counter(), collections.defaultdict(collections.Counter)
    for x in prompts:
        prompts_tag_projekt[(x["ts"][:10], bucket(x.get("project") or "?"))] += 1
        for sk in x["skills"]:
            skill_projekt[r.short(sk["skill"])][bucket(x.get("project") or "?")] += 1
    return {
        "runden": len(rounds), "prompts": len(prompts),
        "mit_skill": sum(1 for x in prompts if x["skills"]),
        "ohne_jeden": sum(1 for x in prompts if not x["skills"] and not x["aktiv"]),
        "fehler": sum(1 for x in prompts for s in x["skills"] if not s["ok"]),
        "fired": fired.most_common(), "days": list(days.items()), "projects": projects,
        "zeit_projekt": sorted(zeit_projekt.items(), key=lambda kv: -kv[1]["aktiv"]),
        "zeit_rechner": sorted(zeit_rechner.items(), key=lambda kv: -kv[1]["aktiv"]), "gesamt": gesamt,
        "reihen": reihen,
        "zeit_tag_projekt": [(day, [(p, zeit_tag_projekt.get((day, p), {}).get("aktiv", 0) / 3600) for p in reihen])
                             for day in days],
        "prompts_tag_projekt": [(day, [(p, prompts_tag_projekt[(day, p)]) for p in reihen]) for day in days],
        "skill_projekt": [(name, [(p, skill_projekt[name][p]) for p in reihen]) for name, _ in fired.most_common()], "guard": guard.most_common(), "hosts": hosts,
        "von": rounds[0]["ts"][:10] if rounds else "-", "bis": rounds[-1]["ts"][:16].replace("T", " ") if rounds else "-",
    }


def hbars(rows, unit):
    """Waagrechte Balken (eine Reihe, eine Farbe): rows = [(label, wert)]."""
    if not rows:
        return '<p class="leer">Keine Daten im Zeitraum.</p>'
    top = max(v for _, v in rows) or 1
    bar_h, gap, label_w, w = 22, 8, 150, 560
    h = len(rows) * (bar_h + gap)
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" class="chart">']
    for i, (label, value) in enumerate(rows):
        y = i * (bar_h + gap)
        bw = max(2, (w - label_w - 50) * value / top)
        tip = html.escape(f"{label}: {value} {unit}")
        out.append(f'<g class="mark" data-tip="{tip}"><rect class="hit" x="0" y="{y}" width="{w}" height="{bar_h + gap}"/>'
                   f'<text class="lbl" x="{label_w - 8}" y="{y + bar_h / 2 + 4}" text-anchor="end">{html.escape(label)}</text>'
                   f'<path class="bar" d="M{label_w},{y} h{bw - 4} a4,4 0 0 1 4,4 v{bar_h - 8} a4,4 0 0 1 -4,4 h-{bw - 4} z"/>'
                   f'<text class="val" x="{label_w + bw + 6}" y="{y + bar_h / 2 + 4}">{value}</text></g>')
    out.append("</svg>")
    return "".join(out)


def vbars(days, key, unit):
    """Senkrechte Balken je Tag (eine Reihe)."""
    if not days:
        return '<p class="leer">Keine Daten im Zeitraum.</p>'
    top = max(d[key] for _, d in days) or 1
    w, h, pad_l, pad_b = 560, 180, 34, 24
    step = (w - pad_l) / len(days)
    bw = max(4, min(28, step - 2))
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" class="chart">']
    for frac in (0.5, 1.0):
        y = (h - pad_b) * (1 - frac)
        out.append(f'<line class="grid" x1="{pad_l}" x2="{w}" y1="{y}" y2="{y}"/>'
                   f'<text class="axis" x="{pad_l - 6}" y="{y + 4}" text-anchor="end">{round(top * frac)}</text>')
    out.append(f'<line class="base" x1="{pad_l}" x2="{w}" y1="{h - pad_b}" y2="{h - pad_b}"/>')
    for i, (day, d) in enumerate(days):
        v = d[key]
        bh = (h - pad_b) * v / top
        x = pad_l + i * step + (step - bw) / 2
        tip = html.escape(f"{day[8:10]}.{day[5:7]}.: {v} {unit}")
        out.append(f'<g class="mark" data-tip="{tip}"><rect class="hit" x="{pad_l + i * step}" y="0" width="{step}" height="{h - pad_b}"/>')
        if bh > 0:
            r4 = min(4, bh / 2, bw / 2)
            out.append(f'<path class="bar" d="M{x},{h - pad_b} v-{bh - r4} a{r4},{r4} 0 0 1 {r4},-{r4} h{bw - 2 * r4} '
                       f'a{r4},{r4} 0 0 1 {r4},{r4} v{bh - r4} z"/>')
        out.append("</g>")
        if len(days) <= 14 or i % 2 == 0:
            out.append(f'<text class="axis" x="{x + bw / 2}" y="{h - 6}" text-anchor="middle">{day[8:10]}.{day[5:7]}.</text>')
    out.append("</svg>")
    return "".join(out)


def legend(series):
    return '<div class="legende">' + "".join(
        f'<span class="lg" style="background:var(--{css})"></span>{html.escape(name)}&nbsp;&nbsp;' for name, css in series) + "</div>"


def fmt(value, unit):
    text = f"{value:.1f}" if isinstance(value, float) else str(value)
    return f"{text} {unit}" if unit else text


def hstack(rows, series, unit):
    """Waagrechte gestapelte Balken: rows = [(label, [(reihe, wert), …])], series = [(reihe, css-variable)]."""
    rows = [(label, parts) for label, parts in rows if sum(v for _, v in parts) > 0]
    if not rows:
        return '<p class="leer">Keine Daten im Zeitraum.</p>'
    css = dict(series)
    top = max(sum(v for _, v in parts) for _, parts in rows)
    bar_h, gap, label_w, w = 22, 8, 150, 560
    out = [f'<svg viewBox="0 0 {w} {len(rows) * (bar_h + gap)}" role="img" class="chart">']
    for i, (label, parts) in enumerate(rows):
        y, x = i * (bar_h + gap), label_w
        total = sum(v for _, v in parts)
        tip = html.escape(f"{label}: " + ", ".join(fmt(v, unit) + " " + n for n, v in parts if v) + f" (gesamt {fmt(total, unit)})")
        out.append(f'<g class="mark" data-tip="{tip}"><rect class="hit" x="0" y="{y}" width="{w}" height="{bar_h + gap}"/>'
                   f'<text class="lbl" x="{label_w - 8}" y="{y + bar_h / 2 + 4}" text-anchor="end">{html.escape(label)}</text>')
        for name, v in parts:
            bw = (w - label_w - 60) * v / top
            if bw <= 0:
                continue
            out.append(f'<rect class="seg" x="{x}" y="{y}" width="{bw}" height="{bar_h}" rx="3" style="fill:var(--{css[name]})"/>')
            x += bw
        out.append(f'<text class="val" x="{x + 6}" y="{y + bar_h / 2 + 4}">{fmt(total, "").strip()}</text></g>')
    out.append("</svg>")
    return "".join(out) + legend(series)


def vstack(cols, series, unit):
    """Senkrechte gestapelte Balken je Tag: cols = [(tag, [(reihe, wert), …])]."""
    if not cols:
        return '<p class="leer">Keine Daten im Zeitraum.</p>'
    css = dict(series)
    top = max(sum(v for _, v in parts) for _, parts in cols) or 1
    w, h, pad_l, pad_b = 560, 180, 34, 24
    step = (w - pad_l) / len(cols)
    bw = max(4, min(28, step - 2))
    out = [f'<svg viewBox="0 0 {w} {h}" role="img" class="chart">']
    for frac in (0.5, 1.0):
        y = (h - pad_b) * (1 - frac)
        label = f"{top * frac:.1f}" if isinstance(top, float) else str(round(top * frac))
        out.append(f'<line class="grid" x1="{pad_l}" x2="{w}" y1="{y}" y2="{y}"/>'
                   f'<text class="axis" x="{pad_l - 6}" y="{y + 4}" text-anchor="end">{label}</text>')
    out.append(f'<line class="base" x1="{pad_l}" x2="{w}" y1="{h - pad_b}" y2="{h - pad_b}"/>')
    for i, (day, parts) in enumerate(cols):
        x = pad_l + i * step + (step - bw) / 2
        total = sum(v for _, v in parts)
        tip = html.escape(f"{day[8:10]}.{day[5:7]}.: " + (", ".join(fmt(v, unit) + " " + n for n, v in parts if v) or "nichts"))
        out.append(f'<g class="mark" data-tip="{tip}"><rect class="hit" x="{pad_l + i * step}" y="0" width="{step}" height="{h - pad_b}"/>')
        base = h - pad_b
        for name, v in parts:
            bh = (h - pad_b) * v / top
            if bh <= 0:
                continue
            out.append(f'<rect class="seg" x="{x}" y="{base - bh}" width="{bw}" height="{bh}" rx="3" style="fill:var(--{css[name]})"/>')
            base -= bh
        out.append("</g>")
        if len(cols) <= 14 or i % 2 == 0:
            out.append(f'<text class="axis" x="{x + bw / 2}" y="{h - 6}" text-anchor="middle">{day[8:10]}.{day[5:7]}.</text>')
    out.append("</svg>")
    return "".join(out) + legend(series)


def project_section(projects):
    rows = [(name, p["prompts"]) for name, p in projects if p["prompts"]]
    tips = {name: f'{p["prompts"]} Prompts, {p["zuendungen"]} Zündungen, {p["blockaden"]} Blockaden' for name, p in projects}
    chart = hbars(rows, "Prompts")
    for name, count in rows:  # Tooltip der Balken um Zündungen und Blockaden ergänzen
        old = html.escape(f"{name}: {count} Prompts")
        chart = chart.replace(f'data-tip="{old}"', f'data-tip="{html.escape(name + ": " + tips[name])}"', 1)
    detail = [(name, p["prompts"], p["zuendungen"], p["blockaden"],
               ", ".join(f"{k} {v}" for k, v in p["skills"].most_common(3)) or "–") for name, p in projects]
    return chart + table(["Projekt", "Prompts", "Zündungen", "Blockaden", "häufigste Skills"], detail)


MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November",
          "Dezember"]
WOCHENTAGE = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


def level(value, top):
    """Stufe 0–4 für die Farbe: 0 = kein Prompt, sonst Viertel des Maximums."""
    if not value:
        return 0
    return min(4, 1 + int(4 * (value - 1) / max(1, top)))


def calendar(days):
    """Kalender je Monat: ein Kästchen je Tag (Zeilen Mo–So), Farbe nach Prompts des Tages."""
    if not days:
        return '<p class="leer">Keine Daten im Zeitraum.</p>'
    data = dict(days)
    top = max(d["prompts"] for d in data.values()) or 1
    first = datetime.date.fromisoformat(days[0][0]).replace(day=1)
    last = datetime.date.fromisoformat(days[-1][0])
    out = ['<div class="kal">']
    month = first
    cell, gap = 18, 3
    while month <= last:
        nxt = (month.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        ndays = (nxt - month).days
        offset = month.weekday()
        weeks = (offset + ndays + 6) // 7
        w, h = 22 + weeks * (cell + gap), 7 * (cell + gap)
        svg = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">']
        for i, name in enumerate(WOCHENTAGE):
            if i % 2 == 0:
                svg.append(f'<text class="axis" x="0" y="{i * (cell + gap) + 13}">{name}</text>')
        for d in range(ndays):
            day = month + datetime.timedelta(days=d)
            pos = offset + d
            x, y = 22 + (pos // 7) * (cell + gap), (pos % 7) * (cell + gap)
            v = data.get(day.isoformat(), {"prompts": 0, "zuendungen": 0, "aktiv": 0})
            tip = html.escape(f"{WOCHENTAGE[day.weekday()]} {day:%d.%m.}: {v['prompts']} Prompts, {v['zuendungen']} Zündungen, "
                              f"{r.stunden(v.get('aktiv', 0))} aktiv")
            svg.append(f'<rect class="mark tag l{level(v["prompts"], top)}" data-tip="{tip}" x="{x}" y="{y}" '
                       f'width="{cell}" height="{cell}" rx="4"/>')
        svg.append("</svg>")
        out.append(f'<div class="monat"><div class="mname">{MONATE[month.month - 1]} {month.year}</div>{"".join(svg)}</div>')
        month = nxt
    out.append("</div>")
    legend = "".join(f'<span class="lg l{i}"></span>' for i in range(5))
    out.append(f'<div class="legende">weniger {legend} mehr · dunkelste Stufe ≈ {top} Prompts am Tag</div>')
    return "".join(out)


def zeit_section(zeiten):
    rows = [(name, [("Claude rechnet", t["claude"] / 3600), ("Du", max(0, t["aktiv"] - t["claude"]) / 3600)])
            for name, t in zeiten if t["aktiv"] >= 360]
    chart = hstack(rows, [("Claude rechnet", "claude"), ("Du", "du")], "h")
    return chart + table(["", "aktiv", "davon Claude"], [(n, r.stunden(t["aktiv"]), r.stunden(t["claude"])) for n, t in zeiten])


def table(headers, rows):
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>" for row in rows)
    return f'<details><summary>Als Tabelle</summary><table><tr>{head}</tr>{body}</table></details>'


def page(s, title):
    projekt_reihen = [(n, "p%d" % (i + 1) if n != "Andere" else "pa") for i, n in enumerate(s["reihen"])]
    tiles = [("Arbeitszeit aktiv", r.stunden(s["gesamt"]["aktiv"])), ("davon Claude", r.stunden(s["gesamt"]["claude"])),
             ("Prompts", s["prompts"]), ("mit Skill-Zündung", s["mit_skill"]), ("ganz ohne Skill", s["ohne_jeden"]),
             ("Wächter-Blockaden", sum(v for _, v in s["guard"])), ("gescheiterte Aufrufe", s["fehler"])]
    tiles_html = "".join(f'<div class="tile"><div class="num">{v}</div><div class="cap">{html.escape(k)}</div></div>'
                         for k, v in tiles)
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root {{ --surface: #fcfcfb; --card: #ffffff; --line: #e4e3df; --ink: #0b0b0b; --ink-2: #52514e; --series: #2a78d6;
  --k0: #f0efec; --k1: #86b6ef; --k2: #5598e7; --k3: #2a78d6; --k4: #1c5cab;
  --p1: #2a78d6; --p2: #eb6834; --p3: #1baf7a; --p4: #eda100; --pa: #a3a29d; --claude: #1c5cab; --du: #86b6ef; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --surface: #1a1a19; --card: #232321; --line: #383835;
  --ink: #ffffff; --ink-2: #c3c2b7; --series: #3987e5; --k0: #383835; --k1: #184f95; --k2: #256abf; --k3: #3987e5;
  --k4: #86b6ef; --p1: #3987e5; --p2: #d95926; --p3: #199e70; --p4: #c98500; --pa: #6f6e69; --claude: #86b6ef; --du: #256abf; }} }}
:root[data-theme="dark"] {{ --surface: #1a1a19; --card: #232321; --line: #383835; --ink: #ffffff; --ink-2: #c3c2b7; --series: #3987e5;
  --k0: #383835; --k1: #184f95; --k2: #256abf; --k3: #3987e5; --k4: #86b6ef;
  --p1: #3987e5; --p2: #d95926; --p3: #199e70; --p4: #c98500; --pa: #6f6e69; --claude: #86b6ef; --du: #256abf; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--surface); color: var(--ink); font: 15px/1.45 system-ui, -apple-system, "Segoe UI", sans-serif; }}
main {{ max-width: 960px; margin: 0 auto; padding: 24px 16px 48px; }}
h1 {{ font-size: 22px; margin: 0 0 4px; }} h2 {{ font-size: 16px; margin: 0 0 12px; }}
.sub {{ color: var(--ink-2); margin: 0 0 20px; font-size: 13px; }}
.tiles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 16px; }}
.tile, .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 14px 16px; }}
.num {{ font-size: 28px; font-weight: 650; font-variant-numeric: tabular-nums; }} .cap {{ color: var(--ink-2); font-size: 13px; }}
.grid2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 12px; }}
.card {{ margin-bottom: 12px; }}
.chart {{ width: 100%; height: auto; display: block; overflow: visible; }}
.bar {{ fill: var(--series); }} .seg {{ stroke: var(--card); stroke-width: 2; }} .mark:hover .seg {{ opacity: .85; }} .hit {{ fill: transparent; }} .mark:hover .bar {{ opacity: .8; }}
.lbl, .val, .axis {{ fill: var(--ink-2); font-size: 12px; font-variant-numeric: tabular-nums; }} .val {{ fill: var(--ink); }}
.grid {{ stroke: var(--line); stroke-width: 1; }} .base {{ stroke: var(--ink-2); stroke-width: 1; }}
.leer {{ color: var(--ink-2); }}
.kal {{ display: flex; flex-wrap: wrap; gap: 24px; }} .mname {{ font-size: 13px; color: var(--ink-2); margin-bottom: 6px; }}
.tag {{ stroke: var(--card); stroke-width: 2; }} .tag:hover {{ stroke: var(--ink); }}
.l0 {{ fill: var(--k0); background: var(--k0); }} .l1 {{ fill: var(--k1); background: var(--k1); }}
.l2 {{ fill: var(--k2); background: var(--k2); }} .l3 {{ fill: var(--k3); background: var(--k3); }}
.l4 {{ fill: var(--k4); background: var(--k4); }}
.legende {{ margin-top: 10px; font-size: 12px; color: var(--ink-2); display: flex; align-items: center; gap: 4px; }}
.lg {{ display: inline-block; width: 14px; height: 14px; border-radius: 3px; }}
details {{ margin-top: 10px; font-size: 13px; }} summary {{ cursor: pointer; color: var(--ink-2); }}
table {{ border-collapse: collapse; margin-top: 8px; width: 100%; }} td, th {{ text-align: left; padding: 4px 8px; border-bottom: 1px solid var(--line); }}
#tip {{ position: fixed; pointer-events: none; background: var(--ink); color: var(--surface); padding: 4px 8px; border-radius: 6px;
  font-size: 12px; display: none; z-index: 10; }}
</style></head>
<body><main>
<h1>{html.escape(title)}</h1>
<p class="sub">Skill-Log {html.escape(s["von"])} bis {html.escape(s["bis"])} UTC · Rechner: {html.escape(", ".join(s["hosts"]))} · {s["runden"]} Runden, ohne Testprojekte</p>
<div class="tiles">{tiles_html}</div>
<div class="card"><h2>Aktivität je Tag</h2>{calendar(s["days"])}</div>
<div class="card"><h2>Arbeitszeit je Projekt</h2>{zeit_section(s["zeit_projekt"])}
<p class="sub" style="margin:8px 0 0">aktiv = Zeit zwischen Ereignissen einer Sitzung, Pausen ab 15 min zählen nicht; Claude = vom Prompt bis zur fertigen Antwort (höchstens 2 h je Antwort); parallele Fenster zählen einmal.</p></div>
<div class="card"><h2>Projekte (Prompts)</h2>{project_section(s["projects"])}</div>
<div class="card"><h2>Arbeitszeit je Tag nach Projekt (h aktiv)</h2>{vstack(s["zeit_tag_projekt"], projekt_reihen, "h")}{table(["Tag"] + s["reihen"], [(d, *[f"{v:.1f}" for _, v in parts]) for d, parts in s["zeit_tag_projekt"]])}</div>
<div class="card"><h2>Zündungen je Skill nach Projekt</h2>{hstack(s["skill_projekt"], projekt_reihen, "")}{table(["Skill"] + s["reihen"], [(n, *[v for _, v in parts]) for n, parts in s["skill_projekt"]])}</div>
<div class="grid2">
<div class="card"><h2>Prompts je Tag nach Projekt</h2>{vstack(s["prompts_tag_projekt"], projekt_reihen, "Prompts")}{table(["Tag", "Prompts", "Zündungen"], [(d, v["prompts"], v["zuendungen"]) for d, v in s["days"]])}</div>
<div class="card"><h2>Skill-Zündungen je Tag</h2>{vbars(s["days"], "zuendungen", "Zündungen")}</div>
</div>
<div class="card"><h2>Skill-Wächter: Blockaden je Regel</h2>{hbars(s["guard"], "Blockaden")}{table(["Regel", "Blockaden"], s["guard"])}</div>
<div class="card"><h2>Rechner</h2>{table(["Rechner", "aktiv", "davon Claude"], [(n, r.stunden(t["aktiv"]), r.stunden(t["claude"])) for n, t in s["zeit_rechner"]]).replace("<details>", "<details open>")}</div>
</main><div id="tip"></div>
<script>
const tip = document.getElementById("tip");
document.querySelectorAll(".mark").forEach(m => {{
  m.addEventListener("mousemove", e => {{ tip.textContent = m.dataset.tip; tip.style.display = "block";
    tip.style.left = (e.clientX + 12) + "px"; tip.style.top = (e.clientY + 12) + "px"; }});
  m.addEventListener("mouseleave", () => tip.style.display = "none");
  m.addEventListener("click", e => {{ tip.textContent = m.dataset.tip; tip.style.display = "block";
    tip.style.left = (e.clientX + 12) + "px"; tip.style.top = (e.clientY + 12) + "px"; }});
}});
</script></body></html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("dirs", nargs="*", default=r.DEFAULT_DIRS)
    parser.add_argument("--since", help="ab Datum JJJJ-MM-TT (UTC)")
    parser.add_argument("--projekt", help="nur dieses Projekt")
    parser.add_argument("--out", default="skill-log-dashboard.html")
    parser.add_argument("--transcripts", default="~/.claude/projects")
    args = parser.parse_args()
    entries = r.read_entries(args.dirs)
    if args.since:
        entries = [e for e in entries if (e.get("ts") or "") >= args.since]
    rounds = r.build_rounds(entries, r.known_skill_names(entries), os.path.expanduser(args.transcripts) or None)
    rounds = [x for x in rounds if x.get("project") not in TEST_PROJECTS]
    entries = [e for e in entries if e.get("project") not in TEST_PROJECTS]
    for x in rounds + entries:
        x["project"] = RENAMED.get(x.get("project"), x.get("project"))
    if args.projekt:
        rounds = [x for x in rounds if x.get("project") == args.projekt]
        entries = [e for e in entries if e.get("project") == args.projekt]
    stand = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    title = f"Skill-Statistik{' · ' + args.projekt if args.projekt else ''} · Stand {stand}"
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(page(collect(rounds, entries), title))
    print(args.out)


if __name__ == "__main__":
    main()
