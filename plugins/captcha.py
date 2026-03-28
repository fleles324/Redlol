import asyncio
import re
import random
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/captcha\s+(on|off)$'
    ],
    'on_callback_query': [
        r'^###cb:captcha:(.*)$'
    ]
}

# Dicionário temporário para armazenar desafios de captcha
# Formato: {user_id: {'chat_id': chat_id, 'answer': answer, 'message_id': message_id}}
pending_captchas = {}

async def captcha_cmd(message):
    """Ativa ou desativa o CAPTCHA no grupo (Apenas Admin)"""
    # Verifica se é admin
    try:
        admins = await bot.get_chat_administrators(message.chat.id)
        admin_ids = [admin.user.id for admin in admins]
        if message.from_user.id not in admin_ids and message.from_user.id not in config.SUPERADMINS:
            return await bot.reply_to(message, "❌ Apenas administradores podem usar este comando.")
    except:
        pass

    match = re.search(r'^/captcha\s+(on|off)$', message.text.lower())
    if not match:
        return await bot.reply_to(message, "❌ Use: `/captcha on` ou `/captcha off`", parse_mode='Markdown')
        
    status = match.group(1)
    
    # Salvar configuração no banco
    db.set_quick_reply(f"captcha_status_{message.chat.id}", status)
    
    if status == 'on':
        await bot.reply_to(message, "✅ **CAPTCHA Ativado!**\nNovos membros precisarão resolver um desafio matemático para falar no grupo.", parse_mode='Markdown')
    else:
        await bot.reply_to(message, "❌ **CAPTCHA Desativado!**\nNovos membros podem falar livremente.", parse_mode='Markdown')

async def captcha_cb(call):
    """Lida com as respostas do desafio captcha"""
    data = call.data.split(':')
    if len(data) < 4:
        return
        
    is_correct = data[2] == "1"
    target_user_id = int(data[3])
    
    if call.from_user.id != target_user_id:
        return await bot.answer_callback_query(call.id, "❌ Esse desafio não é para você!", show_alert=True)
        
    if is_correct:
        try:
            # Libera o usuário
            await bot.restrict_chat_member(
                call.message.chat.id, 
                target_user_id,
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
            await bot.answer_callback_query(call.id, "✅ Verificação concluída! Bem-vindo(a).", show_alert=True)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            await bot.answer_callback_query(call.id, f"❌ Erro ao liberar: {e}")
    else:
        try:
            await bot.answer_callback_query(call.id, "❌ Resposta incorreta! Você foi banido temporariamente.", show_alert=True)
            await bot.kick_chat_member(call.message.chat.id, target_user_id, until_date=int(asyncio.get_event_loop().time()) + 60)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            await bot.answer_callback_query(call.id, f"❌ Erro ao banir: {e}")

async def on_new_chat_members(message):
    """Gatilho para quando um novo membro entra no grupo"""
    status = db.get_quick_reply(f"captcha_status_{message.chat.id}")
    if status != 'on':
        return True # Deixa outros plugins (como welcome) processarem
        
    for new_member in message.new_chat_members:
        if new_member.id == bot.get_me().id:
            continue
            
        # Restringe o usuário
        try:
            await bot.restrict_chat_member(
                message.chat.id, 
                new_member.id,
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False
            )
            
            # Gera o desafio
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            answer = num1 + num2
            
            # Opções de resposta (1 correta, 2 erradas)
            options = [answer, answer + random.randint(1, 5), answer - random.randint(1, 3)]
            random.shuffle(options)
            
            keyboard = types.InlineKeyboardMarkup(row_width=3)
            buttons = []
            for opt in options:
                # O callback_data contém se é correto ou errado e o ID do usuário
                is_correct = "1" if opt == answer else "0"
                cb_data = f"###cb:captcha:{is_correct}:{new_member.id}"
                buttons.append(types.InlineKeyboardButton(str(opt), callback_data=cb_data))
                
            keyboard.add(*buttons)
            
            text = (
                f"🛡️ **Verificação de Segurança**\n\n"
                f"Olá [{new_member.first_name}](tg://user?id={new_member.id}), bem-vindo(a) ao grupo!\n"
                f"Para provar que você é humano e ser liberado para falar, resolva a conta abaixo:\n\n"
                f"**{num1} + {num2} = ?**\n\n"
                f"⏳ _Você tem 2 minutos para responder._"
            )
            
            msg = await bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='Markdown')
            
            # Agenda a remoção se não responder
            asyncio.create_task(kick_if_unverified(message.chat.id, new_member.id, msg.message_id))
            
        except Exception as e:
            print(f"Erro no captcha: {e}")
            
    return False # Intercepta a mensagem de entrada para não mostrar o welcome padrão

async def kick_if_unverified(chat_id, user_id, message_id):
    """Kicka o usuário se ele não resolver o captcha em 2 minutos"""
    await asyncio.sleep(120) # 2 minutos
    
    # Verifica se a mensagem ainda existe (se não existe, é porque ele resolveu)
    try:
        # Tenta deletar a mensagem. Se der erro, ela já foi apagada (resolvido)
        await bot.delete_message(chat_id, message_id)
        
        # Se chegou aqui, ele não resolveu. Kicka o usuário.
        await bot.kick_chat_member(chat_id, user_id)
        await bot.unban_chat_member(chat_id, user_id) # Unban para permitir que ele volte
        
        # Avisa no grupo
        msg = await bot.send_message(chat_id, "🤖 Um usuário não passou no CAPTCHA e foi removido.")
        await asyncio.sleep(10)
        await bot.delete_message(chat_id, msg.message_id)
    except:
        pass # Já foi resolvido e a mensagem apagada

async def on_callback_query(call):
    """Trata os callbacks do CAPTCHA"""
    match = re.search(r'^###cb:captcha:(\d):(\d+)$', call.data)
    if not match:
        return
        
    is_correct = match.group(1)
    target_user_id = int(match.group(2))
    
    # Verifica se quem clicou é o alvo do captcha
    if call.from_user.id != target_user_id:
        return await bot.answer_callback_query(call.id, "❌ Este botão não é para você!", show_alert=True)
        
    if is_correct == "1":
        # Acertou! Libera o usuário
        try:
            await bot.restrict_chat_member(
                call.message.chat.id,
                target_user_id,
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
            await bot.answer_callback_query(call.id, "✅ Verificação concluída! Você já pode falar no grupo.", show_alert=True)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            await bot.answer_callback_query(call.id, "❌ Erro ao liberar você. Contate um admin.")
    else:
        # Errou! Kicka o usuário
        try:
            await bot.answer_callback_query(call.id, "❌ Resposta incorreta! Você foi removido do grupo.", show_alert=True)
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await bot.kick_chat_member(call.message.chat.id, target_user_id)
            await bot.unban_chat_member(call.message.chat.id, target_user_id)
        except:
            pass

from bot import bot
