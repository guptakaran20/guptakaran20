#!/usr/bin/env python3
"""Render the animated SVG cards for the profile README.

    python scripts/render_cards.py            # fetch data (if a token is set) and render
    STATIC=1 python scripts/render_cards.py   # render the end state of every animation

Reads a GitHub token from GITHUB_TOKEN or GH_TOKEN to refresh
data/contributions.json and data/repos.json. Without one it renders from the
JSON already committed. Standard library only, so the Action needs no installs.
Every card is written twice, cards/<name>-light.svg and cards/<name>-dark.svg,
and the README picks one with <picture> + prefers-color-scheme.
"""
from __future__ import annotations

import base64
import datetime as dt
import json
import math
import os
import urllib.request
from collections import OrderedDict
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CARDS = ROOT / "cards"
FONTS = ROOT / "fonts"
USER = "guptakaran20"
STATIC = os.environ.get("STATIC") == "1"

# ---------------------------------------------------------------- content

TILES = [
    dict(key="build", label="BUILD", accent="blue", number="repos", caption="public repositories",
         sub="EventFlow · CodeArena · ImportlyAI"),
    dict(key="ship", label="SHIP", accent="red", number=219, caption="PRs merged at XCEED",
         sub="AI attendance + XCEED Learning App"),
    dict(key="solve", label="SOLVE", accent="yellow", number=639, caption="LeetCode problems",
         sub="1870 rating · Knight · top 5.7%"),
]

REPOS = [
    dict(key="eventflow", repo="EventFlow", name="EventFlow", kind="Workflow orchestration engine",
         lines=["DAG workflows on Redis Streams consumer groups:", "at-least-once delivery, XCLAIM recovery, a DLQ."],
         tags=["FastAPI", "Redis Streams", "gRPC", "PostgreSQL"], meta="53 commits · Jul 2026"),
    dict(key="codearena", repo="CodeBattle", name="CodeArena", kind="Real-time coding battles",
         lines=["Battle rooms, tournaments and leaderboards with", "Redis matchmaking and Piston code runs on EC2."],
         tags=["Next.js", "Socket.IO", "Redis", "AWS EC2"], meta="50 commits · Jun 2026"),
    dict(key="importlyai", repo="ImportlyAI", name="ImportlyAI", kind="AI-powered CSV import",
         lines=["A batched multi-stage Gemini pipeline that maps", "any CSV onto a CRM schema, with 180+ tests."],
         tags=["Next.js", "Gemini API", "PapaParse", "Express"], meta="15 commits · Jul 2026"),
    dict(key="sponsorgrid", repo="Sponsorship", name="SponsorGrid", kind="Sponsorship SaaS",
         lines=["Sponsors, deals and funding workflows with", "CSRF-safe cookie auth and Google OAuth."],
         tags=["Next.js", "PostgreSQL", "Prisma", "Zod"], meta="41 commits · Mar 2026"),
]

TERMINAL = [
    ("cmd", "whoami"),
    ("out", "karan · B.Tech ICE, NIT Jalandhar '29"),
    ("cmd", "leetcode --rating"),
    ("out", "1870 · Knight · top 5.7% · 639 solved"),
]

LANG_COLORS = {"TypeScript": "#3178c6", "Python": "#3572A5", "JavaScript": "#f1e05a"}

# ---------------------------------------------------------------- themes

THEMES = {
    "light": dict(
        paper="#fbf8f2", ink="#1b1a17", muted="#6f6a60", line="#e6e0d4", soft="#efe9dd",
        blue="#2f55f4", red="#e5484d", yellow="#f2b705", on_blue="#ffffff", on_red="#ffffff",
        on_yellow="#1b1a17", term="#1b1a17", term_ink="#ece9e2", term_muted="#8d877c",
        bar="#d9d1c2", grid=["#ece6da", "#d3dcff", "#99adff", "#5c7bff", "#2f55f4"],
        shine="#ffffff",
    ),
    "dark": dict(
        paper="#14171d", ink="#ece9e2", muted="#8b9099", line="#272c35", soft="#1c2028",
        blue="#6d8bff", red="#ff6b6e", yellow="#ffc53d", on_blue="#0d1117", on_red="#0d1117",
        on_yellow="#0d1117", term="#0b0d11", term_ink="#ece9e2", term_muted="#6c727c",
        bar="#2e3440", grid=["#1d222b", "#1f2c66", "#2c44b3", "#4a68f0", "#9fb2ff"],
        shine="#ffffff", invert_art=True,
    ),
}

