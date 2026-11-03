#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /content/<id> one item's decision and review status (stretch)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import uuid

from flask import Flask, jsonify, request
from werkzeug.exceptions import RequestEntityTooLarge

import audit
import config
import detector
import scoring
import stylometry

app = Flask(__name__)

# Flask refuses any body over this with a 413 the moment a route reads it,
# before the route's own checks run. The handler below makes that 413 JSON
# and leaves a trace, like every other refusal.
app.config["MAX_CONTENT_LENGTH"] = config.MAX_REQUEST_BYTES


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def _json_body() -> dict:
        """The request's JSON object, or {} when there isn't one to read."""
        try:
            payload = request.get_json(silent=True)
        except RequestEntityTooLarge:
            # silent= only covers bad JSON. A body over MAX_REQUEST_BYTES
            # raises while it's read, and if that happens here the limiter
            # never records the hit, so an oversized flood would never reach
            # a 429. The route reads it again and refuses it with a 413.
            return {}
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        return payload if isinstance(payload, dict) else {}

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.

        The id is cleaned the same way the log cleans it, so " bob" and "bob "
        share bob's budget, and an id too long to log falls back to the
        address instead of becoming a new key of any size.
        """
        return _clean_creator_id(_json_body().get("creator_id")) or get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        strategy=config.RATE_LIMIT_STRATEGY,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        audit.log_rejection(
            creator_id=_clean_creator_id(_json_body().get("creator_id")) or "unknown",
            reason="rate_limited",
            route=request.path,
            http_status=429,
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── YOU BUILD THIS ────────────────────────────────────────────────────────────

@app.post("/submit")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.
    ← TODO — Milestones 3, 4 and 5

    Expects JSON:
        {"text": "...", "creator_id": "..."}

    Should return JSON with, at minimum:
        {"content_id": "...", "guess": "...", "confidence": 0.0, "label": "...",
         "model_score": 0.0, "style_score": 0.0}

    ⚠️ **Both signal scores go in the response, not just the log.** Unit 8's
    `run_attacks.py` and `run_eval.py` read `model_score` and `style_score`
    straight off this response and put them in your reports. Leave them out and
    every row of next unit's evidence says `null` — which is exactly the
    diagnostic you need to name a stage and a mechanism. You do not want to
    find that out after running the attack set.

    ─────────────────────────────────────────────────────────────────────────
    Build it in three passes. Do not skip ahead — the ordering is how you tell
    a broken route from a broken signal.

    **Milestone 3 — the route answers.**
      1. Return a hardcoded response. Confirm `curl` gets it back before you
         add any logic at all.
      2. Then pull `text` and `creator_id` out of the payload.
      3. Then call ONE signal — `detector.model_signal(text)` — and put the
         real number in. Leave confidence and label as placeholders.
      4. Log every submission with `audit.log_decision(...)`. The content_id
         matters: `/appeal` needs it, and a student who skips it rebuilds this
         whole flow later.

    **Milestone 4 — the second signal and the score.**
      5. Add `stylometry.style_signal(text)`.
      6. Combine them with `scoring.combine_signals(...)`.
      7. Log BOTH signal scores alongside the combined one, and put them in the
         response too. Next unit you can't diagnose anything without them.

    **Milestone 5 — the label.**
      8. `scoring.score_to_label(...)` and put the real label in the response.

    ─────────────────────────────────────────────────────────────────────────
    Worth deciding early, because unit 8's attack set will decide it for you:
    what should this do when `text` is missing, empty, or enormous? A crash on
    a malformed input is one of the most common real failures there is.

    The answer is in docs/trace.md, section 4: every bad body is a 4xx with a
    JSON `error`, and a `rejected` line in the log.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _refuse(400, "invalid_json",
                       "Send a JSON object with \"text\" and \"creator_id\".")

    creator_id = _clean_creator_id(payload.get("creator_id"))
    raw_text = payload.get("text")

    if not isinstance(raw_text, str) or not raw_text.strip():
        return _refuse(400, "missing_text",
                       "There's no text to look at. Send the writing as \"text\".",
                       creator_id=creator_id)
    if creator_id is None:
        return _refuse(400, "missing_creator_id",
                       f"\"creator_id\" must be a non-empty string of at most "
                       f"{config.MAX_CREATOR_ID_CHARS} characters.")

    text = raw_text.strip()
    if len(text) > config.MAX_TEXT_CHARS:
        return _refuse(413, "text_too_long",
                       f"That's {len(text):,} characters. The limit is "
                       f"{config.MAX_TEXT_CHARS:,}.",
                       creator_id=creator_id, text_chars=len(text))

    word_count = len(stylometry.words(text))
    if word_count < config.MIN_WORDS:
        return _refuse(422, "text_too_short",
                       f"This is {word_count} words. We need at least "
                       f"{config.MIN_WORDS} to say anything useful about how it "
                       f"was written, so we haven't labelled it.",
                       creator_id=creator_id, word_count=word_count)

    try:
        model_score = detector.model_signal(text)
    except (detector.DetectorUnavailable, ValueError) as exc:
        # ValueError is GPT-2 finding too few tokens. MIN_WORDS should stop
        # that first, so reaching here means the two disagree about length.
        return _refuse(503, "detector_unavailable",
                       "We couldn't check this right now. Nothing was decided "
                       "about your writing. Please try again later.",
                       creator_id=creator_id, detail=type(exc).__name__)

    style_score = stylometry.style_signal(text)
    confidence = scoring.combine_signals(model_score, style_score)
    guess, label = scoring.score_to_label(confidence)

    content_id = str(uuid.uuid4())
    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=confidence,
        label=label,
        status="decided",
        word_count=word_count,
        text_preview=text[:80],
    )

    return jsonify({
        "content_id": content_id,
        "creator_id": creator_id,
        "guess": guess,
        "confidence": confidence,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
        "status": "decided",
    })


def _clean_creator_id(value):
    """The creator id if it's usable, else None."""
    if not isinstance(value, str):
        return None
    value = value.strip()
    if not value or len(value) > config.MAX_CREATOR_ID_CHARS:
        return None
    return value


