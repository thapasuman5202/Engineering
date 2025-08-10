# Kathmandu Pilot — One-Button Starter Kit

This is the simplest possible skeleton so you can click a button on a web page and send a JSON payload to a tiny backend. The backend saves your run request, creates placeholder artifacts, and gives you a Run ID you can view.

## What you get
- `frontend/` — a single HTML page with the **90‑second wizard**.
- `backend/` — a small Flask API with one endpoint: `POST /v1/run`.
- `codepacks/kathmandu/` — a **YAML rule pack** with 10 placeholder rules.
- `orchestrator/` — a **DAG stub** showing the steps the real system will run.
- `sample-data/` — an example JSON payload you can send.

## How to run (5 steps)

1) **Open a terminal** in this folder.
2) Create a venv and install backend dependencies:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```
3) Start the backend:
   ```bash
   python backend/app.py
   ```
   You should see: `* Running on http://127.0.0.1:5000`
4) Open `frontend/index.html` in your browser (double‑click or use a local server).
   - Fill the form and click **Run God‑Mode**.
5) Check the run:
   - The page will show your **Run ID**.
   - The backend writes files to `backend/runs/<RUN_ID>/` including:
     - `request.json` (what you sent)
     - `artifacts/` with dummy outputs (IFC, glTF, estimate.csv, reports.pdf placeholders)

## Files you will touch first
- Edit **`frontend/index.html`** if you want to change the questions/fields.
- Edit **`codepacks/kathmandu/rules.yaml`** to add real rules (start with the 10 placeholders).
- Edit **`orchestrator/dag.yaml`** to add real steps (keep names the same).

## What to do next
- Replace dummy artifact writers in `backend/app.py` with calls to your real services.
- Implement the first 10 real Kathmandu rules in `codepacks/kathmandu/rules.yaml`.
- Wire an actual generator behind the `generate` step in the DAG.

That’s it. Keep it simple. Make the button work first, then deepen each step.
