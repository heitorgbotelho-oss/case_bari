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

Os principais limites são a falta de histórico e de valores aprovados ou desembolsados, que impede confirmar causas e perdas reais; o RPA foi testado com datas diferentes, mas sobre o mesmo CSV; e o extrator ainda não foi avaliado contra uma referência independente. 

Com **mais 40 horas**, testaria novas cargas e falhas, obteria dados históricos e analisaria linha por linha de cada código, afim de evitar ao máximo falhas.

**Pergunta que eu faria ao time de negócios antes de começar:** Qual decisão de negócio este projeto deve apoiar e quais definições devo usar para medir o resultado — especialmente o que conta como conversão ou perda, qual status considerar e se o valor de crédito é o solicitado, aprovado ou desembolsado

**Fontes usadas:** enunciado e dados sintéticos fornecidos no case; documentação oficial da [Gemini API (saída estruturada)](https://ai.google.dev/gemini-api/docs/structured-output). Nenhum dado real de cliente foi utilizado.
