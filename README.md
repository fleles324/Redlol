# 🤖 Segurança Privada - Ecossistema Completo de Gestão e Suporte (v4.5.0)

O **Segurança Privada** é uma solução profissional e modular para gerenciamento, segurança e atendimento em comunidades do Telegram. Desenvolvido em **Python** com a biblioteca `async_telebot`, ele utiliza o **Supabase (PostgreSQL)** como backend para garantir persistência robusta, velocidade de resposta e escalabilidade para grandes redes de grupos.

---

## 🚀 Funcionalidades Principais

### 👮 Menu Centralizado e Interativo
O bot conta com um sistema de **Menu por Categorias** totalmente interativo via botões inline, facilitando a navegação sem poluir o chat.
- **Navegação Intuitiva**: Categorias como Moderação, Configurações, Segurança, Diversão, Suporte e Estatísticas.
- **Acesso Rápido**: Comando `/menu` ou `/start` no privado.

### 🛡️ Segurança e Moderação de Elite
Proteção total contra ataques, spam e comportamentos indesejados.
- **CAPTCHA Inteligente**: Novos membros são silenciados e precisam resolver um desafio matemático (`X + Y = ?`) para serem liberados.
- **Anti-Spam Dinâmico**: Bloqueio automático de links externos, convites e encaminhamentos de canais/bots.
- **Anti-Flood Adaptativo**: Monitora a frequência de mensagens e aplica punições automáticas (Mute, Kick ou Ban).
- **Proteção de Mídia (Lock/Unlock)**: Controle granular sobre o que pode ser enviado (Fotos, Vídeos, Stickers, Áudios, GIFs, etc).
- **Sistema de Advertências (Warns)**: Gestão de punições acumulativas com banimento automático ao atingir o limite configurado.
- **Banimento Global (Blacklist)**: Bloqueio de usuários mal-intencionados em todos os grupos da rede.

### � Sistema de Suporte Multi-Idioma (Client-Staff)
Um sistema de tickets profissional integrado diretamente ao Telegram via Forum Topics.
- **Tradução em Tempo Real**: Tradução automática entre o idioma do cliente e o idioma da staff (PT-BR), permitindo suporte global.
- **Tópicos Dedicados**: Cada chamado abre um tópico exclusivo no grupo de suporte para a equipe de atendimento.
- **Painel do Atendente**: Interface com respostas rápidas, variáveis dinâmicas (`{user}`, `{atendente}`) e encerramento de ticket.
- **Avaliação CSAT**: Sistema de estrelas após o atendimento para medir a satisfação do usuário.

### 🏰 Gestão de Reinos e Comunidades (Realms)
Ideal para redes de grupos que desejam compartilhar configurações e segurança.
- **Realms**: Interligue múltiplos grupos para compartilhar administradores e banimentos globais.
- **Configurações via Botões**: Menu `/config` completo para gerenciar todas as funções do grupo visualmente.

### 📝 Notas, FAQ e Inteligência Artificial
- **Sistema de Notas (#)**: Salve conteúdos com `/note <nome>` e acesse instantaneamente usando `#nome`.
- **FAQ Inteligente**: Respostas automáticas baseadas em palavras-chave e relevância por categoria.
- **IA Chatter**: Integração com IA para conversas naturais e suporte básico automatizado.

### 🎮 Engajamento e Utilidades
- **Ranking de Atividade**: Top 10 membros mais ativos do grupo (`/ranking`).
- **Diversão**: Jogos de sorte (`/roll`, `/dice`), Bola Mágica (`/8ball`), Piadas (`/joke`) e interações sociais (`/slap`, `/hug`).
- **Utilidades**: Tradutor direto (`/translate`), Busca no Google Maps (`/gmaps`), Consulta de ID (`/id`) e muito mais.

---

## 📊 Administração e Controle

- **Dashboard Pessoal**: `/dashboard` para ver perfil, estatísticas e trocar idioma.
- **Broadcast Global**: Envio de mensagens em massa para todos os usuários do bot (Super Admin).
- **Backup de Dados**: Exportação completa do banco de dados em formato JSON (`/backup`).
- **Logs de Auditoria**: Registro detalhado de ações administrativas em canais/tópicos dedicados.

---

## 🛠️ Arquitetura Modular (57 Plugins)

O bot é 100% modular, permitindo ativar ou desativar funções conforme a necessidade.
Lista completa de módulos ativos:
`about`, `admin`, `antispam`, `atendente`, `atendimento`, `backup`, `banhammer`, `block`, `broadcast`, `captcha`, `cats`, `chatter`, `chatter2`, `configure`, `dashboard`, `doacoes`, `donations`, `extra`, `faq`, `floodmanager`, `formatacao`, `formatting`, `fun`, `gmaps`, `groups`, `grupos`, `help`, `id`, `links`, `logchannel`, `mediasettings`, `menu`, `moderators`, `notes`, `onmessage`, `pin`, `private`, `private_settings`, `protection`, `ranking`, `ranking_data`, `realms`, `report`, `rules`, `search`, `service`, `setlang`, `sobre`, `sorteio`, `start`, `stats`, `support`, `tools`, `translate`, `users`, `warn`, `welcome`.

---

## ⚙️ Instalação e Execução

### Requisitos
- Python 3.10+
- PostgreSQL (Supabase recomendado)

### Configuração
1. Instale as dependências: `python install.py` ou `pip install -r requirements.txt`
2. Configure as chaves no arquivo `.env`.
3. Importe o esquema do banco de dados usando o arquivo `supabase_schema.sql`.
4. Inicie o bot: `python start.bat` (Windows) ou `python launch.py` (Linux).

---
## 📄 Licença
Este projeto está sob a licença MIT. Desenvolvido para **Segurança Privada**.
"# autoresponde-faq" 