def _refuse(status: int, error: str, message: str, creator_id=None, **extra):
    """
    Turn a request away with a JSON reason, and leave a trace in the log.

    A refused request that writes nothing looks exactly like no request at
    all, so every refusal gets a `rejected` line.
    """
    audit.log_rejection(
        creator_id=creator_id or "unknown",
        reason=error,
        route=request.path,
        http_status=status,
        **extra,
    )
    return jsonify({"error": error, "message": message}), status


@app.errorhandler(RequestEntityTooLarge)
def request_too_large(exc):
    """Bodies over MAX_REQUEST_BYTES are refused when the route reads them. Refuse them in JSON."""
    return _refuse(413, "request_too_large",
                   f"That request is over {config.MAX_REQUEST_BYTES // 1024} KB. "
                   f"The text limit is {config.MAX_TEXT_CHARS:,} characters.")


@app.post("/appeal")
def appeal():
    """
    A writer says you got it wrong. ← TODO — Milestone 5

    Expects JSON:
        {"content_id": "...", "reasoning": "..."}

    Should:
      1. Check the content_id actually exists — `audit.entries_for(id)` tells
         you. A typo here fails silently and looks like a broken endpoint,
         which is the single most common way this milestone eats an hour.
      2. Record the appeal with `audit.log_appeal(...)`, which moves the item
         to `under_review`.
      3. Confirm to the writer. No automatic re-checking needed.

    This is the smallest endpoint in the project and the one that matters most
    to the person on the other end. It's the only thing standing between a
    wrong accusation and nothing at all.

    Contract: docs/trace.md, section 4. A second appeal on the same item is
    allowed and logged too; the writer may have more to add.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _refuse(400, "invalid_json",
                       "Send a JSON object with \"content_id\" and \"reasoning\".")

    content_id = payload.get("content_id")
    if not isinstance(content_id, str) or not content_id.strip():
        return _refuse(400, "missing_content_id",
                       "Send the \"content_id\" you got back when you submitted.")
    content_id = content_id.strip()

    reasoning = payload.get("reasoning")
    if not isinstance(reasoning, str) or not reasoning.strip():
        return _refuse(400, "missing_reasoning",
                       "Tell us in a sentence or two why the label is wrong, "
                       "as \"reasoning\".")
    reasoning = reasoning.strip()
    if len(reasoning) > config.MAX_APPEAL_CHARS:
        return _refuse(413, "reasoning_too_long",
                       f"That's {len(reasoning):,} characters. Please keep it "
                       f"under {config.MAX_APPEAL_CHARS:,}.")

    history = _history(content_id)
    if history is None:
        return _refuse(404, "unknown_content_id",
                       "We can't find a submission with that content_id. Check "
                       "it against the one you got back from /submit.",
                       requested_content_id=content_id[:config.MAX_LOGGED_ID_CHARS])

    decision, appeals = history
    previous_status = appeals[-1]["status"] if appeals else decision["status"]
    entry = audit.log_appeal(content_id, decision["creator_id"], reasoning)

    message = ("Your appeal is recorded, and this post is now waiting for a "
               "person to review it.")
    if _shows_pending_label(decision):
        message += (" Until then, its label says a review is pending and the "
                    "automated flag is unconfirmed.")

    return jsonify({
        "content_id": content_id,
        "status": entry["status"],
        "previous_status": previous_status,
        "message": message,
        "appealed_at": entry["timestamp"],
    })


def _shows_pending_label(decision: dict) -> bool:
    """
    Only an AI label is a flag. A human or unsure label already says it is
    not a finding against the writer, so it stays up during a review instead
    of being replaced by text about a flag that never existed.
    """
    return decision.get("guess") == "ai"


def _history(content_id: str):
    """
    (decision, appeals) for one item, read back from the log, or None.

    The decision line is the one without an `event` key. Rejections never
    carry a `content_id`, so a refused request can't make an id look real.
    """
    entries = audit.entries_for(content_id)
    decisions = [e for e in entries if "event" not in e]
    if not decisions:
        return None
    appeals = [e for e in entries if e.get("event") == "appeal"]
    return decisions[0], appeals


# ── Stretch: GET /content/<id> (declared in the README before it was built) ───

@app.get("/content/<content_id>")
def content_status(content_id):
    """
    Where one item stands now: its decision, whether it's under review, and
    the label a reader would see today. Rebuilt from the log on every call,
    so it can never disagree with the audit trail.

    The appeal reasoning stays out of the response. It's the writer's message
    to a reviewer, not something every reader should see.
    """
    history = _history(content_id)
    if history is None:
        return jsonify({"error": "unknown_content_id",
                        "message": "No submission has that content_id."}), 404

    decision, appeals = history
    under_review = bool(appeals)
    pending = under_review and _shows_pending_label(decision)
    return jsonify({
        "content_id": content_id,
        "status": "under_review" if under_review else decision["status"],
        "guess": decision["guess"],
        "confidence": decision["combined_score"],
        "model_score": decision["model_score"],
        "style_score": decision["style_score"],
        "label": scoring.REVIEW_PENDING_LABEL if pending else decision["label"],
        "original_label": decision["label"],
        "decided_at": decision["timestamp"],
        "appeal_count": len(appeals),
        "last_appealed_at": appeals[-1]["timestamp"] if appeals else None,
    })


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
