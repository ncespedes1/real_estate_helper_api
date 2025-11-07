from flask import request, jsonify, Flask, render_template, redirect, url_for
from app.models import County_name_mapping, db
from .schemas import county_name_mapping_schema, county_name_mappings_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import county_name_mapping_bp
import pandas as pd
import io
from sqlalchemy import select


# Create County_name_mapping (multiple) by uploading csv file
@county_name_mapping_bp.route('/upload', methods=['POST'])
def upload_county_name_mapping():

    if 'file' not in request.files:
        return jsonify({'error': 'no file found'}), 400
    
    file = request.files['file']

    if file:
        try:
            existing_county_name_fips = db.session.scalars(select(County_name_mapping.fips_id)).all() #checking existing db
            dataframe = pd.read_csv(io.StringIO(file.stream.read().decode("UTF8")), sep=',', header=0, usecols=['county_fips', 'county_name'], dtype={'county_fips': str})
            new_fips_added = set()

            for row in dataframe.itertuples(index=False):
                new_county_name_mapping = County_name_mapping(fips_id= row.county_fips, county_name= row.county_name)
                if new_county_name_mapping.fips_id not in existing_county_name_fips and new_county_name_mapping.fips_id not in new_fips_added:
                    db.session.add(new_county_name_mapping)
                    new_fips_added.add(new_county_name_mapping.fips_id)
                    print(f"Fips: {row.county_fips}, Name: {row.county_name}")

            db.session.commit()
        
        except Exception as e:
            return jsonify(e.messages), 400

    return jsonify({
        'message': 'Successfully created county_name_mapping'
        # 'county_name_mapping': county_name_mapping_schema.dump(new_county_name_mapping)
    }),200




# View county_mapping (used for comparing)
# @county_name_mapping_bp.route('/<fips_id>', methods=['GET'])
# def get_county_name_mapping(fips_id):
#     county_name_mapping = db.session.get(County_name_mapping, fips_id)
#     if county_name_mapping:
#         return county_name_mapping_schema.jsonify(county_name_mapping), 200
#     return jsonify ({'error': 'Invalid fips id'})


# start the page with this, then frontend- allow user to autofill closest 5 
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