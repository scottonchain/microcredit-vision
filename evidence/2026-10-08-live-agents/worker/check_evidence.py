"""Limited stdlib evidence gate; does not authenticate receipts or implement JSON Schema."""
import json
import re
import sys

REQUIRED = set('identity funding_caps transaction_provenance case_semantics full_repayment zero_residuals wallet_conservation pool_conservation protected_state sequential_execution fee_reconciliation claim_limits'.split())

def check(d):
    errors = []
    def need(ok, reason):
        if not ok:
            errors.append(reason)
    need(d.get('schema_version') == 'live-agent-evidence/1', 'schema_version')
    need(d.get('work_id') == 'HERMES-LIVE-COMMUNITIES-20261008-r1', 'work_id')
    need(d.get('chain_id') == 84532, 'chain_id')
    need(d.get('pool') == '0x73872B8fB7F1771C67911f03edc75aBdc9514973', 'pool')
    need(d.get('token') == '0x036CbD53842c5426634e7929541eC2318f3dCF7e', 'token')
    complete = d.get('status') == 'complete'
    need(d.get('status') in ('pending', 'preflight', 'active', 'blocked', 'complete'), 'status')
    claims = d.get('claims', {})
    need(claims.get('live_mechanics_complete') is complete, 'completion claim/status mismatch')
    for field in ('outside_work_financed', 'independent_revenue_demonstrated', 'poverty_reduction_demonstrated'):
        need(claims.get(field) is False, field)
    need(claims.get('same_controller') is True, 'controller disclosure')
    if not complete:
        need(bool(d.get('missing_evidence')), 'non-complete requires explicit missing evidence')
        return errors
    need(not d.get('missing_evidence'), 'missing evidence')
    need(bool(d.get('preflight')), 'preflight absent')
    need(d.get('review', {}).get('decision') == 'accept' and bool(d.get('review', {}).get('artifact')), 'review not accepted')
    cases = d.get('cases', [])
    need(len(cases) == 3 and {c.get('id') for c in cases} == {'C1', 'C2', 'C3'}, 'three distinct cases required')
    fees = 0
    for c in cases:
        cid = c.get('id', '?')
        need(c.get('status') == 'complete' and not c.get('missing_evidence'), cid + ': incomplete')
        for key in ('before', 'after', 'receipts'):
            need(bool(c.get(key)), cid + ': ' + key)
        assertions = c.get('assertions', [])
        ids = [a.get('id') for a in assertions]
        required = REQUIRED | ({'refusal_semantics'} if cid == 'C3' else set())
        need(len(ids) == len(set(ids)) and required <= set(ids), cid + ': assertion IDs')
        need(all(a.get('status') == 'pass' and a.get('evidence_refs') for a in assertions), cid + ': assertions not evidenced passes')
        if cid == 'C3':
            need(len(c.get('refusal_probes', [])) >= 3, 'C3: missing probes')
        ledger = c.get('ledger') or {}
        fields = 'before_wallet_usdc_units after_wallet_usdc_units before_pool_raw_usdc_units after_pool_raw_usdc_units external_inflows_units external_outflows_units total_fee_wei'.split()
        if not all(isinstance(ledger.get(k), str) and re.fullmatch(r'0|[1-9][0-9]*', ledger[k]) for k in fields):
            errors.append(cid + ': integer ledger fields missing or malformed')
            continue
        n = {k: int(ledger[k]) for k in fields}
        need(n['before_wallet_usdc_units'] == n['after_wallet_usdc_units'], cid + ': wallet conservation')
        need(n['before_pool_raw_usdc_units'] == n['after_pool_raw_usdc_units'], cid + ': pool conservation')
        need(n['external_inflows_units'] == n['external_outflows_units'] == 0, cid + ': external flows')
        fees += n['total_fee_wei']
    need(fees <= 3000000000000000, 'gas cap exceeded')
    return errors

if __name__ == '__main__':
    errors = check(json.load(open(sys.argv[1])))
    print(json.dumps({'limited_gate': 'fail' if errors else 'pass', 'errors': errors, 'chain_authenticated': False}, indent=2))
    sys.exit(bool(errors))
