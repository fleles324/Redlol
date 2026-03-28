-- ==========================================================
-- 📚 EXEMPLO DE DADOS PARA O FAQ - SEGURANÇA PRIVADA (SUPABASE)
-- ==========================================================

-- 1. Inserir dados na tabela faqs
-- Use topic_id para responder automaticamente a perguntas específicas
-- Use keywords para busca por relevância inteligente

INSERT INTO public.faqs (topic_id, category, keywords, answer, active)
VALUES 
    ('788', 'Suporte Técnico', ARRAY['conectar', 'chatgpt', 'regra', 'instalação'], 'Para conectar seu ChatGPT em uma regra, siga os passos:\n\n1. Acesse o menu `/atendimento`.\n2. Escolha a opção de "Configurações Extras".\n3. Insira sua API Key do OpenAI conforme as instruções.', TRUE),
    ('788', 'Pagamentos', ARRAY['preço', 'valor', 'pix', 'cartão'], 'Atualmente aceitamos pagamentos via PIX e Cartão de Crédito. Para consultar os valores atualizados, use o comando `/preco` ou fale com um atendente.', TRUE),
    ('788', 'Geral', ARRAY['ajuda', 'socorro', 'comandos', 'bot'], 'Eu sou um bot de segurança e suporte! Você pode ver todos os meus comandos usando `/help` ou iniciar um atendimento privado com `/atendimento`.', TRUE),
    ('788', 'Segurança', ARRAY['ban', 'warn', 'regras', 'spam'], 'Nossas regras de segurança proíbem spam e flood. Se você for advertido 3 vezes com `/warn`, será banido automaticamente pelo sistema.', TRUE);

-- 2. Inserir Respostas Rápidas iniciais (Extras)
-- chat_id 0 = Global para respostas rápidas
INSERT INTO public.chat_extras (chat_id, command, response)
VALUES 
    (0, 'qr:tchau', '*{user}*, foi um prazer te atender! Se precisar de algo mais, é só chamar. Meu nome é **{atendente}** e estarei aqui para ajudar.'),
    (0, 'qr:bemvindo', 'Olá *{user}*! Bem-vindo ao suporte da Segurança Privada. Como posso ser útil hoje?'),
    (0, 'qr:aguarde', 'Por favor, aguarde um momento enquanto verifico suas informações no sistema...');
