import asyncio
from telebot import types
from database import db

triggers = {
    'on_text_message': [
        r'^/ranking$',
        r'^/rank$'
    ]
}

async def ranking(message):
    """Mostra o ranking dos usuários com mais mensagens no grupo"""
    users = db.get_user_ranking(limit=10)
    
    if not users:
        return await bot.reply_to(message, "Ainda não há dados de ranking para este grupo.")
    
    text = "🏆 **Ranking de Mensagens:**\n\n"
    for i, user in enumerate(users, 1):
        name = user.get('first_name', 'Usuário')
        username = user.get('username', '')
        count = user.get('msg_count', 0)
        
        mention = f"@{username}" if username else name
        text += f"{i}. {mention} — **{count}** msgs\n"
    
    await bot.reply_to(message, text, parse_mode='Markdown')

from bot import bot
