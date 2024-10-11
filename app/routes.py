from flask import Flask, request, jsonify, session
from app import app, db
from app.models import User
from app import db


@app.route('/')
def home():
    return "Bem-vindo a nossa Ong de Adoção de Gatinhos"


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Verificar se o nome de usuário já existe
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Nome de usuário já cadastrado!'}), 400

    # Verificar se o e-mail já existe
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'E-mail já cadastrado!'}), 400

    # Criar um novo usuário
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
        return jsonify({'message': 'Email ou senha inválidos!'}), 401

    session['user_id'] = user.id
    return jsonify({'message': 'Login realizado com sucesso!'})


@app.route('/api/profile', methods=['GET'])
def get_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Usuário não autenticado!'}), 401

    user = User.query.get(user_id)
    if user:
        return jsonify({
            'username': user.username,
            'email': user.email
        })
    else:
        return jsonify({'message': 'Usuário não encontrado!'}), 404
