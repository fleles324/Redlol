import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/donate$',
        r'^/doar$',
        r'^/donations$',
        r'^/doacoes$'
    ]
}

async def donations(message):
    """Mostra informações de doação para o bot"""
    text = (
        f"💖 **Apoie o {config.BOT_NAME}!**\n\n"
        "Se você gosta do meu trabalho e quer ajudar a manter os servidores online "
        "e as novas funcionalidades chegando, considere fazer uma doação.\n\n"
        "💳 **Métodos de Doação:**\n"
        "- **PIX:** `suporte@redlol.com.br`\n"
        "- **PayPal:** [doar via PayPal](https://paypal.me/redlol)\n\n"
        "Cada doação ajuda muito! 🙏"
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("💳 Doar via PayPal", url="https://paypal.me/bot"))
    keyboard.add(types.InlineKeyboardButton("🎁 Ver Sorteios", callback_data="setlang:sorteio"))
    
    await bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

from bot import bot
