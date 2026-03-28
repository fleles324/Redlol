import asyncio
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^#(\w+)$',
        r'^/extra\s+(\w+)\s*\|\s*(.*)',
        r'^/delextra\s+(\w+)'
    ]
}

async def on_every_message(message):
    """Monitora gatilhos de extras (#extra)"""
    if not message.text or message.from_user.is_bot:
        return True

    text = message.text.lower().strip()
    
    # 1. Se for um gatilho de extra (#extra)
    if text.startswith('#'):
        key = text[1:]
        extra = db.get_quick_reply(key) # Reutilizando a lógica de quick_reply para extras
        if extra:
            await bot.reply_to(message, extra, parse_mode='Markdown')
            return False # Interceptado

    return True

async def extra(message):
    """Cria um extra (#chave | mensagem)"""
    import re
    match = re.search(r'^/extra\s+(\w+)\s*\|\s*(.*)', message.text)
    if not match:
        return await bot.reply_to(message, "❌ Formato inválido! Use: `/extra chave | mensagem`", parse_mode='Markdown')
    
    key = match.group(1)
    text = match.group(2)
    
    db.set_quick_reply(key, text)
    await bot.reply_to(message, f"✅ Extra `#{key}` salvo com sucesso!", parse_mode='Markdown')

async def delextra(message):
    """Deleta um extra (#chave)"""
    import re
    match = re.search(r'^/delextra\s+(\w+)', message.text)
    if not match:
        return await bot.reply_to(message, "❌ Formato inválido! Use: `/delextra chave`", parse_mode='Markdown')
    
    key = match.group(1)
    # Lógica de remoção do banco
    db.supabase.table("chat_extras").delete().eq("chat_id", 0).eq("command", f"qr:{key}").execute()
    await bot.reply_to(message, f"🗑 Extra `#{key}` removido com sucesso!")

from bot import bot
