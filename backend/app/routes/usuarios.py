from flask import Blueprint, request, jsonify
from app import db
from app.models import Usuario

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET']) #retorna todos os users
def listar_usuarios():
    usuarios = Usuario.query.all()
    usuarios_list = []
    for usuario in usuarios:
        usuarios_list.append({
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'perfil': usuario.perfil
        })
    return jsonify({'usuarios': usuarios_list})

@usuarios_bp.route('/', methods=['POST'])#insere novos users
def criar_usuario():
    dados = request.get_json()
    if not dados or not all(k in dados for k in ('nome', 'email', 'senha', 'perfil')):
        return jsonify({"mensagem": "Dados incompletos"}), 400
    
    novo_usuario = Usuario(
        nome=dados['nome'], 
        email=dados['email'], 
        senha=dados['senha'], 
        perfil=dados['perfil']
    )
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({"mensagem": "Usuário criado com sucesso", "usuario": {'id': novo_usuario.id}}), 201

@usuarios_bp.route('/<int:id>', methods=['PUT'])#atualiza todos os dados do usuario
def atualizar_usuario(id):
    dados = request.get_json()
    usuario = Usuario.query.get(id)
    
    if usuario:
        usuario.nome = dados['nome']
        usuario.email = dados['email']
        usuario.senha = dados['senha']
        usuario.perfil = dados['perfil']
        
        db.session.commit()
        return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

@usuarios_bp.route('/<int:id>', methods=['PATCH'])# atualiza os dados do usuario (somente parametros)
def modificar_usuario(id):
    dados = request.get_json()
    usuario = Usuario.query.get(id)
    
    if usuario:
        if 'nome' in dados:
            usuario.nome = dados['nome']
        if 'email' in dados:
            usuario.email = dados['email']
        if 'senha' in dados:
            usuario.senha = dados['senha']
        if 'perfil' in dados:
            usuario.perfil = dados['perfil']
        
        db.session.commit()
        return jsonify({"mensagem": "Dados do usuário modificados com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

@usuarios_bp.route('/<int:id>', methods=['DELETE'])#deleta né 
def deletar_usuario(id):
    usuario = Usuario.query.get(id)
    
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"mensagem": "Usuário deletado com sucesso"}), 204
    else:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404
