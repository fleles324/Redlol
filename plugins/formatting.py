import asyncio
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/format$',
        r'^/markdown$',
        r'^/bold$',
        r'^/italic$',
        r'^/code$'
    ]
}

async def formatting(message):
    """Guia de formatação Markdown para usuários e administradores"""
    text = (
        "✍️ **Guia de Formatação Markdown:**\n\n"
        "Use estas formatações em suas mensagens e respostas rápidas:\n\n"
        "- **Negrito:** `*texto*` — Ex: **negrito**\n"
        "- **Itálico:** `_texto_` — Ex: _itálico_\n"
        "- **Código:** `` `texto` `` — Ex: `código`\n"
        "- **Link:** `[nome](url)` — Ex: [Google](https://google.com)\n\n"
        "💡 **Dica:** No sistema de suporte (`/atendente`), você pode usar "
        "as variáveis `{user}`, `{atendente}` e `{id}` para personalizar "
        "suas respostas automaticamente!"
    )
    await bot.reply_to(message, text, parse_mode='Markdown')

async def bold(message):
    """Explicação sobre negrito"""
    await bot.reply_to(message, "Para escrever em **negrito**, use: `*seu texto aqui*`", parse_mode='Markdown')

async def italic(message):
    """Explicação sobre itálico"""
    await bot.reply_to(message, "Para escrever em _itálico_, use: `_seu texto aqui_`", parse_mode='Markdown')

async def code(message):
    """Explicação sobre código"""
    await bot.reply_to(message, "Para escrever em `código`, use: `` `seu texto aqui` ``", parse_mode='Markdown')

from bot import bot
