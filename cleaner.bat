@echo off
title Smart File Cleaner - Organizador Inteligente
cls
python "%~dp0main.py" %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocurrio un error al ejecutar el programa.
    pause
)
