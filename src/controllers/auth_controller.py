from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from src.models.user import User
from src.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Usuário já existe"}), 400
    
    new_user = User(username=data['username'], role=data.get('role', 'user'))
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Usuário criado com sucesso!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        
        token = create_access_token(identity=str(user.id))
        return jsonify(access_token=token), 200
    return jsonify({"msg": "Login inválido"}), 401