from flask import request, jsonify
from app.models import Users, db
from app.blueprints.users.schemas import user_schema
from . import admin_bp
from marshmallow import ValidationError
from app.util.auth import admin_required

from app.blueprints.users.schemas import UserSchema

# View User Profile
@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_user():
    email = request.args.get('email')
    user = db.session.query(Users).where(Users.email==email).first()
    if user:
        return user_schema.jsonify(user), 200
    return jsonify ({'message': 'No user found'}), 404