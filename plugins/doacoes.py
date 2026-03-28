import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/doacoes$'
    ]
}

async def doacoes(message):
    """Alias para donations.py"""
    text = (
        f"💖 **Apoie o Projeto {config.BOT_NAME}**\n\n"
        "Ajude-nos a crescer fazendo uma doação via PIX ou PayPal."
    )
    await bot.reply_to(message, text, parse_mode='Markdown')

from bot import bot
