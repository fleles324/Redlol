import os
import sys
import subprocess
import time

def run_bot():
    """Script de lançamento para o bot em Python (equivalente ao launch.sh)"""
    print("🚀 Iniciando o Bot Segurança Privada...")
    
    # Verifica se as dependências estão instaladas
    try:
        import telebot
        import dotenv
        import supabase
    except ImportError:
        print("❌ Dependências não encontradas. Executando instalação...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    # Loop para reiniciar o bot em caso de erro (como o launch.sh fazia)
    while True:
        try:
            print("🤖 Bot rodando...")
            subprocess.check_call([sys.executable, "bot.py"])
        except subprocess.CalledProcessError:
            print("⚠️ O bot parou inesperadamente. Reiniciando em 5 segundos...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n🛑 Lançamento interrompido pelo usuário.")
            break

if __name__ == "__main__":
    run_bot()
