import asyncio
import re
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/note\s+(\w+)\s*(.*)',
        r'^/save\s+(\w+)\s*(.*)',
        r'^/get\s+(\w+)',
        r'^#(\w+)$',
        r'^/notes$',
        r'^/delnote\s+(\w+)'
    ]
}

async def note(message):
    """Salva uma nota: /note nome_da_nota conteúdo"""
    match = re.search(r'^/(?:note|save)\s+(\w+)(?:\s+(.*))?', message.text, re.DOTALL)
    if not match:
        return await bot.reply_to(message, "❌ Use: `/note <nome> <texto>` ou responda a uma mensagem.", parse_mode='Markdown')
    
    note_name = match.group(1).lower()
    note_content = match.group(2)
    
    # Se não tem conteúdo, verifica se é um reply
    if not note_content or note_content.strip() == '':
        if message.reply_to_message and message.reply_to_message.text:
            note_content = message.reply_to_message.text
        else:
            return await bot.reply_to(message, "❌ Você precisa fornecer o conteúdo da nota ou responder a uma mensagem de texto.", parse_mode='Markdown')
    
    # Salvar a nota (usando a lógica de extra existente no db como base, ou criar nova tabela)
    # Por simplicidade, vamos usar o sistema de quick_reply/extra
    db.set_quick_reply(f"note_{message.chat.id}_{note_name}", note_content)
    
    await bot.reply_to(message, f"✅ Nota `{note_name}` salva com sucesso!\nPara ver, use `/get {note_name}` ou `#{note_name}`", parse_mode='Markdown')

async def get(message):
    """Pega uma nota: /get nome_da_nota"""
    match = re.search(r'^/get\s+(\w+)', message.text)
    if not match:
        return
        
    note_name = match.group(1).lower()
    await _send_note(message, note_name)

async def on_every_message(message):
    """Monitora gatilhos de notas (#nota)"""
    if not message.text or message.from_user.is_bot:
        return True
        
    text = message.text.strip()
    if text.startswith('#') and len(text) > 1:
        note_name = text[1:].split()[0].lower()
        content = db.get_quick_reply(f"note_{message.chat.id}_{note_name}")
        if content:
            await bot.reply_to(message, content, parse_mode='Markdown')
            return False # Interceptado
            
    return True

async def notes(message):
    """Lista todas as notas do chat"""
    # Como não temos acesso direto à tabela aqui de forma simples sem SQL direto, 
    # vamos avisar que está em desenvolvimento ou usar uma query direta
    try:
        res = db.supabase.table("chat_extras").select("command").eq("chat_id", 0).like("command", f"qr:note_{message.chat.id}_%").execute()
        
        if not res.data:
            return await bot.reply_to(message, "📝 Não há notas salvas neste chat.")
            
        text = "📝 **Notas salvas neste chat:**\n\n"
        for item in res.data:
            name = item['command'].replace(f"qr:note_{message.chat.id}_", "")
            text += f"- `#{name}`\n"
            
        await bot.reply_to(message, text, parse_mode='Markdown')
    except Exception as e:
        await bot.reply_to(message, "📝 Sistema de listagem de notas em manutenção.")

async def delnote(message):
    """Deleta uma nota"""
    match = re.search(r'^/delnote\s+(\w+)', message.text)
    if not match:
        return await bot.reply_to(message, "❌ Use: `/delnote <nome>`", parse_mode='Markdown')
        
    note_name = match.group(1).lower()
    
    try:
        db.supabase.table("chat_extras").delete().eq("chat_id", 0).eq("command", f"qr:note_{message.chat.id}_{note_name}").execute()
        await bot.reply_to(message, f"🗑 Nota `{note_name}` apagada com sucesso!", parse_mode='Markdown')
    except:
        await bot.reply_to(message, "❌ Erro ao apagar a nota.")

async def _send_note(message, note_name):
    content = db.get_quick_reply(f"note_{message.chat.id}_{note_name}")
    if content:
        await bot.reply_to(message, content, parse_mode='Markdown')
    else:
        await bot.reply_to(message, f"❌ Nota `{note_name}` não encontrada.")

async def save(message):
    """Alias para note"""
    await note(message)

async def _hash_note(message):
    """Handle para o gatilho #nota"""
    # Já é tratado no on_every_message, mas registramos aqui para evitar avisos
    pass

from bot import bot
