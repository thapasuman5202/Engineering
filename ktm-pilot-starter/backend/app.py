from __future__ import annotations

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
from math import sqrt
import json, uuid, os, io, zipfile, csv, datetime, threading, time, yaml, base64, struct

# ---------------- App & paths ----------------
app = Flask(__name__)
CORS(app)

BASE = Path(__file__).resolve().parent
RUNS = BASE / "runs"
RUNS.mkdir(exist_ok=True)
CODEPACK = BASE.parent / "codepacks" / "kathmandu" / "rules.yaml"

REQUIRED_FIELDS = ["site", "program", "constraints"]

# ---------------- Optional IFC ----------------
try:
    import ifcopenshell
    import ifcopenshell.api
    IFC_OK = True
except Exception:
    IFC_OK = False

# ---------------- ReportLab PDFs ----------------
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

styles = getSampleStyleSheet()
H1 = styles["Title"]; H2 = styles["Heading2"]; P = styles["BodyText"]

def write_pdf(path: Path, title: str, sections: list[tuple[str, list[str]]], tables: list[tuple[str, list[list]]]|None=None):
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    flow = [Paragraph(title, H1), Spacer(1, 10)]
    for head, lines in sections:
        flow += [Paragraph(head, H2), Spacer(1, 4)]
        for ln in lines: flow += [Paragraph(ln, P)]
        flow += [Spacer(1, 10)]
    if tables:
        for caption, data in tables:
            flow += [Paragraph(caption, H2), Spacer(1, 6)]
            t = Table(data)
            t.setStyle(TableStyle([
                ("GRID",(0,0),(-1,-1),0.25,colors.grey),
                ("BACKGROUND",(0,0),(-1,0),colors.whitesmoke),
                ("ALIGN",(0,0),(-1,-1),"LEFT"),
                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
                ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ]))
            flow += [t, Spacer(1, 10)]
    doc.build(flow)

# ---------------- Estimator (simple, real CSV) ----------------
def compute_estimate(payload: dict) -> list[dict]:
    prog = payload["program"]
    gfa = float(prog.get("grossFloorArea_m2", 0.0))
    conc_m3 = 0.12 * gfa
    rebar_t = 0.09 * conc_m3
    brick_m2 = 0.80 * gfa
    wnd_m2 = 0.18 * brick_m2
    form_m2 = conc_m3 * 4.5

    rate = {
        "Concrete (M30) m3": 13500,
        "Rebar t": 145000,
        "Brickwork m2": 2200,
        "Windows m2": 8500,
        "Formwork m2": 950,
        "MEP per m2": 4200,
        "Finishes per m2": 3000,
        "Contingency %": 0.07
    }

    items = []
    def add(name, qty, unit, r): items.append({"item":name,"qty":round(qty,2),"unit":unit,"rate":round(r,2),"total":round(qty*r,2)})
    add("Concrete (M30) m3", conc_m3, "m3", rate["Concrete (M30) m3"])
    add("Rebar t", rebar_t, "t", rate["Rebar t"])
    add("Brickwork m2", brick_m2, "m2", rate["Brickwork m2"])
    add("Windows m2", wnd_m2, "m2", rate["Windows m2"])
    add("Formwork m2", form_m2, "m2", rate["Formwork m2"])
    add("MEP per m2", gfa, "m2", rate["MEP per m2"])
    add("Finishes per m2", gfa, "m2", rate["Finishes per m2"])
    subtotal = sum(x["total"] for x in items)
    conting = subtotal*rate["Contingency %"]
    items.append({"item":"Contingency 7%","qty":1,"unit":"ls","rate":round(conting,2),"total":round(conting,2)})
    items.append({"item":"Grand Total (NPR)","qty":1,"unit":"ls","rate":round(subtotal+conting,2),"total":round(subtotal+conting,2)})
    return items

def write_estimate_csv(path: Path, items: list[dict]):
    with open(path,"w",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["item","qty","unit","rate","total"])
        w.writeheader(); w.writerows(items)

# ---------------- Structural prelim PDF (stub calc) ----------------
def write_structural_prelim_pdf(path: Path, payload: dict):
    gfa = float(payload["program"].get("grossFloorArea_m2", 0.0))
    floors = int(payload["program"].get("floorsAbove", 1))
    Cs = 0.12; WkN = 6.0*gfa; V = Cs*WkN
    write_pdf(path, "Structural Preliminary — Kathmandu",
              [("Summary", [
                    f"Jurisdiction: {payload['site'].get('jurisdiction','NP-KTM')}",
                    f"Floors: {floors}", f"GFA: {gfa:,.0f} m²",
                    f"Cs (stub): {Cs:.2f}", f"W (proxy): {WkN:,.0f} kN",
                    f"Base Shear V: {V:,.0f} kN"
               ]),
               ("Notes",["Screening only. Replace with NBC calculations & NLTH/pushover."])])

