from flask import Blueprint, request, jsonify
from app import db
from app.models import RelatorioEstoque  

relatorios_estoque_bp = Blueprint('relatorios_estoque', __name__)

@relatorios_estoque_bp.route('/', methods=['GET'])
def listar_relatorios_estoque():
    relatorios = RelatorioEstoque.query.all()  
    relatorios_list = []
    for relatorio in relatorios:
        relatorios_list.append({
            'id': relatorio.id,
            'produto_id': relatorio.produto_id,
            'quantidade': relatorio.quantidade,
            'data_geracao': relatorio.data_geracao
        })
    return jsonify({'relatorios_estoque': relatorios_list})

@relatorios_estoque_bp.route('/', methods=['POST'])
def criar_relatorio_estoque():
    dados = request.get_json()
    
    if not dados or not all(k in dados for k in ('produto_id', 'quantidade', 'data_geracao')):
        return jsonify({"mensagem": "Dados incompletos"}), 400
    
    novo_relatorio = RelatorioEstoque(
        produto_id=dados['produto_id'], 
        quantidade=dados['quantidade'], 
        data_geracao=dados['data_geracao']
    )
    
    db.session.add(novo_relatorio)
    db.session.commit()
    
    return jsonify({"mensagem": "Relatório de estoque criado com sucesso", "relatorio_estoque": {'id': novo_relatorio.id}}), 201

@relatorios_estoque_bp.route('/<int:id>', methods=['PUT'])
def atualizar_relatorio_estoque(id):
    dados = request.get_json()
    relatorio = RelatorioEstoque.query.get(id)
    
    if relatorio:
        relatorio.produto_id = dados['produto_id']
        relatorio.quantidade = dados['quantidade']
        relatorio.data_geracao = dados['data_geracao']
        
        db.session.commit()
        return jsonify({"mensagem": "Relatório de estoque atualizado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Relatório de estoque não encontrado"}), 404

@relatorios_estoque_bp.route('/<int:id>', methods=['PATCH'])
def modificar_relatorio_estoque(id):
    dados = request.get_json()
    relatorio = RelatorioEstoque.query.get(id)
    
    if relatorio:
        if 'produto_id' in dados:
            relatorio.produto_id = dados['produto_id']
        if 'quantidade' in dados:
            relatorio.quantidade = dados['quantidade']
        if 'data_geracao' in dados:
            relatorio.data_geracao = dados['data_geracao']
        
        db.session.commit()
        return jsonify({"mensagem": "Relatório de estoque modificado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Relatório de estoque não encontrado"}), 404

@relatorios_estoque_bp.route('/<int:id>', methods=['DELETE'])
def deletar_relatorio_estoque(id):
    relatorio = RelatorioEstoque.query.get(id)
    
    if relatorio:
        db.session.delete(relatorio)
        db.session.commit()
        return jsonify({"mensagem": "Relatório de estoque deletado com sucesso"}), 204
    else:
        return jsonify({"mensagem": "Relatório de estoque não encontrado"}), 404
