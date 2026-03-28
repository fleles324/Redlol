import asyncio
from telebot import types

triggers = {
    'on_text_message': [
        r'^/rules$',
        r'^/setrules\s+(.*)'
    ]
}

async def rules(message):
    """Mostra as regras do grupo"""
    # Lógica de regras (Poderia ser no banco)
    text = (
        "📜 **Regras do Grupo:**\n\n"
        "1. **Respeito**: Trate todos com educação.\n"
        "2. **Spam**: Não envie links ou mensagens repetitivas.\n"
        "3. **Suporte**: Use o comando /atendimento no privado para suporte.\n\n"
        "Siga as regras para não ser banido!"
    )
    await bot.reply_to(message, text, parse_mode='Markdown')

async def setrules(message):
    """Define as regras do grupo"""
    # Lógica de salvamento no banco de dados (exemplo simplificado)
    await bot.reply_to(message, "✅ Regras atualizadas com sucesso!")

from bot import bot
