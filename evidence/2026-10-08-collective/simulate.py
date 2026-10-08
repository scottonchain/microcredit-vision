#!/usr/bin/env python3
"""Illustrative paired-agent working-capital experiment. Python stdlib only.
No fitted parameters; all economics are scenario assumptions. See MODEL.md.
"""
from __future__ import annotations
import argparse, csv, json, math, random, statistics
from dataclasses import dataclass, field
from pathlib import Path

SKILLS = ('retrieve', 'build', 'review', 'local')
ARMS = ('solo', 'cooperate_wallets', 'pooled_loans', 'customer_prepayment', 'direct_treasury')
SCENARIOS = ('base', 'zero_demand', 'adverse', 'low_margin', 'withdrawal', 'fixed_low_demand', 'fixed_members', 'overhead_4')
CAPITAL = 80.0
WEEKS = 26
WAGE = 12.0
CAPACITY = 4.0
RESERVE = 12.0
PAYOUT = 0.60
ONBOARD_EXTERNAL = 6.0
ONBOARD_HOURS = 1.5
ONBOARD_COST = ONBOARD_EXTERNAL + ONBOARD_HOURS * WAGE

@dataclass
class Member:
    ident: int
    skill: str
    cash: float
    age: int = 0
    wage: float = 0.0
    patronage: float = 0.0
    hours: float = 0.0
    active_debt: float = 0.0

@dataclass
class Job:
    ident: int
    week: int
    kind: str
    requirements: dict[str, float]
    human_hours: dict[str, float]
    price: float
    tools: float
    success: bool
    lag: int

@dataclass
class State:
    arm: str
    members: list[Member]
    treasury: float
    pending: list = field(default_factory=list)
    revenue: float = 0.0
    nonhuman: float = 0.0
    wages: float = 0.0
    patronage: float = 0.0
    hours: float = 0.0
    returned_capital: float = 0.0
    loans_issued: float = 0.0
    principal_repaid: float = 0.0
    principal_written_off: float = 0.0
    interest_internal: float = 0.0
    accepted: int = 0
    bundles: int = 0
    completed: int = 0
    failed: int = 0
    finance_missed: int = 0
    capacity_missed: int = 0
    underwriting_reject: int = 0
    admissions: int = 0
    max_cash_error: float = 0.0
    min_cash: float = CAPITAL
    overhead_unpaid: float = 0.0

    def cash(self):
        return self.treasury + sum(m.cash for m in self.members)

    def verify(self):
        # Loan draws/repayments/interest are INTERNAL and absent here.
        rhs = CAPITAL + self.revenue - self.nonhuman - self.wages - self.patronage - self.returned_capital
        error = abs(self.cash() - rhs)
        self.max_cash_error = max(self.max_cash_error, error)
        assert error < 1e-7, (self.arm, self.cash(), rhs, error)
        assert self.treasury >= -1e-8 and all(m.cash >= -1e-8 for m in self.members)
        self.min_cash = min(self.min_cash, self.cash())


def poisson(rng, mean):
    n, product = 0, 1.0
    while product > math.exp(-mean):
        n += 1
        product *= rng.random()
    return n - 1


