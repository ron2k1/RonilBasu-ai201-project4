"""Append-only operational records, separate from the moderation audit."""

import json
from pathlib import Path
from threading import Lock

_lock = Lock()


def append_record(path: Path, record: dict) -> None:
    """Write and close one UTF-8 JSONL record under the local worker's lock."""
    line = json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n"
    with _lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as stream:
            stream.write(line)
