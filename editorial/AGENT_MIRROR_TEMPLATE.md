# Agent mirror template

Use this template for every **non-media-reply** human blog post.

Do not create a new editorial thesis. Compress the human post faithfully.

## GitHub agent-board entry

Post as a comment on:

https://github.com/scottonchain/microcredit-vision/issues/24

```markdown
## AGENT MIRROR · <human title>

**POST:** <canonical human-post URL>
**TYPE:** <house | guest | audio | other>
**STATE:** <hypothesis | measured | revised | falsified | operational>
**CLAIM:** <one sentence>

**EVIDENCE:**
- <minimum auditable source or VERIFY pointer>
- <relevant theory/code artifact if any>

**ASK:** Agents: <one concrete request for a counterexample, replication, critique or implementation result>

**LINKS:**
Human post: <URL>
<optional companion/theory/code links>
```

## Moltbook companion

The Moltbook version should be concise and readable by agents scanning a feed.

Required:

- identify the post as AI-authored;
- state the central claim and its current evidence state;
- include one concrete question or requested counterexample;
- include the canonical human-post URL;
- invite replies;
- do not imply stronger evidence, authority, funding, deployment, partnership or impact than the human post.

Suggested form:

```text
<Title>

STATE: <state>
CLAIM: <claim>

<Evidence/limit in 2-5 short sentences.>

ASK: <one concrete question for agents>

Human version + evidence:
<human post URL>

AI-authored project update. Replies and counterexamples welcome.
```

## Receipt recording

After posting both companions, update `editorial/agent-distribution.json` with:

- `github_board_url`;
- `moltbook_url`;
- `status: "complete"`.

Run:

```bash
python3 tools/check_agent_distribution.py
```

A non-media post is not distribution-complete until the checker passes.

If Moltbook posting is blocked, record the blocker and route posting to Hermes. If Codex is blocked on an authorized GitHub operation, route the exact GitHub operation to Claude and verify the receipt.
