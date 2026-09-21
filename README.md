# IGAD Early Warning System

> A hackathon project for environmental hazard monitoring, risk evaluation and early warning generation

This project is being built around one main idea

**take environmental data → understand the risk → explain it clearly → show it in one place → eventually send warnings when they actually matter**

Right now this is still a prototype and we are building the pieces step by step. The goal is not to pretend that it is already a complete disaster management platform. The goal is to get the core system working properly first and then make it reliable enough for real use.

## What this project is

The IGAD Early Warning System is a full stack early warning prototype.

The current system has a FastAPI backend, PostgreSQL database layer, hazard data sources, a risk engine, Gemini based alert generation and a React dashboard.

At the moment the main hazard foundations are around

- rainfall
- river discharge
- flood risk through river discharge thresholds
- drought risk through rainfall thresholds

The architecture is intentionally modular so more hazards and better models can be added later without rebuilding everything.

## Current status

### Working / implemented

- FastAPI backend
- CORS configuration
- Location API
- Hazard readings API
- Alerts API
- PostgreSQL with SQLAlchemy
- Async database support with asyncpg
- Alembic migrations
- Seed data structure
- Common hazard reading format
- Separate data source layer
- Rainfall data source
- River discharge data source foundation
- Risk engine abstraction
- Threshold based risk calculation
- Flood calculator
- Drought calculator
- Risk calculator registry
- Gemini client
- AI alert generation flow
- React frontend with Vite
- Location selection
- Risk level display
- Alert cards
- Risk trend chart foundation
- Tailwind CSS
- Environment based configuration
- Docker Compose setup for PostgreSQL

### What is not finished yet

There are still quite a few things that need to be built before this can be considered a proper operational early warning system.

For example

- continuous automated data ingestion
- stronger validation of external data
- historical data storage and analysis
- better flood and drought models
- proper forecasting
- multi hazard risk
- real time alert triggering
- notification delivery
- authentication and user roles
- proper monitoring and observability
- production deployment
- security hardening
- proper evaluation against historical events

So if you are looking at this repository right now, it is better to think of it as a **working hackathon foundation** rather than a finished platform.

## How it works

The basic idea currently looks like this

```text
External Data Sources
        ↓
Hazard Readings
        ↓
Risk Engine
        ↓
Risk Classification
        ↓
AI Alert Generation
        ↓
PostgreSQL
        ↓
React Dashboard
```

The important part here is that Gemini is not supposed to decide whether a hazard exists.

The data source and risk engine should determine the actual risk.

AI is mainly used to turn the structured result into a warning that a person can understand.

This separation is important because an early warning system should not depend on a language model guessing the underlying hazard level.

## Architecture

```text
┌─────────────────────────┐
│   External Data Sources │
│ Rainfall / River Data   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│      FastAPI Backend    │
│     APIs + Services     │
└────────────┬────────────┘
             │
       ┌─────┴─────┐
       ▼           ▼
┌────────────┐ ┌─────────────┐
│ Risk Engine│ │ AI Alerts   │
│            │ │ Gemini      │
└─────┬──────┘ └──────┬──────┘
      │               │
      └───────┬───────┘
              ▼
     ┌──────────────────┐
     │    PostgreSQL    │
     └────────┬─────────┘
              │
              ▼
     ┌──────────────────┐
     │ React Dashboard  │
     │ Vite + Tailwind  │
     └──────────────────┘
```

## Repository structure

