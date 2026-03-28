import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/formatacao$'
    ]
}

async def formatacao(message):
    """Alias para formatting.py"""
    text = (
        "✍️ **Guia de Formatação Rápida:**\n\n"
        "**Negrito**: `*texto*`\n"
        "_Itálico_: `_texto_`\n"
        "`Código`: `` `texto` ``"
    )
    await bot.reply_to(message, text, parse_mode='Markdown')

from bot import bot
