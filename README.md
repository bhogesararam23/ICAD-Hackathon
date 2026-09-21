# IGAD Early Warning System

> An early-stage hackathon project for monitoring environmental hazards, evaluating location-level risk, and generating actionable early-warning alerts.

## Overview

**IGAD Early Warning System** is a full-stack prototype built around a simple pipeline:

**data sources → hazard readings → risk evaluation → AI-assisted alerts → web dashboard**

The repository currently contains the foundations of this pipeline: a FastAPI backend, PostgreSQL/SQLAlchemy persistence, Alembic migrations, data-source modules, a risk engine, AI alert generation, and a React + Vite frontend.

The project is under active development. Some modules are foundations or early implementations, so the roadmap below clearly separates the current codebase from planned capabilities.

## Current Status

### Implemented foundations

- FastAPI backend with CORS configuration
- API routers for locations, hazards, and alerts
- SQLAlchemy data models and Pydantic schemas
- PostgreSQL support through asyncpg
- Alembic migration setup
- Dedicated external data-source layer
- Risk-engine structure with:
  - threshold-based risk calculation
  - flood calculation module
  - drought calculation module
  - extensible calculator registry
- AI alert module using Google Gemini
- React 18 frontend with Vite
- React Router and Recharts
- Tailwind CSS setup
- Environment-variable based configuration
- Docker Compose configuration for backend services

### Still in development

The repository is not yet a production-ready early-warning platform. Automated ingestion, extensive validation, forecasting, calibration, historical analytics, user management, notification delivery, observability, security hardening, and deployment automation are part of the roadmap.

## Architecture

```text
┌──────────────────────┐
│ External Data Sources│
│ Open-Meteo / GLOFAS  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ FastAPI Backend      │
│ API + Services       │
└──────────┬───────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌──────────┐ ┌─────────────┐
│ Risk     │ │ AI Alerts   │
│ Engine   │ │ Gemini      │
└────┬─────┘ └──────┬──────┘
     │              │
     └──────┬───────┘
            ▼
┌──────────────────────┐
│ PostgreSQL Database  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ React Dashboard      │
│ Vite + Tailwind      │
└──────────────────────┘
```

## Repository Structure

```text
ICAD-Hackathon/
├── backend/
│   ├── app/
│   │   ├── ai_alerts/       # Gemini client and alert generation
│   │   ├── api/             # FastAPI routes
│   │   ├── data_sources/    # External data integrations
│   │   ├── db/              # Database layer
│   │   ├── models/          # SQLAlchemy models
│   │   ├── risk_engine/     # Hazard/risk calculations
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Application services
│   │   ├── config.py        # Environment configuration
│   │   └── main.py          # FastAPI entry point
│   ├── alembic/             # Database migrations
│   ├── config/
│   │   └── thresholds.yaml  # Risk-threshold configuration
│   ├── .env.sample
│   ├── docker-compose.yml
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/             # Frontend API layer
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page-level UI
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- PostgreSQL
- asyncpg
- Pydantic Settings
- Alembic
- HTTPX
- PyYAML

### AI & Data
- Google Gemini API
- Open-Meteo
- GLOFAS integration point

### Frontend
- React 18
- Vite
- React Router
- Recharts
- Tailwind CSS

## Getting Started

### Prerequisites

Install:

- Python 3.10+
- Node.js 18+
- npm
- PostgreSQL
- Git
- Docker (recommended for local database setup)

### 1. Clone

```bash
git clone https://github.com/bhogesararam23/ICAD-Hackathon.git
cd ICAD-Hackathon
```

### 2. Configure the backend

```bash
cd backend
python -m venv .venv
```

Activate the environment.

**Linux/macOS**
```bash
source .venv/bin/activate
```

**Windows**
```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the environment file:

```bash
cp .env.sample .env
```

Set valid values for the required variables in `backend/.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/igad_early_warning
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1
GLOFAS_API_KEY=your_glofas_api_key_here
ENVIRONMENT=dev
```

### 3. Start PostgreSQL

From the repository root:

```bash
docker compose -f backend/docker-compose.yml up -d
```

### 4. Run migrations

From `backend/`:

```bash
alembic upgrade head
```

### 5. Start the backend

From `backend/`:

```bash
uvicorn app.main:app --reload
```

### 6. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite will print the local URL, normally `http://localhost:5173`.

### 7. Build the frontend

```bash
cd frontend
npm run build
```

## Core Modules

### Risk Engine

The backend contains an extensible risk-engine structure with a registry and hazard-specific calculators. The current repository includes flood, drought, and threshold-based calculation foundations.

### AI Alerts

The `ai_alerts` module contains a Gemini client and alert-generation workflow. Its intended role is to turn structured hazard and risk information into understandable warning messages.

AI should remain downstream of deterministic data and risk calculations and should not be treated as the source of hazard measurements.

