@echo off
title Instalar Dependencias - Segurança Privada Bot
echo ==========================================================
echo 🛠 Instalando Dependencias do Bot Segurança Privada (Windows)
echo ==========================================================
echo.

:: Verifica se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python nao encontrado! Instale o Python antes de continuar.
    pause
    exit /b
)

:: Verifica se o pip está instalado
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ O pip nao esta instalado. 
    pause
    exit /b
)

:: Instala as dependencias do requirements.txt
echo 📦 Instalando bibliotecas necessarias...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✅ Instalacao concluida com sucesso!
    echo Agora configure o arquivo .env e execute start.bat.
) else (
    echo.
    echo ❌ Ocorreu um erro durante a instalacao.
)

pause