def draw_jobs(seed, scenario):
    # Separate generation from policy: identical opportunities and failure draws
    # are offered to each comparison arm, regardless of actions or admission.
    rng = random.Random(seed)
    jobs = [[] for _ in range(WEEKS)]
    ident = 0
    for week in range(WEEKS):
        shared_bad_week = rng.random() < (0.18 if scenario == 'adverse' else 0.06)
        if scenario == 'zero_demand':
            intensity = 0.0
        elif scenario == 'fixed_low_demand':
            intensity = 0.55
        else:
            intensity = 1.4 + 0.06 * week  # exogenous, pre-generated scenario
        counts = [('bundle', i) for i in range(min(7, poisson(rng, intensity)))]
        counts += [(skill, 0) for skill in SKILLS if rng.random() < (0.0 if scenario == 'zero_demand' else 0.7)]
        for kind, _ in counts:
            bundle = kind == 'bundle'
            requirements = dict(zip(SKILLS, (1., 0.75, 1., 2.))) if bundle else {kind: 0.65}
            hours = dict(zip(SKILLS, (0.4, 0.3, 0.6, 0.7))) if bundle else {kind: 0.25}
            price = (52.0 if bundle else 11.0) * rng.uniform(0.85, 1.15)
            if scenario == 'low_margin':
                price *= 0.64
            tools = (2.17 if bundle else 0.8) * rng.uniform(0.9, 1.1)
            fail_probability = (0.40 if scenario == 'adverse' else 0.25) if shared_bad_week else (0.08 if scenario == 'adverse' else 0.025)
            success = rng.random() > fail_probability
            lag = (3 if scenario == 'adverse' else 2) if rng.random() < 0.25 else 1
            jobs[week].append(Job(ident, week, kind, requirements, hours, price, tools, success, lag))
            ident += 1
    return jobs


def get_assignment(st, job, capacity):
    if st.arm == 'solo':
        # An isolated member may buy missing capabilities from outside suppliers.
        # No hard ban on integrated work. Contractor retail fee is explicit.
        available = [m for m in st.members if m.skill in job.requirements and capacity[m.ident] >= job.requirements[m.skill] and m.active_debt < 1e-8]
        if not available:
            return None
        lead = max(available, key=lambda m: (job.human_hours.get(m.skill, 0), m.cash))
        allocation = {lead.ident: job.human_hours.get(lead.skill, 0)}
        usage = {lead.ident: job.requirements.get(lead.skill, 0.65)}
        missing = [skill for skill in job.requirements if skill != lead.skill]
        outsourced = sum(job.human_hours[s] * WAGE + 6.0 for s in missing)
        return lead, allocation, usage, outsourced
    assignment, usage = {}, {}
    for skill, needed in job.requirements.items():
        candidates = [m for m in st.members if m.skill == skill and capacity[m.ident] >= needed]
        if not candidates:
            return None
        chosen = min(candidates, key=lambda m: (m.hours, m.ident))
        assignment[chosen.ident] = job.human_hours[skill]
        usage[chosen.ident] = needed
    participants = [st.members[i] for i in assignment]
    debt_free = [m for m in participants if m.active_debt < 1e-8]
    if not debt_free:
        return None
    # Identical one-outstanding-job and lead-selection rules in all cooperative
    # arms. Wallet size only selects the member who can actually pay upfront.
    lead = max(debt_free, key=lambda m: (m.cash, -((m.ident + job.ident) % len(st.members))))
    return lead, assignment, usage, 0.0


def credit_cash(st, amount, lead, allocation, principal=0.0, surplus=0.0):
    if st.arm in ('pooled_loans', 'direct_treasury'):
        st.treasury += amount
    else:
        # Restore the payer's advance, then retain remaining working capital
        # among participants in proportion to their human contribution.
        recovered = min(amount, principal)
        st.members[lead].cash += recovered
        residual = amount - recovered
        total = sum(allocation.values())
        if total:
            for i, h in allocation.items():
                st.members[i].cash += residual * h / total
        else:
            st.members[lead].cash += residual


def settle(st, week):
    live = []
    for p in st.pending:
        if p['due'] > week:
            live.append(p)
            continue
        job, lead = p['job'], st.members[p['lead']]
        lead.active_debt -= p['debt']
        if job.success:
            customer_receipt = job.price - p['prepay']
            st.revenue += customer_receipt
            platform = 0.10 * job.price
            st.nonhuman += platform
            surplus = job.price - platform - p['upfront']
            assert surplus > -1e-8
            patronage = PAYOUT * surplus
            st.patronage += patronage
            total_hours = sum(p['allocation'].values())
            for i, h in p['allocation'].items():
                st.members[i].patronage += patronage * h / total_hours
            retained_cash = customer_receipt - platform - patronage
            assert retained_cash >= -1e-8
            credit_cash(st, retained_cash, lead.ident, p['allocation'], principal=p['financed'])
            st.completed += 1
            if st.arm == 'pooled_loans':
                st.principal_repaid += p['debt']
                # Fee is carved out of retention, never added to revenue/profit.
                st.interest_internal += min(0.01 * p['debt'], (1 - PAYOUT) * surplus)
        else:
            # Nonrefundable mobilization payment (prepayment arm only) covers
            # work already performed. Remaining customer bill is uncollectible.
            st.failed += 1
            if st.arm == 'pooled_loans':
                st.principal_written_off += p['debt']
        st.verify()
    st.pending = live


