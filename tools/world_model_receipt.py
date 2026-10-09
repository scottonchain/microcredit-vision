#!/usr/bin/env python3
"""Prepare eligible watch findings for the canonical world-model review workflow.

    python3 tools/world_model_receipt.py findings.json --check
    python3 tools/world_model_receipt.py findings.json --output /tmp/model-candidate.json

The default testbed is the sibling microcredit-agent-testbed checkout; override it
with --testbed. This tool does not fetch, switch branches, commit, push or overwrite
world-model/model.json. Apply the validated candidate through that repository's
world-model/README.md protocol after reviewing its diff against the source model.

Each finding supplies finding: true, watch (news-watch or youtube-watch), check_time,
coverage, outcome, url, locator, published_at, author_id and observer_id. The author
is the source's actual entity in the model, never implicitly the observing agent.
Optional derived_from_ids identifies mirrors: they inherit the original's origin
group. Re-reading the same finding does not create another evidence record. Related
findings from one original source share its origin group. Source completeness,
relevance and the political-content exclusion still require editorial judgment.

Legacy --onto and --no-push are rejected before any writes: Git lifecycle management
belongs to the canonical review workflow, not this preparation tool.
"""
import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from common import ROOT, atomic_write, json_text


def source_url(url):
    parts = urlsplit(url)
    if parts.scheme not in ("https", "http") or not parts.netloc or parts.username or parts.password:
        raise ValueError("findings require an original public http(s) source URL")
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path, parts.query, ""))


def finding_key(record):
    outcome = record.get("outcome", record.get("summary", ""))
    # Recognize receipts created by the old script without rewriting their history.
    if " iteration at " in outcome and ". Outcome: " in outcome:
        outcome = outcome.split(". Outcome: ", 1)[1]
    return (source_url(record["url"]), record.get("locator", ""), record.get("published_at"), outcome.strip())


def prepare_model(model, receipts, now=None):
    """Return a candidate and the added IDs. Inputs are never mutated."""
    if not isinstance(receipts, list):
        raise ValueError("findings.json must be a list")
    candidate = copy.deepcopy(model)
    evidence = candidate["evidence"]
    entities = {e["id"] for e in candidate["entities"]}
    by_id = {e["id"]: e for e in evidence}
    keys = {finding_key(e) for e in evidence if e.get("url", "").startswith(("https://", "http://"))}
    added = []
    for receipt in receipts:
        if receipt.get("finding") is not True:
            raise ValueError("only finding: true is accepted; empty watch iterations do not enter the model")
        if receipt.get("watch") not in ("news-watch", "youtube-watch"):
            raise ValueError("watch must be news-watch or youtube-watch")
        for field in ("check_time", "coverage", "outcome", "url", "published_at", "author_id", "observer_id"):
            if not isinstance(receipt.get(field), str) or not receipt[field].strip():
                raise ValueError(f"finding requires {field}; source attribution is never inferred")
        for field in ("author_id", "observer_id"):
            if receipt[field] not in entities:
                raise ValueError(f"{field} {receipt[field]!r} is not an entity in the model")
        key = finding_key(receipt)
        if key in keys:
            continue
        derived = receipt.get("derived_from_ids", [])
        if not isinstance(derived, list) or any(i not in by_id for i in derived):
            raise ValueError("derived_from_ids must identify existing evidence")
        source = (key[0], key[2])
        origins = ({by_id[i]["origin_group"] for i in derived} if derived else
                   {e["origin_group"] for e in evidence if e.get("url", "").startswith(("https://", "http://"))
                    and (source_url(e["url"]), e.get("published_at")) == source})
        if len(origins) > 1:
            raise ValueError("the source has conflicting origin groups; reconcile them in model review first")
        origin = next(iter(origins), "source-" + hashlib.sha256(json.dumps(source).encode()).hexdigest()[:16])
        digest = hashlib.sha256(json.dumps(key, ensure_ascii=False).encode()).hexdigest()[:16]
        ident = f"ev:{receipt['watch']}-finding-{digest}"
        if ident in by_id:
            raise ValueError(f"evidence ID collision: {ident}")
        record = {
            "id": ident, "kind": "mirror" if derived else "primary_public",
            "url": receipt["url"], "locator": receipt.get("locator", ""),
            "author_id": receipt["author_id"], "observer_id": receipt["observer_id"],
            "published_at": receipt["published_at"], "retrieved_at": receipt["check_time"],
            "summary": receipt["outcome"].strip(), "content_sha256": receipt.get("content_sha256"),
            "fingerprint_scope": receipt.get("fingerprint_scope"), "origin_group": origin,
            "derived_from_ids": derived,
            "limitations": [*receipt.get("limitations", []), f"Observer-reported coverage: {receipt['coverage']}"],
        }
        evidence.append(record)
        keys.add(key)
        by_id[ident] = record
        added.append(ident)
    if added:
        version = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", candidate["model_version"])
        if version is None:
            raise ValueError("model_version must have major.minor.patch form")
        major, minor, patch = version.groups()
        candidate["model_version"] = f"{major}.{minor}.{int(patch) + 1}"
        candidate["updated_at"] = (now or datetime.now(timezone.utc)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return candidate, added


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    argv = list(sys.argv[1:] if argv is None else argv)
    if any(arg.split("=", 1)[0] in ("--onto", "--no-push") for arg in argv):
        parser.error("Git options were removed; use --output CANDIDATE or --check, then follow world-model/README.md")
    parser.add_argument("findings", type=Path)
    parser.add_argument("--testbed", type=Path, default=ROOT.parent / "microcredit-agent-testbed")
    output = parser.add_mutually_exclusive_group(required=True)
    output.add_argument("--output", type=Path)
    output.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    testbed = args.testbed.resolve()
    model_path = testbed / "world-model/model.json"
    if args.output and args.output.resolve() in (model_path, args.findings.resolve()):
        parser.error("--output must be a separate candidate file, not the canonical model or input findings")
    model = json.loads(model_path.read_text(encoding="utf-8"))
    receipts = json.loads(args.findings.read_text(encoding="utf-8"))
    try:
        candidate, added = prepare_model(model, receipts)
    except ValueError as exc:
        parser.error(str(exc))
    text = json_text(candidate)
    # Validation uses the canonical implementation; no duplicate schema or Git lifecycle here.
    with tempfile.TemporaryDirectory(prefix="watch-findings-") as temporary:
        path = Path(temporary) / "model.json"
        path.write_text(text, encoding="utf-8")
        subprocess.run([sys.executable, str(testbed / "world-model/validate.py"), str(path), "--check-schema", "--format"], check=True)
        subprocess.run(["bash", str(testbed / "world-model/check-public-content.sh"), "--text", str(path)], cwd=testbed, check=True)
        text = path.read_text(encoding="utf-8")
    if args.output:
        atomic_write(args.output, text)
    print(f"validated {len(added)} new finding(s), model {candidate['model_version']}; canonical model unchanged")
    if args.output:
        print(f"candidate: {args.output}; review and apply through world-model/README.md")


if __name__ == "__main__":
    main()
