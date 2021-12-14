import pandas as pd

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
    planilhaClientes: pd.DataFrame, 
    planilhaPedidos: pd.DataFrame = None, 
    apenasCadastrados: bool = False, 
    somenteEntregues: bool = False
):
    '''
    RF_04 Gênero predominante
    Quantidade de clientes que fizeram um pedido
    ADICIONAR: Somente pedidos já entregues
    '''

    if apenasCadastrados:
        result = planilhaClientes[dic.genero].value_counts()

    else:
        if somenteEntregues:
            planilhaPedidos = planilhaPedidos.loc[planilhaPedidos[dic.status] == dic.entregue]
        result = planilhaClientes.loc[planilhaClientes[dic.id].isin(planilhaPedidos[dic.cliente_id])]
        result = result[dic.genero].value_counts()

    result = result.rename({
        'F': 'Mulheres',
        'M': 'Homens'
    })
    return get_response("Gênero dos clientes", "pie", result)


def faixa_etaria(planilhaClientes: pd.DataFrame, passo: int = 5):
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

    for cliente in range(len(planilhaClientes)):
        dataNascimento = planilhaClientes[dic.data_nascimento][cliente]
        idade = calcula_idade(dataNascimento)

        if idade < 122:
            pos = index[idade]
            chave = chaves[pos]

            if (chave in response) == False:
                response[chave] = 0

            response[chave] += 1

    response = dict(sorted(response.items()))
    return get_response("Faixa Etária", "bar", response)


def cadastros_periodo(
    planilhaClientes: pd.DataFrame, 
    dataInicial: str = None, 
    dataFinal: str = None, 
    tempo: str = "Meses"
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
    for cliente in range(len(planilhaClientes)):
        dataCriacao = planilhaClientes[dic.data_cadastro][cliente].split()[0]

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
