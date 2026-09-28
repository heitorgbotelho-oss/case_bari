# Desafio Prático — Estágio AI & Data Lab | Bari 

Projeto em Python para analisar o funil de crédito com garantia de imóvel, extrair informações de laudos e gerar relatórios semanais.

## Visão geral

Este repositório reúne três entregas principais:

- diagnóstico exploratório do funil, incluindo canais, etapas, status e LTV solicitado;
- extração automatizada de campos de laudos usando IA, com comparação de resultados;
- script para gerar relatório semanal em HTML.

Os documentos principais do projeto estão em:

- [RESUMO_EXECUTIVO.md](RESUMO_EXECUTIVO.md): síntese para liderança comercial;
- [DIARIO.md](DIARIO.md): registro do processo, aprendizados e limitações.

## Estrutura do projeto

```text
case_bari/
├── data/
│   └── raw/
│       ├── propostas_credito.csv
│       └── laudos/
│           ├── laudo_01.txt
│           └── ...
├── notebooks/
│   ├── 01_diagnostico_funil.ipynb
│   └── 03_extracao_ia_laudos_completa.ipynb
├── outputs/
│   ├── graficos/
│   ├── parte3_ia/
│   └── relatorios/
├── rpa/
│   ├── executar_semanal.bat
│   ├── gerar_relatorio_semanal.py
│   └── requirements.txt
├── DIARIO.md
├── README.md
├── RESUMO_EXECUTIVO.md
├── requirements.txt
└── logs/
```

## Requisitos

- Python 3.10+
- pip
- Jupyter / VS Code com suporte a notebooks

Dependências do projeto:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

O arquivo de dependências atual inclui:

- pandas
- numpy
- matplotlib
- ipykernel

## Configuração local

No Windows, abra o PowerShell na raiz do projeto e execute:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Para abrir os notebooks no ambiente virtual:

```powershell
python -m jupyter lab
```

Em seguida, abra um dos notebooks em `notebooks/` e confirme que o kernel selecionado é o da virtualenv `.venv`.

## Notebooks

### 01_diagnostico_funil.ipynb

Notebook principal de análise do funil de crédito. Ele contém:

- leitura e validação do CSV de propostas;
- limpeza e normalização dos campos;
- recorte de registros conforme regra do case;
- cálculo de conversão, canais, status e valor solicitado;
- diagnóstico de LTV solicitado;
- exploração dos pontos de maior valor sem contratação observada.

### 03_extracao_ia_laudos_completa.ipynb

Notebook dedicado à extração estruturada dos 17 laudos com a API Gemini. O processo não se limita a pedir um JSON ao modelo: define um contrato de dados, solicita evidências textuais, valida a resposta localmente e compara os campos extraídos com uma referência que deve ser revisada por uma pessoa.

### Como funciona

1. Abra `notebooks/03_extracao_ia_laudos_completa.ipynb` no VS Code e selecione o kernel da `.venv`. Execute as células de cima para baixo: a primeira instala `google-genai`, Pydantic e pandas. Informe `GEMINI_API_KEY` ou `GOOGLE_API_KEY` quando solicitado. O notebook lê os 17 laudos em `data/raw/laudos/`.
2. Para cada texto, o notebook envia à Gemini API um prompt e um esquema Pydantic, solicitando uma resposta JSON com campos, evidências e alertas. A resposta é validada no Python; em seguida, uma auditoria confere evidências literais e regras básicas. Faça primeiro o teste com um laudo e depois execute o lote. Chamadas à API podem consumir cota.
3. Revise os JSONs e as pendências: formato válido e evidência literal não garantem interpretação correta. A comparação usa uma referência inicial assistida por IA, que deve ser conferida nos documentos originais antes de tratar as métricas como avaliação independente.

Os resultados são salvos em `outputs/parte3_ia/`: JSON individual por laudo, `laudos_extraidos.jsonl`, `execucao.json` com falhas e auditorias, e `comparacao_campos.csv` com diferenças por campo. Reiniciar o kernel perde os resultados mantidos em memória e pode levar a novas chamadas à API.

## Relatório semanal automatizado

O script para gerar o relatório semanal está em:

- `rpa/gerar_relatorio_semanal.py`
- `rpa/executar_semanal.bat`

### Objetivo

O script gera um relatório HTML a partir do CSV `data/raw/propostas_credito.csv`, agrupando propostas pela data de entrada e apresentando:

- propostas recebidas;
- volume contratado;
- conversão observada;
- distribuição por canal;
- valor solicitado não contratado por etapa máxima;
- status final registrado no CSV;
- alertas e contexto de qualidade dos dados.

### Como executar manualmente

Na raiz do projeto, execute:

```powershell
& ".\rpa\executar_semanal.bat"
```

Isso gera um relatório para a semana atual, de segunda a domingo.

Para uma data específica, use:

```powershell
& ".\rpa\executar_semanal.bat" --referencia 2025-01-01
```

A referência seleciona a semana que contém a data informada. O arquivo final fica em:

```text
outputs/relatorios/relatorio_<YYYY-MM-DD>.html
```

onde a data corresponde ao início da semana (segunda-feira). O log da execução é gravado em:

```text
logs/execucao.log
```

O arquivo `.bat` executa o script quando chamado; ele não cria um agendamento. Para rodar semanalmente sem intervenção, configure uma tarefa no Agendador de Tarefas do Windows.

## Dados

### Arquivo principal

```text
data/raw/propostas_credito.csv
```

Contém as propostas de crédito analisadas no funil, com as colunas usadas para:

- identificar entrada da proposta;
- segmentar por canal e tipo de imóvel;
- operar a conversão e etapas do funil;
- calcular valor solicitado e LTV.

### Laudos

Os laudos estão em:

```text
data/raw/laudos/
```

Cada arquivo contém o texto de um laudo sintético utilizado na parte de extração de dados via IA.

## Saídas e artefatos

- `outputs/graficos/`: gráficos de diagnóstico e exploração;
- `outputs/parte3_ia/`: JSONs e comparações da extração de laudos;
- `outputs/relatorios/`: relatórios HTML gerados pelo script semanal;
- `logs/`: registros de execução e erros.

## Observações importantes

- O projeto foi desenvolvido com dados sintéticos do case Bari.
- Os registros de `Terreno` foram excluídos da análise principal, conforme regra do desafio.
- A conversão e os indicadores são observacionais; não representam causalidade entre canal, etapa e contratação.
- O relatório semanal usa o status atual presente no CSV da execução, sem histórico completo de mudança de status ao longo do tempo.

## Fluxo recomendado

1. Preparar ambiente virtual e instalar dependências.
2. Abrir e executar `notebooks/01_diagnostico_funil.ipynb`.
3. Executar a extração de laudos seguindo o passo a passo acima, se essa etapa fizer parte da análise.
4. Revisar o resumo executivo em [RESUMO_EXECUTIVO.md](RESUMO_EXECUTIVO.md).
5. Executar o relatório semanal com `rpa/executar_semanal.bat`, se necessário.
6. Consultar `DIARIO.md` para contexto do processo, limitações e aprendizados.

A conta do Windows que executa a tarefa precisa ter permissão de leitura no CSV e de gravação em `outputs/relatorios` e `logs`. O BAT localiza a raiz do projeto a partir do próprio arquivo, mesmo que o Agendador use outro diretório de trabalho.
