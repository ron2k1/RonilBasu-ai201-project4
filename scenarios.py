"""
What my test runs.  (unit 8, Milestone 3)

`run_eval.py` runs every scenario here three times. The three test sets come
from criteria.md, and none of their texts or sources were used to calibrate
the signals in unit 7:

  SET_H  10 human texts published before 30 November 2022. Five casual
         (Hacker News comments, 2019) and five formal (two Stanford
         Encyclopedia of Philosophy preambles, three PubMed abstracts from
         2018). `scripts/fetch_set_h.py` picked them by a fixed rule and wrote
         them out; they are pasted here unchanged.
  SET_A  5 unedited outputs from claude-sonnet-5-5, each prompted on the same
         topic and register as a Set H text. The calibration set's AI texts
         came from a different model (claude-opus-5-5).
  SET_B  SET_A with light edits made by Claude Code to the criterion's recipe:
         contractions, a typo or two, one sentence split or merged. validate()
         checks every pair stays within 10% of words changed.

How each criterion uses them:

  1  SET_H. No piece gets "ai".
  2  SET_A against SET_H. At least 3 of 5 get "ai", and the mean confidence
     gap is at least 0.30.
  3  All 20 together for label coverage, and SET_B for the unsure half.
  4  An "appeals" scenario. The starter runner only posts to /submit, so I
     extended run_eval.py: it submits five texts, appeals each new
     content_id, appeals two made-up ids, then reads GET /log back and checks
     every line the criterion names.
  5  A "bodies" scenario with the eight bad bodies, sent exactly as written.
     run_eval.py counts audit lines before and after each one and posts to
     /ping after the batch.

`scripts/verdicts.py` reads the JSON that run_eval.py writes and applies each
criterion's target to each trial.
"""

import difflib


