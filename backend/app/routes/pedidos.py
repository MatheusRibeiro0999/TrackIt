from flask import Blueprint, request, jsonify
from app import db
from app.models import Pedido  

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/', methods=['GET'])
def listar_pedidos():
    pedidos = Pedido.query.all()  
    pedidos_list = []
    for pedido in pedidos:
        pedidos_list.append({
            'id': pedido.id,
            'cliente_id': pedido.cliente_id,
            'data_pedido': pedido.data_pedido,
            'status': pedido.status
        })
    return jsonify({'pedidos': pedidos_list})


@pedidos_bp.route('/', methods=['POST'])
def criar_pedido():
    dados = request.get_json()
    
    if not dados or not all(k in dados for k in ('cliente_id', 'data_pedido', 'status')):
        return jsonify({"mensagem": "Dados incompletos"}), 400
    
    novo_pedido = Pedido(
        cliente_id=dados['cliente_id'], 
        data_pedido=dados['data_pedido'], 
        status=dados['status']
    )
    
    db.session.add(novo_pedido)
    db.session.commit()
    
    return jsonify({"mensagem": "Pedido criado com sucesso", "pedido": {'id': novo_pedido.id}}), 201


@pedidos_bp.route('/<int:id>', methods=['PUT'])
def atualizar_pedido(id):
    dados = request.get_json()
    pedido = Pedido.query.get(id)
    
    if pedido:
        pedido.cliente_id = dados['cliente_id']
        pedido.data_pedido = dados['data_pedido']
        pedido.status = dados['status']
        
        db.session.commit()
        return jsonify({"mensagem": "Pedido atualizado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Pedido não encontrado"}), 404


@pedidos_bp.route('/<int:id>', methods=['PATCH'])
def modificar_pedido(id):
    dados = request.get_json()
    pedido = Pedido.query.get(id)
    
    if pedido:
        if 'cliente_id' in dados:
            pedido.cliente_id = dados['cliente_id']
        if 'data_pedido' in dados:
            pedido.data_pedido = dados['data_pedido']
        if 'status' in dados:
            pedido.status = dados['status']
        
        db.session.commit()
        return jsonify({"mensagem": "Pedido modificado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Pedido não encontrado"}), 404


@pedidos_bp.route('/<int:id>', methods=['DELETE'])
def deletar_pedido(id):
    pedido = Pedido.query.get(id)
    
    if pedido:
        db.session.delete(pedido)
        db.session.commit()
        return jsonify({"mensagem": "Pedido deletado com sucesso"}), 204
    else:
        return jsonify({"mensagem": "Pedido não encontrado"}), 404
