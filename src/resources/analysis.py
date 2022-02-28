from flask_restful import marshal_with, reqparse, fields, Resource

from src.common.mine import get_column_data
from src.utils.read_excel import read_excel

parser = reqparse.RequestParser()

parser.add_argument('column', location='args', required=True)
parser.add_argument('somenteEntregues', location='args')
parser.add_argument('apenasCadastrados', location='args')
parser.add_argument('clientes', location='args')

parser.add_argument('pedidos-df', location='cookies')
parser.add_argument('clientes-df', location='cookies')
parser.add_argument('produtos-df', location='cookies')


response_fields = {
    'id': fields.String,
    'title': fields.String,
    'chart_type': fields.String,
    'data': fields.Raw,
}


class AnalysisResource(Resource):
    @marshal_with(response_fields)
    def get(self):
        args = parser.parse_args()

        data = get_column_data(
            clientes_df=read_excel(args['clientes-df']),
            pedidos_df=read_excel(args['pedidos-df']),
            produtos_df=read_excel(args['produtos-df']),
            column=args['column'],
            somenteEntregues=args['somenteEntregues'],
            apenasCadastrados=args['apenasCadastrados'],
            clientes=args['clientes']
        )

        return data, 200
