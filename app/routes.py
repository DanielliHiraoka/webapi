from flask import Flask, request, jsonify, session
from app import app, db
from app.models import User

@app.route("/")
def home():
    return "Bem-vindo a nossa Ong de Adoção de Gatinhos"

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    preferences = data.get("preferences")

    # Validação de campos vazios
    if not username or not email or not password or not phone:
        return jsonify({"message": "Preencha todos os campos obrigatórios!"}), 400

    # Validação de nome de usuário único
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Nome de usuário já cadastrado!"}), 400

    # Validação de e-mail único
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "E-mail já cadastrado!"}), 400

    # Criar novo usuário
    new_user = User(username=username, email=email, phone=phone, preferences=preferences)
    new_user.set_password(password)  # Criptografar senha
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso!"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()


    
    if user is None or not user.check_password(password):
        return jsonify({"message": "Usuário ou senha incorretos!"}), 401

    session["user_id"] = user.id
    return jsonify({"message": "Login realizado com sucesso!"})

@app.route("/api/profile", methods=["GET"])
def get_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "Usuário não autenticado!"}), 401

    user = User.query.get(user_id)
    if user:
        return jsonify({
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "preferences": user.preferences,
            "address": user.address,  # Incluindo o endereço no perfil
            "city": user.city,        # Incluindo a cidade no perfil
            "state": user.state,      # Incluindo o estado no perfil
            "postal_code": user.postal_code  # Incluindo o CEP no perfil
        })
    else:
        return jsonify({"message": "Usuário não encontrado!"}), 404


@app.route("/api/profile", methods=["PUT"])
def update_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "Usuário não autenticado!"}), 401

    user = User.query.get(user_id)
    if user:
        data = request.json
        username = data.get("username")
        email = data.get("email")
        phone = data.get("phone")
        preferences = data.get("preferences")
        address = data.get("address")
        city = data.get("city")
        state = data.get("state")
        postal_code = data.get("postal_code")

        # Validações básicas
        if not username or not email or not phone:
            return jsonify({"message": "Todos os campos obrigatórios devem ser preenchidos!"}), 400

        # Atualizar os dados do usuário
        user.username = username
        user.email = email
        user.phone = phone
        user.preferences = preferences
        user.address = address
        user.city = city
        user.state = state
        user.postal_code = postal_code

        try:
            db.session.commit()
            return jsonify({"message": "Perfil atualizado com sucesso!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Erro ao atualizar o perfil."}), 500
    else:
        return jsonify({"message": "Usuário não encontrado!"}), 404
