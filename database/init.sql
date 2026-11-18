CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    legal_name VARCHAR(180) NOT NULL,
    trade_name VARCHAR(120) NOT NULL,
    tax_id VARCHAR(18) NOT NULL UNIQUE,
    business_type VARCHAR(40) NOT NULL DEFAULT 'COMMERCE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id),
    occurred_on DATE NOT NULL,
    description VARCHAR(220) NOT NULL,
    transaction_type VARCHAR(30) NOT NULL,
    dre_group VARCHAR(40) NOT NULL,
    amount NUMERIC(15,2) NOT NULL CHECK (amount >= 0),
    status VARCHAR(20) NOT NULL DEFAULT 'POSTED',
    source VARCHAR(30) NOT NULL DEFAULT 'SIMULATED',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS tax_scenarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id),
    regime VARCHAR(30) NOT NULL
        CHECK (regime IN ('SIMPLES_NACIONAL', 'REGIME_REGULAR')),
    reference_period CHAR(7) NOT NULL,
    scenario_name VARCHAR(100) NOT NULL,
    is_simulation BOOLEAN NOT NULL DEFAULT TRUE,
    parameters JSONB NOT NULL DEFAULT '{}'::jsonb,
    result JSONB NOT NULL DEFAULT '{}'::jsonb,
    engine_name VARCHAR(100),
    engine_version VARCHAR(80),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_transactions_company_date
    ON transactions(company_id, occurred_on);

INSERT INTO companies (legal_name, trade_name, tax_id, business_type)
VALUES ('NR Comércio e Tecnologia Ltda.', 'NR Tech Store',
        '00.000.000/0001-00', 'COMMERCE')
ON CONFLICT (tax_id) DO NOTHING;

-- Lançamentos integralmente fictícios para validar a DRE gerencial.
WITH company AS (
    SELECT id FROM companies WHERE tax_id = '00.000.000/0001-00'
)
INSERT INTO transactions
    (company_id, occurred_on, description, transaction_type,
     dre_group, amount, source)
SELECT company.id, item.occurred_on::date, item.description,
       item.transaction_type, item.dre_group, item.amount, 'SIMULATED'
FROM company
CROSS JOIN (VALUES
    ('2026-10-03','Venda de notebooks','SALE','GROSS_REVENUE',42000.00),
    ('2026-10-07','Venda de periféricos','SALE','GROSS_REVENUE',18500.00),
    ('2026-10-12','Venda de monitores','SALE','GROSS_REVENUE',27500.00),
    ('2026-10-18','Venda de equipamentos','SALE','GROSS_REVENUE',32000.00),
    ('2026-10-25','Venda de acessórios','SALE','GROSS_REVENUE',30000.00),
    ('2026-10-31','Deduções simuladas sobre vendas','TAX_DEDUCTION','SALES_DEDUCTIONS',18000.00),
    ('2026-10-10','Custo das mercadorias vendidas','COGS','COGS',55000.00),
    ('2026-10-15','Aluguel e condomínio','EXPENSE','OPERATING_EXPENSES',8500.00),
    ('2026-10-20','Folha e encargos gerenciais','EXPENSE','OPERATING_EXPENSES',14500.00),
    ('2026-10-22','Marketing e tecnologia','EXPENSE','OPERATING_EXPENSES',9000.00),
    ('2026-10-28','Resultado financeiro líquido','FINANCIAL','FINANCIAL_RESULT',5000.00),
    ('2026-10-31','Tributos sobre o lucro — simulação','INCOME_TAX','INCOME_TAX',8000.00)
) AS item(occurred_on, description, transaction_type, dre_group, amount)
WHERE NOT EXISTS (
    SELECT 1 FROM transactions existing
    WHERE existing.company_id = company.id
      AND existing.description = item.description
      AND existing.occurred_on = item.occurred_on::date
);
