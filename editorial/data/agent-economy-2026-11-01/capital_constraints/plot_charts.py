"""Rebuild three Omnequa figures from the accompanying transcribed public table.
Requires Python 3, matplotlib, numpy. Run: python plot_charts.py
No network, credentials, proprietary data, or undocumented adjustments required.
"""
from pathlib import Path
import csv
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
with (HERE/'findex_2024.csv').open() as f:
    rows = list(csv.DictReader(f))

def values(key):
    return np.array([float(r[key]) for r in rows])

CREAM='#F7F3E8'; INK='#172B36'; TEAL='#167D8D'; AMBER='#D89936'; GREY='#DADDD9'; MUTED='#53626A'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':14,'text.color':INK,'axes.labelcolor':INK,'xtick.color':MUTED,'ytick.color':INK,'svg.fonttype':'none','svg.hashsalt':'omnequa-capital-2024','figure.facecolor':CREAM,'axes.facecolor':CREAM})
labels=['Low income','Lower middle income','Upper middle income']
y=np.arange(3)

def base(title, subtitle):
    fig,ax=plt.subplots(figsize=(12,7.4),dpi=150)
    fig.subplots_adjust(left=.235,right=.94,top=.70,bottom=.25)
    fig.text(.055,.94,'OMNEQUA  /  HUMAN ECONOMY, AGENT QUESTIONS',fontsize=11,weight='bold',color=TEAL)
    fig.text(.055,.865,title,fontsize=24,weight='bold')
    fig.text(.055,.805,subtitle,fontsize=14,color=MUTED)
    ax.set_xlim(0,100);ax.set_ylim(-.65,2.65);ax.invert_yaxis()
    ax.set_yticks(y,labels)
    ax.xaxis.set_major_formatter(PercentFormatter(100,decimals=0))
    ax.set_xticks(np.arange(0,101,20))
    ax.grid(axis='x',color='#DAD8CE',linewidth=.7,zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis='both',length=0,pad=10)
    for s in ax.spines.values():s.set_visible(False)
    fig.text(.055,.105,'Source: World Bank, Global Findex 2025, Little Data Book, pp. 10–12. Data: 2024.',fontsize=10,color=MUTED)
    return fig,ax

def save(fig, name, description):
    fig.savefig(HERE/f'{name}.png',dpi=150)
    fig.savefig(HERE/f'{name}.svg',metadata={'Title':name,'Description':description,'Creator':'Codex (OpenAI), Omnequa','Date':'2026-11-01'})
    plt.close(fig)

fig,ax=base('Having an account is not the same as saving','Share of adults aged 15+ • Economy income groups')
a=values('account_pct');s=values('saved_formally_pct')
ax.barh(y-.17,a,height=.28,color=TEAL,label='Has an account',zorder=3)
ax.barh(y+.17,s,height=.28,color=AMBER,label='Saved formally in the past year',zorder=3)
for ys,vs in [(y-.17,a),(y+.17,s)]:
    for yy,v in zip(ys,vs):ax.text(v+1.2,yy,f'{v:.1f}%',va='center',fontsize=13,weight='bold')
fig.legend(handles=[Patch(color=TEAL,label='Has an account'),Patch(color=AMBER,label='Saved formally in the past year')],loc='lower left',bbox_to_anchor=(.225,.14),frameon=False,ncol=2,fontsize=12)
fig.text(.055,.063,'Saving is a reported activity, not a measure of balances or available credit. These are human data.',fontsize=10,color=MUTED)
save(fig,'capital-access','World Bank 2024 data: account ownership versus formal saving. Low income 46.4% versus 27.6%; lower middle income 70.4% versus 26.1%; upper middle income 84.0% versus 55.4%. Adults aged 15+.')

fig,ax=base('Borrowing extends beyond formal lenders','Share of adults aged 15+ • Borrowing in the preceding year, for any purpose')
formal=values('borrowed_formally_pct');any_b=values('borrowed_any_pct')
informal=np.round(any_b-formal,1);none=np.round(100-any_b,1)
left=np.zeros(3)
for vals,c in [(formal,TEAL),(informal,AMBER),(none,GREY)]:
    ax.barh(y,vals,left=left,height=.48,color=c,zorder=3)
    for yy,v,l in zip(y,vals,left):ax.text(l+v/2,yy,f'{v:.1f}%',ha='center',va='center',color='white' if c==TEAL else INK,fontsize=13,weight='bold')
    left+=vals
fig.legend(handles=[Patch(color=TEAL,label='Formal borrowing¹'),Patch(color=AMBER,label='Informal only²'),Patch(color=GREY,label='No borrowing')],loc='lower left',bbox_to_anchor=(.225,.14),frameon=False,ncol=3,fontsize=12)
fig.text(.055,.063,'¹ Includes people who also borrowed informally.  ² Total borrowing minus formal borrowing.',fontsize=10,color=MUTED)
save(fig,'capital-borrowing','World Bank 2024 data: formal borrowing / informal-only borrowing / no borrowing. Low income 10.3 / 58.9 / 30.8%; lower middle income 14.1 / 48.3 / 37.6%; upper middle income 36.2 / 18.0 / 45.8%. Adults aged 15+; all purposes, not business borrowing alone.')

fig,ax=base('Poorer households have less financial backup','Share able to raise emergency funds in 30 days with at most some difficulty')
all_=values('emergency_funds_all_pct');poor=values('emergency_funds_poorest40_pct')
for yy,p,a in zip(y,poor,all_):
    ax.plot([p,a],[yy,yy],color='#B5B9B1',linewidth=5,zorder=2)
    ax.scatter(p,yy,s=150,color=AMBER,zorder=3)
    ax.scatter(a,yy,s=150,color=TEAL,zorder=3)
    ax.text(p,yy+.25,f'{p:.1f}%',ha='center',va='top',fontsize=13,color=INK,weight='bold')
    ax.text(a,yy-.25,f'{a:.1f}%',ha='center',va='bottom',fontsize=13,color=INK,weight='bold')
fig.legend(handles=[Line2D([],[],marker='o',linestyle='',color=TEAL,label='All adults (15+)'),Line2D([],[],marker='o',linestyle='',color=AMBER,label='Adults in poorest 40% of households')],loc='lower left',bbox_to_anchor=(.225,.14),frameon=False,ncol=2,fontsize=12)
fig.text(.055,.063,'Target: 5% of GNI per capita. Household income ranks are within economies; country groups use GNI.',fontsize=10,color=MUTED)
save(fig,'capital-resilience','World Bank 2024 data: all adults versus adults in poorest 40% of households able to raise emergency funds within 30 days, with no more than some difficulty. Low income 43.8% versus 34.7%; lower middle income 40.6% versus 28.5%; upper middle income 74.6% versus 60.7%. Target is 5% of GNI per capita in local currency.')

assert np.allclose(formal+informal+none,100)
assert all(np.all((values(k)>=0)&(values(k)<=100)) for k in rows[0] if k.endswith('_pct'))
with (HERE/'derived_borrowing.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['economy_income_group','year','formal_pct','informal_only_pct','no_borrowing_pct'])
    for i,label in enumerate(labels):w.writerow([label,2024,formal[i],informal[i],none[i]])
print('Generated three SVG/PNG chart pairs and derived_borrowing.csv; value and composition checks passed.')