# ---------------------------------------------------------------- data


def _token() -> str | None:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def _request(url: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None)
    req.add_header("Authorization", f"bearer {_token()}")
    req.add_header("User-Agent", "profile-cards")
    if body:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def refresh_data() -> None:
    if not _token():
        print("no token: rendering from committed data/")
        return
    DATA.mkdir(exist_ok=True)
    q = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
        totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
    cal = _request("https://api.github.com/graphql", {"query": q, "variables": {"u": USER}})
    cal = cal["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    (DATA / "contributions.json").write_text(json.dumps(
        {"total": cal["totalContributions"],
         "days": [[d["date"], d["contributionCount"]] for d in days]}, indent=0) + "\n")

    user = _request(f"https://api.github.com/users/{USER}")
    repos = {}
    for r in REPOS:
        info = _request(f"https://api.github.com/repos/{USER}/{r['repo']}")
        repos[r["repo"]] = {"stars": info["stargazers_count"], "forks": info["forks_count"],
                            "language": info["language"]}
    (DATA / "repos.json").write_text(json.dumps(
        {"public_repos": user["public_repos"], "repos": repos}, indent=2) + "\n")


def load_data() -> tuple[dict, dict]:
    return (json.loads((DATA / "contributions.json").read_text()),
            json.loads((DATA / "repos.json").read_text()))


def stats(contrib: dict) -> dict:
    days = [(dt.date.fromisoformat(d), n) for d, n in contrib["days"]]
    longest = run = 0
    for _, n in days:
        run = run + 1 if n else 0
        longest = max(longest, run)
    current = 0
    for i, (_, n) in enumerate(reversed(days)):
        if n:
            current += 1
        elif i:  # today may still be empty
            break
    busiest = max(days, key=lambda x: x[1])
    months: "OrderedDict[str, int]" = OrderedDict()
    for d, n in days:
        months[d.strftime("%Y-%m")] = months.get(d.strftime("%Y-%m"), 0) + n
    last12 = list(months.items())[-12:]
    return dict(total=contrib["total"], longest=longest, current=current, busiest=busiest,
                months=last12, active=sum(1 for _, n in last12 if n), days=days)

# ---------------------------------------------------------------- svg helpers


def font_face(*names: str) -> str:
    families = {"serif": ("Instrument Serif", "normal"), "serif-italic": ("Instrument Serif", "italic"),
                "geist": ("Geist", "normal"), "geistmono": ("Geist Mono", "normal")}
    out = []
    for n in names:
        fam, style = families[n]
        b64 = base64.b64encode((FONTS / f"{n}.woff2").read_bytes()).decode()
        weight = "100 900" if n == "geist" else "400"
        out.append(f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
                   f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "".join(out)


BASE_CSS = """
.serif{font-family:'Instrument Serif',Georgia,serif}
.it{font-style:italic}
.sans{font-family:'Geist',system-ui,sans-serif}
.mono{font-family:'Geist Mono',ui-monospace,monospace}
"""


def svg(w: int, h: int, title: str, fonts: tuple, css: str, anim_css: str, body: str) -> str:
    style = font_face(*fonts) + BASE_CSS + css
    if not STATIC:
        style += anim_css + "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>'
            f"<style>{style}</style>{body}</svg>\n")


def card_bg(w: int, h: int, t: dict, fill: str | None = None, stroke: bool = True) -> str:
    s = f' stroke="{t["line"]}"' if stroke else ""
    return f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" fill="{fill or t["paper"]}"{s}/>'


def smil(tag: str) -> str:
    return "" if STATIC else tag


def shine_gradient(gid: str, t: dict, width: float, dur: float, begin: float, slant: float = 0) -> str:
    """A soft white band that sweeps across, looping every `dur` seconds."""
    anim = smil(f'<animateTransform attributeName="gradientTransform" type="translate" '
                f'values="{-width*0.6} 0;{width*1.6} 0;{width*1.6} 0" keyTimes="0;0.35;1" '
                f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>')
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="0" '
            f'x2="{width*0.25}" y2="{slant}">'
            f'<stop offset="0" stop-color="{t["shine"]}" stop-opacity="0"/>'
            f'<stop offset="0.5" stop-color="{t["shine"]}" stop-opacity="{0 if STATIC else 0.55}"/>'
            f'<stop offset="1" stop-color="{t["shine"]}" stop-opacity="0"/>{anim}</linearGradient>')


