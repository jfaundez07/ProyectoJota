from flask import Flask, jsonify, request
from pymongo import MongoClient

#http://44.219.124.55:8081/status


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

@app.route("/status")
def JF_status():
    return {
        "servidor":"ejecutandose",
        "estado": "1",
    }

@app.route('/POST', methods=['POST'])
def add_persona():
    data = request.get_json()
    print()
    print(data)
    print()
    return jsonify({"message": "Informacion recibida correctamente"}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)