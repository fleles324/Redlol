import asyncio
from telebot import types
from database import db

triggers = {
    'on_text_message': [
        r'^/warn$',
        r'^/unwarn$',
        r'^/warns$'
    ]
}

async def warn(message):
    """Adiciona uma advertência a um usuário"""
    if not message.reply_to_message:
        return await bot.reply_to(message, "Responda à mensagem de quem deseja advertir.")
    
    user_id = message.reply_to_message.from_user.id
    # Simulação de contagem de advertências (poderia ser no BD)
    stat_name = f"warns:{message.chat.id}:{user_id}"
    db.increment_stat(stat_name)
    
    # Busca o valor atualizado (simplificado aqui)
    res = db.supabase.table("bot_stats").select("stat_value").eq("stat_name", stat_name).execute()
    count = res.data[0]['stat_value'] if res.data else 1
    
    await bot.reply_to(message, f"⚠️ Usuário advertido ({count}/3).")
    
    if count >= 3:
        try:
            await bot.ban_chat_member(message.chat.id, user_id)
            await bot.send_message(message.chat.id, f"🚫 Usuário {user_id} banido por atingir o limite de advertências.")
            db.supabase.table("bot_stats").delete().eq("stat_name", stat_name).execute()
        except:
            pass

async def unwarn(message):
    """Remove uma advertência de um usuário"""
    if not message.reply_to_message:
        return await bot.reply_to(message, "Responda à mensagem.")
    
    user_id = message.reply_to_message.from_user.id
    stat_name = f"warns:{message.chat.id}:{user_id}"
    
    # Lógica de remoção
    res = db.supabase.table("bot_stats").select("stat_value").eq("stat_name", stat_name).execute()
    if res.data:
        new_val = max(0, (res.data[0]['stat_value'] or 1) - 1)
        db.supabase.table("bot_stats").update({"stat_value": new_val}).eq("stat_name", stat_name).execute()
        await bot.reply_to(message, f"✅ Advertência removida ({new_val}/3).")
    else:
        await bot.reply_to(message, "Usuário não possui advertências.")

async def warns(message):
    """Mostra as advertências de um usuário"""
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else message.from_user.id
    stat_name = f"warns:{message.chat.id}:{user_id}"
    
    res = db.supabase.table("bot_stats").select("stat_value").eq("stat_name", stat_name).execute()
    count = res.data[0]['stat_value'] if res.data else 0
    
    await bot.reply_to(message, f"📊 O usuário possui {count}/3 advertências.")

from bot import bot
