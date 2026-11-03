"""POST /appeal and the GET /content/<id> stretch route (docs/trace.md, section 4)."""

import json

import pytest

import config
import scoring
from conftest import SAMPLE_TEXT

REASON = "I wrote this myself on my phone during a lab break. I can share my drafts."


def read_log(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def submit(client, creator="writer_1"):
    return client.post("/submit", json={"text": SAMPLE_TEXT, "creator_id": creator}).get_json()


def appeal_lines(path):
    return [e for e in read_log(path) if e.get("event") == "appeal"]


def test_an_appeal_moves_the_item_to_under_review_and_confirms(client):
    decision = submit(client)
    response = client.post("/appeal", json={"content_id": decision["content_id"], "reasoning": REASON})

    assert response.status_code == 200
    body = response.get_json()
    assert body["content_id"] == decision["content_id"]
    assert body["status"] == "under_review"
    assert body["previous_status"] == "decided"
    assert body["message"]
    assert body["appealed_at"]


def test_the_appeal_sits_after_the_untouched_decision_in_the_log(client, log_path):
    decision = submit(client)
    before = read_log(log_path)[0]
    client.post("/appeal", json={"content_id": decision["content_id"], "reasoning": REASON})

    entries = read_log(log_path)
    assert entries[0] == before
    assert entries[0]["status"] == "decided"
    appeal = entries[1]
    assert appeal["event"] == "appeal"
    assert appeal["content_id"] == decision["content_id"]
    assert appeal["creator_id"] == "writer_1"
    assert appeal["reasoning"] == REASON
    assert appeal["status"] == "under_review"


def test_an_unknown_content_id_is_a_404_and_files_no_appeal(client, log_path):
    submit(client)
    response = client.post("/appeal", json={"content_id": "not-a-real-id", "reasoning": REASON})

    assert response.status_code == 404
    assert response.get_json()["error"] == "unknown_content_id"
    assert appeal_lines(log_path) == []
    assert read_log(log_path)[-1]["event"] == "rejected"


@pytest.mark.parametrize("body,status,error", [
    ({"reasoning": REASON}, 400, "missing_content_id"),
    ({"content_id": "", "reasoning": REASON}, 400, "missing_content_id"),
    ({"content_id": 42, "reasoning": REASON}, 400, "missing_content_id"),
    ({"content_id": "ID"}, 400, "missing_reasoning"),
    ({"content_id": "ID", "reasoning": "   "}, 400, "missing_reasoning"),
    ({"content_id": "ID", "reasoning": ["a"]}, 400, "missing_reasoning"),
    ({"content_id": "ID", "reasoning": "x" * (config.MAX_APPEAL_CHARS + 1)}, 413, "reasoning_too_long"),
])
def test_bad_appeal_bodies_are_refused_and_file_nothing(client, log_path, body, status, error):
    decision = submit(client)
    body = {k: (decision["content_id"] if v == "ID" else v) for k, v in body.items()}
    response = client.post("/appeal", json=body)

    assert response.status_code == status
    assert response.get_json()["error"] == error
    assert appeal_lines(log_path) == []


def test_an_appeal_body_that_is_not_an_object_is_refused(client, log_path):
    response = client.post("/appeal", data="[1, 2]", content_type="application/json")
    assert response.status_code == 400
    assert response.get_json()["error"] == "invalid_json"
    assert appeal_lines(log_path) == []


def test_a_second_appeal_is_recorded_too(client, log_path):
    decision = submit(client)
    client.post("/appeal", json={"content_id": decision["content_id"], "reasoning": REASON})
    second = client.post("/appeal", json={"content_id": decision["content_id"], "reasoning": "Adding my draft link."})

    assert second.status_code == 200
    assert second.get_json()["previous_status"] == "under_review"
    assert len(appeal_lines(log_path)) == 2


def test_appealing_one_item_leaves_others_alone(client):
    first, other = submit(client, "a"), submit(client, "b")
    client.post("/appeal", json={"content_id": first["content_id"], "reasoning": REASON})
    assert client.get(f"/content/{other['content_id']}").get_json()["status"] == "decided"


# ── GET /content/<id>, the stretch feature ──────────────────────────────────

def test_content_shows_the_decision_before_any_appeal(client):
    decision = submit(client)
    body = client.get(f"/content/{decision['content_id']}").get_json()

    assert body["status"] == "decided"
    assert body["label"] == decision["label"]
    assert body["guess"] == decision["guess"]
    assert body["appeal_count"] == 0


def test_content_shows_under_review_and_the_pending_label_after_an_appeal(client):
    decision = submit(client)
    client.post("/appeal", json={"content_id": decision["content_id"], "reasoning": REASON})
    body = client.get(f"/content/{decision['content_id']}").get_json()

    assert body["status"] == "under_review"
    assert body["label"] == scoring.REVIEW_PENDING_LABEL
    assert body["original_label"] == decision["label"]
    assert body["guess"] == decision["guess"]
    assert body["appeal_count"] == 1
    assert "reasoning" not in json.dumps(body)


def test_content_for_an_unknown_id_is_a_json_404(client):
    response = client.get("/content/nope")
    assert response.status_code == 404
    assert response.get_json()["error"] == "unknown_content_id"
