# -*- coding: utf-8 -*-
# Script para baixar sentenças judiciais do site do TJSP
import requests
import time
import sys
import os

# Adiciona o diretório do projeto ao sys.path para importar configurações
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root) 

from config.settings import URL_TJSP, PARAMS_TJSP, PATH_SENTENCES, MAX_INTERACOES

path = PATH_SENTENCES

# Cria uma sessão persistente
session = requests.Session()

# 1a requisição para obter os cookies
url_inicial = URL_TJSP

# Dicionário de parâmetros da requisição
params = PARAMS_TJSP

response = session.get(url_inicial, params=params)

if response.status_code == 200:
    for i in range(1, MAX_INTERACOES + 1):
        pagina = str(i)
        url_pagina = f"https://esaj.tjsp.jus.br/cjpg/trocarDePagina.do?pagina={pagina}&conversationId="

        # Usa a mesma sessão para fazer a requisição
        response = session.get(url_pagina)

        if response.status_code == 200:
            # Salva o conteúdo da página
            with open(f"{path}/pagina_{pagina}.html", "wb") as file:
                file.write(response.content)
            print(f"Página {pagina} salva com sucesso.")
        else:
            print(f"Erro ao acessar a página {pagina}: {response.status_code}")

        # Intervalo entre requisições
        time.sleep(2)
else:
    print("Erro ao acessar a página inicial.")
    
# Fim do script