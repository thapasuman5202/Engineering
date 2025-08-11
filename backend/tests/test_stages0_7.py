from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_stage0_build_context():
    payload = {"location": {"lat": 1.0, "lon": 2.0}}
    res = client.post("/stage0/context/build", json=payload)
    assert res.status_code == 200
    body = res.json()
    assert "context_id" in body
    assert body["context"]["request"]["location"]["lat"] == 1.0


def test_stage1_endpoint():
    res = client.get("/stage1")
    assert res.status_code == 200
    assert res.json()["stage"] == 1


def test_stage2_endpoint():
    res = client.get("/stage2")
    assert res.status_code == 200
    assert res.json()["stage"] == 2


def test_stage3_endpoint():
    res = client.get("/stage3")
    assert res.status_code == 200
    assert res.json()["stage"] == 3


def test_stage4_endpoint():
    res = client.get("/stage4")
    assert res.status_code == 200
    assert res.json()["stage"] == 4


def test_stage5_endpoint():
    res = client.get("/stage5")
    assert res.status_code == 200
    assert res.json()["stage"] == 5


def test_stage6_endpoint():
    res = client.get("/stage6")
    assert res.status_code == 200
    assert res.json()["stage"] == 6


def test_stage7_endpoint():
    res = client.get("/stage7")
    assert res.status_code == 200
    assert res.json()["stage"] == 7
