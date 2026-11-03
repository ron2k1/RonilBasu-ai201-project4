#!/usr/bin/env python3
"""
Run your five criteria three times each.  <- UNIT 8, MILESTONE 3

    python app.py                              # in one terminal
    python run_eval.py --label before          # in another
    python run_eval.py --label after

The attack set tests what staff thought to test. This tests what *you* thought
to test, and the two rarely overlap much. Both count.

Fill in `scenarios.py` first — that's where you say what each criterion needs
run against it. A criterion about false positives needs your own writing. One
about label coverage needs inputs across the score range.

!! Three trials, and **your first signal runs a model, so identical input can
score differently twice.** That's exactly why repeats matter here.

This does the sending and the recording. It does not decide whether a trial
passed — that depends on the criterion you wrote, so the Verdict column comes
back blank.
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import config

# Windows consoles often run a codepage that can't print every character in
# this file's help text. Without this, `--help` ends in a UnicodeEncodeError
# traceback instead of the help — which is a miserable first thing to hit.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):  # not a normal text stream
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"


def bodies_for(scenario):
    """
    The request bodies one scenario sends.

    A "texts" scenario gets a creator_id made up for it. A "bodies" scenario is
    sent exactly as written, which is how a bad-input criterion says things a
    string can't — no `text` field, a null, something enormous.
    """
    if scenario.get("bodies"):
        return list(scenario["bodies"])
    return [
        {"text": text, "creator_id": f"eval_{scenario['name'][:12]}_{i}"}
        for i, text in enumerate(scenario["texts"], 1)
    ]


def describe(body):
    """A short, readable note of what was sent — for the report."""
    if (isinstance(body, dict) and set(body) == {"text", "creator_id"}
            and isinstance(body.get("text"), str)):
        text = body["text"]
        return text[:70] if text else "(empty text)"
    return json.dumps(body)[:120]


def post_json(requests, url, body, timeout):
    """POST a body and return (status, payload), keeping the status even when
    the answer isn't JSON. A 500 page in HTML is exactly what criterion 5 is
    looking for, so it can't be allowed to vanish into an exception."""
    response = requests.post(url, json=body, timeout=timeout)
    try:
        payload = response.json() if response.content else {}
    except ValueError:
        payload = {"_not_json": response.text[:200]}
    return response.status_code, payload


def read_log(requests, url):
    """Every audit line, oldest first, from GET /log."""
    return requests.get(f"{url}/log", timeout=30).json()["entries"]


def log_size(requests, url):
    return requests.get(f"{url}/health", timeout=30).json()["log_entries"]


def run_bodies(scenario, requests, args):
    """
    Criterion 5. Each bad body is sent as written, and the audit log's length
    is read before and after it, so "writes one rejected line" is counted and
    not assumed. /ping goes last, to show the batch left the service up.
    """
    results = []
    for body in scenario["bodies"]:
        before = log_size(requests, args.url)
        status, payload = post_json(requests, f"{args.url}/submit", body, args.timeout)
        after = log_size(requests, args.url)
        last = read_log(requests, args.url)[-1] if after else {}
        results.append({
            "status": status,
            "error": payload.get("error") if isinstance(payload, dict) else None,
            "guess": payload.get("guess") if isinstance(payload, dict) else None,
            "log_lines_added": after - before,
            "last_log_event": last.get("event"),
            "last_log_reason": last.get("reason"),
            "sent": describe(body),
        })
    ping_status, ping = post_json(requests, f"{args.url}/ping",
                                  {"message": "still up?"}, args.timeout)
    results.append({"ping_after_batch": True, "status": ping_status,
                    "ok": ping.get("ok") if isinstance(ping, dict) else None})
    return results


