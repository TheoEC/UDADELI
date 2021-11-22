from flask import Flask
from flask_restful import Api
from flask_cors import CORS


class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.cors = CORS(self.app)

        self.app.config["UPLOAD_EXTENSIONS"] = [".xlsx"]

    def run(self):
        self.app.run(debug=True)


server = Server()
