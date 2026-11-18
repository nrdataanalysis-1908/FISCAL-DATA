PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    legal_name TEXT NOT NULL,
    trade_name TEXT NOT NULL,
    tax_id TEXT NOT NULL UNIQUE,
    business_type TEXT NOT NULL DEFAULT 'COMMERCE',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    company_id TEXT NOT NULL REFERENCES companies(id),
    occurred_on TEXT NOT NULL,
    description TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    dre_group TEXT NOT NULL,
    amount NUMERIC NOT NULL CHECK (amount >= 0),
    status TEXT NOT NULL DEFAULT 'POSTED',
    source TEXT NOT NULL DEFAULT 'SIMULATED',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tax_scenarios (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    company_id TEXT NOT NULL REFERENCES companies(id),
    regime TEXT NOT NULL CHECK (regime IN ('SIMPLES_NACIONAL', 'REGIME_REGULAR')),
    reference_period TEXT NOT NULL CHECK (length(reference_period) = 7),
    scenario_name TEXT NOT NULL,
    is_simulation INTEGER NOT NULL DEFAULT 1,
    parameters TEXT NOT NULL DEFAULT '{}',
    result TEXT NOT NULL DEFAULT '{}',
    engine_name TEXT,
    engine_version TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_transactions_company_date
    ON transactions(company_id, occurred_on);

INSERT OR IGNORE INTO companies (legal_name, trade_name, tax_id, business_type)
VALUES ('NR Comércio e Tecnologia Ltda.', 'NR Tech Store',
        '00.000.000/0001-00', 'COMMERCE');

-- Lançamentos integralmente fictícios para validar a DRE gerencial.
INSERT INTO transactions
    (company_id, occurred_on, description, transaction_type,
     dre_group, amount, source)
SELECT company.id, item.occurred_on, item.description,
       item.transaction_type, item.dre_group, item.amount, 'SIMULATED'
FROM companies AS company
CROSS JOIN (
    SELECT '2026-10-03' AS occurred_on, 'Venda de notebooks' AS description, 'SALE' AS transaction_type, 'GROSS_REVENUE' AS dre_group, 42000.00 AS amount
    UNION ALL SELECT '2026-10-07', 'Venda de periféricos', 'SALE', 'GROSS_REVENUE', 18500.00
    UNION ALL SELECT '2026-10-12', 'Venda de monitores', 'SALE', 'GROSS_REVENUE', 27500.00
    UNION ALL SELECT '2026-10-18', 'Venda de equipamentos', 'SALE', 'GROSS_REVENUE', 32000.00
    UNION ALL SELECT '2026-10-25', 'Venda de acessórios', 'SALE', 'GROSS_REVENUE', 30000.00
    UNION ALL SELECT '2026-10-31', 'Deduções simuladas sobre vendas', 'TAX_DEDUCTION', 'SALES_DEDUCTIONS', 18000.00
    UNION ALL SELECT '2026-10-10', 'Custo das mercadorias vendidas', 'COGS', 'COGS', 55000.00
    UNION ALL SELECT '2026-10-15', 'Aluguel e condomínio', 'EXPENSE', 'OPERATING_EXPENSES', 8500.00
    UNION ALL SELECT '2026-10-20', 'Folha e encargos gerenciais', 'EXPENSE', 'OPERATING_EXPENSES', 14500.00
    UNION ALL SELECT '2026-10-22', 'Marketing e tecnologia', 'EXPENSE', 'OPERATING_EXPENSES', 9000.00
    UNION ALL SELECT '2026-10-28', 'Resultado financeiro líquido', 'FINANCIAL', 'FINANCIAL_RESULT', 5000.00
    UNION ALL SELECT '2026-10-31', 'Tributos sobre o lucro — simulação', 'INCOME_TAX', 'INCOME_TAX', 8000.00
) AS item
WHERE company.tax_id = '00.000.000/0001-00'
  AND NOT EXISTS (
      SELECT 1 FROM transactions AS existing
      WHERE existing.company_id = company.id
        AND existing.description = item.description
        AND existing.occurred_on = item.occurred_on
  );
