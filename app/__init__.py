from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)

# Configuração de CORS para permitir o envio de credenciais (cookies)
CORS(
    app,
    supports_credentials=True,  # Isso é essencial para enviar cookies
    resources={r"/api/*": {"origins": "http://localhost:3000"}},
)

# Configurações de sessão (cookies)
app.config['SECRET_KEY'] = 'a1b2c3d4e5f6g7h8i9j0k1234567890abcdefg'
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Cookies de sessão são HTTP apenas
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Para que o cookie seja enviado corretamente
app.config['SESSION_COOKIE_SECURE'] = True  # Defina como True em produção
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:impacta@localhost/db_impacta2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importar as rotas
from app import routes
