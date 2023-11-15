import requests

jsonPrueba = {
    '_id': 1,
    'descp': 'pruebaServidor, avance 1 proyecto',
    'fecha': '15-11-2023'
    }

def post(jsonData):
    response = requests.post("http://44.219.124.55:8081/POST", json=jsonData)
    if response.status_code == 201:
        print("Informacion enviada correctamente")
    else:
        print("Error al enviar la informacion")
                             
print("Enviando informacion al servidor...")
post(jsonPrueba)