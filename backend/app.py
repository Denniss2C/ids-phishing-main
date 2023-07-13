from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
from feature_extraction_DeAd import website
import os
import shutil
#importamos el modelo de ML ya entrenado

modelRF = joblib.load('/Users/denniscaisa/Desktop/DENNIS/TITULACION/Codigo DA/ids-phishing-main/backend/randomForest-DA-Legitime.sav')

app = Flask(__name__)
CORS(app)

@app.route("/")
def raiz():
    return jsonify({"mensaje":"Bienvenido, ingresa a la ruta predict para empezar la predicción"})

@app.route("/predict", methods=["GET","POST"])
def predict():

    respuesta = request.json
    if respuesta:
        print("URL recibida:", respuesta) # mensaje de depuración
        x = website(respuesta["url"])
        x.getFeatures()
        prediction=modelRF.predict([x.features])
        print(x.features)
        return jsonify({"result":int(prediction[0])})
    else:
        return jsonify({"error":"Es necesario el parámetro url"})

if __name__=="main_":
    app.run(debug=True)