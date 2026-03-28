import asyncio
import re
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/menu$',
        r'^/start menu$'
    ],
    'on_callback_query': [
        r'^###cb:menu:(.*)$'
    ]
}

async def menu(message):
    """Menu principal de comandos com visual profissional"""
    bot_info = await bot.get_me()
    text = (
        f"🛡️ **CENTRAL DE COMANDOS - {config.BOT_NAME.upper()}** 🛡️\n\n"
        f"Olá **{message.from_user.first_name}**, seja bem-vindo ao painel interativo. "
        "Aqui você encontra todas as ferramentas necessárias para gerenciar e interagir.\n\n"
        f"💎 **Versão:** `{config.VERSION}`\n"
        "🔧 **Status:** `Online 🟢`\n\n"
        "👇 **SELECIONE UMA CATEGORIA ABAIXO:**"
    )
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("👮 MODERAÇÃO", callback_data="###cb:menu:admin"),
        types.InlineKeyboardButton("⚙️ CONFIGS", callback_data="###cb:menu:config")
    )
    keyboard.add(
        types.InlineKeyboardButton("📝 NOTAS (#)", callback_data="###cb:menu:notes"),
        types.InlineKeyboardButton("🛡️ SEGURANÇA", callback_data="###cb:menu:security")
    )
    keyboard.add(
        types.InlineKeyboardButton("🎮 DIVERSÃO", callback_data="###cb:menu:fun"),
        types.InlineKeyboardButton("ℹ️ SOBRE", callback_data="###cb:menu:info")
    )
    keyboard.add(
        types.InlineKeyboardButton("🎧 SUPORTE", callback_data="###cb:menu:support"),
        types.InlineKeyboardButton("📊 DADOS", callback_data="###cb:menu:stats")
    )
    keyboard.add(
        types.InlineKeyboardButton("🌐 CANAL", url=config.CHANNEL),
        types.InlineKeyboardButton("❌ FECHAR", callback_data="###cb:menu:close")
    )
    
    if hasattr(message, 'data'):
        # É um callback query
        await bot.edit_message_text(text, message.message.chat.id, message.message.message_id, reply_markup=keyboard, parse_mode='Markdown')
    else:
        # É uma mensagem normal
        await bot.reply_to(message, text, reply_markup=keyboard, parse_mode='Markdown')

async def menu_cb(call):
    """Trata os callbacks do menu interativo"""
    match = re.search(r'^###cb:menu:(.*)$', call.data)
    if not match:
        return
        
    action = match.group(1)
    
    if action == "close":
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        return
        
    if action == "main":
        await menu(call)
        return
        
    # Textos de cada categoria formatados profissionalmente
    texts = {
        "admin": (
            "👮 **GESTÃO E MODERAÇÃO**\n\n"
            "Ferramentas para controle total do seu grupo:\n\n"
            "• `/ban` - Bane um usuário permanentemente\n"
            "• `/unban` - Remove o banimento de um usuário\n"
            "• `/kick` - Remove o usuário (permite retorno)\n"
            "• `/mute` / `/unmute` - Controla o chat do usuário\n"
            "• `/warn` - Aplica uma advertência formal\n"
            "• `/unwarn` - Remove advertências acumuladas\n"
            "• `/promote` / `/demote` - Gerencia cargos"
        ),
        "config": (
            "⚙️ **CONFIGURAÇÕES DO SISTEMA**\n\n"
            "Personalize o comportamento do bot:\n\n"
            "• `/configure` - Menu visual de ajustes do grupo\n"
            "• `/welcome` - Configura mensagem de entrada\n"
            "• `/goodbye` - Configura mensagem de saída\n"
            "• `/rules` - Define as regras da comunidade\n"
            "• `/setlang` - Altera o idioma global\n"
            "• `/dashboard` - Visualiza seu perfil e estatísticas"
        ),
        "notes": (
            "📝 **SISTEMA DE NOTAS E GATILHOS**\n\n"
            "Gerencie conteúdo rápido para a comunidade:\n\n"
            "• `/note <nome> <texto>` - Cria uma nova nota\n"
            "• `/get <nome>` - Recupera uma nota salva\n"
            "• `#nome_da_nota` - Atalho rápido para exibir notas\n"
            "• `/notes` - Lista todas as notas ativas no chat\n"
            "• `/delnote <nome>` - Apaga uma nota existente"
        ),
        "security": (
            "🛡️ **MÓDULOS DE SEGURANÇA**\n\n"
            "Proteção ativa contra ataques e spam:\n\n"
            "• `/captcha on/off` - Ativa verificação humana\n"
            "• `/antispam` - Configura filtros de links e canais\n"
            "• `/antiflood` - Controla a velocidade das mensagens\n"
            "• `/lock` / `/unlock` - Bloqueia tipos de mídia (GIF, Stickers, etc)\n"
            "• `/block <id>` - Banimento global da rede"
        ),
        "fun": (
            "🎮 **DIVERSÃO E INTERAÇÃO**\n\n"
            "Comandos sociais para engajar os membros:\n\n"
            "• `/roll` ou `/dice` - Joga um dado da sorte\n"
            "• `/8ball <pergunta>` - Consulte a bola mágica\n"
            "• `/joke` - Conta uma piada aleatória\n"
            "• `/slap` (reply) - Dá um tapa em alguém\n"
            "• `/hug` (reply) - Dá um abraço carinhoso\n"
            "• `/cats` - Foto aleatória de gatinho"
        ),
        "info": (
            "ℹ️ **SOBRE O PROJETO**\n\n"
            f"O **{config.BOT_NAME}** é um bot multifuncional desenvolvido em Python.\n\n"
            "• **Desenvolvedor:** Segurança Privada\n"
            "• **Backend:** Supabase (PostgreSQL)\n"
            "• **Tradução:** Google AI\n"
            "• **Licença:** MIT"
        ),
        "support": (
            "🎧 **CENTRAL DE SUPORTE**\n\n"
            "Precisa de ajuda humana ou técnica?\n\n"
            "• **Abrir Chamado:** Clique no botão abaixo para iniciar.\n"
            "• **FAQ:** Use `/faq` para dúvidas comuns.\n\n"
            "O suporte conta com **tradução automática em tempo real**."
        ),
        "stats": (
            "📊 **ESTATÍSTICAS E DADOS**\n\n"
            "Acompanhe o crescimento e atividade:\n\n"
            "• `/ranking` - Top 10 membros mais ativos\n"
            "• `/ranking_staff` - Ranking Top 10 Atendentes\n"
            "• `/stats` - Dados globais do banco de dados\n"
            "• `/id` - Consulta IDs de usuários ou grupos\n"
            "• `/backup` - Exporta dados (Apenas Super Admin)"
        )
    }
    
    res_text = texts.get(action, "Em desenvolvimento...")
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Se for a categoria suporte, adiciona o botão de abrir ticket e escolher idioma
    if action == "support":
        keyboard.add(types.InlineKeyboardButton("🎧 ABRIR TICKET", callback_data="setlang:atendimento"))
        keyboard.add(types.InlineKeyboardButton("🌍 ESCOLHER IDIOMA", callback_data="setlang:menu"))
    
    keyboard.add(types.InlineKeyboardButton("⬅️ VOLTAR AO MENU", callback_data="###cb:menu:main"))
    
    await bot.edit_message_text(res_text, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='Markdown')

from bot import bot
