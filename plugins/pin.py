import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/pin$',
        r'^/unpin$',
        r'^/pin_silent$'
    ]
}

async def pin(message):
    """Fixa uma mensagem no chat"""
    if not message.reply_to_message:
        return await bot.reply_to(message, "Responda à mensagem que deseja fixar.")
    
    # Verifica permissões
    try:
        await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id, disable_notification=False)
        await bot.reply_to(message, "📌 **Mensagem fixada com sucesso!**", parse_mode='Markdown')
    except Exception as e:
        await bot.reply_to(message, f"Erro ao fixar mensagem: {e}")

async def unpin(message):
    """Desafixa uma mensagem no chat"""
    try:
        await bot.unpin_chat_message(message.chat.id)
        await bot.reply_to(message, "📌 **Mensagem desafixada.**", parse_mode='Markdown')
    except Exception as e:
        await bot.reply_to(message, f"Erro ao desafixar mensagem: {e}")

async def pin_silent(message):
    """Fixa uma mensagem silenciosamente"""
    if not message.reply_to_message:
        return
    
    try:
        await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id, disable_notification=True)
        await bot.reply_to(message, "📌 **Mensagem fixada silenciosamente.**", parse_mode='Markdown')
    except Exception as e:
        await bot.reply_to(message, f"Erro ao fixar mensagem: {e}")

from bot import bot
