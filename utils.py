import config
from telebot import types

def is_superadmin(user_id):
    """Verifica se o usuário é um Super Admin do bot"""
    return user_id in config.SUPERADMINS

async def is_admin(bot, chat_id, user_id):
    """Verifica se o usuário é administrador de um grupo específico"""
    if user_id in config.SUPERADMINS:
        return True
    
    try:
        admins = await bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]
        return user_id in admin_ids
    except:
        return False

def get_user_mention(user):
    """Retorna a menção do usuário em Markdown (Nome com link do ID ou @username)"""
    if user.username:
        return f"@{user.username}"
    else:
        # Se não tiver username, cria um link com o nome e o ID
        return f"[{user.first_name}](tg://user?id={user.id})"

def clean_html(text):
    """Remove tags HTML básicas de uma string para evitar erros no parse_mode"""
    import re
    return re.sub(r'<[^>]+>', '', text)
