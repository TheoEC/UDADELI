import pandas as pd
import json

from src.common.dicionario import Dicionario as dic
from src.common.date import *


def get_response(titulo, tipo_grafico, dados):
    if type(dados) != dict:
        dados = dados.to_dict()

    result = []
    for key, value in dados.items():
        result.append({
            "name": key,
            "value": value
        })

    return {
        "title": titulo,
        "chart": tipo_grafico,
        "result": result
    }


def genero_predominante(
    clientes_df: pd.DataFrame,
    pedidos_df: pd.DataFrame = None,
    apenasCadastrados: bool = False,
    somenteEntregues: bool = False,
    **kwargs
):
    '''
    RF_04 Gênero predominante
    Quantidade de clientes que fizeram um pedido
    ADICIONAR: Somente pedidos já entregues
    '''

    if apenasCadastrados:
        result = clientes_df[dic.genero].value_counts()
        title = 'Gênero dos clientes cadastrados'

    else:
        title = 'Gênero dos clientes que fizeram pedidos'
        if somenteEntregues:
            title = 'Gênero dos clientes que tiveram pedidos entregues'
            pedidos_df = pedidos_df.loc[pedidos_df[dic.status]
                                        == dic.entregue]
        result = clientes_df.loc[clientes_df[dic.id].isin(
            pedidos_df[dic.cliente_id])]
        result = result[dic.genero].value_counts()

    result = result.rename({
        'F': 'Mulheres',
        'M': 'Homens'
    })
    return get_response(title, "pie", result)


def faixa_etaria(clientes_df: pd.DataFrame, passo: int = 5, **kwargs):
    '''
    RF_05 Faixa Etária OK
    '''
    index = []  # [0, 0, 0, 1, 1, 1, 2, 2, 2]
    chaves = []  # ['0-2', '3-5', '6-8']
    response = {}
    count = 0

    for i in range(0, 121, passo):
        for j in range(passo):
            index.append(count)

        count += 1
        chave = str(i)

        if passo > 1:
            chave += '-' + str(i + passo-1)

        chaves.append(chave)

    for cliente in range(len(clientes_df)):
        dataNascimento = clientes_df[dic.data_nascimento][cliente]
        idade = calcula_idade(dataNascimento)

        if idade < 100 and idade > 10:
            pos = index[idade]
            chave = chaves[pos]

            if (chave in response) == False:
                response[chave] = 0

            response[chave] += 1

    response = dict(sorted(response.items()))
    return get_response("Faixa Etária", "bar", response)


def cadastros_periodo(
    clientes_df: pd.DataFrame,
    dataInicial: str = None,
    dataFinal: str = None,
    tempo: str = "Meses",
    **kwargs
):
    '''
    RF_06 Períodos com mais cadastros em MESES
    Geral               OK
    Período definido    OK
    Meses e Anos        OK
    '''
    # dataInicial = dataInicial.split('T')[0]
    # dataFinal = dataFinal.split('T')[0]
    response = {}
    for cliente in range(len(clientes_df)):
        dataCriacao = clientes_df[dic.data_cadastro][cliente].split()[0]

        if tempo == "Meses":
            dataCriacao = dataCriacao[:7]

        elif tempo == "Anos":
            dataCriacao = dataCriacao[:4]

        if (dataInicial != None):
            if entre_datas(dataInicial, dataCriacao, dataFinal, tempo):
                if (dataCriacao in response) == False:
                    response[dataCriacao] = 0
                response[dataCriacao] += 1
        else:
            if (dataCriacao in response) == False:
                response[dataCriacao] = 0
            response[dataCriacao] += 1
    return get_response("Cadastros por período", "line", response)


def pedidos_por_estado(pedidos_df: pd.DataFrame, somenteEntregues: bool = False, **kwargs):
    '''
    RF__01 Quantidade de pedidos por estado   OK
    ADICIONAR Somente já entregues            OK
    '''
    if somenteEntregues:
        pedidos_df = pedidos_df.loc[pedidos_df[dic.status] == dic.entregue]
        title = "Quantidade de pedidos entregues por estado"
    else:
        title = "Quantidade de pedidos por estado"

    pedidos_df = pedidos_df[dic.estado_destino].value_counts()
    return get_response(title, "map", pedidos_df)


def pedidos_por_cidade(pedidos_df: pd.DataFrame, somenteEntregues: bool = False, **kwargs):
    '''
    RF__02 Quantidade de pedidos por cidade   OK
    ADICIONAR Somente já entregues            OK
    '''
    if somenteEntregues:
        pedidos_df = pedidos_df.loc[pedidos_df[dic.status] == dic.entregue]
        title = "10 cidades com mais pedidos entregues"
    else:
        title = "10 cidades com mais pedidos"

    pedidos_df = pedidos_df[dic.cidade_destino].value_counts().head(10)
    return get_response(title, "horizontalBar", pedidos_df)


