import asyncio
from telebot import types
import config
from database import db

triggers = {
    'on_text_message': [
        r'^/stats$'
    ]
}

async def stats(message):
    """Mostra estatísticas globais do bot (apenas Super Admin)"""
    if message.from_user.id not in config.SUPERADMINS:
        return
    
    res = db.supabase.table("bot_stats").select("*").execute()
    total_msgs = 0
    total_users = db.supabase.table("users").select("user_id", count="exact").execute().count
    
    for s in res.data:
        if s['stat_name'] == "total_messages":
            total_msgs = s['stat_value']
            
    text = (
        "📊 **Estatísticas Globais do Bot:**\n\n"
        f"👤 **Total de Usuários:** `{total_users}`\n"
        f"💬 **Total de Mensagens:** `{total_msgs}`\n"
        f"🤖 **Versão:** `{config.VERSION}`"
    )
    await bot.reply_to(message, text, parse_mode='Markdown')

from bot import bot
