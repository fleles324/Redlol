import asyncio
import re
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/search\s+(.*)',
        r'^/pesquisa\s+(.*)'
    ]
}

async def search(message):
    """Busca manual no FAQ"""
    match = re.search(r'^/(?:search|pesquisa)\s+(.*)', message.text)
    if not match:
        return await bot.reply_to(message, "❌ Use: `/search pergunta` ou `/pesquisa pergunta`")
    
    query = match.group(1).lower().strip()
    faq_match = db.search_faq(query)
    
    if faq_match:
        answer = faq_match.get('answer', '')
        category = faq_match.get('category', 'Dúvida')
        await bot.reply_to(message, f"📖 **FAQ - {category}**\n\n{answer}", parse_mode='Markdown')
    else:
        await bot.reply_to(message, "❌ Não encontrei uma resposta para sua dúvida. Tente outras palavras ou fale com o suporte.")

from bot import bot
