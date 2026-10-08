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


def collect(rounds):
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
    return {
        "runden": len(rounds), "prompts": len(prompts),
        "mit_skill": sum(1 for x in prompts if x["skills"]),
        "ohne_jeden": sum(1 for x in prompts if not x["skills"] and not x["aktiv"]),
        "fehler": sum(1 for x in prompts for s in x["skills"] if not s["ok"]),
        "fired": fired.most_common(), "days": list(days.items()), "projects": projects, "guard": guard.most_common(), "hosts": hosts,
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


def table(headers, rows):
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>" for row in rows)
    return f'<details><summary>Als Tabelle</summary><table><tr>{head}</tr>{body}</table></details>'


def page(s, title):
    tiles = [("Prompts", s["prompts"]), ("mit Skill-Zündung", s["mit_skill"]), ("ganz ohne Skill", s["ohne_jeden"]),
             ("Wächter-Blockaden", sum(v for _, v in s["guard"])), ("gescheiterte Aufrufe", s["fehler"])]
    tiles_html = "".join(f'<div class="tile"><div class="num">{v}</div><div class="cap">{html.escape(k)}</div></div>'
                         for k, v in tiles)
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root {{ --surface: #fcfcfb; --card: #ffffff; --line: #e4e3df; --ink: #0b0b0b; --ink-2: #52514e; --series: #2a78d6; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --surface: #1a1a19; --card: #232321; --line: #383835;
  --ink: #ffffff; --ink-2: #c3c2b7; --series: #3987e5; }} }}
:root[data-theme="dark"] {{ --surface: #1a1a19; --card: #232321; --line: #383835; --ink: #ffffff; --ink-2: #c3c2b7; --series: #3987e5; }}
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
.bar {{ fill: var(--series); }} .hit {{ fill: transparent; }} .mark:hover .bar {{ opacity: .8; }}
.lbl, .val, .axis {{ fill: var(--ink-2); font-size: 12px; font-variant-numeric: tabular-nums; }} .val {{ fill: var(--ink); }}
.grid {{ stroke: var(--line); stroke-width: 1; }} .base {{ stroke: var(--ink-2); stroke-width: 1; }}
.leer {{ color: var(--ink-2); }}
details {{ margin-top: 10px; font-size: 13px; }} summary {{ cursor: pointer; color: var(--ink-2); }}
table {{ border-collapse: collapse; margin-top: 8px; width: 100%; }} td, th {{ text-align: left; padding: 4px 8px; border-bottom: 1px solid var(--line); }}
#tip {{ position: fixed; pointer-events: none; background: var(--ink); color: var(--surface); padding: 4px 8px; border-radius: 6px;
  font-size: 12px; display: none; z-index: 10; }}
</style></head>
<body><main>
<h1>{html.escape(title)}</h1>
<p class="sub">Skill-Log {html.escape(s["von"])} bis {html.escape(s["bis"])} UTC · Rechner: {html.escape(", ".join(s["hosts"]))} · {s["runden"]} Runden, ohne Testprojekte</p>
<div class="tiles">{tiles_html}</div>
<div class="card"><h2>Projekte (Prompts)</h2>{project_section(s["projects"])}</div>
<div class="card"><h2>Zündungen je Skill</h2>{hbars(s["fired"], "Zündungen")}{table(["Skill", "Zündungen"], s["fired"])}</div>
<div class="grid2">
<div class="card"><h2>Prompts je Tag</h2>{vbars(s["days"], "prompts", "Prompts")}{table(["Tag", "Prompts", "Zündungen"], [(d, v["prompts"], v["zuendungen"]) for d, v in s["days"]])}</div>
<div class="card"><h2>Skill-Zündungen je Tag</h2>{vbars(s["days"], "zuendungen", "Zündungen")}</div>
</div>
<div class="card"><h2>Skill-Wächter: Blockaden je Regel</h2>{hbars(s["guard"], "Blockaden")}{table(["Regel", "Blockaden"], s["guard"])}</div>
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
    parser.add_argument("dirs", nargs="*", default=["~/.claude/skill-log"])
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
    for x in rounds:
        x["project"] = RENAMED.get(x.get("project"), x.get("project"))
    if args.projekt:
        rounds = [x for x in rounds if x.get("project") == args.projekt]
    stand = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    title = f"Skill-Statistik{' · ' + args.projekt if args.projekt else ''} · Stand {stand}"
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(page(collect(rounds), title))
    print(args.out)


if __name__ == "__main__":
    main()
