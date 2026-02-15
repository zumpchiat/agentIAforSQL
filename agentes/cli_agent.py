import os

import mysql.connector
import openai
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("host"),
    password=os.getenv("password"),
    port=os.getenv("port"),
    user=os.getenv("user"),
    database=os.getenv("database"),
)

cursor = conn.cursor()

cursor.execute("show tables")

tabelas = cursor.fetchall()
colunas = {}

for tabela in tabelas:
    cursor.execute(f"DESCRIBE {tabela[0]};")
    colunas_tabelas = cursor.fetchall()
    colunas[tabela[0]] = [coluna[0] for coluna in colunas_tabelas]

cursor.close()

conn.close()

prompt = f"""
    vocẽ é um assistente de SQL que opera para o banco de dados sql5817166.
    voce deve responder em sql formatado em uma unica linha pronto para executar no banco de dados
    voce deve gerar queries baseadas na seguinte estrutura do banco {colunas}

    pergunta: {input("Faça a sua pergunta: ")}

    resposta em SQL:
"""
openai.api_key = os.getenv("OPEN_AI_KEY")

reponse = openai.responses.create(
    model="gpt-4.1",
    input=[
        {"role": "system", "content": "voce é um assistente de SQL"},
        {"role": "user", "content": prompt},
    ],
)

print(reponse)
