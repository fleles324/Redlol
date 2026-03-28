import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/ban$',
        r'^/kick$',
        r'^/unban$'
    ]
}

async def ban(message):
    """Bane um usuário do grupo"""
    if not message.reply_to_message:
        return await bot.reply_to(message, "Responda à mensagem de quem deseja banir.")
    
    user_id = message.reply_to_message.from_user.id
    try:
        await bot.ban_chat_member(message.chat.id, user_id)
        await bot.reply_to(message, f"🚫 Usuário {user_id} banido.")
    except Exception as e:
        await bot.reply_to(message, f"Erro ao banir: {e}")

async def kick(message):
    """Kick um usuário do grupo"""
    if not message.reply_to_message:
        return await bot.reply_to(message, "Responda à mensagem de quem deseja remover.")
    
    user_id = message.reply_to_message.from_user.id
    try:
        await bot.unban_chat_member(message.chat.id, user_id)
        await bot.reply_to(message, f"👞 Usuário {user_id} removido.")
    except Exception as e:
        await bot.reply_to(message, f"Erro ao kickar: {e}")

async def unban(message):
    """Desbane um usuário do grupo"""
    if not message.reply_to_message and not message.text.split()[-1].isdigit():
        return await bot.reply_to(message, "Responda à mensagem ou informe o ID.")
    
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else int(message.text.split()[-1])
    try:
        await bot.unban_chat_member(message.chat.id, user_id, only_if_banned=True)
        await bot.reply_to(message, f"✅ Usuário {user_id} desbanido.")
    except Exception as e:
        await bot.reply_to(message, f"Erro ao desbanir: {e}")

from bot import bot
