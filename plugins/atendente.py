import asyncio
import re
from telebot import types
from deep_translator import GoogleTranslator
from database import db
import config

# Configurações do plugin (Lado do Staff/Atendente)
triggers = {
    'on_callback_query': [
        r'^atender:',
        r'^close_ticket:',
        r'^qr:'
    ],
    'on_text_message': [
        r'^/atendente$',
        r'^/close_staff$'
    ]
}

async def on_every_message(message):
    """Encaminha mensagens do Atendente para o Cliente com tradução"""
    if not message.from_user or message.from_user.is_bot:
        return True

    chat_id = message.chat.id
    if chat_id == config.SUPPORT_GROUP_ID and message.message_thread_id:
        text = message.text or message.caption or ""
        if text.startswith('/') or text.startswith('!'):
            return True

        ticket = db.get_ticket_by_thread(message.message_thread_id)
        if ticket:
            client_id = ticket['user_id']
            client_lang = (ticket.get('language') or 'pt').split('_')[0]
            
            try:
                if client_lang != 'pt':
                    translated = GoogleTranslator(source='pt', target=client_lang).translate(text)
                    await bot.send_message(client_id, translated)
                else:
                    await bot.send_message(client_id, text)
            except Exception as e:
                print(f"[ERRO] Tradução Atendente->Cliente: {e}")
                await bot.send_message(client_id, text)
            return False

    return True

async def atender(call):
    """Inicia atendimento, cria tópico e remove da fila"""
    user_id = int(call.data.split(':')[1])
    staff_id = call.from_user.id
    staff_name = call.from_user.first_name
    
    # Busca dados do ticket pendente
    ticket = db.get_ticket_by_user(user_id)
    if not ticket or ticket['status'] != 'pending':
        return await bot.answer_callback_query(call.id, "❌ Este chamado já foi aceito ou expirou.", show_alert=True)

    user_lang = ticket.get('language') or 'pt_BR'
    lang_name = config.AVAILABLE_LANGUAGES.get(user_lang, user_lang)
    user_name = ticket.get('user_name', 'Cliente')

    try:
        # 1. Cria o tópico no fórum
        topic = await bot.create_forum_topic(
            config.SUPPORT_GROUP_ID, 
            f"Ticket: {user_name} [{lang_name}]"
        )
        
        # 2. Atualiza o ticket para status 'open' e vincula ao staff e tópico
        db.accept_ticket(user_id, staff_id, staff_name, topic.message_thread_id)
        
        # 3. Mensagem inicial no tópico com botões de QR
        replies = db.get_all_quick_replies()
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for r in replies[:6]:
            keyboard.add(types.InlineKeyboardButton(f"💬 {r['key']}", callback_data=f"qr:{r['key']}"))
        keyboard.add(types.InlineKeyboardButton("❌ ENCERRAR ATENDIMENTO", callback_data=f"close_ticket:{user_id}"))
        
        staff_welcome = (
            f"🛠 **Atendimento Iniciado**\n\n"
            f"👤 **Cliente:** {user_name} (`{user_id}`)\n"
            f"🌐 **Idioma do Cliente:** {lang_name}\n"
            f"👮 **Atendente:** {staff_name}\n\n"
            f"✍️ **Instrução:** Digite em Português. O bot traduzirá para o cliente."
        )
        await bot.send_message(config.SUPPORT_GROUP_ID, staff_welcome, message_thread_id=topic.message_thread_id, reply_markup=keyboard, parse_mode='Markdown')
        
        # 4. Notifica o cliente com tradução
        welcome_client = "🎧 **Um atendente acaba de entrar no chat!**\nVocê já pode enviar sua dúvida."
        try:
            if client_lang != 'pt':
                welcome_client = GoogleTranslator(source='pt', target=client_lang).translate(welcome_client)
        except:
            pass
            
        await bot.send_message(user_id, welcome_client, parse_mode='Markdown')
        
        # 5. Atualiza mensagem de chamado na fila
        await bot.edit_message_text(
            f"✅ **Chamado aceito por {staff_name}!**\nAtendimento movido para o tópico dedicado.",
            call.message.chat.id,
            call.message.message_id
        )
        
        await bot.answer_callback_query(call.id, "Atendimento iniciado!")
        
    except Exception as e:
        print(f"[ERRO] Ao criar tópico: {e}")
        await bot.answer_callback_query(call.id, f"❌ Erro ao iniciar: {e}", show_alert=True)

