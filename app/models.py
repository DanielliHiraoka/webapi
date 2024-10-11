from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    preferences = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(255), nullable=True)  # Novo campo de endereço
    city = db.Column(db.String(100), nullable=True)  # Novo campo de cidade
    state = db.Column(db.String(100), nullable=True)  # Novo campo de estado
    postal_code = db.Column(db.String(20), nullable=True)  # Novo campo de CEP

   

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
