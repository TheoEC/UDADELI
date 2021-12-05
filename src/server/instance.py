from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_session import Session

from src.config import ApplicationConfig


class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.cors = CORS(self.app, supports_credentials=True)
        self.app.config.from_object(ApplicationConfig)
        self.session = Session(self.app)

    def run(self):
        self.app.run(debug=True)


server = Server()