async def close_ticket(call):
    """Encerra o ticket, solicita avaliação e deleta o tópico"""
    user_id = int(call.data.split(':')[1])
    thread_id = call.message.message_thread_id
    
    if thread_id:
        db.close_ticket(thread_id, user_id)
        
        # Envia avaliação para o cliente com tradução
        ticket = db.get_ticket_by_user(user_id)
        client_lang = (ticket.get('language') or 'pt').split('_')[0] if ticket else 'pt'
        
        close_msg = "🌟 **Atendimento concluído!**\nPor favor, avalie o nosso suporte:"
        try:
            if client_lang != 'pt':
                close_msg = GoogleTranslator(source='pt', target=client_lang).translate(close_msg)
        except:
            pass
            
        keyboard = types.InlineKeyboardMarkup(row_width=5)
        buttons = [types.InlineKeyboardButton(str(i), callback_data=f"rate:{user_id}:{i}") for i in range(1, 6)]
        keyboard.add(*buttons)
        
        await bot.send_message(user_id, close_msg, reply_markup=keyboard, parse_mode='Markdown')
        
        # Notifica encerramento no grupo e DELETA o tópico após 5 segundos para limpeza
        await bot.send_message(config.SUPPORT_GROUP_ID, f"🛑 **Atendimento encerrado por {call.from_user.first_name}.**\nEste tópico será removido em breve.", message_thread_id=thread_id)
        await bot.answer_callback_query(call.id, "Ticket encerrado!")
        
        await asyncio.sleep(5)
        try:
            await bot.delete_forum_topic(config.SUPPORT_GROUP_ID, thread_id)
        except:
            pass
    else:
        await bot.answer_callback_query(call.id, "Erro ao encerrar.")

async def qr(call):
    """Resposta rápida com tradução"""
    key = call.data.split(':')[1]
    ticket = db.get_ticket_by_thread(call.message.message_thread_id)
    if not ticket: return

    text = db.get_quick_reply(key)
    if not text: return

    text = text.replace("{user}", ticket['user_name']).replace("{atendente}", call.from_user.first_name)
    
    client_lang = (ticket.get('language') or 'pt').split('_')[0]
    try:
        if client_lang != 'pt':
            text = GoogleTranslator(source='pt', target=client_lang).translate(text)
    except:
        pass

    await bot.send_message(ticket['user_id'], text, parse_mode='Markdown')
    await bot.answer_callback_query(call.id, f"Resposta '{key}' enviada!")

async def atendente(message):
    """Acessa o painel do atendente (Alias para /atendimento staff)"""
    # Se for no grupo de suporte e em um tópico, mostra as opções
    if message.chat.id == config.SUPPORT_GROUP_ID and message.message_thread_id:
        replies = db.get_all_quick_replies()
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for r in replies[:10]:
            keyboard.add(types.InlineKeyboardButton(f"💬 {r['key']}", callback_data=f"qr:{r['key']}"))
        
        ticket = db.get_ticket_by_thread(message.message_thread_id)
        if ticket:
            keyboard.add(types.InlineKeyboardButton("❌ ENCERRAR TICKET", callback_data=f"close_ticket:{ticket['user_id']}"))
            
        await bot.reply_to(message, "📊 **Painel de Atendimento**\nEscolha uma resposta rápida ou encerre o chamado:", reply_markup=keyboard, parse_mode='Markdown')
    else:
        await bot.reply_to(message, "❌ Este comando só pode ser usado dentro de um tópico de atendimento no grupo de suporte.")

async def close_staff(message):
    """Encerra o ticket via comando pelo staff"""
    if message.chat.id == config.SUPPORT_GROUP_ID and message.message_thread_id:
        ticket = db.get_ticket_by_thread(message.message_thread_id)
        if ticket:
            # Simula o clique no botão de encerrar
            class MockCall:
                def __init__(self, message, from_user):
                    self.message = message
                    self.from_user = from_user
                    self.data = f"close_ticket:{ticket['user_id']}"
                async def answer_callback_query(self, *args, **kwargs): pass
            
            await close_ticket(MockCall(message, message.from_user))
        else:
            await bot.reply_to(message, "❌ Nenhum ticket ativo encontrado neste tópico.")
    else:
        await bot.reply_to(message, "❌ Este comando só pode ser usado dentro de um tópico de atendimento.")

from bot import bot
