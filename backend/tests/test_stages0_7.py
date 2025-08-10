from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_stage0_endpoint():
    res = client.get("/stage0")
    assert res.status_code == 200
    assert res.json()["stage"] == 0


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
