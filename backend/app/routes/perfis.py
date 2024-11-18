from flask import Blueprint, request, jsonify
from app import db
from app.models import Perfil
from flask_jwt_extended import jwt_required, get_jwt_identity

perfis_bp = Blueprint('perfis', __name__)

@perfis_bp.route('/perfis', methods=['POST'])
@jwt_required()
def criar_perfil():
    usuario_id = get_jwt_identity()  
    try:
        nome = request.json.get('nome')
        
        if not nome:
            return jsonify({'error': 'Nome do perfil é obrigatório'}), 400
        
        if Perfil.query.filter_by(nome=nome).first():
            return jsonify({'error': f'O perfil {nome} já existe'}), 400
        
        novo_perfil = Perfil(nome=nome)
        db.session.add(novo_perfil)
        db.session.commit()
        
        return jsonify({'message': f'Perfil {nome} criado com sucesso!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@perfis_bp.route('/perfis', methods=['GET'])
@jwt_required()
def listar_perfis():
    try:
        perfis = Perfil.query.all()
        lista_perfis = [{"id": perfil.id, "nome": perfil.nome} for perfil in perfis]
        
        return jsonify(lista_perfis), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@perfis_bp.route('/perfis/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_perfil(id):
    try:
        perfil = Perfil.query.get(id)
        
        if not perfil:
            return jsonify({'error': 'Perfil não encontrado'}), 404
        
        nome = request.json.get('nome')
        
        if not nome:
            return jsonify({'error': 'Nome do perfil é obrigatório'}), 400
        
        perfil.nome = nome
        db.session.commit()
        
        return jsonify({'message': f'Perfil {perfil.id} atualizado com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@perfis_bp.route('/perfis/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_perfil(id):
    try:
        perfil = Perfil.query.get(id)
        
        if not perfil:
            return jsonify({'error': 'Perfil não encontrado'}), 404
        
        db.session.delete(perfil)
        db.session.commit()
        
        return jsonify({'message': f'Perfil {perfil.id} deletado com sucesso!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
