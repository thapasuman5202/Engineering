from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_build_offline_deterministic():
    payload = {"location": {"lat": 1.2345, "lon": 2.3456}}
    res1 = client.post("/stage0/context/build", json=payload)
    res2 = client.post("/stage0/context/build", json=payload)
    assert res1.status_code == 200
    assert res2.status_code == 200
    ctx1 = res1.json()["context"]
    ctx2 = res2.json()["context"]
    assert ctx1 == ctx2


def test_validate_rejects_self_intersection():
    # Self-intersecting polygon (bow-tie) to trigger validation error
    footprint = {
        "type": "Polygon",
        "coordinates": [
            [
                [0.0, 0.0],
                [1.0, 1.0],
                [1.0, 0.0],
                [0.0, 1.0],
                [0.0, 0.0],
            ]
        ],
    }
    context = {
        "request": {"location": {"lat": 0.0, "lon": 0.0}},
        "footprint": footprint,
    }
    res = client.post("/stage0/context/validate", json={"context": context})
    assert res.status_code == 200
    body = res.json()
    assert body["valid"] is False
    assert body["errors"]


def test_scenarios_distinct():
    payload_hist = {
        "location": {"lat": 5.0, "lon": 6.0},
        "climate_scenario": "historical",
    }
    payload_future = {
        "location": {"lat": 5.0, "lon": 6.0},
        "climate_scenario": "ssp5_8.5",
    }
    res_hist = client.post("/stage0/context/build", json=payload_hist)
    res_future = client.post("/stage0/context/build", json=payload_future)
    assert res_hist.status_code == 200
    assert res_future.status_code == 200
    risk_hist = res_hist.json()["context"]["risk"]
    risk_future = res_future.json()["context"]["risk"]
    assert risk_hist != risk_future


def test_counterfactual_changes_risks():
    build = client.post(
        "/stage0/context/build",
        json={"location": {"lat": 8.0, "lon": 9.0}},
    )
    assert build.status_code == 200
    context_id = build.json()["context_id"]
    base_score = build.json()["context"]["risk"]["score"]
    cf = client.post(
        "/stage0/counterfactual",
        json={"context_id": context_id, "scenario": "ssp5_8.5"},
    )
    assert cf.status_code == 200
    cf_score = cf.json()["context"]["risk"]["score"]
    assert cf_score != base_score


def test_resolve_updates_context():
    build = client.post(
        "/stage0/context/build",
        json={"location": {"lat": 3.0, "lon": 4.0}},
    )
    assert build.status_code == 200
    context_id = build.json()["context_id"]
    original_ctx = build.json()["context"]

    res = client.post(
        "/stage0/resolve",
        json={"context_id": context_id, "query": "latest info"},
    )
    assert res.status_code == 200

    updated = client.get(f"/stage0/context/{context_id}")
    assert updated.status_code == 200
    assert updated.json() != original_ctx
