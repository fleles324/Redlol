import asyncio
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/antispam$'
    ]
}

async def on_every_message(message):
    """Lógica específica de anti-spam (separada de protection)"""
    if not message.from_user or message.from_user.is_bot:
        return True

    chat_id = message.chat.id
    text = message.text or message.caption or ""
    settings = db.get_chat_settings(chat_id)
    antispam = settings.get('antispam', config.DEFAULT_CHAT_SETTINGS['antispam'])
    
    # Verifica links
    import re
    if antispam.get('links') == 'fbd' and re.search(r't\.me/|telegram\.me/|http://|https://', text):
        try:
            await bot.delete_message(chat_id, message.message_id)
            return False
        except:
            pass
    return True

async def antispam(message):
    """Menu de configuração do anti-spam"""
    await bot.reply_to(message, "🚫 **Configurações de Anti-Spam:**\n\nUse o comando `/config` para gerenciar o bloqueio de links e forwards.")

from bot import bot
