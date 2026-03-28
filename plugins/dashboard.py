import asyncio
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/dashboard$',
        r'^/painel$'
    ],
    'on_callback_query': [
        r'^###cb:dashboard:(.*)$'
    ]
}

async def dashboard(message):
    """Painel de controle com visual aprimorado"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Coleta dados do usuário
    res = db.supabase.table("users").select("*").eq("user_id", user_id).execute()
    user_data = res.data[0] if res.data else {}
    
    msg_count = user_data.get('msg_count', 0)
    lang_code = db.get_user_lang(user_id) or 'pt_BR'
    lang_name = config.AVAILABLE_LANGUAGES.get(lang_code, lang_code)
    
    text = (
        f"📊 **MEU PAINEL - {config.BOT_NAME.upper()}**\n\n"
        f"👤 **Perfil:** {first_name}\n"
        f"🆔 **ID:** `{user_id}`\n"
        f"🌐 **Idioma:** {lang_name}\n\n"
        f"📈 **ATIVIDADE NO BOT:**\n"
        f"💬 Mensagens Registradas: `{msg_count}`\n"
        f"🏅 Nível: `Membro Ativo`"
    )
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🌍 TROCAR IDIOMA", callback_data="setlang:menu"),
        types.InlineKeyboardButton("🎧 SUPORTE", callback_data="setlang:atendimento")
    )
    keyboard.add(
        types.InlineKeyboardButton("🖥️ MENU PRINCIPAL", callback_data="###cb:menu:main")
    )
    
    if hasattr(message, 'data'):
        await bot.edit_message_text(text, message.message.chat.id, message.message.message_id, reply_markup=keyboard, parse_mode='Markdown')
    else:
        await bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

from bot import bot
