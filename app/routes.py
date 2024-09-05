from flask import Flask, request, jsonify, session, render_template
from app import app, db
from app.models import User

@app.route('/')
def home():
    return "Bem-vindo ao meu site de e-commerce!"

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email já cadastrado!'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuário registrado com sucesso!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({'message': 'Credenciais inválidas!'}), 401

    # Sessão do usuário
    session['user_id'] = user.id
    return jsonify({'message': 'Login realizado com sucesso!'})
