import os
from flask import Flask
from src.extensions import db, jwt

def create_app():
   
    app = Flask(__name__, template_folder='templates')
    
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///local.db")
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "minha-chave-secreta")
    
    db.init_app(app)
    jwt.init_app(app)

    
    from src.models.user import User, Task

  
    with app.app_context():
        db.create_all()
        
        
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", role="admin")
            admin.set_password("admin123") 
            db.session.add(admin)
            db.session.commit()
            print("Admin criado!")

    
    from src.views.auth_view import auth_view_bp
    from src.controllers.task_controller import task_bp
  
    app.register_blueprint(auth_view_bp) 
    app.register_blueprint(task_bp, url_prefix='/api')

    return app