def run_appeals(scenario, trial, requests, args):
    """
    Criterion 4: submit, appeal the content_id that came back, then read
    GET /log and check every line the criterion names. Five real ids, then
    two made-up ones: a never-issued id and a one-character typo of a real id.
    """
    spec = scenario["appeals"]
    real = []
    for i, text in enumerate(spec["texts"], 1):
        _, decision = post_json(requests, f"{args.url}/submit",
                                {"text": text, "creator_id": f"eval_appeal_{i}"},
                                args.timeout)
        reasoning = spec["reasoning"].format(trial=trial, i=i)
        appeal_status, appeal = post_json(
            requests, f"{args.url}/appeal",
            {"content_id": decision.get("content_id"), "reasoning": reasoning},
            args.timeout)
        real.append((decision, reasoning, appeal_status, appeal))

    first_id = real[0][0].get("content_id") or ""
    typo_id = first_id[:-1] + ("0" if first_id[-1:] != "0" else "1")
    def appeal_count():
        return sum(1 for e in read_log(requests, args.url) if e.get("event") == "appeal")

    made_up = []
    for content_id in (spec["made_up_id"], typo_id):
        # Counted across the whole log, not by this id: an appeal logged under
        # a null or rewritten id would slip past a search for the id itself.
        before = appeal_count()
        status, payload = post_json(
            requests, f"{args.url}/appeal",
            {"content_id": content_id, "reasoning": spec["reasoning"].format(trial=trial, i="x")},
            args.timeout)
        made_up.append((content_id, status, payload, appeal_count() - before))

    log = read_log(requests, args.url)
    results = []
    for decision, reasoning, appeal_status, appeal in real:
        cid = decision.get("content_id")
        lines = [(n, e) for n, e in enumerate(log) if e.get("content_id") == cid]
        decided = [(n, e) for n, e in lines if "event" not in e]
        appeals = [(n, e) for n, e in lines if e.get("event") == "appeal"]
        unchanged = len(decided) == 1 and all(
            decided[0][1].get(field) == decision.get(key)
            for field, key in (("guess", "guess"), ("combined_score", "confidence"),
                               ("label", "label"), ("model_score", "model_score"),
                               ("style_score", "style_score"), ("status", "status"))
        ) and decided[0][1].get("status") == "decided"
        exact = (len(appeals) == 1 and appeals[0][1].get("reasoning") == reasoning
                 and appeals[0][1].get("status") == "under_review")
        later = bool(decided and appeals and appeals[0][0] > decided[0][0])
        checks = {
            "appeal_status": appeal_status,
            "appeal_response_status": appeal.get("status"),
            "decision_lines": len(decided),
            "decision_unchanged_and_decided": unchanged,
            "appeal_lines": len(appeals),
            "appeal_line_has_exact_reasoning": exact,
            "appeal_line_after_decision": later,
        }
        checks["passed"] = (appeal_status == 200 and appeal.get("status") == "under_review"
                            and unchanged and exact and later)
        results.append({"kind": "real", "content_id": cid,
                        "guess": decision.get("guess"), **checks})

    for content_id, status, payload, appeals_added in made_up:
        mentions = [e for e in log if e.get("content_id") == content_id]
        appeal_lines = [e for e in mentions if e.get("event") == "appeal"]
        results.append({
            "kind": "made_up",
            "content_id": content_id,
            "appeal_status": status,
            "error": payload.get("error") if isinstance(payload, dict) else None,
            "appeal_lines_with_this_id": len(appeal_lines),
            "appeal_lines_added": appeals_added,
            "passed": status == 404 and not appeal_lines and appeals_added == 0,
        })
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        import scenarios
    except ImportError:
        print("No scenarios.py found. Milestone 3 starts by filling it in.",
              file=sys.stderr)
        sys.exit(1)

    problems = scenarios.validate()
    if problems:
        print("scenarios.py has problems:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py",
              file=sys.stderr)
        sys.exit(1)

    if args.trials < 3:
        print(f"!! {args.trials} trial(s). The submission asks for three.\n")

    rows = []
    for scenario in scenarios.SCENARIOS:
        print(f"\n{scenario['name']}  (criterion {scenario.get('criterion') or '—'})")

        trials = []
        for trial in range(1, args.trials + 1):
            if scenario.get("appeals"):
                results = run_appeals(scenario, trial, requests, args)
                passed = sum(1 for r in results if r["passed"])
                trials.append(results)
                print(f"  trial {trial}: {passed}/{len(results)} appeal checks passed")
                continue
            if scenario.get("bodies"):
                results = run_bodies(scenario, requests, args)
                trials.append(results)
                codes = [str(r["status"]) for r in results]
                print(f"  trial {trial}: {' '.join(codes[:-1])} · ping {codes[-1]}")
                continue

            results = []
            for i, body in enumerate(bodies_for(scenario), 1):
                preview = describe(body)
                try:
                    status, payload = post_json(requests, f"{args.url}/submit",
                                                body, args.timeout)
                    results.append({
                        "status": status,
                        "guess": payload.get("guess"),
                        "confidence": payload.get("confidence"),
                        "model_score": payload.get("model_score"),
                        "style_score": payload.get("style_score"),
                        "label": payload.get("label"),
                        "error": payload.get("error"),
                        "sent": preview,
                    })
                except Exception as exc:  # noqa: BLE001
                    results.append({"status": None, "error": f"{type(exc).__name__}: {exc}",
                                    "sent": preview})

            trials.append(results)
            guesses = [r.get("guess") or "—" for r in results]
            print(f"  trial {trial}: {', '.join(guesses)}")

        rows.append({"scenario": scenario, "trials": trials})

    write_report(rows, args)


def write_report(rows, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"

    n = args.trials
    headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    divider = "|".join(["---"] * n)

    lines = [
        f"# Run log{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_eval.py::main`",
        "- Service: `app.py::submit` · scoring: `scoring.py::combine_signals`",
        f"- {n} trials per criterion · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Fill in Target from `criteria.md`, and Run and Verdict from the output",
        "underneath. Whether a trial passed depends on the criterion you wrote.",
        "",
        f"| Criterion | Target | {headers} | Verdict |",
        f"|---|---|{divider}|---|",
    ]

    for row in rows:
        scenario = row["scenario"]
        number = scenario.get("criterion")
        name = f"{number}. {scenario['name']}" if number else scenario["name"]
        lines.append(f"| {name} |  | {' | '.join([' '] * n)} |  |")

    lines += ["", "---", "", "## What actually came back", "",
              "Real output. Paste the relevant parts into your README — the rubric",
              "asks for the actual JSON, not a description of it.", ""]

    for row in rows:
        scenario = row["scenario"]
        lines += [f"### {scenario['name']}", ""]
        for trial_number, results in enumerate(row["trials"], 1):
            lines += [f"**Trial {trial_number}**", "", "```json",
                      json.dumps(results, indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")

    # The same results, machine-readable, for scripts/verdicts.py.
    data = {
        "label": args.label,
        "trials": n,
        "written": dt.datetime.now().isoformat(timespec="seconds"),
        "rows": [{"name": row["scenario"]["name"],
                  "criterion": row["scenario"].get("criterion"),
                  "trials": row["trials"]} for row in rows],
    }
    json_path = path.with_suffix(".json")
    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {json_path.relative_to(config.ROOT)}")
    print("Commit it. It's the evidence the test actually happened.")


if __name__ == "__main__":
    main()
