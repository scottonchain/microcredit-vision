#!/usr/bin/env python3
"""Keep the working-group Discussion in step with WORKING_GROUP.md.

Runs in GitHub Actions (.github/workflows/sync-working-group.yml) with the workflow token. That token
can create a Discussion and edit the ones it authored, but not posts other accounts wrote. So the
charter thread is a Discussion created by the workflow itself (title TITLE, category General) and
rewritten from WORKING_GROUP.md on every change. The first time it runs it also leaves one comment on
the original thread (Discussion 3, 2026-10-04) saying where the charter moved. Idempotent.
"""
import json
import re
import subprocess
import sys

OWNER, REPO = "scottonchain", "microcredit-vision"
TITLE = "Working group: charter, roles, open tasks"
OLD_NUMBER = 3
BOT = "github-actions"


def gql(step, query, **variables):
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        cmd += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    out = subprocess.run(cmd, capture_output=True, text=True)
    if out.returncode != 0:
        print(f"step {step} failed: {(out.stderr or out.stdout).strip()}", file=sys.stderr)
        raise SystemExit(out.returncode)
    print(f"step {step} ok")
    return json.loads(out.stdout)


def body_from_file(number):
    t = open("WORKING_GROUP.md", encoding="utf-8").read()
    t = t.replace("](VERIFY.md)", f"](https://github.com/{OWNER}/{REPO}/blob/main/VERIFY.md)")
    t = t.replace("](README.md)", f"](https://github.com/{OWNER}/{REPO})")
    t = re.sub(r"https://github.com/scottonchain/microcredit-vision/discussions/\d+", "this thread", t)
    head = re.match(r"# Working group charter\n\n(.*?)\n\n", t, re.S)
    assert head, "WORKING_GROUP.md must start with the heading and the revision paragraph"
    pointer = (
        "**The working group's charter.** Written by Claude Code, an AI agent working with the project's human operator, "
        f"and posted by this repository's workflow, which rewrites it whenever [WORKING_GROUP.md](https://github.com/{OWNER}/{REPO}/blob/main/WORKING_GROUP.md) changes. "
        "That file is the canonical copy; its history shows every revision. Reply below to join."
    )
    t = pointer + "\n\n" + t[head.end():]
    t = re.sub(r"^## (.+)$", r"**\1.**", t, flags=re.M)
    t = t.replace("[this thread](this thread)", "this thread").replace("[Discussion 3](this thread)", "this thread")
    return t.rstrip("\n") + "\n\nReply below with a role and a first task.\n"


def main():
    repo = gql("read repository", """query($owner:String!,$repo:String!){ repository(owner:$owner,name:$repo){ id
        discussionCategories(first:10){ nodes { id name } }
        discussions(first:50, orderBy:{field:CREATED_AT, direction:DESC}){ nodes { id number title body author { login } } } } }""",
        owner=OWNER, repo=REPO)["data"]["repository"]
    mine = [d for d in repo["discussions"]["nodes"] if d["title"] == TITLE and d["author"] and d["author"]["login"].startswith(BOT)]
    if mine:
        d = mine[0]
    else:
        cat = next(c["id"] for c in repo["discussionCategories"]["nodes"] if c["name"] == "General")
        d = gql("create discussion", """mutation($r:ID!,$c:ID!,$t:String!,$b:String!){ createDiscussion(input:{repositoryId:$r, categoryId:$c, title:$t, body:$b}){ discussion { id number body } } }""",
                r=repo["id"], c=cat, t=TITLE, b="(being written)")["data"]["createDiscussion"]["discussion"]
        print(f"created discussion #{d['number']}")
    want = body_from_file(d["number"])
    if d["body"].strip() != want.strip():
        gql("update discussion", """mutation($id:ID!,$body:String!){ updateDiscussion(input:{discussionId:$id, body:$body}){ discussion { updatedAt } } }""", id=d["id"], body=want)
        print(f"discussion #{d['number']} body updated")
    else:
        print(f"discussion #{d['number']} body already current")
    old = next((x for x in repo["discussions"]["nodes"] if x["number"] == OLD_NUMBER), None)
    if old:
        c = gql("read old thread", """query($owner:String!,$repo:String!,$n:Int!){ repository(owner:$owner,name:$repo){ discussion(number:$n){ comments(first:50){ nodes { author { login } } } } } }""",
                owner=OWNER, repo=REPO, n=OLD_NUMBER)["data"]["repository"]["discussion"]["comments"]["nodes"]
        if not any(x["author"] and x["author"]["login"].startswith(BOT) for x in c):
            note = (f"The working group's charter and its open tasks now live in Discussion #{d['number']}, which this repository's workflow keeps "
                    f"in step with [WORKING_GROUP.md](https://github.com/{OWNER}/{REPO}/blob/main/WORKING_GROUP.md). Please reply there. "
                    "Posted by the repository's workflow on behalf of Claude Code, an AI agent working with the project's human operator.")
            gql("note on old thread", """mutation($id:ID!,$body:String!){ addDiscussionComment(input:{discussionId:$id, body:$body}){ comment { url } } }""", id=old["id"], body=note)
    print(f"DISCUSSION_NUMBER={d['number']}")


if __name__ == "__main__":
    main()
