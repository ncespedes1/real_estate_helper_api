from flask import request, jsonify
from app.models import Users, County_name_mapping, db
from .schemas import user_schema, users_schema, login_schema
from app.blueprints.county_name_mapping.schemas import county_name_mappings_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import users_bp
from app.util.auth import encode_token, token_required

#Login and get token
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
    
    return jsonify({'error': 'invalid email or password'}), 401


# Register/Create Users
@users_bp.route('', methods=['POST'])
def create_user():

    try:
        data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    data['password']= generate_password_hash(data['password'])

    user = db.session.query(Users).where(Users.email == data['email']).first()

    if user: 
        return jsonify({'error': 'Email already taken'}), 400
    
    new_user = Users(**data)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201




# View User Profile
@users_bp.route('', methods=['GET'])
@token_required
def get_user():
    user_id= request.user_id
    user = db.session.get(Users, user_id)
    if user:
        return user_schema.jsonify(user), 200
    return jsonify ({'error': 'Invalid user id'}), 400


# View All users
# @users_bp.route('', methods=['GET'])
# def get_users():
#     users = db.session.query(Users).all()
#     return users_schema.jsonify(users), 200


# Update Profile
@users_bp.route('', methods=['PUT'])
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
    if existing and existing.id != user_id:
        return jsonify({"error": "Email already taken."}), 400

    db.session.commit()
    return user_schema.jsonify(existing), 200


# Delete Profile
@users_bp.route('', methods=['DELETE'])
@token_required
def delete_user():
    user_id= request.user_id
    user = db.session.get(Users, user_id)
    if user:
        db.session.delete(user)            
        db.session.commit()
        return jsonify({'message': 'Successfully deleted user'}), 200
    return jsonify({'error': 'Invalid user id'}), 400



#Assign compared counties
@users_bp.route('/assign_compare_county/<county_fips>', methods=['POST'])
@token_required
def assign_compare_county(county_fips):
    user_id= request.user_id
    user = db.session.get(Users, user_id)
    county_name_map = db.session.get(County_name_mapping, county_fips)

    if not user:
        return jsonify({'message': 'User not found'}), 404
    if not county_name_map:
        return jsonify({'message': 'County_name_mapping not found. Check fips_id.'}), 404
    if len(user.county_compare_list) >= 3:
        return ({'message': 'Maximum comparable County_data reached'}), 400

    for county in user.county_compare_list:
        if county_fips == county.fips_id:
            return ({'message': 'County_data already assigned to this user'}), 400
            
    user.county_compare_list.append(county_name_map)
    db.session.commit()

    return jsonify({'message': 'Successfully added a compare_county'}), 200

        
#Delete compare county
@users_bp.route('/remove_compare_county/<county_fips>', methods=['DELETE'])
@token_required
def remove_compare_county(county_fips):
    user_id= request.user_id
    user = db.session.get(Users, user_id)
    
    for county in user.county_compare_list:
        if county_fips == county.fips_id:
            user.county_compare_list.remove(county)
            db.session.commit()
            return jsonify({'message': 'Successfully removed a compare_county'}), 200
        
    return jsonify({'message': 'County_name_mapping not found. Check fips_id.'}), 404


#View compare county list
@users_bp.route('/view_compare_counties', methods=['GET'])
@token_required
def view_compare_counties():
    user_id= request.user_id
    user = db.session.get(Users, user_id)

    return county_name_mappings_schema.jsonify(user.county_compare_list), 200