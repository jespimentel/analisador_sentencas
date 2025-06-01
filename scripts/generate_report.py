import pandas as pd
import datetime

# Define a data atual para o rodapé do relatório
date_now = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

df = pd.read_csv(r'data\processed\analise_sentencas.csv')

def gerar_relatorio_markdown(df: pd.DataFrame, nome_arquivo: str, modelo = "gemini/gemini-2.0-flash-lite") -> None:
    """
    Gera um relatório formatado em Markdown a partir de um DataFrame.

    Args:
        df (pd.DataFrame): O DataFrame a ser analisado.
        nome_arquivo (str): O nome do arquivo onde o relatório Markdown será salvo.
    """
    if df.empty:
        print("O DataFrame está vazio. Nenhum relatório Markdown pode ser gerado.")
        return

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("# Analisador de Sentenças\n\n") 
        f.write(f"**Análise automatizada de Sentenças com a API do {modelo}.**\n\n")
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

gerar_relatorio_markdown(df, r'data\processed\relatorio.md', 'deepseek/deepseek-chat')