import asyncio
import os
import importlib
import re
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import config
from database import db

# Inicializa o Bot
bot = AsyncTeleBot(config.BOT_API_KEY)

# Armazenamento global de plugins carregados
plugins_loaded = {}
triggers = {
    'on_text_message': [],
    'on_callback_query': []
}

def load_plugins():
    """Carrega dinamicamente os plugins listados no config.py uma única vez"""
    for plugin_name in config.PLUGINS:
        try:
            module_path = f"plugins.{plugin_name}"
            module = importlib.import_module(module_path)
            plugins_loaded[plugin_name] = module
            
            # Se o módulo tiver triggers, registra-os
            if hasattr(module, 'triggers'):
                for trigger_key, patterns in module.triggers.items():
                    if trigger_key not in triggers:
                        continue
                    
                    for pattern in patterns:
                        # Extrai o nome da função do pattern ou usa o trigger_key como fallback
                        func_name = None
                        
                        # 1. Tenta extrair o nome da função do pattern (^/comando$)
                        cmd_match = re.search(r'\^/(\w+)', pattern)
                        if cmd_match:
                            func_name = cmd_match.group(1)
                        
                        # 2. Tenta extrair de callbacks complexos (^###cb:nome:)
                        if not func_name and trigger_key == 'on_callback_query':
                            cb_complex_match = re.search(r'cb:(\w+):', pattern)
                            if cb_complex_match:
                                func_name = f"{cb_complex_match.group(1)}_cb"
                            else:
                                cb_match = re.search(r'\^(\w+):', pattern)
                                if cb_match:
                                    func_name = cb_match.group(1)
                        
                        # 3. Se ainda não tem func_name e for comando, tenta variações
                        if func_name and trigger_key == 'on_text_message':
                            if not hasattr(module, func_name):
                                if hasattr(module, f"{func_name}_cmd"):
                                    func_name = f"{func_name}_cmd"
                        
                        # 3. Fallbacks
                        if not func_name or not hasattr(module, func_name):
                            # Se func_name começa com número, tenta com prefixo "_"
                            if func_name and func_name[0].isdigit():
                                alt_func_name = f"_{func_name}"
                                if hasattr(module, alt_func_name):
                                    func_name = alt_func_name
                            
                            # Se ainda não encontrou, tenta outros fallbacks
                            if not hasattr(module, func_name or ""):
                                # Tenta o trigger_key (on_text_message / on_callback_query)
                                if hasattr(module, trigger_key):
                                    func_name = trigger_key
                                # Tenta o nome do plugin
                                elif hasattr(module, plugin_name):
                                    func_name = plugin_name
                        
                        # Se encontrou uma função válida, registra o trigger
                        if func_name and hasattr(module, func_name):
                            func = getattr(module, func_name)
                            triggers[trigger_key].append((pattern, func))
                        else:
                            # Se não encontrou função específica mas tem patterns, avisa
                            if patterns:
                                print(f"[AVISO] Plugin '{plugin_name}' tem triggers mas nenhuma função '{func_name or trigger_key}' foi encontrada.")
            
            print(f"[INFO] Plugin '{plugin_name}' carregado com sucesso.")
        except Exception as e:
            print(f"[ERRO] Falha ao carregar plugin '{plugin_name}': {e}")

@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
    """Handler central que distribui mensagens para os plugins"""
    text = message.text or message.caption or ""
    
    # 1. Executa on_every_message de todos os plugins carregados
    for plugin_name, module in plugins_loaded.items():
        try:
            if hasattr(module, 'on_every_message'):
                continue_exec = await module.on_every_message(message)
                if continue_exec is False:
                    return
        except Exception as e:
            print(f"[ERRO] Erro em on_every_message do plugin {plugin_name}: {e}")

    # 2. Verifica triggers de texto
    for pattern, func in triggers['on_text_message']:
        if re.search(pattern, text, re.IGNORECASE):
            await func(message)
            return

@bot.callback_query_handler(func=lambda call: True)
async def handle_callback_queries(call):
    """Handler central para callback queries"""
    for pattern, func in triggers['on_callback_query']:
        if re.search(pattern, call.data, re.IGNORECASE):
            await func(call)
            return

async def main():
    print(f"--- Iniciando {config.BOT_NAME} (Python) ---")
    load_plugins()
    print("Bot rodando...")
    await bot.polling(non_stop=True, allowed_updates=config.ALLOWED_UPDATES)

if __name__ == "__main__":
    asyncio.run(main())
