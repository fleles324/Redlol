import asyncio
import re
from telebot import types
from deep_translator import GoogleTranslator
from database import db
import config

# Configurações do plugin (Lado do Cliente)
triggers = {
    'on_callback_query': [
        r'^setlang:',
        r'^rate:'
    ],
    'on_text_message': [
        r'^/atendimento$',
        r'^/close$',
        r'^/setlang\s+(\w+)$',
        r'^/lang$'
    ]
}

async def on_every_message(message):
    """Encaminha mensagens do Cliente para o Atendente com fila de espera"""
    if not message.from_user or message.from_user.is_bot:
        return True

    if message.chat.type == 'private':
        text = message.text or message.caption or ""
        if text.startswith('/') or text.startswith('!'):
            return True

        user_id = message.from_user.id
        # Busca ticket ativo (pendente ou aberto)
        ticket = db.get_ticket_by_user(user_id)
        
        if ticket:
            user_lang = ticket.get('language') or 'pt'
            source_lang = user_lang.split('_')[0]
            
            # 1. Se o ticket já foi ACEITO (status 'open')
            if ticket['status'] == 'open' and ticket['thread_id']:
                try:
                    # Traduz apenas se for necessário
                    if source_lang != 'pt':
                        translated = GoogleTranslator(source=source_lang, target='pt').translate(text)
                        log_text = (
                            f"👤 **{message.from_user.first_name}** ({user_lang}):\n"
                            f"📝 **Original:** {text}\n"
                            f"🇧🇷 **Tradução:** {translated}"
                        )
                    else:
                        log_text = f"👤 **{message.from_user.first_name}**:\n{text}"
                    
                    await bot.send_message(config.SUPPORT_GROUP_ID, log_text, message_thread_id=ticket['thread_id'])
                    # O bot NÃO responde nada para o cliente se o atendimento já iniciou (conforme solicitado)
                except Exception as e:
                    print(f"[ERRO] Encaminhamento Suporte: {e}")
                return False

            # 2. Se o ticket está na FILA (status 'pending')
            elif ticket['status'] == 'pending':
                pos = db.get_queue_position(user_id)
                
                # Mensagens base
                if pos == 1:
                    wait_msg = "🌟 **Você é o próximo da fila!**\nUm atendente estará com você em instantes. Por favor, aguarde."
                else:
                    wait_msg = (
                        f"⏳ **Sua mensagem foi enviada para a fila.**\n\n"
                        f"🔢 Sua posição atual: `{pos}º` na fila.\n"
                        f"Por favor, aguarde enquanto um de nossos atendentes se conecta."
                    )
                
                # Tradução dinâmica da mensagem de espera
                try:
                    if source_lang != 'pt':
                        wait_msg = GoogleTranslator(source='pt', target=source_lang).translate(wait_msg)
                except:
                    pass
                
                await bot.reply_to(message, wait_msg, parse_mode='Markdown')
                return False

    return True

async def start_support_flow(message):
    """Inicia o fluxo de suporte perguntando o idioma"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(v, callback_data=f"setlang:{k}")
        for k, v in config.AVAILABLE_LANGUAGES.items()
    ]
    keyboard.add(*buttons)
    await bot.send_message(message.chat.id, "🌐 **Escolha seu idioma para o atendimento:**", reply_markup=keyboard, parse_mode='Markdown')

async def setlang(call):
    """Define o idioma e coloca o usuário na fila"""
    data = call.data.split(':')
    if len(data) < 2: return
    lang = data[1]
    
    if lang in ['menu', 'atendimento']:
        return await start_support_flow(call.message)

    user_id = call.from_user.id
    user_name = call.from_user.first_name
    
    db.set_user_lang(user_id, lang)
    lang_name = config.AVAILABLE_LANGUAGES.get(lang, lang)
    
    # Cria o ticket na fila (status pending)
    db.create_ticket(None, user_id, user_name, lang)
    pos = db.get_queue_position(user_id)

    # Notificação para a equipe (Botão de Aceitar)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🤝 ATENDER CHAMADO", callback_data=f"atender:{user_id}"))
    
    staff_msg = (
        f"🆕 **Novo Chamado na Fila!**\n\n"
        f"👤 **Usuário:** {user_name} (`{user_id}`)\n"
        f"🌐 **Idioma:** {lang_name}\n"
        f"🔢 **Posição na Fila:** `{pos}º`"
    )
    
    try:
        await bot.send_message(config.SUPPORT_GROUP_ID, staff_msg, message_thread_id=config.SUPPORT_THREAD_ID, reply_markup=keyboard, parse_mode='Markdown')
    except:
        await bot.send_message(config.SUPPORT_GROUP_ID, staff_msg, reply_markup=keyboard, parse_mode='Markdown')

    # Resposta para o cliente com tradução dinâmica
    lang_name = config.AVAILABLE_LANGUAGES.get(lang, lang)
    confirmation = (
        f"✅ **Idioma definido para: {lang_name}**\n\n"
        f"Você foi adicionado à nossa fila de suporte.\n"
        f"🔢 Sua posição atual: `{pos}º` na fila.\n\n"
        f"Aguarde um momento, notificaremos você assim que um atendente aceitar seu chamado."
    )
    
    try:
        # Traduz a confirmação se o idioma não for PT
        source_lang = lang.split('_')[0]
        if source_lang != 'pt':
            confirmation = GoogleTranslator(source='pt', target=source_lang).translate(confirmation)
    except:
        pass

    await bot.answer_callback_query(call.id, f"Idioma: {lang_name} ✅", show_alert=True)
    await bot.edit_message_text(confirmation, call.message.chat.id, call.message.message_id, parse_mode='Markdown')

async def close(message):
    """Encerra o ticket pelo cliente"""
    ticket = db.get_ticket_by_user(message.from_user.id)
    if ticket:
        db.close_ticket(ticket.get('thread_id'), message.from_user.id)
        await bot.reply_to(message, "✅ **Atendimento encerrado.**")
        if ticket.get('thread_id'):
            await bot.send_message(config.SUPPORT_GROUP_ID, f"🛑 **O cliente encerrou o atendimento.**", message_thread_id=ticket['thread_id'])
    else:
        await bot.reply_to(message, "❌ Você não possui um atendimento ativo.")

async def rate(call):
    """Processa a avaliação do usuário"""
    data = call.data.split(':')
    user_id = int(data[1])
    score = int(data[2])
    
    db.supabase.table("ratings").insert({"user_id": user_id, "score": score}).execute()
    await bot.answer_callback_query(call.id, "Obrigado! ⭐")
    await bot.edit_message_text(f"✅ **Obrigado!** Você avaliou com {score} estrelas.", call.message.chat.id, call.message.message_id)
    
    await bot.send_message(config.SUPPORT_GROUP_ID, f"⭐ **Nova Avaliação!**\n👤 Usuário: `{user_id}`\n📊 Nota: {score}/5", message_thread_id=config.RATINGS_THREAD_ID)

async def atendimento(message):
    """Alias para iniciar o fluxo de suporte"""
    await start_support_flow(message)

async def lang(message):
    """Alias para abrir o menu de idiomas"""
    await start_support_flow(message)

from bot import bot