def count_up(value: int, x: float, y: float, cls: str, fill: str, begin: float, frames: int = 18) -> str:
    """CSS can't change text, so stack `frames` texts and flip visibility with SMIL <set>."""
    if STATIC:
        return f'<text x="{x}" y="{y}" class="{cls}" fill="{fill}">{value:,}</text>'
    out, step = [], 0.05
    for i in range(1, frames + 1):
        v = round(value * (1 - (1 - i / frames) ** 3))
        start = begin + (i - 1) * step
        end = ' fill="freeze"' if i == frames else f' end="{start + step:.2f}s"'
        out.append(f'<text x="{x}" y="{y}" class="{cls}" fill="{fill}" visibility="hidden">{v:,}'
                   f'<set attributeName="visibility" to="visible" begin="{start:.2f}s"{end}/></text>')
    return "".join(out)

# ---------------------------------------------------------------- cards


PORTRAIT = ROOT / "assets" / "portrait.txt"


def hero(t: dict) -> str:
    W, H = 880, 470
    rows = PORTRAIT.read_text().rstrip("\n").split("\n")
    if t.get("invert_art"):
        # light glyphs on a dark card: dense characters must mean light tones
        ramp = " .:-=+*#%@"
        flip = {c: ramp[10 - i] for i, c in enumerate(ramp) if i}
        rows = [r.translate(str.maketrans(flip)) for r in rows]
    cols = max(len(r) for r in rows)
    px, py, pw, ph = 462, 38, 390, 396  # portrait box
    fs = min(pw / (cols * 0.6), ph / len(rows))
    ox = px + (pw - cols * 0.6 * fs) / 2
    oy = py + (ph - len(rows) * fs) / 2
    art = []
    for i, r in enumerate(rows):
        if not r.strip():
            continue
        lead = len(r) - len(r.lstrip())
        body = r.lstrip()
        art.append(f'<text x="{ox + lead*0.6*fs:.2f}" y="{oy + (i+1)*fs:.2f}" textLength="{len(body)*0.6*fs:.2f}" '
                   f'lengthAdjust="spacing" xml:space="preserve" style="animation-delay:{0.35 + i*0.018:.3f}s">'
                   f'{escape(body)}</text>')
    tx, ty, tw, th = 40, 330, 392, 112
    term, y = [], ty + 48
    for i, (kind, text) in enumerate(TERMINAL):
        if kind == "cmd":
            content = f'<tspan fill="{t["blue"]}">$</tspan> <tspan fill="{t["term_ink"]}">{escape(text)}</tspan>'
        else:
            content = f'<tspan fill="{t["term_muted"]}">{escape(text)}</tspan>'
        term.append(f'<text x="{tx+20}" y="{y}" class="mono tl" xml:space="preserve" font-size="12" '
                    f'style="animation-delay:{1.0 + i*0.3:.2f}s">{content}</text>')
        y += 18
    body = f"""
<defs>{shine_gradient("sh", t, 260, 6, 2.4)}</defs>
{card_bg(W, H, t)}
<g class="up" style="animation-delay:.05s">
  <circle cx="48" cy="56" r="4.5" fill="{t['red']}"/>
  <circle cx="48" cy="56" r="4.5" fill="none" stroke="{t['red']}" class="pulse"/>
  <text x="62" y="60.5" class="mono" font-size="12.5" fill="{t['muted']}">Full Stack Developer &amp; App Lead @ XCEED</text>
</g>
<text x="38" y="158" class="serif up" font-size="104" fill="{t['ink']}" style="animation-delay:.2s">Karan</text>
<g class="up" style="animation-delay:.38s">
  <text x="38" y="246" class="serif it" font-size="104" fill="{t['blue']}">Gupta.</text>
  <text x="38" y="246" class="serif it" font-size="104" fill="url(#sh)">Gupta.</text>
</g>
<text class="sans up" font-size="15" fill="{t['muted']}" style="animation-delay:.56s">
  <tspan x="41" y="286">Full Stack Developer and software engineer for backend</tspan>
  <tspan x="41" y="307">&amp; ML systems: distributed, AI and real-time platforms.</tspan>
</text>
<g class="up" style="animation-delay:.7s">
  <rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{t['term']}"/>
  <circle cx="{tx+18}" cy="{ty+18}" r="4" fill="{t['red']}"/>
  <circle cx="{tx+32}" cy="{ty+18}" r="4" fill="{t['yellow']}"/>
  <circle cx="{tx+46}" cy="{ty+18}" r="4" fill="{t['blue']}"/>
  <text x="{tx+tw-16}" y="{ty+22}" text-anchor="end" class="mono" font-size="10.5" fill="{t['term_muted']}">~/karan</text>
</g>
{''.join(term)}
<rect x="{tx+tw-28}" y="{ty+th-26}" width="7" height="13" fill="{t['blue']}" class="cur"/>
<g class="mono art" font-size="{fs:.3f}" fill="{t['ink']}">{''.join(art)}</g>
"""
    anim = """
.up{animation:up .8s cubic-bezier(.2,.8,.2,1) both}
@keyframes up{from{opacity:0;transform:translateY(22px)}to{opacity:1;transform:none}}
.tl{animation:fade .35s ease-out both}
@keyframes fade{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}
.art text{animation:print .5s ease-out both}
@keyframes print{from{opacity:0;fill:BLUE}40%{opacity:1;fill:BLUE}to{opacity:1}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}
@keyframes pulse{from{transform:scale(1);opacity:.9}to{transform:scale(3.2);opacity:0}}
.cur{animation:blink 1s steps(1) infinite 3.4s}
@keyframes blink{50%{opacity:0}}
""".replace("BLUE", t["blue"])
    return svg(W, H, "Karan Gupta — Full Stack Developer & App Lead @ XCEED, software engineer for backend and ML systems",
               ("serif", "serif-italic", "geist", "geistmono"), "", anim, body)


