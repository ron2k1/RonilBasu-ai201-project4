"""
The /submit rate limit (unit 8, Milestone 1).

These run against the real Flask-Limiter instance in app.py, not a stand-in.
conftest's client fixture resets its counters before every test, so each test
starts from an empty window.
"""

import json

import config
from conftest import SAMPLE_TEXT


def _submit(client, creator_id):
    return client.post("/submit", json={"text": SAMPLE_TEXT, "creator_id": creator_id})


def _log_lines(log_path):
    return [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]


def test_limiting_is_on():
    assert config.RATE_LIMITING_ENABLED is True


def test_one_creator_past_the_minute_limit_gets_429(client):
    allowed = config.RATE_LIMIT_PER_MINUTE
    codes = [_submit(client, "rate_writer").status_code for _ in range(allowed + 2)]

    assert codes == [200] * allowed + [429, 429]


def test_429_is_json_and_leaves_a_rejected_line(client, log_path):
    for _ in range(config.RATE_LIMIT_PER_MINUTE):
        _submit(client, "rate_logger")

    response = _submit(client, "rate_logger")

    assert response.status_code == 429
    assert response.get_json()["error"] == "rate_limited"
    last = _log_lines(log_path)[-1]
    assert last["event"] == "rejected"
    assert last["reason"] == "rate_limited"
    assert last["creator_id"] == "rate_logger"


def test_another_creator_keeps_its_own_budget(client):
    for _ in range(config.RATE_LIMIT_PER_MINUTE + 1):
        _submit(client, "rate_noisy")

    assert _submit(client, "rate_quiet").status_code == 200


def test_spaces_around_an_id_do_not_buy_a_new_budget(client):
    # The log strips the id, so " pad" and "pad " already read as one writer
    # there. The limiter has to count them as one writer too.
    variants = ["rate_pad", " rate_pad", "rate_pad ", "  rate_pad", "rate_pad  "]
    for creator_id in variants:
        assert _submit(client, creator_id).status_code == 200

    assert _submit(client, " rate_pad ").status_code == 429


def test_an_id_too_long_to_log_counts_against_the_address(client):
    # Every distinct over-long id used to get its own budget, and its own
    # 200,000-character key in limiter memory for a day.
    too_long = config.MAX_CREATOR_ID_CHARS + 1
    codes = [_submit(client, letter * too_long).status_code for letter in "abcdef"]

    assert codes[-1] == 429


def test_oversized_bodies_count_against_the_budget(client):
    body = json.dumps({"text": "word " * (config.MAX_REQUEST_BYTES // 4),
                       "creator_id": "rate_big"})
    codes = [client.post("/submit", data=body, content_type="application/json").status_code
             for _ in range(config.RATE_LIMIT_PER_MINUTE + 1)]

    assert codes == [413] * config.RATE_LIMIT_PER_MINUTE + [429]


def test_the_429_line_logs_the_cleaned_id_and_the_route(client, log_path):
    for _ in range(config.RATE_LIMIT_PER_MINUTE + 1):
        _submit(client, "  rate_trimmed  ")

    last = _log_lines(log_path)[-1]
    assert last["reason"] == "rate_limited"
    assert last["creator_id"] == "rate_trimmed"
    assert last["route"] == "/submit"
    assert last["http_status"] == 429


def test_a_null_id_is_logged_as_unknown_on_a_429(client, log_path):
    for _ in range(config.RATE_LIMIT_PER_MINUTE + 1):
        client.post("/submit", json={"text": SAMPLE_TEXT, "creator_id": None})

    last = _log_lines(log_path)[-1]
    assert last["reason"] == "rate_limited"
    assert last["creator_id"] == "unknown"


def test_rejected_requests_do_not_count_as_decisions(client, log_path):
    for _ in range(config.RATE_LIMIT_PER_MINUTE + 3):
        _submit(client, "rate_counted")

    lines = _log_lines(log_path)
    decisions = [e for e in lines if "event" not in e]
    rejected = [e for e in lines if e.get("event") == "rejected"]
    assert len(decisions) == config.RATE_LIMIT_PER_MINUTE
    assert len(rejected) == 3
