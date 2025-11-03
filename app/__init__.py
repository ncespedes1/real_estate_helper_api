from flask import Flask
from .models import db
from .extensions import ma
from .blueprints.users import users_bp
from .blueprints.county_data import county_data_bp
from .blueprints.county_name_mapping import county_name_mapping_bp
from flask_swagger_ui import get_swaggerui_blueprint
# from flask_cors import CORS

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'Real Estate Helper API'} )

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    # CORS(app)

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(county_data_bp, url_prefix='/county_data')
    app.register_blueprint(county_name_mapping_bp, url_prefix='/county_name_mapping')
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    return app