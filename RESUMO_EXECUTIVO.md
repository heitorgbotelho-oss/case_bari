# Resumo executivo — Funil de crédito com garantia de imóvel

**Para:** liderança comercial | **Base:** propostas de 2024–2025, dados sintéticos do case Bari

## Leitura para decisão

Após o recorte exigido pelo desafio (535 propostas com imóvel do tipo Terreno excluídas), analisamos **5.865 propostas**, das quais **1.128 foram contratadas**: conversão observada de **19,23%**.

- **Onde está o maior valor sem contratação observada:** as **1.657 propostas não contratadas** cuja etapa máxima foi a **análise de crédito (etapa 3)** somam **R$ 649,85 milhões solicitados**, ou **35,23%** do valor solicitado não contratado nas etapas válidas. Isso indica onde investigar e testar ações, mas não significa que toda a quantia tenha sido perdida ali ou possa ser recuperada.
- **A conversão caiu?** O resultado observado passou de **20,31% em 2024** para **18,43% em 2025** (−1,88 ponto percentual). Há sinal de queda, mas a faixa aproximada para essa diferença vai de **−3,93 a +0,17 ponto** e inclui zero. Além disso, propostas recentes podem não ter tido o mesmo tempo para contratar. Não concluiria ainda que existe uma tendência persistente.
- **Correspondentes merecem atenção:** contrataram **223 de 1.627 propostas (13,71%)**, abaixo das taxas brutas dos demais canais, entre **20,03% e 22,83%**. A diferença é real nesta base, mas pode refletir o perfil dos clientes e das garantias; o dado não prova que o canal causou a variação geral. Score e LTV solicitado também se associam à contratação, sem demonstrar causa isolada.

## Três ações para testar, em ordem de prioridade

| Prioridade | Piloto proposto | Cenário de crédito adicional contratado* |
|---|---|---:|
| 1 | Qualificação e acompanhamento de correspondentes, com grupo de comparação | **R$ 12,69 mi**, se a conversão subir **2 pontos percentuais** sobre R$ 634,51 mi solicitados no canal, mantendo o ticket médio |
| 2 | Contato ativo com **526** propostas “Sem retorno” que chegaram à etapa 3 | **R$ 10,38 mi**, se **5%** dos R$ 207,69 mi solicitados nesse grupo virarem contratos |
| 3 | Checklist e lembretes para **398** propostas com documentação pendente na etapa 5 | **R$ 7,63 mi**, se **5%** dos R$ 152,57 mi solicitados nesse grupo virarem contratos |

\* **Cenários, não previsões:** os percentuais são hipóteses para dimensionar pilotos. Os públicos podem se sobrepor, portanto **não se somam** os três valores. Crédito solicitado adicional não equivale a receita, lucro ou desembolso.

**Decisão solicitada:** autorizar pilotos controlados e informar a **data de corte dos status**, o histórico de passagem entre etapas e os **valores de crédito aprovados/desembolsados**. Esses dados permitem distinguir propostas ainda abertas de perdas definitivas e avaliar o retorno real das ações. O LTV calculado aqui usa o pedido original; contratos acima de 60% nessa medida não comprovam exceção à política sem conhecer o valor aprovado e a avaliação adotada.

**Fonte e método:** `propostas_credito.csv` fornecido no desafio e `notebooks/01_diagnostico_funil_comentado.ipynb`. Valores nominais; cada proposta não contratada é atribuída uma vez à etapa máxima alcançada. Comparações entre grupos são descritivas.
