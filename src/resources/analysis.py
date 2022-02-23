import pandas as pd

from flask import session
from flask_restful import marshal_with, reqparse, abort, fields, Resource

from src.common.mine import get_column_data

parser = reqparse.RequestParser()
parser.add_argument('column', location='args', required=True)
parser.add_argument('somenteEntregues', location='args')
parser.add_argument('apenasCadastrados', location='args')
parser.add_argument('clientes', location='args')


response_fields = {
    'id': fields.String,
    'title': fields.String,
    'chart_type': fields.String,
    'data': fields.Raw,
}


class AnalysisResource(Resource):
    @marshal_with(response_fields)
    def get(self):
        clientes_df = pd.DataFrame(session.get('clientes'))
        pedidos_df = pd.DataFrame(session.get('pedidos'))
        produtos_df = pd.DataFrame(session.get('produtos'))

        args = parser.parse_args()

        data = get_column_data(
            clientes_df=clientes_df,
            pedidos_df=pedidos_df,
            produtos_df=produtos_df,
            column=args['column'],
            somenteEntregues=args['somenteEntregues'],
            apenasCadastrados=args['apenasCadastrados'],
            clientes=args['clientes']
        )

        return data, 200
