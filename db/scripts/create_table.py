import os
import random
from datetime import datetime

import mysql.connector
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("host"),
    password=os.getenv("password"),
    port=os.getenv("port"),
    user=os.getenv("user"),
    database=os.getenv("database"),
)

cursor = conn.cursor()


cursor.execute(
    """
CREATE TABLE IF NOT EXISTS clientes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    cpf VARCHAR(11),
    email VARCHAR(100)
)"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS enderecos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    rua VARCHAR(100),
    estado VARCHAR(30),
    cidade VARCHAR(30),
    cep VARCHAR(30),
    FOREIGN KEY(client_id) REFERENCES clientes(id)
)"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS pagamentos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    valor DECIMAL(10, 2),
    data_pagamento DATE,
    FOREIGN KEY(client_id) REFERENCES clientes(id)
)"""
)


cursor.execute(
    """
CREATE TABLE IF NOT EXISTS movimentacoes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    tipo_movimentacao VARCHAR(20),
    valor DECIMAL(10, 2),
    data_movimentacao DATE,
    FOREIGN KEY(client_id) REFERENCES clientes(id)
)"""
)

fake = Faker()

for i in range(50):
    nome = fake.name()
    cpf = str(random.randint(11111111111, 99999999999))
    email = fake.email()

    rua = fake.street_address()
    cidade = fake.city()
    estado = fake.state()
    cep = fake.zipcode()

    tipo_movimentacao = random.choice(
        ["trasferencia", "deposito", "saque", "credito", "emprestimo"]
    )
    valor_movimentacao = round(random.uniform(50.0, 1000000000.0), 2)
    data_movimentacao = fake.date_this_year()

    valor_pagamento = round(random.uniform(50.0, 1000000000.0), 2)
    data_pagamento = fake.date_this_year()

    cursor.execute(
        """
        INSERT INTO clientes (nome, cpf,  email) 
                values( %s, %s, %s)
    """,
        (nome, cpf, email),
    )

    cliente_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO enderecos (client_id, rua, estado, cidade, cep) 
                values( %s, %s, %s, %s, %s)
    """,
        (cliente_id, rua, estado, cidade, cep),
    )

    cursor.execute(
        """
        INSERT INTO pagamentos (client_id, valor, data_pagamento) 
                values( %s, %s, %s)
    """,
        (cliente_id, valor_pagamento, data_pagamento),
    )

    cursor.execute(
        """
        INSERT INTO movimentacoes (client_id, tipo_movimentacao, valor, data_movimentacao) 
                values( %s, %s, %s, %s)
    """,
        (cliente_id, tipo_movimentacao, valor_movimentacao, data_movimentacao),
    )


conn.commit()
