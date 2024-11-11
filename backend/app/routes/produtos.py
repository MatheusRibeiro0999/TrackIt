from flask import Blueprint, request, jsonify
from app import db
from app.models import Produto  

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()  
    produtos_list = []
    for produto in produtos:
        produtos_list.append({
            'id': produto.id,
            'nome': produto.nome,
            'preco': produto.preco,
            'estoque': produto.estoque
        })
    return jsonify({'produtos': produtos_list})


@produtos_bp.route('/', methods=['POST'])
def criar_produto():
    dados = request.get_json()
    if not dados or not all(k in dados for k in ('nome', 'preco', 'estoque')):
        return jsonify({"mensagem": "Dados incompletos"}), 400
    
    novo_produto = Produto(
        nome=dados['nome'], 
        preco=dados['preco'], 
        estoque=dados['estoque']
    )
    db.session.add(novo_produto)
    db.session.commit()
    
    return jsonify({"mensagem": "Produto criado com sucesso", "produto": {'id': novo_produto.id}}), 201


@produtos_bp.route('/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.get_json()
    produto = Produto.query.get(id)
    
    if produto:
        produto.nome = dados['nome']
        produto.preco = dados['preco']
        produto.estoque = dados['estoque']
        
        db.session.commit()
        return jsonify({"mensagem": "Produto atualizado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Produto não encontrado"}), 404


@produtos_bp.route('/<int:id>', methods=['PATCH'])
def modificar_produto(id):
    dados = request.get_json()
    produto = Produto.query.get(id)
    
    if produto:
        if 'nome' in dados:
            produto.nome = dados['nome']
        if 'preco' in dados:
            produto.preco = dados['preco']
        if 'estoque' in dados:
            produto.estoque = dados['estoque']
        
        db.session.commit()
        return jsonify({"mensagem": "Dados do produto modificados com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Produto não encontrado"}), 404


@produtos_bp.route('/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get(id)
    
    if produto:
        db.session.delete(produto)
        db.session.commit()
        return jsonify({"mensagem": "Produto deletado com sucesso"}), 204
    else:
        return jsonify({"mensagem": "Produto não encontrado"}), 404

