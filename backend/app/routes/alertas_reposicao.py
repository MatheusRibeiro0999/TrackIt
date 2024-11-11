from flask import Blueprint, request, jsonify
from app import db
from app.models import AlertaReposicao

alertas_reposicao_bp = Blueprint('alertas_reposicao', __name__)

@alertas_reposicao_bp.route('/', methods=['GET'])
def listar_alertas_reposicao():
    alertas = AlertaReposicao.query.all()  
    alertas_json = [{'id': alerta.id, 'produto_id': alerta.produto_id, 'quantidade': alerta.quantidade} for alerta in alertas]
    return jsonify(alertas_json)
    

@alertas_reposicao_bp.route('/', methods=['POST'])
def criar_alerta_reposicao():
    dados = request.get_json()
    novo_alerta = AlertaReposicao(produto_id=dados['produto_id'], quantidade=dados['quantidade'])
    db.session.add(novo_alerta)
    db.session.commit()
    return jsonify({'message': 'Alerta de reposição criado com sucesso!'}), 201


@alertas_reposicao_bp.route('/<int:id>', methods=['PUT'])
def atualizar_alerta_reposicao(id):
    dados = request.get_json()
    alerta = AlertaReposicao.query.get(id)
    
    if alerta:
        alerta.produto_id = dados['produto_id']
        alerta.quantidade = dados['quantidade']
        db.session.commit()
        return jsonify({'message': f'Alerta de reposição {id} atualizado com sucesso!'}), 200
    else:
        return jsonify({'message': 'Alerta não encontrado'}), 404


@alertas_reposicao_bp.route('/<int:id>', methods=['PATCH'])
def editar_alerta_reposicao(id):
    dados = request.get_json()
    alerta = AlertaReposicao.query.get(id)
    
    if alerta:
        if 'produto_id' in dados:
            alerta.produto_id = dados['produto_id']

        if 'quantidade' in dados:
            alerta.quantidade = dados['quantidade']
        db.session.commit()
        return jsonify({'message': f'Alerta de reposição {id} atualizado com sucesso!'}), 200
    else:
        return jsonify({'message': 'Alerta não encontrado'}), 404



@alertas_reposicao_bp.route('/<int:id>', methods=['DELETE'])
def deletar_alerta_reposicao(id):
    alerta = AlertaReposicao.query.get(id)
    
    if alerta:
        db.session.delete(alerta)
        db.session.commit()
        return jsonify({'message': f'Alerta de reposição {id} deletado com sucesso!'}), 200
    else:
        return jsonify({'message': 'Alerta não encontrado'}), 404

