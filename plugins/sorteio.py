import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/sorteio$',
        r'^/giveaway$',
        r'^/start_sorteio\s+(.*)'
    ]
}

async def sorteio(message):
    """Comando /sorteio (Informa sobre sorteios ativos)"""
    text = (
        "🎁 **Sistema de Sorteios:**\n\n"
        "Atualmente não há sorteios ativos no grupo.\n"
        "Para iniciar um sorteio (Admin), use: `/start_sorteio prêmio`"
    )
    await bot.reply_to(message, text, parse_mode='Markdown')

async def start_sorteio(message):
    """Inicia um sorteio no grupo (apenas Admin)"""
    # Lógica de sorteio (exemplo simplificado)
    if message.from_user.id not in config.SUPERADMINS:
        return
    
    import re
    match = re.search(r'^/start_sorteio\s+(.*)', message.text)
    if match:
        prize = match.group(1)
        text = (
            f"🎁 **NOVO SORTEIO INICIADO!**\n\n"
            f"🏆 **Prêmio:** {prize}\n"
            f"👮 **Sorteador:** {message.from_user.first_name}\n\n"
            "Clique no botão abaixo para participar!"
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("🎟 Participar", callback_data="###cb:sorteio:join"))
        
        await bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='Markdown')

from bot import bot
