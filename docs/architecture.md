# Arquitetura técnica

## Contexto

O sistema atende inicialmente uma empresa fictícia de comércio. Os domínios fiscal, contábil e financeiro devem permanecer separados, embora compartilhem identificadores e eventos.

## Componentes

- **API:** FastAPI, validação Pydantic e SQLAlchemy.
- **Persistência:** SQLite local, sem servidor de banco de dados.
- **Interface:** Next.js + TypeScript.
- **Integrações:** adaptadores independentes para cada motor externo.
- **Qualidade:** Pytest, testes de contrato e CI.

## Persistência local

O arquivo padrão é `database/fiscal_data.db`. Na inicialização da API, o script `database/init.sql` cria as tabelas e insere a empresa e os lançamentos fictícios, sem duplicá-los em reinicializações. O SQLite utiliza tipos nativos simples: identificadores em TEXT, datas em texto ISO-8601, valores monetários em NUMERIC e estruturas JSON em TEXT.

Não há dependência de PostgreSQL, Docker ou serviço externo para o ambiente local. Para cenários multiusuário ou concorrência elevada, a camada de persistência poderá ser migrada posteriormente para PostgreSQL gerenciado, sem tornar isso requisito de desenvolvimento.

## Domínios previstos

1. Cadastro de empresas, estabelecimentos, produtos e parceiros.
2. Comercial: vendas, itens, devoluções e descontos.
3. Financeiro: contas a pagar/receber, liquidação e fluxo de caixa.
4. Contábil: plano de contas, partidas e competência.
5. Fiscal: documentos, operações, classificações, débitos e créditos.
6. Governança: fonte normativa, vigência, versão e trilha de auditoria.

## Integração com os motores RTC

Criar contratos internos separados, por exemplo `RegularTaxEngine` e `SimplesTaxEngine`. Cada adaptador deverá encapsular transporte, autenticação se aplicável, serialização, tratamento de erros e versão do motor.

Antes de implementar cada adaptador, inspecionar o README, licença, requisitos, exemplos, modelos de entrada/saída e testes do repositório oficial. Não assumir que ambos possuem o mesmo contrato ou que uma API HTTP esteja disponível sem executar e verificar.

Registrar por cálculo: identificador da operação, motor e versão, referência de código, parâmetros enviados, resposta, timestamp e estado. Proteger dados sensíveis e evitar armazenar documentos completos sem necessidade.

## Segurança e produção

Antes de dados reais: autenticação, autorização por empresa, segregação multi-tenant, gestão de segredos, criptografia, logs sem dados sensíveis, backup, retenção e revisão de segurança.
