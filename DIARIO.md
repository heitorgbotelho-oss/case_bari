# DIARIO.md — Parte 4 | Case Bari

## a) Como usei IA

Usei o **ChatGPT** para discutir regras de análise, estruturar soluções, revisar explicações e código, criar os notebooks e o script de automação. Usei o **Copilot no VS Code** para conferir e corrigir informações sugeridas pelo ChatGPT e ter uma segunda opinião durante a implementação. Comparei as respostas com os dados e o enunciado. A **Gemini API** foi usada como a API chamada pelo notebook de extração dos 17 laudos.

Uma resposta inadequada do ChatGPT surgiu na Parte 3: inicialmente, ele entregou JSONs já preenchidos. Aquilo mostrava um formato, mas não era um **extrator executável e mensurável**, como o case pedia. Pedi para recomeçar. O novo notebook lê os `.txt`, chama a Gemini API, exige o mesmo formato de saída, verifica evidências e compara os campos.

## b) Conceito que aprendi do zero

Em aproximadamente **1 a 2 horas**, aprendi três conceitos e apliquei cada um no projeto:

- **Integração com API de IA:** usei Python para enviar os textos dos laudos à Gemini API, solicitar respostas estruturadas em JSON e validar os resultados no notebook.
- **RPA:** entendi como automatizar uma rotina repetível. No projeto, o script lê os dados, trata e registra a execução e gera um relatório semanal.
- **`.bat` no Windows:** é um arquivo de comandos que inicia o script Python do RPA usando o ambiente virtual e repassa parâmetros, como a data do relatório.


## c) Autocrítica

**O que na minha entrega eu sei que está fraco:**

- Por ainda estar **desenvolvendo meu conhecimento sobre o negócio**, minha análise crítica das premissas e dos resultados ficou limitada. Isso dificultou avaliar se cada parte do projeto atende plenamente às necessidades da área comercial. 

**O que eu faria com mais 40 horas:**

- **Com mais 40 horas de trabalho**, eu buscaria esclarecer o significado de cada demanda com o time de negócio, revisar os scripts linha por linha e validar os resultados à partir dessas regras. Esse aprofundamento permitiria corrigir possíveis inconsistências e apresentar recomendações mais bem fundamentadas.

**Pergunta que eu faria ao time de negócios antes de começar:** 

- Qual decisão vocês esperam tomar com esta análise? Priorizar canais, recuperar propostas paradas ou melhorar a conversão geral?
- Como o negócio calcula o LTV usado na política: com o valor solicitado ou aprovado? Qual avaliação do imóvel vale para essa regra?
- Como funciona cada uma das etapas de forma detalhada? 
