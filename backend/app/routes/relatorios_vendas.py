from flask import Blueprint, request, jsonify
from app import db
from app.models import RelatorioVendas  

relatorios_vendas_bp = Blueprint('relatorios_vendas', __name__)

@relatorios_vendas_bp.route('/', methods=['GET'])
def listar_relatorios_vendas():
    relatorios = RelatorioVendas.query.all()  
    relatorios_list = []
    for relatorio in relatorios:
        relatorios_list.append({
            'id': relatorio.id,
            'produto_id': relatorio.produto_id,
            'quantidade_vendida': relatorio.quantidade_vendida,
            'data_venda': relatorio.data_venda
        })
    return jsonify({'relatorios_vendas': relatorios_list})

@relatorios_vendas_bp.route('/', methods=['POST'])
def criar_relatorio_vendas():
    dados = request.get_json()
    
    if not dados or not all(k in dados for k in ('produto_id', 'quantidade_vendida', 'data_venda')):
        return jsonify({"mensagem": "Dados incompletos"}), 400
    
    novo_relatorio = RelatorioVendas(
        produto_id=dados['produto_id'], 
        quantidade_vendida=dados['quantidade_vendida'], 
        data_venda=dados['data_venda']
    )
    
    db.session.add(novo_relatorio)
    db.session.commit()
    
    return jsonify({"mensagem": "Relatório de vendas criado com sucesso", "relatorio_venda": {'id': novo_relatorio.id}}), 201

@relatorios_vendas_bp.route('/<int:id>', methods=['PUT'])
def atualizar_relatorio_vendas(id):
    dados = request.get_json()
    relatorio = RelatorioVendas.query.get(id)
    
    if relatorio:
        relatorio.produto_id = dados['produto_id']
        relatorio.quantidade_vendida = dados['quantidade_vendida']
        relatorio.data_venda = dados['data_venda']
        
        db.session.commit()
        return jsonify({"mensagem": "Relatório de vendas atualizado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Relatório de vendas não encontrado"}), 404

@relatorios_vendas_bp.route('/<int:id>', methods=['PATCH'])
def modificar_relatorio_vendas(id):
    dados = request.get_json()
    relatorio = RelatorioVendas.query.get(id)
    
    if relatorio:
        if 'produto_id' in dados:
            relatorio.produto_id = dados['produto_id']
        if 'quantidade_vendida' in dados:
            relatorio.quantidade_vendida = dados['quantidade_vendida']
        if 'data_venda' in dados:
            relatorio.data_venda = dados['data_venda']
        
        db.session.commit()
        return jsonify({"mensagem": "Relatório de vendas modificado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Relatório de vendas não encontrado"}), 404

@relatorios_vendas_bp.route('/<int:id>', methods=['DELETE'])
def deletar_relatorio_vendas(id):
    relatorio = RelatorioVendas.query.get(id)
    
    if relatorio:
        db.session.delete(relatorio)
        db.session.commit()
        return jsonify({"mensagem": "Relatório de vendas deletado com sucesso"}), 204
    else:
        return jsonify({"mensagem": "Relatório de vendas não encontrado"}), 404
