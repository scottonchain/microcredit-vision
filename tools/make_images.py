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


MOTIFS = {
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
