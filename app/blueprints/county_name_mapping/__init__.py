from flask import Blueprint

county_name_mapping_bp = Blueprint('county_name_mapping_bp', __name__)

from . import routes
