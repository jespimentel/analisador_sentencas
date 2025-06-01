# -*- coding: utf-8 -*-
# Script para baixar sentenças judiciais do site do TJSP

import requests
import time

MAX_INTERACOES = 520
path = 'data/raw/'

# -*- coding: utf-8 -*-
# Primeiro Grau
# Cria uma sessão persistente
session = requests.Session()

# 1a requisição para obter os cookies
url_inicial = "https://esaj.tjsp.jus.br/cjpg/pesquisar.do"

# Dicionário de parâmetros da requisição
params = {
    "conversationId": "",
    "dadosConsulta.pesquisaLivre": "tráfico",
    "tipoNumero": "UNIFICADO",
    "numeroDigitoAnoUnificado": "",
    "foroNumeroUnificado": "",
    "dadosConsulta.nuProcesso": "",
    "dadosConsulta.nuProcessoAntigo": "",
    "classeTreeSelection.values": "",
    "classeTreeSelection.text": "",
    "assuntoTreeSelection.values": "7961,3751,3370,3371,3372",
    "assuntoTreeSelection.text": "5 Registros selecionados",
    "agenteSelectedEntitiesList": "",
    "contadoragente": "0",
    "contadorMaioragente": "0",
    "cdAgente": "",
    "nmAgente": "",
    "dadosConsulta.dtInicio": "",
    "dadosConsulta.dtFim": "",
    "varasTreeSelection.values": "",
    "varasTreeSelection.text": "",
    "dadosConsulta.ordenacao": "DESC"
}

response = session.get(url_inicial, params=params)

if response.status_code == 200:
    for i in range(1, MAX_INTERACOES + 1):
        pagina = str(i)
        url_pagina = f"https://esaj.tjsp.jus.br/cjpg/trocarDePagina.do?pagina={pagina}&conversationId="

        # Usa a mesma sessão para fazer a requisição
        response = session.get(url_pagina)

        if response.status_code == 200:
            # Salva o conteúdo da página
            with open(f"{path}pagina_{pagina}.html", "wb") as file:
                file.write(response.content)
            print(f"Página {pagina} salva com sucesso.")
        else:
            print(f"Erro ao acessar a página {pagina}: {response.status_code}")

        # Intervalo entre requisições
        time.sleep(2)
else:
    print("Erro ao acessar a página inicial.")
    
# Fim do script