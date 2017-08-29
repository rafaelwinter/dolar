from http.client import HTTPConnection
from datetime import datetime

import json

API_HOST = "api.promasters.net.br"
PATH = "/cotacao/v1/valores"
QUERY = "moedas="

def get_value(moeda):
    request_string = "{}?{}{}".format(PATH, QUERY, moeda)
        
    try:
        connection = HTTPConnection(API_HOST)
        connection.request("GET", request_string)
        response = connection.getresponse()
    except Exception as e:
        print("Ocorreu um erro ao conectar ao servidor:", e)
        raise e

    if response.status != 200:
        print("O servidor retornou uma resposta inesperada:", response.status, response.reason)
        raise Exception("Invalid response")

    try:
        json_data = response.read()
        data = json.loads(json_data)

        if data['status'] == False:
            print("O servidor não conseguiu processar a requisição:", data['retorno'])
            raise Exception("Invalid response")
        
        cotacao = data['valores'][moeda]['valor']
        atualizacao = data['valores'][moeda]['ultima_consulta']
    except Exception as e:
        print("Ocorreu um erro ao decodificar a resposta do servidor:", e)
        raise e
    
    return (cotacao, atualizacao)

def format_date(utc_timestamp):
    d = datetime.utcfromtimestamp(utc_timestamp)
    offset = datetime.now() - datetime.utcnow()
    date = d + offset

    return date.strftime("%d/%m às %H:%M")

if __name__ == "__main__":
    try:
        cotacao, atualizacao = get_value("USD")
    except:
        print("Por favor tente novamente mais tarde.")
    else:
        print("Cotação USD: R${}\nÚltima atualização: {}".format(cotacao, format_date(atualizacao)))

