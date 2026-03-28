import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/chatter$',
        r'^/ai$',
        r'^/ia$'
    ]
}

async def on_every_message(message):
    """Lógica de conversa inteligente (Chatter)"""
    if not message.text or message.from_user.is_bot:
        return True

    # IGNORA se for no grupo de suporte ou em tópicos administrativos
    if message.chat.id == config.SUPPORT_GROUP_ID:
        return True

    # Se o bot for mencionado ou responderem a ele
    bot_info = await bot.get_me()
    is_reply_to_bot = message.reply_to_message and message.reply_to_message.from_user.id == bot_info.id
    is_mention = f"@{bot_info.username}" in message.text
    
    if (is_reply_to_bot or is_mention) and not message.text.startswith('/'):
        # Simulação de resposta inteligente (Poderia usar OpenAI/Gemini)
        await bot.send_chat_action(message.chat.id, 'typing')
        await asyncio.sleep(1)
        await bot.reply_to(message, "🤖 Estou processando sua pergunta... Como posso ajudar mais especificamente?")
        return False # Interceptado

    return True

async def chatter(message):
    """Configurações do chatter/IA"""
    await bot.reply_to(message, "🤖 **Configurações de IA/Chatter:**\n\nNo momento, estou operando em modo de resposta básica. Em breve, integrações com modelos GPT.")

from bot import bot