def graph(t: dict, s: dict) -> str:
    W, H = 880, 210
    days = s["days"]
    # align to Sunday-start weeks like GitHub's calendar
    first = days[0][0]
    offset = (first.weekday() + 1) % 7
    peak = max(n for _, n in days) or 1
    cell, gap, x0, y0 = 12, 3, 44, 82
    rects, month_labels, last_month = [], [], None
    for i, (d, n) in enumerate(days):
        idx = i + offset
        wk, dow = divmod(idx, 7)
        x, y = x0 + wk * (cell + gap), y0 + dow * (cell + gap)
        lvl = 0 if n == 0 else min(4, 1 + int(3.999 * math.sqrt(n / peak)))
        rects.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{t["grid"][lvl]}" '
                     f'style="animation-delay:{0.25 + wk*0.022:.3f}s"><title>{n} on {d.isoformat()}</title></rect>')
        if d.day <= 7 and dow == 0 and d.month != last_month:
            last_month = d.month
            month_labels.append(f'<text x="{x}" y="{y0-10}" class="mono" font-size="10.5" '
                                f'fill="{t["muted"]}">{d.strftime("%b")}</text>')
    legend = "".join(f'<rect x="{W-150+i*15}" y="36" width="12" height="12" rx="3" fill="{c}"/>'
                     for i, c in enumerate(t["grid"]))
    body = f"""
{card_bg(W, H, t)}
<text x="40" y="50" class="serif" font-size="28" fill="{t['ink']}">{s['total']:,} <tspan class="it" fill="{t['blue']}">contributions</tspan> in the last year</text>
<text x="{W-160}" y="46" text-anchor="end" class="mono" font-size="10.5" fill="{t['muted']}">less</text>
{legend}
<text x="{W-70}" y="46" class="mono" font-size="10.5" fill="{t['muted']}">more</text>
{''.join(month_labels)}
<g class="cells">{''.join(rects)}</g>
"""
    anim = """
.cells rect{transform-box:fill-box;transform-origin:center;animation:pop .45s cubic-bezier(.3,1.6,.5,1) both}
@keyframes pop{from{opacity:0;transform:scale(.2)}to{opacity:1;transform:none}}
"""
    return svg(W, H, f"{s['total']} GitHub contributions in the last year",
               ("serif", "serif-italic", "geistmono"), "", anim, body)


