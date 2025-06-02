# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import os
import sys

# Adiciona o diretório do projeto ao sys.path para importar configurações
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root) 

from config.settings import PROCESSED_DATA_PATH, MODEL

# Define a data atual para o rodapé do relatório
date_now = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

df = pd.read_csv(PROCESSED_DATA_PATH + '/analise_sentencas.csv')

def gerar_relatorio_markdown(df: pd.DataFrame) -> None:
    """
    Gera um relatório formatado em Markdown a partir de um DataFrame.

    Args:
        df (pd.DataFrame): O DataFrame a ser analisado.
        
    """
    if df.empty:
        print("O DataFrame está vazio. Nenhum relatório Markdown pode ser gerado.")
        return
    
    nome_arquivo = PROCESSED_DATA_PATH +'/relatorio_' + date_now + '.md'

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("# Analisador de Sentenças\n\n") 
        f.write(f"**Análise automatizada de Sentenças com a API do {MODEL}.**\n\n")
        f.write(f"**Código-fonte:** https://github.com/jespimentel/analisador_sentencas\n\n") 
        f.write(f"**Data de geração:** {date_now}\n\n") 
        f.write("--- \n\n") 
        f.write("## Detalhes dos Processos\n\n") 

        for row in df.itertuples(index=False):  
            f.write(f"## Processo: {row.numero_do_processo}\n\n")
            f.write(f"**Comarca:** {row.comarca}  |  **Foro:** {row.foro}  |  **Vara:** {row.vara}\n\n")
            f.write(f"**Data de disponibilização:** {row.data_disponibilizacao}\n\n")
            f.write(f"**Tipo de Decisão:** {row.tipo_decisao}\n\n") 
            f.write(f"**Réu(s):** {row.reus}\n\n")
            f.write(f"**Resumo da Sentença:** {row.resumo_sentenca}\n\n")
            f.write(f"**Penas Aplicadas:** {row.penas_aplicadas}\n\n")
            f.write(f"**Relação de Tráfico e Confirmação:** {row.relacao_trafico_confirmacao}\n\n")
            f.write(f"**Resumo da Relação de Tráfico:** {row.resumo_relacao_trafico}\n\n")
            
            f.write("--- \n\n")
        # Resumo da análise
        f.write("--- \n\n")
        f.write("## Resumo da análise\n\n") 
        f.write(f"**Total de registros:** {len(df)}\n")

    print(f"Relatório Markdown gerado com sucesso em '{nome_arquivo}'.")

gerar_relatorio_markdown(df)

# Fim do script