import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/start$'
    ]
}

async def start(message):
    """Comando /start com visual profissional e menu de acesso rápido"""
    bot_info = await bot.get_me()
    
    # Se for no privado, mostra o menu de boas-vindas completo
    if message.chat.type == 'private':
        text = (
            f"👋 **Olá {message.from_user.first_name}!**\n\n"
            f"Eu sou o **{config.BOT_NAME}**, seu assistente de segurança e gestão inteligente. "
            "Estou aqui para proteger seus grupos e facilitar o atendimento da sua comunidade.\n\n"
            "🚀 **Como posso te ajudar agora?**"
        )
        
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton("🖥️ MENU PRINCIPAL", callback_data="###cb:menu:main"),
            types.InlineKeyboardButton("🎧 SUPORTE", callback_data="###cb:menu:support")
        )
        keyboard.add(
            types.InlineKeyboardButton("🌍 IDIOMA", callback_data="setlang:menu"),
            types.InlineKeyboardButton("📊 MEU PERFIL", callback_data="###cb:menu:stats")
        )
        keyboard.add(
            types.InlineKeyboardButton("🌐 NOSSO CANAL", url=config.CHANNEL)
        )
        
        await bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')
    
    # Se for em grupo, mostra apenas uma saudação simples para não poluir
    else:
        text = (
            f"🤖 **{config.BOT_NAME} Ativo!**\n\n"
            f"Olá {message.from_user.first_name}, estou operando neste grupo.\n"
            "Para ver meus comandos, use `/menu` no meu privado."
        )
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Ir para o Privado", url=f"https://t.me/{bot_info.username}?start=menu"))
        await bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

from bot import bot
