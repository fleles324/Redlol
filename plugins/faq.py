import asyncio
import re
from telebot import types
from database import db
import config

# Configurações do plugin
triggers = {
    'on_text_message': []
}

async def on_every_message(message):
    """Monitora mensagens e responde apenas no tópico de FAQ oficial"""
    if not message.text or message.from_user.is_bot:
        return True

    # RESTRIÇÃO: O bot só responde FAQ se estiver no tópico oficial definido no .env
    is_faq_thread = (message.chat.id == config.SUPPORT_GROUP_ID and 
                     message.message_thread_id == config.FAQ_THREAD_ID)
    
    if not is_faq_thread:
        return True # Ignora se não for o tópico de FAQ

    text = message.text.lower().strip()
    
    # Busca no FAQ (database.py implementa a lógica de score)
    faq_match = db.search_faq(text)
    
    if faq_match:
        # Se for no tópico de FAQ, responde sempre
        # Se for em outro lugar, só responde se o score for muito alto (tratado no search_faq)
        answer = faq_match.get('answer', '')
        if answer:
            # Escapa caracteres especiais de Markdown que podem causar erro 400
            # Principalmente se houver símbolos como _ ou * sozinhos
            safe_answer = answer.replace("_", "\\_").replace("*", "\\*")
            
            # Envia a resposta da FAQ
            await bot.reply_to(message, f"📖 **FAQ - {faq_match.get('category', 'Dúvida')}**\n\n{safe_answer}", parse_mode='Markdown')
            
            # Se não for o tópico oficial, podemos encerrar o processamento aqui se quisermos
            if is_faq_thread:
                return False # Interceptado, não deixa outros plugins processarem

    return True

# Exporta o bot para uso nos handlers
from bot import bot