def taxa_reincidencia(pedidos_df: pd.DataFrame, clientes: bool = False, **kwargs):
    ''' 
    RF_03 Reincidencia de compra
    'clientes' = False: Retorna a % de clientes que compraram mais de 1 vez.    OK
    'clientes' = True : Retorna o json de clientes que compraram mais de 1 vez. OK
    Exemplo json: {"nome" : QtdCompras}
    '''
    resultado = pedidos_df[dic.destinatario].value_counts()

    if clientes:
        return get_response("Clientes reincidentes", "table", resultado)

    else:
        novos = 0
        reincidentes = 0

        for k, v in resultado.items():
            if v == 1:
                novos += 1
            else:
                reincidentes += 1

        response = {
            "Clientes que fizeram apenas 1 compra": novos,
            "Clientes que voltaram a comprar": reincidentes,
        }

    return get_response("Taxa de reincidência", "pie", response)


def faturamento_periodo(
    pedidos_df: pd.DataFrame,
    tempo: str = 'Meses',
    dataInicial: str = None,
    dataFinal: str = None,
    **kwargs
):
    '''
    RF_07 Faturamento por período
    Por ano     OK
    Por mês     OK
    Por dias    OK
    Truncar     FAZER
    '''
    response = {}
    # dataInicial = dataInicial.split('T')[0]
    # dataFinal = dataFinal.split('T')[0]
    for pedido in range(len(pedidos_df)):
        status = pedidos_df[dic.status][pedido]

        if status == dic.entregue or status == "Pedido Enviado":
            data = pedidos_df[dic.data_criacao][pedido].split(' ')[0]

            chave = ''
            if (tempo == 'Dias'):
                chave = data

            elif tempo == 'Meses':
                chave = data[:7]    # YYYY-MM

            elif tempo == 'Anos':
                chave = data[:4]

            valorPedido = float(pedidos_df[dic.valor_total][pedido])

            if(dataInicial != None):
                if entre_datas(dataInicial, chave, dataFinal, tempo):
                    if (chave in response.keys()) == False:
                        response[chave] = 0

                    response[chave] += valorPedido

            else:
                if (chave in response.keys()) == False:
                    response[chave] = 0

                response[chave] += valorPedido

    return get_response("Faturamento por período", "line", response)


'''
RF_08 
'''


def cancelamentos_periodo(
    pedidos_df: pd.DataFrame,
    dataInicial: str = None,
    dataFinal: str = None,
    tempo: str = "Meses",
    **kwargs
):
    '''
    RF_09 Cancelamento por período
    '''
    # dataInicial = dataInicial.split('T')[0]
    # dataFinal = dataFinal.split('T')[0]
    response = {}
    for pedido in range(len(pedidos_df)):
        dataCriacao = pedidos_df[dic.data_criacao][pedido].split()[0]

        if tempo == "Meses":
            dataCriacao = dataCriacao[:7]
        elif tempo == "Anos":
            dataCriacao = dataCriacao[:4]

        status = pedidos_df[dic.status][pedido]
        if status == dic.cancelado:
            if (dataInicial != None):
                if entre_datas(dataInicial, dataCriacao, dataFinal, tempo):
                    if (dataCriacao in response) == False:
                        response[dataCriacao] = 0
                    response[dataCriacao] += 1
            else:
                if (dataCriacao in response) == False:
                    response[dataCriacao] = 0
                response[dataCriacao] += 1
    return get_response("Cancelamentos por período", "line", response)


def metodo_pagamento_aprovacoes(pedidos_df: pd.DataFrame, **kwargs):
    '''
    RF__10 Taxa de cancelamento por método de pagamento
    RF__11 Preferência por método de pegamento
    '''
    infoPagamentos = pedidos_df[dic.tipo_pagamento].value_counts()
    # infoPagamentos = {}

    # for tipo in meiosPagamento:
    #     qtdUsos = len(dados.loc[dados[dic.tipo_pagamento] == tipo])
    #     qtdAprovados = len(dados.loc[(dados[dic.tipo_pagamento] == tipo) & (
    #         dados[dic.status] == dic.entregue)])

    #     infoPagamentos[tipo] = [qtdUsos, qtdAprovados]

    return get_response("Preferência por método de pagamento", "pie", infoPagamentos)


def metodo_envio_preferencia(pedidos_df: pd.DataFrame, **kwargs):
    '''
    RF_12 Preferencia pelos meios de envio
    Total   
    Melhoria: Por período FAZER
    '''
    response = {}

    pedidos_df = pedidos_df.loc[pedidos_df[dic.status]
                                == dic.entregue]
    pedidos_df = pedidos_df[dic.metodo_envio].value_counts()
    return get_response("Preferência por método de envio", "pie", pedidos_df)


def produtos_mais_vendidos(pedidos_df: pd.DataFrame, produtos_df: pd.DataFrame, **kwargs):
    df = pedidos_df
    pedido_itens = pedidos_df['pedido-itens'].apply(json.loads)

    df1 = (pd.concat({k: pd.DataFrame(v)
           for k, v in pedido_itens.items()}).reset_index(level=1, drop=True))

    vendas = df1['produto_id']
    produtos = produtos_df[['id', 'nome']]

    result = produtos.merge(vendas, left_on='id', right_on='produto_id')
    result = result['nome'].value_counts().head(10)

    return get_response("Produtos mais vendidos", "horizontalBar", result)
