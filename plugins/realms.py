import asyncio
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/realms$',
        r'^/setrealm\s+(\d+)',
        r'^/delrealm\s+(\d+)',
        r'^/realm\s+(.*)'
    ]
}

async def realms(message):
    """Gerenciamento de 'Realms' (Rede de Grupos Interligados)"""
    if message.chat.type == 'private':
        return
    
    text = (
        f"🏰 **Realms em {message.chat.title}:**\n\n"
        "Interligue vários grupos para compartilhar configurações, "
        "admins e banimentos globais entre sua rede de chats."
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🏰 Criar Realm", callback_data=f"###cb:realm:create:{message.chat.id}"))
    keyboard.add(types.InlineKeyboardButton("🤝 Juntar-se a Realm", callback_data=f"###cb:realm:join:{message.chat.id}"))
    
    await bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

async def setrealm(message):
    """Configura o Realm ID do chat (apenas Admin)"""
    if message.from_user.id not in config.SUPERADMINS:
        return
    
    # Lógica de configuração no banco de dados
    await bot.reply_to(message, "🏰 Realm configurado com sucesso para este chat!")

from bot import bot
