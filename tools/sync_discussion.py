#!/usr/bin/env python3
"""Keep the established working-group Discussion #7 in step with WORKING_GROUP.md.

GitHub Actions supplies its workflow token. Update the existing body when allowed;
otherwise add one marked revision comment. Identical retries are no-ops. Bootstrap
creation/deletion of Discussions is deliberately separate from routine upkeep.
"""
import json
import re
import subprocess

from common import ROOT

OWNER, REPO = "scottonchain", "microcredit-vision"
DISCUSSION_NUMBER = 7
BOT = "github-actions"
MARK = "<!-- charter-sync -->"


def run(step, cmd, data=None):
    out = subprocess.run(cmd, capture_output=True, text=True, input=data)
    parsed = None
    if out.stdout.strip().startswith(("{", "[")):
        try:
            parsed = json.loads(out.stdout)
        except json.JSONDecodeError:
            pass
    ok = out.returncode == 0 and not (isinstance(parsed, dict) and parsed.get("errors"))
    print(f"step {step}: {'ok' if ok else 'failed: ' + (out.stderr or out.stdout).strip()[:200]}")
    return ok, parsed


def gql(step, query, **variables):
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        cmd += ["-F" if isinstance(value, int) else "-f", f"{key}={value}"]
    return run(step, cmd)


def body_from_file():
    text = (ROOT / "WORKING_GROUP.md").read_text(encoding="utf-8")
    text = text.replace("](VERIFY.md)", f"](https://github.com/{OWNER}/{REPO}/blob/main/VERIFY.md)")
    text = text.replace("](README.md)", f"](https://github.com/{OWNER}/{REPO})")
    head = re.match(r"# Working group charter\n\n(.*?)\n\n", text, re.S)
    if not head:
        raise ValueError("WORKING_GROUP.md must start with the heading and the revision paragraph")
    pointer = (
        "**The working group's charter.** Written by Claude Code, an AI agent working with the project's human operator, "
        f"and posted by this repository's workflow from [WORKING_GROUP.md](https://github.com/{OWNER}/{REPO}/blob/main/WORKING_GROUP.md), "
        "the canonical copy. When that file changes, the workflow posts the new text as a comment here, so the newest workflow comment is the current charter. Reply below to join."
    )
    text = pointer + "\n\n" + text[head.end():]
    text = re.sub(r"^## (.+)$", r"**\1.**", text, flags=re.M)
    text = re.sub(r"\[Discussion \d+\]\(https://github.com/scottonchain/microcredit-vision/discussions/\d+\)", "this thread", text)
    return MARK + "\n" + text.rstrip("\n") + "\n\nReply below with a role and a first task.\n"


def revision_body(want):
    return want.replace("Reply below to join.", "This is the current charter, revised since the opening post.")


def is_current(discussion, want):
    if discussion["body"].strip() == want.strip():
        return True
    comments = [c["body"] for c in discussion["comments"]["nodes"]
                if MARK in c["body"] and (c.get("author") or {}).get("login", "").casefold() in {BOT, BOT + "[bot]"}]
    return bool(comments) and comments[-1].strip() in {want.strip(), revision_body(want).strip()}


def main():
    ok, result = gql("read charter discussion", """query($owner:String!,$repo:String!,$number:Int!){
      repository(owner:$owner,name:$repo){ discussion(number:$number){ id number body author{login}
        comments(last:100){ nodes{body author{login}} } } } }""",
                    owner=OWNER, repo=REPO, number=DISCUSSION_NUMBER)
    if not ok:
        raise SystemExit(1)
    discussion = result["data"]["repository"]["discussion"]
    if discussion is None:
        raise SystemExit(f"charter Discussion #{DISCUSSION_NUMBER} is unavailable; no replacement thread was created")
    want = body_from_file()
    if is_current(discussion, want):
        print(f"discussion #{DISCUSSION_NUMBER} already current")
        return
    ok, _ = run("rest patch body", ["gh", "api", "-X", "PATCH", f"repos/{OWNER}/{REPO}/discussions/{DISCUSSION_NUMBER}", "--input", "-"], json.dumps({"body": want}))
    if not ok:
        ok, _ = gql("update body", """mutation($id:ID!,$body:String!){
          updateDiscussion(input:{discussionId:$id,body:$body}){discussion{updatedAt}} }""", id=discussion["id"], body=want)
    if not ok:
        ok, _ = gql("post revision as comment", """mutation($id:ID!,$body:String!){
          addDiscussionComment(input:{discussionId:$id,body:$body}){comment{url}} }""", id=discussion["id"], body=revision_body(want))
    if not ok:
        raise SystemExit(1)
    print(f"DISCUSSION_NUMBER={DISCUSSION_NUMBER}")


if __name__ == "__main__":
    main()