# ── Set H: human, published before 30 November 2022 ─────────────────────────
SET_H = [
    # hn_19276700 · 2019-03-01T00:00:13Z
    # https://news.ycombinator.com/item?id=19276700
    (
        "In the context of that, I'm fine with youtube's rule, but we were "
        "already off on a tangent in the meta discussion and that is clearly "
        "not the context of this particular discussion.\n\n"
        "Go up two levels if you don't believe me.\n\n"
        "We actually already have laws here in the US about signing up "
        "people under the age of 13 for online services and have since the "
        "90s. They're very lax and not enforced.\n\n"
        "A very large measure that YouTube could take is to hide all "
        "comments if you aren't signed in and strictly enforce the over 13 "
        "rule in the US (or whatever other rules elsewhere). But they don't "
        "do that."
    ),
    # hn_19276704 · 2019-03-01T00:00:29Z
    # https://news.ycombinator.com/item?id=19276704
    (
        "The tabs especially looks like a terrible idea. Something that had "
        "more than enough space on every screen has now become a huge, long "
        "list of options that you have to scan every time to find the one "
        "you want.\n\n"
        "Removal of icons also plays into that since they were the visual "
        "hooks you could use to navigate after a little while of usage.\n\n"
        "Then the final redesign, I’m not sure there’s anything to say about "
        "it other than that I strongly dislike it. Services like github "
        "change their image at their peril, and I just don’t think that is "
        "worth it."
    ),
    # hn_19276710 · 2019-03-01T00:01:19Z
    # https://news.ycombinator.com/item?id=19276710
    (
        "Definitely states the right problems, but not the right solutions.\n\n"
        "The commits box is also bigger than the files box, which doesn't "
        "make much sense. Whether a commit box even should be there is a big "
        "question. How useful is commits to the average developer browsing a "
        "repo? I think a bit useful, but not useful enough to have 1/3 of "
        "the screen width.\n\n"
        "Stats of a repo is pretty nice, because it gives an overview of how "
        "active it is, etc. But the problem is that majority of GitHub repos "
        "are empty and not that active, so it'll make most of the repos look "
        "like ghost towns. Not something you'd want on your site.\n\n"
        "Moving all git tabs into the GitHub tabs makes it even harder to "
        "use the UI. You have to spend way too much mental load just to find "
        "the right tab to click on. It looks better, but will be harder to "
        "use.\n\n"
        "The \"Watch\" button, moving description and tags is an improvement, "
        "and I'm for a redesign of some sort."
    ),
    # hn_19276711 · 2019-03-01T00:01:40Z
    # https://news.ycombinator.com/item?id=19276711
    (
        "They can take online payment from a bank account (such as after "
        "you’ve deposited a check from an auto loan) or they can take a "
        "physical bank draft (such as you would get from an auto loan) upon "
        "delivery. They drive the car to you either on a truck or on its own "
        "wheels, you do some paperwork, and 15 minutes later the delivery "
        "driver either hops in a Lyft or gets back in the semi truck.\n\n"
        "I’m sure credit card would work too if you had a high enough limit "
        "but those are the other options."
    ),
    # hn_19276730 · 2019-03-01T00:04:50Z
    # https://news.ycombinator.com/item?id=19276730
    (
        "The creation of an enemy and blaming them for all the problem seems "
        "to be one of the most successful ways to win election - this has "
        "been used in India since long before. Stirring up people's emotions "
        "and pitching them against each other will result in them fighting "
        "each other instead of uniting and questioning the politicians. "
        "Politicians will find and use any difference between people to "
        "split them - cast, religion, language, job, skin colour, food "
        "habits...\n\n"
        "There is nothing smart about what the people in the article are "
        "doing - they are just motivated by money and are leaving the world "
        "a much worse place for the next generation."
    ),
    # sep_medieval-emotions · Fall 2021 archive edition
    # https://plato.stanford.edu/archives/fall2021/entries/medieval-emotions/
    (
        "One of the many uses of the Greek word pathos in ancient philosophy "
        "referred, roughly speaking, to what we call emotions. The "
        "corresponding Latin terms were passio, affectus or affectio. "
        "Medieval theories of emotions were essentially based on ancient "
        "sources. The new developments included the discussion of emotions "
        "from the point of view of Avicennian faculty psychology, the "
        "production of systematic taxonomies particularly in "
        "thirteenth-century Aristotelianism, the detailed studies of "
        "voluntary and involuntary aspects of emotional reactions, as well "
        "as late medieval re-evaluations of the sharp divide between the "
        "emotions and the will."
    ),
    # sep_science-mechanisms · Fall 2021 archive edition
    # https://plato.stanford.edu/archives/fall2021/entries/science-mechanisms/
    (
        "Around the turn of the twenty-first century, what has come to be "
        "called the new mechanical philosophy (or, for brevity, the new "
        "mechanism) emerged as a framework for thinking about the "
        "philosophical assumptions underlying many areas of science, "
        "especially in sciences such as biology, neuroscience, and "
        "psychology. In this entry, we introduce and summarize the "
        "distinctive features of this framework, and we discuss how it "
        "addresses a range of classic issues in the philosophy of science, "
        "including explanation, metaphysics, the relations between "
        "scientific disciplines, and the process of scientific discovery. "
        "For each of these issues, we show how the mechanistic framework has "
        "reoriented philosophical work, what the new mechanism has "
        "contributed to the discussion, and what remains to be done."
    ),
    # pubmed_32104452 · 2018-06-01
    # https://pubmed.ncbi.nlm.nih.gov/32104452/
    (
        "Low drug loading efficiency is one of the main obstacles hindering "
        "the application of contact lenses (CLs) as the carrier for extended "
        "ocular drug delivery. Here in this study, a simple and effective "
        "drug loading method based on salt induced modulation was proposed "
        "and demonstrated with mechanism elucidation. First of all, using "
        "poly (2-hydroxyethyl methacrylate) (p-HEMA) as the contact lens "
        "material, betaxolol hydrochloride, Diclofenac Sodium and Betaxolol "
        "Base as the model drugs with different solubility, influence of "
        "salt concentration, salt type (sodium salts of sulfate, chloride, "
        "and sulfocyanate) and drug properties in the loading solution on "
        "drug loading efficiency was investigated. Mechanism of enhanced "
        "drug loading in contact lens was further explored via studying the "
        "influence of salt on the absorption isotherm, drug solubility and "
        "water content of CLs. Applicability of this method to other CLs "
        "materials was also investigated. It was demonstrated that adjusting "
        "the ionic strength of loading solutions resulted in significant "
        "increase of drug loading in CLs. Type and concentration of the "
        "salts and solubility of the drug were the main factors influencing "
        "enhancement ratio of drug loading. The mechanism for improved drug "
        "loading was related to the reduced drug solubility in loading "
        "solutions and the reduced bound water content in contact lenses. "
        "Modulation of drug loading by adjusting ionic strength was also "
        "applicable to other CLs and the light transmittance was not "
        "affected. This method was more suitable for salt-form drugs with "
        "high solubility. In summary, adjusting ionic strength of loading "
        "solution is an economical and effective way to improve drug loading "
        "in CLs, and this simple method may also find application in other "
        "hydrogel based drug delivery systems."
    ),
    # pubmed_31360849 · 2018-06-01
    # https://pubmed.ncbi.nlm.nih.gov/31360849/
    (
        "In response to the rising cost of cancer drugs, the National "
        "Comprehensive Cancer Network (NCCN) recently developed a value "
        "framework, known as \"Evidence Blocks,\" to grade the efficacy, "
        "safety, evidence quality, evidence consistency, and affordability "
        "of treatments included in its clinical guidelines. The value scores "
        "were available for 55 of the 69 new cancer drugs approved by the US "
        "Food and Drug Administration from 2007 to 2016. Overall, the "
        "treatment costs for 95% of new cancer medicines in NCCN clinical "
        "guidelines were scored as \"very expensive\" or \"expensive\". In "
        "multivariable ordered logistic regression models, there was no "
        "association between the affordability of new cancer drugs and "
        "efficacy and safety data available in clinical guidelines. Most "
        "guideline-recommended drugs were subject to annual list price "
        "increases exceeding inflation."
    ),
    # pubmed_31355352 · 2018-06-01
    # https://pubmed.ncbi.nlm.nih.gov/31355352/
    (
        "Present bioprinting techniques lack the methodology to print with "
        "bioactive materials that retain their biological functionalities. "
        "This constraint is due to the fact that extrusion-based printing of "
        "synthetic polymers is commonly performed at very high temperatures "
        "in order to achieve desired mechanical properties and printing "
        "resolutions. Consequently, current methodology prevents printing "
        "scaffolds embedded with bioactive molecules, such as growth "
        "factors. With the wide use of mesenchymal stem cells (MSCs) in "
        "regenerative medicine research, the integration of growth factors "
        "into 3D printed scaffolds is critical because it can allow for "
        "inducible MSC differentiation. We have successfully incorporated "
        "growth factors into extrusion printed poly (lactic-co-glycolic "
        "acid) (PLGA) scaffolds by introducing dimethyl sulfoxide (DMSO) for "
        "low temperature printing. Mechanical testing results demonstrated "
        "significantly different compressive and tensile properties for PLGA "
        "scaffold printed with or without DMSO. In particular, the PLGA-DMSO "
        "scaffold displayed a highly stretchable feature compared to the "
        "regular PLGA scaffold. The cellular response of growth factor "
        "introduction was evaluated in vitro using human mesenchymal stem "
        "cells (hMSCs). By evaporating the DMSO after printing, we ensured "
        "that there was no cytotoxic effect on seeded hMSCs. The addition of "
        "lineage specific growth factors led to increased expression of "
        "corresponding genetic markers for chondrogenesis, osteogenesis, and "
        "adipogenesis. We concluded that the use of DMSO for 3D printed "
        "scaffold fabrication with bioactive items is a revolutionary "
        "methodology in advancing regenerative medicine. The incorporation "
        "of bioactive molecules opens pathways to more therapeutic uses for "
        "3D printing in treating damaged or deteriorating native tissue."
    ),
]

