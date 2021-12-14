import pandas as pd

from flask import session
from flask_restful import reqparse, abort, Resource

from src.common.mine.clientes import *

parser = reqparse.RequestParser()
parser.add_argument('ageGroup')
parser.add_argument('gender')
parser.add_argument('registrationsOverTime')

class ClientesResource(Resource):
    def get(self):
        clientes_df = pd.DataFrame(session.get('clientes-df'))
        if clientes_df.empty:
            abort(404, message="Missing clients data")

        args = parser.parse_args()
        response = []

        if args['ageGroup']:
            response.append(faixa_etaria(clientes_df))

        if args['gender']:
            response.append(genero_predominante(clientes_df, apenasCadastrados=True))

        if args['registrationsOverTime']:
            response.append(cadastros_periodo(clientes_df))

        return { 'clientes' : response }, 200