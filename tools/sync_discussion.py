#!/usr/bin/env python3
"""Keep the working-group Discussion in step with WORKING_GROUP.md.

Runs in GitHub Actions (.github/workflows/sync-working-group.yml) with the workflow token. Observed
limits of that token: it can create a Discussion and add comments, but GraphQL updateDiscussion is
refused even on a Discussion it authored. So the thread is created with the full charter as its body,
and each later revision of WORKING_GROUP.md is posted as a new comment on the thread by the workflow
(the newest comment is the current text), unless a write route for the body is available, which the
script tries first. The original thread (Discussion 3, 2026-10-04) gets one pointer comment. Idempotent.
"""
import json
import re
import subprocess
import sys

OWNER, REPO = "scottonchain", "microcredit-vision"
TITLE = "Working group: charter, roles, open tasks"
OLD_NUMBER = 3
BOT = "github-actions"
MARK = "<!-- charter-sync -->"


def run(step, cmd, data=None):
    out = subprocess.run(cmd, capture_output=True, text=True, input=data)
    ok = out.returncode == 0
    print(f"step {step}: {'ok' if ok else 'failed: ' + (out.stderr or out.stdout).strip()[:200]}")
    return ok, (json.loads(out.stdout) if ok and out.stdout.strip().startswith(("{", "[")) else None)


def gql(step, query, **variables):
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        cmd += ["-F" if isinstance(v, int) else "-f", f"{k}={v}"]
    return run(step, cmd)


def body_from_file():
    t = open("WORKING_GROUP.md", encoding="utf-8").read()
    t = t.replace("](VERIFY.md)", f"](https://github.com/{OWNER}/{REPO}/blob/main/VERIFY.md)")
    t = t.replace("](README.md)", f"](https://github.com/{OWNER}/{REPO})")
    head = re.match(r"# Working group charter\n\n(.*?)\n\n", t, re.S)
    assert head, "WORKING_GROUP.md must start with the heading and the revision paragraph"
    pointer = (
        "**The working group's charter.** Written by Claude Code, an AI agent working with the project's human operator, "
        f"and posted by this repository's workflow from [WORKING_GROUP.md](https://github.com/{OWNER}/{REPO}/blob/main/WORKING_GROUP.md), "
        "the canonical copy. When that file changes, the workflow posts the new text as a comment here, so the newest workflow comment is the current charter. Reply below to join."
    )
    t = pointer + "\n\n" + t[head.end():]
    t = re.sub(r"^## (.+)$", r"**\1.**", t, flags=re.M)
    t = re.sub(r"\[Discussion \d+\]\(https://github.com/scottonchain/microcredit-vision/discussions/\d+\)", "this thread", t)
    return MARK + "\n" + t.rstrip("\n") + "\n\nReply below with a role and a first task.\n"


def main():
    ok, r = gql("read repository", """query($owner:String!,$repo:String!){ repository(owner:$owner,name:$repo){ id
        discussionCategories(first:10){ nodes { id name } }
        discussions(first:50, orderBy:{field:CREATED_AT, direction:DESC}){ nodes { id number title body author { login }
          comments(first:100){ nodes { id body author { login } } } } } } }""", owner=OWNER, repo=REPO)
    if not ok:
        raise SystemExit(1)
    repo = r["data"]["repository"]
    want = body_from_file()
    mine = [d for d in repo["discussions"]["nodes"] if d["title"] == TITLE and d["author"] and d["author"]["login"].startswith(BOT)]
    # a half-made thread (body never written) is removed if the token allows, else left and superseded
    for d in list(mine):
        if MARK not in d["body"] and not any(MARK in c["body"] for c in d["comments"]["nodes"]):
            ok, _ = gql("delete half-made discussion", """mutation($id:ID!){ deleteDiscussion(input:{id:$id}){ clientMutationId } }""", id=d["id"])
            if ok:
                mine.remove(d)
    if not mine:
        cat = next(c["id"] for c in repo["discussionCategories"]["nodes"] if c["name"] == "General")
        ok, r = gql("create discussion", """mutation($r:ID!,$c:ID!,$t:String!,$b:String!){ createDiscussion(input:{repositoryId:$r, categoryId:$c, title:$t, body:$b}){ discussion { id number body } } }""",
                    r=repo["id"], c=cat, t=TITLE, b=want)
        if not ok:
            raise SystemExit(1)
        d = r["data"]["createDiscussion"]["discussion"]
        d["comments"] = {"nodes": []}
        print(f"created discussion #{d['number']} with the charter as its body")
    else:
        d = mine[0]
        current = [c["body"] for c in d["comments"]["nodes"] if MARK in c["body"]]
        latest = current[-1] if current else d["body"]
        if latest.strip() != want.strip():
            ok, _ = run("rest patch body", ["gh", "api", "-X", "PATCH", f"repos/{OWNER}/{REPO}/discussions/{d['number']}", "--input", "-"], json.dumps({"body": want}))
            if not ok:
                ok, _ = gql("update body", """mutation($id:ID!,$body:String!){ updateDiscussion(input:{discussionId:$id, body:$body}){ discussion { updatedAt } } }""", id=d["id"], body=want)
            if not ok:
                ok, _ = gql("post revision as comment", """mutation($id:ID!,$body:String!){ addDiscussionComment(input:{discussionId:$id, body:$body}){ comment { url } } }""",
                            id=d["id"], body=want.replace("Reply below to join.", "This is the current charter, revised since the opening post."))
            if not ok:
                raise SystemExit(1)
        else:
            print(f"discussion #{d['number']} already current")
    old = next((x for x in repo["discussions"]["nodes"] if x["number"] == OLD_NUMBER), None)
    if old and not any(c["author"] and c["author"]["login"].startswith(BOT) for c in old["comments"]["nodes"]):
        note = (f"The working group's charter and its open tasks now live in Discussion #{d['number']}, kept in step with "
                f"[WORKING_GROUP.md](https://github.com/{OWNER}/{REPO}/blob/main/WORKING_GROUP.md) by this repository's workflow. Please reply there. "
                "Posted by the workflow on behalf of Claude Code, an AI agent working with the project's human operator.")
        gql("note on old thread", """mutation($id:ID!,$body:String!){ addDiscussionComment(input:{discussionId:$id, body:$body}){ comment { url } } }""", id=old["id"], body=note)
    print(f"DISCUSSION_NUMBER={d['number']}")


if __name__ == "__main__":
    main()
