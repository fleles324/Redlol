import asyncio
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/configure$',
        r'^/settings$',
        r'^/config$'
    ],
    'on_callback_query': [
        r'^###cb:config:(.*)$'
    ]
}

async def configure(message):
    """Abre o menu de configurações do chat (apenas Admin)"""
    if message.chat.type == 'private':
        return await bot.reply_to(message, "Este comando deve ser usado em um grupo.")
    
    # Verifica se é admin
    try:
        admins = await bot.get_chat_administrators(message.chat.id)
        admin_ids = [admin.user.id for admin in admins]
        if message.from_user.id not in admin_ids and message.from_user.id not in config.SUPERADMINS:
            return await bot.reply_to(message, "❌ Você não tem permissão para configurar este chat.")
    except:
        pass

    settings = db.get_chat_settings(message.chat.id)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # 1. Botões de Alternância (Exemplos)
    welcome_status = "✅ LIGADO" if settings.get('settings', {}).get('Welcome') == 'on' else "❌ DESLIGADO"
    keyboard.add(types.InlineKeyboardButton(f"Boas-vindas: {welcome_status}", callback_data=f"###cb:config:welcome:{message.chat.id}"))
    
    rules_status = "✅ LIGADO" if settings.get('settings', {}).get('Rules') == 'on' else "❌ DESLIGADO"
    keyboard.add(types.InlineKeyboardButton(f"Regras: {rules_status}", callback_data=f"###cb:config:rules:{message.chat.id}"))
    
    antispam_status = "✅ LIGADO" if settings.get('antispam', {}).get('links') == 'fbd' else "❌ DESLIGADO"
    keyboard.add(types.InlineKeyboardButton(f"Anti-Spam: {antispam_status}", callback_data=f"###cb:config:antispam:{message.chat.id}"))
    
    keyboard.add(types.InlineKeyboardButton("🌍 Idioma do Chat", callback_data=f"###cb:config:lang:{message.chat.id}"))
    
    text = (
        f"🛠 **Configurações de {message.chat.title}**\n\n"
        "Use os botões abaixo para gerenciar as funcionalidades do bot neste grupo."
    )
    
    # Envia no privado por segurança ou no grupo conforme preferência (aqui vamos mandar no grupo/privado conforme config original)
    try:
        await bot.send_message(message.from_user.id, text, reply_markup=keyboard, parse_mode='Markdown')
        await bot.reply_to(message, "📩 **Enviei as configurações no seu privado!**", parse_mode='Markdown')
    except:
        await bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

from bot import bot
