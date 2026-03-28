import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/sobre$'
    ]
}

async def sobre(message):
    """Informações detalhadas sobre o bot (Alias para about)"""
    text = (
        f"🤖 **Sobre o {config.BOT_NAME}:**\n\n"
        "Este bot foi reconstruído em Python para oferecer o máximo de performance "
        "e segurança para sua comunidade.\n\n"
        "Desenvolvido com 💙 para Segurança Privada."
    )
    await bot.reply_to(message, text, parse_mode='Markdown')

from bot import bot
