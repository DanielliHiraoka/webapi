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
            "address": user.address,  
            "city": user.city,        
            "state": user.state,      
            "postal_code": user.postal_code  
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
    
from flask import Flask, jsonify, request
from models import Cat, AdoptionProposal  # Ajuste conforme seus modelos

app = Flask(__name__)

# Endpoint para listar todos os gatos
@app.route('/api/cats', methods=['GET'])
def get_cats():
    cats = Cat.query.all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'age': cat.age,
        'description': cat.description,
        'image': cat.image_url
    } for cat in cats])


@app.route('/api/cats/<int:cat_id>', methods=['GET'])
def get_cat(cat_id):
    cat = Cat.query.get(cat_id)
    if not cat:
        return jsonify({'error': 'Cat not found'}), 404
    return jsonify({
        'id': cat.id,
        'name': cat.name,
        'age': cat.age,
        'description': cat.description,
        'image': cat.image_url
    })
    
    
 
@app.route('/api/adoption', methods=['POST'])
def create_adoption_proposal():
    data = request.get_json()
    name = data.get('name')
    contact = data.get('contact')
    reason = data.get('reason')
    cat_id = data.get('catId')

    # Validação básica
    if not all([name, contact, reason, cat_id]):
        return jsonify({'error': 'Dados incompletos'}), 400

    # Criação da proposta
    proposal = AdoptionProposal(name=name, contact=contact, reason=reason, cat_id=cat_id)
    db.session.add(proposal)
    db.session.commit()

    return jsonify({'message': 'Proposta de adoção enviada com sucesso!'}), 201

