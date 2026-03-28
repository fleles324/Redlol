import asyncio
import re
import random
from telebot import types
import config

triggers = {
    'on_text_message': [
        r'^/roll$',
        r'^/dice$',
        r'^/8ball\s+(.*)',
        r'^/joke$',
        r'^/slap$',
        r'^/hug$'
    ]
}

async def roll(message):
    """Rola um dado de 1 a 6 ou envia o emoji de dado do Telegram"""
    await bot.send_dice(message.chat.id, emoji='🎲')

async def dice(message):
    await roll(message)

async def _8ball(message):
    """Responde a uma pergunta com a Bola Mágica 8"""
    match = re.search(r'^/8ball\s+(.*)', message.text, re.DOTALL)
    if not match:
        return await bot.reply_to(message, "❌ Faça uma pergunta! Ex: `/8ball Vou ficar rico?`", parse_mode='Markdown')
        
    respostas = [
        "Com certeza!", "É decididamente assim.", "Sem dúvida.", 
        "Sim, definitivamente.", "Você pode contar com isso.", 
        "A meu ver, sim.", "Provavelmente.", "Perspectiva boa.", 
        "Sim.", "Os sinais apontam que sim.",
        "Resposta nebulosa, tente de novo.", "Pergunte novamente mais tarde.", 
        "Melhor não te contar agora.", "Não é possível prever agora.", 
        "Concentre-se e pergunte de novo.",
        "Não conte com isso.", "Minha resposta é não.", 
        "Minhas fontes dizem não.", "Perspectiva não muito boa.", "Muito duvidoso."
    ]
    
    resposta = random.choice(respostas)
    await bot.reply_to(message, f"🎱 **Pergunta:** {match.group(1)}\n\n🔮 **Resposta:** {resposta}", parse_mode='Markdown')

async def joke(message):
    """Conta uma piada aleatória"""
    piadas = [
        "Por que o computador foi ao médico? Porque estava com um vírus!",
        "O que o zero disse para o oito? Belo cinto!",
        "Qual é o animal mais antigo? A zebra, porque está em preto e branco.",
        "Por que o livro de matemática se suicidou? Porque tinha muitos problemas.",
        "O que o pato disse para a pata? Vem Quack!",
        "Como o Batman faz para entrar na Bat-caverna? Ele bat-palma.",
        "Qual a diferença entre a lagoa e a padaria? Na lagoa há sapinho, na padaria assa pão."
    ]
    await bot.reply_to(message, f"😂 {random.choice(piadas)}")

async def slap(message):
    """Dá um tapa em alguém (reply)"""
    if not message.reply_to_message:
        return await bot.reply_to(message, "Você precisa responder à mensagem da pessoa que quer dar um tapa!")
        
    alvo = message.reply_to_message.from_user.first_name
    autor = message.from_user.first_name
    
    await bot.reply_to(message.reply_to_message, f"🖐 **{autor}** deu um tapa bem dado em **{alvo}**!")

async def hug(message):
    """Abraça alguém (reply)"""
    if not message.reply_to_message:
        return await bot.reply_to(message, "Você precisa responder à mensagem da pessoa que quer abraçar!")
        
    alvo = message.reply_to_message.from_user.first_name
    autor = message.from_user.first_name
    
    await bot.reply_to(message.reply_to_message, f"🫂 **{autor}** deu um abraço apertado em **{alvo}**!")

from bot import bot
