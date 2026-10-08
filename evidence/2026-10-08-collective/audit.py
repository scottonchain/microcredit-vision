#!/usr/bin/env python3
"""Independent accounting and reproducibility audit for the collective model.

Uses Python's standard library. Run after simulate.py has written results:
    python audit.py
    python audit.py --results results --json audit-result.json

This checks implementation consistency, not empirical validity of assumptions.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import statistics
import sys


TOLERANCE = 1e-7


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path(__file__).with_name('simulate.py'))
    parser.add_argument('--results', type=Path, default=Path(__file__).with_name('results'))
    parser.add_argument('--json', type=Path, help='Optional path for the audit report')
    args = parser.parse_args()

    spec = importlib.util.spec_from_file_location('independent_audit_target', args.source)
    model = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = model
    spec.loader.exec_module(model)

    csv_path = args.results / 'runs.csv'
    with csv_path.open(newline='') as f:
        rows = list(csv.DictReader(f))
    assert rows, 'No saved histories'
    for row in rows:
        for key in row:
            if key not in ('arm', 'scenario'):
                row[key] = float(row[key])
                assert math.isfinite(row[key]), ('non-finite value', key, row)

    by_key = {(r['scenario'], int(r['seed']), r['arm']): r for r in rows}
    assert len(by_key) == len(rows), 'Duplicate scenario/seed/arm histories'
    seeds = sorted({int(r['seed']) for r in rows})
    expected = {(s, seed, a) for s in model.SCENARIOS for seed in seeds for a in model.ARMS}
    assert set(by_key) == expected, 'Missing or unexpected comparison histories'

    errors = {
        'cash_conservation': max(abs(
            r['external_revenue'] - r['external_nonhuman_cost'] - r['human_wages']
            - r['human_patronage'] - (r['end_cash'] + r['capital_returned'] - model.CAPITAL)
        ) for r in rows),
        'economic_surplus': max(abs(
            r['external_revenue'] - r['external_nonhuman_cost']
            - model.WAGE * r['human_hours'] - r['total_surplus_after_opportunity_cost']
        ) for r in rows),
        'entrant_earnings': max(abs(
            r['entrant_cash_income'] - model.WAGE * r['entrant_hours'] - r['entrant_net_income']
        ) for r in rows),
        'principal_reconciliation': max(abs(
            r['loans_issued'] - r['principal_repaid'] - r['principal_written_off']
        ) for r in rows if r['arm'] == 'pooled_loans'),
        'loan_fee_loss_reconciliation': max(abs(
            r['interest_internal'] - r['principal_written_off'] - r['loan_book_interest_less_writeoffs']
        ) for r in rows if r['arm'] == 'pooled_loans'),
    }
    for name, error in errors.items():
        assert error < TOLERANCE, (name, error)
    assert all(r['end_cash'] >= -TOLERANCE for r in rows), 'Negative terminal cash'

    economic_keys = (
        'external_revenue', 'external_nonhuman_cost', 'human_wages', 'human_patronage',
        'human_hours', 'end_cash', 'capital_returned', 'members', 'admissions',
        'entrant_cash_income', 'entrant_net_income', 'total_surplus_after_opportunity_cost',
        'unpaid_overhead',
    )
    parity_error = max(
        abs(r[k] - by_key[(r['scenario'], int(r['seed']), 'direct_treasury')][k])
        for r in rows if r['arm'] == 'pooled_loans' for k in economic_keys
    )
    assert parity_error < TOLERANCE, ('loan/direct economic parity', parity_error)

    # Re-execution also exercises the model's transaction-level conservation,
    # exposure completion and settlement-runoff assertions.
    sample_seeds = sorted({seeds[0], seeds[min(19, len(seeds) - 1)], seeds[-1]})
    rerun_count = 0
    reproduction_error = 0.0
    for seed in sample_seeds:
        for scenario in model.SCENARIOS:
            offers = model.draw_jobs(seed, scenario)
            for arm in model.ARMS:
                actual = model.run(seed, scenario, arm, offers)
                saved = by_key[(scenario, seed, arm)]
                for key, value in actual.items():
                    if isinstance(value, (int, float)):
                        reproduction_error = max(reproduction_error, abs(value - saved[key]))
                rerun_count += 1
    assert reproduction_error < TOLERANCE, ('reproducibility', reproduction_error)

    base = [r for r in rows if r['scenario'] == 'base' and r['arm'] == 'pooled_loans']
    overhead = [r for r in rows if r['scenario'] == 'overhead_4' and r['arm'] == 'pooled_loans']
    report = {
        'status': 'passed',
        'histories_checked': len(rows),
        'seeds': len(seeds),
        'scenarios': len(model.SCENARIOS),
        'arms': len(model.ARMS),
        'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
        'runs_csv_sha256': hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        'maximum_errors_usd': errors,
        'loan_direct_economic_parity_error': parity_error,
        'histories_reexecuted': rerun_count,
        'sample_seeds': sample_seeds,
        'maximum_reexecution_difference': reproduction_error,
        'base_loan_fee_less_writeoffs_median': statistics.median(
            r['interest_internal'] - r['principal_written_off'] for r in base),
        'base_loan_fee_less_writeoffs_negative_fraction': statistics.fmean(
            r['interest_internal'] < r['principal_written_off'] for r in base),
        'base_retrospective_extra_cost_ceiling_per_week': statistics.median(
            r['total_surplus_after_opportunity_cost'] / model.WEEKS for r in base),
        'base_retrospective_retained_only_cost_ceiling_per_week': statistics.median(
            r['retained_capital_change'] / model.WEEKS for r in base),
        'overhead_scenario_unfunded_budget_histories': sum(
            r['unpaid_overhead'] > TOLERANCE for r in overhead),
        'limitations': [
            'Consistency checks do not validate customer demand, prices or poverty effects.',
            'Extra fixed-cost ceilings hold jobs fixed and do not establish cash-flow feasibility.',
            'Unpaid overhead is tracked as an unmet service budget, not deducted as creditor debt.',
        ],
    }
    output = json.dumps(report, indent=2) + '\n'
    if args.json:
        args.json.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
