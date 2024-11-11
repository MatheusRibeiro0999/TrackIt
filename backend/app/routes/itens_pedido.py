from flask import Blueprint, request, jsonify
from app import db
from app.models import ItemPedido  

itens_pedido_bp = Blueprint('itens_pedido', __name__)

@itens_pedido_bp.route('/', methods=['GET'])
def listar_itens_pedido():
    itens = ItemPedido.query.all()   
    itens_list = []
    for item in itens:
        itens_list.append({
            'id': item.id,
            'pedido_id': item.pedido_id,
            'produto_id': item.produto_id,
            'quantidade': item.quantidade,
            'preco': item.preco
        })
    return jsonify({'itens_pedido': itens_list})

@itens_pedido_bp.route('/', methods=['POST'])
def criar_item_pedido():
    dados = request.get_json()
    
    if not dados or not all(k in dados for k in ('pedido_id', 'produto_id', 'quantidade', 'preco')):
        return jsonify({"mensagem": "Dados incompletos"}), 400
    
    novo_item_pedido = ItemPedido(
        pedido_id=dados['pedido_id'], 
        produto_id=dados['produto_id'], 
        quantidade=dados['quantidade'], 
        preco=dados['preco']
    )
    
    db.session.add(novo_item_pedido)
    db.session.commit()
    
    return jsonify({"mensagem": "Item de pedido criado com sucesso", "item_pedido": {'id': novo_item_pedido.id}}), 201

@itens_pedido_bp.route('/<int:id>', methods=['PUT'])
def atualizar_item_pedido(id):
    dados = request.get_json()
    item = ItemPedido.query.get(id)
    
    if item:
        item.pedido_id = dados['pedido_id']
        item.produto_id = dados['produto_id']
        item.quantidade = dados['quantidade']
        item.preco = dados['preco']
        
        db.session.commit()
        return jsonify({"mensagem": "Item de pedido atualizado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Item de pedido não encontrado"}), 404

@itens_pedido_bp.route('/<int:id>', methods=['PATCH'])
def modificar_item_pedido(id):
    dados = request.get_json()
    item = ItemPedido.query.get(id)
    
    if item:
        if 'pedido_id' in dados:
            item.pedido_id = dados['pedido_id']
        if 'produto_id' in dados:
            item.produto_id = dados['produto_id']
        if 'quantidade' in dados:
            item.quantidade = dados['quantidade']
        if 'preco' in dados:
            item.preco = dados['preco']
        
        db.session.commit()
        return jsonify({"mensagem": "Item de pedido modificado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Item de pedido não encontrado"}), 404

@itens_pedido_bp.route('/<int:id>', methods=['DELETE'])
def deletar_item_pedido(id):
    item = ItemPedido.query.get(id)
    
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"mensagem": "Item de pedido deletado com sucesso"}), 204
    else:
        return jsonify({"mensagem": "Item de pedido não encontrado"}), 404
