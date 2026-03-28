import asyncio
import aiohttp
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/cat$',
        r'^/gato$'
    ]
}

async def cat(message):
    """Envia uma foto aleatória de um gato usando TheCatApi"""
    await bot.send_chat_action(message.chat.id, 'upload_photo')
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(config.THECATAPI_KEY) as response:
                if response.status == 200:
                    data = await response.json()
                    cat_url = data[0]['url']
                    await bot.send_photo(message.chat.id, cat_url, caption="🐱 Miaaau! Aqui está seu gato!")
                else:
                    await bot.reply_to(message, "❌ Erro ao buscar foto de gato. Tente novamente mais tarde.")
    except Exception as e:
        print(f"Erro no plugin cats: {e}")
        await bot.reply_to(message, "❌ Erro ao buscar foto de gato.")

# Alias para cat
async def gato(message):
    await cat(message)

from bot import bot
