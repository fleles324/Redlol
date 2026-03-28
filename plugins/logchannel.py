import asyncio
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/setlog$',
        r'^/dellog$'
    ]
}

async def on_every_message(message):
    """Monitora eventos e envia logs para o canal configurado"""
    # Exemplo: Logar novas mensagens de Super Admin
    if message.from_user and message.from_user.id in config.SUPERADMINS:
        log_text = (
            f"📝 **Log de Super Admin:**\n\n"
            f"👤 **Admin:** {message.from_user.first_name} (`{message.from_user.id}`)\n"
            f"💬 **Mensagem:** `{message.text or message.caption}`\n"
            f"📍 **Chat:** `{message.chat.title or 'Privado'}` (`{message.chat.id}`)"
        )
        try:
            # Envia para o LOG_CHAT configurado no config.py (SUPPORT_GROUP_ID)
            await bot.send_message(config.LOG_CHAT, log_text, parse_mode='Markdown')
        except:
            pass
    return True

async def setlog(message):
    """Define o chat atual como canal de logs (apenas Super Admin)"""
    if message.from_user.id not in config.SUPERADMINS:
        return
    
    chat_id = message.chat.id
    db.update_chat_setting(chat_id, 'log_channel', True)
    await bot.reply_to(message, f"✅ Canal de logs configurado para `{chat_id}`.")

async def dellog(message):
    """Remove a configuração de log do chat atual"""
    if message.from_user.id not in config.SUPERADMINS:
        return
    db.update_chat_setting(message.chat.id, 'log_channel', False)
    await bot.reply_to(message, "🗑 Canal de logs desativado para este chat.")

from bot import bot
