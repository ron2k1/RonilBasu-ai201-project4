"""scoring.py::combine_signals and the recentered model signal (docs/calibration.md)."""

import pytest

import config
import detector
import scoring

CAP = round(config.AI_THRESHOLD - 0.01, 4)


def test_the_rule_numbers_are_the_documented_ones():
    assert config.WEIGHT_MODEL_SIGNAL == pytest.approx(1 / 3)
    assert config.WEIGHT_STYLE_SIGNAL == pytest.approx(2 / 3)
    assert config.AGREEMENT_FLOOR == 0.5
    assert config.HUMAN_THRESHOLD == 0.45
    assert config.AI_THRESHOLD == 0.70
    assert config.MODEL_PPL_MIDPOINT == 25.0


def test_style_counts_double_when_both_lean_ai():
    assert scoring.combine_signals(0.6, 0.9) == pytest.approx(0.6 / 3 + 0.9 * 2 / 3, abs=1e-4)


def test_low_scores_average_with_no_gate():
    assert scoring.combine_signals(0.1, 0.2) == pytest.approx(0.1 / 3 + 0.2 * 2 / 3, abs=1e-4)


@pytest.mark.parametrize("model,style", [(0.28, 0.96), (0.5, 1.0), (1.0, 0.5), (0.9, 0.45)])
def test_one_signal_alone_cannot_reach_the_ai_band(model, style):
    combined = scoring.combine_signals(model, style)
    assert combined < config.AI_THRESHOLD
    average = model / 3 + style * 2 / 3
    if average >= config.AI_THRESHOLD:
        assert combined == CAP


@pytest.mark.parametrize("style", [0.8, 0.85, 0.9, 0.95, 1.0])
def test_no_model_score_at_or_below_the_floor_reaches_ai_even_at_the_rounding_edge(style):
    # Both signals arrive rounded to 4 places, so walk every 4-place model
    # score up to the floor. An average a hair under 0.70 that slipped past
    # the gate and then rounded up to 0.7000 is the case this guards.
    for i in range(0, 5001):
        model = i / 10_000
        combined = scoring.combine_signals(model, style)
        assert combined < config.AI_THRESHOLD, (model, style, combined)
        assert scoring.score_to_label(combined)[0] != "ai"


def test_the_gate_leaves_a_split_that_is_already_unsure_alone():
    # model low, style middling: average 0.5, nowhere near AI, so no cap
    assert scoring.combine_signals(0.2, 0.65) == pytest.approx(0.2 / 3 + 0.65 * 2 / 3, abs=1e-4)


def test_both_signals_leaning_ai_can_reach_the_ai_band():
    assert scoring.combine_signals(0.75, 0.8) >= config.AI_THRESHOLD


def test_combined_is_always_between_zero_and_one():
    for m in (0.0, 0.25, 0.5, 0.75, 1.0):
        for s in (0.0, 0.25, 0.5, 0.75, 1.0):
            assert 0.0 <= scoring.combine_signals(m, s) <= 1.0


def test_model_signal_is_one_half_at_the_new_midpoint(monkeypatch):
    monkeypatch.setattr(detector, "perplexity", lambda text: 25.0)
    assert detector.model_signal("x") == pytest.approx(0.5)


def test_model_signal_rises_as_text_gets_more_predictable(monkeypatch):
    monkeypatch.setattr(detector, "perplexity", lambda text: 12.5)
    expected = 1 / (1 + 0.5 ** config.MODEL_PPL_STEEPNESS)
    assert detector.model_signal("x") == pytest.approx(expected, abs=1e-4)
