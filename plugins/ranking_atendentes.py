import asyncio
import re
from telebot import types
from database import db
import config

triggers = {
    'on_text_message': [
        r'^/ranking_staff$'
    ]
}

async def generate_ranking_text():
    """Gera o texto formatado do ranking"""
    ranking = db.get_staff_ranking()
    
    if not ranking:
        return "📊 **Ranking ainda não disponível.** É necessário que os atendentes concluam atendimentos com avaliações."

    text = "🥇 **RANKING TOP 10 ATENDENTES**\n\n"
    text += "🏅 Legenda:\n👤 Atendente | ⭐ CSAT | 💙 NPS\n⚡ FRT | 🎯 FCR | 🕐 AHT\n📈 Média Geral\n\n---\n\n"
    
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for i, s in enumerate(ranking):
        medal = medals[i] if i < len(medals) else f"{i+1}️⃣"
        
        text += (
            f"{medal}\n"
            f"**{s['name']}**\n"
            f"{s['csat']} ⭐\n"
            f"+{s['nps']} 💙\n"
            f"{s['frt']} ⚡\n"
            f"{s['fcr']} 🎯\n"
            f"{s['aht']} 🕐\n"
            f"**{s['media']}%** 🏆\n\n"
        )
    return text

async def post_updated_ranking():
    """Limpa mensagens antigas e posta o novo ranking"""
    try:
        # 1. Tenta deletar a última mensagem postada (se existir no banco)
        last_msg_id = db.get_last_ranking_msg()
        if last_msg_id:
            try:
                await bot.delete_message(config.SUPPORT_GROUP_ID, last_msg_id)
            except:
                pass # Mensagem pode ser muito antiga ou já deletada

        # 2. Gera o novo texto
        text = await generate_ranking_text()

        # 3. Posta a nova lista
        new_msg = await bot.send_message(
            config.SUPPORT_GROUP_ID, 
            text, 
            message_thread_id=config.RATINGS_THREAD_ID,
            parse_mode='Markdown'
        )

        # 4. Salva o ID da nova mensagem para a próxima limpeza
        db.set_last_ranking_msg(new_msg.message_id)
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao atualizar ranking automático: {e}")
        return False

async def ranking_staff(message):
    """Comando manual para forçar atualização do ranking"""
    if message.from_user.id not in config.SUPERADMINS:
        return await bot.reply_to(message, "❌ Apenas administradores podem gerar o ranking oficial.")

    success = await post_updated_ranking()
    if success:
        await bot.reply_to(message, "✅ **Ranking atualizado e postado no tópico de avaliações!**")
    else:
        await bot.reply_to(message, "❌ Erro ao atualizar ranking.")

# --- LOOP DE ATUALIZAÇÃO AUTOMÁTICA (1 HORA) ---
async def ranking_auto_updater():
    """Loop que roda a cada 1 hora para atualizar o ranking"""
    await asyncio.sleep(10) # Espera o bot inicializar completamente
    while True:
        print(f"[INFO] Atualizando ranking de atendentes automaticamente (Intervalo: {config.RANKING_UPDATE_INTERVAL}s)...")
        await post_updated_ranking()
        await asyncio.sleep(config.RANKING_UPDATE_INTERVAL) # Usa o valor dinâmico do .env

# Inicia o loop em background
asyncio.ensure_future(ranking_auto_updater())

from bot import bot
