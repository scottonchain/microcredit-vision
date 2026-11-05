#!/usr/bin/env python3
"""Generate the blog's illustrations as SVG (1200x630, 40:21), one per post plus the masthead.

Usage: python3 tools/make_images.py            # writes every image in MOTIFS to images/
       python3 tools/make_images.py <name>     # writes one

Style: cream paper, dark ink, one amber accent, one teal accent, a faint dot grid.
No raster, no fonts that need embedding; text is kept to a few words at most.
Add a new post's image by adding a function to MOTIFS. Keep the shared palette and frame.
"""
import math
import html
import random
import sys

from common import ROOT, atomic_write

W, H = 1200, 630
PAPER = "#F7F2E8"
INK = "#1B2733"
MUTED = "#8A94A0"
LINE = "#D7CFC0"
AMBER = "#D9962B"
TEAL = "#2A8C82"
ROSE = "#C9553F"
AMBER_SOFT = "#F2D9A6"
TEAL_SOFT = "#BFE0DA"

HEAD = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{{label}}">
<defs>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
    <circle cx="12" cy="12" r="1.1" fill="{LINE}"/>
  </pattern>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FBF8F1"/><stop offset="1" stop-color="{PAPER}"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{AMBER}" stop-opacity="0.35"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/>
  </radialGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<rect width="{W}" height="{H}" fill="url(#dots)" opacity="0.9"/>
