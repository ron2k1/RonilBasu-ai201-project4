"""POST /submit: the contract in docs/trace.md, section 4."""

import json

import pytest

import config
from conftest import SAMPLE_TEXT


def read_log(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_submit_returns_the_contract_fields(client):
    response = client.post("/submit", json={"text": SAMPLE_TEXT, "creator_id": "writer_1"})

    assert response.status_code == 200
    body = response.get_json()
    for field in ("content_id", "creator_id", "guess", "confidence", "label",
                  "model_score", "style_score", "status"):
        assert field in body, field
    assert body["creator_id"] == "writer_1"
    assert body["model_score"] == 0.8
    assert body["status"] == "decided"
    assert body["guess"] in ("ai", "human", "unsure")
    assert 0.0 <= body["confidence"] <= 1.0


def test_confidence_is_the_combining_rule_applied_to_both_signals(client, log_path):
    import scoring
    import stylometry

    body = client.post("/submit", json={"text": SAMPLE_TEXT, "creator_id": "w"}).get_json()

    assert body["style_score"] == stylometry.style_signal(SAMPLE_TEXT)
    assert body["confidence"] == scoring.combine_signals(0.8, body["style_score"])
    entry = read_log(log_path)[0]
    assert (entry["model_score"], entry["style_score"], entry["combined_score"]) == (
        body["model_score"], body["style_score"], body["confidence"])


def test_each_submission_gets_its_own_content_id(client):
    first = client.post("/submit", json={"text": SAMPLE_TEXT, "creator_id": "w"}).get_json()
    second = client.post("/submit", json={"text": SAMPLE_TEXT, "creator_id": "w"}).get_json()
    assert first["content_id"] != second["content_id"]


def test_submit_writes_one_decision_line_matching_the_response(client, log_path):
    body = client.post("/submit", json={"text": SAMPLE_TEXT, "creator_id": "writer_1"}).get_json()

    entries = read_log(log_path)
    assert len(entries) == 1
    entry = entries[0]
    assert entry["content_id"] == body["content_id"]
    assert entry["creator_id"] == "writer_1"
    assert entry["status"] == "decided"
    for field in ("guess", "model_score", "style_score", "label"):
        assert entry[field] == body[field], field
    assert entry["combined_score"] == body["confidence"]
    assert entry["timestamp"]


def test_text_is_trimmed_before_it_is_judged(client, log_path):
    response = client.post("/submit", json={"text": "\n\n  " + SAMPLE_TEXT + "  \n", "creator_id": "w"})
    assert response.status_code == 200
    entry = read_log(log_path)[0]
    assert entry["word_count"] == 50
    # word_count alone can't tell: words() skips whitespace either way.
    assert entry["text_preview"] == SAMPLE_TEXT[:80]


def test_padding_does_not_count_against_the_length_cap(client):
    padded = " " * config.MAX_TEXT_CHARS + SAMPLE_TEXT + "\n" * 100
    assert len(padded) > config.MAX_TEXT_CHARS
    response = client.post("/submit", json={"text": padded, "creator_id": "w"})
    assert response.status_code == 200


BAD_BODIES = [
    ("no text field", {"creator_id": "w"}, 400, "missing_text"),
    ("text is null", {"text": None, "creator_id": "w"}, 400, "missing_text"),
    ("text is empty", {"text": "", "creator_id": "w"}, 400, "missing_text"),
    ("text is whitespace", {"text": "  \n\t ", "creator_id": "w"}, 400, "missing_text"),
    ("text is a number", {"text": 12345, "creator_id": "w"}, 400, "missing_text"),
    ("text is a list", {"text": ["a", "b"], "creator_id": "w"}, 400, "missing_text"),
    ("no creator_id", {"text": SAMPLE_TEXT}, 400, "missing_creator_id"),
    ("blank creator_id", {"text": SAMPLE_TEXT, "creator_id": "   "}, 400, "missing_creator_id"),
    ("numeric creator_id", {"text": SAMPLE_TEXT, "creator_id": 7}, 400, "missing_creator_id"),
    ("huge creator_id", {"text": SAMPLE_TEXT, "creator_id": "x" * 201}, 400, "missing_creator_id"),
    ("five words", {"text": "this is only five words", "creator_id": "w"}, 422, "text_too_short"),
    ("over the cap", {"text": "word " * 5000, "creator_id": "w"}, 413, "text_too_long"),
]


@pytest.mark.parametrize("name,body,status,error", BAD_BODIES, ids=[b[0] for b in BAD_BODIES])
def test_bad_bodies_get_a_4xx_and_a_rejected_line(client, log_path, name, body, status, error):
    response = client.post("/submit", json=body)

    assert response.status_code == status
    payload = response.get_json()
    assert payload["error"] == error
    assert payload["message"]
    assert "label" not in payload

    entries = read_log(log_path)
    assert len(entries) == 1
    assert entries[0]["event"] == "rejected"
    assert entries[0]["reason"] == error


@pytest.mark.parametrize("raw", ["[1, 2, 3]", '"just a string"', "42", "null", "{not json"])
def test_a_body_that_is_not_a_json_object_is_refused(client, log_path, raw):
    response = client.post("/submit", data=raw, content_type="application/json")

    assert response.status_code == 400
    assert response.get_json()["error"] == "invalid_json"
    assert read_log(log_path)[0]["reason"] == "invalid_json"


def test_a_250k_character_text_is_refused_not_crashed(client, log_path):
    response = client.post("/submit", json={"text": "a" * 250_000, "creator_id": "w"})

    assert response.status_code == 413
    assert response.get_json()["error"] in ("text_too_long", "request_too_large")
    assert read_log(log_path)[0]["event"] == "rejected"


def test_a_body_over_the_byte_cap_is_refused_before_the_route(client, log_path):
    raw = json.dumps({"text": "a" * (config.MAX_REQUEST_BYTES + 10), "creator_id": "w"})
    response = client.post("/submit", data=raw, content_type="application/json")

    assert response.status_code == 413
    assert response.get_json()["error"] == "request_too_large"
    assert read_log(log_path)[0]["reason"] == "request_too_large"


def test_a_model_failure_is_a_503_not_a_500(client, log_path, monkeypatch):
    import detector

    def broken(text):
        raise detector.DetectorUnavailable("no model on disk")

    monkeypatch.setattr(detector, "model_signal", broken)
    response = client.post("/submit", json={"text": SAMPLE_TEXT, "creator_id": "w"})

    assert response.status_code == 503
    assert response.get_json()["error"] == "detector_unavailable"
    assert read_log(log_path)[0]["reason"] == "detector_unavailable"


def test_ping_still_answers_after_bad_input(client):
    for _, body, _, _ in BAD_BODIES:
        client.post("/submit", json=body)
    response = client.post("/ping", json={"message": "still here"})
    assert response.status_code == 200
    assert response.get_json()["you_sent"] == "still here"
