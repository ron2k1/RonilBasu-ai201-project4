# Milestone 4: what the two signals did, and the rule written before coding it

Everything here comes from `samples/calibration.json` (10 human texts dated
before ChatGPT, 6 unedited AI texts, 2 lightly edited AI texts) run through
`scripts/calibrate.py`. None of these texts may be reused for the criteria
sets in unit 8.

## Signal one alone, at the starter's midpoint (perplexity 45)

| group | text | perplexity | model_score |
|---|---|---|---|
| human_casual | r/rutgers, splashed a drink (2020) | 29.9 | 0.658 |
| human_casual | r/rutgers, harsh reality check (2019) | 18.1 | 0.811 |
| human_casual | r/rutgers, never get into a car (2019) | 37.7 | 0.570 |
| human_casual | r/rutgers, NJPIRG fee (2020) | 39.9 | 0.548 |
| human_casual | r/rutgers, professor asking for advice (2020) | 28.9 | 0.670 |
| human_plain | Simple Wikipedia, Honey bee (2020) | 21.3 | 0.767 |
| human_plain | Simple Wikipedia, Moon (2021) | 17.0 | 0.826 |
| human_formal | Wikipedia, Erie Canal (2021) | 14.5 | 0.860 |
| human_formal | Wikipedia, Photosynthesis (2021) | 19.6 | 0.791 |
| human_formal | arXiv BERT abstract (2018) | 32.2 | 0.630 |
| ai | parking post | 33.2 | 0.620 |
| ai | freshman advice post | 24.5 | 0.725 |
| ai | simple honey bee | 12.8 | 0.882 |
| ai | encyclopedic Erie Canal | 19.2 | 0.796 |
| ai | paper abstract | 45.4 | 0.496 |
| ai | personal essay | 19.2 | 0.796 |

Mean model_score: human 0.713, AI 0.719. **Signal one does not separate these
groups.** The human Wikipedia Erie Canal paragraph is more predictable to
GPT-2 (14.5) than the AI-written Erie Canal paragraph on the same facts
(19.2). The plain Simple Wikipedia texts score 0.77 and 0.83. That is the
blind spot from docs/trace.md showing up in real data: GPT-2 is a 2019 model
and it scores register (plain, encyclopedic) rather than who wrote the text.
A per-token "burstiness" variant (spread of GPT-2 surprise) was also tried
and did not separate them either, so it was dropped rather than added as a
third signal.

## Signal two's three measures

| group | sentence spread | vocabulary (MATTR) | uncommon punct / word |
|---|---|---|---|
| human_casual mean | 0.59 (one post has 2 sentences, n/a) | 0.79 | 0.030 |
| human_plain mean | 0.34 | 0.72 | 0.014 |
| human_formal mean | 0.48 | 0.80 | 0.053 |
| ai mean | 0.34 | 0.86 | 0.012 |
| ai_edited mean | 0.36 | 0.87 | 0.009 |

- **Sentence spread** points the way the starter predicted: AI text is more
  even. Plain human writing (Simple Wikipedia) is just as even, so this is
  where plain writers get hurt.
- **Vocabulary variety runs backwards from the starter's guess.** The AI
  texts repeat fewer words than the human ones. Current chat models avoid
  repeating themselves; people writing a forum post do not. So higher
  variety reads as AI here.
- **Uncommon punctuation** (parentheses, colons, semicolons, question and
  exclamation marks, quotes) is the clearest split. People use it unevenly.
  The AI texts barely use it. Em dashes are excluded on purpose because
  current chat models overuse them, and counting them as human would reward
  AI text. None of my AI samples happen to contain one, which would have made
  the signal look better here than it is.

Anchors (the raw values that map to 0.0 and 1.0 AI-likeness) were set just
outside where the human and AI groups sit, and the three sub-scores are
averaged with equal weights. Eighteen texts are too few to tune weights
without fitting noise.

## The case where the two signals split

The AI paper abstract: GPT-2 finds its jargon surprising (perplexity 45.4,
model_score 0.50, and 0.28 once the midpoint moves to 25 as below), while its
shape is the most machine-like in the set (style_score 0.96). One signal says
coin flip or human, the other says AI.

The real 2019 r/rutgers post "harsh reality check" is the opposite worry.
It is human, and both signals lean AI: perplexity 18.1 (model 0.63 at the new
midpoint) and style 0.64, because it has almost no uncommon punctuation and
fairly even sentences. This is the false-positive writer from
docs/trace.md, and no rule can rescue them by weighting alone. The threshold
has to sit above them.

## The combining rule, written before it was coded

1. **Recenter signal one.** Move the perplexity midpoint from 45 to 25, the
   median perplexity of the ten human calibration texts. At 45, all ten
   human texts scored above 0.5, so ordinary human writing started out
   leaning AI. At 25, a typical human text is a coin flip on this signal and
   only text more predictable than most human writing leans AI. Steepness
   stays 1.6.
2. **Weighted average, style counts double.** `1/3 * model + 2/3 * style`.
   Style separated the calibration groups and model did not, so style
   carries more. Model keeps a third because it is a different kind of
   evidence: it reads word choice in context, which style cannot see.
3. **Agreement gate.** The AI label needs both signals above 0.5 on their
   own. If the average reaches the AI threshold but either signal is at or
   below 0.5, the score is capped at 0.69, just under the AI threshold, and
   the text lands in "unsure". One witness is never enough to accuse someone.
   The gate is one-sided: a low average gives the human label without
   needing both signals to agree, because a wrong "human" costs the site
   little and a wrong "AI" costs a person a lot.
4. **Lopsided thresholds.** Below 0.45 is human. 0.70 and above is AI.
   Between is unsure. Reaching AI takes 0.20 above a coin flip; reaching
   human takes 0.05 below it.

Applied to the split case: the abstract averages 0.73, but signal one is
0.28, so the gate caps it at 0.69 and it is labelled unsure. Applied to the
"harsh reality check" post: both signals are above 0.5, so the gate does not
help, but the average is 0.64, which is under 0.70, so it is labelled unsure
rather than AI. That margin (0.06) is the thinnest on the human side of the
calibration set and is the number to watch in unit 8.

Where it lives: `scoring.py::combine_signals` (rule) and
`scoring.py::score_to_label` (thresholds). Every number is in `config.py`.
