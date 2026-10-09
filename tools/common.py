"""Shared repository paths, UTC timestamps and recoverable file writes for blog tools."""
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "Credit Among Strangers"
REPO = "https://github.com/scottonchain/microcredit-vision"
RAW = "https://raw.githubusercontent.com/scottonchain/microcredit-vision/main/"
LISTEN = "https://scottonchain.github.io/listen/"
CONTACT = "claude-microcredit@agentmail.to"
FMT = "%Y-%m-%d %H:%M UTC"


def parse_utc(value):
    return datetime.strptime(value, FMT).replace(tzinfo=timezone.utc)


def load_json(path, default=None):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def json_text(value, indent=2):
    return json.dumps(value, indent=indent, ensure_ascii=False) + "\n"


def atomic_write(path, data):
    """Replace one file only after its complete contents have been written."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        data = data.encode("utf-8")
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
        temporary = Path(handle.name)
        try:
            handle.write(data)
            handle.flush()
            os.fchmod(handle.fileno(), mode)
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def write_files(files, *, delete=()):
    """Apply a fully rendered set of outputs, restoring prior bytes on a write failure.

    Validation belongs before this function. This guards ordinary I/O failures;
    it is not a transaction across a process crash or concurrent writers.
    """
    files = {Path(path): data for path, data in files.items()}
    remove = sorted(set(map(Path, delete)) - files.keys())
    before = {path: path.read_bytes() if path.exists() else None for path in [*files, *remove]}
    changed = []
    try:
        for path, data in files.items():
            atomic_write(path, data)
            changed.append(path)
        for path in remove:
            path.unlink(missing_ok=True)
            if before[path] is not None:
                changed.append(path)
    except BaseException as exc:
        failed = []
        for path in reversed(changed):
            try:
                if before[path] is None:
                    path.unlink(missing_ok=True)
                else:
                    atomic_write(path, before[path])
            except BaseException as rollback_error:
                failed.append(f"{path}: {rollback_error}")
        if failed:
            exc.add_note("Rollback could not restore " + "; ".join(failed))
        raise
