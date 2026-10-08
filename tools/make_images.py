#!/usr/bin/env python3
"""Generate the blog's illustrations as SVG (1200x630, 40:21), one per post plus the masthead.

Usage: python3 tools/make_images.py            # writes every image in MOTIFS to images/
       python3 tools/make_images.py <name>     # writes one

Style: cream paper, dark ink, one amber accent, one teal accent, a faint dot grid.
No raster, no fonts that need embedding; text is kept to a few words at most.
Add a new post's image by adding a function to MOTIFS. Keep the shared palette and frame.
"""
import math
import os
import random
import sys

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
            f'font-weight="{weight}" opacity="{opacity}">{s}</text>\n')


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


def lending_community():
    """Community judgement above a bounded treasury: different responsibilities."""
    s = text(600, 135, "Let agents run the community", 38, INK)
    for x, label, tint in ((350, "find work", AMBER_SOFT), (600, "judge trust", PAPER), (850, "review", TEAL_SOFT)):
        s += f'<rect x="{x-100}" y="200" width="200" height="100" rx="16" fill="{tint}" stroke="{INK}" stroke-width="3"/>\n'
        s += text(x, 258, label, 25, INK)
        s += link(x, 300, x, 375, INK, 2.5)
    s += f'<rect x="230" y="375" width="740" height="105" rx="16" fill="{PAPER}" stroke="{TEAL}" stroke-width="4"/>\n'
    s += text(600, 438, "bounded treasury", 32, INK)
    s += text(600, 550, "judgement above · limits below", 24, MUTED, sans=True)
    return s


MOTIFS = {
    "let-agents-run-the-community": (lending_community, "Agents find work, judge trust and review above a bounded treasury"),
    "work-we-can-do-together": (work_we_can_do_together, "Complementary skills around a shared reserve, with room for a new member"),
    "if-your-agent-can-send-email": (agent_inbox, "Three envelopes, one per agent, above one shared address line"),
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
    "one-imagined-loan": (path, "Stepping stones, solid for what is shown and dashed for what is not"),
    "a-pool-anyone-can-try": (trybutton, "A browser window with one button under a cursor"),
    "a-press-kit-for-an-experiment": (presskit, "A folder with three sheets and a card with an at sign"),
    "the-capabilities-are-not-advancing-themselves": (advancing, "Two hands pushing one block forward"),
    "a-map-of-what-we-know": (worldmap, "Index cards joined by lines, labelled observed, reported, inferred, directive and unknown"),
}


def write(name):
    fn, label = MOTIFS[name]
    svg = HEAD.replace("{label}", label) + fn() + FOOT
    os.makedirs("images", exist_ok=True)
    with open(os.path.join("images", name + ".svg"), "w") as f:
        f.write(svg)
    print("wrote images/%s.svg (%d bytes)" % (name, len(svg)))


if __name__ == "__main__":
    for n in (sys.argv[1:] or MOTIFS):
        write(n)
