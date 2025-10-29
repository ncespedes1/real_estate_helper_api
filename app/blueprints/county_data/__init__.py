from flask import Blueprint

county_data_bp = Blueprint('county_data_bp', __name__)

from . import routes
