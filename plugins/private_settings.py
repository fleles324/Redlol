import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/private_settings$'
    ]
}

async def private_settings(message):
    """Configurações específicas para o modo privado"""
    if message.chat.type != 'private':
        return
    
    await bot.reply_to(message, "🔐 **Configurações Privadas:**\n\nGerencie suas notificações e preferências de tradução aqui.")

from bot import bot
