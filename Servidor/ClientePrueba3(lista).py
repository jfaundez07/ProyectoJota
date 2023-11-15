import requests

def getLastTen():
    response = requests.get("http://44.219.124.55:8081/GETLASTTEN")
    data = response.json()
    return data

def printData(data):
    print("Temperatura: " + str(data['Temperatura']) + "°C")
    print("Humedad: " + str(data['Humedad']) + "%")
    print("PM2.5: " + str(data['PM25']) + "ug/m3")
    print("PM10: " + str(data['PM10']) + "ug/m3")
    print("#-----------------------------------------------------#")

ListaJson = getLastTen()

def recorreListaPretty(ListaJsons):
    print("Tipo de arreglo: ")
    print(type(ListaJson))
    print("Tamaño del arreglo: ")
    print(str(len(ListaJson)) + "\n")

    for data in ListaJson:
        print(ListaJson.index(data) + 1)
        printData(data)
    
def recorrerLista(ListaJson):
    for data in ListaJson:
        print(data)
        print("Tipo de dato: " + str(type(data)))
        print("\n")

#recorreListaPretty(ListaJson)
recorrerLista(ListaJson)