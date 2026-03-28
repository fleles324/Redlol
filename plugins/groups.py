import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/groups$',
        r'^/grupos$',
        r'^/canais$',
        r'^/channel$'
    ]
}

async def groups(message):
    """Mostra os grupos de suporte e canais oficiais do bot"""
    text = (
        f"👥 **Grupos de Suporte e Canais:**\n\n"
        f"📢 **Canal Oficial:** {config.CHANNEL}\n"
        f"🎧 **Suporte Oficial:** {config.HELP_GROUPS_LINK}\n\n"
        "Siga nosso canal para atualizações constantes sobre o bot!"
    )
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📢 Canal Oficial", url=config.CHANNEL))
    keyboard.add(types.InlineKeyboardButton("🎧 Suporte", url=config.HELP_GROUPS_LINK))
    
    await bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

from bot import bot