```text
ICAD-Hackathon/
├── backend/
│   ├── app/
│   │   ├── ai_alerts/        # Gemini client and alert generation
│   │   ├── api/              # FastAPI routes
│   │   ├── data_sources/     # External hazard data sources
│   │   ├── db/               # Database and seed logic
│   │   ├── models/           # SQLAlchemy models
│   │   ├── risk_engine/      # Risk calculation logic
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Application services and pipeline
│   │   ├── config.py         # Environment configuration
│   │   └── main.py           # FastAPI entry point
│   ├── alembic/              # Database migrations
│   ├── config/
│   │   └── thresholds.yaml   # Risk thresholds
│   ├── .env.sample
│   ├── docker-compose.yml
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/              # API client
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Application pages
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

## Tech stack

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

### AI and data

- Google Gemini API
- Open-Meteo
- GLOFAS integration point
- Threshold based risk calculations

### Frontend

- React 18
- Vite
- React Router
- Recharts
- Tailwind CSS

## Getting started

### Requirements

You will need

- Python 3.10+
- Node.js 18+
- npm
- PostgreSQL
- Git
- Docker is recommended

### 1. Clone the repository

```bash
git clone https://github.com/bhogesararam23/ICAD-Hackathon.git
cd ICAD-Hackathon
```

### 2. Setup the backend

```bash
cd backend
python -m venv .venv
```

Linux / macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\\Scripts\\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create the environment file

```bash
cp .env.sample .env
```

Then add the required values to `backend/.env`

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/igad_early_warning
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1
GLOFAS_API_KEY=your_glofas_api_key_here
ENVIRONMENT=dev
```

Do not commit the real `.env` file or any API keys.

### 3. Start PostgreSQL

From the repository root

```bash
docker compose -f backend/docker-compose.yml up -d
```

### 4. Run migrations

From `backend/`

```bash
alembic upgrade head
```

### 5. Start the backend

```bash
uvicorn app.main:app --reload
```

The backend will normally be available at

```text
http://localhost:8000
```

### 6. Start the frontend

Open another terminal

```bash
cd frontend
npm install
npm run dev
```

Vite will normally start the frontend at

```text
http://localhost:5173
```

### 7. Build the frontend

```bash
cd frontend
npm run build
```

## Main modules

### Data sources

The data source layer keeps external APIs separate from the rest of the application.

Currently the repository has foundations for rainfall and river discharge data.

The plan is to keep adding sources without making the rest of the backend depend directly on a specific provider.

### Risk engine

The risk engine is designed around separate calculators for different hazards.

Currently there are foundations for

- rainfall based drought risk
- river discharge based flood risk
- generic threshold based classification

The calculator registry makes it possible to add more hazard calculators later.

### AI alerts

The AI alert layer uses Gemini to turn structured risk information into a short warning.

The model gets information such as

- location
- hazard type
- risk level
- current value
- explanation for the risk level

The intention is to keep the generated message understandable and actionable.

Again the AI layer is downstream of the actual risk calculation.

### Dashboard

The React frontend currently provides the basic dashboard structure for selecting locations, viewing risk information, alerts and trend data.

Some parts of the dashboard are still using demo or mock data and will be connected to the full historical and real time pipeline as the project develops.

## Roadmap

This is the part of the project that is most likely to change as we learn more during development.

The current direction is

**working prototype → reliable data pipeline → better risk intelligence → real time warnings → operational system → research and scale**

### Phase 0 — Make the current prototype solid

**Status: in progress**

- [x] Backend and frontend structure
- [x] FastAPI application
- [x] PostgreSQL and SQLAlchemy setup
- [x] Alembic migrations
- [x] Data source abstraction
- [x] Rainfall source foundation
- [x] River discharge source foundation
- [x] Risk engine abstraction
- [x] Flood calculator foundation
- [x] Drought calculator foundation
- [x] Gemini alert generation foundation
- [x] Initial React dashboard
- [ ] Add proper backend tests
- [ ] Add frontend tests
- [ ] Improve API validation and error handling
- [ ] Add better demo/seed data
- [ ] Document API behaviour properly
- [ ] Remove remaining demo/mock dashboard data

### Phase 1 — Build a reliable data pipeline

**Status: next**

- [ ] Scheduled data ingestion
- [ ] Common schema for all hazard readings
- [ ] Data freshness tracking
- [ ] Data quality checks
- [ ] Retries and timeout handling
- [ ] Rate limit handling
- [ ] Historical observations
- [ ] Better external source integration
- [ ] Complete GLOFAS integration
- [ ] Source level logging

The main goal here is simple

**the system should be able to keep getting data without someone manually running everything**

### Phase 2 — Improve risk intelligence

**Status: planned**

