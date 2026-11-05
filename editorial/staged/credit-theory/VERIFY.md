# Technical report verification map

Codex (AI), November5 2026. Every numerical statement is either a derived illustrative calculation, a pinned internal observation or a candidate study parameter. None is a calibrated borrower-risk estimate.

| Report material | Source / reproduction | Status |
| --- | --- | --- |
| Deployment84532/source1812e7d; prior32 personas; original27 tests | PR433 and pinned deployment/source links in report; fresh preflight in testbed supplement | Recorded deployment, offline results; fresh RPC blocked, no live release verification |
| PageRank normalization, alpha/k and cycle attack | Geometric-series derivation in report; test_bounds.py star/cycle cases | Conditional mathematics and synthetic counterexample |
| O+D<=B0 | Transition proof in report; bounded fixture tests | Assumes authentic serializable complete ledger; reference not production |
| -5.12 margin; 7.4468 break-even | Substitution in stated cashflow formula; original test_oracle.py | Illustrative, not price recommendation |
| 2.8x and10x variance | n10,L100,p.05,rho.2/1, test_bounds.py | Equal-exposure, full-loss-on-default correlation model, not tail-loss guarantee |
| 9.50% and0.994% zero-default bound | 1-.05**(1/n), n30/300 | iid same-risk assumption; not applicable to agent or correlated sample |
| 60-day horizon; six-decimal reference amounts | Candidate proposal; bounds.py | Unfrozen horizon; fixed synthetic currency precision, not arbitrary money arithmetic |
| p_eff=.127 | .9*.03+.1*1 | Admitted-exposure attack-mixture scenario, not measured rate |
| 17 reference tests and8 guard tests; five-case probe; recommendations10/1/10 | testbed supplement at58c9569; SOURCE.json, probe receipt and reproducible commands | Offline, zero model calls/transactions; no live integration |
| Human feasibility and recruitment | HUMAN-STUDY.md in same supplement | Proposed up to5 adults/25minutes/seven-day passive invitation; not enrollment or authorization |
| Rounding and guard defects/fixes | REVIEW.md; regression tests | Separate internal AI review, not external expert approval |

Primary-source passages inspected November5 2026: Basel Committee2025 credit-risk principles; NIST800-63-4 identity guidance and AI100-2 taxonomy abstract; OWASP prompt-injection and transaction-authorization guidance; Karlan group-banking introduction; IFC2026 Fintech Credit Innovation publisher introduction. SOURCE-REVIEW.md states the exact passage scope and limitations. The EBA page returned403 and its paraphrase was removed without retry; it is not claimed verified. Exact links are beside the retained claims in REPORT.md. They inform design but do not establish project compliance, repayment calibration or safe deployment.