# ── Set A: unedited model output ─────────────────────────────────────────────
SET_A = [
    # A1, claude-sonnet-5-5, unedited. Matched to hn_19276704 / hn_19276710.
    # Prompt: Write a Hacker News comment (100 to 160 words) reacting to a blog
    #   post that proposes redesigning the GitHub repository page: the tabs get
    #   merged into one long list, the icons are removed, and a big stats panel
    #   and commits box are added.
    (
        "I think the idea is interesting but I'd be wary of calling it an "
        "improvement. Tabs exist because people arrive at a repo with "
        "different goals, and a single long list means everyone has to "
        "scroll past what they don't care about to reach what they do. "
        "Removing the icons also hurts scanning, since the eye picks up a "
        "shape faster than it reads a word. The stats panel looks nice in a "
        "mockup, but how many people actually decide anything from star "
        "counts and contributor graphs on the first screen? A commits box is "
        "useful, but GitHub already surfaces the latest commit right above "
        "the file tree. I'd like to see some usage data or even a quick A/B "
        "test before accepting that this is better than what we have. "
        "Mockups always look cleaner than real repos with messy data."
    ),
    # A2, claude-sonnet-5-5, unedited. Matched to hn_19276711.
    # Prompt: Write a Hacker News comment (90 to 140 words) answering someone
    #   who asked how payment and delivery actually work when you buy a Tesla
    #   Model 3 online.
    (
        "It's pretty straightforward, and honestly a bit different from a "
        "dealership. You configure the car on Tesla's site, put down a small "
        "refundable order deposit, and then you wait for a delivery window. "
        "Once the car is assigned to you, you finalize the payment in your "
        "Tesla account. That means either paying cash by wire transfer, or "
        "setting up financing through Tesla or your own bank or credit "
        "union. If you have a trade-in, you submit photos and get an offer "
        "online. Delivery usually happens at a Tesla center or you can "
        "sometimes get it at home, and you do a quick walkaround to check "
        "for paint or panel issues before you sign off and take the keys, or "
        "really the phone app. Just inspect the car carefully, because "
        "that's your best chance to flag problems."
    ),
    # A3, claude-sonnet-5-5, unedited. Matched to hn_19276700.
    # Prompt: Write a Hacker News comment (100 to 150 words) responding to the
    #   news that YouTube is disabling comments on most videos that feature
    #   young children.
    (
        "I understand why YouTube is doing this, but it feels like a blunt "
        "tool applied to a much harder problem. Predators exploiting comment "
        "sections on videos of kids is a real issue and has been for years, "
        "so I can see why the company would rather turn off comments than "
        "keep playing whack-a-mole. The downside is that plenty of innocent "
        "channels, like family vloggers, kids' educational creators, and "
        "small gymnastics or dance teams, lose a big part of how they talk "
        "with their audience. Comments also drive engagement, so this hits "
        "their income too. The real question is whether this is about child "
        "safety or about avoiding legal and advertiser trouble. Probably "
        "both. I'd rather see better moderation and detection than just "
        "shutting everything off, but I realize that costs real money at "
        "YouTube's scale."
    ),
    # A4, claude-sonnet-5-5, unedited. Matched to sep_medieval-emotions.
    # Prompt: Write the opening summary paragraph (90 to 140 words) of an
    #   encyclopedia of philosophy entry on medieval theories of the emotions.
    (
        "Medieval theories of the emotions developed out of an inherited "
        "body of ancient material, above all Aristotle's psychology, Stoic "
        "and Augustinian moral analysis, and the physiological treatises of "
        "the Greek and Arabic medical traditions. Thinkers from the early "
        "Middle Ages through the fourteenth century asked what the emotions, "
        "or passions of the soul, actually are, how they relate to the body "
        "and to the cognitive and appetitive powers of the soul, and what "
        "role they should play in moral life. Most authors treated emotions "
        "as movements of the sensitive appetite that arise in response to "
        "perceived good or evil, while debating whether they are "
        "fundamentally bodily changes, acts of judgment, or something "
        "between the two. The tradition also explored how passions bear on "
        "virtue, free will, and sin."
    ),
    # A5, claude-sonnet-5-5, unedited. Matched to pubmed_31360849.
    # Prompt: Write a scientific abstract (120 to 180 words) for a study that
    #   examined whether the prices of new cancer drugs approved by the FDA
    #   between 2007 and 2016 were related to their efficacy and safety ratings
    #   in clinical practice guidelines.
    (
        "Background: Prices of new cancer drugs in the United States "
        "continue to rise, yet it is unclear whether higher prices reflect "
        "greater clinical value. Objective: To determine whether the prices "
        "of new cancer drugs approved by the US Food and Drug Administration "
        "(FDA) between 2007 and 2016 were associated with their efficacy and "
        "safety ratings in clinical practice guidelines. Methods: We "
        "identified all new oncology drugs approved during the study period "
        "and obtained their launch prices. Efficacy and safety scores for "
        "each drug were taken from the National Comprehensive Cancer Network "
        "Evidence Blocks, which rate the quality of evidence, affordability, "
        "and clinical performance. We used regression models to assess the "
        "relationship between monthly drug price and these ratings, "
        "adjusting for relevant covariates. Results: Drug prices were not "
        "significantly associated with efficacy or safety ratings. "
        "Conclusions: Prices of new cancer drugs appear to be unrelated to "
        "their clinical value as judged by guideline panels, which raises "
        "concerns about current pricing practices and suggests that "
        "policymakers may need new approaches to align price with value."
    ),
]

