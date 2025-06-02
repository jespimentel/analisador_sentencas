# -*- coding: utf-8 -*-
# Script para analisar sentenças judiciais utilizando a API do modelo de linguagem LiteLLM

import os
import sys
import pandas as pd
from litellm import completion
from dotenv import load_dotenv

# Adiciona o diretório do projeto ao sys.path para importar configurações
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root) 

from config.settings import PROCESSED_DATA_PATH, MODEL


load_dotenv()

path = PROCESSED_DATA_PATH
df = pd.read_csv(f"{path}/sentencas_tjsp.csv")

def analisar_sentenca_litellm(sentenca: str) -> dict:
    """
    Analisa uma sentença judicial utilizando a API do modelo de linguagem através do LiteLLM.

    Args:
        sentenca (str): O texto completo da sentença a ser analisada.
            
    Returns:
        dict: Um dicionário contendo as respostas para perguntas predefinidas.
              Em caso de erro em alguma pergunta, o valor correspondente será
              uma mensagem de erro.
    """
    
    # Lista de perguntas para extrair as informações da sentença
    perguntas = [
        # Pergunta 1: Nome(s) do(s) réu(s)
        "Informe o(s) nome(s) completo(s) do(s) réu(s) na sentença. Use o formato: Nome (para um réu) ou Nome1; Nome2; Nome3 (para múltiplos réus).",
        # Pergunta 2: Relação com o tráfico
        "A sentença menciona relação do réu ou réus com o tráfico de drogas? Responda com 'Sim' ou 'Não'.",
        # Pergunta 3: Especifica a relação com o tráfico?
        "Resuma, se for o caso, a relação do réu ou réus com o tráfico de drogas em até 50 palavras.",
        # Pergunta 4: Tipo de decisão
        "A decisão foi de pronúncia, impronúncia, absolvição, desclassificação, extinção da punibilidade, condenatória ou outras? Responda com apenas uma palavra:\
             pronúncia, impronúncia, absolvição, desclassificação, extinção da punibilidade, condenatória, outras. Havendo mais de um réu, responda, por exemplo: \
             pronúncia; absolvição; impronúncia (para múltiplos réus).",
        # Pergunta 5: Resumo da sentença
        "Resuma a sentença em até 50 palavras, focando nos principais pontos e decisões. Não inclua detalhes excessivos ou explicações adicionais.",
        # Pergunta 6: Penas
        "Quais foram as penas aplicadas ao réu ou réus? Liste as penas de forma clara e objetiva, separando por ponto e vírgula (;) se houver mais de um réu. \
            Se não houver penas, responda 'Sem penas aplicadas'."
    ]

    # Chaves do dicionário de saída (uma para cada pergunta)
    chaves_json = [
        "reus",
        "relacao_trafico_confirmacao",
        "resumo_relacao_trafico",
        "tipo_decisao",
        "resumo_sentenca",
        "penas_aplicadas"
    ]

    respostas_dict = {}
    respostas_coletadas = []

    system_message = "Você é um assistente jurídico especializado em analisar decisões judiciais. \
        Responda de forma clara, objetiva e no formato especificado. \
        **Não adicione explicações ou comentários extras.**"

    # Loop para processar cada pergunta
    for i, pergunta_especifica in enumerate(perguntas):
        
        prompt_usuario = f"""
        **Sentença:**
        \"\"\"
        {sentenca}
        \"\"\"

        **Pergunta:** {pergunta_especifica}

        **Resposta:**
        """

        resposta_api = None # Inicializa a variável de resposta
        try:
            response = completion(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt_usuario}
                ]
            )
            if response and response.choices and response.choices[0].message and response.choices[0].message.content:
                resposta_api = response.choices[0].message.content.strip()
            else:
                resposta_api = "Erro ao obter resposta da API."
                print(f"Resposta inesperada da API para a pergunta {i+1}: {response}")

        except Exception as e:
            # Captura outras exceções do LiteLLM ou erros gerais de processamento
            resposta_api = f"Exceção geral com o modelo {MODEL}."
            print(f"Exceção geral na pergunta {i+1} com o modelo {MODEL}: {e}")

        respostas_coletadas.append(resposta_api)

    # Monta o dicionário final de respostas
    for i in range(len(chaves_json)):
        respostas_dict[chaves_json[i]] = respostas_coletadas[i]

    return respostas_dict

resultados_api = []

for index, row in df.iterrows():
    numero_do_processo = row['numero_do_processo'] if 'numero_do_processo' in row else None
    comarca = row['comarca'] if 'comarca' in row else None
    foro = row['foro'] if 'foro' in row else None
    vara = row['vara'] if 'vara' in row else None
    data_disponibilizacao = row['data_disponibilização'] if 'data_disponibilização' in row else None
    texto_sentenca = row['sentença'] if 'sentença' in row else None 

    print(f"Analisando a sentença do processo nº {numero_do_processo}. Aguarde...") 
    
    try:
        retorno_api = analisar_sentenca_litellm(texto_sentenca)
        retorno_api['numero_do_processo'] = numero_do_processo
        retorno_api['comarca'] = comarca
        retorno_api['foro'] = foro
        retorno_api['vara'] = vara
        retorno_api['data_disponibilizacao'] = data_disponibilizacao

        resultados_api.append(retorno_api)
        
    except Exception as e:
        print(f"Erro ao processar '{numero_do_processo}...': {e}")
        resultados_api.append({
            'numero_do_processo': numero_do_processo,
            'reus': "Erro ao processar",
            'relacao_trafico_confirmacao': "Erro ao processar",
            'resumo_relacao_trafico': "Erro ao processar",
            'tipo_decisao': "Erro ao processar",
            'resumo_sentenca': "Erro ao processar",
            'penas_aplicadas': "Erro ao processar"
        })
# Salva os resultados em um DataFrame
resultados_df = pd.DataFrame(resultados_api)

colunas_ordenadas = [
    'numero_do_processo',
    'comarca',
    'foro',
    'vara',
    'data_disponibilizacao',
    'tipo_decisao',
    'relacao_trafico_confirmacao',
    'resumo_relacao_trafico',
    'resumo_sentenca',
    'reus',
    'penas_aplicadas', 
]

# Reordena as colunas do DataFrame
resultados_df = resultados_df[colunas_ordenadas]

# Salva o DataFrame em um arquivo CSV
resultados_df.to_csv(f"{path}/analise_sentencas.csv", index=False)

print("\nAnálise concluída. Resultados salvos em 'analise_sentencas_tjsp.csv'.")
print(f"Total de sentenças processadas: {len(resultados_df)}")

# Fim do script