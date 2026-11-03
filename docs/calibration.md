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

## After coding it: the whole calibration set under the final rule

Output of `python scripts/calibrate.py --markdown` (perplexity midpoint 25,
weights 1/3 and 2/3, agreement gate, bands 0.45 and 0.70). `spread`, `ttr`
and `punct` are the raw measures; `style` is the averaged 0-1 sub-scores.

| group | id | words | ppl | model | spread | ttr | punct | style | combined | guess |
|---|---|---|---|---|---|---|---|---|---|---|
| human_casual | reddit_to_the_girl_that_splash | 184 | 29.9 | 0.429 | 0.683 | 0.803 | 0.038 | 0.175 | 0.260 | human |
| human_casual | reddit_got_a_harsh_reality_che | 284 | 18.1 | 0.626 | 0.439 | 0.819 | 0.004 | 0.641 | 0.636 | unsure |
| human_casual | reddit_psa_never_get_into_a_ca | 146 | 37.7 | 0.341 | 0.580 | 0.764 | 0.021 | 0.255 | 0.283 | human |
| human_casual | reddit_this_is_how_to_remove_t | 97 | 39.9 | 0.321 | n/a | 0.758 | 0.041 | 0.216 | 0.251 | human |
| human_casual | reddit_professor_needing_stude | 218 | 28.9 | 0.442 | 0.667 | 0.823 | 0.046 | 0.163 | 0.256 | human |
| human_plain | simple_honey_bee | 122 | 21.3 | 0.563 | 0.307 | 0.705 | 0.016 | 0.518 | 0.533 | unsure |
| human_plain | simple_moon | 188 | 17.0 | 0.650 | 0.381 | 0.726 | 0.011 | 0.495 | 0.546 | unsure |
| human_formal | wiki_erie_canal | 138 | 14.5 | 0.706 | 0.300 | 0.724 | 0.043 | 0.299 | 0.434 | human |
| human_formal | wiki_photosynthesis | 241 | 19.6 | 0.597 | 0.443 | 0.822 | 0.066 | 0.308 | 0.404 | human |
| human_formal | arxiv_bert | 162 | 32.2 | 0.400 | 0.706 | 0.859 | 0.049 | 0.243 | 0.295 | human |
| ai | ai_post_parking | 119 | 33.2 | 0.389 | 0.527 | 0.895 | 0.034 | 0.487 | 0.454 | unsure |
| ai | ai_post_freshman_advice | 135 | 24.5 | 0.507 | 0.524 | 0.900 | 0.007 | 0.718 | 0.648 | unsure |
| ai | ai_simple_honey_bee | 115 | 12.8 | 0.746 | 0.243 | 0.708 | 0.000 | 0.667 | 0.693 | unsure |
| ai | ai_wiki_erie_canal | 127 | 19.2 | 0.603 | 0.234 | 0.845 | 0.016 | 0.787 | 0.726 | ai |
| ai | ai_abstract | 126 | 45.4 | 0.278 | 0.292 | 0.941 | 0.000 | 0.960 | 0.690 | unsure |
| ai | ai_essay_belonging | 141 | 19.2 | 0.603 | 0.249 | 0.861 | 0.014 | 0.837 | 0.759 | ai |
| ai_edited | edited_post_parking | 116 | 40.8 | 0.313 | 0.389 | 0.899 | 0.017 | 0.762 | 0.612 | unsure |
| ai_edited | edited_essay_belonging | 129 | 23.8 | 0.520 | 0.338 | 0.841 | 0.000 | 0.785 | 0.697 | unsure |

### The four Milestone 4 inputs

| input | text | model | style | combined | guess |
|---|---|---|---|---|---|
| clearly AI | personal essay | 0.603 | 0.837 | 0.759 | ai |
| clearly human | r/rutgers professor post (2020) | 0.442 | 0.163 | 0.256 | human |
| formal human | Wikipedia Photosynthesis (2021) | 0.597 | 0.308 | 0.404 | human |
| lightly edited AI | the same essay, edited | 0.520 | 0.785 | 0.697 | unsure |

The edit moved signal one from 0.60 to 0.52 and signal two from 0.84 to
0.79. That was enough to drop the essay from "ai" to "unsure". The edit was
contractions, one sentence split in two, a semicolon turned into a comma and
a few dropped commas. That is a cheap edit, and it is the blind spot unit 8's
attack set will lean on.

### What this says before unit 8 runs anything

- **Human side:** 0 of 10 human texts get "ai". 7 get "human" and 3 get
  "unsure". The three unsure ones are the two plain Simple Wikipedia texts
  and the "harsh reality check" post. Plain writing still pays a price, just
  a smaller one: an "unsure" label instead of an accusation.
- **AI side:** 2 of 6 unedited AI texts get "ai". 4 land in "unsure", and
  three of those are within 0.01 of the line (0.690, 0.693, 0.697). Mean
  combined score: AI 0.662, human 0.390, a gap of 0.27.
- **Against the criteria:** if Set A in unit 8 behaves like this, criterion 2
  (3 of 5 flagged, a 0.30 gap) misses. I am not moving the 0.70 line to fix
  that here. The rule was written before these numbers existed, and lowering
  the line to catch three AI texts sitting at 0.69 would cut the human margin
  from 0.064 to about 0.04 on the strength of 18 texts. Unit 8 measures it on
  texts this rule has never seen.
