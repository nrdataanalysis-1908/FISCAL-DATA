# NR Fiscal Intelligence

Plataforma experimental de inteligência fiscal, contábil e financeira para uma empresa fictícia de comércio.

> **Aviso:** esta versão utiliza dados simulados. Não realiza apuração fiscal oficial, não substitui escrituração contábil e não deve ser utilizada para recolhimento de tributos.

## Objetivos

- Consolidar vendas, custos, despesas e documentos fiscais.
- Produzir uma DRE gerencial reproduzível.
- Simular cenários tributários para Simples Nacional e Regime Regular.
- Preparar integrações desacopladas com motores públicos da Reforma Tributária.
- Manter rastreabilidade de dados, regras, versões e resultados.

## Escopo atual

1. API FastAPI com indicadores, movimentações e DRE gerencial.
2. SQLite local, criado automaticamente na primeira inicialização.
3. Base fictícia da NR Tech Store, carregada de forma idempotente.
4. Endpoint de estimativa matemática ilustrativa — a taxa é informada pelo usuário e não é inferida pelo sistema.
5. Dashboard Next.js com indicadores e DRE.

## Tecnologias

- Python 3.12+, FastAPI, Pydantic e SQLAlchemy
- SQLite (sem servidor de banco de dados)
- Next.js 14, React 18 e TypeScript
- Pytest e GitHub Actions

## Estrutura

```text
.
├── backend/
│   ├── app/main.py
│   ├── requirements.txt
│   └── tests/
├── database/
│   ├── init.sql
│   └── fiscal_data.db       # criado automaticamente; não versionado
├── frontend/
│   └── app/
├── docs/
│   ├── architecture.md
│   └── tax-model.md
└── .github/workflows/ci.yml
```

## Execução local no Windows (PowerShell)

Abra um terminal na pasta do projeto.

### 1. Preparar o backend

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .\backend\requirements.txt
```

### 2. Iniciar a API

Na raiz do projeto, com o ambiente virtual ativado:

```powershell
python -m uvicorn app.main:app --app-dir backend --reload
```

Na primeira inicialização, o arquivo `database/fiscal_data.db` e as tabelas serão criados e os dados fictícios serão inseridos automaticamente.

### 3. Iniciar o frontend

Abra outro PowerShell na raiz do projeto:

```powershell
Set-Location "$HOME\FISCAL-DATA\frontend"
npm install
npm run dev
```

Acesse:

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

## Persistência

O banco padrão fica em `database/fiscal_data.db`. O SQLite é embarcado no Python e não exige instalação de servidor, PostgreSQL, Docker ou serviço externo. Não é necessário configurar `DATABASE_URL`.

## Motores públicos de referência

- [Calculadora RTC — Regime Regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular)
- [Calculadora RTC — Simples Nacional](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional)

A integração será implementada por adaptadores independentes após análise dos contratos, instruções de execução, dependências, licença e versões de cada repositório. Não presumimos compatibilidade de API entre os motores.

## Princípios de engenharia

- Valores monetários tratados com `Decimal` na camada Python.
- Regime tributário, natureza da operação e classificação fiscal não são intercambiáveis.
- Nenhuma alíquota universal aplicada indiscriminadamente ao faturamento.
- Regras fiscais devem possuir fonte normativa, vigência e versão.
- Simulações devem ser explicitamente identificadas e segregadas de dados oficiais.
- Toda integração deve ter testes de contrato e registro de versão.

## Roadmap

- [x] Estrutura inicial e documentação
- [x] Banco SQLite e carga idempotente dos dados demonstrativos
- [x] API de indicadores e DRE demonstrativa
- [x] Interface web de indicadores
- [ ] Cadastro de produtos, NCM e operações
- [ ] Importação de XML fiscal
- [ ] Adaptador do motor RTC — Regime Regular
- [ ] Adaptador do motor RTC — Simples Nacional
- [ ] Comparador de cenários e trilha de auditoria
- [ ] Autenticação, autorização e segregação multiempresa
