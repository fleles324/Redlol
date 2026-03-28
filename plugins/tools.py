import asyncio
import re
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/ping$',
        r'^/echo\s+(.*)',
        r'^/post\s+(.*)'
    ]
}

async def ping(message):
    """Responde 'Pong!' para verificar a conexão do bot"""
    import time
    start = time.time()
    msg = await bot.reply_to(message, "🏓 Pong!")
    end = time.time()
    
    # Calcula latência
    latency = round((end - start) * 1000)
    await bot.edit_message_text(f"🏓 **Pong!**\n⏱ **Latência:** `{latency}ms`", message.chat.id, msg.message_id, parse_mode='Markdown')

async def echo(message):
    """Repete a mensagem enviada pelo usuário"""
    match = re.search(r'^/echo\s+(.*)', message.text, re.DOTALL)
    if match:
        await bot.reply_to(message, match.group(1))

async def post(message):
    """Envia uma mensagem formatada como post (apenas Admin)"""
    match = re.search(r'^/post\s+(.*)', message.text, re.DOTALL)
    if match:
        # Verifica se é admin
        try:
            admins = await bot.get_chat_administrators(message.chat.id)
            admin_ids = [admin.user.id for admin in admins]
            if message.from_user.id not in admin_ids and message.from_user.id not in config.SUPERADMINS:
                return
        except:
            pass
            
        text = match.group(1)
        # Deleta a mensagem do comando para o post parecer nativo
        try:
            await bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
            
        await bot.send_message(message.chat.id, text, parse_mode='Markdown')

from bot import bot
