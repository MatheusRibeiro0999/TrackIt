from flask import Blueprint, request, jsonify
from app import db
from app.models import LogAtividade  

logs_atividades_bp = Blueprint('logs_atividades', __name__)

@logs_atividades_bp.route('/', methods=['GET'])
def listar_logs_atividades():
    logs = LogAtividade.query.all()  
    logs_list = []
    for log in logs:
        logs_list.append({
            'id': log.id,
            'usuario_id': log.usuario_id,
            'acao': log.acao,
            'data_hora': log.data_hora
        })
    return jsonify({'logs_atividades': logs_list})

@logs_atividades_bp.route('/', methods=['POST'])
def criar_log_atividade():
    dados = request.get_json()
    
    if not dados or not all(k in dados for k in ('usuario_id', 'acao', 'data_hora')):
        return jsonify({"mensagem": "Dados incompletos"}), 400
    
    novo_log = LogAtividade(
        usuario_id=dados['usuario_id'], 
        acao=dados['acao'], 
        data_hora=dados['data_hora']
    )
    
    db.session.add(novo_log)
    db.session.commit()
    
    return jsonify({"mensagem": "Log de atividade criado com sucesso", "log_atividade": {'id': novo_log.id}}), 201

@logs_atividades_bp.route('/<int:id>', methods=['PUT'])
def atualizar_log_atividade(id):
    dados = request.get_json()
    log = LogAtividade.query.get(id)
    
    if log:
        log.usuario_id = dados['usuario_id']
        log.acao = dados['acao']
        log.data_hora = dados['data_hora']
        
        db.session.commit()
        return jsonify({"mensagem": "Log de atividade atualizado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Log de atividade não encontrado"}), 404

@logs_atividades_bp.route('/<int:id>', methods=['PATCH'])
def modificar_log_atividade(id):
    dados = request.get_json()
    log = LogAtividade.query.get(id)
    
    if log:
        if 'usuario_id' in dados:
            log.usuario_id = dados['usuario_id']
        if 'acao' in dados:
            log.acao = dados['acao']
        if 'data_hora' in dados:
            log.data_hora = dados['data_hora']
        
        db.session.commit()
        return jsonify({"mensagem": "Log de atividade modificado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Log de atividade não encontrado"}), 404

@logs_atividades_bp.route('/<int:id>', methods=['DELETE'])
def deletar_log_atividade(id):
    log = LogAtividade.query.get(id)
    
    if log:
        db.session.delete(log)
        db.session.commit()
        return jsonify({"mensagem": "Log de atividade deletado com sucesso"}), 204
    else:
        return jsonify({"mensagem": "Log de atividade não encontrado"}), 404
