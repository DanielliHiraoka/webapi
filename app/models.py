from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    preferences = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(255), nullable=True)  
    city = db.Column(db.String(100), nullable=True)  
    state = db.Column(db.String(100), nullable=True)  
    postal_code = db.Column(db.String(20), nullable=True)  

   

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Cat(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

class AdoptionProposal(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey('cat.id'), nullable=False)
    cat = db.relationship('Cat', backref=db.backref('proposals', lazy=True))