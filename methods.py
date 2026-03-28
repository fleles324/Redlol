import asyncio
import config

async def send_message(chat_id, text, parse_mode='Markdown', reply_markup=None):
    """Wrapper para envio de mensagens assíncronas"""
    from bot import bot
    return await bot.send_message(chat_id, text, parse_mode=parse_mode, reply_markup=reply_markup)

async def delete_message(chat_id, message_id):
    """Wrapper para deletar mensagens"""
    from bot import bot
    try:
        return await bot.delete_message(chat_id, message_id)
    except:
        return False

async def get_me():
    """Retorna informações do bot"""
    from bot import bot
    return await bot.get_me()
