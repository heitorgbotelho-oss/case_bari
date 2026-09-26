@echo off
setlocal
cd /d "%~dp0.."
if errorlevel 1 exit /b %ERRORLEVEL%
set "ROOT=%CD%"
if not exist "%ROOT%\.venv\Scripts\python.exe" (
    echo Ambiente Python ausente. Siga as instrucoes do README.md.
    exit /b 1
)
"%ROOT%\.venv\Scripts\python.exe" "%ROOT%\rpa\gerar_relatorio_semanal.py" %*
exit /b %ERRORLEVEL%
