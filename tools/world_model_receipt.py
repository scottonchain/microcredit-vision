"""Add watch-iteration receipts to the team world model (CLAUDE.md "Watch findings enter the world model", operator direction 2026-10-08).

Usage: python3 tools/world_model_receipt.py <receipts.json> [--testbed /home/user/microcredit-agent-testbed] [--no-push]

receipts.json is a list of objects: {"watch": "news-watch"|"youtube-watch", "check_time": "2026-10-08T20:07:00Z",
"coverage": "...", "outcome": "...", "limitations": ["..."], "url": "<public record of the iteration>", "locator": "...",
"published_at": "<event or release time or null>", "derived_from_ids": ["ev:..."]}. Each becomes one `evidence` record of kind
internal_report (a receipt) or primary_public (a finding with a source URL), authored and observed by agent:claude, under an
origin_group of its own, so no receipt is counted as independent evidence of anything. The script fetches the testbed's main,
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
receipts = json.load(open(args[0]))
run = lambda *c, **k: subprocess.run(c, cwd=testbed, check=True, text=True, capture_output=True, **k).stdout.strip()
run("git", "fetch", "-q", "origin", "main")
run("git", "checkout", "-q", "--detach", "origin/main")
base = run("git", "rev-parse", "--short", "HEAD")
path = os.path.join(testbed, "world-model", "model.json")
m = json.load(open(path))
ids = {e["id"] for e in m["evidence"]}
now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
added = []
for r in receipts:
    stamp = re.sub(r"[-:]", "", r["check_time"])[:13].lower()  # yyyymmddthhmm (ids are lowercase)
    rid = f"ev:{r['watch']}-{'finding' if r.get('finding') else 'receipt'}-{stamp}z"
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
branch = f"claude/watch-receipts-{now[:13].replace('-', '').replace('T', 't')}z"
run("git", "checkout", "-q", "-b", branch)
run("git", "add", "world-model/model.json")
msg = f"World model: watch-iteration receipts, {len(added)} record(s), model {m['model_version']} (base {base})\n\n" + "\n".join(added) + "\n\nCo-Authored-By: Claude <noreply@anthropic.com>"
run("git", "-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com", "commit", "-q", "-m", msg)
subprocess.run(["/home/user/microcredit-contract/scripts/check-public-content.sh", "--range", "origin/main..HEAD"], cwd=testbed, check=True)
if push:
    run("git", "push", "-q", "-u", "origin", branch)
print("branch", branch, "version", m["model_version"], "added", added)
