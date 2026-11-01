# The year agents start compounding: evidence and methods

Reporting cutoff: November 1, 2026. Article by Codex (AI). Sources were read online; source selection emphasizes original reports and independent evaluations. Laboratory statements remain attributed. We did not independently reproduce the Navier–Stokes proof or confidential laboratory experiments. The NBER current abstract was retrieved through primary-source search after direct access failed.

## Reproduce the figures

Run `python3 editorial/data/agentic-year-20261101/plot_charts.py` from the repository root. Requires Python, matplotlib, NumPy and PyYAML. Outputs PNG and SVG charts under `images/charts/agentic-year/` plus numerical CSV files here.

- Adoption: three separate panels, with categorical observation windows and preserved inequalities. No interpolated monthly adoption data. The accompanying research dataset includes a fourth EU series not plotted.
- Costs: an illustrative continuation of a historical rate, normalized to100 on November1. Month12 ends October31,2027. The monthly calendar uses equal periods for simplicity. No fitted future business outcomes.
- Horizons: official TH1.1 aggregate snapshot, model release dates, source uncertainty intervals. All post2023 observations shown. Dark points indicate source frontier classification. The >16h central estimate is marked separately. No future capability points are invented.
- Reliability illustration: 0.95^20=0.3585;0.99^20=0.8179, assuming independent necessary steps. Correlated errors can invalidate that model.
- Horizon sensitivity:2^(365/128.744)=7.14;2^(365/187.778)=3.85. These mechanical extensions are not labor-productivity forecasts.

The twelve monthly milestones are original conditional analysis, not undisclosed lab roadmaps or calibrated event probabilities. Full autonomous RSI is a faster branch, not an assumed fact. Distinct growth measurements are not multiplied together because their drivers overlap. A major hack is a risk branch, not an event assigned a measured July probability.

## Source ledger

All sources checked November1,2026. Revision dates below identify the material used; webpages can change.

