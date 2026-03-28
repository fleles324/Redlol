import asyncio
from telebot import types
from database import db

triggers = {
    'on_text_message': [
        r'^/users$'
    ]
}

async def users(message):
    """Informações detalhadas de usuários"""
    user_id = message.from_user.id
    res = db.supabase.table("users").select("*").eq("user_id", user_id).execute()
    
    if res.data:
        data = res.data[0]
        text = (
            f"👤 **Dados de {data.get('first_name')}:**\n\n"
            f"🆔 ID: `{data.get('user_id')}`\n"
            f"💬 Msgs: `{data.get('msg_count')}`\n"
            f"🗓 Visto: `{data.get('last_seen')}`"
        )
        await bot.reply_to(message, text, parse_mode='Markdown')

from bot import bot
