# God-Mode Ultra Flow Platform

This repository hosts a full-stack platform implementing the God-Mode Ultra Flow vision. The system orchestrates generative design and construction workflows across twelve stages:

0. Context ingestion
1. Multi-agent variant generation (combinatorial attribute exploration)
2. Surrogate multiphysics analysis
3. Multi-objective optimization
4. Compliance & authority pre-check
5. Procurement & finance lock
6. Fabrication & robotics mobilization
7. Permit submission & construction start
8. Live construction control
9. Handover & operations
10. Long-term optimization
11. End-of-life circularity

## Stack

- **Backend**: FastAPI
- **Frontend**: Vite + React + TailwindCSS
- **Containerization**: Docker & Docker Compose
- **CI**: GitHub Actions

## Quick Start

```bash
git clone <repo>
cd <repo>
docker-compose up --build
```

The backend will be available at `http://localhost:8000` and the frontend at `http://localhost:5173`.

## Environment Variables

The backend uses the `pydantic-settings` package for configuration, built atop
`pydantic.BaseSettings`. Values can be supplied via environment variables or a
`.env` file in the `backend` directory.

| Variable  | Description                                | Default               |
|-----------|--------------------------------------------|-----------------------|
| `APP_NAME` | Title used for the FastAPI backend.    | `"God Mode Ultra Flow"` |
| `VITE_API_BASE` | Base URL the frontend uses for API requests. | `http://localhost:8000` |