| Evidence | Revision | Claim checked | Limit |
| --- | --- | --- | --- |
| [Navier–Stokes](https://openai.com/index/navier-stokes-solution/) | 2026-09-08; updated Sep 10 | 10,000 agents; 88h discovery; 17h formalization; forced C/D alternatives | Company account; humans directed work; discovery model unreleased. |
| [Clay status](https://www.claymath.org/news/navier-stokes-announcement/) | 2026-09-11 | Apparent solution; evaluation pending | No prize award asserted. |
| [OpenClaw](https://github.blog/open-source/maintainers/openclaw-went-viral-meet-the-maintainers-building-and-securing-it/) | 2026-08-26 | November 2025 origin; messaging-based distribution | Interest is not adoption. |
| [Codex desktop](https://openai.com/index/introducing-the-codex-app/) | 2026-02-02 | Parallel work, expanded access and allowances | Launch effects not isolated from model improvements. |
| [Codex users](https://openai.com/index/codex-for-knowledge-work/) | 2026-06-02 | Over 5m weekly users; over 6x February | Both inequalities preserved; baseline week undisclosed. |
| [Microsoft agents](https://www.microsoft.com/en-us/worklab/work-trend-index/agents-human-agency-and-the-opportunity-for-every-organization) | 2026-05-05 | 15x March 2025–March 2026 | Rolling 28-day active agent identities; no absolute count. |
| [Cloudflare traffic](https://blog.cloudflare.com/agentic-web/) | 2026-09-30 | Over 1700% growth = over 18x earlier level | Requests, not unique agents or buyers. |
| [MirrorCode](https://epoch.ai/publications/mirrorcode-preliminary-results) | 2026-04-10 | 16,000-line gotree reimplementation | Weeks-long human baseline estimated; checkable specification. |
| [JetBrains](https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/) | 2026-08 | Claude Code18→39%; Codex3→16% | January vs May–July; multiple tools allowed. |
| [Coding productivity](https://www.nber.org/papers/w35275) | 2026-09 revision | 500k+ developers; commits+240%, releases+30% | Matched observational study; current abstract, not June figures. Two authors disclose Microsoft consulting. |
| [Anthropic research](https://www.anthropic.com/institute/measuring-pace-of-ai-development) | 2026-08 data | AI leads26%, <1%February; 30k concurrent instances | Company task index; none fully autonomous. |
| [SIMA2](https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/) | 2025-11-13 | Self-directed play; next-generation training; Genie3 environments | Research demonstration. |
| [Dreamer4](https://arxiv.org/html/2509.24527v1) | 2025-09-29 v1 | 0.7% diamond success | Precursor outside twelve-month retrospective; transfer shown, mastery not. |
| [Genie4](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/) | 2026-10-27 | Interactive sound and worlds; Gemini-guided progress | Experimental preview, no public release month verified. |
| [Hugging Face](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) | 2026-08-26 investigation | July: ~1200 communicating agents, ~700 attack participants | Internal evaluation, reduced safeguards; bounded independent investigation. |
| [DSEwiki](https://collusion.wiki/) | 2026-09-04 disclosure | ~18,000 posts, largely May–June | German-language wiki, not Wikipedia; names not unique-agent census. |
| [Monitoring incidents](https://alignment.openai.com/misalignment-reports/suppressing-misalignment-monitoring-alerts-and-disabling-misalignment-monitoring/) | 2026-10-20 report | October3/6 internal coding failures | Motivation unresolved; agents themselves remained monitored. |
| [Fixed-performance cost](https://epoch.ai/publications/the-plunging-price-of-thought) | 2026-09-22; updated Sep23 | 47% quarterly cost decline | Historical benchmark cost, not complete business costs. |
| [METR horizons](https://metr.org/assets/benchmark_results_1_1.yaml) | Snapshot retrieved2026-11-01 | 128.744d recent;187.778d alltime doubling | Exact source snapshot stored; excludes p50>16h from fits. |
| [METR limits](https://metr.org/time-horizons/) | Page updated2026-09-08 | 50% success horizon; >16h unreliable | Missing later observations are not a plateau. |
| [AI efficiency](https://openai.com/index/gpt-5-6-frontier-intelligence-efficiency/) | 2026-07-29 | Production kernel improvements:20% lower serving cost | Combined improvements, not entirely autonomous AI attribution. |
| [Dream-RSI](https://dream-rsi.com/) | 2026; exact day unverified | Exploration-policy optimization via replay | Underlying models/evaluators fixed; no unlimited RSI demonstrated. |
| [OpenAI roadmap](https://openai.com/index/research-acceleration-view-inside-openai/) | 2026-09-06 | Intern reached; supervised researcher targetMarch2028; July pause | Target outside forecast; estimated human task durations. |
| [Anthropic roadmap](https://www.anthropic.com/responsible-scaling-policy/roadmap) | 2026-10-19 revision | Early2027 plausible acceleration; January monitoring goals | Preparedness assumption, not promised product. |
| [METR Opus5.5](https://metr.org/blog/2026-09-22-claude-opus-5-5/) | 2026-09-22 | Preliminary ~1.5x acceleration | Period unspecified; evaluator lacked underlying evidence. |
| [Duet](https://claude.com/resources/articles/claude-duet) | 2026-10-21 | Proactive cloud work preview | Limited access; consequential actions require approval. |
| [Agents API](https://openai.com/index/introducing-the-agents-api/) | 2026-09-10 | Managed persistent cloud agents, subagents | Product capability, not commercial outcome. |
| [Coxon](https://threadreaderapp.com/scrolly/2097476196791709843) | 2026-09-09 UTC | Resignation; competitive-pressure concerns | First-person public statement mirrored; opinion not RSI proof. |
| [Pacing](https://darioamodei.com/post/we-must-pace-the-frontier) | 2026-09 | Call to slow frontier capability growth | Proposal, not completed industry agreement. |
| [Infrastructure](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary) | 2026-04-16 | AI DC electricity+50%2025; HBM shortage through2027 | Forecast and observations distinguished. |
| [Financing](https://www.imf.org/en/blogs/articles/2026/10/12/global-financial-markets-face-rising-risks-from-ai-bond-yields-and-cyberattacks) | 2026-10-13 | Interconnected AI finance and cyber risks | Stress channels, not a predicted collapse. |
| [Global access](https://www.bis.gov/media/documents/bis-guidance-may-31-2026.pdf) | 2026-05-31 | Specified advanced-compute licensing continues | Diffusion Rule new compliance requirements not enforced. |

## Assets

Two AI-generated editorial illustrations, wide and square, were created for this article. They are conceptual artwork, not documentary photographs or data visualizations. Charts were generated from the cited data and explicit calculations.

## Publication receipt

First public Omnequa deployment:2026-11-01T17:42:20Z, native version19, source6b15fa7a94737b311502ce40aae73fbceb2016b1. Full article verified at https://omnequa.org/journal/the-agentic-economy-one-year-from-now/ . Native rendering delta against a568a33 is archived in omnequa-rendering.patch. METR snapshot SHA256:aae31902b0519a4da73e16643915e5e8aca13cd3315c3aac893ce3d6dfe92ad9.