def activity(t: dict, s: dict) -> str:
    W, H = 880, 320
    months = s["months"]
    peak = max(n for _, n in months) or 1
    best = max(range(len(months)), key=lambda i: months[i][1])
    bx, by, bw, bh = 40, 276, 800, 108
    slot = bw / len(months)
    bars = []
    for i, (m, n) in enumerate(months):
        h = max(3, bh * n / peak)
        x = bx + i * slot + slot * 0.2
        color = t["blue"] if i == best else t["bar"]
        bars.append(f'<rect x="{x:.1f}" y="{by-h:.1f}" width="{slot*0.6:.1f}" height="{h:.1f}" rx="5" '
                    f'fill="{color}" class="bar" style="animation-delay:{0.5 + i*0.06:.2f}s"/>')
        label = dt.date.fromisoformat(m + "-01").strftime("%b")
        bars.append(f'<text x="{x + slot*0.3:.1f}" y="{by+22}" text-anchor="middle" class="mono" '
                    f'font-size="10.5" fill="{t["blue"] if i == best else t["muted"]}">{label}</text>')
        if i == best:
            bars.append(f'<text x="{x + slot*0.3:.1f}" y="{by-h-10:.1f}" text-anchor="middle" '
                        f'class="mono val" font-size="12" fill="{t["blue"]}" '
                        f'style="animation-delay:{0.5 + len(months)*0.06 + 0.4:.2f}s">{n}</text>')
    bd, bn = s["busiest"]
    figures = [(s["total"], "contributions"), (s["active"], "active months"),
               (s["longest"], "day best streak"), (bn, f"busiest day · {bd.strftime('%d %b')}")]
    stat_svg = []
    for i, (v, lbl) in enumerate(figures):
        x = 40 + i * 205
        stat_svg.append(f'<g class="up" style="animation-delay:{0.1 + i*0.08:.2f}s">'
                        + count_up(v, x, 104, "serif", t["ink"], 0.3 + i * 0.08)
                        + f'<text x="{x}" y="122" class="mono" font-size="11" fill="{t["muted"]}">{escape(lbl)}</text></g>')
    for i in range(1, 4):
        stat_svg.append(f'<line x1="{40 + i*205 - 22}" y1="72" x2="{40 + i*205 - 22}" y2="122" stroke="{t["line"]}"/>')
    body = f"""
{card_bg(W, H, t)}
<text x="40" y="44" class="mono" font-size="11.5" fill="{t['muted']}" letter-spacing="1.5">ACTIVITY · LAST 12 MONTHS</text>
<text x="{W-40}" y="44" text-anchor="end" class="mono" font-size="11.5" fill="{t['muted']}">current streak <tspan fill="{t['blue']}">{s['current']}d</tspan></text>
{''.join(stat_svg)}
<line x1="{bx}" y1="{by}" x2="{bx+bw}" y2="{by}" stroke="{t['line']}"/>
{''.join(bars)}
"""
    css = ".serif{font-size:40px}"
    anim = """
.up{animation:up .7s cubic-bezier(.2,.8,.2,1) both}
@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.bar{transform-box:fill-box;transform-origin:bottom;animation:grow .8s cubic-bezier(.2,.9,.25,1.15) both}
@keyframes grow{from{transform:scaleY(0)}to{transform:none}}
.val{transform-box:fill-box;transform-origin:center;animation:pop .4s cubic-bezier(.3,1.8,.5,1) both}
@keyframes pop{from{opacity:0;transform:scale(.3) translateY(8px)}to{opacity:1;transform:none}}
"""
    return svg(W, H, f"Monthly contributions: {s['total']} total, {s['longest']}-day best streak",
               ("serif", "geistmono"), css, anim, body)


def tile(t: dict, spec: dict, number: int, idx: int) -> str:
    W, H = 286, 200
    bg, fg = t[spec["accent"]], t["on_" + spec["accent"]]
    delay = 0.15 + idx * 0.14
    body = f"""
<defs>{shine_gradient("sh", t, W, 7, 2.5 + idx * 0.6, slant=60)}
<clipPath id="c"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
<g class="swing" style="animation-delay:{delay:.2f}s">
  {card_bg(W, H, t, fill=bg, stroke=False)}
  <g clip-path="url(#c)">
    <circle cx="{W-30}" cy="30" r="10" fill="none" stroke="{fg}" stroke-opacity=".5" class="ring"/>
    <circle cx="{W-30}" cy="30" r="4" fill="{fg}"/>
    <rect width="{W}" height="{H}" fill="url(#sh)"/>
  </g>
  <text x="24" y="40" class="mono" font-size="12" letter-spacing="2" fill="{fg}">{spec['label']}<tspan class="arrow"> ↗</tspan></text>
  {count_up(number, 22, 118, "serif", fg, delay + 0.45)}
  <text x="24" y="146" class="sans" font-size="14" font-weight="600" fill="{fg}">{escape(spec['caption'])}</text>
  <text x="24" y="170" class="sans" font-size="12.5" fill="{fg}" fill-opacity=".78">{escape(spec['sub'])}</text>
</g>
"""
    css = ".serif{font-size:72px}"
    anim = """
.swing{transform-box:view-box;transform-origin:50% 100%;animation:swing .9s cubic-bezier(.2,.9,.3,1.25) both}
@keyframes swing{0%{opacity:0;transform:translateY(60px) rotate(-7deg)}60%{opacity:1;transform:translateY(-5px) rotate(1.2deg)}100%{transform:none}}
.ring{transform-box:fill-box;transform-origin:center;animation:ring 2.4s ease-out infinite 1.4s}
@keyframes ring{from{transform:scale(.6);opacity:1}to{transform:scale(3.4);opacity:0}}
.arrow{animation:nudge 2.4s ease-in-out infinite 1.6s}
@keyframes nudge{0%,60%,100%{opacity:1}75%{opacity:.35}}
"""
    return svg(W, H, f"{spec['label']}: {number} {spec['caption']}", ("serif", "geist", "geistmono"),
               css, anim, body)


