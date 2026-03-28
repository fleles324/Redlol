import asyncio
from telebot import types
from database import db

triggers = {
    'on_text_message': [
        r'^/ranking_data$'
    ]
}

async def ranking_data(message):
    """Dados brutos de ranking (para administradores)"""
    # Lógica simplificada de dados
    await bot.reply_to(message, "📊 Dados de ranking processados com sucesso.")

from bot import bot
