from flask import request, jsonify
from app.models import County_name_mapping, db
from .schemas import county_name_mapping_schema, county_name_mappings_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import county_name_mapping_bp



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




# View county_mapping (used for comparing)
# @county_name_mapping_bp.route('/<fips_id>', methods=['GET'])
# def get_county_name_mapping(fips_id):
#     county_name_mapping = db.session.get(County_name_mapping, fips_id)
#     if county_name_mapping:
#         return county_name_mapping_schema.jsonify(county_name_mapping), 200
#     return jsonify ({'error': 'Invalid fips id'})


# start the page with this, then allow user to pick from closest 5 
# View counties_mapping
@county_name_mapping_bp.route('', methods=['GET'])
def get_county_name_mappings():
    county_name_mappings = db.session.query(County_name_mapping).all()
    return county_name_mappings_schema.jsonify(county_name_mappings), 200


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