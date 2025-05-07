# nlp-symbolic-solution

O objetivo desse projeto é, além de reforçar os aprendizados da disciplina _SCC0633/SCC5908 - Processamento de Linguagem Natural_ da Universidade de São Paulo, fornecer uma nova maneira de receber insights sobre um filme: a partir da análise de sentimentos dos comentários do Letterboxd.

## Sobre o repositório
O projeto tem diversos arquivos `main_*.py`. Segue uma descrição de cada um, além de um notebook:
- `main_analysis.py`: ele calcula a acurácia a nível de comentário de diversos filmes a partir do arquivo `all_comments.csv` gerado pelo `main_make_database.py`
- `main_make_database.py`: usado para criar um grande dataset de comentários de diversos filmes a partir de web scraping dos filmes contidos em `data/movies.txt`
- `main_sentiment.py`: pode ser considerado o pontapé do trabalho. Ele faz a análise de sentimentos dos comentários de um único filme e avalia sua performance.
- `main_site.py`: usado para executar o site criado com Streamlit. Fornece uma interface gráfica em que usuários podem pedir uma análise de um filme, ou seja, vendo se ele é recomendado ou não e vendo quantos comentários são positivos, negativos ou neutros.
- `analysis_notebook.ipynb`: utilizado para analisar a acurácia a nível de recomendação do filme e o efeito da mudança de threshold.

O arquivo de dicionário em português brasileiro utilizado ao longo do trabalho foi fornecido a pedido e não foi permitido o compartilhamento dele neste repositório.

## Como executar:
```
cd symbolic

# Executar o main_analysis:
python3 ./src/symbolic/main_analysis.py

# Executar o main_make_database:
python3 ./src/symbolic/main_make_database.py

# Executar o main_sentiment:
python3 ./src/symbolic/main_sentiment.py

# Executar o main_site:
python3 -m streamlit run ./src/symbolic/main_site.py
```