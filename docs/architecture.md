# Arquitetura técnica

## Contexto

O sistema atende inicialmente uma empresa fictícia de comércio. Os domínios fiscal, contábil e financeiro devem permanecer separados, embora compartilhem identificadores e eventos.

## Componentes

- **API:** FastAPI, validação Pydantic e serviços de domínio.
- **Persistência:** PostgreSQL; valores monetários em NUMERIC.
- **Interface:** Next.js + TypeScript (próxima etapa).
- **Integrações:** adaptadores independentes para cada motor externo.
- **Qualidade:** Pytest, testes de contrato e CI.

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
