import json


def series_to_json(dados):
    result = dados.to_json(orient="columns", force_ascii=False)
    parsed = json.loads(result)

    return parsed


def dict_to_json(dicionario):
    '''Converte um dicionário para json, usar quando o dic estiver ainda vazio'''
    response = json.dumps(dicionario, sort_keys=False, indent=4)
    response = json.loads(response)

    return response


def jsonPrint(json):
    print("{")
    for dado in json.keys():
        print("    \"" + str(dado) + "\"" + ":", json[dado])
    print("}")
