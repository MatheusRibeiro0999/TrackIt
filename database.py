import sqlite3
from datetime import datetime

def conectar_banco():
    return sqlite3.connect('produtos.db')

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            produto TEXT,
            quantidade INTEGER,
            categoria TEXT,
            data_hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

def inserir_venda(cliente, produto, quantidade, categoria):
    conn = conectar_banco()
    cursor = conn.cursor()
    data_hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO vendas (cliente, produto, quantidade, categoria, data_hora)
        VALUES (?, ?, ?, ?, ?)
    ''', (cliente, produto, quantidade, categoria, data_hora_atual))
    conn.commit()
    conn.close()