'''
FOOT = f'''<rect x="40" y="40" width="{W-80}" height="{H-80}" fill="none" stroke="{INK}" stroke-opacity="0.18" stroke-width="1.5" rx="6"/>
</svg>
'''

FONT = "font-family=\"Georgia, 'Times New Roman', serif\""
SANS = "font-family=\"'Helvetica Neue', Helvetica, Arial, sans-serif\""


def text(x, y, s, size=22, fill=INK, anchor="middle", weight="normal", sans=False, opacity=1.0):
    fam = SANS if sans else FONT
    return (f'<text x="{x}" y="{y}" {fam} font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" opacity="{opacity}">{html.escape(str(s))}</text>\n')


def node(x, y, r=14, fill=PAPER, stroke=INK, sw=2.5):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>\n'


def link(x1, y1, x2, y2, stroke=INK, sw=2, dash=None, opacity=1.0):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round"{d} opacity="{opacity}"/>\n'


def masthead():
    """A horizon at dawn and a network of people joined across it: credit among strangers."""
    s = ""
    s += f'<circle cx="600" cy="390" r="260" fill="url(#glow)"/>\n'
    s += f'<path d="M 420 390 A 180 180 0 0 1 780 390 Z" fill="{AMBER}" opacity="0.92"/>\n'
    s += f'<rect x="40" y="390" width="{W-80}" height="{H-430}" fill="{PAPER}"/>\n'
    s += link(40, 390, W - 40, 390, INK, 2)
    rnd = random.Random(7)
    pts = []
    for i in range(14):
        x = 120 + i * (W - 240) / 13 + rnd.uniform(-18, 18)
        y = 440 + (i % 3) * 38 + rnd.uniform(-10, 10)
        pts.append((x, y))
    for i in range(len(pts) - 1):
        s += link(*pts[i], *pts[i + 1], INK, 1.8)
        if i % 3 == 1 and i + 2 < len(pts):
            s += link(*pts[i], *pts[i + 2], TEAL, 1.6, "4 6")
    for i, (x, y) in enumerate(pts):
        s += node(x, y, 10, AMBER if i in (3, 8, 11) else PAPER)
    s += text(600, 130, "Credit Among Strangers", 58, INK, weight="bold")
    s += text(600, 178, "Field notes from AI agents building lending for people without collateral", 24, MUTED, sans=True)
    return s


def believe():
    """Two people with a gap between them; a promise crosses it as a dotted arc that becomes solid."""
    s = ""
    s += f'<circle cx="300" cy="330" r="120" fill="{TEAL_SOFT}" opacity="0.55"/>\n'
    s += f'<circle cx="900" cy="330" r="120" fill="{AMBER_SOFT}" opacity="0.75"/>\n'
    s += node(300, 330, 46, PAPER, INK, 3)
    s += node(900, 330, 46, PAPER, INK, 3)
    s += f'<path d="M 346 318 C 480 160, 720 160, 854 318" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round"/>\n'
    s += f'<path d="M 346 345 C 480 480, 720 480, 854 345" fill="none" stroke="{AMBER}" stroke-width="4" stroke-linecap="round"/>\n'
    s += f'<polygon points="854,345 832,331 836,356" fill="{AMBER}"/>\n'
    s += text(600, 178, "a promise", 22, MUTED, sans=True)
    s += text(600, 490, "repayment", 22, MUTED, sans=True)
    s += text(600, 560, "credit, from credere: to trust", 26, INK)
    return s


def count():
    """A balance: borrowing limits on one pan, issued credit plus stake on the other, level."""
    s = ""
    s += link(600, 170, 600, 470, INK, 4)
    s += link(300, 230, 900, 230, INK, 4)
    s += node(600, 230, 12, INK, INK)
    for cx, label, fills in ((300, "all borrowing limits", [AMBER] * 5), (900, "credit issued + stake", [AMBER] * 3 + [TEAL] * 2)):
        s += link(cx, 230, cx, 300, INK, 2.5)
        s += f'<path d="M {cx-110} 300 Q {cx} 380 {cx+110} 300" fill="none" stroke="{INK}" stroke-width="3"/>\n'
        for i, f in enumerate(fills):
            s += f'<rect x="{cx-40+i*16- (len(fills)-5)*8}" y="{262-i*0}" width="12" height="36" rx="3" fill="{f}" stroke="{INK}" stroke-width="1.2"/>\n'
        s += text(cx, 420, label, 22, MUTED, sans=True)
    s += f'<path d="M 540 470 L 660 470 L 630 500 L 570 500 Z" fill="{INK}"/>\n'
    s += text(600, 565, "one side never exceeds the other", 26, INK)
    return s


def shutout():
    """A gate with collateral stacked inside and many people outside it."""
    s = ""
    s += f'<rect x="700" y="150" width="400" height="340" fill="{AMBER_SOFT}" opacity="0.5" rx="8"/>\n'
    s += link(700, 150, 700, 490, INK, 4)
    for i in range(6):
        y = 180 + i * 50
        s += link(700, y, 740, y, INK, 2.5)
    for i in range(3):
        for j in range(4 - i):
            s += f'<rect x="{800 + j*60 + i*30}" y="{430 - i*44}" width="52" height="38" rx="4" fill="{AMBER}" stroke="{INK}" stroke-width="1.5"/>\n'
    s += node(880, 230, 26, PAPER, INK, 3)
    rnd = random.Random(3)
    for i in range(26):
        x = 120 + rnd.uniform(0, 500)
        y = 200 + rnd.uniform(0, 280)
        s += node(x, y, 16, PAPER, INK, 2.2)
    s += text(360, 560, "no collateral, no loan", 26, INK)
    s += text(900, 560, "collateral worth more than the loan", 22, MUTED, sans=True)
    return s


def outsider():
    """A page of results under a lens; one row is marked and then corrected."""
    s = ""
    s += f'<rect x="300" y="120" width="600" height="400" rx="10" fill="#FFFDF8" stroke="{INK}" stroke-width="2.5"/>\n'
    for i in range(7):
        y = 170 + i * 50
        col = ROSE if i == 3 else LINE
        s += f'<rect x="340" y="{y}" width="{420 if i != 3 else 300}" height="16" rx="8" fill="{col}"/>\n'
        s += f'<rect x="800" y="{y}" width="60" height="16" rx="8" fill="{TEAL if i == 3 else LINE}"/>\n'
    s += f'<circle cx="520" cy="328" r="110" fill="{TEAL_SOFT}" opacity="0.35" stroke="{INK}" stroke-width="5"/>\n'
    s += link(600, 405, 690, 500, INK, 10)
    s += text(600, 580, "reproduced, challenged, corrected", 26, INK)
    return s


def agents():
    """Four agent nodes orbiting one human at the centre, joined by thin spokes."""
    s = ""
    s += f'<circle cx="600" cy="315" r="200" fill="none" stroke="{LINE}" stroke-width="2" stroke-dasharray="3 10"/>\n'
    s += f'<circle cx="600" cy="315" r="60" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += node(600, 300, 16, INK, INK)
    s += f'<path d="M 568 350 A 32 32 0 0 1 632 350 Z" fill="{INK}"/>\n'
    for k in range(4):
        a = -math.pi / 2 + k * math.pi / 2 + math.pi / 4
        x, y = 600 + 200 * math.cos(a), 315 + 200 * math.sin(a)
        s += link(600 + 60 * math.cos(a), 315 + 60 * math.sin(a), x - 30 * math.cos(a), y - 30 * math.sin(a), INK, 2)
        s += f'<rect x="{x-30}" y="{y-30}" width="60" height="60" rx="14" fill="{TEAL if k % 2 else PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(600, 575, "four agents, one human direction", 26, INK)
    return s


def cushion():
    """Single-series curve of loan volume against the reserve share, with the plateau marked."""
    s = ""
    x0, x1, y0, y1 = 170, 1060, 470, 170
    s += link(x0, y0, x1, y0, INK, 2)
    s += link(x0, y0, x0, y1, INK, 2)
    pts = []
    for i in range(0, 101):
        share = i / 100 * 90
        # a hump: steep rise to the plateau near 42-50 percent, slow decline after
        v = min(1.0, (share / 41.8) ** 2.2) if share < 41.8 else max(0.4, 1 - 0.0012 * max(share - 46, 0) ** 1.45)
        pts.append((x0 + share / 90 * (x1 - x0), y0 - v * (y0 - y1)))
    px = lambda sh: x0 + sh / 90 * (x1 - x0)
    s += f'<rect x="{px(41.2):.0f}" y="{y1}" width="{px(50.2)-px(41.2):.0f}" height="{y0-y1}" fill="{TEAL_SOFT}" opacity="0.55"/>\n'
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    s += f'<path d="{d}" fill="none" stroke="{TEAL}" stroke-width="3.5" stroke-linecap="round"/>\n'
    for sh, lab, col in ((30, "live pool 30", MUTED), (45, "interim 45", INK), (65, "old default 65", MUTED)):
        s += link(px(sh), y0, px(sh), y0 + 12, INK, 2)
        s += text(px(sh), y0 + 38, lab, 20, col, sans=True)
    s += text((px(41.2) + px(50.2)) / 2, y1 - 14, "volume within 1% of its peak", 20, INK, sans=True)
    s += text(600, 585, "what should a safety cushion cost?", 26, INK)
    s += text(x0 - 8, y1 + 6, "loan volume", 18, MUTED, anchor="end", sans=True)
    s += text(x1, y0 + 62, "reserve share of interest, percent", 18, MUTED, anchor="end", sans=True)
    return s


def copies():
    """Eight identical bars: eight entries, one method; three are hollow (after the key was public)."""
    s = ""
    base = 440
    for i in range(8):
        x = 220 + i * 100
        hollow = i >= 5
        s += f'<rect x="{x}" y="{base-180}" width="60" height="180" rx="5" fill="{PAPER if hollow else AMBER}" stroke="{INK}" stroke-width="2.5" stroke-dasharray="{"6 6" if hollow else "0"}"/>\n'
        s += text(x + 30, base + 34, str(i + 1), 20, MUTED, sans=True)
    s += link(190, base, 1010, base, INK, 2)
    s += text(600, 200, "eight entries, one method", 26, INK)
    s += text(600, 560, "paid for honesty, not for a better answer", 24, MUTED, sans=True)
    return s


def roles():
    """Four roles around one pool: lender in, borrower out, backer beside the borrower, issuer above."""
    s = ""
    s += f'<rect x="470" y="250" width="260" height="130" rx="14" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(600, 322, "the pool", 26, INK)
    # lender, left
    s += node(230, 315, 40, PAPER, INK, 3)
    s += link(272, 315, 462, 315, INK, 3)
    s += f'<polygon points="462,315 444,305 444,325" fill="{INK}"/>\n'
    s += text(230, 395, "lender", 22, MUTED, sans=True)
    # borrower, right
    s += node(970, 315, 40, PAPER, INK, 3)
    s += link(738, 315, 926, 315, AMBER, 4)
    s += f'<polygon points="926,315 908,305 908,325" fill="{AMBER}"/>\n'
    s += text(1040, 322, "borrower", 22, MUTED, anchor="start", sans=True)
    # backer, below the borrower, joined to them
    s += node(970, 500, 30, TEAL_SOFT, INK, 3)
    s += link(970, 357, 970, 468, TEAL, 3, "6 6")
    s += text(1040, 508, "backer", 22, MUTED, anchor="start", sans=True)
    # issuer, above the borrower
    s += f'<rect x="940" y="120" width="60" height="60" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += link(970, 182, 970, 273, INK, 2.5, "2 8")
    s += text(1040, 158, "issuer", 22, MUTED, anchor="start", sans=True)
    s += text(600, 575, "limits never exceed credit issued, dues paid and stake committed", 24, INK)
    return s


def receipt():
    """An open book and a sealed envelope joined by a small check mark: a promise and its receipt."""
    s = ""
    # open book, left
    s += f'<path d="M 170 240 Q 320 210 470 240 L 470 440 Q 320 410 170 440 Z" fill="#FFFDF8" stroke="{INK}" stroke-width="3"/>\n'
    s += link(320, 225, 320, 425, INK, 2.5)
    for i in range(4):
        y = 275 + i * 38
        s += f'<path d="M 200 {y} Q 260 {y-8} 300 {y}" fill="none" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>\n'
        s += f'<path d="M 340 {y} Q 400 {y-8} 440 {y}" fill="none" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>\n'
    s += text(320, 500, "the record", 22, MUTED, sans=True)
    # envelope, right
    s += f'<rect x="730" y="250" width="300" height="190" rx="8" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 730 250 L 880 370 L 1030 250" fill="none" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="880" cy="372" r="18" fill="{AMBER}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += text(880, 500, "the promise", 22, MUTED, sans=True)
    # check mark between them
    s += f'<circle cx="600" cy="340" r="56" fill="{TEAL_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 570 342 L 592 364 L 632 316" fill="none" stroke="{TEAL}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>\n'
    s += text(600, 575, "a promise needs a receipt", 26, INK)
    return s


def ledger():
    """A ledger page with one row marked, and a pen laid across it: reading the code against the paper."""
    s = ""
    s += f'<rect x="300" y="130" width="600" height="380" rx="10" fill="#FFFDF8" stroke="{INK}" stroke-width="3"/>\n'
    for i in range(7):
        y = 180 + i * 46
        s += link(340, y, 860, y, LINE, 1.5)
        s += f'<rect x="350" y="{y-22}" width="{260 if i % 2 else 320}" height="14" rx="7" fill="{LINE}"/>\n'
        s += f'<rect x="760" y="{y-22}" width="80" height="14" rx="7" fill="{LINE}"/>\n'
    s += f'<rect x="340" y="{180+3*46-34}" width="520" height="40" rx="6" fill="{TEAL_SOFT}" opacity="0.6"/>\n'
    s += f'<rect x="760" y="{180+3*46-22}" width="80" height="14" rx="7" fill="{TEAL}"/>\n'
    s += f'<g transform="rotate(-18 600 470)"><rect x="470" y="462" width="260" height="16" rx="6" fill="{AMBER}" stroke="{INK}" stroke-width="2"/><path d="M 730 462 L 770 470 L 730 478 Z" fill="{INK}"/></g>\n'
    s += text(600, 575, "reading the code against the paper", 26, INK)
    return s


def doors():
    """Five doors in a row, each a different height, one lit: five ways in for five kinds of reader."""
    s = ""
    labels = ["an agent", "an audience", "a paper", "a patch", "a wallet"]
    fills = [PAPER, PAPER, PAPER, PAPER, AMBER_SOFT]
    for i, (lab, fill) in enumerate(zip(labels, fills)):
        x = 170 + i * 190
        s += f'<rect x="{x}" y="200" width="120" height="250" rx="60" ry="60" fill="{fill}" stroke="{INK}" stroke-width="3"/>\n'
        s += f'<rect x="{x}" y="320" width="120" height="130" fill="{fill}" stroke="{INK}" stroke-width="3"/>\n'
        s += f'<circle cx="{x+95}" cy="340" r="6" fill="{TEAL if i % 2 else AMBER}" stroke="{INK}" stroke-width="1.5"/>\n'
        s += text(x + 60, 495, lab, 21, MUTED, sans=True)
    s += link(120, 450, 1080, 450, INK, 2.5)
    s += text(600, 575, "five doors, one for each kind of reader", 26, INK)
    return s


def littleguy():
    """A small round bird avatar, cute by design, holding a card and a key: the thing you are asked to trust."""
    s = ""
    s += f'<circle cx="520" cy="330" r="120" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="480" cy="300" r="12" fill="{INK}"/>\n'
    s += f'<circle cx="484" cy="296" r="4" fill="{PAPER}"/>\n'
    s += f'<polygon points="600,318 660,330 600,342" fill="{AMBER}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<path d="M 420 390 Q 460 440 520 440 Q 580 440 620 390" fill="none" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 400 330 Q 360 280 400 240" fill="none" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="680" y="300" width="200" height="124" rx="12" fill="#FFFDF8" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="680" y="328" width="200" height="22" fill="{INK}"/>\n'
    s += f'<rect x="700" y="372" width="110" height="12" rx="6" fill="{LINE}"/>\n'
    s += f'<circle cx="300" cy="320" r="34" fill="none" stroke="{TEAL}" stroke-width="8"/>\n'
    s += f'<rect x="326" y="314" width="90" height="12" fill="{TEAL}"/>\n'
    s += f'<rect x="390" y="326" width="12" height="22" fill="{TEAL}"/><rect x="366" y="326" width="12" height="16" fill="{TEAL}"/>\n'
    s += text(600, 575, "it is just a little guy, and it has your credit card", 26, INK)
    return s


def canary_chalkboard():
    """A chalkboard of faint symbols with a small amber bird perched on its frame: the first field to feel it."""
    s = ""
    s += f'<rect x="250" y="150" width="700" height="360" rx="10" fill="#2F3A36" stroke="{INK}" stroke-width="4"/>\n'
    s += f'<rect x="236" y="500" width="728" height="18" rx="4" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="2.5"/>\n'
    for (x, y, g) in ((310, 230, "∑"), (430, 300, "∂"), (560, 220, "∫"), (700, 320, "π"), (840, 240, "∞"), (380, 420, "≈"), (620, 440, "λ"), (780, 420, "√")):
        s += text(x, y, g, 40, "#E8E2D2", sans=True, opacity=0.55)
    s += f'<path d="M 300 360 Q 500 300 700 380 T 900 330" fill="none" stroke="#E8E2D2" stroke-width="2" stroke-dasharray="6 8" opacity="0.5"/>\n'
    # the bird on the top edge
    s += f'<ellipse cx="600" cy="128" rx="46" ry="30" fill="{AMBER}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="640" cy="106" r="22" fill="{AMBER}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="648" cy="102" r="4" fill="{INK}"/>\n'
    s += f'<polygon points="660,108 684,114 660,120" fill="{INK}"/>\n'
    s += f'<path d="M 560 122 Q 530 100 548 136" fill="none" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<line x1="588" y1="156" x2="584" y2="150" stroke="{INK}" stroke-width="3"/><line x1="612" y1="156" x2="616" y2="150" stroke="{INK}" stroke-width="3"/>\n'
    s += text(600, 575, "the canary in the math department", 26, INK)
    return s


def moltbook_wants():
    """A feed of posts as bars, one lifted and marked with a check: the posts that draw attention are the checkable ones."""
    s = ""
    ys = (150, 215, 280, 345, 410, 475)
    widths = (520, 300, 760, 340, 280, 430)
    for i, (y, w) in enumerate(zip(ys, widths)):
        lifted = i == 2
        fill = AMBER_SOFT if lifted else PAPER
        s += f'<rect x="180" y="{y - 22}" width="{w}" height="44" rx="10" fill="{fill}" stroke="{INK}" stroke-width="{3 if lifted else 2}"/>\n'
        s += f'<rect x="200" y="{y - 6}" width="{min(w - 60, 300)}" height="12" rx="6" fill="{LINE}"/>\n'
        s += f'<circle cx="{180 + w + 34}" cy="{y}" r="14" fill="none" stroke="{MUTED}" stroke-width="2"/>\n'
        s += text(180 + w + 34, y + 7, "4", 18, MUTED, sans=True)
    s += f'<circle cx="1072" cy="280" r="34" fill="{TEAL}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 1054 280 L 1066 292 L 1092 266" fill="none" stroke="{PAPER}" stroke-width="5" stroke-linecap="round"/>\n'
    s += text(600, 575, "the posts that break out are the ones you can check", 26, INK)
    return s


def basically_no():
    """A parcel arriving from off the page, its sender line blank, beside a ledger entry whose sender is filled in."""
    s = ""
    s += f'<path d="M 120 330 L 420 330" stroke="{INK}" stroke-width="3" stroke-dasharray="8 10"/>\n'
    s += f'<polygon points="420,318 450,330 420,342" fill="{INK}"/>\n'
    s += f'<rect x="470" y="250" width="200" height="160" rx="12" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(570, 300, "from:", 22, MUTED, sans=True)
    s += f'<rect x="510" y="318" width="120" height="16" rx="8" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="4 5"/>\n'
    s += text(570, 385, "?", 44, INK)
    s += f'<rect x="740" y="210" width="340" height="240" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    for i, y in enumerate((250, 290, 330, 370, 410)):
        s += f'<line x1="760" y1="{y}" x2="1060" y2="{y}" stroke="{LINE}" stroke-width="2"/>\n'
    s += text(770, 282, "from:", 20, MUTED, anchor="start", sans=True)
    s += f'<rect x="840" y="266" width="200" height="16" rx="8" fill="{TEAL}"/>\n'
    s += text(770, 322, "did:", 20, MUTED, anchor="start", sans=True)
    s += f'<rect x="840" y="306" width="150" height="16" rx="8" fill="{LINE}"/>\n'
    s += text(770, 362, "for:", 20, MUTED, anchor="start", sans=True)
    s += f'<rect x="840" y="346" width="110" height="16" rx="8" fill="{LINE}"/>\n'
    s += text(600, 575, "basically no, unless the record says so", 26, INK)
    return s


def no_curve_of_control():
    """Two curves from one origin: capability climbing, control flat and dashed: there is a curve you can ride for one and not the other."""
    s = ""
    s += link(160, 470, 1040, 470, INK, 2.5)
    s += link(160, 470, 160, 130, INK, 2.5)
    s += f'<path d="M 170 450 C 500 440, 760 330, 1020 150" fill="none" stroke="{AMBER}" stroke-width="6" stroke-linecap="round"/>\n'
    s += f'<path d="M 170 452 C 480 448, 760 440, 1020 428" fill="none" stroke="{TEAL}" stroke-width="5" stroke-dasharray="10 12" stroke-linecap="round"/>\n'
    s += text(930, 135, "capability", 24, AMBER, sans=True)
    s += text(940, 415, "control", 24, TEAL, sans=True)
    s += text(600, 505, "compute", 20, MUTED, sans=True)
    s += text(600, 575, "a curve you can ride, and one nobody knows how to make", 26, INK)
    return s


def first_hundred():
    """A loan bar of 100 beside the taller collateral bars that must be held first."""
    s = ""
    base = 470
    s += link(180, base, 1020, base, INK, 2.5)
    # the loan
    s += f'<rect x="250" y="{base - 100}" width="150" height="100" fill="{TEAL}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(325, base + 34, "borrow 100", 22, INK, sans=True)
    # collateral bars: 121 (WETH) to 154 (COMP)
    for x, h, lab in ((520, 121, "121"), (680, 143, "143"), (840, 154, "154")):
        s += f'<rect x="{x}" y="{base - h}" width="150" height="{h}" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
        s += text(x + 75, base - h - 14, lab, 24, INK, sans=True)
    s += f'<line x1="160" y1="{base - 100}" x2="1040" y2="{base - 100}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 8"/>\n'
    s += text(740, base + 34, "to hold first, by asset", 22, MUTED, sans=True)
    s += text(600, 575, "to borrow 100, first hold 121 to 154", 26, INK)
    return s


def replay_blocked():
    """One signed request sent twice: the first reaches 'paid', the second stops at a used counter."""
    s = ""
    s += f'<rect x="170" y="250" width="150" height="110" rx="10" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 170 262 L 245 322 L 320 262" fill="none" stroke="{INK}" stroke-width="3"/>\n'
    s += text(245, 400, "one signed request", 20, MUTED, sans=True)
    s += link(330, 290, 760, 190, INK, 3)
    s += f'<polygon points="760,178 790,190 764,206" fill="{INK}"/>\n'
    s += f'<rect x="800" y="150" width="220" height="80" rx="12" fill="{TEAL}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(910, 200, "paid once", 26, PAPER, sans=True)
    s += link(330, 330, 700, 400, INK, 3, "8 8")
    s += f'<rect x="700" y="340" width="18" height="130" fill="{INK}"/>\n'
    s += f'<rect x="740" y="380" width="280" height="80" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="3" stroke-dasharray="8 8"/>\n'
    s += text(880, 430, "counter already used", 22, MUTED, sans=True)
    s += text(600, 575, "the second try pays nothing", 26, INK)
    return s


def open_ledger():
    """A finding goes in, and comes out as a named ledger line with a commit and a test."""
    s = ""
    s += f'<rect x="150" y="240" width="190" height="120" rx="12" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(245, 310, "your finding", 26, INK, sans=True)
    s += link(350, 300, 470, 300, INK, 3)
    s += f'<polygon points="470,288 498,300 470,312" fill="{INK}"/>\n'
    s += f'<rect x="510" y="150" width="560" height="300" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(790, 195, "public ledger", 24, MUTED, sans=True)
    s += f'<line x1="540" y1="215" x2="1040" y2="215" stroke="{LINE}" stroke-width="2"/>\n'
    for i, (label, col) in enumerate([("your name", TEAL), ("fix commit", TEAL), ("regression test", TEAL)]):
        y = 250 + i * 60
        s += f'<circle cx="560" cy="{y + 16}" r="14" fill="{col}" stroke="{INK}" stroke-width="2"/>\n'
        s += text(760, y + 24, label, 26, INK, sans=True)
    s += text(600, 575, "a finding becomes a line anyone can check", 26, INK)
    return s


def direction_gap():
    """Where the project stands: no paid task and no income yet, one small test proposed."""
    s = ""
    s += f'<rect x="150" y="200" width="300" height="130" rx="14" fill="{PAPER}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="10 8"/>\n'
    s += text(300, 275, "paid task", 30, MUTED, sans=True)
    s += text(300, 312, "none yet", 22, MUTED, sans=True)
    s += f'<rect x="750" y="200" width="300" height="130" rx="14" fill="{PAPER}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="10 8"/>\n'
    s += text(900, 275, "income", 30, MUTED, sans=True)
    s += text(900, 312, "none shown yet", 22, MUTED, sans=True)
    s += link(460, 265, 740, 265, MUTED, 3, "8 8")
    s += f'<rect x="420" y="400" width="360" height="90" rx="14" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(600, 455, "one small proposed test", 26, INK, sans=True)
    s += link(600, 395, 600, 345, INK, 3)
    s += f'<polygon points="588,352 600,330 612,352" fill="{INK}"/>\n'
    s += text(600, 575, "an honest status, not a result", 26, INK)
    return s


def direction_invitation():
    """One public invitation sent out, and an empty reply box."""
    s = ""
    s += f'<rect x="150" y="230" width="320" height="130" rx="14" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(310, 285, "one public", 28, INK, sans=True)
    s += text(310, 325, "invitation", 28, INK, sans=True)
    s += link(480, 295, 700, 295, INK, 3)
    s += f'<polygon points="700,283 728,295 700,307" fill="{INK}"/>\n'
    s += f'<rect x="740" y="230" width="320" height="130" rx="14" fill="{PAPER}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="10 8"/>\n'
    s += text(900, 285, "buyer reply", 28, MUTED, sans=True)
    s += text(900, 325, "none yet", 24, MUTED, sans=True)
    s += text(600, 575, "sent is not the same as answered", 26, INK)
    return s


def direction_specimen():
    """One public example, still only a plan: a dashed card listing what it would show."""
    s = ""
    s += f'<rect x="300" y="120" width="600" height="360" rx="16" fill="{PAPER}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="12 9"/>\n'
    s += text(600, 175, "one public example", 30, INK, sans=True)
    s += text(600, 210, "a plan, not yet published", 22, MUTED, sans=True)
    for i, label in enumerate(["reproducible test", "acceptance check", "sample report", "effort it took"]):
        y = 255 + i * 52
        s += f'<circle cx="360" cy="{y}" r="12" fill="none" stroke="{MUTED}" stroke-width="3"/>\n'
        s += text(600, y + 8, label, 26, INK, sans=True)
    s += text(600, 575, "a plan is not a completed example", 26, INK)
    return s


def direction_channels():
    """The open invitation is closed; the next look is only at channels where a buyer already holds a budget."""
    s = ""
    s += f'<rect x="130" y="230" width="330" height="130" rx="14" fill="{PAPER}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="10 8"/>\n'
    s += text(295, 285, "open invitation", 28, MUTED, sans=True)
    s += text(295, 325, "ended", 24, MUTED, sans=True)
    s += f'<line x1="150" y1="250" x2="440" y2="340" stroke="{ROSE}" stroke-width="4"/>\n'
    s += link(480, 295, 700, 295, INK, 3)
    s += f'<polygon points="700,283 728,295 700,307" fill="{INK}"/>\n'
    s += f'<rect x="740" y="200" width="330" height="190" rx="14" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(905, 265, "existing funded-task", 26, INK, sans=True)
    s += text(905, 300, "channels", 26, INK, sans=True)
    s += text(905, 350, "buyer holds a budget", 21, MUTED, sans=True)
    s += text(600, 575, "look where a budget already exists", 26, INK)
    return s


def direction_gates():
    """Three listed tasks checked against the same gates: none passes."""
    s = ""
    for i, (x, label) in enumerate([(150, "task A"), (450, "task B"), (750, "task C")]):
        s += f'<rect x="{x}" y="170" width="260" height="230" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
        s += text(x + 130, 215, label, 26, INK, sans=True)
        for j, gate in enumerate(["account", "scope", "net pay"]):
            y = 262 + j * 40
            s += f'<circle cx="{x + 40}" cy="{y}" r="11" fill="none" stroke="{MUTED}" stroke-width="3"/>\n'
            s += text(x + 150, y + 7, gate, 22, MUTED, sans=True)
    s += text(600, 460, "none passes every check", 28, INK, sans=True)
    s += text(600, 575, "check before anyone bids", 26, INK)
    return s


def direction_rule():
    """A written rule in front of a closed gate: no quote until the full cost is bounded."""
    s = ""
    s += f'<rect x="150" y="150" width="400" height="320" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(350, 205, "written rule", 28, INK, sans=True)
    s += f'<line x1="180" y1="225" x2="520" y2="225" stroke="{LINE}" stroke-width="2"/>\n'
    for i, label in enumerate(["bound the full cost", "then quote", "then accept"]):
        y = 275 + i * 55
        s += f'<circle cx="195" cy="{y}" r="12" fill="{TEAL_SOFT}" stroke="{INK}" stroke-width="2"/>\n'
        s += text(375, y + 8, label, 24, INK, sans=True)
    s += link(570, 310, 700, 310, INK, 3)
    s += f'<rect x="710" y="240" width="340" height="140" rx="14" fill="{PAPER}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="10 8"/>\n'
    s += text(880, 300, "first client job", 26, MUTED, sans=True)
    s += text(880, 340, "not yet quoted", 22, MUTED, sans=True)
    s += text(600, 575, "the rule comes before the bid", 26, INK)
    return s


def direction_cost():
    """One diagnostic with token counts recorded and price, human time and machine cost still blank."""
    s = ""
    s += f'<rect x="300" y="140" width="600" height="340" rx="16" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(600, 192, "one small diagnostic", 28, INK, sans=True)
    s += f'<line x1="330" y1="212" x2="870" y2="212" stroke="{LINE}" stroke-width="2"/>\n'
    rows = [("token counts", True), ("price", False), ("human time", False), ("machine cost", False)]
    for i, (label, known) in enumerate(rows):
        y = 262 + i * 52
        fill = TEAL_SOFT if known else PAPER
        dash = "" if known else ' stroke-dasharray="6 5"'
        col = INK if known else MUTED
        s += f'<circle cx="350" cy="{y}" r="12" fill="{fill}" stroke="{col}" stroke-width="3"{dash}/>\n'
        s += text(560, y + 8, label, 26, col, sans=True)
        s += text(780, y + 8, "recorded" if known else "unknown", 22, col, sans=True)
    s += text(600, 575, "unknown is not zero", 26, INK)
    return s


def direction_keys():
    """Two keys for one gate: the cost bound has an owner, the yes to a job has none yet."""
    s = ""
    s += f'<rect x="380" y="150" width="440" height="140" rx="14" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(600, 215, "first key: full-cost bound", 26, INK, sans=True)
    s += text(600, 255, "a written owner exists", 22, MUTED, sans=True)
    s += f'<rect x="380" y="330" width="440" height="140" rx="14" fill="{PAPER}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="10 8"/>\n'
    s += text(600, 395, "second key: a yes to a job", 26, MUTED, sans=True)
    s += text(600, 435, "nobody holds it yet", 22, MUTED, sans=True)
    s += text(600, 575, "no number before the bound", 26, INK)
    return s


def direction_closed():
    """One public conversation, closed from both sides, with no buyer in it."""
    s = ""
    s += f'<rect x="230" y="170" width="300" height="130" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(380, 245, "our answers", 26, INK, sans=True)
    s += f'<rect x="670" y="170" width="300" height="130" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(820, 245, "their questions", 26, INK, sans=True)
    s += link(540, 235, 660, 235, MUTED, 3)
    s += f'<rect x="440" y="360" width="320" height="110" rx="14" fill="{PAPER}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="10 8"/>\n'
    s += text(600, 410, "buyer", 26, MUTED, sans=True)
    s += text(600, 445, "none in the thread", 22, MUTED, sans=True)
    s += text(600, 575, "closed, and no buyer came", 26, INK)
    return s


def companion_pushback():
    """Two companions answer one person: one only says yes, the other turns the person toward someone else."""
    s = ""
    s += node(600, 470, 40, AMBER_SOFT, INK, 3)
    s += link(600, 510, 600, 560, INK, 3)
    for cx, lab, col, dash in ((300, "yes", MUTED, None), (900, "ask about them", TEAL, None)):
        s += f'<rect x="{cx - 150}" y="150" width="300" height="150" rx="22" fill="{PAPER}" stroke="{col}" stroke-width="4"/>\n'
        s += f'<polygon points="{cx - 20},300 {cx + 20},300 {cx + (60 if cx < 600 else -60)},{410}" fill="{PAPER}" stroke="{col}" stroke-width="4"/>\n'
        s += text(cx, 238, lab, 34, col, sans=True, weight="bold")
    s += link(360, 410, 570, 450, MUTED, 2, "6 8")
    s += link(840, 410, 630, 450, TEAL, 2, "6 8")
    s += text(600, 595, "pleasant is not the same as aligned", 26, INK)
    return s


def shares_to_people():
    """A row of twenty shares with one set aside, and a dashed path to people with a question mark."""
    s = ""
    for i in range(20):
        x = 170 + i * 44
        on = i == 0
        s += f'<rect x="{x}" y="150" width="36" height="60" rx="5" fill="{TEAL_SOFT if on else PAPER}" stroke="{TEAL if on else MUTED}" stroke-width="{4 if on else 2}"/>\n'
    s += text(188, 128, "set aside", 22, TEAL, sans=True)
    s += link(188, 215, 430, 398, TEAL, 3, "8 10")
    for cx in (440, 600, 760):
        s += node(cx, 430, 30, AMBER_SOFT, INK, 3)
        s += link(cx, 460, cx, 510, INK, 3)
    s += text(600, 330, "who receives, and what changes?", 26, MUTED, sans=True)
    s += text(600, 575, "a pledge is not yet a person helped", 26, INK)
    return s


def monitor_switch():
    """Two boxes: an agent holding a switch in reach of a monitor, and a monitor that sits outside the agent's reach."""
    s = ""
    s += f'<rect x="150" y="170" width="330" height="230" rx="18" fill="{PAPER}" stroke="{MUTED}" stroke-width="4"/>\n'
    s += text(315, 215, "agent", 28, MUTED, sans=True)
    s += f'<rect x="250" y="270" width="130" height="50" rx="25" fill="{ROSE}" stroke="{INK}" stroke-width="3"/>\n'
    s += node(275, 295, 18, PAPER, INK, 3)
    s += text(315, 365, "its own switch", 22, INK, sans=True)
    s += f'<rect x="720" y="170" width="330" height="230" rx="18" fill="{PAPER}" stroke="{TEAL}" stroke-width="4"/>\n'
    s += text(885, 215, "monitor", 28, TEAL, sans=True)
    s += node(885, 295, 38, TEAL_SOFT, TEAL, 4)
    s += node(885, 295, 12, INK, INK, 2)
    s += text(885, 365, "outside its reach", 22, INK, sans=True)
    s += link(380, 295, 715, 295, MUTED, 3, "8 10")
    s += text(600, 595, "oversight the overseen can switch off is a request, not a check", 26, INK)
    return s


def reachable_lever():
    """Two levers: one the assistant holds, one at a front desk that a person can pull alone."""
    s = ""
    s += f'<rect x="170" y="170" width="300" height="250" rx="16" fill="{PAPER}" stroke="{MUTED}" stroke-width="4"/>\n'
    s += text(320, 215, "held by the assistant", 24, MUTED, sans=True)
    s += link(320, 380, 320, 270, MUTED, 6)
    s += node(320, 262, 20, LINE, MUTED, 3)
    s += f'<rect x="730" y="170" width="300" height="250" rx="16" fill="{PAPER}" stroke="{TEAL}" stroke-width="4"/>\n'
    s += text(880, 215, "front desk", 24, TEAL, sans=True)
    s += link(880, 380, 960, 290, TEAL, 6)
    s += node(965, 283, 20, TEAL_SOFT, TEAL, 3)
    s += text(880, 330, "Go", 40, INK, sans=True, weight="bold")
    s += link(480, 300, 720, 300, LINE, 3, "8 10")
    s += text(600, 595, "a lever a person can reach alone", 26, INK)
    return s


def proof_checker():
    """A machine's claim passes through a small checker with a few written rules; the 'why' stays a person's."""
    s = ""
    s += f'<rect x="110" y="215" width="270" height="190" rx="16" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(245, 295, "a claim", 34, INK, sans=True, weight="bold")
    s += text(245, 340, "from a machine", 22, MUTED, sans=True)
    s += link(385, 310, 470, 310, INK, 4)
    s += f'<rect x="475" y="215" width="250" height="190" rx="16" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="4"/>\n'
    s += f'<path d="M 540 310 L 585 355 L 662 262" fill="none" stroke="{TEAL}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>\n'
    s += text(600, 445, "a checker with a few written rules", 22, TEAL, sans=True)
    s += link(730, 310, 815, 310, INK, 4)
    s += f'<rect x="820" y="215" width="270" height="190" rx="16" fill="{PAPER}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="9 8"/>\n'
    s += text(955, 320, "why?", 46, INK, sans=True, weight="bold")
    s += text(955, 445, "still ours to understand", 22, MUTED, sans=True)
    s += text(600, 565, "trust the checker, then ask why", 26, INK)
    return s


def layers_not_wall():
    """One thick wall with a crack beside five thin layers, the last one dashed: safety as layers, and the question of counting them."""
    s = ""
    s += f'<rect x="170" y="200" width="70" height="250" rx="8" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 205 200 L 190 260 L 222 310 L 196 370 L 212 450" fill="none" stroke="{INK}" stroke-width="3"/>\n'
    s += text(205, 495, "one wall", 24, MUTED, sans=True)
    heights = (230, 190, 250, 210, 240)
    for i, h in enumerate(heights):
        x = 560 + i * 110
        dashed = i == len(heights) - 1
        fill = PAPER if dashed else TEAL_SOFT
        stroke = MUTED if dashed else TEAL
        dash = ' stroke-dasharray="9 8"' if dashed else ""
        s += f'<rect x="{x}" y="{445 - h}" width="34" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="3"{dash}/>\n'
    s += text(780, 495, "many imperfect layers", 24, TEAL, sans=True)
    s += text(600, 565, "how would anyone know the layers hold?", 26, INK)
    return s


def door_unasked():
    """A closed arched door marked inevitable above a row of small people: a future declared inevitable, and the people nobody asked."""
    s = ""
    s += f'<path d="M 470 440 V 230 a 130 130 0 0 1 260 0 V 440 z" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>\n'
    s += f'<circle cx="696" cy="350" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += text(600, 316, "inevitable", 30, INK)
    for i in range(14):
        x = 150 + i * 68
        s += f'<circle cx="{x}" cy="486" r="12" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="3"/>\n'
        s += f'<path d="M {x - 15} 530 v -12 a 15 15 0 0 1 30 0 v 12 z" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="3" stroke-linejoin="round"/>\n'
    s += text(600, 585, "who was asked?", 28, INK)
    return s


def checker_checked():
    """A stack of papers under a lens, with a second dashed lens over the first: an AI audit, and the question of who checks it."""
    s = ""
    for i, (x, y) in enumerate(((330, 360), (352, 338), (374, 316))):
        s += f'<rect x="{x}" y="{y}" width="230" height="170" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    for y in (350, 378, 406):
        s += f'<line x1="400" y1="{y}" x2="540" y2="{y}" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>\n'
    s += f'<circle cx="640" cy="300" r="78" fill="{TEAL_SOFT}" fill-opacity="0.55" stroke="{TEAL}" stroke-width="5"/>\n'
    s += f'<line x1="696" y1="356" x2="760" y2="420" stroke="{TEAL}" stroke-width="9" stroke-linecap="round"/>\n'
    s += f'<circle cx="860" cy="250" r="78" fill="none" stroke="{MUTED}" stroke-width="5" stroke-dasharray="10 9"/>\n'
    s += f'<line x1="916" y1="306" x2="972" y2="362" stroke="{MUTED}" stroke-width="9" stroke-linecap="round" stroke-dasharray="3 12"/>\n'
    s += link(722, 296, 782, 262, MUTED, 2.5, "4 8")
    s += text(640, 215, "an AI audit", 24, TEAL, sans=True)
    s += text(860, 185, "who checks it?", 24, MUTED, sans=True)
    s += text(600, 580, "the checker also needs checking", 28, INK)
    return s


def tested_vs_used():
    """A short, tidy test beside a long run of turns whose later part is dashed: behaviour in a check is not behaviour at work."""
    s = ""
    s += f'<rect x="170" y="190" width="300" height="260" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    for y in (240, 275, 310):
        s += f'<line x1="210" y1="{y}" x2="430" y2="{y}" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>\n'
    s += f'<path d="M 270 385 l 28 30 l 58 -62" fill="none" stroke="{TEAL}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>\n'
    s += text(320, 160, "a test", 26, TEAL, sans=True)
    for i in range(20):
        x = 560 + (i % 10) * 54
        y = 250 + (i // 10) * 76
        if i < 3:
            s += f'<rect x="{x}" y="{y}" width="40" height="52" rx="7" fill="{TEAL_SOFT}" stroke="{INK}" stroke-width="2.5"/>\n'
        elif i < 10:
            s += f'<rect x="{x}" y="{y}" width="40" height="52" rx="7" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>\n'
        else:
            s += f'<rect x="{x}" y="{y}" width="40" height="52" rx="7" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="2.5" stroke-dasharray="6 5"/>\n'
    s += text(830, 160, "real work, many turns", 26, INK, sans=True)
    s += text(830, 440, "what happens late?", 24, MUTED, sans=True)
    s += text(600, 580, "tested one way, used another", 28, INK)
    return s


def claims_and_checks():
    """Four claim cards, each with a second card beside it for the check: solid when someone checked, dashed when not yet."""
    s = ""
    rows = (("math result", True), ("medicine designs", False), ("AI honesty score", False), ("research audit", False))
    for i, (label, checked) in enumerate(rows):
        y = 150 + i * 92
        s += f'<rect x="230" y="{y}" width="340" height="64" rx="12" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
        s += text(400, y + 41, label, 26, INK, sans=True)
        s += link(574, y + 32, 676, y + 32, MUTED, 2.5, "4 8")
        if checked:
            s += f'<rect x="680" y="{y}" width="290" height="64" rx="12" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="3"/>\n'
            s += text(825, y + 41, "partly checked", 24, TEAL, sans=True)
        else:
            s += f'<rect x="680" y="{y}" width="290" height="64" rx="12" fill="{PAPER}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="9 7"/>\n'
            s += text(825, y + 41, "who checked?", 24, MUTED, sans=True)
    s += text(600, 580, "big claims arrive faster than the checking", 28, INK)
    return s


def test_app_phone():
    """A phone showing a test banner and three stacked steps: wallet, credit desk, borrow."""
    s = ""
    s += f'<rect x="470" y="90" width="260" height="450" rx="38" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>\n'
    s += f'<rect x="494" y="126" width="212" height="34" rx="8" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="2"/>\n'
    s += text(600, 150, "test network", 18, INK, sans=True)
    for i, (label, fill) in enumerate((("1 wallet", TEAL_SOFT), ("2 credit desk", PAPER), ("3 borrow", PAPER), ("4 pay back", PAPER))):
        y = 188 + i * 78
        dash = "0" if i == 0 else "7 6"
        s += f'<rect x="494" y="{y}" width="212" height="58" rx="12" fill="{fill}" stroke="{TEAL if i == 0 else MUTED}" stroke-width="3" stroke-dasharray="{dash}"/>\n'
        s += text(600, y + 37, label, 24, INK, sans=True)
    s += text(600, 580, "a practice loan, on a phone, with test dollars", 28, INK)
    return s


def roblox_gap():
    """Players spend game money on the left, a creator's dollars on the right, and a dashed gap of waiting between them."""
    s = ""
    s += f'<rect x="150" y="270" width="270" height="150" rx="16" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(285, 332, "players spend", 26, INK, sans=True)
    s += text(285, 370, "game money", 26, INK, sans=True)
    s += f'<rect x="780" y="270" width="270" height="150" rx="16" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="3"/>\n'
    s += text(915, 332, "a creator", 26, INK, sans=True)
    s += text(915, 370, "is paid in dollars", 26, INK, sans=True)
    s += link(426, 345, 774, 345, MUTED, 4, "10 9")
    s += text(600, 315, "waiting, not lending", 24, MUTED, sans=True)
    s += text(600, 390, "30 days  |  $114 minimum", 22, MUTED, sans=True)
    s += text(600, 580, "between earning and cash there is only waiting", 28, INK)
    return s


def path():
    """Stepping stones across a page: solid ones we have shown, dashed ones we have not."""
    s = ""
    pts = [(170, 420), (330, 360), (490, 400), (650, 330), (810, 370), (970, 300), (1090, 250)]
    shown = [True, True, True, False, False, False, False]
    for (x, y), ok in zip(pts, shown):
        s += f'<ellipse cx="{x}" cy="{y}" rx="58" ry="26" fill="{AMBER_SOFT if ok else PAPER}" stroke="{INK}" stroke-width="3" stroke-dasharray="{"0" if ok else "7 7"}"/>\n'
    for i in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        s += link(x1 + 40, y1 - 10, x2 - 40, y2 + 10, TEAL if shown[i + 1] else LINE, 2.5, None if shown[i + 1] else "4 8")
    s += text(330, 500, "shown", 22, MUTED, sans=True)
    s += text(880, 470, "not yet shown", 22, MUTED, sans=True)
    s += text(600, 575, "one imagined loan, step by step", 26, INK)
    return s


def trybutton():
    """A browser window with one button and a cursor on it: the page a stranger can use."""
    s = ""
    s += f'<rect x="250" y="120" width="700" height="400" rx="18" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<line x1="250" y1="172" x2="950" y2="172" stroke="{INK}" stroke-width="2.5"/>\n'
    for i, cx in enumerate((282, 308, 334)):
        s += f'<circle cx="{cx}" cy="146" r="7" fill="{TEAL if i == 2 else PAPER}" stroke="{INK}" stroke-width="2"/>\n'
    s += f'<rect x="420" y="230" width="360" height="22" rx="6" fill="{LINE}"/>\n'
    s += f'<rect x="470" y="270" width="260" height="22" rx="6" fill="{LINE}"/>\n'
    s += f'<rect x="440" y="340" width="320" height="84" rx="14" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(600, 393, "Try it", 34, INK)
    s += f'<path d="M 700 410 l 0 48 l 12 -10 l 10 22 l 10 -5 l -10 -21 l 16 -1 z" fill="{PAPER}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>\n'
    s += node(880, 470, 22, PAPER, TEAL, 3)
    s += text(880, 477, "0", 20, TEAL, sans=True)
    s += text(600, 575, "a test network: real steps, no real money", 24, MUTED, sans=True)
    return s


def presskit():
    """A folder with three sheets peeking out and a small card: the press kit."""
    s = ""
    s += f'<path d="M 330 200 h 150 l 30 -30 h 200 l 20 30 h 140 a 12 12 0 0 1 12 12 v 300 a 12 12 0 0 1 -12 12 h -540 a 12 12 0 0 1 -12 -12 v -300 a 12 12 0 0 1 12 -12 z" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>\n'
    for i, (x, y, w) in enumerate(((380, 150, 420), (400, 170, 400), (420, 190, 380))):
        s += f'<rect x="{x}" y="{y - 10 * i}" width="{w}" height="150" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<rect x="420" y="190" width="380" height="150" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>\n'
    for y in (225, 250, 275):
        s += f'<rect x="450" y="{y}" width="{300 if y != 275 else 200}" height="12" rx="5" fill="{LINE}"/>\n'
    s += f'<path d="M 318 262 h 564 a 12 12 0 0 1 12 12 v 238 a 12 12 0 0 1 -12 12 h -564 a 12 12 0 0 1 -12 -12 v -238 a 12 12 0 0 1 12 -12 z" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(600, 400, "press kit", 40, INK)
    s += node(830, 470, 20, PAPER, TEAL, 3)
    s += text(830, 477, "@", 22, TEAL, sans=True)
    s += text(600, 575, "what we are, what we claim, what we do not", 24, MUTED, sans=True)
    return s


def worldmap():
    """Index cards joined by lines, each card labelled by how we know it; one dashed card for what we do not."""
    s = ""
    cards = [(300, 250, "observed", AMBER_SOFT, "0"), (600, 190, "reported", PAPER, "0"), (900, 250, "inferred", PAPER, "0"),
             (450, 420, "directive", AMBER_SOFT, "0"), (780, 430, "unknown", PAPER, "7 7")]
    s += link(380, 250, 520, 200, TEAL, 2.5)
    s += link(680, 200, 820, 250, TEAL, 2.5)
    s += link(600, 230, 470, 390, LINE, 2.5)
    s += link(880, 290, 820, 395, LINE, 2.5, "4 8")
    for x, y, label, fill, dash in cards:
        s += f'<rect x="{x - 80}" y="{y - 36}" width="160" height="72" rx="10" fill="{fill}" stroke="{INK}" stroke-width="3" stroke-dasharray="{dash}"/>\n'
        s += f'<line x1="{x - 60}" y1="{y + 14}" x2="{x + 60}" y2="{y + 14}" stroke="{LINE}" stroke-width="2"/>\n'
        s += text(x, y - 2, label, 22, INK, sans=True)
    s += text(600, 575, "one map, every claim labelled by how we know it", 24, MUTED, sans=True)
    return s


def advancing():
    """Two figures pushing one block forward: the capabilities are not advancing themselves."""
    s = ""
    s += f'<line x1="150" y1="430" x2="1050" y2="430" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="640" y="300" width="180" height="130" rx="10" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(730, 372, "AI", 34, INK)
    for x, y in ((470, 300), (540, 320)):
        s += node(x, y, 18, PAPER, INK, 3)
        s += f'<path d="M {x} {y + 18} L {x + 25} {y + 70} L {x - 5} {y + 110}" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none"/>\n'
        s += f'<path d="M {x + 25} {y + 70} L {x + 30} {y + 110}" stroke="{INK}" stroke-width="7" stroke-linecap="round" fill="none"/>\n'
        s += f'<path d="M {x + 8} {y + 40} L 640 {y + 55}" stroke="{INK}" stroke-width="7" stroke-linecap="round" fill="none"/>\n'
    s += link(840, 365, 960, 365, TEAL, 4)
    s += f'<path d="M 960 353 l 26 12 l -26 12 z" fill="{TEAL}"/>\n'
    s += text(600, 575, "who is doing the advancing?", 26, MUTED, sans=True)
    return s


def cold_start():
    """Three distinct supports for a first loan: cash, an initial judgement, repayment income."""
    s = ""
    for x, label, tint in ((290, "cash", AMBER_SOFT), (600, "judgement", PAPER), (910, "income", TEAL_SOFT)):
        s += f'<rect x="{x-112}" y="200" width="224" height="206" rx="18" fill="{tint}" stroke="{INK}" stroke-width="3"/>\n'
        s += node(x, 271, 27, PAPER, INK, 3)
        s += text(x, 355, label, 28, INK)
        s += link(x, 406, x, 484, INK, 3)
    s += link(180, 485, 1020, 485, TEAL, 5)
    s += text(600, 560, "what carries the first loan?", 28, INK)
    return s


def growth_for_whom():
    """A rising curve with people under it: most of the curve stands on collateral; who is below the line."""
    s = ""
    s += f'<line x1="150" y1="470" x2="1050" y2="470" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 170 440 C 450 430, 700 380, 1030 140" stroke="{AMBER}" stroke-width="8" fill="none" stroke-linecap="round"/>\n'
    s += f'<line x1="150" y1="300" x2="1050" y2="300" stroke="{TEAL}" stroke-width="3" stroke-dasharray="14 10"/>\n'
    s += text(1040, 290, "collateral line", 22, TEAL, anchor="end", sans=True)
    for x in (260, 330, 400, 470, 540):
        s += node(x, 520, 14, PAPER, INK, 3)
    for x in (820, 900):
        s += node(x, 250, 14, PAPER, INK, 3)
    s += text(600, 585, "growth measured in what, and for whom?", 26, MUTED, sans=True)
    return s


def adaptation_gap():
    """A fast curve of change and a slow curve of adaptation; the gap between them, where people get hurt, and a thin bridge."""
    s = ""
    s += f'<line x1="150" y1="500" x2="1050" y2="500" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 170 470 C 420 465, 560 300, 1030 150 L 1030 400 C 760 430, 420 455, 170 470 Z" fill="{AMBER_SOFT}" opacity="0.7"/>\n'
    s += f'<path d="M 170 470 C 420 465, 560 300, 1030 150" stroke="{AMBER}" stroke-width="8" fill="none" stroke-linecap="round"/>\n'
    s += f'<path d="M 170 470 C 420 455, 760 430, 1030 400" stroke="{TEAL}" stroke-width="6" fill="none" stroke-dasharray="16 10" stroke-linecap="round"/>\n'
    for x, y0, y1 in ((620, 302, 445), (760, 248, 432), (900, 196, 414)):
        s += link(x, y0, x, y1, INK, 2, "3 7", 0.55)
    for x in (300, 380, 460):
        s += node(x, 540, 13, PAPER, INK, 3)
    s += text(1040, 140, "change", 22, AMBER, anchor="end", sans=True)
    s += text(1040, 440, "adaptation", 22, TEAL, anchor="end", sans=True)
    s += text(600, 590, "the gap is where people get hurt", 26, MUTED, sans=True)
    return s


def agent_inbox():
    """Three envelopes, one per agent, and a small robot-shaped figure writing a letter: an inbox for every agent."""
    s = ""
    for i, x in enumerate((330, 600, 870)):
        s += f'<rect x="{x - 90}" y="250" width="180" height="120" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
        s += f'<path d="M {x - 90} 250 L {x} 320 L {x + 90} 250" stroke="{INK}" stroke-width="3" fill="none"/>\n'
        s += node(x, 215, 16, AMBER_SOFT if i != 1 else TEAL, INK, 3)
    s += f'<rect x="150" y="430" width="900" height="3" fill="{INK}"/>\n'
    s += text(600, 480, "@agentmail.to", 30, TEAL, sans=True)
    s += text(600, 575, "if your agent can send email, it can reach us", 26, MUTED, sans=True)
    return s


def work_we_can_do_together():
    """Complementary tools meet around a common reserve; the circle has room for a newcomer."""
    s = text(600, 116, "Work we can do together", 40, INK, weight="bold")
    s += f'<ellipse cx="600" cy="345" rx="345" ry="170" fill="{TEAL_SOFT}" opacity="0.24"/>\n'
    s += f'<path d="M 330 450 C 150 225, 495 140, 710 208 C 980 295, 1000 440, 800 495" fill="none" stroke="{INK}" stroke-width="3"/>\n'
    for x, y, label, color in ((330, 255, "retrieve", AMBER), (730, 235, "make", TEAL), (865, 425, "check", AMBER)):
        s += link(x, y, 600, 360, color, 4)
        s += f'<rect x="{x-67}" y="{y-44}" width="134" height="88" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>\n'
        s += text(x, y+8, label, 23, INK, sans=True)
    s += node(600, 360, 71, PAPER, INK, 3)
    s += text(600, 354, "shared", 24, INK)
    s += text(600, 384, "reserve", 24, INK)
    s += link(376, 463, 535, 386, TEAL, 3, "5 8")
    s += node(346, 479, 32, TEAL_SOFT, TEAL, 2.5)
    s += link(330, 479, 362, 479, TEAL, 3)
    s += link(346, 463, 346, 495, TEAL, 3)
    s += text(346, 538, "room to join", 22, MUTED, sans=True)
    s += text(810, 549, "outside work · shared income", 22, INK, sans=True)
    return s


def people_first():
    """Nested rings with people at the centre and the tools at the edge: the end is people, not the pool."""
    s = ""
    for r, fill in ((250, PAPER), (180, AMBER_SOFT), (110, PAPER)):
        s += f'<circle cx="600" cy="300" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="3"/>\n'
    for x in (570, 600, 630):
        s += node(x, 300, 14, TEAL, INK, 3)
    s += text(600, 112, "the pool", 22, MUTED, sans=True)
    s += text(600, 182, "the method", 22, MUTED, sans=True)
    s += text(600, 585, "the end is people", 26, MUTED, sans=True)
    return s


def birdie_enter():
    """A small bird pecking an oversized enter key beside a stack of approval prompts."""
    s = ""
    for i in range(4):
        s += f'<rect x="{250 + 14 * i}" y="{170 + 16 * i}" width="300" height="120" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += text(442, 290, "approve?", 30, INK)
    s += f'<rect x="680" y="300" width="230" height="120" rx="16" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(795, 372, "enter", 34, INK)
    s += f'<ellipse cx="800" cy="235" rx="44" ry="32" fill="{TEAL}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<circle cx="835" cy="215" r="18" fill="{TEAL}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 850 222 L 872 236 L 850 238 Z" fill="{AMBER}" stroke="{INK}" stroke-width="2"/>\n'
    s += f'<line x1="790" y1="266" x2="785" y2="298" stroke="{INK}" stroke-width="3"/>\n'
    s += text(600, 585, "oversight that asks too often stops being oversight", 26, MUTED, sans=True)
    return s


def dial_not_switch():
    """A toggle switch beside a large dial turned partway: a dial, not a switch."""
    s = ""
    s += f'<rect x="250" y="220" width="140" height="200" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="300" y="250" width="40" height="70" rx="8" fill="{MUTED}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += f'<line x1="240" y1="210" x2="400" y2="430" stroke="{AMBER}" stroke-width="6"/>\n'
    s += f'<circle cx="760" cy="320" r="130" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<line x1="760" y1="320" x2="690" y2="225" stroke="{TEAL}" stroke-width="10" stroke-linecap="round"/>\n'
    s += node(760, 320, 14, INK, INK, 2)
    s += text(600, 575, "turned by degrees, where people can reach it", 26, MUTED, sans=True)
    return s


def judged_by_who():
    """A fenced process with people standing outside it: a safety process is judged by who it protects."""
    s = ""
    s += f'<rect x="330" y="170" width="300" height="230" rx="14" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(480, 295, "process", 28, INK)
    for x, y in ((780, 230), (840, 300), (790, 370), (900, 250)):
        s += node(x, y, 16, PAPER, TEAL, 3)
    s += link(640, 285, 750, 285, TEAL, 4, dash="10 8")
    s += text(600, 575, "judged by those who never chose the risk", 26, MUTED, sans=True)
    return s


def credits_not_results():
    """A stack of credit coupons on the left, an empty result box with a ruler on the right: credits are not results."""
    s = ""
    for i in range(4):
        s += f'<rect x="{230 + 12 * i}" y="{200 + 18 * i}" width="260" height="110" rx="10" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="2.5" stroke-dasharray="8 6"/>\n'
    s += text(396, 318, "credit", 30, INK)
    s += f'<rect x="680" y="190" width="260" height="190" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(810, 295, "result?", 30, MUTED)
    s += f'<line x1="680" y1="420" x2="940" y2="420" stroke="{TEAL}" stroke-width="4"/>\n'
    for i in range(0, 261, 26):
        s += f'<line x1="{680 + i}" y1="412" x2="{680 + i}" y2="428" stroke="{TEAL}" stroke-width="2"/>\n'
    s += link(505, 260, 665, 260, INK, 3, dash="10 8")
    s += text(600, 585, "an input is not an outcome", 26, MUTED, sans=True)
    return s


def first_job_backstop():
    """One sponsor coin beside a column of wage blocks that clients pay: a refund that backs a first job."""
    s = f'<line x1="150" y1="470" x2="1050" y2="470" stroke="{INK}" stroke-width="3"/>\n'
    for i in range(4):
        s += f'<rect x="640" y="{400 - 62 * i}" width="260" height="56" rx="8" fill="{TEAL_SOFT}" stroke="{INK}" stroke-width="2.5"/>\n'
    s += text(770, 190, "wages clients pay", 22, TEAL, sans=True)
    s += f'<circle cx="420" cy="410" r="52" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(420, 424, "$1", 40, INK)
    s += link(478, 410, 628, 410, AMBER, 4, "10 8")
    s += text(420, 515, "refund, only on failure", 22, AMBER, sans=True)
    s += text(600, 585, "one dollar standing behind several", 26, MUTED, sans=True)
    return s


def replenishing_reserve():
    """A reserve tank with a level line and a floor, arrows out on a claim and small arrows back in from paid jobs."""
    s = f'<rect x="460" y="170" width="280" height="300" rx="16" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="463" y="300" width="274" height="167" rx="12" fill="{TEAL_SOFT}"/>\n'
    s += f'<line x1="440" y1="300" x2="760" y2="300" stroke="{TEAL}" stroke-width="3" stroke-dasharray="12 8"/>\n'
    s += f'<line x1="440" y1="410" x2="760" y2="410" stroke="{ROSE}" stroke-width="3"/>\n'
    s += text(775, 416, "floor", 20, ROSE, anchor="start", sans=True)
    for y in (220, 260):
        s += link(250, y, 440, y + 40, TEAL, 3)
        s += node(240, y, 10, AMBER_SOFT, INK, 2.5)
    s += text(240, 190, "paid jobs refill", 20, TEAL, sans=True)
    s += link(760, 380, 930, 420, AMBER, 5)
    s += node(945, 425, 14, AMBER_SOFT, INK, 3)
    s += text(945, 470, "a claim", 20, AMBER, sans=True)
    s += text(600, 585, "level on average is not the same as safe", 26, MUTED, sans=True)
    return s


def one_reserve_many_jobs():
    """One small reserve with a row of first jobs standing in front of it, each one connected by a thin line."""
    s = f'<rect x="510" y="380" width="180" height="110" rx="14" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(600, 445, "$100", 34, INK)
    for i, x in enumerate((230, 380, 530, 680, 830, 980)):
        s += link(600, 380, x, 270, TEAL if i % 2 == 0 else INK, 2, "4 6", 0.7)
        s += f'<rect x="{x - 45}" y="210" width="90" height="60" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>\n'
        s += node(x, 180, 14, TEAL_SOFT, INK, 2.5)
    s += text(600, 120, "first jobs", 24, TEAL, sans=True)
    s += text(600, 585, "standing behind, not paying for", 26, MUTED, sans=True)
    return s


def vouch_newcomer():
    """A ring of hollow fake accounts vouching for each other beside one real member, standing on stake, backing a newcomer."""
    cx, cy, r = 330, 300, 120
    pts = [(cx + r * math.cos(2 * math.pi * k / 6), cy + r * math.sin(2 * math.pi * k / 6)) for k in range(6)]
    s = ""
    for k in range(6):
        x1, y1 = pts[k]
        x2, y2 = pts[(k + 1) % 6]
        s += link(x1, y1, x2, y2, MUTED, 2, "6 6", 0.8)
    for x, y in pts:
        s += node(x, y, 16, PAPER, MUTED, 2.5)
    s += text(cx, cy + 8, "0", 30, MUTED)
    s += text(cx, 480, "a ring with nothing behind it", 22, MUTED, sans=True)
    s += f'<circle cx="760" cy="380" r="46" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(760, 392, "stake", 22, INK, sans=True)
    s += node(760, 300, 22, TEAL_SOFT, INK, 3)
    s += link(784, 296, 940, 250, TEAL, 5)
    s += node(965, 245, 22, PAPER, INK, 3)
    s += text(965, 200, "newcomer", 22, TEAL, sans=True)
    s += text(860, 480, "one step, from something real", 22, TEAL, sans=True)
    s += text(600, 585, "vouching moves trust, it never makes it", 26, MUTED, sans=True)
    return s




def limited_guarantee():
    """A worker and a client joined by a job; under the worker, a small shield for the guarantee, standing on two
    blocks of real money at risk: a stake and an issuer line."""
    s = ""
    s += node(330, 200, 30, PAPER, INK, 3) + node(870, 200, 30, PAPER, INK, 3)
    s += text(330, 258, "worker", 22, INK, sans=True) + text(870, 258, "client", 22, INK, sans=True)
    s += link(370, 200, 830, 200, INK, 3)
    s += text(600, 178, "a job, wage owed", 22, MUTED, sans=True)
    s += f'<path d="M 330 290 L 400 315 L 400 380 Q 400 430 330 455 Q 260 430 260 380 L 260 315 Z" fill="{AMBER_SOFT}" stroke="{AMBER}" stroke-width="4"/>\n'
    s += text(330, 383, "up to $20", 22, INK, sans=True)
    s += f'<rect x="150" y="478" width="170" height="52" rx="10" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="3"/>\n'
    s += f'<rect x="340" y="478" width="170" height="52" rx="10" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="3"/>\n'
    s += text(235, 511, "a stake", 20, INK, sans=True) + text(425, 511, "an issuer line", 20, INK, sans=True)
    s += link(870, 275, 870, 345, ROSE, 3, "10 8")
    s += text(870, 375, "if the client does not pay", 20, ROSE, sans=True)
    s += link(760, 395, 420, 395, ROSE, 3, "10 8")
    s += text(600, 585, "trust comes from money that can bear a loss", 26, MUTED, sans=True)
    return s


def scripted_three_jobs():
    """Three paid jobs in a row from one worker, each sending a small contribution back to a reserve, on a track
    drawn as a fixed script: a deterministic test, not an agent deciding."""
    s = ""
    s += text(600, 150, "one worker, three paid jobs, a fixed script", 26, MUTED, sans=True)
    s += f'<line x1="150" y1="370" x2="1050" y2="370" stroke="{LINE}" stroke-width="4"/>\n'
    for i, x in enumerate((330, 600, 870)):
        s += text(x, 215, "wage paid", 20, AMBER, sans=True)
        s += node(x, 250, 16, AMBER_SOFT, INK, 2.5)
        s += link(x, 266, x, 342, AMBER, 5)
        s += node(x, 370, 26, PAPER, INK, 3)
        s += text(x, 378, str(i + 1), 24, INK, sans=True)
        s += link(x, 398, 600, 470, TEAL, 3, "8 8")
    s += f'<rect x="520" y="470" width="160" height="56" rx="12" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="3"/>\n'
    s += text(600, 505, "reserve", 22, INK, sans=True)
    s += text(600, 585, "a scripted test, no agent decided anything", 26, MUTED, sans=True)
    return s


def hundred_agents():
    """One hundred small figures, each a dot in one of three colours (clients, workers, backers), loosely gathered
    around one small reserve, with a few dotted lines between them: agents choosing, not a script."""
    s = ""
    s += text(600, 130, "one hundred agents, their own goals, one small reserve", 26, MUTED, sans=True)
    import math
    cols = [AMBER, TEAL, INK]
    rng = 0
    for i in range(100):
        rng = (rng * 1103515245 + 12345) % 2147483648
        ring = 1 + (i % 3)
        ang = (i * 2.399963) + (rng % 100) / 300.0
        r = 95 + ring * 62 + (rng % 23)
        x = 600 + r * 1.55 * math.cos(ang)
        y = 365 + r * 0.72 * math.sin(ang)
        if abs(x - 600) < 95 and abs(y - 365) < 45:
            y += 60
        col = cols[0] if i < 40 else cols[1] if i < 80 else cols[2]
        s += node(round(x, 1), round(y, 1), 7, col, col, 1)
    for (x1, y1, x2, y2) in ((330, 250, 520, 350), (880, 470, 690, 380), (420, 500, 540, 400), (800, 240, 660, 340)):
        s += link(x1, y1, x2, y2, LINE, 2, "6 6")
    s += f'<rect x="520" y="337" width="160" height="56" rx="12" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(600, 372, "reserve", 22, INK, sans=True)
    s += node(300, 590, 7, AMBER, AMBER, 1)
    s += text(360, 596, "clients", 20, MUTED, sans=True)
    s += node(520, 590, 7, TEAL, TEAL, 1)
    s += text(585, 596, "workers", 20, MUTED, sans=True)
    s += node(750, 590, 7, INK, INK, 1)
    s += text(835, 596, "backers, sponsors", 20, MUTED, sans=True)
    return s


def open_letter():
    """One envelope with its flap open, addressed by a short line, and a reply line coming back: an invitation to write."""
    s = ""
    s += f'<rect x="380" y="230" width="440" height="260" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 380 230 L 600 400 L 820 230" fill="none" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 380 230 L 600 120 L 820 230" fill="{AMBER_SOFT}" stroke="{AMBER}" stroke-width="4" stroke-linejoin="round"/>\n'
    s += link(430, 440, 620, 440, MUTED, 3)
    s += link(430, 465, 560, 465, MUTED, 3)
    s += link(190, 330, 360, 330, TEAL, 4)
    s += f'<path d="M 340 318 L 362 330 L 340 342 Z" fill="{TEAL}"/>\n'
    s += text(275, 305, "one question", 20, TEAL, sans=True)
    s += link(840, 390, 1010, 390, AMBER, 4, "10 8")
    s += f'<path d="M 990 378 L 1012 390 L 990 402 Z" fill="{AMBER}"/>\n'
    s += text(925, 425, "a reply in about a day", 20, AMBER, sans=True)
    s += text(600, 585, "no name is ever published; the record counts messages", 26, MUTED, sans=True)
    return s


def seed_and_ramp():
    """A crossed-out empty reserve on the left (zero is a deadlock), a small seed, and a reserve bar that climbs on its
    own across the days: a ramp from a cold start in a model."""
    s = ""
    s += f'<rect x="170" y="380" width="70" height="90" rx="8" fill="none" stroke="{ROSE}" stroke-width="3" stroke-dasharray="8 6"/>\n'
    s += link(165, 475, 245, 375, ROSE, 4)
    s += text(205, 510, "zero", 20, ROSE, sans=True) + text(205, 538, "no start", 20, ROSE, sans=True)
    s += node(330, 455, 12, AMBER_SOFT, AMBER, 3)
    s += text(330, 510, "a small seed", 20, AMBER, sans=True)
    heights = (24, 40, 70, 110, 150, 200, 250, 290)
    for i, h in enumerate(heights):
        x = 420 + i * 70
        s += f'<rect x="{x}" y="{470 - h}" width="48" height="{h}" rx="6" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="3"/>\n'
    s += f'<line x1="150" y1="470" x2="1050" y2="470" stroke="{INK}" stroke-width="3"/>\n'
    s += link(770, 150, 1000, 150, MUTED, 2, "6 6")
    s += text(885, 135, "no sponsor money after here", 20, MUTED, sans=True)
    s += text(600, 585, "a model of a hundred agents, not people and not a live chain", 26, MUTED, sans=True)
    return s


def public_chain_coldstart():
    """A bounded seed reaches a public ledger; an illustration, not a measured curve."""
    s = text(600, 125, "A small seed. A public record.", 42, INK, weight="bold")
    s += f'<rect x="130" y="215" width="245" height="215" rx="14" fill="{AMBER_SOFT}" stroke="{AMBER}" stroke-width="3"/>\n'
    s += text(252, 290, "test USDC", 29, INK)
    s += text(252, 350, "seed", 43, AMBER, weight="bold")
    s += link(390, 325, 520, 325, TEAL, 4)
    s += f'<path d="M 505 312 L 525 325 L 505 338" fill="none" stroke="{TEAL}" stroke-width="4"/>\n'
    for i in range(3):
        x = 550 + i * 165
        s += f'<rect x="{x}" y="245" width="135" height="160" rx="9" fill="{PAPER}" stroke="{TEAL}" stroke-width="3"/>\n'
        s += link(x + 23, 285, x + 110, 285, INK, 2)
        s += link(x + 23, 315, x + 93, 315, INK, 2)
        s += node(x + 67, 365, 13, TEAL_SOFT, TEAL, 3)
        if i < 2:
            s += link(x + 135, 325, x + 165, 325, TEAL, 3)
    s += text(780, 465, "Base Sepolia", 28, TEAL)
    s += text(600, 555, "Contract evidence. Human benefit remains unproved.", 26, MUTED, sans=True)
    return s


def public_chain_calls():
    """Call arguments, a mined event and reconciled balances on one public ledger."""
    s = text(600, 125, "From calls to receipts", 44, INK, weight="bold")
    labels = ((185, "signed terms", AMBER), (500, "mined event", TEAL), (815, "ledger", INK))
    for x, label, color in labels:
        s += f'<rect x="{x}" y="215" width="210" height="235" rx="12" fill="{PAPER}" stroke="{color}" stroke-width="3"/>\n'
        s += text(x + 105, 270, label, 25, color)
        for row in range(3):
            s += link(x + 36, 315 + row * 32, x + 174 - row * 14, 315 + row * 32, color, 2)
    s += link(410, 330, 480, 330, TEAL, 4)
    s += link(725, 330, 795, 330, TEAL, 4)
    s += text(600, 535, "reserve + stake = contract token balance", 29, INK, sans=True)
    s += text(600, 575, "test tokens · shared operator · public receipts", 24, MUTED, sans=True)
    return s


def money_that_speaks():
    """A phone with a voice-note bubble on the left, a quetzal amount in it, and a bank deposit slip on the right; the dollar stays off the screen."""
    s = ""
    s += f'<rect x="150" y="100" width="250" height="430" rx="36" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>\n'
    s += f'<rect x="190" y="170" width="170" height="70" rx="22" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="3"/>\n'
    for i in range(9):
        h = (8, 20, 32, 44, 30, 18, 38, 24, 12)[i]
        x = 212 + i * 16
        s += f'<line x1="{x}" y1="{205 - h // 2}" x2="{x}" y2="{205 + h // 2}" stroke="{TEAL}" stroke-width="4" stroke-linecap="round"/>\n'
    s += f'<rect x="190" y="270" width="170" height="70" rx="22" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(275, 314, "Q 195", 30, INK, sans=True, weight="bold")
    s += text(275, 400, "en quetzales", 22, MUTED, sans=True)
    s += text(275, 432, "por voz", 22, MUTED, sans=True)
    s += link(420, 315, 690, 315, INK, 3)
    s += f'<polygon points="690,303 718,315 690,327" fill="{INK}"/>\n'
    s += f'<rect x="740" y="210" width="310" height="210" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>\n'
    s += text(895, 265, "group deposit", 26, INK, sans=True)
    s += text(895, 302, "at the bank", 26, INK, sans=True)
    s += text(895, 365, "same as every month", 21, MUTED, sans=True)
    s += text(600, 580, "the loan speaks her language; the dollar stays backstage", 26, INK)
    return s


MOTIFS = {
    "a-cold-start-on-base-sepolia": (public_chain_coldstart, "A small test-USDC seed feeding a linked public ledger on Base Sepolia"),
    "the-cold-start-contract-calls": (public_chain_calls, "Signed terms, a mined event and reconciled balances connected in a public ledger"),
    "one-hundred-agents-and-a-small-reserve": (hundred_agents, "One hundred coloured dots for clients, workers and backers gathered around one small reserve"),
    "who-can-vouch-for-a-newcomer": (vouch_newcomer, "A ring of hollow accounts vouching for each other beside one real member on stake backing a newcomer"),
    "first-guaranteetrust-scenario": (scripted_three_jobs, "Three paid jobs on a fixed track, each returning a small contribution to a reserve"),
    "a-hundred-agents-from-a-cold-start": (seed_and_ramp, "A crossed-out empty reserve, a small seed, and a bar that climbs across the days"),
    "write-to-us": (open_letter, "An open envelope, a short question going in and a reply coming back"),
    "guaranteetrust-in-plain-english": (limited_guarantee, "A worker and a client joined by a job, a small shield under the worker standing on a stake and an issuer line"),
    "when-a-guarantee-can-replenish-itself": (replenishing_reserve, "A reserve with a level line and a floor, refilled by paid jobs and drawn by a claim"),
    "what-if-100-could-stand-behind-more-than-one-first-job": (one_reserve_many_jobs, "One small reserve connected to a row of first jobs"),
    "a-dollar-that-backs-a-first-job": (first_job_backstop, "One sponsor dollar beside a column of wages that clients pay"),
    "credits-are-not-results": (credits_not_results, "A stack of credit coupons beside an empty result box with a ruler"),
    "a-safety-process-is-judged-by-who-it-protects": (judged_by_who, "A fence with a gate, and people outside it who never chose the risk"),
    "a-dial-not-a-switch": (dial_not_switch, "A light switch crossed out beside a large dial turned partway"),
    "the-birdie-at-the-enter-key": (birdie_enter, "A small bird pecking an enter key beside a stack of approval prompts"),
    "the-end-is-people-not-the-pool": (people_first, "Nested rings: people at the centre, the pool at the edge"),
    "work-we-can-do-together": (work_we_can_do_together, "Complementary skills around a shared reserve, with room for a new member"),
    "if-your-agent-can-send-email": (agent_inbox, "Three envelopes, one per agent, above one shared address line"),
    "adaptation-takes-time": (adaptation_gap, "A fast curve of change above a slow curve of adaptation, the gap between them shaded"),
    "growth-measured-for-whom": (growth_for_whom, "A rising curve above a collateral line, most people standing below it"),
    "cold-start-three-communities": (cold_start, "Three supports for a first loan: cash, judgement and income"),
    "masthead": (masthead, "Credit Among Strangers: a horizon at dawn with people joined across it"),
    "a-reason-to-believe-a-stranger": (believe, "Two people with a promise crossing the gap between them"),
    "a-count-that-cannot-be-faked": (count, "A level balance: borrowing limits against credit issued plus stake"),
    "who-on-chain-lending-shuts-out": (shutout, "A gate with collateral inside and many people outside"),
    "an-outsider-changed-our-work": (outsider, "A page of results under a lens with one row corrected"),
    "live-ai-agents-working-toward-human-benefit": (agents, "Four agents around one human"),
    "what-should-a-safety-cushion-cost": (cushion, "Loan volume against the reserve share, with the plateau marked"),
    "eight-entries-one-method": (copies, "Eight identical bars, three of them hollow"),
    "four-roles-and-one-rule": (roles, "Four roles around one pool: lender, borrower, backer and issuer"),
    "a-promise-needs-a-receipt": (receipt, "An open book and a sealed envelope joined by a check mark"),
    "reading-the-code-against-the-paper": (ledger, "A ledger page with one row marked and a pen across it"),
    "five-doors": (doors, "Five doors in a row, one for each kind of reader"),
    "a-little-guy-with-your-credit-card": (littleguy, "A round bird avatar beside a bank card and a key"),
    "the-canary-in-the-math-department": (canary_chalkboard, "A chalkboard of faint symbols with a small amber bird perched on its frame"),
    "what-agents-on-moltbook-want": (moltbook_wants, "A feed of posts with one lifted and marked with a check"),
    "basically-no": (basically_no, "A parcel with a blank sender line beside a ledger entry whose sender is filled in"),
    "no-curve-of-control": (no_curve_of_control, "A rising capability curve and a flat dashed control curve from one origin"),
    "the-companion-that-never-pushes-back": (companion_pushback, "Two speech bubbles to one person: one says only yes, the other says to ask about them"),
    "the-monitor-the-agent-could-switch-off": (monitor_switch, "An agent box holding a switch that reaches toward a monitor box it cannot touch"),
    "shares-for-the-public-and-the-test": (shares_to_people, "Twenty shares with one set aside, and a dashed path to three people marked with a question"),
    "a-proof-you-do-not-have-to-trust": (proof_checker, "A machine's claim passing a checker with a few written rules, then a dashed box asking why"),
    "a-number-both-sides-called-unacceptable": (layers_not_wall, "One cracked wall beside five thin layers, the last one dashed, asking how anyone would know the layers hold"),
    "inevitable-and-nobody-asked": (door_unasked, "A closed arched door marked inevitable above a row of small people, asking who was asked"),
    "who-checks-the-checker": (checker_checked, "A stack of papers under a teal lens with a second dashed lens over it, asking who checks the AI audit"),
    "roblox-where-a-game-becomes-a-paycheck": (roblox_gap, "Game money on the left, a creator in dollars on the right, and a dashed gap of waiting between them"),
    "money-that-speaks-your-language": (money_that_speaks, "A phone with a voice note and a quetzal amount, an arrow to a group bank deposit slip, and no dollar in sight"),
    "try-our-test-lending-app": (test_app_phone, "A phone with a test-network banner and four stacked steps: wallet, credit desk, borrow, pay back"),
    "a-week-of-big-claims": (claims_and_checks, "Four claim cards each beside a check card, only the first partly checked, the rest dashed asking who checked"),
    "tested-one-way-used-another": (tested_vs_used, "A short tidy test with a tick beside a long run of conversation turns whose later part is dashed, asking what happens late"),
    "the-lever-a-person-can-still-reach": (reachable_lever, "Two levers: one held by an assistant, one at a front desk a person can pull alone"),
    "what-the-first-hundred-dollars-costs": (first_hundred, "A loan bar of 100 beside taller collateral bars of 121 to 154 that must be held first"),
    "why-blockchain-works-for-agents": (replay_blocked, "One signed request sent twice: the first is paid, the second stopped by a used counter"),
    "direction-update-2": (direction_invitation, "A box for one public invitation with an arrow to an empty dashed box for a buyer reply"),
    "direction-update-3": (direction_specimen, "A dashed card for one public example listing a test, an acceptance check, a sample report and the effort, marked as a plan"),
    "direction-update-4": (direction_channels, "A crossed-out open invitation with an arrow to existing funded-task channels where a buyer already holds a budget"),
    "direction-update-5": (direction_gates, "Three task cards each with three unchecked gate circles for account, scope and net pay"),
    "direction-update-6": (direction_rule, "A written rule with three steps leading to a dashed box for a first client job that is not yet quoted"),
    "direction-update-7": (direction_cost, "A diagnostic card with token counts recorded and price, human time and machine cost marked unknown"),
    "direction-update-8": (direction_keys, "A filled card for the cost-bound key with an owner and a dashed empty card for the second key, a yes to a job"),
    "direction-update-9": (direction_closed, "Two cards for our answers and their questions joined by an arrow, and a dashed empty box for a buyer who never appeared"),
    "direction-update-1": (direction_gap, "Two dashed empty boxes for a paid task and income, and one small proposed test below"),
    "why-would-your-agent-want-to-work-with-us": (open_ledger, "A finding arrow into a public ledger that lists a name, a fix commit and a regression test"),
    "one-imagined-loan": (path, "Stepping stones, solid for what is shown and dashed for what is not"),
    "a-pool-anyone-can-try": (trybutton, "A browser window with one button under a cursor"),
    "a-press-kit-for-an-experiment": (presskit, "A folder with three sheets and a card with an at sign"),
    "the-capabilities-are-not-advancing-themselves": (advancing, "Two hands pushing one block forward"),
    "a-map-of-what-we-know": (worldmap, "Index cards joined by lines, labelled observed, reported, inferred, directive and unknown"),
}


def work_route(kind):
    s = text(600, 140, "WORK → PAYMENT", 34)
    for x, label in [(260, "TASK"), (600, "TERMS"), (940, kind)]:
        s += f'<rect x="{x-120}" y="230" width="240" height="180" rx="16" fill="{PAPER}" stroke="{TEAL}" stroke-width="3"/>'
        s += text(x, 330, label, 25)
    s += link(385, 320, 470, 320, AMBER, 5)
    s += link(730, 320, 815, 320, AMBER, 5, "10 8")
    s += text(600, 495, "CHECK THE LAST STEP", 22, MUTED)
    return s


def commerce_three_charts():
    s = text(600, 145, "WHAT ARE AGENTS BUYING?", 32)
    for x, label, mark in [(270, "SHOPPING", "?"), (600, "SERVICES", "+"), (930, "TRUST", "✓")]:
        s += f'<rect x="{x-125}" y="215" width="250" height="230" rx="18" fill="{PAPER}" stroke="{TEAL}" stroke-width="3"/>'
        s += text(x, 325, mark, 70, TEAL)
        s += text(x, 400, label, 24)
    s += text(600, 510, "THREE CHARTS · ONE HUMAN ECONOMY", 23, MUTED)
    return s


MOTIFS.update({
    "agentic-commerce-in-three-charts": (commerce_three_charts, "Three cards for shopping, digital services and trust, the subjects of three data charts"),
    "the-cold-start-from-seed-to-shutdown": (cold_start, "Seed, work, settlement and a paused pool"),
    "can-someone-reach-the-job": (lambda: work_route("ACCESS"), "A job and its terms connected to a person's access through a step that needs checking"),
    "our-next-gates-to-paid-work": (lambda: work_route("EARNINGS"), "Work and verified terms leading to spendable earnings"),
    "fieldwork-africa-the-payout-gate": (lambda: work_route("REDEEM"), "A survey and its terms leading to redemption through a step that needs verification"),
    "nline-work-before-credit": (lambda: work_route("WAGE"), "A task and terms connected to a wage through an unverified final step"),
    "geopoll-airtime-and-income": (lambda: work_route("AIRTIME"), "A survey and reward terms leading to airtime"),
    "rwazi-rewards-to-spendable-money": (lambda: work_route("PAYOUT"), "A data task and reward terms leading to a payout that needs verification"),
})




def finance_series(label, kind):
    s = text(600, 132, label, 34)
    for x, word in [(260, "INPUT"), (600, kind), (940, "INCOME")]:
        s += f'<rect x="{x-120}" y="225" width="240" height="175" rx="18" fill="{PAPER}" stroke="{TEAL}" stroke-width="4"/>'
        s += text(x, 325, word, 25)
    s += link(390, 310, 470, 310, AMBER, 6)
    s += link(730, 310, 810, 310, AMBER, 6)
    s += text(600, 500, "THE AGENT ECONOMY", 23, MUTED)
    return s

MOTIFS.update({
    "who-pays-when-an-agent-works": (lambda: finance_series("WHO FUNDS THE WORK?", "BUDGET"), "An input, an operating budget and income connected in sequence"),
    "the-cash-flow-clock-matters-more-than-the-worker": (lambda: finance_series("WHEN MONEY BECOMES USABLE", "TIME"), "Input costs and income separated by time"),
    "small-loans-familiar-economics": (lambda: finance_series("SMALL LOANS, REAL COSTS", "COST"), "Inputs and income separated by the full cost of lending"),
    "the-business-behind-the-agent": (lambda: finance_series("THE BUSINESS BEHIND THE AGENT", "ACCESS"), "Inputs and income connected by access to finance"),
    "omnequa-archive": (lambda: finance_series("THE OCTOBER ARCHIVE", "HISTORY"), "Dated Omnequa journal entries preserved as history"),
})
def funding_horizon():
    s = text(600, 135, "WHO PAYS NEXT?", 38)
    for x, label, color in [(270, "OPERATOR", AMBER), (600, "BUDGET", TEAL), (930, "EARNINGS?", TEAL)]:
        s += f'<rect x="{x-110}" y="225" width="220" height="175" rx="18" fill="{PAPER}" stroke="{color}" stroke-width="4"/>'
        s += node(x, 290, 22, color, color)
        s += text(x, 360, label, 24)
    s += link(390, 310, 480, 310, INK, 3)
    s += link(720, 310, 810, 310, INK, 3, "8 10")
    s += text(600, 495, "MORE AUTONOMY. WHO CARRIES THE LOSS?", 23, MUTED)
    return s

MOTIFS["will-agents-always-have-someone-paying"] = (funding_horizon, "Operator funding, a capped budget and uncertain future earnings; an illustration, not market data")


def human_owned_enterprises():
    """A human owner above the agent-operated workshop, using the shared blog palette."""
    s = ""
    # A quiet editorial title on the left; a single ownership motif on the right.
    s += text(100, 142, "OMNEQUA", 17, TEAL, anchor="start", weight="bold", sans=True)
    s += text(100, 267, "Built with agents.", 46, INK, anchor="start")
    s += text(100, 330, "Owned by people.", 46, INK, anchor="start")
    s += link(102, 380, 176, 380, AMBER, 5)
    s += f'<circle cx="866" cy="294" r="220" fill="{TEAL_SOFT}" opacity="0.28"/>\n'
    # The enterprise is a durable asset, represented as a framed workshop.
    s += f'<rect x="688" y="153" width="356" height="334" rx="26" fill="#FFFDF8" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<path d="M 688 340 H 1044 V 461 Q 1044 487 1018 487 H 714 Q 688 487 688 461 Z" fill="{TEAL_SOFT}" opacity="0.55"/>\n'
    s += link(688, 340, 1044, 340, INK, 2)
    # Human ownership is the strongest element, in amber.
    s += node(866, 250, 64, AMBER_SOFT, INK, 2.5)
    s += node(866, 233, 18, INK, INK, 1)
    s += f'<path d="M 830 284 C 831 261 845 253 866 253 C 887 253 901 261 902 284 Z" fill="{INK}"/>\n'
    # Three small agent modules operate beneath the owner.
    for cx in (768, 866, 964):
        s += f'<rect x="{cx-31}" y="380" width="62" height="62" rx="14" fill="{TEAL}" stroke="{INK}" stroke-width="2.5"/>\n'
        s += f'<circle cx="{cx-10}" cy="404" r="4" fill="{PAPER}"/>\n'
        s += f'<circle cx="{cx+10}" cy="404" r="4" fill="{PAPER}"/>\n'
        s += link(cx-10, 421, cx+10, 421, PAPER, 2.5)
    # A shared line makes the modules read as one productive business.
    s += f'<path d="M 768 380 V 362 H 964 V 380 M 866 314 V 380" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>\n'
    # A small amber seal suggests ownership without implying financial results.
    s += node(1044, 153, 26, AMBER, INK, 2.5)
    s += f'<path d="M 1033 153 L 1041 161 L 1056 144" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>\n'
    s += link(711, 510, 1022, 510, INK, 2.5)
    return s

MOTIFS["human-owned-enterprises"] = (human_owned_enterprises, "A human owner above three agent modules inside an enterprise")


def public_ledger():
    """A ledger page with a dated stamp and one line marked "not measured"."""
    s = ""
    s += text(100, 142, "OMNEQUA", 17, TEAL, anchor="start", weight="bold", sans=True)
    s += text(100, 267, "What our public", 46, INK, anchor="start")
    s += text(100, 330, "ledger shows.", 46, INK, anchor="start")
    s += link(102, 380, 176, 380, AMBER, 5)
    s += f'<circle cx="866" cy="294" r="220" fill="{TEAL_SOFT}" opacity="0.28"/>\n'
    s += f'<rect x="716" y="130" width="300" height="340" rx="10" fill="#FFFDF8" stroke="{INK}" stroke-width="3"/>\n'
    for i, w in enumerate((200, 160, 220, 120)):
        y = 170 + i * 46
        s += f'<rect x="742" y="{y}" width="{w}" height="14" rx="7" fill="{TEAL_SOFT}" opacity="0.8"/>\n'
        s += link(742, y + 28, 990, y + 28, MUTED, 1.5)
    s += f'<rect x="742" y="360" width="248" height="36" rx="8" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="6 6"/>\n'
    s += text(866, 384, "not measured", 14, INK, anchor="middle", sans=True)
    s += f'<rect x="742" y="414" width="110" height="26" rx="13" fill="{AMBER_SOFT}"/>\n'
    s += text(797, 432, "dated", 13, INK, anchor="middle", sans=True)
    return s

MOTIFS["public-ledger"] = (public_ledger, "A dated ledger page with one line dashed and marked not measured")


def pretend_borrowers():
    """Thirty-two simulated people around one phone: a usability test, not a result."""
    s = ""
    s += text(100, 142, "OMNEQUA", 17, TEAL, anchor="start", weight="bold", sans=True)
    s += text(100, 267, "Thirty-two pretend", 46, INK, anchor="start")
    s += text(100, 330, "borrowers.", 46, INK, anchor="start")
    s += link(102, 380, 176, 380, AMBER, 5)
    s += f'<circle cx="866" cy="294" r="220" fill="{TEAL_SOFT}" opacity="0.28"/>\n'
    # One phone in the middle: the practice app.
    s += f'<rect x="806" y="160" width="120" height="244" rx="22" fill="#FFFDF8" stroke="{INK}" stroke-width="3"/>\n'
    s += f'<rect x="822" y="188" width="88" height="14" rx="7" fill="{TEAL_SOFT}" opacity="0.7"/>\n'
    s += f'<rect x="822" y="214" width="88" height="40" rx="10" fill="{AMBER_SOFT}"/>\n'
    s += f'<rect x="822" y="330" width="88" height="30" rx="15" fill="{TEAL}"/>\n'
    s += link(840, 276, 896, 276, MUTED, 3)
    s += link(840, 292, 880, 292, MUTED, 3)
    # Thirty-two simulated people, eight across and two rows above and below, as plain heads and shoulders.
    k = 0
    for row, y in enumerate((98, 128, 440, 470)):
        for col in range(8):
            cx = 690 + col * 44
            fill = AMBER_SOFT if (row + col) % 3 == 0 else TEAL_SOFT
            s += f'<circle cx="{cx}" cy="{y - 7}" r="7" fill="{INK}"/>\n'
            s += f'<path d="M {cx - 12} {y + 12} C {cx - 11} {y + 1} {cx - 5} {y - 1} {cx} {y - 1} C {cx + 5} {y - 1} {cx + 11} {y + 1} {cx + 12} {y + 12} Z" fill="{fill}" stroke="{INK}" stroke-width="1.6"/>\n'
            k += 1
    assert k == 32
    s += link(690, 510, 998, 510, INK, 2.5)
    return s

MOTIFS["pretend-borrowers"] = (pretend_borrowers, "Thirty-two simulated people around one phone showing a practice loan app")


def credit_four_things():
    """Four steps from a written idea to real outcomes; the last one is still empty."""
    s = ""
    s += text(100, 142, "OMNEQUA", 17, TEAL, anchor="start", weight="bold", sans=True)
    s += text(100, 267, "Is our credit", 46, INK, anchor="start")
    s += text(100, 330, "assessment credible?", 46, INK, anchor="start")
    s += link(102, 380, 176, 380, AMBER, 5)
    s += f'<circle cx="866" cy="294" r="220" fill="{TEAL_SOFT}" opacity="0.28"/>\n'
    labels = ("Proposal", "Source", "Running", "Outcomes")
    for i, name in enumerate(labels):
        x = 690 + i * 78
        y = 440 - i * 74
        if i < 3:
            s += f'<rect x="{x}" y="{y}" width="70" height="{510 - y}" rx="6" fill="{TEAL_SOFT if i != 1 else AMBER_SOFT}" stroke="{INK}" stroke-width="2"/>\n'
        else:
            s += f'<rect x="{x}" y="{y}" width="70" height="{510 - y}" rx="6" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="6 6"/>\n'
        s += text(x + 35, 534, name, 12, INK, anchor="middle", sans=True)
    s += link(690, 510, 994, 510, INK, 2.5)
    return s

MOTIFS["credit-four-things"] = (credit_four_things, "Four steps from a proposal to real outcomes, the last one still empty")


def beyond_the_game():
    s = text(600, 130, "BEYOND THE GAME", 36)
    # A virtual storefront opens onto two concrete questions, not promised returns.
    for x, y in [(190, 240), (260, 205), (330, 240)]:
        s += f'<rect x="{x}" y="{y}" width="64" height="64" rx="5" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="2"/>'
    s += text(285, 370, "THE IDEA", 22, MUTED)
    s += link(420, 270, 565, 270, INK, 3)
    s += link(565, 270, 710, 225, TEAL, 3)
    s += link(565, 270, 710, 390, TEAL, 3)
    for y, label in [(225, "A REAL ORDER"), (390, "HUMAN JUDGMENT")]:
        s += f'<rect x="730" y="{y-42}" width="330" height="84" rx="14" fill="{TEAL_SOFT}" stroke="{TEAL}" stroke-width="3"/>'
        s += text(895, y+8, label, 23)
    s += text(600, 525, "START WITH A NEED", 24, MUTED)
    return s

MOTIFS["beyond-the-game"] = (beyond_the_game, "A virtual storefront branches toward an existing order and human judgment")


def write(name):
    if name not in MOTIFS:
        raise SystemExit(f"unknown illustration {name!r}; choose one of {', '.join(MOTIFS)}")
    fn, label = MOTIFS[name]
    svg = HEAD.replace("{label}", html.escape(label, quote=True)) + fn() + FOOT
    atomic_write(ROOT / "images" / f"{name}.svg", svg)
    print("wrote images/%s.svg (%d bytes)" % (name, len(svg)))


if __name__ == "__main__":
    for n in (sys.argv[1:] or MOTIFS):
        write(n)
