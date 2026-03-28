import asyncio
from telebot import types
from database import db
import config

# Simulação simples de controle de flood por usuário (poderia ser no Redis/BD)
flood_counter = {}

# Configurações do plugin
triggers = {}

async def on_every_message(message):
    """Monitora spam e flood em tempo real"""
    if not message.from_user or message.from_user.is_bot:
        return True

    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text or message.caption or ""
    
    # --- 1. Sistema Anti-Spam (Links e Forwards) ---
    settings = db.get_chat_settings(chat_id)
    antispam = settings.get('antispam', config.DEFAULT_CHAT_SETTINGS['antispam'])
    
    # Se for link
    import re
    if antispam.get('links') == 'fbd' and re.search(r't\.me/|telegram\.me/|http://|https://', text):
        try:
            await bot.delete_message(chat_id, message.message_id)
            await bot.send_message(chat_id, f"🚫 **{message.from_user.first_name}**, links não são permitidos neste chat!", parse_mode='Markdown')
            return False # Interceptado
        except:
            pass
            
    # Se for forward de canal
    if antispam.get('forwards') == 'fbd' and message.forward_from_chat and message.forward_from_chat.type == 'channel':
        try:
            await bot.delete_message(chat_id, message.message_id)
            await bot.send_message(chat_id, f"🚫 **{message.from_user.first_name}**, mensagens encaminhadas de canais não são permitidas!", parse_mode='Markdown')
            return False # Interceptado
        except:
            pass

    # --- 2. Sistema Anti-Flood ---
    flood_settings = settings.get('flood', config.DEFAULT_CHAT_SETTINGS['flood'])
    max_flood = flood_settings.get('MaxFlood', 5)
    
    # Lógica simples de flood
    user_key = f"{chat_id}:{user_id}"
    flood_counter[user_key] = flood_counter.get(user_key, 0) + 1
    
    # Reseta o contador a cada 5 segundos
    async def reset_flood(key):
        await asyncio.sleep(5)
        if key in flood_counter:
            flood_counter[key] = 0
            
    asyncio.create_task(reset_flood(user_key))
    
    if flood_counter[user_key] > max_flood:
        try:
            # Punição (ex: ban ou kick)
            action = flood_settings.get('ActionFlood', 'kick')
            if action == 'kick':
                await bot.unban_chat_member(chat_id, user_id)
            elif action == 'ban':
                await bot.ban_chat_member(chat_id, user_id)
                
            await bot.send_message(chat_id, f"👞 **{message.from_user.first_name}** foi removido por praticar flood ({flood_counter[user_key]}/{max_flood} msgs/5s).", parse_mode='Markdown')
            return False # Interceptado
        except:
            pass

    return True

from bot import bot
