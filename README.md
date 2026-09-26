# case_bari

## Executar o notebook

O notebook do projeto está em `notebooks/teste.ipynb`. No Windows, abra o PowerShell na pasta raiz do projeto e execute:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install jupyterlab
python -m jupyter lab
```

No JupyterLab, abra `notebooks/teste.ipynb` e execute as células com **Run All**. Também é possível abrir esse arquivo no VS Code, selecionar o kernel Python do ambiente `.venv` e usar **Run All**.

O notebook atualmente contém apenas exemplos básicos de Python e não precisa de bibliotecas adicionais. O arquivo de dados está em `data/raw/propostas_credito.csv`; como o JupyterLab é iniciado na raiz do projeto, esse é o caminho relativo a usar quando o notebook passar a carregar o CSV. A instrução de upload presente no notebook é voltada ao Google Colab e não é necessária para execução local.

## Parte 2: relatório semanal automatizado

A Parte 2 gera um relatório HTML usando o CSV `data/raw/propostas_credito.csv`:

- `rpa/gerar_relatorio_semanal.py` carrega e valida os dados, calcula os indicadores e grava o relatório.
- `rpa/executar_semanal.bat` ativa o fluxo usando o Python do ambiente `.venv` na raiz do projeto e encaminha os argumentos para o script.

### Preparar o ambiente

Na primeira configuração, abra o PowerShell na raiz do projeto e instale as dependências no ambiente virtual usado pelo BAT:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Confirme que `data/raw/propostas_credito.csv` existe antes de executar o relatório.

### Executar manualmente

Para gerar o relatório da semana atual, de segunda a domingo, execute o BAT **sem parâmetros**:

```powershell
& ".\rpa\executar_semanal.bat"
```

Para gerar o relatório da semana que contém uma data específica, informe `--referencia` no formato `AAAA-MM-DD`:

```powershell
& ".\rpa\executar_semanal.bat" --referencia 2025-01-01
```

Esse exemplo seleciona a semana de segunda-feira, 30/12/2024, a domingo, 05/01/2025. A referência seleciona a semana que contém a data; não significa necessariamente uma semana começando no dia 1º do mês. Não passe uma referência fixa na tarefa recorrente, a menos que queira que ela gere sempre o relatório histórico daquela semana.

Por padrão, o HTML é gravado em `outputs/relatorios/relatorio_DATA.html`, em que `DATA` é a segunda-feira que inicia o período. A execução e eventuais erros também são registrados em `logs/execucao.log`. Se o CSV não tiver propostas na semana escolhida, o relatório será gerado com zero propostas e um alerta de período vazio.

### Agendar no Agendador de Tarefas do Windows

1. Abra o menu Iniciar, pesquise **Agendador de Tarefas** e abra o aplicativo.
2. No painel **Ações**, escolha **Criar Tarefa Básica...**. Dê um nome, por exemplo `Relatório semanal do funil`, e avance.
3. Escolha a frequência desejada, normalmente **Semanal**, e configure dia e horário. Para o relatório da semana atual, agende a execução no momento em que deseja gerar ou atualizar o resumo dessa semana.
4. Em **Ação**, selecione **Iniciar um programa**.
5. Em **Programa/script**, informe o caminho completo do BAT, por exemplo:

	```text
	\case_bari\rpa\executar_semanal.bat
	```

6. Deixe **Adicionar argumentos (opcional)** vazio para gerar a semana atual. Para uma execução histórica pontual, informe, por exemplo, `--referencia 2025-01-01`.
7. Em **Iniciar em (opcional)**, informe a raiz do projeto, por exemplo:

	```text
	\case_bari
	```

8. Conclua o assistente. Para conferir a configuração, localize a tarefa na Biblioteca do Agendador, abra **Propriedades** e use **Executar** para fazer um teste.

A conta do Windows que executa a tarefa precisa ter permissão de leitura no CSV e permissão de gravação nas pastas `outputs/relatorios` e `logs`. O BAT localiza a raiz do projeto a partir do próprio arquivo, então também funciona se o Agendador usar outro diretório de trabalho.