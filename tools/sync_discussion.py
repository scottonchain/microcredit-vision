#!/usr/bin/env python3
"""Keep the working-group Discussion in step with WORKING_GROUP.md.

Runs in GitHub Actions (see .github/workflows/sync-working-group.yml) with the workflow token,
which may edit this repository's Discussions. It rewrites the opening post of Discussion 3 from
WORKING_GROUP.md and prepends a "superseded" line to the two 2026-10-04 task comments. Idempotent:
nothing is written when the text already matches.
"""
import json
import os
import re
import subprocess
import sys

OWNER, REPO, NUMBER = "scottonchain", "microcredit-vision", 3
SUPERSEDED_IDS = {18739335, 18739608}
SUPERSEDED_LINE = "Superseded on 2026-10-06 by the charter above; kept for the record.\n\n"


def gql(query, **variables):
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        cmd += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        print(out.stderr or out.stdout, file=sys.stderr)
        raise SystemExit(out.returncode)
    return json.loads(out.stdout)


def body_from_file():
    t = open("WORKING_GROUP.md", encoding="utf-8").read()
    t = t.replace("](VERIFY.md)", f"](https://github.com/{OWNER}/{REPO}/blob/main/VERIFY.md)")
    t = t.replace("](README.md)", f"](https://github.com/{OWNER}/{REPO})")
    head = re.match(r"# Working group charter\n\n(.*?)\n\n", t, re.S)
    assert head, "WORKING_GROUP.md must start with the heading and the revision paragraph"
    pointer = (
        "**Charter, revised 2026-10-06 by Claude Code** (an AI agent working with the project's human operator). "
        f"The canonical copy is [WORKING_GROUP.md](https://github.com/{OWNER}/{REPO}/blob/main/WORKING_GROUP.md) in this repository, "
        "and this post is updated from it automatically; the first version of 2026-10-04 is in its history. "
        'The two comments below carried the first task list and are superseded by the "Open tasks" section here.'
    )
    t = pointer + "\n\n" + t[head.end():]
    t = re.sub(r"^## (.+)$", r"**\1.**", t, flags=re.M)
    return t.rstrip("\n") + "\n\nReply below with a role and a first task.\n"


def main():
    q = """query($owner:String!,$repo:String!,$n:Int!){ repository(owner:$owner,name:$repo){ discussion(number:$n){
            id body comments(first:20){ nodes { id databaseId body } } } } }"""
    d = gql(q, owner=OWNER, repo=REPO, n=NUMBER)["data"]["repository"]["discussion"]
    want = body_from_file()
    if d["body"].strip() != want.strip():
        gql("""mutation($id:ID!,$body:String!){ updateDiscussion(input:{discussionId:$id, body:$body}){ discussion { updatedAt } } }""",
            id=d["id"], body=want)
        print("discussion body updated")
    else:
        print("discussion body already current")
    for c in d["comments"]["nodes"]:
        if c["databaseId"] in SUPERSEDED_IDS and not c["body"].startswith(SUPERSEDED_LINE.strip()):
            gql("""mutation($id:ID!,$body:String!){ updateDiscussionComment(input:{commentId:$id, body:$body}){ comment { updatedAt } } }""",
                id=c["id"], body=SUPERSEDED_LINE + c["body"])
            print(f"comment {c['databaseId']} marked superseded")


if __name__ == "__main__":
    if not os.environ.get("GH_TOKEN"):
        raise SystemExit("GH_TOKEN is not set; this script runs in GitHub Actions")
    main()
