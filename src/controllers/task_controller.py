from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.models import User, Task
from src.extensions import db

task_bp = Blueprint('tasks', __name__)

# 1a. CRIAR (Admin ou User cria para si mesmo)
@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.json
    new_task = Task(title=data['title'], description=data.get('description', ''), user_id=user_id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"msg": "Tarefa criada", "id": new_task.id}), 201

# 1b. LISTAR (Admin vê todas, User vê as suas)
@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def list_tasks():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role == 'admin':
        tasks = Task.query.all() # Admin vê tudo
    else:
        tasks = Task.query.filter_by(user_id=user_id).all() # User vê só as dele
        
    result = [{"id": t.id, "title": t.title, "user_id": t.user_id} for t in tasks]
    return jsonify(result), 200

# 1c. EDITAR (Admin edita qualquer uma, User edita a sua)
@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    task = Task.query.get_or_404(id)
    
    if user.role != 'admin' and task.user_id != user.id:
        return jsonify({"error": "Acesso negado: você não é dono desta tarefa"}), 403
        
    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    db.session.commit()
    return jsonify({"msg": "Tarefa atualizada com sucesso!"}), 200

# 1d. EXCLUIR (Admin exclui qualquer uma, User exclui a sua)
@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    task = Task.query.get_or_404(id)
    
    if user.role != 'admin' and task.user_id != user.id:
        return jsonify({"error": "Acesso negado: apenas o admin ou dono podem excluir"}), 403
        
    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Tarefa removida com sucesso!"}), 200