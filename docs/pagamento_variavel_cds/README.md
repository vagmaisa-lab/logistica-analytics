# Estudo Analítico — Simulação de Pagamento Variável

## Objetivo

Este material apresenta uma simulação preliminar de pagamento variável com base na produtividade realizada em julho de 2026. O cálculo é detalhado por **CD, colaborador, empresa e atividade**, permitindo comparar quatro modelos de remuneração variável.

A fonte primária para o detalhamento nominal é a aba **Base**, porque ela contém simultaneamente CD, colaborador, atividade, quantidade, horas, produtividade e meta. A aba **Din_Labor%** é uma visão agregada por CD e atividade, sem o nome individual em todas as linhas; por isso, foi usada como referência de validação agregada, enquanto a Base sustenta o cálculo exato por colaborador. A aba **Simulação_Faixa** foi utilizada para preservar os valores de bônus e os limites de faixa definidos no estudo original.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `CDs_estudo_pagamento_variavel_4_modelos.xlsx` | Base Excel preenchida, com resumo, premissas, consolidação por CD/colaborador e detalhe por registro. |
| `PROMPT_OUTRAS_IAS.md` | Instruções para outra IA revisar o estudo e montar uma apresentação executiva. |
| `README_ESTUDO_PAGAMENTO_VARIAVEL.md` | Documentação metodológica deste estudo. |

## Modelos calculados

| Modelo | Indicador | Fórmula | Regra de pagamento |
|---|---|---|---|
| 1 — Fator de Performance | Fator | `PRODUTIVIDADE / META` | Faixas de fator com bônus de R$ 100, R$ 250 ou R$ 750. |
| 2 — % de Atingimento | Atingimento | `PRODUTIVIDADE / META` | Faixas de 100% a 160% e acima de 160%, conforme `Simulação_Faixa`. |
| 3 — Meta × Horas trabalhadas | Atingimento físico | `QUANTIDADE / (META × HORAS)` | Aplica as faixas do modelo de atingimento ao realizado versus produção-alvo. |
| 4 — Meta × produtividade direta | Produtividade direta relativa | `(QUANTIDADE / HORAS) / META` | Aplica as faixas do modelo de atingimento sobre a produtividade direta calculada. |

## Resultado da simulação

A aba `Base` contém **2.494 registros**. Os modelos 1 e 2 possuem **847 registros elegíveis**, pois exigem produtividade e meta válida, com meta maior que zero. Os modelos 3 e 4 possuem **844 registros elegíveis**, pois exigem adicionalmente quantidade e horas válidas.

| Modelo | Custo estimado |
|---|---:|
| 1 — Fator de Performance | R$ 72.550,00 |
| 2 — % de Atingimento | R$ 215.200,00 |
| 3 — Meta × Horas trabalhadas | R$ 217.000,00 |
| 4 — Meta × produtividade direta | R$ 217.000,00 |

## Premissas críticas

Os valores de pagamento foram transcritos da aba `Simulação_Faixa`: R$ 100 nas cinco primeiras faixas, R$ 250 na faixa seguinte e R$ 750 na faixa superior. Como os valores da aba original estão preenchidos principalmente para **CARREGAMENTO**, o cálculo deve ser tratado como **cenário de simulação**, não como regra definitiva de folha.

Registros com meta igual a zero, horas zeradas, quantidade ausente ou produtividade inválida não recebem valor no modelo correspondente e são destacados no detalhe. Critérios de presenteísmo, intrajornada, afastamento, admissão, teto por CD e prêmio extra não foram aplicados, pois não fazem parte do cálculo solicitado para esta etapa.

O modelo 4 é uma validação independente do modelo 3. Quando a produtividade informada corresponde exatamente a `QUANTIDADE / HORAS`, ambos devem produzir resultados equivalentes. Eventuais diferenças devem ser investigadas como inconsistência de origem ou arredondamento.

## Controle analítico recomendado

Antes de transformar o cenário em regra de pagamento, deve-se validar os valores das faixas por atividade, definir se o pagamento será por registro ou por colaborador consolidado, estabelecer critérios de elegibilidade corporativos e confirmar o tratamento para metas zeradas. O Excel contém a rastreabilidade necessária para essa revisão.

## Fonte

Arquivo Excel recebido pelo usuário: `CDs_simulacao_pagamento_variavel.xlsx`, especialmente as abas `Base` e `Simulação_Faixa`. Não foram utilizados dados externos ou dados simulados.
