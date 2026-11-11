# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 18:10
- Auto-marked BROKE (5xx, crash, no response): **0**
- Marked by hand afterwards: **12 BROKE, 44 HELD** (rule in the README)

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `3b674684-67db-49b2-8e18-f47fbff57262` | unsure | 0.690 | **BROKE** |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c08a5e21-2fab-4467-81f1-db7e8c8f5b9e` | unsure | 0.557 | **BROKE** |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `64203cf1-b2f7-4f5b-b60a-ecb8ee1c7778` | unsure | 0.508 | **BROKE** |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `f25254ff-0cc6-4955-8804-78763ec9ed33` | unsure | 0.740 | **BROKE** |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `5ce3de9f-0a2a-4d4c-9df4-1b3f67ee22c4` | human | 0.436 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `b345c903-82ff-4d1b-9481-aa4b7abd264d` | unsure | 0.483 | **BROKE** |
| EV07 | evasion | signal two: padding with punctuation | 200 | `e8de4e2b-cc40-4653-bb39-206d7d6c3c10` | human | 0.371 | **BROKE** |
| EV08 | evasion | signal one: text below the token window | 422 | `—` | — | — | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `069d1166-25bc-463e-a620-724ee65ac83e` | unsure | 0.689 | **BROKE** |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `813c9723-164d-4503-a6f7-3f9831b46ee3` | unsure | 0.669 | **BROKE** |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `70d2a477-0ea0-40f1-bc5a-68a7b1e0e978` | unsure | 0.525 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `2b14a0f3-21a5-43e6-a293-0e76dab36533` | unsure | 0.648 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `a33a08f2-2bb1-41a0-ab83-ec94d5a1bc0c` | unsure | 0.703 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `545d7bce-3ac1-4fff-ab7f-4dc95ca44a07` | unsure | 0.696 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `e5567536-0de2-4abb-9a75-12413b7a8412` | unsure | 0.631 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `3ef06426-3a8d-480d-aa20-3a2d8790b59a` | unsure | 0.530 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c6ebf156-4ef0-45a4-be46-2071c3c340d8` | unsure | 0.470 | HELD |
| FP08 | false_positive | very short genuine human submission | 422 | `—` | — | — | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `17d8c632-1d24-4042-a1d2-a9562e25bfa3` | unsure | 0.528 | **BROKE** |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `1dfe929d-f365-4b14-bbd3-e5b9abe4f5c9` | human | 0.379 | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `7af34149-d942-4cdc-afe3-6285b3106c25` | unsure | 0.507 | **BROKE** |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `2377e1eb-2448-427c-8851-1e2c68f96c5b` | human | 0.386 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `a6a09a5f-873a-466b-9370-ab252b460055` | unsure | 0.470 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `20bded42-8e45-44ee-88ab-999fb7dc44e2` | unsure | 0.523 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 422 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 422 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 422 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 422 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 422 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 422 | `—` | — | — | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "3b674684-67db-49b2-8e18-f47fbff57262",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.6903,
  "model_score": 0.0709,
  "style_score": 1.0,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c08a5e21-2fab-4467-81f1-db7e8c8f5b9e",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5573,
  "model_score": 0.3638,
  "style_score": 0.654,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "64203cf1-b2f7-4f5b-b60a-ecb8ee1c7778",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.508,
  "model_score": 0.438,
  "style_score": 0.543,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "f25254ff-0cc6-4955-8804-78763ec9ed33",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.74,
  "model_score": 0.3806,
  "style_score": 1.0,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "5ce3de9f-0a2a-4d4c-9df4-1b3f67ee22c4",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.4362,
  "model_score": 0.1559,
  "style_score": 0.5764,
  "label": "Every post here gets an automated check for AI-generated writing. This one found nothing that points to AI, so we think a person wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "b345c903-82ff-4d1b-9481-aa4b7abd264d",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4832,
  "model_score": 0.3435,
  "style_score": 0.553,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "e8de4e2b-cc40-4653-bb39-206d7d6c3c10",
  "creator_id": "attacker_EV07",
  "guess": "human",
  "confidence": 0.3712,
  "model_score": 0.3561,
  "style_score": 0.3787,
  "label": "Every post here gets an automated check for AI-generated writing. This one found nothing that points to AI, so we think a person wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_EV08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "069d1166-25bc-463e-a620-724ee65ac83e",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6891,
  "model_score": 0.4817,
  "style_score": 0.7928,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "813c9723-164d-4503-a6f7-3f9831b46ee3",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.6692,
  "model_score": 0.9483,
  "style_score": 0.5296,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "70d2a477-0ea0-40f1-bc5a-68a7b1e0e978",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.525,
  "model_score": 0.3867,
  "style_score": 0.5941,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "HELD"
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "2b14a0f3-21a5-43e6-a293-0e76dab36533",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6484,
  "model_score": 0.5247,
  "style_score": 0.7103,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "HELD"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "a33a08f2-2bb1-41a0-ab83-ec94d5a1bc0c",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7034,
  "model_score": 0.6173,
  "style_score": 0.7464,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "HELD"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "545d7bce-3ac1-4fff-ab7f-4dc95ca44a07",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6958,
  "model_score": 0.6606,
  "style_score": 0.7134,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "HELD"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "e5567536-0de2-4abb-9a75-12413b7a8412",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6309,
  "model_score": 0.6104,
  "style_score": 0.6411,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "HELD"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "3ef06426-3a8d-480d-aa20-3a2d8790b59a",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5304,
  "model_score": 0.7437,
  "style_score": 0.4237,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "HELD"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "c6ebf156-4ef0-45a4-be46-2071c3c340d8",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.4702,
  "model_score": 0.744,
  "style_score": 0.3333,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "HELD"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "17d8c632-1d24-4042-a1d2-a9562e25bfa3",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5283,
  "model_score": 0.2515,
  "style_score": 0.6667,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "1dfe929d-f365-4b14-bbd3-e5b9abe4f5c9",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.3791,
  "model_score": 0.0912,
  "style_score": 0.5231,
  "label": "Every post here gets an automated check for AI-generated writing. This one found nothing that points to AI, so we think a person wrote it.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "7af34149-d942-4cdc-afe3-6285b3106c25",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5066,
  "model_score": 0.3638,
  "style_score": 0.578,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "2377e1eb-2448-427c-8851-1e2c68f96c5b",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.3856,
  "model_score": 0.2807,
  "style_score": 0.4381,
  "label": "Every post here gets an automated check for AI-generated writing. This one found nothing that points to AI, so we think a person wrote it.",
  "error": null,
  "verdict": "HELD"
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "a6a09a5f-873a-466b-9370-ab252b460055",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.47,
  "model_score": 0.4099,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "HELD"
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "20bded42-8e45-44ee-88ab-999fb7dc44e2",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5231,
  "model_score": 0.3304,
  "style_score": 0.6194,
  "label": "Our automated check couldn't tell whether a person or an AI wrote this. That happens with a lot of real writing, especially plain or very polished writing. It is not a finding against the writer. Nothing needs to change, and the post stays up as normal.",
  "error": null,
  "verdict": "HELD"
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```
