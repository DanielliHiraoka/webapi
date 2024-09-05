from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Isso permitirá que todas as origens façam requisições

# Restante da configuração do app


app = Flask (__name__)

@app.route("/")

def hello_world():
    return "<p>Hello, World!</p>"
    