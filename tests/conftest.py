"""
Shared test setup.

Every test gets its own audit log under pytest's tmp_path, so running the
suite never touches the committed logs/audit.jsonl.

Route tests replace the GPT-2 signal with a fixed number. They test the
route's contract (validation, logging, response shape), not the model, and
loading a 550 MB model per test would make the suite unusable. The real
model is exercised by scripts/calibrate.py and by hand with curl.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app as app_module  # noqa: E402
import config  # noqa: E402
import detector  # noqa: E402

# 50 plain words over four sentences: past MIN_WORDS, and short enough to read.
SAMPLE_TEXT = (
    "I walked to the library after class because my room was too loud. "
    "The second floor was full, so I sat by the window near the stairs. "
    "It rained the whole afternoon and I barely noticed. "
    "By six I had finished two problem sets and most of a lab report."
)


@pytest.fixture
def log_path(tmp_path, monkeypatch):
    log_dir = tmp_path / "logs"
    monkeypatch.setattr(config, "LOG_DIR", log_dir)
    monkeypatch.setattr(config, "AUDIT_LOG", log_dir / "audit.jsonl")
    return log_dir / "audit.jsonl"


@pytest.fixture
def fixed_model(monkeypatch):
    """Signal one returns a set value instead of running GPT-2."""
    state = {"score": 0.8}
    monkeypatch.setattr(detector, "model_signal", lambda text: state["score"])
    return state


@pytest.fixture
def client(log_path, fixed_model):
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()
