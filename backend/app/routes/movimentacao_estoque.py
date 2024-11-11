from flask import Blueprint, request, jsonify
from app import db
from app.models import MovimentacaoEstoque

movimentacao_estoque_bp = Blueprint('movimentacao_estoque', __name__)

@movimentacao_estoque_bp.route('/', methods=['GET'])
def listar_movimentacoes():
    movimentacoes = MovimentacaoEstoque.query.all()  
    movimentacoes_list = []
    for movimentacao in movimentacoes:
        movimentacoes_list.append({
            'id': movimentacao.id,
            'produto_id': movimentacao.produto_id,
            'quantidade': movimentacao.quantidade,
            'tipo': movimentacao.tipo
        })
    return jsonify({'movimentacoes': movimentacoes_list})


@movimentacao_estoque_bp.route('/', methods=['POST'])
def criar_movimentacao():
    dados = request.get_json()
    if not dados or not all(k in dados for k in ('produto_id', 'quantidade', 'tipo')):
        return jsonify({"mensagem": "Dados incompletos"}), 400
    
    nova_movimentacao = MovimentacaoEstoque(
        produto_id=dados['produto_id'], 
        quantidade=dados['quantidade'], 
        tipo=dados['tipo']
    )
    
    db.session.add(nova_movimentacao)
    db.session.commit()
    
    return jsonify({"mensagem": "Movimentação criada com sucesso", "movimentacao": {'id': nova_movimentacao.id}}), 201


@movimentacao_estoque_bp.route('/<int:id>', methods=['PUT'])
def atualizar_movimentacao(id):
    dados = request.get_json()
    movimentacao = MovimentacaoEstoque.query.get(id)
    
    if movimentacao:
        movimentacao.produto_id = dados['produto_id']
        movimentacao.quantidade = dados['quantidade']
        movimentacao.tipo = dados['tipo']
        
        db.session.commit()
        return jsonify({"mensagem": "Movimentação de estoque atualizada com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Movimentação não encontrada"}), 404


@movimentacao_estoque_bp.route('/<int:id>', methods=['PATCH'])
def modificar_movimentacao(id):
    dados = request.get_json()
    movimentacao = MovimentacaoEstoque.query.get(id)
    
    if movimentacao:
        if 'produto_id' in dados:
            movimentacao.produto_id = dados['produto_id']
        if 'quantidade' in dados:
            movimentacao.quantidade = dados['quantidade']
        if 'tipo' in dados:
            movimentacao.tipo = dados['tipo']
        
        db.session.commit()
        return jsonify({"mensagem": "Dados da movimentação de estoque modificados com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Movimentação não encontrada"}), 404


@movimentacao_estoque_bp.route('/<int:id>', methods=['DELETE'])
def deletar_movimentacao(id):
    movimentacao = MovimentacaoEstoque.query.get(id)
    
    if movimentacao:
        db.session.delete(movimentacao)
        db.session.commit()
        return jsonify({"mensagem": "Movimentação de estoque deletada com sucesso"}), 204
    else:
        return jsonify({"mensagem": "Movimentação não encontrada"}), 404
