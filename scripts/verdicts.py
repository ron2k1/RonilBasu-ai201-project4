#!/usr/bin/env python3
"""
Apply criteria.md's five targets to a run_eval.py result.  (unit 8, M3-M5)

    python scripts/verdicts.py results/run_<stamp>_before.json

run_eval.py records what came back and leaves the Verdict column blank. This
reads its JSON, checks each trial against the criterion's target, and prints
the five-row table plus a per-text score sheet. A criterion is MET only if it
holds in every trial. It writes the same thing to results/verdicts_<stem>.md.
"""

import json
import statistics
import sys
from pathlib import Path

TARGETS = {
    1: "0 of 10 Set H get ai",
    2: ">= 3 of 5 Set A get ai, and mean confidence A - H >= 0.30",
    3: "ai, unsure, human each >= 2 of all 20; >= 3 of 5 Set B unsure",
    4: "7 of 7 appeal checks",
    5: "8 of 8 bad bodies: 4xx + error field + one rejected line; /ping answers",
}


def guesses(results):
    return [r.get("guess") for r in results]


def trial_cells(rows, t):
    H = rows["set_h_human"][t]
    A = rows["set_a_ai"][t]
    B = rows["set_b_edited"][t]
    cells, passed = {}, {}

    all_ok = all(r.get("status") == 200 for r in H + A + B)

    h_ai = guesses(H).count("ai")
    cells[1] = f"{h_ai}/10 ai"
    passed[1] = all_ok and h_ai == 0

    a_ai = guesses(A).count("ai")
    gap = (statistics.mean(r["confidence"] for r in A)
           - statistics.mean(r["confidence"] for r in H)) if all_ok else float("nan")
    cells[2] = f"{a_ai}/5 ai, gap {gap:+.3f}"
    passed[2] = all_ok and a_ai >= 3 and gap >= 0.30

    every = guesses(H + A + B)
    counts = {k: every.count(k) for k in ("ai", "unsure", "human")}
    b_unsure = guesses(B).count("unsure")
    cells[3] = (f"ai {counts['ai']} · unsure {counts['unsure']} · human "
                f"{counts['human']}; B unsure {b_unsure}/5")
    passed[3] = all_ok and min(counts.values()) >= 2 and b_unsure >= 3

    appeals = rows["appeals"][t]
    ok = sum(1 for r in appeals if r.get("passed"))
    cells[4] = f"{ok}/{len(appeals)}"
    passed[4] = ok == 7 and len(appeals) == 7

    bodies = [r for r in rows["bad_input"][t] if not r.get("ping_after_batch")]
    ping = next((r for r in rows["bad_input"][t] if r.get("ping_after_batch")), {})
    clean = sum(1 for r in bodies
                if isinstance(r.get("status"), int) and 400 <= r["status"] < 500
                and r.get("error") and r.get("log_lines_added") == 1
                and r.get("last_log_event") == "rejected")
    ping_ok = ping.get("status") == 200 and ping.get("ok") is True
    cells[5] = f"{clean}/{len(bodies)}, ping {'ok' if ping_ok else 'FAILED'}"
    passed[5] = clean == 8 and len(bodies) == 8 and ping_ok
    return cells, passed


def score_sheet(rows, n):
    lines = ["| Text | Sent | " + " | ".join(f"Run {t + 1}" for t in range(n)) + " |",
             "|---|---|" + "|".join(["---"] * n) + "|"]
    for name, tag in (("set_h_human", "H"), ("set_a_ai", "A"), ("set_b_edited", "B")):
        for i in range(len(rows[name][0])):
            first = rows[name][0][i]
            runs = []
            for t in range(n):
                r = rows[name][t][i]
                if r.get("status") == 200:
                    runs.append(f"{r['guess']} {r['confidence']:.4f} "
                                f"(m {r['model_score']:.3f}, s {r['style_score']:.3f})")
                else:
                    runs.append(f"{r.get('status')} {r.get('error')}")
            sent = first["sent"].replace("|", "\\|").replace("\n", " ")[:40]
            lines.append(f"| {tag}{i + 1} | {sent} | " + " | ".join(runs) + " |")
    return lines


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    n = data["trials"]
    rows = {row["name"]: row["trials"] for row in data["rows"]}
    criteria = {row["name"]: row["criterion"] for row in data["rows"]}
    assert sorted(criteria.values()) == [1, 2, 3, 4, 5], criteria

    per_trial = [trial_cells(rows, t) for t in range(n)]
    out = [f"# Verdicts for `{path.name}`", "",
           "- Produced by: `scripts/verdicts.py::main` from `run_eval.py`'s JSON",
           "- A criterion is MET only if its target holds in every trial.", "",
           "| Criterion | Target | " + " | ".join(f"Run {t + 1}" for t in range(n))
           + " | Verdict |",
           "|---|---|" + "|".join(["---"] * n) + "|---|"]
    for c in range(1, 6):
        cells = [per_trial[t][0][c] + (" ✓" if per_trial[t][1][c] else " ✗")
                 for t in range(n)]
        verdict = "MET" if all(per_trial[t][1][c] for t in range(n)) else "MISSED"
        out.append(f"| {c} | {TARGETS[c]} | " + " | ".join(cells) + f" | {verdict} |")
    out += ["", "## Every scored text", "",
            "guess, combined score, and the two signals (m = model, s = style).", ""]
    out += score_sheet(rows, n)

    text = "\n".join(out) + "\n"
    print(text)
    dest = path.parent / f"verdicts_{path.stem}.md"
    dest.write_text(text, encoding="utf-8")
    print(f"Wrote {dest}")


if __name__ == "__main__":
    main()
