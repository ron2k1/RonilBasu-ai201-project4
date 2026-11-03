"""scoring.py::score_to_label: three labels, no gaps, all reachable."""

import re

import pytest

import config
import scoring


@pytest.mark.parametrize("score,guess", [
    (0.0, "human"), (0.2, "human"), (0.4499, "human"),
    (0.45, "unsure"), (0.51, "unsure"), (0.6999, "unsure"),
    (0.70, "ai"), (0.95, "ai"), (1.0, "ai"),
])
def test_bands(score, guess):
    assert scoring.score_to_label(score)[0] == guess


def test_a_flip_at_one_half_is_not_what_this_does():
    assert scoring.score_to_label(0.51) != scoring.score_to_label(0.95)


def test_every_score_from_zero_to_one_gets_exactly_one_of_three_labels():
    seen = {}
    for i in range(0, 1001):
        guess, text = scoring.score_to_label(i / 1000)
        assert guess in ("human", "unsure", "ai")
        seen.setdefault(guess, set()).add(text)
    assert set(seen) == {"human", "unsure", "ai"}
    assert all(len(texts) == 1 for texts in seen.values())


def test_the_three_label_texts_are_full_distinct_sentences():
    texts = [scoring.score_to_label(s)[1] for s in (0.1, 0.6, 0.9)]
    assert len(set(texts)) == 3
    for text in texts:
        assert text.endswith(".")
        assert len(text.split()) >= 8
        assert "PLACEHOLDER" not in text


def test_labels_carry_no_jargon_and_no_numbers():
    for score in (0.1, 0.6, 0.9):
        text = scoring.score_to_label(score)[1].lower()
        assert not re.search(r"\d", text)
        for word in ("threshold", "confidence", "score", "signal", "perplexity", "probability"):
            assert word not in text


def test_the_ai_label_tells_the_writer_they_can_ask_for_a_review():
    text = scoring.score_to_label(0.9)[1].lower()
    assert "review" in text
    assert "can be wrong" in text


def test_the_review_pending_label_is_its_own_text():
    assert scoring.REVIEW_PENDING_LABEL not in [scoring.score_to_label(s)[1] for s in (0.1, 0.6, 0.9)]
    assert "review" in scoring.REVIEW_PENDING_LABEL.lower()


@pytest.mark.parametrize("model,style,guess", [
    (0.2, 0.2, "human"),
    (0.5, 0.5, "unsure"),
    (0.8, 0.8, "ai"),
])
def test_each_label_is_reachable_through_the_combining_rule(model, style, guess):
    assert scoring.score_to_label(scoring.combine_signals(model, style))[0] == guess


def test_label_ranges_match_config():
    ranges = dict(scoring.label_ranges())
    assert ranges["high-confidence human"].endswith(f"{config.HUMAN_THRESHOLD:.2f}")
    assert ranges["high-confidence AI"].startswith(f"{config.AI_THRESHOLD:.2f}")
