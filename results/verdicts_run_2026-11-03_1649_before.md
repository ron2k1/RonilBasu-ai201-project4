# Verdicts for `run_2026-11-03_1649_before.json`

- Produced by: `scripts/verdicts.py::main` from `run_eval.py`'s JSON
- A criterion is MET only if its target holds in every trial.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1 | 0 of 10 Set H get ai | 0/10 ai ✓ | 0/10 ai ✓ | 0/10 ai ✓ | MET |
| 2 | >= 3 of 5 Set A get ai, and mean confidence A - H >= 0.30 | 0/5 ai, gap +0.051 ✗ | 0/5 ai, gap +0.051 ✗ | 0/5 ai, gap +0.051 ✗ | MISSED |
| 3 | ai, unsure, human each >= 2 of all 20; >= 3 of 5 Set B unsure | ai 0 · unsure 12 · human 8; B unsure 2/5 ✗ | ai 0 · unsure 12 · human 8; B unsure 2/5 ✗ | ai 0 · unsure 12 · human 8; B unsure 2/5 ✗ | MISSED |
| 4 | 7 of 7 appeal checks | 7/7 ✓ | 7/7 ✓ | 7/7 ✓ | MET |
| 5 | 8 of 8 bad bodies: 4xx + error field + one rejected line; /ping answers | 8/8, ping ok ✓ | 8/8, ping ok ✓ | 8/8, ping ok ✓ | MET |

## Every scored text

guess, combined score, and the two signals (m = model, s = style).

| Text | Sent | Run 1 | Run 2 | Run 3 |
|---|---|---|---|---|
| H1 | In the context of that, I'm fine with yo | human 0.4273 (m 0.380, s 0.451) | human 0.4273 (m 0.380, s 0.451) | human 0.4273 (m 0.380, s 0.451) |
| H2 | The tabs especially looks like a terribl | unsure 0.5968 (m 0.354, s 0.718) | unsure 0.5968 (m 0.354, s 0.718) | unsure 0.5968 (m 0.354, s 0.718) |
| H3 | Definitely states the right problems, bu | unsure 0.4664 (m 0.434, s 0.483) | unsure 0.4664 (m 0.434, s 0.483) | unsure 0.4664 (m 0.434, s 0.483) |
| H4 | They can take online payment from a bank | human 0.3262 (m 0.282, s 0.348) | human 0.3262 (m 0.282, s 0.348) | human 0.3262 (m 0.282, s 0.348) |
| H5 | The creation of an enemy and blaming the | unsure 0.6340 (m 0.348, s 0.777) | unsure 0.6340 (m 0.348, s 0.777) | unsure 0.6340 (m 0.348, s 0.777) |
| H6 | One of the many uses of the Greek word p | human 0.3490 (m 0.299, s 0.374) | human 0.3490 (m 0.299, s 0.374) | human 0.3490 (m 0.299, s 0.374) |
| H7 | Around the turn of the twenty-first cent | unsure 0.6199 (m 0.694, s 0.583) | unsure 0.6199 (m 0.694, s 0.583) | unsure 0.6199 (m 0.694, s 0.583) |
| H8 | Low drug loading efficiency is one of th | human 0.3369 (m 0.510, s 0.250) | human 0.3369 (m 0.510, s 0.250) | human 0.3369 (m 0.510, s 0.250) |
| H9 | In response to the rising cost of cancer | human 0.3929 (m 0.569, s 0.305) | human 0.3929 (m 0.569, s 0.305) | human 0.3929 (m 0.569, s 0.305) |
| H10 | Present bioprinting techniques lack the  | unsure 0.5613 (m 0.510, s 0.587) | unsure 0.5613 (m 0.510, s 0.587) | unsure 0.5613 (m 0.510, s 0.587) |
| A1 | I think the idea is interesting but I'd  | unsure 0.5805 (m 0.189, s 0.776) | unsure 0.5805 (m 0.189, s 0.776) | unsure 0.5805 (m 0.189, s 0.776) |
| A2 | It's pretty straightforward, and honestl | unsure 0.4663 (m 0.345, s 0.527) | unsure 0.4663 (m 0.345, s 0.527) | unsure 0.4663 (m 0.345, s 0.527) |
| A3 | I understand why YouTube is doing this,  | unsure 0.5515 (m 0.289, s 0.683) | unsure 0.5515 (m 0.289, s 0.683) | unsure 0.5515 (m 0.289, s 0.683) |
| A4 | Medieval theories of the emotions develo | unsure 0.4728 (m 0.340, s 0.539) | unsure 0.4728 (m 0.340, s 0.539) | unsure 0.4728 (m 0.340, s 0.539) |
| A5 | Background: Prices of new cancer drugs i | unsure 0.5383 (m 0.693, s 0.461) | unsure 0.5383 (m 0.693, s 0.461) | unsure 0.5383 (m 0.693, s 0.461) |
| B1 | I think the idea's interesting but I'd b | unsure 0.5962 (m 0.162, s 0.814) | unsure 0.5962 (m 0.162, s 0.814) | unsure 0.5962 (m 0.162, s 0.814) |
| B2 | It's pretty straightforward, and honestl | human 0.4367 (m 0.307, s 0.501) | human 0.4367 (m 0.307, s 0.501) | human 0.4367 (m 0.307, s 0.501) |
| B3 | I understand why YouTube's doing this, b | unsure 0.6544 (m 0.247, s 0.858) | unsure 0.6544 (m 0.247, s 0.858) | unsure 0.6544 (m 0.247, s 0.858) |
| B4 | Medieval theories of the emotions develo | human 0.3653 (m 0.274, s 0.411) | human 0.3653 (m 0.274, s 0.411) | human 0.3653 (m 0.274, s 0.411) |
| B5 | Background: Prices of new cancer drugs i | human 0.4144 (m 0.650, s 0.296) | human 0.4144 (m 0.650, s 0.296) | human 0.4144 (m 0.650, s 0.296) |
