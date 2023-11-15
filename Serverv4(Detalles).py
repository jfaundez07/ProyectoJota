from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import json_util

#http://44.219.124.55:8081/ESTADO

Cliente = MongoClient('mongodb://localhost:27017/')
db = Cliente['Proyecto'] #Nombre base de datos
Coleccion = db['LecturasCompost'] #Nombre de la coleccion


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

#http://44.219.124.55:8081/ESTADO
@app.route("/ESTADO")
def JF_status():
    return {
        "informacion":"proyecto final",
        "servidor":"ejecutandose",
        "estado": "activo",
    }

@app.route('/POST', methods=['POST'])
def postData():
    data = request.get_json()
    data['Temperatura'] = round(data['Temperatura'], 2)
    data['Humedad'] = round(data['Humedad'], 2)
    print(data)
    db.Coleccion.insert_one(data)
    return jsonify({"message": "Informacion recibida correctamente"}), 201

#http://44.219.124.55:8081/GETLAST
@app.route('/GETLAST', methods=['GET'])
def getLastData():
    lastData =  db.Coleccion.find_one(sort=[('_id', -1)])
    if lastData:
        lastData['_id'] = str(lastData['_id'])
        print(lastData)
        return jsonify(lastData)
    else:
        return jsonify({"message": "No se encontraron datos"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)