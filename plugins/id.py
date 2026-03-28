import asyncio
from telebot import types

triggers = {
    'on_text_message': [
        r'^/id$'
    ]
}

async def id(message):
    """Comando /id"""
    text = f"👤 **Seu ID:** `{message.from_user.id}`\n👥 **ID do Chat:** `{message.chat.id}`"
    if message.message_thread_id:
        text += f"\n📁 **ID do Tópico:** `{message.message_thread_id}`"
    await bot.reply_to(message, text, parse_mode='Markdown')

from bot import bot
