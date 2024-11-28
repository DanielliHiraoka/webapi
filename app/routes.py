from flask import Flask, request, jsonify, session
from app import app, db
from app.models import User, Cat, AdoptionProposal
from functools import wraps


@app.route('/api/users/admin-check', methods=['GET'])
def admin_check():
    user_id = request.headers.get('User-Id')
    if not user_id:
        return jsonify({"error": "Usuário não autenticado"}), 401

    user = User.query.get(user_id)
    if user and user.is_admin:
        return jsonify({"message": "Usuário é administrador"}), 200

    return jsonify({"error": "Acesso negado"}), 403


# Decorador para verificar se o usuário está autenticado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({"error": "Usuário não autenticado!"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Decorador para verificar se o usuário é administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.headers.get("User-Id") 
        if not user_id:
            return jsonify({"error": "Autenticação necessária"}), 401

        user = User.query.get(user_id)
        if not user or not user.is_admin:
            return jsonify({"error": "Acesso negado. Privilégios de administrador são necessários."}), 403

        return f(*args, **kwargs)
    return decorated_function

# Rotas públicas
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    preferences = data.get("preferences")

    if not username or not email or not password or not phone:
        return jsonify({"error": "Preencha todos os campos obrigatórios!"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Nome de usuário já cadastrado!"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "E-mail já cadastrado!"}), 400

    new_user = User(username=username, email=email, phone=phone, preferences=preferences)
    new_user.set_password(password)  
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso!"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Usuário ou senha incorretos!"}), 401

    session["user_id"] = user.id
    print(f"Usuário autenticado com ID: {user.id}")  # Log para depuração

    return jsonify({"message": "Login realizado com sucesso!", "user_id": user.id, "is_admin": user.is_admin}), 200



# Rotas protegidas para usuários autenticados
@app.route("/api/profile", methods=["GET"])
@login_required
def get_profile():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "preferences": user.preferences,
            "address": user.address,
            "city": user.city,
            "state": user.state,
            "postal_code": user.postal_code
        })
    return jsonify({"error": "Usuário não encontrado!"}), 404

@app.route("/api/profile", methods=["PUT"])
@login_required
def update_profile():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if user:
        data = request.json
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.phone = data.get("phone", user.phone)
        user.preferences = data.get("preferences", user.preferences)
        user.address = data.get("address", user.address)
        user.city = data.get("city", user.city)
        user.state = data.get("state", user.state)
        user.postal_code = data.get("postal_code", user.postal_code)
        db.session.commit()
        return jsonify({"message": "Perfil atualizado com sucesso!"}), 200
    return jsonify({"error": "Usuário não encontrado!"}), 404


@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "address": user.address,
        "city": user.city,
        "state": user.state,
        "postal_code": user.postal_code
    } for user in users]), 200


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Consultar o usuário pelo ID
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Converter o usuário para um formato serializável
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "preferences": user.preferences,
        "address": user.address,
        "city": user.city,
        "state": user.state,
        "postal_code": user.postal_code
    }

    # Retornar os dados do usuário como JSON
    return jsonify(user_data), 200
    

@app.route('/api/cats', methods=['GET'])
@login_required
def get_cats():
    cats = Cat.query.all()
    return jsonify([{
        "id": cat.id,
        "name": cat.name,
        "age": cat.age,
        "description": cat.description,
        "image": cat.image_url
    } for cat in cats]), 200


@app.route('/api/cats/<int:cat_id>', methods=['GET'])
def get_cat(cat_id):
    cat = Cat.query.get(cat_id)
    if not cat:
        return jsonify({'error': 'Gato não encontrado'}), 404
    return jsonify({
        'id': cat.id,
        'name': cat.name,
        'age': cat.age,
        'description': cat.description,
        'image': cat.image_url
    }), 200

    
 
@app.route('/api/adoption', methods=['POST'])
def create_adoption_proposal():
    data = request.get_json()

    name = data.get('name')
    contact = data.get('contact')
    reason = data.get('reason')
    cat_id = data.get('catId')

    if not all([name, contact, reason, cat_id]):
        return jsonify({'error': 'Todos os campos são obrigatórios.'}), 400

    cat = Cat.query.get(cat_id)
    if not cat:
        return jsonify({'error': 'O gato selecionado não foi encontrado.'}), 404

    try:
        proposal = AdoptionProposal(name=name, contact=contact, reason=reason, cat_id=cat_id)
        db.session.add(proposal)
        db.session.commit()
        return jsonify({'message': 'Proposta de adoção enviada com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao salvar a proposta: {str(e)}'}), 500

@app.route('/api/adoption-proposals', methods=['GET'])
@admin_required
def get_adoption_proposals():
    proposals = AdoptionProposal.query.all()
    result = [
        {
            "id": proposal.id,
            "name": proposal.name,
            "contact": proposal.contact,
            "catName": proposal.cat.name if proposal.cat else "Não informado",
            "reason": proposal.reason,
        }
        for proposal in proposals
    ]
    return jsonify(result), 200

