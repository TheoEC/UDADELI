from datetime import datetime as dt


def converte_data(data):
    data = data.split()[1:4]
    data = "/".join(data)
    data = dt.strptime(data, "%b/%d/%Y")
    return data.strftime("%Y-%m-%d")


def calcula_idade(dataNascimento):
    dataNascimento = dataNascimento.replace('/', '-')
    dataNascimento = dt.strptime(dataNascimento, "%Y-%m-%d")
    agora = dt.today()
    idade = agora - dataNascimento
    return (idade.days // 365)


def entre_datas(dataInicio, dataVerificar, dataLimite=None, tempo='Dias'):
    '''
    Verifica se uma data está entre outras duas datas.
    OBS: Também são consideradas as datas de inicio e fim.
    Return: Boolean.
    '''
    if tempo == 'Meses':
        dataInicio = dataInicio[:7]    # YYYY-MM
        dataLimite = dataLimite[:7]
        dataVerificar = dataVerificar[:7]

    elif tempo == 'Anos':
        dataInicio = dataInicio[:4]  # YYYY
        dataLimite = dataLimite[:4]
        dataVerificar = dataVerificar[:4]

    dataVerificar = dataVerificar.replace('/', '-')
    dataInicio = dataInicio.replace('/', '-')

    response = False
    if (dataLimite == None):
        if(tempo == 'Dias'):
            inicio = dt.strptime(dataInicio,    "%Y-%m-%d")
            verificar = dt.strptime(dataVerificar, "%Y-%m-%d")
            response = (inicio <= verificar)
        elif(tempo == 'Meses'):
            inicio = dt.strptime(dataInicio,    "%Y-%m")
            verificar = dt.strptime(dataVerificar, "%Y-%m")
            response = (inicio <= verificar)
        elif tempo == 'Anos':
            inicio = dt.strptime(dataInicio,    "%Y")
            verificar = dt.strptime(dataVerificar, "%Y")
            response = (inicio <= verificar)

    else:
        if tempo == 'Dias':
            dataLimite = dataLimite.replace('/', '-')
            inicio = dt.strptime(dataInicio,    "%Y-%m-%d")
            verificar = dt.strptime(dataVerificar, "%Y-%m-%d")
            limite = dt.strptime(dataLimite,    "%Y-%m-%d")
            response = (inicio <= verificar) and (verificar <= limite)
        elif tempo == 'Meses':
            dataLimite = dataLimite.replace('/', '-')
            inicio = dt.strptime(dataInicio,    "%Y-%m")
            verificar = dt.strptime(dataVerificar, "%Y-%m")
            limite = dt.strptime(dataLimite,    "%Y-%m")
            response = (inicio <= verificar) and (verificar <= limite)
        elif tempo == 'Anos':
            inicio = dt.strptime(dataInicio,    "%Y")
            verificar = dt.strptime(dataVerificar, "%Y")
            limite = dt.strptime(dataLimite,    "%Y")
            response = (inicio <= verificar) and (verificar <= limite)

    return response