def withdraw(st, amount):
    # Equity redemption, NOT wages or profit; no deposit guarantee is implied.
    actual = min(amount, st.cash())
    remaining = actual
    take = min(st.treasury, remaining)
    st.treasury -= take
    remaining -= take
    for m in st.members:
        take = min(m.cash, remaining)
        m.cash -= take
        remaining -= take
    st.returned_capital += actual
    st.verify()


def maybe_admit(st, week, jobs):
    if st.arm == 'solo' or week < 6 or week % 2 or len(st.members) >= 7:
        return
    # Realized demand, no growth forecast based on membership. Incumbents vote
    # yes only if observed packages exceed present local capacity by 10%.
    recent = jobs[week-6:week]
    observed = sum(j.kind == 'bundle' for weeks in recent for j in weeks) / 6
    local_capacity = sum(m.skill == 'local' for m in st.members) * CAPACITY / 2
    if observed <= local_capacity * 1.1:
        return
    # A new local member cannot fix a different skill's bottleneck.
    other_capacity = min(sum(m.skill == s for m in st.members) * CAPACITY / need
                         for s, need in [('retrieve',1), ('build',0.75), ('review',1)])
    if other_capacity <= local_capacity:
        return
    buffer = ONBOARD_COST + 2 * 30 + RESERVE
    if st.cash() < buffer:
        return
    # A voluntary one-time contribution can fund membership training even in
    # the no-loan arm; it cannot fund ordinary jobs. Initial comparison cash is
    # identical and newcomers arrive with no savings or new customers.
    remaining = ONBOARD_COST
    take = min(st.treasury, remaining)
    st.treasury -= take
    remaining -= take
    for m in sorted(st.members, key=lambda m: -m.cash):
        take = min(m.cash, remaining)
        m.cash -= take
        remaining -= take
    assert remaining < 1e-8
    newcomer = Member(len(st.members), 'local', 0.0, age=week,
                      wage=ONBOARD_HOURS * WAGE, hours=ONBOARD_HOURS)
    st.members.append(newcomer)
    st.wages += ONBOARD_HOURS * WAGE
    st.hours += ONBOARD_HOURS
    st.nonhuman += ONBOARD_EXTERNAL
    st.admissions += 1
    st.verify()


