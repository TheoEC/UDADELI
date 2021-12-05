import pandas as pd
from flask import request, session
from flask_restful import Resource

from src.common.mine_code import *

class Data(Resource):
	def get(self):
		args = request.json
		pedidos_df = pd.DataFrame(session.get('pedidos-df'))
		clientes_df = pd.DataFrame(session.get('clientes-df'))

		accepted_analysis = {
			'state': lambda: pedidos_por_estado(pedidos_df),
			'city': lambda: pedidos_por_cidade(pedidos_df),
			'repeatCostumers': lambda: taxa_reincidencia(pedidos_df),
			'gender': lambda: genero_predominante(clientes_df, pedidos_df),
			'ageGroup': lambda: faixa_etaria(clientes_df),
			'registrationByPeriod': lambda: cadastros_periodo(clientes_df),
			'incomesByPeriod': lambda: faturamento_periodo(pedidos_df),
			'cancellationsByPeriod': lambda: cancelamentos_periodo(pedidos_df),
			'paymentMethodPreference': lambda: metodo_pagamento_aprovacoes(pedidos_df),
			'sendingMethodPreference': lambda: metodo_envio_preferencia(pedidos_df)
		}

		if args and not pedidos_df.empty:
			response = { "dataAnalysis": [] }
			
			for arg in args.get('query'):
				analysis = accepted_analysis.get(arg)
				if analysis:
					response["dataAnalysis"].append(analysis())

			return response, 200
		return { "message": "No data uploaded" }, 404