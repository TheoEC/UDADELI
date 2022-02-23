from flask_restful import abort
import pandas as pd

from ..dicionario import Dicionario as dic
from . import functions


def get_column_data(
    clientes_df: pd.DataFrame,
    pedidos_df: pd.DataFrame,
    produtos_df: pd.DataFrame,
    column: str,
    **kwargs
):
    switcher = {
        dic.estado_destino: functions.pedidos_por_estado,
        dic.cidade_destino: functions.pedidos_por_cidade,
        dic.destinatario: functions.taxa_reincidencia,
        dic.valor_total: functions.faturamento_periodo,
        dic.status: functions.cancelamentos_periodo,
        dic.tipo_pagamento: functions.metodo_pagamento_aprovacoes,
        dic.metodo_envio: functions.metodo_envio_preferencia,
        dic.genero: functions.genero_predominante,
        dic.data_nascimento: functions.faixa_etaria,
        dic.data_cadastro: functions.cadastros_periodo,
        'produtos': functions.produtos_mais_vendidos
    }

    func = switcher.get(column)

    if func is None:
        abort(404, message="Não existe análise para essa coluna")

    data = func(
        clientes_df=clientes_df,
        pedidos_df=pedidos_df,
        produtos_df=produtos_df,
        **kwargs
    )

    return data
