from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configurando a URI de conexão ao PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://:impacta@localhost:5432/db_impacta2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando a extensão SQLAlchemy e Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importe seus modelos aqui


# Importar as rotas
from app import routes