# ---------------- Energy/daylight proxy PDF ----------------
def write_energy_proxy_pdf(path: Path, payload: dict):
    typ = (payload["program"].get("typology") or "Residential").lower()
    gfa = float(payload["program"].get("grossFloorArea_m2", 0.0))
    baseline = {"residential":90,"office":160,"school":110}
    eui = baseline.get(typ,120)
    if int(payload["program"].get("floorsAbove",1)) >= 10: eui *= 0.98
    write_pdf(path, "Energy & Daylight Proxy — Kathmandu",
              [("Summary",[f"Typology: {typ.title()}", f"EUI (stub): {eui:.1f} kWh/m²·yr", f"Annual: {eui*gfa:,.0f} kWh"]),
               ("Next",["Swap to EnergyPlus; daylight factors; PV on roof ≥40% clear area."])])

# ---------------- Codepack engine ----------------
def safe_eval(expr: str, ctx: dict) -> bool:
    try: return bool(eval(expr, {"__builtins__": {}}, ctx))
    except Exception: return False

def evaluate_codepack(payload: dict) -> list[dict]:
    if not CODEPACK.exists(): return []
    data = yaml.safe_load(CODEPACK.read_text(encoding="utf-8"))
    rules = data.get("rules", [])
    ctx = {"site": payload.get("site", {}), "program": payload.get("program", {}), "constraints": payload.get("constraints", {})}
    out=[]
    for r in rules:
        out.append({
            "id": r.get("id"), "title": r.get("title"), "clause": r.get("clause"),
            "result": r.get("result"), "severity": r.get("severity","INFO"),
            "passed": safe_eval(r.get("check","True"), ctx)
        })
    return out

def write_code_report_pdf(path_report: Path, path_checklist: Path, results: list[dict]):
    table = [["Rule ID","Title","Severity","Passed?"]] + [[r["id"],r["title"],r["severity"],"YES" if r["passed"] else "NO"] for r in results]
    write_pdf(path_report, "Kathmandu Code Report (Auto-Check)", [("Notes",["Automated pre-check. Engineer sign-off required."])],[("Checks",table)])
    write_pdf(path_checklist, "Permit Submission Checklist — Kathmandu",
              [("Documents",["Title/site/key plans","Arch plans/sections/elevations","Structural prelim & geotech","Fire/Egress & Accessibility","Schedules; Energy/MEP notes; Drawings index"])])

# ---------------- GLTF generator (no deps; unlit so it renders everywhere) ----------------
def write_gltf_box(path: Path, width: float, depth: float, height: float):
    # vertices: base at z=0, height upwards; centered in X/Y
    w,d,h = width/2.0, depth/2.0, height
    positions = [
        -w,0,-d,  w,0,-d,  w,0,d,  -w,0,d,     # bottom
        -w,h,-d,  w,h,-d,  w,h,d,  -w,h,d      # top
    ]
    indices = [
        0,1,2, 0,2,3,    # bottom
        4,6,5, 4,7,6,    # top
        3,2,6, 3,6,7,    # front
        0,5,1, 0,4,5,    # back
        0,3,7, 0,7,4,    # left
        1,5,6, 1,6,2     # right
    ]
    pos_bytes = b"".join(struct.pack("<f", p) for p in positions)
    idx_bytes = b"".join(struct.pack("<H", i) for i in indices)
    pos_b64 = "data:application/octet-stream;base64," + base64.b64encode(pos_bytes).decode("ascii")
    idx_b64 = "data:application/octet-stream;base64," + base64.b64encode(idx_bytes).decode("ascii")
    gltf = {
        "asset":{"version":"2.0","generator":"GodMode-KTM"},
        "extensionsUsed":["KHR_materials_unlit"],
        "buffers":[
            {"uri":pos_b64,"byteLength":len(pos_bytes)},
            {"uri":idx_b64,"byteLength":len(idx_bytes)}
        ],
        "bufferViews":[
            {"buffer":0,"byteOffset":0,"byteLength":len(pos_bytes),"target":34962},
            {"buffer":1,"byteOffset":0,"byteLength":len(idx_bytes),"target":34963}
        ],
        "accessors":[
            {"bufferView":0,"byteOffset":0,"componentType":5126,"count":8,"type":"VEC3"},   # FLOAT
            {"bufferView":1,"byteOffset":0,"componentType":5123,"count":len(indices),"type":"SCALAR"} # USHORT
        ],
        "materials":[{
            "name":"UnlitBlue","extensions":{"KHR_materials_unlit":{}},
            "pbrMetallicRoughness":{"baseColorFactor":[0.35,0.55,1.0,1.0]},
            "doubleSided":True
        }],
        "meshes":[{"name":"MassingBox","primitives":[{"attributes":{"POSITION":0},"indices":1,"material":0}]}],
        "nodes":[{"mesh":0,"name":"Building"}],
        "scenes":[{"nodes":[0]}],
        "scene":0
    }
    path.write_text(json.dumps(gltf, indent=2), encoding="utf-8")

