import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/about$',
        r'^/sobre$',
        r'^/version$',
        r'^/creator$'
    ]
}

async def about(message):
    """Informações sobre o bot e o criador"""
    text = (
        f"🤖 **Sobre o {config.BOT_NAME}:**\n\n"
        "Este bot foi desenvolvido para ser um assistente multifuncional "
        "de segurança, moderação e suporte para grupos de Telegram.\n\n"
        f"👤 **Criador:** [Segurança Privada](https://t.me/SegurancaPrivadaBot)\n"
        f"📢 **Canal Oficial:** {config.CHANNEL}\n"
        f"🛠 **Versão:** `{config.VERSION}`\n"
        "⚙️ **Tecnologia:** `Python` (`async_telebot`) & `Supabase` (PostgreSQL)\n\n"
        "Se você precisar de ajuda, use o comando `/help` ou entre em contato "
        "através do comando `/atendimento` no privado."
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📢 Canal Oficial", url=config.CHANNEL))
    keyboard.add(types.InlineKeyboardButton("🎧 Suporte", url=config.HELP_GROUPS_LINK))
    
    await bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

async def version(message):
    """Mostra a versão atual do bot"""
    await bot.reply_to(message, f"🤖 **Versão do Bot:** `{config.VERSION}`", parse_mode='Markdown')

from bot import bot
