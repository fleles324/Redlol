import os
import sys
import subprocess

def install_dependencies():
    """Script de instalação para o bot em Python (equivalente ao install.sh)"""
    print("🛠 Iniciando a instalação das dependências do Bot Segurança Privada...")
    
    # Verifica se o Python é suportado
    if sys.version_info < (3, 10):
        print("❌ O bot requer Python 3.10 ou superior!")
        sys.exit(1)

    # Verifica se o pip está instalado
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
    except subprocess.CalledProcessError:
        print("❌ O pip não está instalado. Instale-o antes de continuar.")
        sys.exit(1)

    # Instala as dependências do requirements.txt
    print("📦 Instalando dependências (requirements.txt)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Instalação concluída com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro durante a instalação: {e}")
        sys.exit(1)

    # Criação do arquivo .env caso não exista
    if not os.path.exists(".env"):
        print("⚠️ Arquivo .env não encontrado. Criando modelo .env.example...")
        with open(".env.example", "w", encoding="utf-8") as f:
            f.write("# Configurações do Bot\nBOT_API_KEY=TOKEN_AQUI\n\n# Banco de Dados\nSUPABASE_URL=URL_AQUI\nSUPABASE_KEY=KEY_AQUI\n")

    print("\n🚀 Instalação finalizada. Configure o arquivo .env e execute: python launch.py")

if __name__ == "__main__":
    install_dependencies()
