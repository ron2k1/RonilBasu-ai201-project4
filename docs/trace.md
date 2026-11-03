# Milestone 1: the trace, written before any code

This is the plan the build has to keep. It was written before `/submit` existed,
so the scores below are what I expect, not what I measured.

## 1. The path a submission takes

1. **The route (`app.py::submit`).** A JSON body arrives at `POST /submit`. The
   route checks it before anything else runs: the body must be an object,
   `text` must be a non-empty string under the size cap, and `creator_id` must
   be a non-empty string. A body that fails gets a 4xx with a JSON `error`
   field and a `rejected` line in the audit log. It never reaches a model.
2. **The content id.** The route mints a `content_id` (a UUID). Everything
   after this point is tied to it, and `/appeal` needs it later.
3. **Signal one (`detector.py::model_signal`).** GPT-2 runs on the first 400
   tokens and returns its perplexity. That is squashed onto 0 to 1, where
   higher means more predictable and so more AI-like.
4. **Signal two (`stylometry.py::style_signal`).** Three measures of the text
   as text: how much sentence length varies, how much vocabulary repeats, and
   how punctuation is used. Each becomes a 0 to 1 sub-score and they are
   averaged. Higher means more AI-like.
5. **The combining rule (`scoring.py::combine_signals`).** The two scores
   become one number from 0 (confidently human) to 1 (confidently AI). This is
   where the false-positive decision lives.
6. **The label (`scoring.py::score_to_label`).** The number is mapped to one of
   three guesses (`human`, `unsure`, `ai`) and the full sentence a reader sees.
7. **The log and the answer.** One decision line goes to `logs/audit.jsonl`
   with both signal scores, the combined score, the guess, the label and
   `status: decided`. The same fields go back to the caller as JSON.

An appeal is a separate path: `POST /appeal` looks the `content_id` up in the
log, appends an `appeal` line with the writer's reasoning and
`status: under_review`, and confirms. The original decision line is never
edited.

## 2. The two signals and what they cannot see

### Signal one: predictability to a language model

- **Property measured:** perplexity under GPT-2, which is how surprised the
  model is by each next token.
- **Why it could differ:** a model writes by picking likely next words, so its
  own output is easy for a model to predict. People take odd turns, use
  specific names and make choices a model would not.
- **Blind spot:** it scores plainness, not authorship. Someone writing in a
  second language, a younger writer, or anyone keeping their sentences simple
  on purpose produces predictable text and will look like a model. The reverse
  also holds: AI text asked to use rare words or jargon looks human. It also
  only reads the first 400 tokens, so anything after roughly 300 words is
  invisible to it.

### Signal two: the shape of the text

- **Property measured:** sentence-length spread (coefficient of variation),
  vocabulary variety (moving-window type-token ratio, so long and short texts
  compare fairly) and punctuation use.
- **Why it could differ:** generated prose tends to march in even, mid-length
  sentences with tidy punctuation. People write a three-word sentence next to
  a forty-word one and punctuate unevenly.
- **Blind spot:** it cannot read. It has no idea what the text says. Anything
  that changes the shape without changing the words' source moves it: breaking
  sentences up, adding typos, pasting in a quotation, a list or a poem with
  line breaks. Short texts give it almost nothing to measure, and a text with
  one sentence has no spread at all.

The two are different on purpose. Signal one depends on word choice in
context. Signal two ignores meaning and looks only at counts.

## 3. Following a false positive through the service

A writer posts a 200-word personal essay they wrote themselves. They write in
short, plain sentences because English is their second language.

- **Signal one:** plain common words give low perplexity, maybe around 20.
  The default squash maps that to roughly 0.78. It says AI.
- **Signal two:** their sentences are similar lengths and their vocabulary is
  narrow, so it leans AI too, maybe 0.65.
- **Combined:** both lean AI, so even a cautious rule lands them around 0.7.
- **What they see:** the high-confidence AI label. That is the worst outcome
  this service can produce, because they did nothing wrong.
- **What they can do:** the label has to tell them the result is not final and
  that they can ask for a person to look. They send `POST /appeal` with their
  `content_id` and a sentence of reasoning. The item moves to `under_review`
  and the appeal sits in the log next to the original decision.

What this decides about thresholds:

- The high-confidence AI label must need **both** signals leaning AI. One
  signal alone, however sure, should never be enough to accuse someone.
- The AI threshold should sit further from the middle than the human one. A
  missed AI text costs the site a little. A wrong accusation costs a person a
  lot. Lopsided bands are how that trade gets written down.
- The AI label's wording must offer the appeal in the same breath.

This writer may still get flagged when both signals agree. That is the case
the appeal path exists for, and it is why the appeal must never fail
silently.

## 4. The endpoint contract

### `POST /submit`

Request body (JSON object):

| Field | Type | Rule |
|---|---|---|
| `text` | string | required. After trimming, at least `MIN_WORDS` words and at most `MAX_TEXT_CHARS` characters (both in `config.py`) |
| `creator_id` | string | required, non-empty, at most 200 characters |

Success, `200`:

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | UUID for this submission. Pass it to `/appeal` |
| `creator_id` | string | echoed back |
| `guess` | string | `"ai"`, `"human"` or `"unsure"` |
| `confidence` | float, 0 to 1 | the combined score. 0 means confidently human, 1 means confidently AI, 0.5 is a coin flip |
| `label` | string | the full sentence a reader sees |
| `model_score` | float, 0 to 1 | signal one on its own |
| `style_score` | float, 0 to 1 | signal two on its own |
| `status` | string | `"decided"` |

Refusals all return JSON `{"error": <code>, "message": <sentence>}` and write
a `rejected` line to the log:

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_json` | the body is not a JSON object |
| 400 | `missing_text` | `text` is absent, null, not a string, or blank |
| 400 | `missing_creator_id` | `creator_id` is absent, blank, not a string, or too long |
| 413 | `text_too_long` | `text` is over `MAX_TEXT_CHARS` |
| 422 | `text_too_short` | under `MIN_WORDS` words. Too little to judge, so no label at all rather than a guess |

### `POST /appeal`

Request body (JSON object):

| Field | Type | Rule |
|---|---|---|
| `content_id` | string | required, must match a decided submission in the log |
| `reasoning` | string | required, non-empty, at most `MAX_APPEAL_CHARS` characters |

Success, `200`:

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | echoed back |
| `status` | string | `"under_review"` |
| `previous_status` | string | what it was before this appeal |
| `message` | string | the confirmation the writer reads |
| `appealed_at` | string | ISO timestamp of the appeal line |

Refusals: `400 invalid_json`, `400 missing_content_id`, `400 missing_reasoning`,
`413 reasoning_too_long`, and `404 unknown_content_id` when no decision exists
for that id. A 404 writes nothing to the log as an appeal.
