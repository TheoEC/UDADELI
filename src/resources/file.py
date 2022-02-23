import os

import pandas as pd
from flask import current_app, request, session
from flask_restful import abort, Resource


def abort_if_spreadsheet_doesnt_exist(spreadsheet_id):
    if spreadsheet_id not in session:
        abort(404, message=f"A planilha de {spreadsheet_id} não foi carregada")


class FileResource(Resource):
    def post(self):
        if "file" not in request.files:
            return "No file uploaded"

        file = request.files["file"]
        filename = file.filename

        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config["UPLOAD_EXTENSIONS"]:
                abort(400, message="O tipo do arquivo deve ser '.xlsx'")

        df = pd.read_excel(file)

        if 'pedidos' in filename:
            session['pedidos'] = df.to_dict()
            name = 'pedidos'

        elif 'clientes' in filename:
            session['clientes'] = df.to_dict()
            name = 'clientes'

        elif 'produtos' in filename:
            session['produtos'] = df.to_dict()
            name = 'produtos'

        else:
            return {
                "message": "Você deve enviar as planilhas de pedidos, clientes ou produtos"
            }, 400

        return {
            "id": name,
            "message": f"A planilha de {name} foi carregada com sucesso",
        }, 200

    def delete(self, spreadsheet_id):
        abort_if_spreadsheet_doesnt_exist(spreadsheet_id)
        del session[spreadsheet_id]
        return '', 204
