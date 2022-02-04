import pandas as pd

from ..dicionario import Dicionario as dic
from . import functions


def get_column_data(df: pd.DataFrame, column: str, **kwargs):
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
        dic.data_cadastro: functions.cadastros_periodo
    }

    func = switcher.get(column, lambda: "Invalid column")

    data = func(df, **kwargs)

    return data
