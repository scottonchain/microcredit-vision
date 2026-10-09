"""Add watch findings to the team world model (CLAUDE.md "Watch findings enter the world model", operator direction 2026-10-08, narrowed 2026-10-09: relevant findings only, no iteration receipts, nothing political).

Usage: python3 tools/world_model_receipt.py <receipts.json> [--testbed /home/user/microcredit-agent-testbed] [--no-push] [--onto <branch>]

--onto <branch> appends to an existing receipts branch (an open pull request) instead of starting a new one from main.

receipts.json is a list of findings: {"watch": "news-watch"|"youtube-watch", "check_time": "2026-10-08T20:07:00Z",
"coverage": "<what was read: the complete source and its kind>", "outcome": "<the finding: who holds what position on AI,
agents or alignment, in their own published words, and what it means for the project>", "limitations": ["..."],
"url": "<the original source>", "locator": "...", "published_at": "<the source's time>", "derived_from_ids": ["ev:..."],
"slug": "<a short tag, e.g. the video id, so two findings from one tick get distinct ids>"}.
Each becomes one `evidence` record of kind primary_public, authored and observed by agent:claude, under an origin_group of
its own, so a finding is never counted twice. An object without "finding": true is refused: a watch iteration that found
nothing eligible adds nothing to the model. The script fetches the testbed's main,
appends the records, bumps the patch version, validates with the testbed's validator, commits on a branch with the noreply
identity, runs the public-content check and pushes the branch. Open the pull request from the printed branch name."""
import json, os, re, subprocess, sys, datetime

args = sys.argv[1:]
testbed = "/home/user/microcredit-agent-testbed"
push = True
if "--testbed" in args:
    i = args.index("--testbed"); testbed = args[i + 1]; del args[i:i + 2]
if "--no-push" in args:
    push = False; args.remove("--no-push")
onto = None
if "--onto" in args:
    i = args.index("--onto"); onto = args[i + 1]; del args[i:i + 2]
receipts = json.load(open(args[0]))
run = lambda *c, **k: subprocess.run(c, cwd=testbed, check=True, text=True, capture_output=True, **k).stdout.strip()
run("git", "fetch", "-q", "origin", "main")
if onto:
    run("git", "checkout", "-q", onto)
else:
    run("git", "checkout", "-q", "--detach", "origin/main")
base = run("git", "rev-parse", "--short", "HEAD")
path = os.path.join(testbed, "world-model", "model.json")
m = json.load(open(path))
ids = {e["id"] for e in m["evidence"]}
now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
added = []
for r in receipts:
    if not r.get("finding"):
        raise SystemExit(f"refused: {r.get('watch')} at {r.get('check_time')} is not a finding; iteration receipts do not enter the model")
    stamp = re.sub(r"[-:]", "", r["check_time"])[:13].lower()  # yyyymmddthhmm (ids are lowercase)
    slug = re.sub(r"[^a-z0-9]+", "-", r.get("slug", "").lower()).strip("-")
    rid = f"ev:{r['watch']}-finding-{stamp}z" + (f"-{slug}" if slug else "")
    if rid in ids:
        continue
    rec = {
        "id": rid,
        "kind": "primary_public" if r.get("finding") else "internal_report",
        "url": r["url"],
        "locator": r.get("locator", ""),
        "author_id": "agent:claude",
        "observer_id": "agent:claude",
        "published_at": r.get("published_at"),
        "retrieved_at": r["check_time"],
        "summary": f"{r['watch']} iteration at {r['check_time']}: coverage {r['coverage']}. Outcome: {r['outcome']}",
        "content_sha256": None,
        "fingerprint_scope": None,
        "origin_group": rid[3:],
        "derived_from_ids": r.get("derived_from_ids", []),
        "limitations": r.get("limitations", []),
    }
    m["evidence"].append(rec); ids.add(rid); added.append(rid)
if not added:
    print("nothing new"); sys.exit(0)
major, minor, patch = m["model_version"].split(".")
m["model_version"] = f"{major}.{minor}.{int(patch) + 1}"
m["updated_at"] = now
json.dump(m, open(path, "w"), indent=2, ensure_ascii=False); open(path, "a").write("\n")
print(run("python3", "world-model/validate.py", "--check-schema"))
branch = onto or f"claude/watch-receipts-{now[:13].replace('-', '').replace('T', 't')}z"
if not onto:
    run("git", "checkout", "-q", "-b", branch)
run("git", "add", "world-model/model.json")
msg = f"World model: watch findings, {len(added)} record(s), model {m['model_version']} (base {base})\n\n" + "\n".join(added) + "\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
run("git", "-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com", "commit", "-q", "-m", msg)
subprocess.run(["/home/user/microcredit-contract/scripts/check-public-content.sh", "--range", "origin/main..HEAD"], cwd=testbed, check=True)
if push:
    run("git", "push", "-q", "-u", "origin", branch)
print("branch", branch, "version", m["model_version"], "added", added)