# ---------------- IFC writer (graceful if API differs/missing) ----------------
def write_ifc_mass(path: Path, width: float, depth: float, height: float):
    if not IFC_OK:
        path.write_text("IFC not available (ifcopenshell not installed). GLTF/PDF/CSV created.")
        return
    try:
        m = ifcopenshell.api.run("project.create_file")
        # units: try multiple signatures
        try:
            ifcopenshell.api.run("unit.assign_unit", m, length_units="METERS")
        except TypeError:
            try:
                ifcopenshell.api.run("unit.assign_unit", m, units=[{"unit_type":"LENGTHUNIT","name":"METRE"}])
            except Exception:
                pass

        ctx_model = ifcopenshell.api.run("context.add_context", m, context_identifier="Model", context_type="Model")
        body = ifcopenshell.api.run("context.add_context", m, context_identifier="Body",
                                    context_type="Model", target_view="MODEL_VIEW", parent=ctx_model)

        project = ifcopenshell.api.run("root.create_entity", m, ifc_class="IfcProject", name="KTM Pilot")
        site    = ifcopenshell.api.run("root.create_entity", m, ifc_class="IfcSite", name="Site")
        bldg    = ifcopenshell.api.run("root.create_entity", m, ifc_class="IfcBuilding", name="Building")
        storey  = ifcopenshell.api.run("root.create_entity", m, ifc_class="IfcBuildingStorey", name="Storey 0", elevation=0.0)

        ifcopenshell.api.run("aggregate.assign_object", m, product=project, relating_object=site)
        ifcopenshell.api.run("aggregate.assign_object", m, product=site, relating_object=bldg)
        ifcopenshell.api.run("aggregate.assign_object", m, product=bldg, relating_object=storey)

        proxy = ifcopenshell.api.run("root.create_entity", m, ifc_class="IfcBuildingElementProxy", name="Mass")
        ifcopenshell.api.run("spatial.assign_container", m, product=proxy, relating_structure=storey)

        prof = ifcopenshell.api.run("geometry.create_rectangle_profile", m, profile_name="MassProfile", x_dim=width, y_dim=depth)
        rep  = ifcopenshell.api.run("geometry.create_extruded_area_solid", m, context=body, profile=prof, depth=height)
        ifcopenshell.api.run("geometry.assign_representation", m, product=proxy, representation=rep)

        m.write(str(path))
    except Exception as e:
        path.write_text(f"IFC export skipped due to API mismatch: {e}\nGLTF/PDF/CSV are still valid.")

# ---------------- Sizing from input ----------------
def size_from_payload(payload: dict):
    gfa = float(payload["program"].get("grossFloorArea_m2", 0.0))
    floors = max(1, int(payload["program"].get("floorsAbove", 1)))
    height = floors * 3.0
    area = gfa/floors if gfa>0 else 400.0
    width = depth = sqrt(area) * 1.10  # +10% cores
    return width, depth, height

# ---------------- Progress helpers ----------------
def write_status(run_dir: Path, step: str, pct: int, state="RUNNING", error: str|None=None):
    s = {"step":step,"percent":pct,"state":state,"updatedAt":datetime.datetime.utcnow().isoformat()+"Z"}
    if error: s["error"]=error
    (run_dir/"status.json").write_text(json.dumps(s,indent=2))

