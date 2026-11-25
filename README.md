# NR Fiscal Intelligence

An experimental tax, accounting, and financial intelligence platform for a fictional retail company.

> **Disclaimer:** This version uses simulated data. It does not perform official tax assessments, replace statutory bookkeeping, or support actual tax payments.

## Objectives

- Consolidate sales, costs, expenses, and tax documents.
- Produce a reproducible management income statement.
- Simulate tax scenarios for Simples Nacional and the Regular Tax Regime.
- Prepare decoupled integrations with public Tax Reform engines.
- Maintain traceability across data, rules, versions, and results.

## Current scope

1. FastAPI service with indicators, transactions, and a management income statement.
2. Local SQLite database, created automatically on first startup.
3. Fictional NR Tech Store dataset, loaded idempotently.
4. Illustrative mathematical estimate endpoint — the rate is supplied by the user and is not inferred by the system.
5. Next.js dashboard with indicators and income statement.

## Technology stack

- Python 3.12+, FastAPI, Pydantic, and SQLAlchemy
- SQLite (no database server required)
- Next.js 14, React 18, and TypeScript
- Pytest and GitHub Actions

## Repository structure

```text
.
├── backend/
│   ├── app/main.py
│   ├── requirements.txt
│   └── tests/
├── database/
│   ├── init.sql
│   └── fiscal_data.db       # created automatically; not versioned
├── frontend/
│   └── app/
├── docs/
│   ├── architecture.md
│   └── tax-model.md
└── .github/workflows/ci.yml
```

## Local setup on Windows (PowerShell)

Open a terminal in the project directory.

### 1. Set up the backend

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .\backend\requirements.txt
```

### 2. Start the API

From the project root, with the virtual environment activated:

```powershell
python -m uvicorn app.main:app --app-dir backend --reload
```

On first startup, the `database/fiscal_data.db` file and its tables are created, and the fictional sample data is inserted automatically.

### 3. Start the frontend

Open another PowerShell window in the project root:

```powershell
Set-Location "$HOME\FISCAL-DATA\frontend"
npm install
npm run dev
```

Open:

- Dashboard: http://localhost:3000
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Endpoints

- `GET /health`
- `GET /api/v1/dashboard/summary?period=2026-10`
- `GET /api/v1/dre?period=2026-10`
- `GET /api/v1/transactions?period=2026-10`
- `POST /api/v1/tax/scenarios/estimate`

## Persistence

The default database is located at `database/fiscal_data.db`. SQLite is embedded in Python and does not require a server installation, PostgreSQL, Docker, or an external service. There is no need to configure `DATABASE_URL`.

## Public reference engines

- [RTC Calculator — Regular Tax Regime](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular)
- [RTC Calculator — Simples Nacional](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional)

Integration will be implemented through independent adapters after reviewing each repository's contracts, execution instructions, dependencies, license, and versions. API compatibility between the engines is not assumed.

## Engineering principles

- Monetary values are handled with `Decimal` in the Python layer.
- Tax regime, transaction nature, and tax classification are not interchangeable.
- No universal tax rate is indiscriminately applied to revenue.
- Tax rules must have a regulatory source, effective period, and version.
- Simulations must be explicitly labeled and kept separate from official data.
- Every integration must have contract tests and version tracking.

## Roadmap

- [x] Initial structure and documentation
- [x] SQLite database and idempotent loading of demonstration data
- [x] API for demonstration indicators and income statement
- [x] Web interface for indicators
- [ ] Product, NCM, and transaction registration
- [ ] Tax XML import
- [ ] RTC engine adapter — Regular Tax Regime
- [ ] RTC engine adapter — Simples Nacional
- [ ] Scenario comparison and audit trail
- [ ] Authentication, authorization, and multi-company data isolation
