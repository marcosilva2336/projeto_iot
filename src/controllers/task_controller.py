from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, Task
from src.extensions import db

task_bp = Blueprint('tasks', __name__)

# LISTAR (Read)
@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Admin vê tudo, User comum vê só as suas
    if user.role == 'admin':
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(user_id=user_id).all()
        
    return jsonify([{"id": t.id, "desc": t.description} for t in tasks])

# CRIAR (Create)
@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()
    data = request.json
    new_task = Task(description=data['description'], user_id=user_id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"msg": "Tarefa criada!"}), 201

# EXCLUIR (Delete)
@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    task = Task.query.get_or_404(id)

    # Autorização: Admin deleta qualquer uma, User só a sua
    if user.role != 'admin' and task.user_id != user.id:
        return jsonify({"msg": "Acesso negado!"}), 403

    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Tarefa removida!"})