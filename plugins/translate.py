import asyncio
import re
from telebot import types
from deep_translator import GoogleTranslator
import config

triggers = {
    'on_text_message': [
        r'^/translate\s+(\w+)\s*\|\s*(.*)',
        r'^/traduzir\s+(\w+)\s*\|\s*(.*)'
    ]
}

async def translate(message):
    """Comando de tradução direta: /translate lang | texto"""
    match = re.search(r'^/(?:translate|traduzir)\s+(\w+)\s*\|\s*(.*)', message.text, re.DOTALL)
    if not match:
        return await bot.reply_to(message, "❌ Use: `/translate idioma | texto` (Ex: `/translate en | Olá mundo`)", parse_mode='Markdown')
    
    target_lang = match.group(1).lower()
    text = match.group(2)
    
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        await bot.reply_to(message, f"🌐 **Tradução ({target_lang}):**\n\n{translated}", parse_mode='Markdown')
    except Exception as e:
        await bot.reply_to(message, f"❌ Erro na tradução: {e}")

async def traduzir(message):
    """Alias para translate"""
    await translate(message)

from bot import bot