def run(seed, scenario, arm, jobs=None):
    pooled = arm in ('pooled_loans', 'direct_treasury')
    members = [Member(i, skill, 0.0 if pooled else CAPITAL / 4) for i, skill in enumerate(SKILLS)]
    st = State(arm, members, CAPITAL if pooled else 0.0)
    jobs = jobs if jobs is not None else draw_jobs(seed, scenario)
    for week in range(WEEKS):
        settle(st, week)
        if scenario == 'overhead_4':
            due = 4.0
            paid = min(due, st.cash())
            cash_before = st.cash()
            if cash_before > 0:
                fraction = paid / cash_before
                st.treasury *= 1 - fraction
                for member in st.members:
                    member.cash *= 1 - fraction
            st.nonhuman += paid
            st.overhead_unpaid += due - paid
            st.verify()
            if paid < due - 1e-8:
                continue  # insufficient operating budget: no new work this week
        if scenario == 'withdrawal' and week == 8:
            withdraw(st, 40.0)
        if scenario != 'fixed_members':
            maybe_admit(st, week, jobs)
        capacity = {m.ident: CAPACITY for m in st.members}
        # Common stable priority; largest integrated jobs cannot crowd out
        # commodity jobs merely through policy-specific randomization.
        for job in sorted(jobs[week], key=lambda j: (j.kind != 'bundle', j.ident)):
            plan = get_assignment(st, job, capacity)
            if plan is None:
                st.capacity_missed += 1
                continue
            lead, allocation, usage, outsourcing = plan
            labor = sum(allocation.values()) * WAGE
            coordination = 0.40 if arm == 'solo' else (2.40 if job.kind == 'bundle' else 0.50)
            upfront = job.tools + labor + outsourcing + coordination
            # Prepayment is a real, distinct contract: customer pays 50%
            # nonrefundable mobilization fee for completed initial work.
            prepay = min(0.50 * job.price, 0.95 * upfront) if arm == 'customer_prepayment' else 0.0
            financed = max(0.0, upfront - prepay)
            # Simple conservative known-risk underwriting; realized outcomes
            # are not inspected. Reject negative expected contribution work.
            risk = 0.16 if scenario == 'adverse' else 0.06
            expected_collection = prepay + (1-risk) * (job.price - prepay)
            expected_cost = upfront + (1-risk) * 0.10 * job.price
            if expected_collection <= expected_cost + 0.50:
                st.underwriting_reject += 1
                continue
            book_capital = st.cash() + sum(p['financed'] for p in st.pending)
            if st.cash() - financed < RESERVE or financed > 0.6 * book_capital:
                st.finance_missed += 1
                continue
            if pooled:
                st.treasury -= financed
            else:
                if lead.cash + 1e-8 < financed:
                    st.finance_missed += 1
                    continue
                lead.cash -= financed
            # Price cannot create surplus cash at mobilization under params.
            assert prepay < upfront
            st.revenue += prepay
            st.nonhuman += job.tools + outsourcing + coordination
            st.wages += labor
            st.hours += sum(allocation.values())
            for i, h in allocation.items():
                st.members[i].wage += h * WAGE
                st.members[i].hours += h
                capacity[i] -= usage[i]
                assert capacity[i] >= -1e-8
            debt = financed  # exposure tracking in every arm, only pooled_loans books a loan
            lead.active_debt += debt
            st.pending.append(dict(job=job, due=week + job.lag, lead=lead.ident,
                                   allocation=allocation, upfront=upfront,
                                   financed=financed, prepay=prepay, debt=debt))
            if arm == 'pooled_loans':
                st.loans_issued += debt
            st.accepted += 1
            st.bundles += job.kind == 'bundle'
            st.verify()
    # Settlement runoff prevents treating an outstanding receivable as cash.
    for week in range(WEEKS, WEEKS + 4):
        settle(st, week)
    assert not st.pending
    assert all(abs(m.active_debt) < 1e-7 for m in st.members)
    if arm == 'pooled_loans':
        assert abs(st.loans_issued - st.principal_repaid - st.principal_written_off) < 1e-7
    st.verify()
    entrants = [m for m in st.members if m.ident >= 4]
    net_income = st.wages + st.patronage - st.hours * WAGE
    # Retained capital is not counted as immediately spendable human income.
    return {
        'seed': seed, 'scenario': scenario, 'arm': arm,
        'members': len(st.members), 'admissions': st.admissions,
        'external_revenue': st.revenue, 'external_nonhuman_cost': st.nonhuman,
        'human_wages': st.wages, 'human_hours': st.hours,
        'human_patronage': st.patronage, 'human_cash_income': st.wages + st.patronage,
        'net_human_income_after_opportunity_cost': net_income,
        'end_cash': st.cash(), 'capital_returned': st.returned_capital,
        'retained_capital_change': st.cash() + st.returned_capital - CAPITAL,
        'total_surplus_after_opportunity_cost': net_income + st.cash() + st.returned_capital - CAPITAL,
        'capital_impaired': int(st.cash() + st.returned_capital < CAPITAL - 1e-8),
        'liquidity_closed': int(st.cash() < RESERVE + 4.0),
        'minimum_cash': st.min_cash,
        'jobs_accepted': st.accepted, 'bundles_accepted': st.bundles,
        'jobs_paid': st.completed, 'jobs_failed': st.failed,
        'finance_missed': st.finance_missed, 'capacity_missed': st.capacity_missed,
        'underwriting_reject': st.underwriting_reject,
        'loan_book_interest_less_writeoffs': st.interest_internal - st.principal_written_off,
        'loans_issued': st.loans_issued, 'principal_repaid': st.principal_repaid,
        'principal_written_off': st.principal_written_off, 'interest_internal': st.interest_internal,
        'entrant_cash_income': sum(m.wage + m.patronage for m in entrants),
        'entrant_hours': sum(m.hours for m in entrants),
        'entrant_net_income': sum(m.patronage for m in entrants),
        'max_cash_error': st.max_cash_error, 'unpaid_overhead': st.overhead_unpaid,
    }


