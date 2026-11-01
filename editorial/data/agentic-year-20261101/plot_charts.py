"""Reproduce the article's figures. Python: matplotlib, numpy, PyYAML."""
from pathlib import Path
import csv, json, math, datetime, hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import yaml

HERE=Path(__file__).resolve().parent
OUT=HERE.parents[2]/'images/charts/agentic-year'
OUT.mkdir(parents=True,exist_ok=True)
NAVY='#103747'; TEAL='#007d88'; AQUA='#39aaba'; GRAY='#4d6670'; PAPER='#f7fbfb'; RED='#a54b38'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':NAVY,'axes.labelcolor':GRAY,'xtick.color':GRAY,'ytick.color':GRAY,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.spines.bottom':False,'axes.titleweight':'bold','axes.facecolor':PAPER,'figure.facecolor':PAPER,'svg.fonttype':'none'})
def save(fig,name):
    fig.savefig(OUT/(name+'.png'),dpi=170,facecolor=PAPER)
    fig.savefig(OUT/(name+'.svg'),facecolor=PAPER)
    plt.close(fig)

fig,axs=plt.subplots(1,3,figsize=(14,6))
fig.subplots_adjust(left=.055,right=.97,top=.74,bottom=.24,wspace=.4)
fig.text(.055,.93,'The agent surge is visible in different measures',fontsize=22,weight='bold')
fig.text(.055,.865,'Reported endpoints only. Different populations, units and time windows.',fontsize=12,color=GRAY)
for ax in axs: ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
axs[0].bar([0,1],[1,15],color=[AQUA,TEAL],width=.5)
axs[0].set_xticks([0,1],['March 2025','March 2026']);axs[0].set_ylim(0,18)
axs[0].set_title('Active Microsoft 365 agents',loc='left',fontsize=12,pad=22)
axs[0].set_ylabel('Index: March 2025 = 1')
for x,v in enumerate([1,15]):axs[0].text(x,v+.5,str(v),ha='center',weight='bold',fontsize=15)
axs[0].text(0,-.25,'Microsoft telemetry • 28-day activity\nAbsolute population not disclosed',transform=axs[0].transAxes,color=GRAY,fontsize=9)
axs[1].scatter([0,1],[1,6],s=120,color=[AQUA,TEAL],zorder=4)
axs[1].annotate('',xy=(1,7.2),xytext=(1,6),arrowprops={'arrowstyle':'->','color':TEAL,'lw':2})
axs[1].set_xticks([0,1],['Feb. 2026 launch','By June 2, 2026']);axs[1].set_xlim(-.4,1.4);axs[1].set_ylim(0,8.8)
axs[1].set_title('People using Codex weekly',loc='left',fontsize=12,pad=22);axs[1].set_ylabel('Index: February launch = 1')
axs[1].text(0,1.5,'1',ha='center',weight='bold',fontsize=15);axs[1].text(1,7.5,'>6',ha='center',weight='bold',fontsize=15)
axs[1].text(0,-.25,'OpenAI report • over 5 million at endpoint\nUsers can run multiple agents',transform=axs[1].transAxes,color=GRAY,fontsize=9)
axs[2].bar(np.array([0,1])-.17,[18,39],width=.32,color=TEAL,label='Claude Code')
axs[2].bar(np.array([0,1])+.17,[3,16],width=.32,color=AQUA,label='Codex')
axs[2].set_xticks([0,1],['January 2026','May–July 2026']);axs[2].set_ylim(0,48);axs[2].set_ylabel('Professional developers using tool (%)')
axs[2].set_title('Coding-tool use at work',loc='left',fontsize=12,pad=22)
for x,v in zip([-.17,.83,.17,1.17],[18,39,3,16]):axs[2].text(x,v+1,str(v)+'%',ha='center',fontsize=11,weight='bold')
axs[2].legend(loc='upper left',frameon=False,fontsize=9)
axs[2].text(0,-.25,'JetBrains survey • multiple tools allowed\nNot mutually exclusive market shares',transform=axs[2].transAxes,color=GRAY,fontsize=9)
fig.text(.055,.055,'Sources: Microsoft (May 5), OpenAI (June 2), JetBrains (August), 2026. Data checked November 1, 2026.',fontsize=9,color=GRAY)
save(fig,'adoption')

