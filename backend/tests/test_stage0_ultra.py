from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_build_offline_deterministic():
    payload = {
        "site_name": "Test",
        "lat": 1.2345,
        "lon": 2.3456,
        "radius_m": 500,
        "scenarios": ["baseline"],
    }
    res1 = client.post("/stage0/context/build", json=payload)
    res2 = client.post("/stage0/context/build", json=payload)
    assert res1.status_code == 200 and res2.status_code == 200
    ctx1 = res1.json()
    ctx2 = res2.json()
    assert ctx1["audit"]["inputs_hash"] == ctx2["audit"]["inputs_hash"]
    assert ctx1["risk_scores"] == ctx2["risk_scores"]


def test_validate_rejects_self_intersection():
    bow = {
        "type": "Polygon",
        "coordinates": [[[0, 0], [1, 1], [1, 0], [0, 1], [0, 0]]],
    }
    res = client.post("/stage0/context/validate", json={"boundary_geojson": bow})
    body = res.json()
    assert body["valid"] is False
    assert body["errors"]


def test_scenarios_distinct():
    payload = {
        "site_name": "Test",
        "lat": 5.0,
        "lon": 6.0,
        "scenarios": ["baseline", "RCP8.5"],
    }
    res = client.post("/stage0/context/build", json=payload)
    assert res.status_code == 200
    ctx = res.json()
    base = ctx["climate_scenarios"]["baseline"]["heatwave_days"]["value"]
    rcp = ctx["climate_scenarios"]["RCP8.5"]["heatwave_days"]["value"]
    assert base != rcp


def test_counterfactual_changes_risks():
    build = client.post(
        "/stage0/context/build",
        json={"site_name": "Test", "lat": 8.0, "lon": 9.0},
    )
    ctx = build.json()
    cf = client.post(
        "/stage0/counterfactual",
        json={"context_id": ctx["context_id"], "delta": {"greenspace_pct": 0.1}},
    )
    body = cf.json()
    before = body["before"]["risk_scores"]
    after = body["after"]["risk_scores"]
    assert after["heat_0_100"] <= before["heat_0_100"]
    assert after["pollution_0_100"] <= before["pollution_0_100"]


def test_resolve_updates_context():
    build = client.post(
        "/stage0/context/build",
        json={"site_name": "Test", "lat": 3.0, "lon": 4.0},
    )
    ctx = build.json()
    res = client.post(
        "/stage0/resolve",
        json={"context_id": ctx["context_id"], "patch": {"constraints": ["manual"]}},
    )
    assert res.status_code == 200
    updated = client.get(f"/stage0/context/{ctx['context_id']}").json()
    assert updated["constraints"] == ["manual"]
    assert updated["lineage"]["climate"]["transform"].endswith("+ human_override")
