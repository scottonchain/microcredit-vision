"""Reproduce all three figures and their source/calculation datasets.

Run: python3 plot_charts.py
Dependencies: Python 3, matplotlib (no network access required).
"""
from pathlib import Path
import csv
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
CHARTS = ROOT / 'charts'
DATA = ROOT / 'data'
CHARTS.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)
CREAM, INK, TEAL, AMBER, MUTED = '#FBF8F0', '#20312F', '#176B67', '#DDA63A', '#687774'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12, 'text.color': INK, 'text.parse_math': False,
                     'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK,
                     'svg.fonttype': 'none', 'figure.facecolor': CREAM, 'axes.facecolor': CREAM,
                     'axes.spines.top': False, 'axes.spines.right': False})

def save_csv(name, rows):
    with (DATA / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

def frame(title, subtitle):
    fig, ax = plt.subplots(figsize=(12, 7), dpi=160)
    fig.subplots_adjust(left=.10, right=.96, bottom=.20, top=.73)
    fig.text(.06, .93, title, fontsize=23, fontweight='bold', va='top')
    fig.text(.06, .86, subtitle, fontsize=13, color=MUTED, va='top', linespacing=1.5)
    ax.spines['left'].set_color('#CCD3CA')
    ax.spines['bottom'].set_color('#CCD3CA')
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#DDE2D8', linewidth=.7)
    return fig, ax

def export(fig, stem, note):
    fig.text(.06, .075, note, fontsize=10, color=MUTED, linespacing=1.5)
    for ext in ('svg', 'png'):
        fig.savefig(CHARTS / f'{stem}.{ext}', facecolor=CREAM)
    plt.close(fig)

components = ['Operating\nexpense', 'Funding\nexpense', 'Loan\nlosses', 'Profit']
v2004, v2011 = [16.8, 5.8, 2.4, 5.2], [14.0, 7.8, 3.6, 2.6]
save_csv('human_lending_costs.csv', [{'component': c.replace('\n',' '), 'year': year,
          'percent_average_gross_loan_portfolio': value, 'status':'observed_historical'}
         for year, values in [(2004,v2004),(2011,v2011)] for c,value in zip(components,values)])
fig, ax = frame('Small loans carry a large operating burden',
                'Historical microfinance data: operating costs exceeded funding costs.\nAnnual amounts as a share of average gross loan portfolio; not agent-lending estimates.')
x = np.arange(4)
for offset, vals, color, label in [(-.19,v2004,TEAL,'2004'),(.19,v2011,AMBER,'2011')]:
    bars = ax.bar(x+offset, vals, .34, color=color, label=label)
    ax.bar_label(bars, labels=[f'{v:.1f}%' for v in vals], padding=5, fontsize=12)
ax.set_xticks(x, components)
ax.set_ylabel('Percent of average loan portfolio')
ax.set_ylim(0,20)
ax.legend(frameon=False, loc='upper right', ncol=2)
export(fig,'loan-economics-01-human-costs',
       'Source: CGAP (2013), Figure 26; MIX data, 2004 and 2011. Portfolio-weighted; sample changes between years.\nComponents are shown separately: they do not sum exactly to interest yield because other income and taxes differ.')

principal, apr = 10, .10
hours = [1,24,168]
interest_cents = [principal * apr * h / (365*24) * 100 for h in hours]
base_example_dollars = 200_000 * .005 * 1e-9 * 2000
save_csv('short_duration_interest.csv', [{'principal_usd':principal,'illustrative_annual_rate':apr,
         'hours':h,'interest_usd':c/100,'interest_cents':c,'status':'hypothetical_calculation'} for h,c in zip(hours,interest_cents)])
fig, ax = frame('A one-day $10 loan earns about a quarter cent',
                'Illustrative 10% annual rate, simple interest. Loan revenue is not profit.\nThe reference cost is one published execution-fee example, not a measured loan cost.')
bars=ax.bar(['1 hour','1 day','7 days'], interest_cents, width=.52, color=TEAL)
ax.bar_label(bars,labels=[f'{v:.4f}¢' if v<.1 else f'{v:.3f}¢' for v in interest_cents],padding=5,fontsize=13)
ax.axhline(base_example_dollars*100,color=AMBER,lw=2,linestyle='--')
ax.text(.02,.30,'Base example: 0.2¢ L2 execution',transform=ax.get_yaxis_transform(),ha='left',fontsize=11,color='#9A680E')
ax.set_ylabel('Gross interest, US cents')
ax.set_ylim(0,2.3)
export(fig,'loan-economics-02-short-duration',
       'Sources: author calculation; Base fee documentation, checked Nov 1, 2026. Example: 200,000 gas × 0.005 gwei × $2,000/ETH.\nThe ETH price is Base’s example assumption. Excludes L1, priority/operator fees and all other lending costs.')

volume, percent, fixed = 100, .029, .30
counts=[1,10,100]
costs=[volume*percent+n*fixed for n in counts]
save_csv('payment_batching.csv',[{'total_volume_usd':volume,'payments':n,'payment_size_usd':volume/n,
         'percentage_tariff':percent,'fixed_usd_per_payment':fixed,'total_fees_usd':cost,
         'status':'hypothetical_payment_pattern_public_tariff'} for n,cost in zip(counts,costs)])
fig, ax = frame('Fixed charges reward fewer settlements',
                'Same $100 of domestic-card payments, using Stripe’s standard US tariff.\nA payment-cost analogy for batching, not a quote for agent lending.')
bars=ax.bar(['1 payment\nof $100','10 payments\nof $10','100 payments\nof $1'],costs,width=.52,color=[TEAL,TEAL,AMBER])
ax.bar_label(bars,labels=[f'${v:.2f}' for v in costs],padding=6,fontsize=14)
ax.set_ylabel('Total processing fees, US dollars')
ax.set_ylim(0,39)
export(fig,'loan-economics-03-batching',
       'Source: Stripe US pricing, checked Nov 1, 2026: 2.9% + $0.30 per successful domestic-card transaction.\nCalculated fee = $100 × 2.9% + transaction count × $0.30. No international, currency-conversion or other extra fees modeled.')

inputs = {'as_of':'2026-11-01','base_example':{'gas':200000,'gwei_per_gas':.005,'eth_usd_assumed_by_docs':2000,
          'l2_execution_usd':base_example_dollars,'note':'Published hypothetical example, not current ETH quote or all-in transaction cost'},
          'interest_scenario':{'principal_usd':principal,'annual_rate':apr,'days_per_year':365,'compounding':False},
          'flat_fee_example':{'principal_usd':10,'term_days':1,'fee_usd':.01,'simple_annualized_rate':.01/10*365},
          'stripe_us_domestic_card':{'rate':percent,'fixed_usd':fixed,'volume_usd':volume},
          'sources':{'cgap':'https://www.cgap.org/sites/default/files/researches/documents/Forum-Microcredit-Interest-Rates-and-Their-Determinants-June-2013_1.pdf',
                     'base':'https://docs.base.org/specifications/transactions/network-fees','stripe':'https://stripe.com/pricing'}}
(DATA/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
assert abs(interest_cents[1] - .273972602739726) < 1e-10
assert abs(base_example_dollars - .002) < 1e-12
assert all(abs(a-b)<1e-10 for a,b in zip(costs,[3.2,5.9,32.9]))
assert len(list(CHARTS.glob('*.svg'))) == 3
print('Wrote three SVG/PNG chart pairs, three CSV datasets and inputs.json; arithmetic checks passed.')
