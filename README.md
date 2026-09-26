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