"""Reproduce three publication figures from the accompanying transcribed public data.

Run: python plot_charts.py
Inputs, definitions and exact source locators: sources.json and FACTCHECK.md.
Charts describe AI spending/adoption and human firms, not a census of agent wealth.
"""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'charts'
OUT.mkdir(exist_ok=True)
PAPER, INK, TEAL, AMBER, MUTED = '#F8F3E8', '#173B3F', '#197C80', '#D39D39', '#617578'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':14, 'text.color':INK,
    'axes.labelcolor':INK, 'xtick.color':MUTED, 'ytick.color':INK,
    'axes.facecolor':PAPER, 'figure.facecolor':PAPER, 'svg.fonttype':'none',
    'axes.spines.top':False, 'axes.spines.right':False, 'axes.spines.left':False,
    'axes.spines.bottom':False})

def rows(name):
    with (ROOT/'data'/name).open(newline='') as f: return list(csv.DictReader(f))

def canvas(title, subtitle, source, note):
    fig, ax = plt.subplots(figsize=(12, 6.3))
    fig.subplots_adjust(left=.13, right=.94, top=.74, bottom=.22)
    fig.text(.06,.94,'OMNEQUA  /  THE AGENT ECONOMY',fontsize=10,fontweight='bold',color=TEAL)
    fig.text(.06,.86,title,fontsize=25,fontweight='bold')
    fig.text(.06,.80,subtitle,fontsize=12,color=MUTED)
    fig.text(.06,.115,source,fontsize=10,color=MUTED)
    fig.text(.06,.07,note,fontsize=10,color=MUTED)
    return fig,ax

def save(fig, slug):
    fig.savefig(OUT/f'{slug}.png',dpi=160)
    fig.savefig(OUT/f'{slug}.svg')
    plt.close(fig)

d=rows('enterprise_ai_spending.csv')
fig,ax=canvas('AI has buyers with budgets', 'Estimated enterprise generative AI spending, US$ billions',
    'Source: Menlo Ventures, 2025 State of Generative AI in the Enterprise.',
    'Restated series; excludes chips, inference/model serving and AI bundled into existing software. Estimates, not agent balances.')
values=[float(r['usd_billions']) for r in d]
bars=ax.bar([r['year'] for r in d],values,color=[AMBER,TEAL,INK],width=.52)
ax.set_ylim(0,42); ax.set_yticks([0,10,20,30,40]); ax.set_ylabel('US$ billions')
ax.yaxis.grid(True,color=INK,alpha=.12);ax.set_axisbelow(True);ax.tick_params(length=0)
for bar,v in zip(bars,values): ax.text(bar.get_x()+bar.get_width()/2,v+1,f'${v:g}B',ha='center',fontsize=20,fontweight='bold')
save(fig,'01-enterprise-ai-budgets')

d=rows('ai_adoption_by_firm_size.csv')
fig,ax=canvas('AI users are not all large companies','Businesses reporting AI use, by employment size · four-period average to June 14, 2026',
    'Source: U.S. Census BTOS, reproduced in Federal Reserve Board accessible data, Figure 8 (July 17, 2026).',
    'Each observation concerns a business, not an agent. AI use does not measure operator wealth or credit access.')
values=[float(r['percent']) for r in d]
bars=ax.barh([r['employees'] for r in d],values,color=[TEAL]*6+[AMBER],height=.62)
ax.invert_yaxis();ax.set_xlim(0,46);ax.set_xticks([0,10,20,30,40]);ax.xaxis.set_major_formatter(PercentFormatter())
ax.set_ylabel('Employees');ax.xaxis.grid(True,color=INK,alpha=.12);ax.set_axisbelow(True);ax.tick_params(length=0)
for bar,v in zip(bars,values):ax.text(v+.8,bar.get_y()+bar.get_height()/2,f'{v:.1f}%',va='center',fontsize=13,fontweight='bold')
save(fig,'02-ai-use-by-firm-size')

d=rows('firm_financing_constraint.csv')
fig,ax=canvas('Financing constraints are not universal','Did financing access or cost constrain investment or spending plans? · September 2026 CFO Survey',
    'Source: Richmond Fed, “Are Firms Financially Constrained?” (September 23, 2026), Figure 3 and accompanying text.',
    '19% is the published share; 81% is its complement. Survey respondents, not all human enterprises or an agent comparison.')
ax.barh([0],[19],color=AMBER,height=.55)
ax.barh([0],[81],left=[19],color=TEAL,height=.55)
ax.text(9.5,0,'19%',ha='center',va='center',fontsize=28,fontweight='bold',color=INK)
ax.text(59.5,0,'81%',ha='center',va='center',fontsize=28,fontweight='bold',color='white')
ax.text(9.5,-.43,'Constrained',ha='center',fontsize=14,fontweight='bold')
ax.text(59.5,-.43,'Not constrained',ha='center',fontsize=14,fontweight='bold')
ax.set_xlim(0,100);ax.set_ylim(-.8,.8);ax.set_xticks([]);ax.set_yticks([])
save(fig,'03-human-firms-and-finance')
print('Wrote three SVG and three PNG charts.')
