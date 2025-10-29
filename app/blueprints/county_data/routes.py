from flask import request, jsonify
from app.models import County_data, db
from .schemas import county_data_schema, counties_data_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import county_data_bp



# Register/Create Location
# @locations_bp.route('', methods=['POST'])
# def create_location():

#     try:
#         data = location_schema.load(request.json)
#     except ValidationError as e:
#         return jsonify(e.messages), 400
    
#     new_location = Location(**data)
#     db.session.add(new_location)
#     db.session.commit()

#     return jsonify({
#         'message': 'Successfully created location',
#         'location': location_schema.dump(new_location)
#     })




# View Profile
@county_data_bp.route('/<fips_id>', methods=['GET'])
def get_county_data(fips_id):
    county_data = db.session.get(County_data, fips_id)
    if county_data:
        return county_data_schema.jsonify(county_data), 200
    return jsonify ({'error': 'Invalid fips id'})


# View All locations
# @locations_bp.route('', methods=['GET'])
# def get_locations():
#     locations = db.session.query(Location).all()
#     return locations_schema.jsonify(locations), 200


# Update Profile
# @locations_bp.route('/<int:location-id>', methods=['PUT'])
# def update_location(location_id):
#     location = db.session.get(Location, location_id)

#     if not location:
#             return jsonify({'error': 'Invalid Location Id'}), 404

#     try:
#         data = location_schema.load(request.json)
#     except ValidationError as e:
#         return jsonify(e.messages), 400
    
#     for key, value in data.items():
#         setattr(location, key, value)

#     db.session.commit()
#     return jsonify({
#          'message': 'Successfully updated account',
#          'location': location_schema.dump(location)
#     }), 200


# Delete Profile
# @locations_bp.route('/<int:location-id>', methods=['DELETE'])
# def delete_location(location_id):
#     location = db.session.get(Location, location_id)
#     if location:
#         db.session.delete(location)            
#         db.session.commit()
#         return jsonify({'message': 'Successfully deleted location'}), 200
#     return jsonify({'error': 'Invalid location id'}), 400