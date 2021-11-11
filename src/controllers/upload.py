import os
import pandas as pd
from flask import request, abort
from flask_restful import Resource

from src.server.instance import server
from src.utils.mine_code import *

app, api = server.app, server.api
app.config["UPLOAD_EXTENSIONS"] = [".xlsx"]


class Upload(Resource):
    def post(self):
        files = request.files.getlist("spreadsheets")

        args = request.form

        for file in files:
            filename = file.filename

            if filename != "":
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
                    abort(400)

        df_pedidos = pd.read_excel(files[0])
        df_clientes = pd.read_excel(files[1])

        result = {}
        args = args.to_dict()
        for key in args:
            args[key] = json.loads(args[key])

        if args["address"]["state"]:
            result["Pedidos por estado"] = pedidos_por_estado(df_pedidos)

        if args["address"]["city"]:
            result["Pedidos por cidade"] = pedidos_por_cidade(df_pedidos)

        if args["repeatCostumers"]["percentage"]:
            result["Clientes reincidentes"] = taxa_reincidencia(
                df_pedidos, False)

        if args["gender"]["all"]:
            result["Gênero dos clientes"] = genero_predominante(
                df_clientes, df_pedidos)

        if args["identification"]["ageGroup"]:
            result["Faixa Etária"] = faixa_etaria(df_clientes)

        if args["identification"]["periodsWithMoreRegistrations"]:
            data = args["identification"]["date"]
            tempo = args["identification"]["frequency"]
            result["Períodos com mais cadastros"] = cadastros_periodo(
                df_clientes, dataInicial=data["from"], dataFinal=data["to"], tempo=tempo)

        if args["incomes"]["period"]:
            data = args["incomes"]["date"]
            tempo = args["incomes"]["frequency"]
            result["Faturamento por período"] = faturamento_periodo(
                df_pedidos, dataInicial=data["from"], dataFinal=data["to"], tempo=tempo)

        if args["cancellation"]["period"]:
            data = args["cancellation"]["date"]
            tempo = args["cancellation"]["frequency"]
            result["Cancelamentos por período"] = cancelamentos_periodo(
                df_pedidos, dataInicial=data["from"], dataFinal=data["to"], tempo=tempo)

        if args["preference"]["paymentMethod"]:
            result["Preferência por método de pagamento"] = metodo_pagamento_aprovacoes(
                df_pedidos)

        if args["preference"]["sendingMethod"]:
            result["Preferência por método de envio"] = metodo_envio_preferencia(
                df_pedidos)

        return result, 200


api.add_resource(Upload, "/upload")
