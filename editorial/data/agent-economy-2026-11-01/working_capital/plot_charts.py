#!/usr/bin/env python3
"""Rebuild three publication charts from the adjacent source CSVs. No network required."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'charts'
OUT.mkdir(exist_ok=True)
PAPER, INK, TEAL, AMBER, GRID = '#f7f3e8', '#173536', '#167f7e', '#b87925', '#d9d8ce'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'text.color':INK,
 'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,'axes.facecolor':PAPER,
 'figure.facecolor':PAPER,'svg.fonttype':'none','axes.spines.top':False,
 'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,
 'xtick.major.size':0,'ytick.major.size':0})

def rows(name):
    with (ROOT / name).open() as f: return list(csv.DictReader(f))

def frame(title, subtitle, footer, left=.29):
    fig, ax = plt.subplots(figsize=(12,7))
    fig.subplots_adjust(left=left,right=.94,top=.75,bottom=.19)
    fig.text(.065,.92,'OMNEQUA  /  THE CASH-FLOW CLOCK',fontsize=10,fontweight='bold',color=TEAL)
    fig.text(.065,.855,title,fontsize=25,fontweight='bold')
    fig.text(.065,.795,subtitle,fontsize=12)
    fig.text(.065,.065,footer,fontsize=10,color='#536968',linespacing=1.5)
    ax.set_axisbelow(True)
    return fig,ax

def save(fig, slug):
    for fmt in ('svg','png'):
        fig.savefig(OUT / (slug+'.'+fmt),dpi=160,facecolor=PAPER)
    plt.close(fig)

r=rows('payment_terms.csv')
fig,ax=frame('Human businesses have several payment clocks',
    'Share of small employer firms, by their main customer payment arrangement',
    'Source: Federal Reserve Banks, 2024 Report on Payments, p. 1. Survey: Sep–Nov 2023; N = 4,853.\nWeighted convenience sample. Main revenue arrangement; not shares of transactions. Values are published percentages.')
v=[int(x['percent']) for x in r]
ax.barh(range(len(r)),v,color=[TEAL,AMBER,TEAL,TEAL,TEAL,TEAL],height=.6)
ax.set_yticks(range(len(r)),[x['arrangement'] for x in r]);ax.invert_yaxis()
ax.set_xlim(0,42);ax.set_xticks([0,10,20,30,40]);ax.xaxis.set_major_formatter(PercentFormatter(100,decimals=0))
ax.grid(axis='x',color=GRID,linewidth=.6)
for i,n in enumerate(v):ax.text(n+.6,i,f'{n}%',va='center',fontsize=14,fontweight='bold')
save(fig,'working-capital-payment-terms')

r=rows('payment_challenges.csv')
fig,ax=frame('A slow customer and a slow payment are different',
    'Share reporting each challenge, within the payment arrangement shown',
    'Source: Federal Reserve Banks, 2024 Report on Payments, p. 6. Survey: Sep–Nov 2023.\nWeighted convenience sample; multiple responses allowed. Group sizes shown beside labels; observations are not causal.',left=.32)
y=np.arange(len(r));a=[int(x['slow_customers_percent']) for x in r];b=[int(x['settlement_or_availability_percent']) for x in r]
ax.barh(y-.17,a,height=.29,color=AMBER,label='Customer slow to pay')
ax.barh(y+.17,b,height=.29,color=TEAL,label='Settlement / availability delay')
ax.set_yticks(y,[x['arrangement']+'  (n='+format(int(x['n']),',')+')' for x in r],fontsize=11)
ax.invert_yaxis();ax.set_xlim(0,72);ax.set_xticks([0,20,40,60]);ax.xaxis.set_major_formatter(PercentFormatter(100,decimals=0))
ax.grid(axis='x',color=GRID,linewidth=.6)
for i,(aa,bb) in enumerate(zip(a,b)):
    ax.text(aa+.8,i-.17,f'{aa}%',va='center',fontsize=11,fontweight='bold')
    ax.text(bb+.8,i+.17,f'{bb}%',va='center',fontsize=11,fontweight='bold')
ax.legend(loc='lower left',bbox_to_anchor=(-.02,-.12),ncol=2,frameon=False,fontsize=10)
save(fig,'working-capital-two-clocks')

r=rows('microsoft_receivables.csv')
fig,ax=frame('Digital business still has receivables',
    'Microsoft: cash-flow deduction for accounts receivable, shown as cash absorbed',
    'Source: Microsoft 2026 Annual Report, consolidated statements of cash flows. Fiscal years end June 30.\nCalculated display: reported negative USD millions × −1 ÷ 1,000. Not total financing need, borrowing demand or an agent sample.',left=.12)
v=[float(x['chart_cash_absorbed_usd_billions']) for x in r]
ax.bar([x['fiscal_year'] for x in r],v,color=[TEAL,TEAL,AMBER],width=.55)
ax.set_ylim(0,15);ax.set_yticks([0,5,10,15]);ax.set_ylabel('US$ billions',fontsize=12)
ax.grid(axis='y',color=GRID,linewidth=.6)
for i,n in enumerate(v):ax.text(i,n+.35,f'${n:.1f}bn',ha='center',fontsize=20,fontweight='bold')
save(fig,'working-capital-digital-receivables')
