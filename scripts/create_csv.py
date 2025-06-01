# -*- coding: utf-8 -*-
# Script para extrair informações de sentenças a partir de arquivos HTML baixados do site do TJSP

import pandas as pd
import os
from bs4 import BeautifulSoup

# Diretório contendo os arquivos HTML
directory = 'data/raw/'

data = []

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding='utf-8') as f:  # encoding para lidar com caracteres especiais
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")

        for result in soup.find_all("div", id="divDadosResultado"):
            for row in result.find_all("tr", class_="fundocinza1"):
                item = {}

                processo_link = row.find("a", title="Visualizar Inteiro Teor")
                if processo_link:
                    item["numero_do_processo"] = processo_link.find("span", class_="fonteNegrito").text.strip()
                else:
                    item["numero_do_processo"] = None

                table_data = row.find_all("td")
                if len(table_data) > 1:
                    info_table = table_data[1].find('table')
                    if info_table: # Verifica se a tabela de informações existe
                        for info_row in info_table.find_all("tr", class_="fonte"):
                            cells = info_row.find_all("td")
                            if cells:
                                if cells[0].strong:
                                    key = cells[0].strong.text.strip().replace(":", "")
                                    value = cells[0].text.replace(cells[0].strong.text,"").strip() if len(cells) == 1 else cells[1].text.strip()
                                    if key.lower() not in ["data de disponibilização"]:
                                        item[key.lower()] = value
                                    else:
                                        item['data_disponibilização'] = value
                            else:
                                pass  # Ou adicione um valor padrão se necessário

                else:
                    # Define valores padrão se não houver informações adicionais
                    item['classe'] = None
                    item['assunto'] = None
                    item['magistrado'] = None
                    item['comarca'] = None
                    item['foro'] = None
                    item['vara'] = None
                    item['data_disponibilização'] = None

                sentenca_divs = table_data[1].find_all("div", align="justify") if len(table_data) > 1 else [] # Lidar com casos onde table_data tem apenas um elemento
                full_text = ""
                for div in sentenca_divs:
                    text = div.get_text(strip=True)
                    full_text += text + '\n'
                item["sentença"] = full_text

                data.append(item)

df = pd.DataFrame(data)

# Ordenando as colunas
df = df[['numero_do_processo', 'classe', 'assunto', 'magistrado', 'comarca', 'foro', 'vara', 'data_disponibilização', 'sentença']]

print(df.sample(5))
print(f"Total de sentenças extraídas: {len(df)}")

# Salvando o DataFrame em um arquivo CSV
output_path = 'data/processed/sentencas_tjsp.csv'
df.to_csv(output_path, index=False, encoding='utf-8-sig')  # Usando utf-8-sig para compatibilidade com Excel
print(f"Arquivo CSV salvo em: {output_path}")

# Fim do script