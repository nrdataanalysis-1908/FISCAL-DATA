# NR Fiscal Intelligence

Plataforma experimental de inteligência fiscal, contábil e financeira para uma empresa fictícia de comércio.

> **Aviso:** esta primeira versão utiliza dados simulados. Não realiza apuração fiscal oficial, não substitui escrituração contábil e não deve ser utilizada para recolhimento de tributos.

## Objetivos

- Consolidar vendas, custos, despesas e documentos fiscais.
- Produzir uma DRE gerencial reproduzível.
- Simular cenários tributários para Simples Nacional e Regime Regular.
- Preparar integrações desacopladas com os projetos públicos da Receita Federal.
- Manter rastreabilidade de dados, regras, versões e resultados.

## Escopo inicial

1. API FastAPI com indicadores e DRE gerencial.
2. PostgreSQL com empresa fictícia, lançamentos e cenários tributários.
3. Endpoint de estimativa matemática ilustrativa — a taxa é informada pelo usuário e não é inferida pelo sistema.
4. Documentação da arquitetura e dos limites fiscais.
5. Evolução posterior para integração validada com os motores oficiais.

## Tecnologias

- Python 3.12+, FastAPI, Pydantic e SQLAlchemy
- PostgreSQL 16
- Next.js + TypeScript (interface planejada)
- Docker Compose
- Pytest e GitHub Actions

## Estrutura

```text
.
├── backend/
│   ├── app/main.py
│   ├── requirements.txt
│   └── tests/
├── database/init.sql
├── frontend/app/       # Next.js dashboard
├── docs/
│   ├── architecture.md
│   └── tax-model.md
└── .github/workflows/ci.yml
```

## Execução local

Com Docker Desktop instalado:

```bash
docker compose up --build
```

Dashboard: http://localhost:3000  
API: http://localhost:8000  
Swagger: http://localhost:8000/docs  
Health check: http://localhost:8000/health

Execução manual da API:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints iniciais

- `GET /health`
- `GET /api/v1/dashboard/summary?period=2026-10`
- `GET /api/v1/dre?period=2026-10`
- `GET /api/v1/transactions?period=2026-10`
- `POST /api/v1/tax/scenarios/estimate`

## Motores públicos de referência

- [Calculadora RTC — Regime Regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular)
- [Calculadora RTC — Simples Nacional](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional)

A integração será implementada por adaptadores independentes após análise dos contratos, instruções de execução, dependências, licença e versões de cada repositório. Não presumimos compatibilidade de API entre os motores.

## Princípios de engenharia

- Valores monetários com `Decimal` no Python e `NUMERIC` no PostgreSQL.
- Regime tributário, natureza da operação e classificação fiscal não são intercambiáveis.
- Nenhuma alíquota universal aplicada indiscriminadamente ao faturamento.
- Regras fiscais devem possuir fonte normativa, vigência e versão.
- Simulações devem ser explicitamente identificadas e segregadas de dados oficiais.
- Toda integração deve ter testes de contrato e registro de versão.

## Roadmap

- [x] Estrutura inicial e documentação
- [x] Modelo inicial de dados e DRE demonstrativa
- [ ] Interface web de indicadores
- [ ] Cadastro de produtos, NCM e operações
- [ ] Importação de XML fiscal
- [ ] Adaptador do motor RTC — Regime Regular
- [ ] Adaptador do motor RTC — Simples Nacional
- [ ] Comparador de cenários e trilha de auditoria
- [ ] Autenticação, autorização e segregação multiempresa
