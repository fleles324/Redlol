import asyncio
from telebot import types
from database import db
import config

# Configurações do plugin
triggers = {}

async def on_every_message(message):
    """Monitora todas as mensagens para estatísticas e processamento geral"""
    if not message.from_user or message.from_user.is_bot:
        return True

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # 1. Atualiza dados do usuário no banco
    db.update_user(user_id, username, first_name)
    
    # 2. Incrementa contador de mensagens do usuário
    db.increment_user_msgs(user_id)
    
    # 3. Coleta estatísticas globais
    db.increment_stat("total_messages")
    
    # 4. Logs simples no terminal (Opcional)
    print(f"[LOG] {message.from_user.first_name} [{user_id}] -> {message.chat.id}")

    return True # Deixa o processamento continuar para outros plugins

from bot import bot
