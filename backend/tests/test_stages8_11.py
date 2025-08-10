from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_stage8_endpoints():
    res = client.get("/stage8/plan")
    assert res.status_code == 200
    assert res.json()["stage"] == 8
    res = client.post("/stage8/telemetry", json={"value": 1})
    assert res.status_code == 200
    assert res.json()["stage"] == 8


def test_stage9_endpoints():
    res = client.get("/stage9/wellness")
    assert res.status_code == 200
    assert res.json()["stage"] == 9
    res = client.post("/stage9/tuning", json={"value": 1})
    assert res.status_code == 200
    assert res.json()["stage"] == 9


def test_stage10_endpoints():
    res = client.get("/stage10/resilience")
    assert res.status_code == 200
    assert res.json()["stage"] == 10
    res = client.post("/stage10/revenue", json={"value": 1})
    assert res.status_code == 200
    assert res.json()["stage"] == 10


def test_stage11_endpoints():
    res = client.get("/stage11/match")
    assert res.status_code == 200
    assert res.json()["stage"] == 11
    res = client.post("/stage11/salvage", json={"value": 1})
    assert res.status_code == 200
    assert res.json()["stage"] == 11
