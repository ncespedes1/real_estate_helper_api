from flask import Flask
from .models import db
from .extensions import ma
from .blueprints.users import users_bp
from .blueprints.county_data import county_data_bp
from .blueprints.county_name_mapping import county_name_mapping_bp


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(county_data_bp, url_prefix='/counties_data')
    app.register_blueprint(county_name_mapping_bp, url_prefix='/county_name_mappings')


    return app