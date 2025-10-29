from flask import request, jsonify
from app.models import Users, db
from .schemas import user_schema, users_schema, login_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import users_bp
from app.util.auth import encode_token, token_required

#Login
@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    user = db.session.query(Users).where(Users.email==data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        token = encode_token(user.id, user.role)
        return jsonify({
            'message': 'Successfully Logged in',
            'token': token,
            'user': user_schema.dump(user)
        }), 200
    
    return jsonify({'error': 'invalid email or password'})


# Register/Create Users
@users_bp.route('', methods=['POST'])
def create_user():

    try:
        data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    data['password']= generate_password_hash(data['password'])

    user = db.session.query(Users).filter_by(Users.email == data['email']).first()

    if user: 
        return jsonify({'error': 'Email already taken'}), 400
    
    new_user = Users(**data)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'Successfully created user',
        'user': user_schema.dump(new_user)
    })




# View Profile
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(Users, user_id)
    if user:
        return user_schema.jsonify(user), 200
    return jsonify ({'error': 'Invalid user id'})


# View All users
# @users_bp.route('', methods=['GET'])
# def get_users():
#     users = db.session.query(Users).all()
#     return users_schema.jsonify(users), 200


# Update Profile

@users_bp.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user():
    user_id= request.user_id
    user = db.session.get(Users, user_id)

    if not user:
            return jsonify({'error': 'Invalid User Id'}), 404

    try:
        data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in data.items():
        setattr(user, key, value)

    data['password'] = generate_password_hash(data['password'])

    existing = db.session.query(Users).where(Users.email == data['email']).first()
    if existing:
        return jsonify({"error": "Email already taken."})

    db.session.commit()
    return jsonify({
         'message': 'Successfully updated account',
         'user': user_schema.dump(user)
    }), 200


# Delete Profile
@users_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user():
    user_id= request.user_id
    user = db.session.get(Users, user_id)
    if user:
        db.session.delete(user)            
        db.session.commit()
        return jsonify({'message': 'Successfully deleted user'}), 200
    return jsonify({'error': 'Invalid user id'}), 400