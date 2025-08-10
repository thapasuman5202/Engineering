import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.main import app
from app.services import stage8, stage9, stage10, stage11

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_services():
    """Ensure service state is reset before each test case."""
    stage8.reset_state()
    stage9.reset_state()
    stage10.reset_state()
    stage11.reset_state()


def test_stage8_state_accumulates_within_test():
    res = client.get("/stage8/plan")
    assert res.status_code == 200
    assert res.json()["stage"] == 8

    res1 = client.post("/stage8/telemetry", json={"value": 1})
    res2 = client.post("/stage8/telemetry", json={"value": 2})
    assert res1.json()["data"]["count"] == 1
    assert res2.json()["data"]["count"] == 2


def test_stage8_state_resets_between_tests():
    res = client.post("/stage8/telemetry", json={"value": 3})
    assert res.json()["data"]["count"] == 1


def test_stage9_state_accumulates_within_test():
    res = client.get("/stage9/wellness")
    assert res.status_code == 200
    assert res.json()["stage"] == 9

    res1 = client.post("/stage9/tuning", json={"value": 1})
    res2 = client.post("/stage9/tuning", json={"value": 2})
    assert res1.json()["data"]["count"] == 1
    assert res2.json()["data"]["count"] == 2


def test_stage9_state_resets_between_tests():
    res = client.post("/stage9/tuning", json={"value": 3})
    assert res.json()["data"]["count"] == 1


def test_stage10_state_accumulates_within_test():
    res = client.get("/stage10/resilience")
    assert res.status_code == 200
    assert res.json()["stage"] == 10

    res1 = client.post("/stage10/revenue", json={"value": 1})
    res2 = client.post("/stage10/revenue", json={"value": 2})
    assert res1.json()["data"]["count"] == 1
    assert res2.json()["data"]["count"] == 2


def test_stage10_state_resets_between_tests():
    res = client.post("/stage10/revenue", json={"value": 3})
    assert res.json()["data"]["count"] == 1


def test_stage11_state_accumulates_within_test():
    res = client.get("/stage11/match")
    assert res.status_code == 200
    assert res.json()["stage"] == 11

    res1 = client.post("/stage11/salvage", json={"value": 1})
    res2 = client.post("/stage11/salvage", json={"value": 2})
    assert res1.json()["data"]["count"] == 1
    assert res2.json()["data"]["count"] == 2


def test_stage11_state_resets_between_tests():
    res = client.post("/stage11/salvage", json={"value": 3})
    assert res.json()["data"]["count"] == 1
