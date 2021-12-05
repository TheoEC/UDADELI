import os

import pandas as pd
from flask import abort, request, session
from flask_restful import Resource
from src.server.instance import server
from src.common.mine_code import *

app = server.app

class Upload(Resource):
    def post(self):
        if "file" not in request.files:
            return "No file uploaded"

        file = request.files["file"]
        filename = file.filename

        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
                abort(400, { "message": "File must be .xlsx" })

        df = pd.read_excel(file)

        if 'cliente-id' in df:
            session['pedidos-df'] = df.to_dict()
        else:
            session['clientes-df'] = df.to_dict()


        return { "message": "Data uploaded" }, 200
