# -*- coding: utf-8 -*-

# CONFIGURAÇÕES DA APLICAÇÃO

URL_TJSP = "https://esaj.tjsp.jus.br/cjpg/pesquisar.do"

PARAMS_TJSP = {
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

PATH_SENTENCES = "data/raw"

MAX_INTERACOES = 520

PROCESSED_DATA_PATH = "data/processed"

CSV_SENTENCES = 'data/processed/sentencas_tjsp.csv'

# MODEL = 'gpt-4o-mini'  
# MODEL = "deepseek/deepseek-chat"
MODEL = "gemini/gemini-2.0-flash-lite"
