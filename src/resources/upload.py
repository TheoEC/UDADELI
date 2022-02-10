import os

import pandas as pd
from flask import abort, current_app, request, session
from flask_restful import Resource


class UploadResource(Resource):
    def post(self):
        if "file" not in request.files:
            return "No file uploaded"

        file = request.files["file"]
        filename = file.filename

        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config["UPLOAD_EXTENSIONS"]:
                abort(400, {"message": "File must be .xlsx"})

        df = pd.read_excel(file)

        if 'cliente-id' in df:
            session['pedidos-df'] = df.to_dict()
        elif 'email' in df:
            session['clientes-df'] = df.to_dict()
        else:
            session['produtos-df'] = df.to_dict()

        return {"message": "Data uploaded"}, 200
