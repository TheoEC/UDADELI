import pandas as pd

from flask import session
from flask_restful import marshal_with, reqparse, abort, fields, Resource

from src.common.mine import get_column_data

parser = reqparse.RequestParser()
parser.add_argument('column', location='args')
parser.add_argument('somenteEntregues', location='args')
parser.add_argument('apenasCadastrados', location='args')
parser.add_argument('clientes', location='args')


response_fields = {
    'title': fields.String,
    'chart': fields.String,
    'result': fields.Raw
}


class AnalysisResource(Resource):
    @marshal_with(response_fields)
    def get(self):
        clientes_df = pd.DataFrame(session.get('clientes-df'))
        pedidos_df = pd.DataFrame(session.get('pedidos-df'))

        if clientes_df.empty and pedidos_df.empty:
            abort(404, message="Missing data")

        args = parser.parse_args()
        column = args['column']

        if column in pedidos_df.columns:
            df = pedidos_df

        elif column in clientes_df.columns:
            df = clientes_df

        else:
            abort(400, message="Invalid column")

        data = get_column_data(
            df,
            column,
            somenteEntregues=args['somenteEntregues'],
            apenasCadastrados=args['apenasCadastrados'],
            clientes=args['clientes']
        )

        return data, 200
