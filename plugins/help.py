import asyncio
from telebot import types

triggers = {
    'on_text_message': [
        r'^/help$'
    ]
}

async def help(message):
    """Comando /help"""
    text = (
        "📖 **Lista de Comandos:**\n\n"
        "**/start** - Inicia o bot\n"
        "**/id** - Mostra seu ID e o ID do chat\n"
        "**/help** - Mostra esta mensagem\n"
        "**/atendimento** - Abre o suporte\n"
        "**/atendente** - Painel do atendente (no tópico)\n"
        "**/setm** - Salva resposta rápida\n"
        "**/close** - Encerra atendimento\n"
    )
    await bot.reply_to(message, text, parse_mode='Markdown')

from bot import bot
