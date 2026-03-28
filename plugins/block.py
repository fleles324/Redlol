import asyncio
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/block\s+(\d+)',
        r'^/unblock\s+(\d+)',
        r'^/blocked$'
    ]
}

async def on_every_message(message):
    """Verifica se o usuário está bloqueado de usar o bot"""
    if not message.from_user:
        return True

    user_id = message.from_user.id
    # Se o usuário for Super Admin, nunca bloqueia
    if user_id in config.SUPERADMINS:
        return True

    # Verifica no banco de dados se há um registro de bloqueio
    res = db.supabase.table("bot_stats").select("stat_value").eq("stat_name", f"blocked:{user_id}").execute()
    if res.data and res.data[0]['stat_value'] == 1:
        # Se for no privado, avisa o usuário (opcional)
        if message.chat.type == 'private':
            try:
                await bot.reply_to(message, "🚫 **Você foi bloqueado de usar este bot.**", parse_mode='Markdown')
            except:
                pass
        return False # Interceptado: o bot ignora o usuário

    return True

async def block(message):
    """Bloqueia um usuário de interagir com o bot (apenas Super Admin)"""
    if message.from_user.id not in config.SUPERADMINS:
        return

    import re
    match = re.search(r'^/block\s+(\d+)', message.text)
    if not match:
        return await bot.reply_to(message, "❌ Use: `/block ID`")
    
    user_id = int(match.group(1))
    db.supabase.table("bot_stats").upsert({"stat_name": f"blocked:{user_id}", "stat_value": 1}).execute()
    await bot.reply_to(message, f"🚫 Usuário `{user_id}` bloqueado com sucesso.", parse_mode='Markdown')

async def unblock(message):
    """Desbloqueia um usuário (apenas Super Admin)"""
    if message.from_user.id not in config.SUPERADMINS:
        return

    import re
    match = re.search(r'^/unblock\s+(\d+)', message.text)
    if not match:
        return await bot.reply_to(message, "❌ Use: `/unblock ID`")
    
    user_id = int(match.group(1))
    db.supabase.table("bot_stats").delete().eq("stat_name", f"blocked:{user_id}").execute()
    await bot.reply_to(message, f"✅ Usuário `{user_id}` desbloqueado.", parse_mode='Markdown')

from bot import bot
