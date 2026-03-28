@echo off
title Redlol Bot - Local Server
echo ==========================================================
echo 🚀 Iniciando o Bot Segurança Privada (Seguranca Privada)
echo ==========================================================
echo.

:: Verifica se o Python está no PATH
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python nao encontrado! Por favor, instale o Python 3.10 ou superior.
    pause
    exit /b
)

:: Verifica se o arquivo .env existe
if not exist .env (
    echo ⚠️ Arquivo .env nao encontrado! 
    echo Criando um modelo basico... Configure-o antes de rodar novamente.
    echo BOT_API_KEY=TOKEN_AQUI > .env
    echo SUPABASE_URL=URL_AQUI >> .env
    echo SUPABASE_KEY=KEY_AQUI >> .env
    pause
    exit /b
)

:: Inicia o bot com loop de reinicializacao automatica
:loop
echo [%time%] 🤖 Bot iniciado...
python bot.py
echo.
echo ⚠️ O bot parou de funcionar ou foi encerrado.
echo [%time%] Reiniciando em 5 segundos... (Pressione Ctrl+C para cancelar)
timeout /t 5 >nul
goto loop
