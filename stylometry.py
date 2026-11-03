"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics

import config

# Uncommon punctuation: the marks that vary between writers. Periods, commas,
# apostrophes and in-word hyphens are left out because everyone uses them; em
# and en dashes are left out because current chat models use them heavily (see
# config.py). Straight and curly double quotes, and both ellipsis spellings.
_UNCOMMON_PUNCT = re.compile(r"\.\.\.|[;:!?()\"“”…/&*]")


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float | None:
    """
    How much sentence length varies: the coefficient of variation (sample
    stdev / mean) of words per sentence.

    Returns:
        0.0 when every sentence is the same length, rising as they get more
        uneven. Higher means more human. Typical prose sits between 0.2 and
        0.8. Returns None below config.MIN_SENTENCES_FOR_SPREAD sentences: two
        sentences give one difference, which is noise rather than a habit, and
        `stdev` raises on one. None means "no evidence", not "uniform".
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < config.MIN_SENTENCES_FOR_SPREAD:
        return None
    return statistics.stdev(lengths) / statistics.mean(lengths)


def type_token_ratio(text: str) -> float | None:
    """
    Vocabulary variety as a moving-average type-token ratio (MATTR).

    Plain unique/total falls as a text gets longer, because common words
    repeat. So the ratio is taken inside every window of
    config.MATTR_WINDOW consecutive words and averaged. A text shorter than
    one window gets the plain ratio.

    Returns:
        A float between 0 and 1, or None for a text with no words. Higher
        means more varied vocabulary, which on the calibration set reads as
        MORE AI-like, not less (see config.py).
    """
    tokens = words(text)
    if not tokens:
        return None
    window = config.MATTR_WINDOW
    if len(tokens) <= window:
        return len(set(tokens)) / len(tokens)
    ratios = [len(set(tokens[i:i + window])) / window
              for i in range(len(tokens) - window + 1)]
    return statistics.mean(ratios)


def punctuation_density(text: str) -> float | None:
    """
    Uncommon punctuation marks per word.

    Counts ; : ! ? ( ) double quotes, ellipses, / & and *. Leaves out the marks
    every writer uses (periods, commas, apostrophes, in-word hyphens) and em
    dashes, which current chat models overuse.

    Returns:
        A float, 0.0 for text with none, or None for a text with no words.
        Higher means more human. Casual posts and formal prose with
        parentheses and colons sit around 0.04 to 0.10; tidy generated prose
        sits near 0.01.
    """
    tokens = words(text)
    if not tokens:
        return None
    return len(_UNCOMMON_PUNCT.findall(text)) / len(tokens)


# ── Combining them ───────────────────────────────────────────────────────────

def _ramp(value: float, human: float, ai: float) -> float:
    """
    Map a raw measure onto 0 (reads human) to 1 (reads AI), clipped.

    `human` is the raw value that maps to 0.0 and `ai` the one that maps to
    1.0. Either may be the larger, so one function handles measures that
    point either way.
    """
    position = (value - human) / (ai - human)
    return min(max(position, 0.0), 1.0)


def style_breakdown(text: str) -> dict[str, float]:
    """
    The three sub-scores on the 0-1 AI-likeness scale, before weighting.

    A measure with no evidence (too few sentences or no words) sits at 0.5,
    so it pulls neither way.
    """
    spread = sentence_length_spread(text)
    vocab = type_token_ratio(text)
    punct = punctuation_density(text)
    return {
        "spread": 0.5 if spread is None else _ramp(
            spread, config.SPREAD_HUMAN_ANCHOR, config.SPREAD_AI_ANCHOR),
        "vocab": 0.5 if vocab is None else _ramp(
            vocab, config.VOCAB_HUMAN_ANCHOR, config.VOCAB_AI_ANCHOR),
        "punct": 0.5 if punct is None else _ramp(
            punct, config.PUNCT_HUMAN_ANCHOR, config.PUNCT_AI_ANCHOR),
    }


def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.

    The decisions, written down:
      1. Direction. Spread and uncommon punctuation point human, so their
         ramps run downward (more of them, lower score). Vocabulary variety
         points AI on the calibration set, so its ramp runs upward.
      2. Scale. Each raw measure goes through `_ramp` between two anchors in
         config.py, so all three land on the same 0-1 scale before they are
         averaged. Weights are equal: the calibration set is 18 texts, too few
         to justify tuning them.
    """
    parts = style_breakdown(text)
    score = (config.STYLE_WEIGHT_SPREAD * parts["spread"]
             + config.STYLE_WEIGHT_VOCAB * parts["vocab"]
             + config.STYLE_WEIGHT_PUNCT * parts["punct"])
    return round(min(max(score, 0.0), 1.0), 4)


def _fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.3f}"


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    parts = style_breakdown(text)
    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"{'measure':<24} {'raw':>7}   AI-likeness 0-1")
    print(f"{'sentence_length_spread':<24} {_fmt(sentence_length_spread(text)):>7}   {parts['spread']:.3f}")
    print(f"{'type_token_ratio':<24} {_fmt(type_token_ratio(text)):>7}   {parts['vocab']:.3f}")
    print(f"{'punctuation_density':<24} {_fmt(punctuation_density(text)):>7}   {parts['punct']:.3f}")
    print(f"\nstyle_signal             {style_signal(text)}   (higher = more likely AI)")
