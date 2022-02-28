import os

from flask import current_app
from flask_restful import reqparse, Resource

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files')

ALLOWED_EXTENSIONS = ['xlsx']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class FileResource(Resource):
    def post(self):
        args = parser.parse_args()

        file = args["file"]

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                current_app.config['UPLOAD_PATH'], filename))

            if 'pedidos' in filename:
                name = 'pedidos'

            elif 'clientes' in filename:
                name = 'clientes'

            elif 'produtos' in filename:
                name = 'produtos'

            return {
                "id": filename,
                "message": f"O arquivo '{filename}' foi carregado com sucesso",
            }, 200, {'Set-Cookie': f'{name}-df={filename}'}

    def delete(self, filename):
        os.remove(os.path.join(current_app.config['UPLOAD_PATH'], filename))
        return f'A planilha de {filename} foi deletada', 204
