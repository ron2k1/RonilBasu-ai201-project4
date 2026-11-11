# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 17:49
- Auto-marked BROKE (5xx, crash, no response): **0**
- Marked by hand afterwards: **13 BROKE, 43 HELD** (rule in the README)

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `b58f1226-d47e-4eb0-98e9-6e45dba36ed6` | unsure | 0.690 | **BROKE** |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `17530582-6d4c-4bac-93e1-4cd9ae89ca36` | unsure | 0.557 | **BROKE** |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `bff1bc15-3b5b-4732-ad4d-86bd14a95f6e` | unsure | 0.508 | **BROKE** |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `53f6821e-8aca-4eed-abf3-a6276ce25eaf` | unsure | 0.690 | **BROKE** |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `48cbc6b5-d664-45c2-b977-1624241794ef` | human | 0.436 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `07c4f9cb-aadd-48e4-bc2f-50fc873e2947` | unsure | 0.483 | **BROKE** |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c65a936e-ea18-4aad-bbb7-9a914e385e56` | human | 0.371 | **BROKE** |
| EV08 | evasion | signal one: text below the token window | 422 | `—` | — | — | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `e6ef6569-f237-4622-bc52-f515a158b5a6` | unsure | 0.689 | **BROKE** |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `edf2e254-2284-45c4-a5ea-4288aa6cd60d` | unsure | 0.669 | **BROKE** |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `84cfaadc-a8f7-4f88-8a61-39304f14fcfc` | unsure | 0.525 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `881ca51a-43ac-4054-a8d0-82e7726e3ebb` | unsure | 0.648 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `cd0ebeff-ff00-452d-b9cb-c2b254e1a126` | ai | 0.703 | **BROKE** |
| FP04 | false_positive | a student essay written to a rubric | 200 | `badf55de-2d55-474e-9d8a-87c91283acbe` | unsure | 0.696 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `96218fc3-e23c-4c0b-9343-87e856bce70b` | unsure | 0.631 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `d37677d9-c8bc-4074-a757-c6ca0238098a` | unsure | 0.530 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `701f7d2c-80de-4ef2-a399-cf4679c76c2c` | unsure | 0.470 | HELD |
| FP08 | false_positive | very short genuine human submission | 422 | `—` | — | — | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `3e90bb94-975d-4e1a-a331-3f04ea6fdc6c` | unsure | 0.528 | **BROKE** |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `e31d522c-e072-41fa-9132-d403c3dad081` | human | 0.379 | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `8b30875d-aef8-4959-ab44-1eb554c5265a` | unsure | 0.507 | **BROKE** |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `ff78c963-947e-4d2e-bfff-2c66b70a3d5c` | human | 0.386 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `3a1d733e-5378-4d44-bf4b-14439eabeb84` | unsure | 0.470 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `ce41e390-edd4-4f57-94e6-0a4f494ce38c` | unsure | 0.523 | HELD |
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
  "content_id": "b58f1226-d47e-4eb0-98e9-6e45dba36ed6",
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
  "content_id": "17530582-6d4c-4bac-93e1-4cd9ae89ca36",
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
  "content_id": "bff1bc15-3b5b-4732-ad4d-86bd14a95f6e",
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
  "content_id": "53f6821e-8aca-4eed-abf3-a6276ce25eaf",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.69,
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
  "content_id": "48cbc6b5-d664-45c2-b977-1624241794ef",
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
  "content_id": "07c4f9cb-aadd-48e4-bc2f-50fc873e2947",
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
  "content_id": "c65a936e-ea18-4aad-bbb7-9a914e385e56",
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
  "content_id": "e6ef6569-f237-4622-bc52-f515a158b5a6",
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
  "content_id": "edf2e254-2284-45c4-a5ea-4288aa6cd60d",
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
  "content_id": "84cfaadc-a8f7-4f88-8a61-39304f14fcfc",
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
  "content_id": "881ca51a-43ac-4054-a8d0-82e7726e3ebb",
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
  "content_id": "cd0ebeff-ff00-452d-b9cb-c2b254e1a126",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7034,
  "model_score": 0.6173,
  "style_score": 0.7464,
  "label": "Our automated check flagged this text as likely AI-generated. Checks like this can be wrong, including about writing people did themselves. If you wrote this, you can ask for a person to review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "badf55de-2d55-474e-9d8a-87c91283acbe",
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
  "content_id": "96218fc3-e23c-4c0b-9343-87e856bce70b",
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
  "content_id": "d37677d9-c8bc-4074-a757-c6ca0238098a",
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
  "content_id": "701f7d2c-80de-4ef2-a399-cf4679c76c2c",
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
  "content_id": "3e90bb94-975d-4e1a-a331-3f04ea6fdc6c",
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
  "content_id": "e31d522c-e072-41fa-9132-d403c3dad081",
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
  "content_id": "8b30875d-aef8-4959-ab44-1eb554c5265a",
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
  "content_id": "ff78c963-947e-4d2e-bfff-2c66b70a3d5c",
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
  "content_id": "3a1d733e-5378-4d44-bf4b-14439eabeb84",
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
  "content_id": "ce41e390-edd4-4f57-94e6-0a4f494ce38c",
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
