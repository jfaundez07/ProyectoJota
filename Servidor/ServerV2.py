from flask import Flask, jsonify, request
from pymongo import MongoClient



Cliente = MongoClient('mongodb://localhost:27017/')
db = Cliente['Proyecto'] #Nombre base de datos
Coleccion = db['LecturasCompost'] #Nombre de la coleccion


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

@app.route("/ESTADO")
def JF_status():
    return {
        "informacion":"proyecto final",
        "servidor":"ejecutandose",
        "estado": "activo",
    }

@app.route('/POST', methods=['POST'])
def add_persona():
    data = request.get_json()
    print(data)
    db.Coleccion.insert_one(data)
    return jsonify({"message": "Informacion recibida correctamente"}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)