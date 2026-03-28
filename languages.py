import config

# Simulação do languages.lua para Python
def get_string(key, lang='pt_BR'):
    """Retorna uma string traduzida baseada na chave e idioma"""
    # Em uma versão real, carregaria dos arquivos .po/.mo
    strings = {
        'pt_BR': {
            'welcome': 'Bem-vindo ao bot!',
            'help': 'Aqui está a ajuda.'
        }
    }
    return strings.get(lang, strings['pt_BR']).get(key, key)
