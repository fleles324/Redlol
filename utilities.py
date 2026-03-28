import os
import config

def bash(command):
    """Executa um comando bash/shell"""
    return os.popen(command).read().strip()

def is_admin(chat_id, user_id):
    """Verifica se o usuário é admin (exemplo síncrono)"""
    return user_id in config.SUPERADMINS

def dump(label, data):
    """Debug helper"""
    print(f"[{label}] {data}")
