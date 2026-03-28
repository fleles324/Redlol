import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/moderators$',
        r'^/mods$',
        r'^/addmod$',
        r'^/delmod$'
    ]
}

async def moderators(message):
    """Lista todos os moderadores e administradores do chat atual"""
    try:
        admins = await bot.get_chat_administrators(message.chat.id)
        text = f"👔 **Moderadores de {message.chat.title}:**\n\n"
        for admin in admins:
            status = "👑 Criador" if admin.status == 'creator' else "👔 Admin"
            name = admin.user.first_name
            text += f"- {name} (`{admin.user.id}`) — **{status}**\n"
        
        await bot.reply_to(message, text, parse_mode='Markdown')
    except Exception as e:
        await bot.reply_to(message, f"❌ Erro ao obter moderadores: {e}")

async def addmod(message):
    """Comando /addmod para promover um moderador (Super Admin)"""
    if message.from_user.id not in config.SUPERADMINS:
        return
    
    if not message.reply_to_message:
        return await bot.reply_to(message, "Responda à mensagem de quem deseja promover.")
    
    user_id = message.reply_to_message.from_user.id
    try:
        await bot.promote_chat_member(message.chat.id, user_id, can_change_info=False, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=False)
        await bot.reply_to(message, f"✅ Moderador adicionado: `{user_id}`")
    except Exception as e:
        await bot.reply_to(message, f"Erro ao promover: {e}")

from bot import bot
