from flask import request, jsonify
from app.models import County_data, db
from .schemas import county_data_schema, counties_data_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import county_data_bp
from datetime import datetime
import pandas as pd
import io


# Create county_data multiple by uploading csv file
@county_data_bp.route('/upload', methods=['POST'])
def upload_county_data():

    if 'file' not in request.files:
        return jsonify({'error': 'no file found'}), 400
    
    file = request.files['file']

    if file:
        dataframe = pd.read_csv(io.StringIO(file.stream.read().decode("UTF8")), sep=',', header=0, usecols=[
            'month_date_yyyymm', 
            'county_fips', 
            'median_listing_price', 
            'active_listing_count', 
            'active_listing_count_yy', 
            'median_days_on_market', 
            'price_reduced_count', 
            'pending_listing_count'], 
            dtype={'month_date_yyyymm':str,'county_fips': str, 'active_listing_county_yy': float})
        
        dataframe = dataframe.fillna(0) #'Nan' data will register as 0

        for row in dataframe.itertuples(index=False):
            if row.county_fips is None:
                continue
            county_date= datetime.strptime(row.month_date_yyyymm + "01", '%Y%m%d')

            
            new_county_data = County_data(
                info_date= county_date, 
                fips_id= row.county_fips,
                median_listing_price= row.median_listing_price,
                active_listing_count= row.active_listing_count,
                active_listing_count_yy= row.active_listing_count_yy,
                median_days_on_market= row.median_days_on_market,
                price_reduced_count= row.price_reduced_count,
                pending_listing_count= row.pending_listing_count 
                )
            
            db.session.add(new_county_data)
            print(f"Fips: {row.county_fips}, Median_listing_price: {row.median_listing_price}, Median_days_on_market: {row.median_days_on_market}")

        db.session.commit()


    return jsonify({
        'message': 'Successfully created county_data'
    }), 200




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