import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/chatter2$'
    ]
}

async def chatter2(message):
    """Versão avançada do chatter (IA)"""
    await bot.reply_to(message, "🤖 **Chatter 2.0:**\n\nModo avançado de interação ativado.")

from bot import bot
