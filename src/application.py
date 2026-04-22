import os
from flask import Flask
from src.extensions import db, jwt

def create_app():
    app = Flask(__name__)
    
    # Pega o banco de dados do Render (Requisito 6)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///local.db")
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "minha-chave-secreta")
    
    db.init_app(app)
    jwt.init_app(app)

    # Cria as tabelas na primeira execução
    with app.app_context():
        db.create_all()

    # Registra os Controllers (Rotas)
    from src.controllers.auth_controller import auth_bp
    from src.controllers.task_controller import task_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(task_bp, url_prefix='/api')

    return app