import asyncio
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/flood$'
    ]
}

flood_tracker = {}

async def on_every_message(message):
    """Lógica específica de anti-flood (separada de protection)"""
    if not message.from_user or message.from_user.is_bot:
        return True

    chat_id = message.chat.id
    user_id = message.from_user.id
    
    key = f"{chat_id}:{user_id}"
    flood_tracker[key] = flood_tracker.get(key, 0) + 1
    
    # Reseta após 3 segundos
    async def reset(k):
        await asyncio.sleep(3)
        if k in flood_tracker: flood_tracker[k] = 0
    
    asyncio.create_task(reset(key))
    
    if flood_tracker[key] > 5:
        try:
            await bot.delete_message(chat_id, message.message_id)
            return False
        except:
            pass
    return True

async def flood(message):
    """Configurações de flood"""
    await bot.reply_to(message, "⚡️ **Configurações de Anti-Flood:**\n\nLimite atual: 5 msgs / 3s.")

from bot import bot
