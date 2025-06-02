# analisador_sentencas

Análise massiva de sentenças judiciais com IA Gen, via LiteLLM.

---

### Bibliotecas necessárias
pip install pandas litellm python-dotenv beautifulsoup4 requests

---

### Uso
1. Baixe as sentenças com **download_sentences.py** (selecione os parâmetros de pesquisa no código);
1. Crie o dataframe de sentenças baixadas e salve em arquivo "csv" com **create_csv.py**;
1. Recupere o dataframe e analise as sentenças com **call_api.py**. O resultado estará disponível em novo arquivo "csv".
1. Gere um relatório formatado com **generate_report.py**.

---
