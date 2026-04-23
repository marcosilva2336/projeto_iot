from flask import Blueprint, request, render_template
from src.controllers.auth_controller import AuthController

auth_view_bp = Blueprint('auth_view', __name__)

# --- Rotas para as Páginas (Front-end) ---

@auth_view_bp.route('/')
def index():
    return render_template('index.html')

@auth_view_bp.route('/auth/register-page')
def register_page():
    return render_template('register.html')

@auth_view_bp.route('/auth/login-page')
def login_page():
    return render_template('login.html')

@auth_view_bp.route('/dashboard') # Rota amigável para o navegador
def dashboard_page():
    # O nome aqui deve ser EXATAMENTE o nome do seu arquivo HTML
    return render_template('dashboard.html')

# --- Rotas da API (JSON) ---
@auth_view_bp.route('/auth/register', methods=['POST'])
def register_api():
    return AuthController.register(request.json)

@auth_view_bp.route('/auth/login', methods=['POST'])
def login_api():
    return AuthController.login(request.json)