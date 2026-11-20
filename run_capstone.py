#!/usr/bin/env python3
"""Run three trials per locked criterion against real local worker processes."""

import argparse
import json
import math
import os
from contextlib import contextmanager
from pathlib import Path
import socket
import statistics
import subprocess
import sys
from tempfile import TemporaryDirectory
import time
from uuid import uuid4

import requests

ROOT = Path(__file__).resolve().parent
MIN_WORDS = 30
FIXTURES = (
    "At the library I moved my notes away from the window because the afternoon light made the diagram hard to read. When I returned after dinner, a student had left a forgotten blue scarf on the bench near the elevator. I took it to the circulation desk before walking back to the bus.",
    "A reproducible experiment uses the same inputs and documents the exact sequence of operations. The results should identify which measurements came from an actual run and which values were selected beforehand. Reporting uncertainty makes it easier for a reader to use those measurements without mistaking them for promises.",
    "We tried the old route first, the one that cuts behind the brick building toward the garden. It was muddy. My brother took the long way around to keep his shoes clean. By the time we reached the gate he was laughing, because the shortcut had put me several minutes behind him.",
)
BAD = (
    ("malformed", 400, "invalid_json"),
    ("missing", 400, "missing_text"),
    ("short", 422, "text_too_short"),
)


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@contextmanager
def server(workdir, module, run_dir, log_path):
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    env = dict(os.environ, AI201_CAPSTONE_LOG=str(log_path),
               OMP_NUM_THREADS="1", MKL_NUM_THREADS="1",
               TOKENIZERS_PARALLELISM="false",
               AI201_DETECTOR_MODEL=os.environ.get("AI201_DETECTOR_MODEL", "gpt2"))
    console = run_dir / f"{module}-{port}.txt"
    with console.open("wb") as output:
        process = subprocess.Popen(
            [sys.executable, "-m", "gunicorn", "--workers", "1",
             "--bind", f"127.0.0.1:{port}", "--timeout", "180", f"{module}:app"],
            cwd=workdir, env=env, stdout=output, stderr=subprocess.STDOUT,
        )
        try:
            for _ in range(120):
                if process.poll() is not None:
                    raise RuntimeError(console.read_text(errors="replace"))
                try:
                    if requests.get(base + "/health", timeout=1).ok:
                        break
                except requests.RequestException:
                    pass
                time.sleep(0.25)
            else:
                raise RuntimeError("Worker never opened the health route")
            yield base
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


def records(path):
    return [json.loads(s) for s in path.read_text().splitlines()] if path.exists() else []


def submit(base, index=0, creator=None, bad=None):
    identity = creator or "capstone-demo-" + uuid4().hex
    if bad == "malformed":
        response = requests.post(base + "/submit", data="{", timeout=175,
                                 headers={"Content-Type": "application/json"})
    else:
        payload = {"creator_id": identity}
        if bad != "missing":
            payload["text"] = "Too short." if bad == "short" else FIXTURES[index % 3]
        response = requests.post(base + "/submit", json=payload, timeout=175)
    try:
        body = response.json()
    except requests.exceptions.JSONDecodeError:
        body = {}
    return {"request_id": response.headers.get("X-Request-ID"),
            "http_status": response.status_code, "label": body.get("label"),
            "guess": body.get("guess"), "confidence": body.get("confidence"),
            "error": body.get("error")}


def warm(base):
    result = submit(base)
    if result["http_status"] != 200:
        raise RuntimeError(f"Cannot score a real fixture: {result!r}")


def matched(rows, request_id):
    return [row for row in rows if row["request_id"] == request_id]


def valid_record(row):
    required = {"timestamp", "request_id", "input_words", "http_status",
                "label", "duration_ms"}
    return (required <= row.keys() and row["timestamp"].endswith("+00:00")
            and bool(row["request_id"]) and isinstance(row["input_words"], int)
            and row["input_words"] >= MIN_WORDS and row["http_status"] == 200
            and bool(row["label"]) and row["duration_ms"] >= 0)


def trial(n, target, sample):
    return {"observed": n, "target": target, "met": n == target, "sample": sample}


