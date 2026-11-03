"""stylometry.py: each measure on its own, then the combined style signal."""

import pytest

import config
import stylometry


def test_spread_is_zero_when_every_sentence_is_the_same_length():
    text = "One two three four. Five six seven eight. Nine ten eleven twelve."
    assert stylometry.sentence_length_spread(text) == pytest.approx(0.0)


def test_spread_is_coefficient_of_variation_of_sentence_lengths():
    # lengths 2, 4, 6: mean 4, sample stdev 2, so 0.5
    text = "Short one. This one has four. This sentence here has six words."
    assert stylometry.sentence_length_spread(text) == pytest.approx(0.5)


@pytest.mark.parametrize("text", ["Just one sentence here with words.",
                                  "Two sentences. Only two of them here."])
def test_spread_is_none_below_the_sentence_minimum(text):
    assert config.MIN_SENTENCES_FOR_SPREAD == 3
    assert stylometry.sentence_length_spread(text) is None


def test_type_token_ratio_on_a_short_text_is_unique_over_total():
    assert stylometry.type_token_ratio("the cat and the dog") == pytest.approx(4 / 5)


def test_type_token_ratio_is_none_for_no_words():
    assert stylometry.type_token_ratio("... !!! ???") is None


def test_type_token_ratio_does_not_fall_just_because_text_is_longer():
    # The same 60-word passage once and repeated three times. Plain TTR would
    # roughly third; the moving window keeps them close.
    passage = (
        "Rain came in off the river before noon and the market packed up early. "
        "A man selling peaches gave the last crate to a kid with a wagon. "
        "By two the street was empty except for pigeons, puddles, and one dog "
        "asleep under the awning of a shuttered bakery that never reopened after "
        "the flood."
    )
    once = stylometry.type_token_ratio(passage)
    thrice = stylometry.type_token_ratio(" ".join([passage] * 3))
    assert abs(once - thrice) < 0.08


def test_punctuation_density_counts_only_the_uncommon_marks():
    # 9 words. Counted: ! ? ( ) ; : = 6. Not counted: . , ' and the hyphen.
    text = "Wait! Really? (Yes.) It's fine; well-known: done, ok."
    assert len(stylometry.words(text)) == 9
    assert stylometry.punctuation_density(text) == pytest.approx(6 / 9)


def test_punctuation_density_ignores_em_dashes():
    plain = "The plan worked and the team went home happy that night."
    dashed = "The plan worked — and the team went home — happy that night."
    assert stylometry.punctuation_density(plain) == stylometry.punctuation_density(dashed) == 0.0


def test_punctuation_density_counts_curly_quotes_and_ellipses():
    text = "She said “maybe” and then… nothing at all happened."
    assert stylometry.punctuation_density(text) == pytest.approx(3 / 9)


def test_ramp_maps_anchors_to_zero_and_one_and_clips():
    assert stylometry._ramp(0.60, human=0.60, ai=0.25) == 0.0
    assert stylometry._ramp(0.25, human=0.60, ai=0.25) == 1.0
    assert stylometry._ramp(0.425, human=0.60, ai=0.25) == pytest.approx(0.5)
    assert stylometry._ramp(0.90, human=0.60, ai=0.25) == 0.0
    assert stylometry._ramp(0.10, human=0.60, ai=0.25) == 1.0
    # increasing direction works too
    assert stylometry._ramp(0.90, human=0.75, ai=0.90) == 1.0


def test_style_signal_is_between_zero_and_one():
    for text in ["", "word", "One. Two. Three.", "a b c d e f g h i j k l m n o p"]:
        assert 0.0 <= stylometry.style_signal(text) <= 1.0


LUMPY = (
    "Okay so. I parked in Yellow Lot at 7:40 (yes, before eight!) and it was "
    "already full; I circled three times, gave up, drove to the stadium, waited "
    "twenty minutes for an LX that never came, and walked. Twenty-five minutes. "
    "In the rain? Never again. My lab partner said \"just bike\" like that's an "
    "option from Edison."
)

EVEN = (
    "The library offers many useful resources for students. It provides quiet "
    "spaces for focused study and research. The staff are helpful and "
    "knowledgeable about academic databases. Students can borrow laptops and "
    "other equipment for short periods. Overall the library is an important "
    "part of campus life for everyone."
)


def test_even_tidy_text_scores_more_ai_like_than_lumpy_text():
    assert stylometry.style_signal(EVEN) > stylometry.style_signal(LUMPY) + 0.2


def test_style_breakdown_reports_each_sub_score():
    parts = stylometry.style_breakdown(EVEN)
    assert set(parts) == {"spread", "vocab", "punct"}
    assert all(0.0 <= v <= 1.0 for v in parts.values())
