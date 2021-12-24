from flask import Flask, Blueprint
from flask_cors import CORS
from flask_restful import Api
from flask_session import Session
# from flasgger import Swagger

from src.api.config import env_config

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def create_app(config_name):
    import src.resources

    app = Flask(__name__)
    app.config.from_object(env_config[config_name])
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    CORS(app, supports_credentials=True)
    Session(app)
    # Swagger(app)

    return app
