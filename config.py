import re
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

BOT_NAME = os.getenv("BOT_NAME", "Segurança Privada")

# Configuração do Bot
BOT_API_KEY = os.getenv("BOT_API_KEY", "8635961689:AAEt_cGXdbF-Ht9MymVAzyV0R306MlpxFQk")
THECATAPI_KEY = 'http://thecatapi.com/?id=5vs'
CMD_PREFIX = r'^[/!#]'
ALLOWED_UPDATES = ["message", "edited_message", "callback_query"]

# Supabase (Substitui o Redis para SQL)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://alqegjahchedaoncstdu.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFscWVnamFoY2hlZGFvbmNzdGR1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzMDc2ODUsImV4cCI6MjA4OTg4MzY4NX0.BenGt5hnQuWkbrlZ12GlZyPfekr-LIqoymvbHo9a3_4")

# Admins e Logs
SUPERADMINS = [8422287086]
SUPPORT_GROUP_ID = int(os.getenv("SUPPORT_GROUP_ID", "-1003765734362"))
SUPPORT_THREAD_ID = int(os.getenv("SUPPORT_THREAD_ID", "668"))
RATINGS_THREAD_ID = int(os.getenv("RATINGS_THREAD_ID", "672"))
FAQ_THREAD_ID = int(os.getenv("FAQ_THREAD_ID", "788"))
RANKING_UPDATE_INTERVAL = int(os.getenv("RANKING_UPDATE_INTERVAL", "3600"))
LOG_CHAT = SUPPORT_GROUP_ID
LOG_ADMIN = 8422287086

VERSION = '4.2.0 (Python)'
CHANNEL = os.getenv("BOT_CHANNEL", "https://t.me/soofertasbr")
HELP_GROUPS_LINK = os.getenv("BOT_SUPPORT_GROUP", "https://t.me/soofertasbr")

AVAILABLE_LANGUAGES = {
    'en': 'English 🇬🇧',
    'it': 'Italiano 🇮🇹',
    'es': 'Español 🇪🇸',
    'pt_BR': 'Português 🇧🇷',
    'ru': 'Русский 🇷🇺',
    'de': 'Deutsch 🇩🇪',
    'ar': 'العربية 🇸🇩',
    'zh': '中文 🇨🇳',
    'fa': 'فarسی 🇮🇷',
    'id': 'Bahasa Indonesia 🇮🇩',
    'nl': 'Dutch 🇱🇺'
}

# Configurações Padrão de Chat
DEFAULT_CHAT_SETTINGS = {
    'settings': {
        'Welcome': 'off',
        'Goodbye': 'off',
        'Extra': 'on',
        'Silent': 'off',
        'Rules': 'off',
        'Reports': 'off',
        'Welbut': 'off',
        'Antibot': 'off'
    },
    'antispam': {
        'links': 'alwd',
        'forwards': 'alwd',
        'warns': 2,
        'action': 'ban'
    },
    'flood': {
        'MaxFlood': 5,
        'ActionFlood': 'kick'
    }
}

# Lista de Plugins Ativos (Python)
PLUGINS = [
    'atendente',
    'support',
    'atendimento',
    'translate',
    'onmessage', 
    'start', 
    'id', 
    'help', 
    'banhammer', 
    'warn', 
    'welcome', 
    'rules', 
    'extra', 
    'ranking',
    'report',
    'protection',
    'admin',
    'private',
    'configure',
    'dashboard',
    'pin',
    'block',
    'moderators',
    'logchannel',
    'service',
    'about',
    'formatting',
    'backup',
    'cats',
    'tools',
    'groups',
    'sorteio',
    'chatter',
    'donations',
    'gmaps',
    'links',
    'mediasettings',
    'realms',
    'antispam',
    'floodmanager',
    'menu',
    'sobre',
    'grupos',
    'doacoes',
    'formatacao',
    'users',
    'private_settings',
    'ranking_data',
    'ranking_atendentes',
    'chatter2',
    'broadcast',
    'stats',
    'search',
    'faq',
    'notes',
    'fun',
    'captcha'
]