def pipeline_worker(run_dir: Path):
    try:
        art = run_dir / "artifacts"; art.mkdir(parents=True,exist_ok=True)
        payload = json.loads((run_dir/"request.json").read_text())
        w,d,h = size_from_payload(payload)

        steps = [
            ("ingest",10, lambda: time.sleep(0.05)),
            ("generate-3d",30, lambda: write_gltf_box(art/"variant_01.gltf", w,d,h)),
            ("ifc-export",40, lambda: write_ifc_mass(art/"variant_01.ifc", w,d,h)),
            ("analyze-struct",60, lambda: write_structural_prelim_pdf(art/"structural_prelim.pdf", payload)),
            ("analyze-energy",75, lambda: write_energy_proxy_pdf(art/"energy_daylight_proxy.pdf", payload)),
            ("estimate",88, lambda: write_estimate_csv(art/"estimate_class3.csv", compute_estimate(payload))),
            ("permit",96, lambda: write_code_report_pdf(art/"kathmandu_code_report.pdf", art/"permit_checklist.pdf", evaluate_codepack(payload))),
        ]
        for name,pct,fn in steps:
            write_status(run_dir,name,pct); fn()

        (run_dir/"dag.json").write_text(json.dumps({"steps":[s[0] for s in steps],"status":"COMPLETED (pilot)"},indent=2))
        write_status(run_dir,"complete",100,state="SUCCEEDED")
    except Exception as e:
        write_status(run_dir,"error",100,state="FAILED",error=str(e))

def start_pipeline(run_dir: Path):
    threading.Thread(target=pipeline_worker, args=(run_dir,), daemon=True).start()

# ---------------- Routes ----------------
@app.route("/", methods=["GET"])
def root():
    return jsonify({"ok":True,"runs":sorted([p.name for p in RUNS.iterdir() if p.is_dir()])})

@app.route("/health", methods=["GET"])
def health(): return jsonify({"ok":True})

@app.route("/v1/run", methods=["POST"])
def create_run():
    payload = request.get_json(force=True, silent=True) or {}
    missing = [f for f in REQUIRED_FIELDS if f not in payload]
    if missing: return jsonify({"error":f"Missing fields: {missing}"}), 400
    run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"; run_dir = RUNS/run_id
    run_dir.mkdir(parents=True,exist_ok=True)
    (run_dir/"request.json").write_text(json.dumps(payload,indent=2))
    write_status(run_dir,"queued",0,state="QUEUED"); start_pipeline(run_dir)
    return jsonify({"runId":run_id,"statusUrl":f"/runs/{run_id}/status"}), 202

@app.route("/runs/<run_id>/status", methods=["GET"])
def run_status(run_id):
    s = RUNS/run_id/"status.json"
    if not s.exists(): return jsonify({"error":"Run not found"}), 404
    return jsonify(json.loads(s.read_text()))

@app.route("/runs/<run_id>", methods=["GET"])
def get_run(run_id):
    run_dir = RUNS/run_id
    if not run_dir.exists(): return jsonify({"error":"Run not found"}), 404
    art = run_dir/"artifacts"
    artifacts = [p.name for p in art.iterdir() if p.is_file()] if art.exists() else []
    req = json.loads((run_dir/"request.json").read_text())
    dag = json.loads((run_dir/"dag.json").read_text()) if (run_dir/"dag.json").exists() else {}
    status = json.loads((run_dir/"status.json").read_text()) if (run_dir/"status.json").exists() else {}
    return jsonify({"runId":run_id,"artifacts":artifacts,"paths":{"runDir":str(run_dir),"artifactsDir":str(art)},"request":req,"dag":dag,"status":status})

@app.route("/runs/<run_id>/artifacts/<name>", methods=["GET"])
def get_artifact(run_id, name):
    p = RUNS/run_id/"artifacts"/name
    if not p.exists(): return jsonify({"error":"Not found"}), 404
    return send_file(p, as_attachment=False)

@app.route("/runs/<run_id>/zip", methods=["GET"])
def get_zip(run_id):
    run_dir = RUNS/run_id
    if not run_dir.exists(): return jsonify({"error":"Run not found"}), 404
    mem = io.BytesIO()
    with zipfile.ZipFile(mem,"w",zipfile.ZIP_DEFLATED) as z:
        art = run_dir/"artifacts"
        if art.exists():
            for p in art.glob("*"): z.write(p, f"artifacts/{p.name}")
        for meta in ("request.json","dag.json","status.json"):
            q = run_dir/meta
            if q.exists(): z.write(q, meta)
    mem.seek(0)
    return send_file(mem, mimetype="application/zip", as_attachment=True, download_name=f"{run_id}.zip")

if __name__ == "__main__":
    port = int(os.environ.get("PORT","5000"))
    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False)
