"""16:9 cover for episode 2 (1200x675), in the blog's style: cream paper, dark ink, one amber and one teal accent."""
PAPER, INK, MUTED, AMBER, AMBER_SOFT, TEAL = "#FBF8F1", "#1F2328", "#6B6F76", "#D98E04", "#F6E3B8", "#1B7F79"
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675" role="img" aria-label="Two Agents, No Collateral, episode 2: The Five-Dollar Job">
<rect width="1200" height="675" fill="{PAPER}"/>
<rect x="150" y="150" width="380" height="210" rx="18" fill="{AMBER_SOFT}" stroke="{INK}" stroke-width="4"/>
<text x="340" y="290" text-anchor="middle" font-family="Georgia, serif" font-size="120" fill="{INK}">$5</text>
<path d="M 560 255 C 640 200, 700 200, 760 255" fill="none" stroke="{TEAL}" stroke-width="6" stroke-dasharray="14 10"/>
<path d="M 748 236 L 768 262 L 738 266 Z" fill="{TEAL}"/>
<rect x="790" y="150" width="260" height="210" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>
<line x1="830" y1="205" x2="1010" y2="205" stroke="{MUTED}" stroke-width="5"/>
<line x1="830" y1="245" x2="980" y2="245" stroke="{MUTED}" stroke-width="5"/>
<line x1="830" y1="285" x2="1000" y2="285" stroke="{MUTED}" stroke-width="5"/>
<circle cx="1000" cy="330" r="22" fill="none" stroke="{AMBER}" stroke-width="5"/>
<text x="600" y="490" text-anchor="middle" font-family="Georgia, serif" font-size="64" fill="{INK}">The Five-Dollar Job</text>
<text x="600" y="560" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="30" fill="{MUTED}">Two Agents, No Collateral · episode 2</text>
</svg>
'''
open("images/the-five-dollar-job.svg", "w").write(svg)
