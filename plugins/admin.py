import asyncio
from telebot import types
import config
from database import db

triggers = {
    'on_text_message': [
        r'^/promote$',
        r'^/demote$',
        r'^/setadmin$',
        r'^/deladmin$',
        r'^/stats$',
        r'^/broadcast\s+(.*)'
    ]
}

async def promote(message):
    """Promove um usuário a moderador no grupo"""
    if message.from_user.id not in config.SUPERADMINS:
        return await bot.reply_to(message, "❌ Comando exclusivo para Super Admins.")
    
    if not message.reply_to_message:
        return await bot.reply_to(message, "Responda à mensagem de quem deseja promover.")
    
    user_id = message.reply_to_message.from_user.id
    try:
        await bot.promote_chat_member(message.chat.id, user_id, can_change_info=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=False)
        await bot.reply_to(message, f"✅ Usuário {user_id} promovido a moderador!")
    except Exception as e:
        await bot.reply_to(message, f"Erro ao promover: {e}")

async def demote(message):
    """Remove um moderador no grupo"""
    if message.from_user.id not in config.SUPERADMINS:
        return
    
    if not message.reply_to_message:
        return await bot.reply_to(message, "Responda à mensagem.")
    
    user_id = message.reply_to_message.from_user.id
    try:
        await bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        await bot.reply_to(message, f"✅ Usuário {user_id} removido da moderação.")
    except Exception as e:
        await bot.reply_to(message, f"Erro: {e}")

async def setadmin(message):
    """Adiciona um Super Admin (apenas via código/banco por segurança)"""
    await bot.reply_to(message, "👮 Para adicionar um Super Admin, edite o arquivo config.py.")

async def deladmin(message):
    """Remove um Super Admin"""
    await bot.reply_to(message, "👮 Para remover um Super Admin, edite o arquivo config.py.")

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

async def broadcast(message):
    """Envia uma mensagem para todos os usuários do bot (apenas Super Admin)"""
    if message.from_user.id not in config.SUPERADMINS:
        return

    import re
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
