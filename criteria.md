# Acceptance criteria: Provenance Guard

Written in unit 7, before `/submit` returned a single score. Unit 8 runs each
one three times, and a target only counts as met if it holds in all three.

## The test sets these criteria name

None of these texts are used to tune the signals in unit 7. They get built in
unit 8 inside `scenarios.py`, from sources the calibration set never touched.

- **Set H, human (10 pieces).** Real human writing, 80 to 300 words each, all
  published before 30 November 2022 (the day ChatGPT came out), so none of it
  can be AI. Five are plain and casual (forum posts). Five are formal
  (encyclopedia or academic prose).
- **Set A, clearly AI (5 pieces).** Language-model output with no edits, 80 to
  300 words, on the same kinds of topics and in the same registers as Set H.
- **Set B, borderline (5 pieces).** Language-model output that a person then
  lightly edited: contractions, a typo or two, one sentence split or merged,
  with no more than 10% of the words changed.

---

## 1. No human writing gets the AI label

Of the 10 pieces in Set H, **0** get `guess: "ai"`, in each of the three
trials.

**Why this target:** a wrong accusation lands on one person and nothing
undoes it. With 10 pieces the smallest failure rate I can even observe is 1 in
10, and I would not accept a 1 in 10 chance of being called a cheater for
something I wrote. At this sample size, zero is the only target that means
rare.

---

## 2. The detector still catches unedited AI text

At least **3 of the 5** pieces in Set A get `guess: "ai"`, and the mean
`confidence` of Set A is at least **0.30 higher** than the mean of Set H, in
each of the three trials.

**Why this target:** a service that never says "AI" passes criterion 1 for
free. This criterion stops me from buying zero false positives by making the
detector useless. I ask for 3 of 5 rather than 5 of 5 because missing some AI
text is the cheaper mistake, and my thresholds are set to make that trade on
purpose. The 0.30 gap is about the width an unsure band needs. If the two
sets sit closer than that, any threshold that leaves room for doubt has
human and AI text inside the same band, and the score is not separating them.

---

## 3. All three labels are reachable, and borderline text lands in the middle

Across all 20 inputs (Sets H, A and B together), each of `ai`, `unsure` and
`human` appears **at least 2 times** in every trial. Separately, at least
**3 of the 5** pieces in Set B get `guess: "unsure"`.

**Why this target:** a label no real text can reach is a label that does not
exist, and a gap in the bands would hide it. The Set B half checks that the
unsure label does its job. Lightly edited AI is the honest middle case, and
if most of it lands at either end, the unsure band is not catching what it is
there for.

---

## 4. Every appeal changes the status and is recorded

For 5 appeals against real `content_id`s from earlier submissions, **5 of 5**
return `200` with `status: "under_review"`, and `GET /log` shows both:

- the original decision line, unchanged, still `status: "decided"`, and
- a later appeal line with the same `content_id`, the exact reasoning text,
  and `status: "under_review"`.

For 2 appeals with made-up `content_id`s, **2 of 2** return `404` and add no
appeal line to the log. That is 7 of 7 in each of the three trials.

**Why this target:** the appeal is the only remedy for a criterion 1 failure.
It is plain code with no model in it, so anything short of every time is a
bug, and that bug leaves a wrongly accused writer with nothing. The 404 half
matters because a typo in a content id that quietly "succeeds" looks like a
filed appeal to the writer and is lost for good.

---

## 5. Bad input is refused cleanly and leaves a trace

These 8 bodies sent to `POST /submit`:

1. no `text` field
2. `text` is `null`
3. `text` is `""`
4. `text` is only spaces and newlines
5. `text` is a number
6. the body is a JSON list instead of an object
7. `text` is 250,000 characters long
8. `text` is five words

**8 of 8** get a `4xx` status (never a `500`, never a `200` with a label), each
with a JSON body that has an `error` field, and each writes one `rejected`
line to the audit log. `POST /ping` still answers after the batch. This holds
in each of the three trials.

**Why this target:** an input that crashes the route takes the service down
for every writer, and a `500` tells the person nothing about what to fix. A
five-word text getting a label would be a guess dressed up as a judgment, so
it gets refused instead. The log line matters because a refused request that
leaves no trace is invisible, and an attack that shows up only as an absence
never gets found.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
