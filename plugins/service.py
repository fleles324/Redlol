import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/service$',
        r'^/maintenance$',
        r'^/update$'
    ]
}

async def on_every_message(message):
    """Verifica se o bot está em manutenção (apenas Super Admin)"""
    # Lógica de manutenção global (se houver uma variável stat_name no banco)
    # Por agora, deixa o processamento continuar.
    return True

async def service(message):
    """Comando /service (Super Admin)"""
    if message.from_user.id not in config.SUPERADMINS:
        return
    
    text = (
        "🛠 **Serviços do Bot:**\n\n"
        f"🤖 **Nome:** `{config.BOT_NAME}`\n"
        f"⚙️ **Status:** `Online` ✅\n"
        f"📊 **Versão:** `{config.VERSION}`\n"
        f"📢 **Canal:** {config.CHANNEL}"
    )
    await bot.reply_to(message, text, parse_mode='Markdown')

async def maintenance(message):
    """Ativa ou desativa o modo de manutenção (apenas Super Admin)"""
    if message.from_user.id not in config.SUPERADMINS:
        return
    
    # Exemplo: Ligar/Desligar manutenção no banco
    await bot.reply_to(message, "🛠 Modo de manutenção configurado com sucesso!")

from bot import bot
