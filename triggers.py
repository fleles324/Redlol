# triggers.py - Sistema de gerenciamento de gatilhos do bot Segurança Privada

import re
import config
import importlib

# Dicionário global de triggers
triggers = {
    'on_text_message': [],
    'on_callback_query': []
}

def register_plugin_triggers(plugin_name, module):
    """Registra os triggers de um plugin no sistema global"""
    if hasattr(module, 'triggers'):
        for func_name, patterns in module.triggers.items():
            if func_name not in triggers:
                triggers[func_name] = []
            
            # Obtém a função do módulo
            func = getattr(module, func_name)
            for pattern in patterns:
                triggers[func_name].append((pattern, func))
        return True
    return False

async def process_text_triggers(message):
    """Processa triggers de texto baseados em regex"""
    text = message.text or message.caption or ""
    if 'on_text_message' in triggers:
        for pattern, func in triggers['on_text_message']:
            if re.search(pattern, text, re.IGNORECASE):
                await func(message)
                return True
    return False

async def process_callback_triggers(call):
    """Processa triggers de callback queries baseados em regex"""
    if 'on_callback_query' in triggers:
        for pattern, func in triggers['on_callback_query']:
            if re.search(pattern, call.data, re.IGNORECASE):
                await func(call)
                return True
    return False
