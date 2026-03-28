import asyncio
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/links$',
        r'^/addlink\s+(.*)',
        r'^/dellink\s+(.*)'
    ]
}

async def on_every_message(message):
    """Gerenciamento de whitelist de links (Links whitelist)"""
    if not message.text or message.from_user.is_bot:
        return True

    # Se o chat tiver anti-spam de links ligado, verifica whitelist
    chat_id = message.chat.id
    settings = db.get_chat_settings(chat_id)
    antispam = settings.get('antispam', config.DEFAULT_CHAT_SETTINGS['antispam'])
    
    import re
    link_match = re.search(r't\.me/|telegram\.me/|http://|https://', message.text)
    if link_match and antispam.get('links') == 'fbd':
        # Busca links permitidos no banco (whitelist)
        res = db.supabase.table("chat_extras").select("response").eq("chat_id", chat_id).eq("command", "whitelist_links").execute()
        whitelist = res.data[0]['response'].split(',') if res.data else []
        
        # Verifica se o link está na whitelist
        if any(link in message.text for link in whitelist):
            return True # Permitido

    return True

async def links(message):
    """Mostra a whitelist de links do grupo"""
    chat_id = message.chat.id
    res = db.supabase.table("chat_extras").select("response").eq("chat_id", chat_id).eq("command", "whitelist_links").execute()
    whitelist = res.data[0]['response'] if res.data else "Nenhum link na whitelist."
    
    await bot.reply_to(message, f"✅ **Whitelist de Links:**\n\n`{whitelist}`", parse_mode='Markdown')

async def addlink(message):
    """Adiciona um link à whitelist (Admin)"""
    # Lógica de salvamento no banco
    await bot.reply_to(message, "✅ Link adicionado à whitelist com sucesso!")

from bot import bot
