from decimal import Decimal, ROUND_HALF_UP
import os
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://fiscal_data:change_me@localhost:5432/fiscal_data",
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

app = FastAPI(
    title="NR Fiscal Intelligence API",
    version="0.1.0",
    description="API demonstrativa de inteligência contábil, fiscal e financeira.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def get_company_id(conn):
    company = conn.execute(
        text("SELECT id FROM companies WHERE tax_id = :tax_id"),
        {"tax_id": "00.000.000/0001-00"},
    ).scalar_one_or_none()
    if company is None:
        raise HTTPException(status_code=404, detail="Empresa demonstrativa não encontrada.")
    return company


def period_filter(period: str) -> dict:
    if len(period) != 7 or period[4] != "-":
        raise HTTPException(status_code=422, detail="Período deve seguir AAAA-MM.")
    return {"period": period}


@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected", "version": "0.1.0"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Banco de dados indisponível.") from exc


@app.get("/api/v1/transactions")
def list_transactions(
    period: str = Query("2026-10", pattern=r"^\d{4}-\d{2}$")
):
    with engine.connect() as conn:
        company_id = get_company_id(conn)
        rows = conn.execute(
            text("""
                SELECT id, occurred_on, description, transaction_type,
                       dre_group, amount, source
                FROM transactions
                WHERE company_id = :company_id
                  AND to_char(occurred_on, 'YYYY-MM') = :period
                ORDER BY occurred_on, description
            """),
            {"company_id": company_id, **period_filter(period)},
        ).mappings().all()

    return [
        {
            "id": str(row["id"]),
            "date": row["occurred_on"].isoformat(),
            "description": row["description"],
            "type": row["transaction_type"],
            "group": row["dre_group"],
            "amount": str(row["amount"]),
            "source": row["source"],
        }
        for row in rows
    ]


@app.get("/api/v1/dre")
def get_dre(period: str = Query("2026-10", pattern=r"^\d{4}-\d{2}$")):
    with engine.connect() as conn:
        company_id = get_company_id(conn)
        rows = conn.execute(
            text("""
                SELECT dre_group, SUM(amount) AS total
                FROM transactions
                WHERE company_id = :company_id
                  AND to_char(occurred_on, 'YYYY-MM') = :period
                  AND status = 'POSTED'
                GROUP BY dre_group
            """),
            {"company_id": company_id, **period_filter(period)},
        ).mappings().all()

    totals = {row["dre_group"]: Decimal(row["total"]) for row in rows}
    zero = Decimal("0.00")
    gross = totals.get("GROSS_REVENUE", zero)
    deductions = totals.get("SALES_DEDUCTIONS", zero)
    net_revenue = gross - deductions
    cogs = totals.get("COGS", zero)
    gross_profit = net_revenue - cogs
    operating_expenses = totals.get("OPERATING_EXPENSES", zero)
    operating_result = gross_profit - operating_expenses
    financial_result = totals.get("FINANCIAL_RESULT", zero)
    before_income_tax = operating_result - financial_result
    income_tax = totals.get("INCOME_TAX", zero)
    net_income = before_income_tax - income_tax
    margin = (net_income / gross * 100) if gross else zero

    def line(label: str, amount: Decimal) -> dict:
        return {"label": label, "amount": str(money(amount))}

    return {
        "period": period,
        "currency": "BRL",
        "is_simulated": True,
        "rows": [
            line("Receita bruta", gross),
            line("(-) Deduções e tributos sobre vendas", -deductions),
            line("Receita líquida", net_revenue),
            line("(-) Custo das mercadorias vendidas", -cogs),
            line("Lucro bruto", gross_profit),
            line("(-) Despesas operacionais", -operating_expenses),
            line("Resultado operacional", operating_result),
            line("(-) Resultado financeiro líquido", -financial_result),
            line("Resultado antes dos tributos sobre o lucro", before_income_tax),
            line("(-) Tributos sobre o lucro", -income_tax),
            line("Lucro líquido gerencial", net_income),
        ],
        "gross_revenue": str(money(gross)),
        "net_revenue": str(money(net_revenue)),
        "net_income": str(money(net_income)),
        "net_margin_percent": str(money(margin)),
        "note": (
            "DRE gerencial demonstrativa. A classificação e a composição "
            "devem ser validadas antes de qualquer uso contábil oficial."
        ),
    }


class TaxEstimateRequest(BaseModel):
    regime: Literal["SIMPLES_NACIONAL", "REGIME_REGULAR"]
    taxable_base: Decimal = Field(ge=0)
    illustrative_rate_percent: Decimal = Field(ge=0, le=100)
    reference_period: str = Field(pattern=r"^\d{4}-\d{2}$")
    scenario_name: str = Field(min_length=3, max_length=100)


@app.post("/api/v1/tax/scenarios/estimate")
def estimate_tax(payload: TaxEstimateRequest):
    estimated = money(
        payload.taxable_base * payload.illustrative_rate_percent / Decimal("100")
    )
    return {
        "regime": payload.regime,
        "reference_period": payload.reference_period,
        "scenario_name": payload.scenario_name,
        "taxable_base": str(money(payload.taxable_base)),
        "illustrative_rate_percent": str(payload.illustrative_rate_percent),
        "estimated_amount": str(estimated),
        "is_simulation": True,
        "engine": "NR illustrative estimator",
        "warning": (
            "Operação matemática com taxa informada no request. "
            "Não consulta legislação, não determina alíquota aplicável "
            "e não constitui apuração tributária oficial."
        ),
    }


@app.get("/api/v1/dashboard/summary")
def dashboard_summary(period: str = Query("2026-10", pattern=r"^\\d{4}-\\d{2}$")):
    dre = get_dre(period)
    transactions = list_transactions(period)
    return {
        "period": period,
        "gross_revenue": dre["gross_revenue"],
        "net_revenue": dre["net_revenue"],
        "net_income": dre["net_income"],
        "net_margin_percent": dre["net_margin_percent"],
        "transaction_count": len(transactions),
        "is_simulated": True,
    }
