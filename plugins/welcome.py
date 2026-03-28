import asyncio
from telebot import types
from database import db

triggers = {
    'on_text_message': [
        r'^/welcome$',
        r'^/goodbye$',
        r'^###new_chat_member$',
        r'^###left_chat_member$'
    ]
}

async def on_every_message(message):
    """Monitora entrada e saída de membros"""
    # 1. Entrada de novo membro
    if message.new_chat_members:
        for user in message.new_chat_members:
            if user.id == (await bot.get_me()).id:
                await bot.send_message(message.chat.id, f"👋 Olá! Eu sou o **{user.first_name}**, seu assistente de segurança e suporte.")
            else:
                # Simula boas-vindas
                await bot.send_message(message.chat.id, f"🎉 Bem-vindo(a), {user.first_name}!")
        return False # Interceptado

    # 2. Saída de membro
    elif message.left_chat_member:
        user = message.left_chat_member
        await bot.send_message(message.chat.id, f"👋 Até logo, {user.first_name}!")
        return False # Interceptado

    return True

async def welcome(message):
    """Ativa ou desativa a mensagem de boas-vindas"""
    # Lógica de configuração
    await bot.reply_to(message, "⚙️ Mensagem de boas-vindas configurada com sucesso!")

async def goodbye(message):
    """Ativa ou desativa a mensagem de despedida"""
    await bot.reply_to(message, "⚙️ Mensagem de despedida configurada com sucesso!")

from bot import bot