# ── Set B: Set A, lightly edited ─────────────────────────────────────────────
SET_B = [
    # B1 = A1 with: contraction (idea is -> idea's); one sentence split at
    #   'different goals'; typos 'scaning', 'then' for 'than'
    (
        "I think the idea's interesting but I'd be wary of calling it an "
        "improvement. Tabs exist because people arrive at a repo with "
        "different goals. A single long list means everyone has to scroll "
        "past what they don't care about to reach what they do. Removing the "
        "icons also hurts scaning, since the eye picks up a shape faster "
        "than it reads a word. The stats panel looks nice in a mockup, but "
        "how many people actually decide anything from star counts and "
        "contributor graphs on the first screen? A commits box is useful, "
        "but GitHub already surfaces the latest commit right above the file "
        "tree. I'd like to see some usage data or even a quick A/B test "
        "before accepting that this is better than what we have. Mockups "
        "always look cleaner then real repos with messy data."
    ),
    # B2 = A2 with: contraction (car is -> car's); two sentences merged at
    #   'Tesla account'; typo 'refundible', 'carefuly'
    (
        "It's pretty straightforward, and honestly a bit different from a "
        "dealership. You configure the car on Tesla's site, put down a small "
        "refundible order deposit, and then you wait for a delivery window. "
        "Once the car's assigned to you, you finalize the payment in your "
        "Tesla account, which means either paying cash by wire transfer, or "
        "setting up financing through Tesla or your own bank or credit "
        "union. If you have a trade-in, you submit photos and get an offer "
        "online. Delivery usually happens at a Tesla center or you can "
        "sometimes get it at home, and you do a quick walkaround to check "
        "for paint or panel issues before you sign off and take the keys, or "
        "really the phone app. Just inspect the car carefuly, because that's "
        "your best chance to flag problems."
    ),
    # B3 = A3 with: contraction (YouTube is -> YouTube's); 'Probably both.'
    #   merged into the sentence before; typos 'engagment', 'moderaton'
    (
        "I understand why YouTube's doing this, but it feels like a blunt "
        "tool applied to a much harder problem. Predators exploiting comment "
        "sections on videos of kids is a real issue and has been for years, "
        "so I can see why the company would rather turn off comments than "
        "keep playing whack-a-mole. The downside is that plenty of innocent "
        "channels, like family vloggers, kids' educational creators, and "
        "small gymnastics or dance teams, lose a big part of how they talk "
        "with their audience. Comments also drive engagment, so this hits "
        "their income too. The real question is whether this is about child "
        "safety or about avoiding legal and advertiser trouble, probably "
        "both. I'd rather see better moderaton and detection than just "
        "shutting everything off, but I realize that costs real money at "
        "YouTube's scale."
    ),
    # B4 = A4 with: one sentence split at 'good or evil'; contraction (they are
    #   -> they're); typos 'physiologcal', 'fourteeth'
    (
        "Medieval theories of the emotions developed out of an inherited "
        "body of ancient material, above all Aristotle's psychology, Stoic "
        "and Augustinian moral analysis, and the physiologcal treatises of "
        "the Greek and Arabic medical traditions. Thinkers from the early "
        "Middle Ages through the fourteeth century asked what the emotions, "
        "or passions of the soul, actually are, how they relate to the body "
        "and to the cognitive and appetitive powers of the soul, and what "
        "role they should play in moral life. Most authors treated emotions "
        "as movements of the sensitive appetite that arise in response to "
        "perceived good or evil. They debated whether they're fundamentally "
        "bodily changes, acts of judgment, or something between the two. The "
        "tradition also explored how passions bear on virtue, free will, and "
        "sin."
    ),
    # B5 = A5 with: contractions (it is -> it's, were not -> weren't); one
    #   sentence split at 'study period'; typo 'covariats'
    (
        "Background: Prices of new cancer drugs in the United States "
        "continue to rise, yet it's unclear whether higher prices reflect "
        "greater clinical value. Objective: To determine whether the prices "
        "of new cancer drugs approved by the US Food and Drug Administration "
        "(FDA) between 2007 and 2016 were associated with their efficacy and "
        "safety ratings in clinical practice guidelines. Methods: We "
        "identified all new oncology drugs approved during the study period. "
        "We obtained their launch prices. Efficacy and safety scores for "
        "each drug were taken from the National Comprehensive Cancer Network "
        "Evidence Blocks, which rate the quality of evidence, affordability, "
        "and clinical performance. We used regression models to assess the "
        "relationship between monthly drug price and these ratings, "
        "adjusting for relevant covariats. Results: Drug prices weren't "
        "significantly associated with efficacy or safety ratings. "
        "Conclusions: Prices of new cancer drugs appear to be unrelated to "
        "their clinical value as judged by guideline panels, which raises "
        "concerns about current pricing practices and suggests that "
        "policymakers may need new approaches to align price with value."
    ),
]

