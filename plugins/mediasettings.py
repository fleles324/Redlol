import asyncio
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/media$',
        r'^/mediasettings$',
        r'^/setmedia\s+(\w+)\s*\|\s*(\w+)'
    ]
}

async def on_every_message(message):
    """Monitora mídias e restringe conforme configurações do chat"""
    if not message.from_user or message.from_user.is_bot:
        return True

    chat_id = message.chat.id
    settings = db.get_chat_settings(chat_id)
    mediasettings = settings.get('media', config.DEFAULT_CHAT_SETTINGS.get('media', {}))
    
    # Verifica tipos de mídia
    media_type = None
    if message.photo: media_type = 'photo'
    elif message.video: media_type = 'video'
    elif message.audio: media_type = 'audio'
    elif message.document: media_type = 'document'
    elif message.sticker: media_type = 'sticker'
    elif message.voice: media_type = 'voice'
    elif message.video_note: media_type = 'video_note'
    
    # Se a mídia estiver proibida nas configurações do grupo
    if media_type and mediasettings.get(media_type) == 'fbd':
        try:
            # Deleta a mídia proibida
            await bot.delete_message(chat_id, message.message_id)
            await bot.send_message(chat_id, f"🚫 **{message.from_user.first_name}**, o envio de {media_type} não é permitido neste chat!", parse_mode='Markdown')
            return False # Interceptado
        except:
            pass

    return True

async def mediasettings(message):
    """Menu de configurações de mídia (Admin)"""
    if message.chat.type == 'private':
        return
    
    text = (
        f"📸 **Configurações de Mídia em {message.chat.title}**\n\n"
        "Escolha quais mídias são permitidas no grupo:"
    )
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    # Exemplos de botões de configuração de mídia
    keyboard.add(types.InlineKeyboardButton("Fotos: ✅", callback_data=f"###cb:media:photo:{message.chat.id}"))
    keyboard.add(types.InlineKeyboardButton("Vídeos: ✅", callback_data=f"###cb:media:video:{message.chat.id}"))
    keyboard.add(types.InlineKeyboardButton("Áudios: ✅", callback_data=f"###cb:media:audio:{message.chat.id}"))
    keyboard.add(types.InlineKeyboardButton("Figurinhas: ✅", callback_data=f"###cb:media:sticker:{message.chat.id}"))
    
    await bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

from bot import bot
