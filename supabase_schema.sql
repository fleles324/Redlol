-- ==========================================================
-- 🛠️ ESQUEMA COMPLETO DO BANCO DE DADOS - SEGURANÇA PRIVADA (SUPABASE)
-- v4.5.0 - Atualizado com Notas, CAPTCHA e Warns Detalhados
-- ==========================================================

-- 1. Tabela de Usuários (Estatísticas e Identificação)
CREATE TABLE IF NOT EXISTS public.users (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    msg_count BIGINT DEFAULT 0,
    language TEXT DEFAULT 'pt_BR',
    is_banned BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE
);

-- 2. Tabela de Configurações de Chat (Grupos e Canais)
CREATE TABLE IF NOT EXISTS public.chat_settings (
    chat_id BIGINT PRIMARY KEY,
    title TEXT,
    language TEXT DEFAULT 'pt_BR',
    settings JSONB DEFAULT '{"Welcome": "off", "Rules": "off", "Captcha": "off", "Goodbye": "off"}'::jsonb,
    antispam JSONB DEFAULT '{"links": "off", "forwards": "off", "antibot": "off"}'::jsonb,
    flood JSONB DEFAULT '{"MaxFlood": 5, "ActionFlood": "kick"}'::jsonb,
    media JSONB DEFAULT '{"photo": "on", "video": "on", "audio": "on", "sticker": "on", "gif": "on", "url": "on"}'::jsonb,
    realm_id BIGINT, -- ID do Reino ao qual o chat pertence
    log_channel_id BIGINT, -- ID do canal de logs específico do grupo
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Tabela de Tickets e Fila de Suporte
CREATE TABLE IF NOT EXISTS public.tickets (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    user_name TEXT,
    thread_id BIGINT,
    status TEXT DEFAULT 'pending', -- 'pending', 'open', 'closed'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    closed_at TIMESTAMP WITH TIME ZONE,
    staff_id BIGINT,
    staff_name TEXT,
    language TEXT
);

-- 4. Tabela de Avaliações (CSAT e Métricas de Atendimento)
CREATE TABLE IF NOT EXISTS public.ratings (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    score INT NOT NULL, -- 1 a 5 (CSAT)
    staff_id BIGINT,
    staff_name TEXT,
    ticket_id BIGINT REFERENCES public.tickets(id),
    nps_score INT, -- 0 a 10
    frt_seconds INT, -- First Response Time em segundos
    fcr BOOLEAN DEFAULT TRUE, -- First Contact Resolution
    aht_seconds INT, -- Average Handle Time em segundos
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Tabela de FAQ (Auto-Responder Inteligente)
CREATE TABLE IF NOT EXISTS public.faqs (
    id BIGSERIAL PRIMARY KEY,
    topic_id TEXT, -- ID do tópico para resposta automática (ex: 788)
    category TEXT,
    keywords TEXT[], -- Array de palavras-chave para busca por relevância
    answer TEXT,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Tabela de Extras e Respostas Rápidas (Notas)
-- Usada para /note, #hashtags e qr:responses
CREATE TABLE IF NOT EXISTS public.chat_extras (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT DEFAULT 0, -- 0 para Global, ID específico para notas de grupo
    command TEXT, -- Ex: qr:tchau ou note:regras ou #ajuda
    response TEXT,
    media_id TEXT, -- Para notas que contêm fotos/vídeos (file_id do Telegram)
    media_type TEXT, -- photo, video, document, etc.
    created_by BIGINT, -- ID do usuário que criou a nota
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_chat_extras_chat_command ON public.chat_extras(chat_id, command);

-- 7. Tabela de Warns (Avisos Detalhados)
CREATE TABLE IF NOT EXISTS public.warns (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    reason TEXT DEFAULT 'Sem motivo especificado',
    admin_id BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_warns_chat_user ON public.warns(chat_id, user_id);

-- 8. Tabela de Reinos (Realms - Grupos Interligados)
CREATE TABLE IF NOT EXISTS public.realms (
    realm_id BIGINT PRIMARY KEY,
    realm_name TEXT,
    owner_id BIGINT REFERENCES public.users(user_id),
    settings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 9. Tabela de Estatísticas Globais e Bloqueios
CREATE TABLE IF NOT EXISTS public.bot_stats (
    stat_name TEXT PRIMARY KEY, -- Ex: total_messages, blocked:12345
    stat_value BIGINT DEFAULT 0,
    stat_value_text TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 10. Tabela de Sorteios (Giveaways)
CREATE TABLE IF NOT EXISTS public.giveaways (
    id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL,
    message_id BIGINT,
    prize TEXT NOT NULL,
    winners_count INTEGER DEFAULT 1,
    end_at TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'active', -- active, finished, cancelled
    participants BIGINT[] DEFAULT '{}', -- Array de IDs de usuários
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ==========================================================
-- 🔒 POLÍTICAS DE SEGURANÇA (RLS)
-- ==========================================================

-- Habilitar RLS em todas as tabelas
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tickets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ratings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.faqs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_extras ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.warns ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.realms ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bot_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.giveaways ENABLE ROW LEVEL SECURITY;

-- Criar política para permitir acesso total do Bot (Anon Key)
-- Nota: Em produção real, você restringiria isso, mas para bots de Telegram via Supabase SDK é o padrão comum.
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Acesso Total Anon') THEN
        CREATE POLICY "Acesso Total Anon" ON public.users FOR ALL USING (true);
        CREATE POLICY "Acesso Total Anon" ON public.chat_settings FOR ALL USING (true);
        CREATE POLICY "Acesso Total Anon" ON public.tickets FOR ALL USING (true);
        CREATE POLICY "Acesso Total Anon" ON public.ratings FOR ALL USING (true);
        CREATE POLICY "Acesso Total Anon" ON public.faqs FOR ALL USING (true);
        CREATE POLICY "Acesso Total Anon" ON public.chat_extras FOR ALL USING (true);
        CREATE POLICY "Acesso Total Anon" ON public.warns FOR ALL USING (true);
        CREATE POLICY "Acesso Total Anon" ON public.realms FOR ALL USING (true);
        CREATE POLICY "Acesso Total Anon" ON public.bot_stats FOR ALL USING (true);
        CREATE POLICY "Acesso Total Anon" ON public.giveaways FOR ALL USING (true);
    END IF;
END $$;

-- ==========================================================
-- 📦 DADOS INICIAIS E CONFIGURAÇÕES GLOBAIS
-- ==========================================================

-- Inserir registro global para respostas rápidas e configurações padrão
INSERT INTO public.chat_settings (chat_id, title, language) 
VALUES (0, 'Global Settings', 'pt_BR') 
ON CONFLICT (chat_id) DO NOTHING;

-- Exemplo de Respostas Rápidas Globais
INSERT INTO public.chat_extras (chat_id, command, response)
VALUES 
    (0, 'qr:bemvindo', 'Olá *{user}*! Bem-vindo ao suporte da Segurança Privada. Como posso ser útil hoje?'),
    (0, 'qr:tchau', '*{user}*, foi um prazer te atender! Se precisar de algo mais, é só chamar. Meu nome é **{atendente}**.'),
    (0, 'qr:aguarde', 'Por favor, aguarde um momento enquanto verifico suas informações no sistema...')
ON CONFLICT DO NOTHING;