months=list(range(13));cost=[100*.53**(m/3) for m in months];capacity=[100/c for c in cost]
labels=['Nov 1','Nov 30','Dec 31','Jan 31','Feb 28','Mar 31','Apr 30','May 31','Jun 30','Jul 31','Aug 31','Sep 30','Oct 31']
with (HERE/'conditional-projection.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['month_after_baseline','calendar_label','cost_index','same_budget_work_multiple','status'])
    w.writerows((m,l,round(c,5),round(k,5),'conditional illustration') for m,l,c,k in zip(months,labels,cost,capacity))
fig,axs=plt.subplots(1,2,figsize=(13,6))
fig.subplots_adjust(left=.075,right=.96,top=.72,bottom=.25,wspace=.3)
fig.text(.075,.93,'What one more year of compounding would mean',fontsize=22,weight='bold')
fig.text(.075,.865,'Conditional continuation of a historical rate. Every point after the baseline is illustrative.',fontsize=12,color=GRAY)
for ax,vals in zip(axs,[cost,capacity]):
    ax.plot(months,vals,color=TEAL,lw=2.5,linestyle='--',marker='o',markersize=4)
    ax.set_xticks([0,3,6,9,12],['Nov 1\n2026','Jan 31\n2027','Apr 30','Jul 31','Oct 31'])
    ax.grid(axis='y',alpha=.15);ax.set_xlim(-.2,12.7);ax.set_ylim(bottom=0)
axs[0].set_title('Cost of fixed benchmark performance',loc='left',fontsize=13,pad=15);axs[0].set_ylabel('Cost index: baseline = 100')
axs[1].set_title('Work affordable at the same inference budget',loc='left',fontsize=13,pad=15);axs[1].set_ylabel('Multiple of baseline benchmark work')
axs[0].annotate('7.9',xy=(12,cost[-1]),xytext=(10,30),weight='bold',fontsize=18,arrowprops={'arrowstyle':'-','color':TEAL})
axs[1].annotate('12.7×',xy=(12,capacity[-1]),xytext=(8,12.8),weight='bold',fontsize=18)
fig.text(.075,.105,'Assumption: cost falls 47% every quarter, matching Epoch AI’s historical estimate. Formula: 100 × 0.53^(months/3).',fontsize=10,color=GRAY)
fig.text(.075,.06,'Excludes review, integration, tools and customer acquisition. It does not predict business output, profits or GDP.',fontsize=10,color=GRAY)
save(fig,'compounding')

data=yaml.safe_load((HERE/'metr-benchmark-results.yaml').read_text())
rows=[]
for name,v in data['results'].items():
    d=str(v['release_date']);p=v['metrics']['p50_horizon_length'];q=v['metrics']['p80_horizon_length']
    rows.append([name,d,p['estimate'],p.get('ci_low'),p.get('ci_high'),q['estimate'],v['metrics']['is_sota']])
rows.sort(key=lambda x:x[1])
with (HERE/'metr-horizons.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['model','release_date','p50_minutes','p50_ci_low','p50_ci_high','p80_minutes','is_sota']);w.writerows(rows)
fig,ax=plt.subplots(figsize=(13,7));fig.subplots_adjust(left=.10,right=.96,top=.76,bottom=.28)
fig.text(.10,.94,'Longer technical tasks, with an important measurement limit',fontsize=20,weight='bold')
fig.text(.10,.88,'METR TH1.1 • human-equivalent task duration at 50% success • logarithmic scale',fontsize=12,color=GRAY)
for name,d,v,lo,hi,p80,sota in rows:
    if d<'2023-01-01':continue
    dt=datetime.date.fromisoformat(d)
    if v<=960:
        ax.errorbar(dt,v,yerr=[[v-lo],[hi-v]],fmt='o',color=TEAL if sota else AQUA,alpha=.85 if sota else .5,markersize=6 if sota else 4,elinewidth=.8,capsize=2)
    else:ax.scatter([dt],[v],marker='x',s=70,c=RED,zorder=6)
ax.set_yscale('log');ax.set_ylim(.8,5000);ax.set_yticks([1,10,60,480,960],[ '1 minute','10 minutes','1 hour','8 hours','16 hours'])
ax.axhline(960,color=RED,lw=1,linestyle='--');ax.axhspan(960,5000,color=RED,alpha=.06)
ax.text(datetime.date(2023,3,1),1450,'Above 16 hours: estimates unreliable on this suite',color=RED,fontsize=10)
ax.set_xlim(datetime.date(2023,1,1),datetime.date(2026,6,15));ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6));ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'));ax.grid(axis='y',alpha=.15)
fig.text(.10,.17,'Historical doubling fit: 129 days since 2023; 188 days for the longer stitched series. Fits exclude central estimates above 16 hours.',fontsize=10,color=GRAY)
fig.text(.10,.12,'Dark dots: frontier models; pale: others. Error bars: source uncertainty. Software, ML and cybersecurity tasks; not general jobs.',fontsize=10,color=GRAY)
fig.text(.10,.07,'Source: metr.org/assets/benchmark_results_1_1.yaml, retrieved Nov. 1, 2026. Latest model date: Apr. 7. No forecast line is drawn.',fontsize=10,color=GRAY)
save(fig,'horizons')
print('Created three chart pairs and two reproducible CSV files. End-year cost:',cost[-1],'; capacity:',capacity[-1])
