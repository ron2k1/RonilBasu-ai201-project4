"""
Settings for Provenance Guard.

Everything you're likely to change lives here, at the top, on purpose.

You'll edit the thresholds in Milestone 5 and the rate limits in unit 8.
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent


# ─── The service ─────────────────────────────────────────────────────────────

# `127.0.0.1` is loopback — only your own machine can reach it, which is what
# you want all through units 7 and 8. A host somewhere else has to accept
# traffic from outside the box, and that means `0.0.0.0`. Setting the env var
# is how you get it; the default keeps your local `curl` commands unchanged.
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))

# Flask's debug mode gives anyone who can reach the service an interactive
# Python prompt inside your process. Fine on loopback, a gift to strangers
# anywhere else — so it turns itself off the moment HOST isn't loopback.
DEBUG = os.getenv("AI201_DEBUG", "1") == "1" and HOST in ("127.0.0.1", "localhost")


# ─── The local model ─────────────────────────────────────────────────────────
# Your first signal runs a language model ON YOUR OWN MACHINE. No account, no
# key, no card. It downloads about 550 MB the first time — do that before
# class, not during it.
#
# What it measures: how *predictable* your text is to a language model. Text a
# model finds easy to predict tends to be text a model wrote.
#
# The first call is the slow one — ten to twenty seconds while the model loads,
# longer on an older laptop. After that it stays in memory and a submission
# takes a second or two. That cost is part of what you're learning: this is
# what running a model inline in a request actually looks like.

DETECTOR_MODEL = os.getenv("AI201_DETECTOR_MODEL", "gpt2")

# Longer text gives a steadier reading but takes longer. 400 tokens is roughly
# 300 words, which is enough for the signal to mean something.
DETECTOR_MAX_TOKENS = 400

# The perplexity that scores 0.5, and how sharply the score moves around it.
# The starter's midpoint was 45. At 45 all ten human calibration texts scored
# above 0.5, so ordinary human writing started out leaning AI. 25 is the
# median perplexity of those ten texts: a typical human text is now a coin
# flip, and only text more predictable than most human writing leans AI.
# docs/calibration.md has the table.
MODEL_PPL_MIDPOINT = 25.0
MODEL_PPL_STEEPNESS = 1.6


# ─── What the routes accept (Milestone 3) ────────────────────────────────────
# Decided in docs/trace.md before the route existed. Every refusal is a 4xx
# with a JSON `error` field and a `rejected` line in the audit log.

# Fewer words than this and neither signal has anything to measure. GPT-2's
# perplexity on a dozen words is noise, and one sentence has no length spread.
# The writer gets "too short to judge" and no label at all, which is better
# than a guess that reads like a verdict.
MIN_WORDS = 30

# About 3,500 words. Longer than nearly any post, and signal one only reads
# the first 400 tokens anyway, so more text buys no accuracy.
MAX_TEXT_CHARS = 20_000

# Flask refuses any request body bigger than this before the route runs.
# Generous enough that MAX_TEXT_CHARS of multi-byte text still fits.
MAX_REQUEST_BYTES = 256 * 1024

MAX_CREATOR_ID_CHARS = 200
MAX_APPEAL_CHARS = 5_000


# ─── Signal two: the style signal (Milestone 4) ──────────────────────────────
# Each measure becomes a 0-1 "AI-likeness" sub-score by a straight ramp between
# two anchors: the value that maps to 0.0 (reads human) and the value that maps
# to 1.0 (reads AI). Past either anchor it clips. The anchors were read off
# samples/calibration.json with scripts/calibrate.py; docs/calibration.md has
# the table they came from.

# Sentence-length spread (stdev / mean of words per sentence). Uneven is human.
SPREAD_HUMAN_ANCHOR = 0.60
SPREAD_AI_ANCHOR = 0.25
# Fewer sentences than this and spread is noise, so that sub-score sits at 0.5.
MIN_SENTENCES_FOR_SPREAD = 3

# Vocabulary variety: moving-window type-token ratio, window MATTR_WINDOW words.
# On the calibration set this runs the OPPOSITE way to the starter's guess:
# current chat models avoid repeating words, so higher variety reads as AI.
MATTR_WINDOW = 50
VOCAB_HUMAN_ANCHOR = 0.75
VOCAB_AI_ANCHOR = 0.90

# Uncommon punctuation per word: ; : ! ? ( ) quotes ellipses / & *. Periods,
# commas, apostrophes and hyphens are left out because everyone uses them.
# Em dashes are left out on purpose: current chat models use them heavily, so
# counting them as a human habit would reward AI text.
PUNCT_HUMAN_ANCHOR = 0.045
PUNCT_AI_ANCHOR = 0.005

# How the three sub-scores are weighted inside the style signal.
STYLE_WEIGHT_SPREAD = 1 / 3
STYLE_WEIGHT_VOCAB = 1 / 3
STYLE_WEIGHT_PUNCT = 1 / 3


# ─── Scoring (Milestone 4) ───────────────────────────────────────────────────
# How much each signal counts toward the combined score. The rule was written
# down before it was coded, in docs/calibration.md.
#
# Style counts double. On the calibration set it separated human from AI
# (group means about 0.33 vs 0.74); GPT-2 did not (0.713 vs 0.719). The model
# keeps a third because it reads word choice in context, which style can't.

WEIGHT_MODEL_SIGNAL = 1 / 3
WEIGHT_STYLE_SIGNAL = 2 / 3

# The agreement gate. The AI label needs BOTH signals above this on their own.
# If the average reaches AI_THRESHOLD while either signal is at or below it,
# the score is capped just under AI_THRESHOLD and lands in "unsure". One
# witness is never enough to accuse someone. The gate is one-sided on purpose:
# a wrong "human" label costs little, a wrong "AI" label costs a person a lot.
AGREEMENT_FLOOR = 0.5


# ─── Thresholds (Milestone 5) ────────────────────────────────────────────────
# Where one label becomes another. Scores run 0.0 (confidently human) to 1.0
# (confidently AI).
#
#   score <  HUMAN_THRESHOLD         -> high-confidence human
#   between the two                  -> unsure
#   score >= AI_THRESHOLD            -> high-confidence AI
#
# ⚠️ This is where your false-positive decision from Milestone 1 actually gets
# made. Widening the unsure band means fewer wrong accusations and more AI text
# getting through. There is no setting that avoids the trade — only settings
# that decide who pays for it.
#
# Lopsided on purpose. The AI label takes 0.20 above a coin flip; the human
# label takes 0.05 below one. The thinnest human margin on the calibration set
# is a real 2019 r/rutgers post at 0.636, under 0.70 by 0.06.

HUMAN_THRESHOLD = 0.45
AI_THRESHOLD = 0.70

# ⚠️ One thing that catches people out in Milestone 5. A weighted average can
# only land between its two inputs — so while `style_signal` is still the stub
# returning 0.5, the combined score can never leave 0.25–0.75 no matter what
# the model signal says, and the human label needs a model score below 0.20 to
# be reachable at all.
#
# If a label you can't reach is the problem, the fix is upstream of the
# thresholds: a style signal that actually varies. `scoring.label_ranges()`
# prints the bands; the reachable range is a different question.


# ─── Rate limiting (UNIT 8) ──────────────────────────────────────────────────
# Off in unit 7. You turn it on and choose the numbers in unit 8, Milestone 1.
#
# Think about two people: a real writer submitting their own work a few times
# an hour, and a script sending a thousand variations to map your thresholds.
# Your README has to say why your numbers and not others.

RATE_LIMITING_ENABLED = os.getenv("AI201_RATE_LIMITS", "0") == "1"

RATE_LIMIT_PER_MINUTE = 10
RATE_LIMIT_PER_DAY = 200

# Flask-Limiter warns loudly without this. In-memory is right for one laptop
# and wrong for anything real — a restart forgets every count, and two copies
# of the service wouldn't share limits.
RATE_LIMIT_STORAGE = "memory://"


# ─── Paths ───────────────────────────────────────────────────────────────────

LOG_DIR = ROOT / "logs"
AUDIT_LOG = LOG_DIR / "audit.jsonl"
RESULTS_DIR = ROOT / "results"