- [ ] Region specific thresholds
- [ ] Better flood risk calculation
- [ ] Better drought indicators
- [ ] Trend based risk signals
- [ ] Multi hazard risk
- [ ] Confidence and data quality indicators
- [ ] Historical calibration
- [ ] Forecasting where enough data exists
- [ ] Explain why every risk level was generated
- [ ] Compare models against simple baselines

This phase is important because a threshold alone is not enough for a serious early warning system.

### Phase 3 — Build the actual early warning dashboard

**Status: planned**

- [ ] Location centric dashboard
- [ ] Hazard maps
- [ ] Historical risk timeline
- [ ] Alert history
- [ ] Alert acknowledgement
- [ ] Location subscriptions
- [ ] Severity metadata
- [ ] Confidence metadata
- [ ] Alert expiry
- [ ] Multilingual warnings
- [ ] Better mobile support
- [ ] Accessibility improvements

### Phase 4 — Real time alert delivery

**Status: planned**

- [ ] Background jobs
- [ ] Automatic risk evaluation
- [ ] Automatic alert triggering
- [ ] Email alerts
- [ ] SMS integration
- [ ] WhatsApp integration
- [ ] Push notifications
- [ ] Alert deduplication
- [ ] Escalation logic
- [ ] Alert cancellation and expiry
- [ ] Delivery status tracking

### Phase 5 — Production readiness

**Status: planned**

- [ ] Authentication
- [ ] Role based access
- [ ] Operator dashboard
- [ ] Admin workflows
- [ ] Structured logging
- [ ] Metrics
- [ ] Observability
- [ ] CI/CD
- [ ] Production containers
- [ ] Database backups
- [ ] Migration procedures
- [ ] Secrets management
- [ ] Load testing
- [ ] Security hardening

### Phase 6 — Research and scale

**Status: longer term**

- [ ] Benchmark forecasting methods
- [ ] Model version tracking
- [ ] Region specific models
- [ ] Satellite and remote sensing inputs
- [ ] Environmental anomaly detection
- [ ] Historical event replay
- [ ] Simulation environment
- [ ] False positive / false negative evaluation
- [ ] Warning lead time evaluation
- [ ] Alert usefulness evaluation
- [ ] Larger scale deployment experiments

## Development principles

### Deterministic first

The actual hazard measurement and risk classification should come from data, thresholds or validated models.

AI should mainly help with communication.

### Modular by hazard

Adding a new hazard should not mean rewriting the whole backend.

The idea is to add a data source and a calculator and then connect them through the existing registry and pipeline.

### Explainable warnings

A warning should eventually be traceable back to

1. the source data
2. the hazard reading
3. the risk calculation
4. the threshold or model condition
5. the final warning shown to the user

### Reliability before feature count

There is no point having 20 different features if the basic warning itself cannot be trusted.

So testing, validation and measuring the actual quality of warnings will stay important as the project grows.

## Current limitations

Being transparent about this because this is still a hackathon project

- The project is not production ready
- Some integrations are still foundations rather than complete integrations
- Some frontend visualizations still use mock/demo data
- Risk thresholds are currently rule based
- Forecasting is not implemented yet
- Automated continuous ingestion is not implemented yet
- Real time notification delivery is not implemented yet
- There is no complete authentication system yet
- There is no proper large scale historical validation yet
- The API and data contracts can still change

These are not hidden parts of the project. They are exactly what the roadmap is trying to solve.

## Contributing

This project is still evolving so changes are expected.

A simple workflow is

```text
Issue → Branch → Build → Test → Pull Request → Review → Merge
```

When adding something new, try to keep it modular and update the README when the actual project status changes.

For larger changes it is useful to document changes to

- data sources
- risk calculations
- thresholds
- database models
- API schemas
- alert behaviour

## Security

Never commit

- API keys
- database passwords
- production credentials
- private tokens
- local `.env` files

Use `backend/.env.sample` as the template for local configuration.

## Project status

**Current status: active hackathon prototype**

The repository is being built incrementally. The checkboxes above are meant to reflect what is actually implemented and what is still planned.

If something is marked planned, it should not be assumed to already work.

## License

No license file is currently present in the repository.

A license should be added before treating this as a reusable open source project.
