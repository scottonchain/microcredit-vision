# Internal independent challenge and disposition

November5 2026. Separate Codex reviewer; no external expert or human borrower validation. Reviewer read the draft and code independently and reproduced the numerical defect. Author: Codex (AI).

| Challenge | Disposition |
| --- | --- |
| Full unit plus1e-30 bypasses Decimal ceiling | ACCEPT/FIXED: reject excess precision and size; regression; production integer minor units specified. |
| Collateral promise counted as cash recovery | ACCEPT/FIXED: only settled principal cash in recovery; expected collateral belongs in separate LGD/timing model. |
| Narrative-ignoring helper does not test an actual security boundary | ACCEPT: actual pinned interview source probed; candidate guard tested; live UI/backend/oracle boundary remains a release gate. |
| Familiarity cannot waive affordability/security | ACCEPT: tier table keeps essential checks; attack-mixture sensitivity and incident hold added. |
| Single group misses overlapping correlation | ACCEPT: production requires all applicable groups; reference explicitly limited to one partition. |
| Conservation not security/solvency | ACCEPT: assumptions, unrelated liabilities and limit-decrease behavior stated. |
| Self-loop ban could appear to repair graph attack | ACCEPT/FIXED: directed cycle test demonstrates same trapped cluster mass. |
| Crash, broadcast retry, forged recovery and reorg absent | ACCEPT: explicit live-adapter acceptance cases; no unsupported passed claim. |
| Brier loss is proper, not an incentive to lie | ACCEPT/FIXED: low absolute score can reflect base rate, not incremental skill. |
| Noninteger n silently truncated | ACCEPT/FIXED with regression. |

Stronger alternative adopted: consented no-debt feasibility study, verified-facts baseline, graph shadow-only, funded maximum-loss envelope for any later separately authorized credit, and an unendorsed application/appeal route. The reviewer does not certify deployed underwriting or human readiness. A factual/technical maintainer review and the existing publication owner remain required before publication.

Delta review accepted report and human protocol as preparation, and required guard amendments: catch extractor exceptions without leaking messages; reject null/malformed results; allowlist diagnostic fields; project only validated inputs; state that an in-process callback is not sandboxed. All four amendments are implemented with two additional regression tests (seven guard tests total). No deployment or outside validation follows.