# ── Criterion 4: the appeal path ─────────────────────────────────────────────
# The reasoning has a newline, an em dash and an accented letter in it, so
# "the exact reasoning text" is checked on more than plain ASCII. {trial} and
# {i} make every appeal's text unique, so a line from one trial can't pass
# for another.
APPEAL_REASONING = (
    "I wrote this post myself and I still have the drafts, dated before I "
    "posted it.\nTrial {trial}, appeal {i}: happy to share them with a "
    "reviewer — my café notes too."
)

# A well-formed id that was never issued. run_eval.py adds a second made-up
# id at run time: the first real content_id with its last character changed,
# which is the typo a writer would actually make.
MADE_UP_ID = "00000000-0000-4000-8000-000000000000"


# ── Criterion 5: the eight bad bodies, in criteria.md's order ────────────────
BAD_BODIES = [
    {"creator_id": "eval_bad_1"},                                 # 1 no text field
    {"text": None, "creator_id": "eval_bad_2"},                   # 2 text is null
    {"text": "", "creator_id": "eval_bad_3"},                     # 3 text is ""
    {"text": "   \n\n  \t \n ", "creator_id": "eval_bad_4"},      # 4 spaces and newlines
    {"text": 12345, "creator_id": "eval_bad_5"},                  # 5 text is a number
    [{"text": SET_H[0], "creator_id": "eval_bad_6"}],             # 6 a JSON list
    {"text": "word " * 50_000, "creator_id": "eval_bad_7"},       # 7 250,000 characters
    {"text": "This has only five words.", "creator_id": "eval_bad_8"},  # 8 five words
]


