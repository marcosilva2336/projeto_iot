from flask import Blueprint, request, render_template
from src.controllers.auth_controller import AuthController

auth_view_bp = Blueprint('auth_view', __name__)

# --- Rotas para as Páginas (Front-end) ---
@auth_view_bp.route('/auth/register-page')
def register_page():
    return render_template('register.html')

@auth_view_bp.route('/auth/login-page')
def login_page():
    return render_template('login.html')

# --- Rotas da API (JSON) ---
@auth_view_bp.route('/auth/register', methods=['POST'])
def register_api():
    return AuthController.register(request.json)

@auth_view_bp.route('/auth/login', methods=['POST'])
def login_api():
    return AuthController.login(request.json)