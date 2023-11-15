import requests

def getLastData():
    response = requests.get("http://44.219.124.55:8081/GETLAST")
    data = response.json()
    if response.status_code == 200:
        print("\nInformacion recibida correctamente")
        printData(data)
    else:
        print("Error al recibir la informacion")

def printData(data):
    print("\nTemperatura: " + str(data['Temperatura']) + "°C")
    print("Humedad: " + str(data['Humedad']) + "%")
    print("PM2.5: " + str(data['PM25']) + "ug/m3")
    print("PM10: " + str(data['PM10']) + "ug/m3\n")
        
while(True):

    seleccion = str(input("1. Recibir informacion\n2. Salir\nOpcion: "))
    if seleccion == "1":
        getLastData()
    elif seleccion == "2":
        break
    else:
        print("Opcion no valida")