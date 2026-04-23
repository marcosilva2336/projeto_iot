from flask import jsonify
from flask_jwt_extended import create_access_token
from src.models.user import User
from src.extensions import db

class AuthController:
    @staticmethod
    def register(data):
        # Verifica se usuário já existe
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Usuário já existe"}), 400
        
        # Cria novo usuário com role (Requisito 3)
        new_user = User(
            username=data['username'], 
            role=data.get('role', 'user') # Padrão é usuário comum
        )
        new_user.set_password(data['password']) # Hashing seguro
        
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "Conta criada com sucesso!"}), 201

    @staticmethod
    def login(data):
        user = User.query.filter_by(username=data['username']).first()
        
        # Valida senha e gera Token JWT
        if user and user.check_password(data['password']):
            # O 'identity' no token será o ID do usuário
            token = create_access_token(identity=str(user.id))
            return jsonify({"access_token": token, "role": user.role}), 200
            
        return # Valida senha e gera Token JWT
        if user and user.check_password(data['password']):
            token = create_access_token(identity=str(user.id))
            return jsonify({
                "access_token": token, 
                "role": user.role, 
                "username": user.username
            }), 200