def evaluate(baseline_dir, run_dir, path):
    rows = {str(i): [] for i in range(1, 6)}
    cost_rows = []
    with server(ROOT, "capstone_service", run_dir, path) as current, server(
        baseline_dir, "app", run_dir, path
    ) as baseline:
        warm(current)
        warm(baseline)
        for repeat in range(3):
            start = len(records(path))
            valid = [submit(current, k) for k in range(10)]
            fresh = records(path)[start:]
            observed = sum(valid_record(row) for row in fresh)
            if len(fresh) != 10 or not all(r["http_status"] == 200 for r in valid):
                observed = -1
            rows["1"].append(trial(observed, 10, fresh[:1]))
            if repeat == 0:
                cost_rows = fresh[:]

            responses = [submit(current, k) for k in range(5)]
            ids = [res["request_id"] for res in responses]
            log = records(path)
            ok = 0
            for res in responses:
                hits = matched(log, res["request_id"])
                if (res["request_id"] and ids.count(res["request_id"]) == 1
                    and len(hits) == 1 and res["http_status"] == hits[0]["http_status"] == 200
                    and res["label"] == hits[0]["label"]):
                    ok += 1
            rows["2"].append(trial(ok, 5, {"response": responses[0],
                                               "log": matched(log, ids[0])}))

            failure_sample = []
            for kind, status, reason in BAD:
                res = submit(current, bad=kind)
                hits = matched(records(path), res["request_id"])
                good = (res["http_status"] == status and res["error"] == reason
                        and res["request_id"] and len(hits) == 1
                        and hits[0]["http_status"] == status and hits[0]["reason"] == reason
                        and "label" not in hits[0] and hits[0]["duration_ms"] >= 0)
                failure_sample.append({"response": res, "log": hits, "ok": bool(good)})
            rows["3"].append(trial(sum(f["ok"] for f in failure_sample), 3,
                                         failure_sample))

            pair_sample = []
            for k in range(3):
                old, new = submit(baseline, k), submit(current, k)
                good = (old["http_status"] == new["http_status"] == 200
                        and old["label"] == new["label"] and old["guess"] == new["guess"]
                        and isinstance(old["confidence"], (int, float))
                        and isinstance(new["confidence"], (int, float))
                        and math.isclose(old["confidence"], new["confidence"],
                                         rel_tol=0.0, abs_tol=0.000001))
                pair_sample.append({"fixture": k + 1, "unit_8": old,
                                    "capstone": new, "ok": good})
            rows["5"].append(trial(sum(s["ok"] for s in pair_sample), 3, pair_sample))

        # Exercise the ordinary documented 429 path without changing the limit.
        creator = "capstone-rate-limit-control"
        limit_responses = [submit(current, k, creator=creator) for k in range(6)]
        rejected = limit_responses[-1]
        limit_check = {"status_sequence": [s["http_status"] for s in limit_responses],
                       "last_response": rejected,
                       "log": matched(records(path), rejected["request_id"])}

    for _ in range(3):
        with server(ROOT, "capstone_service", run_dir, path) as current:
            first = [submit(current, 0), submit(current, 1)]
        with server(ROOT, "capstone_service", run_dir, path) as current:
            last = submit(current, 2)
        responses = first + [last]
        ids = [res["request_id"] for res in responses]
        log = records(path)
        ok = sum(bool(res["request_id"] and res["http_status"] == 200
                      and ids.count(res["request_id"]) == 1
                      and len(matched(log, res["request_id"])) == 1)
                 for res in responses)
        rows["4"].append(trial(ok, 3, {"responses": responses,
                                           "log": [r for r in log if r["request_id"] in ids]}))

    for check in rows.values():
        if len(check) != 3:
            raise RuntimeError("Expected exactly three trials per criterion")
    if len(cost_rows) != 10 or not all(valid_record(r) for r in cost_rows):
        raise RuntimeError("The ten-request warm cost sample was incomplete")
    evidence = {"model": os.environ.get("AI201_DETECTOR_MODEL", "gpt2"),
                "criteria": rows, "rate_limit_control": limit_check,
                "cost_sample": cost_rows,
                "mean_cpu_seconds": statistics.mean(r["cpu_ms"] for r in cost_rows) / 1000,
                "mean_wall_seconds": statistics.mean(r["duration_ms"] for r in cost_rows) / 1000}
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True,
                        help="disposable clean checkout of Unit 8")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    log_path = (args.output / "requests.jsonl").resolve()
    with TemporaryDirectory(prefix="ai201-capstone-runs-") as directory:
        result = evaluate(args.baseline.resolve(), Path(directory), log_path)
    (args.output / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"trials": {k: [r["observed"] for r in v]
                                  for k, v in result["criteria"].items()},
                      "rate_limit_control": result["rate_limit_control"],
                      "mean_cpu_seconds": result["mean_cpu_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
