import pandas as pd

from flask import session
from flask_restful import reqparse, abort, Resource

from src.common.mine.pedidos import *

parser = reqparse.RequestParser()
parser.add_argument('state')
parser.add_argument('city')
parser.add_argument('repeatCostumers')
parser.add_argument('incomesOverTime')
parser.add_argument('cancellationsOverTime')
parser.add_argument('paymentMethodPreference')
parser.add_argument('sendMethodPreference')

class PedidosResource(Resource):
    def get(self):
        pedidos_df = pd.DataFrame(session.get('pedidos-df'))
        if pedidos_df.empty:
            abort(404, message="Missing orders data")

        args = parser.parse_args()
        response = []

        if args['state']:
            response.append(pedidos_por_estado(pedidos_df))

        if args['city']:
            response.append(pedidos_por_cidade(pedidos_df))

        if args['repeatCostumers']:
            response.append(taxa_reincidencia(pedidos_df))

        if args['incomesOverTime']:
            response.append(faturamento_periodo(pedidos_df))

        if args['cancellationsOverTime']:
            response.append(cancelamentos_periodo(pedidos_df))

        if args['paymentMethodPreference']:
            response.append(metodo_pagamento_aprovacoes(pedidos_df))

        if args['sendMethodPreference']:
            response.append(metodo_envio_preferencia(pedidos_df))

        return { 'pedidos' : response }, 200