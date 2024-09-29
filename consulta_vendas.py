import sqlite3
from tkinter import *
from tkinter import ttk

# Função para realizar a consulta
def consultar_dados():
    cliente = entry_cliente.get()
    produto = entry_produto.get()

    query = "SELECT * FROM vendas WHERE 1=1"
    params = []

    if cliente:
        query += " AND cliente = ?"
        params.append(cliente)
    
    if produto:
        query += " AND produto = ?"
        params.append(produto)

    cursor.execute(query, params)
    resultados = cursor.fetchall()

    # Limpando a tabela antes de mostrar os resultados
    for row in tree.get_children():
        tree.delete(row)

    if resultados:
        for row in resultados:
            tree.insert("", "end", values=row)
        label_status['text'] = f"{len(resultados)} resultado(s) encontrado(s)."
    else:
        label_status['text'] = "Nenhum resultado encontrado."

# Conectando ao banco de dados
conexao = sqlite3.connect('produtos.db')
cursor = conexao.cursor()

# Interface gráfica
root = Tk()
root.title("Consulta de Vendas")

# Labels e Entradas
Label(root, text="Cliente").grid(row=0, column=0)
entry_cliente = Entry(root)
entry_cliente.grid(row=0, column=1)

Label(root, text="Produto").grid(row=1, column=0)
entry_produto = Entry(root)
entry_produto.grid(row=1, column=1)

# Botão para consultar
btn_consultar = Button(root, text="Consultar", command=consultar_dados)
btn_consultar.grid(row=2, column=0, columnspan=2)

# Tabela para mostrar os resultados
tree = ttk.Treeview(root, columns=("ID", "Cliente", "Produto", "Quantidade", "Categoria", "Data e Hora"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Cliente", text="Cliente")
tree.heading("Produto", text="Produto")
tree.heading("Quantidade", text="Quantidade")
tree.heading("Categoria", text="Categoria")
tree.heading("Data e Hora", text="Data e Hora")
tree.grid(row=3, column=0, columnspan=2)

# Status label
label_status = Label(root, text="")
label_status.grid(row=4, column=0, columnspan=2)

# Rodando o loop da interface
root.mainloop()

# Fechando a conexão com o banco de dados ao fechar o programa
conexao.close()
