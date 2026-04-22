import os
from flask import Flask
from src.extensions import db, jwt

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "dev")
    
    db.init_app(app)
    jwt.init_app(app)

    # Inicia o banco automaticamente 
    with app.app_context():
        db.create_all()

    from src.controllers.task_controller import task_bp
    app.register_blueprint(task_bp)
    
    return app