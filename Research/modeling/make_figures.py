"""Generate the authored figures FROM the models — stdlib only, SVG by hand.

Figures read the same modules the data does, so a corrected number propagates
automatically and cannot drift from the table it assesses (working rule 4 of
the research programme).

    python3 make_figures.py     # writes Research/figures/authored/*.svg
"""

from __future__ import annotations

import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import forces
import allegiance
from calendar import t_of_julian

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures", "authored")

BG = "#14171c"; FG = "#e8e4da"; MUT = "#9a948a"; GRID = "#2a2f36"
COLORS = {"Spanish": "#6b7fa8", "Tlaxcalteca and Nahua allies": "#3f8f6b",
          "Mexica defenders": "#a83232"}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fig_forces():
    """Log-scale band chart: who fought, phase by phase, as ranges."""
    W, H = 1080, 560
    L, R, T = 250, 230, 90
    x0, x1 = math.log10(100), math.log10(300000)

    def X(v):
        return L + (math.log10(max(v, 100)) - x0) / (x1 - x0) * (W - L - R)

    rows = []
    y = T
    for pid, _, label in forces.PHASES:
        rows.append(("phase", label, y)); y += 30
        for c in forces.SERIES:
            b = forces.SERIES[c][pid]
            if b["hi"] == 0:
                continue
            rows.append(("band", (c, b), y)); y += 24
        y += 14
    H = y + 50

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'font-family="Georgia, serif">',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<text x="{L}" y="34" fill="{FG}" font-size="21">The conquest had more '
         f'participants than the story does</text>',
         f'<text x="{L}" y="56" fill="{MUT}" font-size="13">force composition as the '
         f'sources\' own ranges — log scale; a single confident number would be a bug</text>']
    for e in (100, 1000, 10000, 100000):
        p.append(f'<line x1="{X(e):.0f}" y1="{T-18}" x2="{X(e):.0f}" y2="{H-40}" '
                 f'stroke="{GRID}"/>')
        p.append(f'<text x="{X(e):.0f}" y="{H-22}" fill="{MUT}" font-size="12" '
                 f'text-anchor="middle">{e:,}</text>')
    for kind, payload, y in rows:
        if kind == "phase":
            p.append(f'<text x="24" y="{y+14}" fill="{FG}" font-size="14.5" '
                     f'font-style="italic">{esc(payload)}</text>')
        else:
            c, b = payload
            col = COLORS[c]
            xa, xb = X(b["lo"]), X(b["hi"])
            p.append(f'<text x="{L-10}" y="{y+12}" fill="{MUT}" font-size="12" '
                     f'text-anchor="end">{esc(c.split(" and ")[0])}</text>')
            p.append(f'<rect x="{xa:.0f}" y="{y}" width="{max(xb-xa,3):.0f}" height="15" '
                     f'rx="7" fill="{col}" fill-opacity="0.75"/>')
            lab = f'{b["lo"]:,} – {b["hi"]:,}' + ("  (contested)" if b["confidence"] == "contested" else "")
            p.append(f'<text x="{xb+8:.0f}" y="{y+12}" fill="{FG}" font-size="12">{lab}</text>')
    p.append(f'<text x="{W-16}" y="{H-6}" fill="{MUT}" font-size="11" text-anchor="end">'
             f'generated from modeling/forces.py — the figure cannot drift from the table</text>')
    p.append('</svg>')
    return "\n".join(p)


def fig_allegiance():
    """Stacked step-area of polity counts by state, 1518-1524 monthly."""
    W, H = 900, 480
    L, R, T, B = 70, 210, 92, 50
    t0, t1 = 1518.0, 1524.0
    order = ["alliance-core", "tributary", "contested", "independent", "rival",
             "allied-coalition", "occupied", "colonial-ally", "new-spain", "spanish"]
    color = {"alliance-core": "#a83232", "tributary": "#c96f4a", "contested": "#d9a441",
             "independent": "#7d5fb2", "rival": "#8a6d3b", "allied-coalition": "#3f8f6b",
             "occupied": "#5a7d9a", "colonial-ally": "#4a9a8f", "new-spain": "#8a8f98",
             "spanish": "#6b7fa8"}
    samples = []
    steps = 96
    for i in range(steps + 1):
        t = t0 + (t1 - t0) * i / steps
        samples.append((t, allegiance.counts_at(t)))
    total = max(sum(c.values()) for _, c in samples)

    def X(t):
        return L + (t - t0) / (t1 - t0) * (W - L - R)

    def Y(n):
        return T + (1 - n / total) * (H - T - B)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'font-family="Georgia, serif">',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         f'<text x="{L}" y="30" fill="{FG}" font-size="20">The map is a coalition, '
         f'not a two-colour war</text>',
         f'<text x="{L}" y="50" fill="{MUT}" font-size="13">the {len(allegiance.TIMELINES)} '
         f'modelled polities by allegiance state, 1518–1524 — from modeling/allegiance.py</text>']
    # stacked areas
    for si, state in enumerate(order):
        pts_top, pts_bot = [], []
        for t, counts in samples:
            below = sum(counts.get(s, 0) for s in order[:si])
            here = counts.get(state, 0)
            pts_bot.append((X(t), Y(below)))
            pts_top.append((X(t), Y(below + here)))
        path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts_top) \
               + " L" + " L".join(f"{x:.1f},{y:.1f}" for x, y in reversed(pts_bot)) + " Z"
        p.append(f'<path d="{path}" fill="{color[state]}" fill-opacity="0.85"/>')
    # year gridlines + key event lines
    for yr in range(1518, 1525):
        p.append(f'<line x1="{X(yr):.0f}" y1="{T}" x2="{X(yr):.0f}" y2="{H-B}" '
                 f'stroke="{GRID}"/>')
        p.append(f'<text x="{X(yr):.0f}" y="{H-B+18}" fill="{MUT}" font-size="12" '
                 f'text-anchor="middle">{yr}</text>')
    for i, (label, t) in enumerate((("Tlaxcala pact", t_of_julian(1519, 9, 23)),
                                    ("Noche Triste", t_of_julian(1520, 7, 1)),
                                    ("Texcoco turns", t_of_julian(1520, 12, 31)),
                                    ("the fall", t_of_julian(1521, 8, 13)))):
        ylab = T - 10 - (12 if i % 2 else 0)          # stagger to avoid collisions
        p.append(f'<line x1="{X(t):.0f}" y1="{ylab+3}" x2="{X(t):.0f}" y2="{H-B}" '
                 f'stroke="{FG}" stroke-opacity="0.5" stroke-dasharray="3 3"/>')
        p.append(f'<text x="{X(t):.0f}" y="{ylab}" fill="{FG}" font-size="11" '
                 f'text-anchor="middle">{esc(label)}</text>')
    # legend
    ly = T + 4
    for state in order:
        p.append(f'<rect x="{W-R+16}" y="{ly}" width="12" height="12" '
                 f'fill="{color[state]}"/>')
        p.append(f'<text x="{W-R+34}" y="{ly+10}" fill="{MUT}" font-size="12">'
                 f'{esc(state)}</text>')
        ly += 19
    p.append('</svg>')
    return "\n".join(p)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("forces-bands.svg", fig_forces),
                     ("allegiance-states.svg", fig_allegiance)):
        svg = fn()
        with open(os.path.join(OUT, name), "w") as f:
            f.write(svg)
        print(f"  wrote {name} ({len(svg)/1024:.1f} KB)")


if __name__ == "__main__":
    main()