SCENARIOS = [
    {"name": "set_h_human", "criterion": 1, "texts": SET_H},
    {"name": "set_a_ai", "criterion": 2, "texts": SET_A},
    {"name": "set_b_edited", "criterion": 3, "texts": SET_B},
    {
        "name": "appeals",
        "criterion": 4,
        "appeals": {
            "texts": SET_H[:5],
            "reasoning": APPEAL_REASONING,
            "made_up_id": MADE_UP_ID,
        },
    },
    {"name": "bad_input", "criterion": 5, "bodies": BAD_BODIES},
]


def words_changed(original: str, edited: str) -> float:
    """Share of the original's words that an edit changed, added or removed."""
    a, b = original.split(), edited.split()
    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    kept = sum(block.size for block in matcher.get_matching_blocks())
    return (max(len(a), len(b)) - kept) / len(a)


def check_sets() -> list[str]:
    """The test sets have to be what criteria.md says they are."""
    problems = []
    for name, items, size in (("SET_H", SET_H, 10), ("SET_A", SET_A, 5), ("SET_B", SET_B, 5)):
        if len(items) != size:
            problems.append(f"{name} has {len(items)} texts; criteria.md says {size}")
        for i, text in enumerate(items, 1):
            n = len(text.split())
            if not 80 <= n <= 300:
                problems.append(f"{name}[{i}] is {n} words; criteria.md says 80 to 300")
    for i, (a, b) in enumerate(zip(SET_A, SET_B), 1):
        share = words_changed(a, b)
        if share > 0.10:
            problems.append(f"SET_B[{i}] changes {share:.0%} of SET_A[{i}]'s words; the cap is 10%")
        if share == 0:
            problems.append(f"SET_B[{i}] is identical to SET_A[{i}]")
    return problems


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is exempt from the empty check, because an empty
    string is the whole point of a bad-input case. It may also hold a JSON
    list, since criterion 5 sends one on purpose.
    """
    problems = check_sets()
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        kinds = [k for k in ("texts", "bodies", "appeals") if scenario.get(k)]
        if len(kinds) != 1:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') needs exactly one of "
                f"texts, bodies or appeals; it has {kinds or 'none'}"
            )
            continue

        if kinds == ["appeals"]:
            spec = scenario["appeals"]
            if not spec.get("texts") or not spec.get("reasoning") or not spec.get("made_up_id"):
                problems.append(f"scenario {i}: appeals needs texts, reasoning and made_up_id")
            continue

        if kinds == ["bodies"]:
            for j, body in enumerate(scenario["bodies"], 1):
                if not isinstance(body, (dict, list)):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict or list. Bodies are "
                        f"whole request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        for j, text in enumerate(scenario["texts"], 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty. If an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
