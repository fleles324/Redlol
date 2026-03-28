import asyncio
from telebot import types

triggers = {
    'on_text_message': [
        r'^/atendimento$'
    ]
}

async def atendimento(message):
    """Comando /atendimento direto"""
    from plugins.support import start_support_flow
    await start_support_flow(message)

from bot import bot
