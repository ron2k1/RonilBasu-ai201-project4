"""Local WSGI entry point for Provenance Guard with request instrumentation."""

import os
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter_ns, process_time_ns
from uuid import uuid4

from flask import g, request
from werkzeug.exceptions import RequestEntityTooLarge

import config
from app import app
from capstone_log import append_record
from stylometry import words

LOG_PATH = Path(os.environ.get("AI201_CAPSTONE_LOG", ".capstone/requests.jsonl"))

# Keep earlier exercise evidence intact in the default capstone run.
config.LOG_DIR = LOG_PATH.parent
config.AUDIT_LOG = LOG_PATH.parent / "capstone-audit.jsonl"


def input_word_count() -> int | None:
    """Observe the cached request without retaining text or creator ID."""
    try:
        payload = request.get_json(silent=True)
    except RequestEntityTooLarge:
        return None
    text = payload.get("text") if isinstance(payload, dict) else None
    return len(words(text.strip())) if isinstance(text, str) else None


@app.before_request
def begin_submit_record():
    if request.method == "POST" and request.path == "/submit":
        g.capstone_id = uuid4().hex
        g.capstone_start = perf_counter_ns()
        g.capstone_cpu = process_time_ns()
        g.capstone_timestamp = datetime.now(timezone.utc).isoformat(
            timespec="milliseconds"
        )


@app.after_request
def record_submit_response(response):
    request_id = getattr(g, "capstone_id", None)
    if request_id is None or getattr(g, "capstone_recorded", False):
        return response

    # Prevent a second write if Flask runs response handlers for an error.
    g.capstone_recorded = True
    payload = response.get_json(silent=True)
    payload = payload if isinstance(payload, dict) else {}
    response.headers["X-Request-ID"] = request_id

    metadata_start = perf_counter_ns()
    input_words = input_word_count()
    metadata_ms = (perf_counter_ns() - metadata_start) / 1_000_000
    event = {
        "timestamp": g.capstone_timestamp,
        "request_id": request_id,
        "route": request.path,
        "input_content_bytes": request.content_length,
        "input_words": input_words,
        "http_status": response.status_code,
        "duration_ms": round((perf_counter_ns() - g.capstone_start) / 1_000_000, 6),
        "cpu_ms": round((process_time_ns() - g.capstone_cpu) / 1_000_000, 6),
        "input_metadata_ms": round(metadata_ms, 6),
    }
    if response.status_code < 400:
        event["label"] = payload.get("label")
        event["guess"] = payload.get("guess")
    else:
        event["reason"] = payload.get("error", f"http_{response.status_code}")
    try:
        append_record(LOG_PATH, event)
    except OSError:
        app.logger.exception("Capstone request log write failed for %s", request_id)
    return response
