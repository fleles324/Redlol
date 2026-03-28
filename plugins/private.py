import asyncio
from telebot import types
import config
from database import db

triggers = {
    'on_text_message': [
        r'^/private$',
        r'^/settings_private$'
    ],
    'on_callback_query': [
        r'^###cb:private:(.*)$'
    ]
}

async def on_every_message(message):
    """Lógica para mensagens privadas (Boas-vindas e etc)"""
    if message.chat.type == 'private' and not message.text.startswith('/'):
        # Se o usuário mandar qualquer coisa no privado pela primeira vez
        user_id = message.from_user.id
        if not db.get_user_lang(user_id):
            # Se não tem idioma, manda boas-vindas e pede idioma
            text = (
                f"👋 Olá **{message.from_user.first_name}**! Bem-vindo ao **{config.BOT_NAME}**.\n\n"
                "Eu sou um bot multifuncional de segurança e suporte.\n"
                "Para começar, escolha o seu idioma padrão abaixo:"
            )
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            buttons = [
                types.InlineKeyboardButton(v, callback_data=f"setlang:{k}")
                for k, v in config.AVAILABLE_LANGUAGES.items()
            ]
            keyboard.add(*buttons)
            await bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='Markdown')
            return False # Interceptado

    return True

async def settings_private(message):
    """Menu de configurações privadas"""
    text = (
        "⚙️ **Configurações Privadas:**\n\n"
        "Aqui você pode gerenciar suas preferências no bot."
    )
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🌍 Alterar Idioma", callback_data="setlang:menu"))
    await bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

async def private(message):
    """Alias para iniciar conversa no privado"""
    await on_every_message(message)

async def on_callback_query(call):
    """Handler genérico para callbacks no privado se necessário"""
    pass

from bot import bot