def repo_card(t: dict, spec: dict, info: dict, idx: int) -> str:
    W, H = 432, 210
    lang = info.get("language") or ""
    chips, cx = [], 24
    for tag in spec["tags"]:
        w = 14 + len(tag) * 6.6
        chips.append(f'<rect x="{cx}" y="138" width="{w:.0f}" height="22" rx="11" fill="{t["soft"]}"/>'
                     f'<text x="{cx + w/2:.1f}" y="153" text-anchor="middle" class="mono" font-size="11" '
                     f'fill="{t["ink"]}">{escape(tag)}</text>')
        cx += w + 6
    stars = f' · ★ {info["stars"]}' if info.get("stars") else ""
    body = f"""
{card_bg(W, H, t)}
<g class="up" style="animation-delay:{0.1 + idx*0.12:.2f}s">
  <text x="24" y="52" class="serif" font-size="32" fill="{t['ink']}">{escape(spec['name'])}<tspan class="arrow" fill="{t['blue']}" font-size="22" dx="8">↗</tspan></text>
  <text x="24" y="76" class="mono" font-size="11.5" letter-spacing="1" fill="{t['blue']}">{escape(spec['kind'].upper())}</text>
  <text class="sans" font-size="13.5" fill="{t['muted']}">
    <tspan x="24" y="106">{escape(spec['lines'][0])}</tspan>
    <tspan x="24" y="125">{escape(spec['lines'][1])}</tspan>
  </text>
  {''.join(chips)}
  <line x1="24" y1="178" x2="{W-24}" y2="178" stroke="{t['line']}"/>
  <circle cx="30" cy="193" r="5" fill="{LANG_COLORS.get(lang, t['muted'])}"/>
  <text x="42" y="197" class="mono" font-size="11" fill="{t['muted']}">{escape(lang)}{stars}</text>
  <text x="{W-24}" y="197" text-anchor="end" class="mono" font-size="11" fill="{t['muted']}">{escape(spec['meta'])}</text>
</g>
"""
    anim = """
.up{animation:up .7s cubic-bezier(.2,.8,.2,1) both}
@keyframes up{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
.arrow{animation:nudge 2.6s ease-in-out infinite 1.2s}
@keyframes nudge{0%,70%,100%{opacity:1}80%{opacity:.3}}
"""
    return svg(W, H, f"{spec['name']}: {spec['kind']}", ("serif", "geist", "geistmono"), "", anim, body)

# ---------------------------------------------------------------- main


def main() -> None:
    refresh_data()
    contrib, repos = load_data()
    s = stats(contrib)
    CARDS.mkdir(exist_ok=True)
    for mode, t in THEMES.items():
        out = {"hero": hero(t), "graph": graph(t, s), "activity": activity(t, s)}
        for i, spec in enumerate(TILES):
            n = repos["public_repos"] if spec["number"] == "repos" else spec["number"]
            out[f"tile-{spec['key']}"] = tile(t, spec, n, i)
        for i, spec in enumerate(REPOS):
            out[f"repo-{spec['key']}"] = repo_card(t, spec, repos["repos"].get(spec["repo"], {}), i % 2)
        for name, content in out.items():
            (CARDS / f"{name}-{mode}.svg").write_text(content)
    print(f"rendered {len(out) * len(THEMES)} cards{' (static)' if STATIC else ''}")


if __name__ == "__main__":
    main()
