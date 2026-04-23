import os
from flask import Flask
from src.extensions import db, jwt

def create_app():
    # O template_folder garante que o Flask ache seus HTMLs na pasta certa
    app = Flask(__name__, template_folder='templates')
    
    # Configurações de Banco e Segurança
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///local.db")
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "minha-chave-secreta")
    
    db.init_app(app)
    jwt.init_app(app)

    # 1. IMPORTAR OS MODELOS PRIMEIRO
    # Isso avisa ao SQLAlchemy que as tabelas User e Task precisam existir
    from src.models.user import User, Task

    # 2. CRIAR AS TABELAS DEPOIS
    with app.app_context():
        db.create_all()

        with app.app_context():
        db.create_all()
        
        # Lógica para garantir que o Admin exista
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", role="admin")
            admin.set_password("admin123") 
            db.session.add(admin)
            db.session.commit()
            

    # 3. REGISTRAR AS ROTAS POR ÚLTIMO
    from src.views.auth_view import auth_view_bp
    from src.controllers.task_controller import task_bp
  
    app.register_blueprint(auth_view_bp) 
    app.register_blueprint(task_bp, url_prefix='/api')

    return app