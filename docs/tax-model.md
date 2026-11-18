# Modelo tributário e limites da simulação

## Regimes e enquadramentos

O produto deve suportar cenários Simples Nacional e Regime Regular para os cálculos relacionados à Reforma Tributária. O enquadramento de IRPJ/CSLL — por exemplo, Lucro Real ou Lucro Presumido — deve ser modelado separadamente, pois não é sinônimo de regime de IBS/CBS.

## Determinantes do cálculo

Não existe uma alíquota genérica segura para aplicar indistintamente ao faturamento. A análise pode depender, entre outros fatores, de natureza e destino da operação, classificação do item, NCM/NBS quando aplicável, CST, classificação tributária, data do fato, regime, benefícios, reduções, imunidades, regimes específicos e regras de crédito.

## Requisitos de governança

Toda regra efetivamente implementada deverá registrar:
- fonte normativa e dispositivo;
- início e fim de vigência;
- versão da regra e do motor;
- parâmetros de entrada;
- resultado e memória de cálculo;
- testes e responsável pela revisão.

## Simulador inicial

O endpoint `/api/v1/tax/scenarios/estimate` realiza apenas uma multiplicação matemática com uma taxa percentual fornecida no próprio request. Ele não seleciona alíquotas, não interpreta legislação e não representa uma apuração fiscal.

## DRE

A DRE atual é gerencial e simplificada. Evoluções necessárias incluem competência, devoluções, descontos, cancelamentos, critérios de CMV e estoque, depreciação, resultado financeiro detalhado, plano de contas e fechamento. A apresentação deverá ser validada por profissional contábil antes de qualquer uso oficial.