### Data Sources

A dedicated data-source layer isolates external APIs from application logic. Current configuration includes Open-Meteo and a GLOFAS integration point.

### API

The FastAPI application currently includes router groups for:

- Locations
- Hazards
- Alerts

The API contract is still evolving.

## Roadmap

The roadmap is deliberately ordered as:

**prototype hardening → reliable intelligence → real-time warning → operational scale**

### Phase 0 — Prototype Hardening
**Status: In progress**

- [x] Establish frontend/backend structure
- [x] Create FastAPI application
- [x] Add PostgreSQL/SQLAlchemy foundation
- [x] Add Alembic migration framework
- [x] Create risk-engine abstraction
- [x] Add initial flood and drought calculator modules
- [x] Add Gemini alert-generation foundation
- [x] Create initial React dashboard
- [ ] Add backend unit/integration tests
- [ ] Add frontend component tests
- [ ] Add API examples and documentation
- [ ] Add consistent validation/error handling
- [ ] Add seed/demo data

### Phase 1 — Reliable Hazard Data Pipeline
**Status: Planned**

- [ ] Build scheduled data ingestion
- [ ] Normalize external data into a common hazard-reading schema
- [ ] Track source freshness and data quality
- [ ] Add retries, timeouts, and rate-limit handling
- [ ] Store historical observations
- [ ] Validate incoming measurements before risk calculation
- [ ] Complete GLOFAS integration
- [ ] Add additional authoritative environmental sources

### Phase 2 — Risk Intelligence
**Status: Planned**

- [ ] Make thresholds configurable per hazard and region
- [ ] Add trend and time-window signals
- [ ] Add multi-hazard risk aggregation
- [ ] Add confidence/data-quality indicators
- [ ] Calibrate thresholds against historical events
- [ ] Add forecasting models where sufficient data exists
- [ ] Produce explainable risk factors for every warning

### Phase 3 — Early-Warning Dashboard
**Status: Planned**

- [ ] Build complete location-centric dashboard
- [ ] Add hazard maps
- [ ] Add historical risk timelines
- [ ] Add alert history and acknowledgement
- [ ] Add location subscriptions
- [ ] Add severity, confidence, and expiry metadata
- [ ] Add multilingual warnings
- [ ] Improve accessibility

### Phase 4 — Real-Time Alert Delivery
**Status: Planned**

- [ ] Add background job/scheduling infrastructure
- [ ] Trigger alerts automatically from risk conditions
- [ ] Add email delivery
- [ ] Add SMS/WhatsApp/push integrations
- [ ] Add alert deduplication and escalation
- [ ] Add alert expiry/cancellation workflows
- [ ] Track delivery status

### Phase 5 — Operational Platform
**Status: Planned**

- [ ] Add authentication and role-based access
- [ ] Add operator/admin workflows
- [ ] Add structured logging, metrics, and observability
- [ ] Add alert-decision audit trails
- [ ] Add CI/CD
- [ ] Containerize production deployment
- [ ] Add database backup and migration procedures
- [ ] Add secrets management
- [ ] Add performance/load testing
- [ ] Add security hardening

### Phase 6 — Research & Scale
**Status: Planned**

- [ ] Benchmark forecasting approaches against baselines
- [ ] Add model/version tracking
- [ ] Support region-specific models
- [ ] Investigate satellite and remote-sensing inputs
- [ ] Add environmental anomaly detection
- [ ] Add historical-event replay/simulation
- [ ] Measure false positives and false negatives
- [ ] Measure warning lead time and alert usefulness
- [ ] Evaluate larger-scale deployment

## Development Principles

### Deterministic first, generative second

Measurements and risk decisions should come from structured data, explicit thresholds, or validated models. Generative AI is intended primarily for communication and summarization.

### Modular by hazard

A new hazard should be addable through independent data adapters and calculators without rewriting the whole system.

### Explainable warnings

Each warning should be traceable to:

1. source data,
2. evaluated hazard/risk,
3. threshold or model condition,
4. generated warning content.

### Reliability before feature count

Testing, validation, observability, and measurable warning quality are core project requirements, not post-hackathon cleanup.

## Contributing

The project is under active development.

Recommended workflow:

```text
Issue → Branch → Implementation → Tests → Pull Request → Review → Merge
```

Keep changes modular and document changes to:

- data-source contracts
- database models
- thresholds
- API schemas
- alert behaviour

## Security

Never commit:

- API keys
- database passwords
- production credentials
- private tokens
- local `.env` files

Use `backend/.env.sample` as the configuration template.

## Project Status

This repository is an evolving hackathon prototype. The **Implemented foundations** section describes code that exists in the current repository; items in the roadmap are future work and are not claimed as completed.

## License

No license file is currently present. Add an appropriate license before distributing the project for reuse.
