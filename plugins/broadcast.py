import asyncio
import re
from telebot import types
import config
from database import db

triggers = {
    'on_text_message': [
        r'^/broadcast\s+(.*)'
    ]
}

async def broadcast(message):
    """Envia uma mensagem para todos os usuários do bot (apenas Super Admin)"""
    if message.from_user.id not in config.SUPERADMINS:
        return

    match = re.search(r'^/broadcast\s+(.*)', message.text, re.DOTALL)
    if not match:
        return await bot.reply_to(message, "❌ Use: `/broadcast mensagem`")
    
    text = match.group(1)
    users = db.supabase.table("users").select("user_id").execute()
    
    sent = 0
    for user in users.data:
        try:
            await bot.send_message(user['user_id'], text, parse_mode='Markdown')
            sent += 1
            await asyncio.sleep(0.1) # Evita flood
        except:
            pass
            
    await bot.reply_to(message, f"✅ Mensagem enviada para {sent} usuários.")

from bot import bot
