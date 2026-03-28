import asyncio
import os
import json
from telebot import types
import config
from database import db

triggers = {
    'on_text_message': [
        r'^/backup$',
        r'^/export$'
    ]
}

async def backup(message):
    """Gera um backup JSON dos dados do bot (apenas Super Admin)"""
    if message.from_user.id not in config.SUPERADMINS:
        return
    
    await bot.reply_to(message, "📦 Gerando backup do banco de dados... Aguarde.")
    
    try:
        # Busca dados de todas as tabelas principais
        users = db.supabase.table("users").select("*").execute().data
        settings = db.supabase.table("chat_settings").select("*").execute().data
        stats = db.supabase.table("bot_stats").select("*").execute().data
        faqs = db.supabase.table("faqs").select("*").execute().data
        extras = db.supabase.table("chat_extras").select("*").execute().data
        
        backup_data = {
            "users": users,
            "chat_settings": settings,
            "bot_stats": stats,
            "faqs": faqs,
            "chat_extras": extras,
            "version": config.VERSION,
            "timestamp": "now"
        }
        
        # Salva em um arquivo temporário
        file_path = "backup_bot.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=4, ensure_ascii=False)
        
        # Envia o arquivo para o administrador
        with open(file_path, "rb") as f:
            await bot.send_document(message.chat.id, f, caption="✅ **Backup gerado com sucesso!**", parse_mode='Markdown')
        
        # Remove o arquivo temporário
        os.remove(file_path)
    except Exception as e:
        await bot.reply_to(message, f"❌ Erro ao gerar backup: {e}")

from bot import bot
