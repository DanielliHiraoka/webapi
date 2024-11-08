from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)


CORS(
    app,
    supports_credentials=True,  
    resources={r"/api/*": {"origins": "http://localhost:3000"}},
)

# Configurações de sessão (cookies)
app.config['SECRET_KEY'] = 'a1b2c3d4e5f6g7h8i9j0k1234567890abcdefg'
app.config['SESSION_COOKIE_HTTPONLY'] = True  
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  
app.config['SESSION_COOKIE_SECURE'] = True  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:impacta@localhost/db_impacta2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes
