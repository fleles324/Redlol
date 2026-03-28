import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^@admin$',
        r'^/report$'
    ]
}

async def report(message):
    """Encaminha uma denúncia para os administradores"""
    if not message.reply_to_message:
        return await bot.reply_to(message, "Responda à mensagem que deseja denunciar usando @admin ou /report.")
    
    # Detalhes da denúncia
    reported_user = message.reply_to_message.from_user
    reporter = message.from_user
    chat_title = message.chat.title or "Chat Privado"
    
    # Notificação para administradores (enviada para o log de admin configurado)
    report_text = (
        "🚨 **Nova Denúncia!**\n\n"
        f"📍 **Chat:** `{chat_title}` (`{message.chat.id}`)\n"
        f"👤 **Denunciado:** {reported_user.first_name} (`{reported_user.id}`)\n"
        f"👮 **Denunciante:** {reporter.first_name} (`{reporter.id}`)\n\n"
        f"🔗 [Link da Mensagem](https://t.me/c/{str(message.chat.id)[4:]}/{message.reply_to_message.message_id})"
    )
    
    try:
        # Envia para o log de admin ou chat de logs
        await bot.send_message(config.LOG_ADMIN, report_text, parse_mode='Markdown')
        await bot.reply_to(message, "✅ Denúncia enviada para os administradores!")
    except Exception as e:
        print(f"Erro ao enviar denúncia: {e}")
        await bot.reply_to(message, "❌ Erro ao processar a denúncia.")

from bot import bot
