import asyncio
import aiohttp
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/maps\s+(.*)',
        r'^/googlemaps\s+(.*)',
        r'^/mapa\s+(.*)'
    ]
}

async def maps(message):
    """Integração básica com Google Maps (gera link de localização)"""
    import re
    match = re.search(r'^/maps\s+(.*)', message.text)
    if not match:
        return await bot.reply_to(message, "❌ Use: `/maps endereço ou lugar`")
    
    query = match.group(1).replace(" ", "+")
    google_maps_url = f"https://www.google.com/maps/search/{query}"
    
    text = (
        f"🗺 **Google Maps:**\n\n"
        f"📍 **Busca:** `{match.group(1)}`\n"
        f"🔗 [Ver no Mapa]({google_maps_url})"
    )
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📍 Ver no Google Maps", url=google_maps_url))
    
    await bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

# Aliases
async def googlemaps(message):
    await maps(message)

async def mapa(message):
    await maps(message)

from bot import bot
