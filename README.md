# Desafio Prático — Estágio AI & Data Lab | Bari 

Projeto em Python para análise de funil de crédito com garantia de imóvel, diagnóstico do cenário atual e extração estruturada de informações de laudos.

## Visão geral

Este repositório reúne três frentes do case:

- diagnóstico exploratório do funil de crédito;
- avaliação do impacto de canais, etapas e status finais;
- extração automatizada de campos de laudos usando IA, com comparação de resultados;
- relatório semanal automático em HTML para acompanhamento operacional.

Os documentos principais do projeto estão em:

- [RESUMO_EXECUTIVO.md](RESUMO_EXECUTIVO.md): síntese para liderança comercial;
- [DIARIO.md](DIARIO.md): registro do processo, aprendizados e limitações;
- [reports/diagnostico_funil.md](reports/diagnostico_funil.md): relatório do diagnóstico do funil (arquivo ainda em evolução);

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
├── reports/
│   └── diagnostico_funil.md
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

Notebook dedicado à extração de campos de laudos usando IA. Ele inclui:

- leitura dos arquivos em `data/raw/laudos/`;
- normalização do esquema de saída;
- chamadas à API para extração estruturada em JSON;
- comparação dos campos extraídos com uma referência;
- registro de divergências e itens não extraídos.

## Relatório semanal automatizado

A geração do relatório semanal está implementada em:

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

## Dados

### Arquivo principal

```text
data/raw/propostas_credito.csv
```

Contém as propostas de crédito analisadas no funil, com as colunas usadas para:

<<<<<<< HEAD
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
- `logs/`: registros de execução e erros;
- `reports/`: relatórios textuais e consolidados.

## Observações importantes

- O projeto foi desenvolvido com dados sintéticos do case Bari.
- Os registros de `Terreno` foram excluídos da análise principal, conforme regra do desafio.
- A conversão e os indicadores são observacionais; não representam causalidade entre canal, etapa e contratação.
- O relatório semanal usa o status atual presente no CSV da execução, sem histórico completo de mudança de status ao longo do tempo.

## Fluxo recomendado

1. Preparar ambiente virtual e instalar dependências.
2. Abrir e executar `notebooks/01_diagnostico_funil.ipynb`.
3. Revisar o resumo executivo em [RESUMO_EXECUTIVO.md](RESUMO_EXECUTIVO.md).
4. Executar o relatório semanal com `rpa/executar_semanal.bat`.
5. Consultar `DIARIO.md` para contexto do processo, limitações e aprendizados.

## Próximo passo

Se quiser, posso também:

- revisar e enriquecer [reports/diagnostico_funil.md](reports/diagnostico_funil.md);
- criar um guia de execução mais detalhado por etapa;
- preparar uma versão do README em inglês ou com badges e tabela de status.
=======
A conta do Windows que executa a tarefa precisa ter permissão de leitura no CSV e permissão de gravação nas pastas `outputs/relatorios` e `logs`. O BAT localiza a raiz do projeto a partir do próprio arquivo, então também funciona se o Agendador usar outro diretório de trabalho.
>>>>>>> cbc1d02003a6ce4a04dc37293df41a001822dd4d
