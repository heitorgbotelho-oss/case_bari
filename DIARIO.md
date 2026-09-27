# DIARIO.md — Parte 4 | Case Bari

## a) Como usei IA

Usei o **ChatGPT** para discutir as regras de limpeza do CSV, gerar e comentar o notebook do funil, estruturar o script do relatório semanal e revisar o código. Na extração dos laudos, usei a **API Gemini** para ler os textos e devolver campos em JSON. Executei e revisei os resultados dos 17 laudos. Conferi decisões no enunciado, nos arquivos originais e nas saídas, em vez de aceitar uma resposta apenas por parecer plausível.

Um erro de rumo concreto ocorreu na Parte 3: a primeira resposta da IA foi produzir JSONs preenchidos manualmente. Isso demonstrava um formato, mas não resolvia o pedido de **construir e medir um extrator**. Pedi para recomeçar. A solução passou a fazer chamadas à API para cada laudo, exigir um esquema de saída, preservar evidências e alertas e comparar os campos com uma referência revisável. A referência começou com auxílio de IA; por isso, uma pontuação obtida contra ela precisa ser apresentada com essa ressalva e com as correções justificadas pelo texto original.

Outra falha apareceu no teste do notebook: o comparador tentava ler um campo de um laudo que ainda não tinha resposta, produzindo um erro. Corrigi a comparação para registrar esse documento como **não extraído** e manter os nove campos dele no denominador, sem inflar a taxa de acerto. Também mantive a divergência de área total do laudo 17 (95 e 92 m²) sem escolher um valor, e distingui a penhora cancelada do laudo 13 de um ônus ativo.

Na Parte 1, a IA ajudou a montar os gráficos, mas precisei revisar sua interpretação. A barra da etapa 3 soma **crédito solicitado** por propostas não contratadas que chegaram até essa etapa; não comprova receita perdida ali. A conversão menor dos correspondentes é uma associação bruta, não prova que o canal causou a queda. Removi os 535 registros de **Terreno** da análise do CSV porque o enunciado mandava, preservando os arquivos brutos e incluindo os laudos de terreno na Parte 3.

## b) Conceito que aprendi do zero: LTV

Aprendi **loan-to-value (LTV)** a partir do enunciado, do cálculo no notebook e das explicações que pedi à IA. É a proporção entre o crédito e o valor do imóvel dado em garantia. Se alguém pede R$ 300 mil e o imóvel vale R$ 500 mil, o LTV solicitado é **60%** (`300.000 ÷ 500.000`). Levei aproximadamente **1 a 2 horas** para entender a fórmula e, principalmente, seu limite de interpretação. A política informa teto de 60%, mas o CSV permite calcular o LTV do **valor solicitado**, não confirma qual valor aprovado e qual avaliação final foram usados na decisão. Por isso não classifiquei automaticamente cada contrato acima de 60% no cálculo exploratório como violação da política.

## c) Autocrítica

O ponto mais fraco da análise do funil é a ausência de histórico das mudanças de status: a conversão por mês de entrada pode mudar conforme as propostas amadurecem. Os impactos das recomendações são **cenários condicionados às premissas**, não previsão de receita. Na Parte 3, há apenas 17 documentos sintéticos; evidência literal e JSON válido não garantem interpretação correta, e a referência de comparação nasceu assistida por IA. A revisão precisa ser demonstrável campo a campo.

Com **mais 40 horas**, eu pediria histórico de transições e valores efetivamente aprovados/desembolsados, compararia coortes com o mesmo tempo de maturação e testaria as recomendações em grupos comparáveis. No extrator, faria uma segunda anotação independente dos laudos, mediria concordância entre revisores, ampliaria os casos de teste e avaliaria falhas por formato, ausência, contradição e tipo de ônus.

**Pergunta que eu faria ao time de negócios antes de começar:** qual valor do imóvel, qual valor do crédito e qual momento do processo definem o LTV usado na regra de 60%, e como são registradas as exceções?

**Fontes usadas:** enunciado e dados sintéticos fornecidos no case; documentação oficial da [Gemini API (saída estruturada)](https://ai.google.dev/gemini-api/docs/structured-output). Nenhum dado real de cliente foi utilizado.
