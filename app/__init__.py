from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'a1b2c3d4e5f6g7h8i9j0k1234567890abcdefg'

# Configurando a URI de conexão ao PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:impacta@localhost/db_impacta2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando a extensão SQLAlchemy e Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importe seus modelos aqui


# Importar as rotas
from app import routes


