import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/grupos$'
    ]
}

async def grupos(message):
    """Alias para groups.py"""
    text = (
        f"👥 **Grupos Oficiais:**\n\n"
        f"📢 Canal: {config.CHANNEL}\n"
        f"🎧 Suporte: {config.HELP_GROUPS_LINK}"
    )
    await bot.reply_to(message, text, parse_mode='Markdown')

from bot import bot
