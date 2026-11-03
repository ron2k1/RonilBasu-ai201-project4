#!/usr/bin/env python3
"""
Print both signals for every text in samples/calibration.json, side by side.

    python scripts/calibrate.py
    python scripts/calibrate.py --markdown      # a table to paste into docs

This is the Milestone 4 instruction "print both signals for all inputs in one
table and look at it", for the whole calibration set. It calls the same
functions the route calls, so what it prints is what /submit would decide.
"""

import argparse
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import detector  # noqa: E402
import scoring  # noqa: E402
import stylometry  # noqa: E402

SAMPLES = ROOT / "samples" / "calibration.json"


def fmt(value, places=3):
    return "n/a" if value is None else f"{value:.{places}f}"


def measure(item):
    text = item["text"]
    model = detector.model_signal(text)
    style = stylometry.style_signal(text)
    combined = scoring.combine_signals(model, style)
    guess, _ = scoring.score_to_label(combined)
    return {
        "id": item["id"],
        "group": item["group"],
        "words": len(stylometry.words(text)),
        "ppl": detector.perplexity(text),
        "model": model,
        "spread": stylometry.sentence_length_spread(text),
        "ttr": stylometry.type_token_ratio(text),
        "punct": stylometry.punctuation_density(text),
        "style": style,
        "combined": combined,
        "guess": guess,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()

    items = json.loads(SAMPLES.read_text(encoding="utf-8"))["items"]
    rows = [measure(item) for item in items]

    cols = ["group", "id", "words", "ppl", "model", "spread", "ttr", "punct",
            "style", "combined", "guess"]
    if args.markdown:
        print("| " + " | ".join(cols) + " |")
        print("|" + "---|" * len(cols))
    for r in rows:
        cells = [r["group"], r["id"][:30], str(r["words"]), f"{r['ppl']:.1f}",
                 fmt(r["model"]), fmt(r["spread"]), fmt(r["ttr"]), fmt(r["punct"]),
                 fmt(r["style"]), fmt(r["combined"]), r["guess"]]
        if args.markdown:
            print("| " + " | ".join(cells) + " |")
        else:
            print(f"{cells[0]:<13} {cells[1]:<31} {cells[2]:>4} {cells[3]:>6} "
                  + " ".join(f"{c:>6}" for c in cells[4:10]) + f"  {cells[10]}")

    print()
    for group in dict.fromkeys(r["group"] for r in rows):
        sub = [r for r in rows if r["group"] == group]
        print(f"{group:<13} mean model {statistics.mean(r['model'] for r in sub):.3f}  "
              f"mean style {statistics.mean(r['style'] for r in sub):.3f}  "
              f"mean combined {statistics.mean(r['combined'] for r in sub):.3f}  "
              f"guesses {[r['guess'] for r in sub]}")


if __name__ == "__main__":
    main()
