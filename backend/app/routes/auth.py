from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.models import db, Usuario
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    senha = request.json.get('senha', None)
    
    #verifica email e senha
    if not email or not senha:
        return jsonify({"msg": "Email e senha são obrigatórios!"}), 400

    #busca pelo email
    usuario = Usuario.query.filter_by(email=email).first()
    
    if usuario and check_password_hash(usuario.senha, senha):
        #gera JWT
        access_token = create_access_token(identity=usuario.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Credenciais inválidas!"}), 401
