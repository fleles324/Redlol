import asyncio
import os
import sys
import bot

async def main():
    """Ponto de entrada alternativo para o bot (equivalente ao bot.lua)"""
    # Verifica se as pastas data/ e locales/ existem para o bot (importante para traduções)
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("locales"):
        os.makedirs("locales")

    print("🚀 Iniciando via main.py...")
    # Chama a função principal do bot.py
    await bot.main()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot interrompido.")
        sys.exit(0)