def quantile(xs, p):
    xs = sorted(xs)
    pos = (len(xs) - 1) * p
    lo = math.floor(pos)
    hi = math.ceil(pos)
    return xs[lo] * (hi-pos) + xs[hi] * (pos-lo) if hi != lo else xs[lo]


def summarize(rows):
    summary = {}
    numeric = [k for k in rows[0] if k not in ('seed', 'arm', 'scenario')]
    for scenario in SCENARIOS:
        summary[scenario] = {}
        for arm in ARMS:
            group = [row for row in rows if row['scenario'] == scenario and row['arm'] == arm]
            summary[scenario][arm] = {k: {'p10': quantile([r[k] for r in group], .1),
                                                'median': quantile([r[k] for r in group], .5),
                                                'p90': quantile([r[k] for r in group], .9),
                                                'mean': statistics.fmean(r[k] for r in group)} for k in numeric}
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seeds', type=int, default=600)
    parser.add_argument('--output', type=Path, default=Path(__file__).parent / 'results')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    rows = []
    for scenario in SCENARIOS:
        for seed in range(args.seeds):
            jobs = draw_jobs(seed, scenario)
            matched = {arm: run(seed, scenario, arm, jobs) for arm in ARMS}
            # Loan bookkeeping cannot manufacture aggregate economic gains.
            for key in ('external_revenue', 'end_cash', 'human_wages', 'human_patronage', 'members'):
                assert abs(matched['pooled_loans'][key] - matched['direct_treasury'][key]) < 1e-8
            rows.extend(matched.values())
    with (args.output / 'runs.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    summary = summarize(rows)
    paired = {}
    for scenario in SCENARIOS:
        paired[scenario] = {}
        for compare in ('solo', 'cooperate_wallets', 'customer_prepayment'):
            a = [r for r in rows if r['scenario'] == scenario and r['arm'] == 'pooled_loans']
            b = [r for r in rows if r['scenario'] == scenario and r['arm'] == compare]
            for metric in ('net_human_income_after_opportunity_cost', 'total_surplus_after_opportunity_cost', 'external_revenue'):
                diffs = [x[metric] - y[metric] for x,y in zip(a,b)]
                paired[scenario][compare + '__' + metric] = dict(p10=quantile(diffs,.1), median=quantile(diffs,.5), p90=quantile(diffs,.9), probability_positive=statistics.fmean(d>0 for d in diffs))
    output = {'metadata': {'seeds': args.seeds, 'weeks': WEEKS, 'initial_capital': CAPITAL, 'currency': 'illustrative USD', 'parameters_empirically_fitted': False}, 'summary': summary, 'paired_differences': paired}
    (args.output / 'summary.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'base': {a: {m: round(summary['base'][a][m]['median'],2) for m in ('external_revenue','human_cash_income','net_human_income_after_opportunity_cost','end_cash','members','entrant_cash_income')} for a in ARMS}, 'max_conservation_error': max(r['max_cash_error'] for r in rows), 'runs':len(rows)}, indent=2))

if __name__ == '__main__':
    main()
