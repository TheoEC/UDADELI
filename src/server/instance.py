from flask import Flask
from flask_restful import Api
from flask_cors import CORS


class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.cors = CORS(self.app)
        self.api = Api(self.app)

    def run(self):
        self.app.run(debug=True)


server = Server()
